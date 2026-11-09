#!/usr/bin/env python3
"""Offline, read-only lint for a Knowledge_Wiki Vault.

Usage:
    python3 _system/lint.py [--root PATH] [--no-hash] [--strict] [--verbose] [--json]

The script implements the mechanically decidable part of WORKFLOW section 11.
It never writes, repairs, or contacts Zotero. It needs only the Python
standard library (3.8+). An agent without Python performs the same checks by
hand; the protocol does not depend on this file being runnable.

Severity:
    ERROR  a protocol invariant from SCHEMA/WORKFLOW is violated.
    WARN   report-only; needs agent or human judgment.
    INFO   statistics that support maintenance decisions (--verbose lists items).

Not covered (still an agent task): unsourced numbers or quotations, possible
duplicate pages, scientific conflict, and every live Zotero check (attachment
availability, current bytes, live collection membership).

Exit status: 0 when there is no ERROR (and, with --strict, no WARN); 1 otherwise;
2 when the Vault root cannot be read.
"""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

PAGE_DIRS = {
    "wiki/sources": "source",
    "wiki/concepts": "concept",
    "wiki/entities": "entity",
    "wiki/questions": "question",
    "wiki/syntheses": "synthesis",
}
REQUIRED_KEYS = [
    "title", "type", "summary", "aliases", "tags", "sources",
    "status", "needs_review", "created", "updated",
]
LIST_KEYS = ["aliases", "tags", "sources", "source_refs"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
EXT_KEY_RE = re.compile(r"^zotero:user:(\d+):([A-Z0-9]{8}):([0-9a-f]{64})$")
ITEM_KEY_RE = re.compile(r"^zotero:user:(\d+):([A-Z0-9]{8})$")
LOCAL_PATH_RE = re.compile(
    r"/Users/[^/\s\"']+/|/home/[^/\s\"']+/|[A-Za-z]:\\\\?Users\\|file://|Zotero/storage/[A-Z0-9]{8}"
)
EXTERNAL_FIELDS = [
    "provider", "library", "item_key", "attachment_key", "title", "canonical_id",
    "source_url", "paper_version", "content_hash", "open_uri", "captured_at",
    "ingested_at", "ingest_status", "disposition", "duplicate_of", "pages_created",
    "pages_updated", "coverage", "annotations",
]
SOURCE_FIELDS = [
    "source_url", "canonical_id", "content_hash", "captured_at", "ingested_at",
    "disposition", "pages_created", "pages_updated",
]
ITEM_FIELDS = [
    "source_refs", "classification_status", "rules_revision", "memberships_before",
    "planned_add", "planned_remove", "memberships_after", "inbox_status", "reason",
    "updated_at",
]
VALID_DQ_ESCAPES = set('0abtnvfre "/\\N_LPxuU\t')
SUMMARY_SOFT_LIMIT = 300

TITLES = {
    "E-FM": "Frontmatter missing, malformed, or violating SCHEMA section 3",
    "E-NAME": "Basename not unique across wiki/",
    "E-LINK": "Wikilink does not resolve",
    "E-FOOTNOTE": "Footnote reference without a definition",
    "E-TWOWAY": "Concept/Entity links a Source that does not link back",
    "E-REF": "Page evidence pointer does not resolve",
    "E-INDEX": "index.md out of sync with wiki pages",
    "E-MANIFEST": "manifest.json record violates SCHEMA section 11 / WORKFLOW section 12",
    "E-RAWHASH": "Raw file bytes differ from the registered hash",
    "E-LOCALPATH": "Machine-local path persisted in durable state",
    "W-ANCHOR": "Wikilink heading anchor not found in the target file",
    "W-FOOTNOTE": "Footnote definition never referenced",
    "W-RAW": "Raw file or page source not registered in the manifest",
    "W-DUPHASH": "Same content hash registered more than once without duplicate_of",
    "W-REVIEW": "Page flagged needs_review",
    "W-EVIDENCE": "evidence_basis may be stale or page has no registered evidence",
    "W-PENDING": "Unfinished ingest, annotation, or classification stage",
    "W-SCOPE": "Planned collection change outside the configured managed tree",
    "W-INDEX": "index.md entry needs attention",
    "I-SUMMARY": "Summaries longer than %d characters" % SUMMARY_SOFT_LIMIT,
    "I-ORPHAN": "Non-Source pages with no inbound Wiki link",
    "I-LOCATOR": "Concept/Entity pages with no original-evidence locator in the body",
}


def nfc(s):
    return unicodedata.normalize("NFC", s)


class Lint:
    def __init__(self, root, check_hash=True):
        self.root = root
        self.check_hash = check_hash
        self.findings = []  # (severity, code, where, message)
        self.files = {}     # NFC posix relative path -> Path
        self.meta = {}      # page -> frontmatter dict
        self.body = {}      # page -> body text
        self.pages = []     # ordinary knowledge pages
        self.stats = {}

    def add(self, code, where, message):
        sev = {"E": "ERROR", "W": "WARN", "I": "INFO"}[code[0]]
        self.findings.append((sev, code, where, message))

    # ---------- file system ----------

    def scan(self):
        for top in ("wiki", "raw", "_system", "inbox", "assets"):
            base = self.root / top
            if not base.is_dir():
                continue
            for p in base.rglob("*"):
                if p.is_file():
                    self.files[nfc(p.relative_to(self.root).as_posix())] = p
        for p in self.root.iterdir():
            if p.is_file():
                self.files[nfc(p.name)] = p

    def read(self, rel):
        return self.files[rel].read_text(encoding="utf-8", errors="replace")

    # ---------- frontmatter ----------

    @staticmethod
    def _dq(s, problems):
        out, i = [], 1
        while i < len(s):
            c = s[i]
            if c == "\\":
                if i + 1 >= len(s):
                    problems.append("dangling backslash in double-quoted scalar")
                    break
                n = s[i + 1]
                if n not in VALID_DQ_ESCAPES:
                    problems.append("invalid escape \\%s in double-quoted scalar" % n)
                out.append(n)
                i += 2
                continue
            if c == '"':
                rest = s[i + 1:].strip()
                if rest and not rest.startswith("#"):
                    problems.append("text after closing quote: %r" % rest[:30])
                return "".join(out)
            out.append(c)
            i += 1
        problems.append("unterminated double-quoted scalar")
        return "".join(out)

    @classmethod
    def _scalar(cls, raw, problems):
        v = raw.strip()
        if v == "" or v in ("~", "null"):
            return None
        if v.startswith('"'):
            return cls._dq(v, problems)
        if v.startswith("'"):
            m = re.match(r"^'((?:[^']|'')*)'\s*(#.*)?$", v)
            if not m:
                problems.append("malformed single-quoted scalar")
                return v
            return m.group(1).replace("''", "'")
        if v.startswith("["):
            if not v.endswith("]"):
                problems.append("unterminated flow list")
                return []
            inner, items, cur, quote = v[1:-1], [], "", None
            for ch in inner:
                if quote:
                    cur += ch
                    if ch == quote and not cur.endswith("\\" + quote):
                        quote = None
                elif ch in "\"'":
                    quote = ch
                    cur += ch
                elif ch == ",":
                    items.append(cur)
                    cur = ""
                else:
                    cur += ch
            if cur.strip():
                items.append(cur)
            return [cls._scalar(x, problems) for x in items if x.strip()]
        v = re.sub(r"\s+#.*$", "", v)
        if v in ("true", "True"):
            return True
        if v in ("false", "False"):
            return False
        return v

    def parse_frontmatter(self, text):
        problems = []
        text = text.lstrip("\ufeff").replace("\r\n", "\n")
        if not text.startswith("---\n"):
            return None, text, ["no frontmatter block"]
        end = text.find("\n---\n", 3)
        if end < 0:
            if text.rstrip().endswith("\n---"):
                end = text.rstrip().rfind("\n---")
            else:
                return None, text, ["frontmatter block is not closed"]
        block, body = text[4:end], text[end + 5:]
        data, key, mode = {}, None, None
        for line in block.split("\n"):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s+(.*)|\s*)$", line)
            if m and not line[0].isspace():
                key, val = m.group(1), (m.group(2) or "").strip()
                if key in data:
                    problems.append("duplicate key %s" % key)
                if val in ("|", ">", "|-", ">-", "|+", ">+"):
                    data[key], mode = "", "block"
                elif val == "":
                    data[key], mode = None, "open"
                else:
                    data[key], mode = self._scalar(val, problems), "done"
                continue
            if key is None:
                problems.append("unparsed line: %r" % line[:40])
                continue
            item = re.match(r"^\s*-(?:\s+(.*))?$", line)
            if item and mode in ("open", "list"):
                if not isinstance(data[key], list):
                    data[key] = []
                data[key].append(self._scalar(item.group(1) or "", problems))
                mode = "list"
            elif line[0].isspace() and mode == "block":
                data[key] = (data[key] + " " + line.strip()).strip()
            elif line[0].isspace() and mode in ("done", "open") and not isinstance(data[key], (list, bool)):
                data[key] = ((data[key] or "") + " " + line.strip()).strip()
            else:
                problems.append("unparsed line: %r" % line[:40])
        return data, body, problems

    def load_pages(self):
        for rel in sorted(self.files):
            if not (rel.startswith("wiki/") and rel.endswith(".md")):
                continue
            fm, body, problems = self.parse_frontmatter(self.read(rel))
            self.body[rel] = body
            if rel == "wiki/Home.md":
                self.meta[rel] = fm or {}
                continue
            self.pages.append(rel)
            self.meta[rel] = fm or {}
            for p in problems:
                self.add("E-FM", rel, p)
            if fm is not None:
                self.check_frontmatter(rel, fm)

    def check_frontmatter(self, rel, fm):
        for k in REQUIRED_KEYS:
            if k not in fm:
                self.add("E-FM", rel, "missing required key %s" % k)
        expected = PAGE_DIRS.get(rel.rsplit("/", 1)[0])
        if expected is None:
            self.add("E-FM", rel, "page is outside the five type directories")
        elif fm.get("type") != expected:
            self.add("E-FM", rel, "type %r does not match directory (%s)" % (fm.get("type"), expected))
        if "status" in fm and fm["status"] not in ("active", "archived"):
            self.add("E-FM", rel, "status %r is not active|archived" % fm["status"])
        if "needs_review" in fm and not isinstance(fm["needs_review"], bool):
            self.add("E-FM", rel, "needs_review %r is not a boolean" % fm["needs_review"])
        for k in ("created", "updated"):
            if k in fm and not DATE_RE.match(str(fm[k])):
                self.add("E-FM", rel, "%s %r is not YYYY-MM-DD" % (k, fm[k]))
        if DATE_RE.match(str(fm.get("created", ""))) and DATE_RE.match(str(fm.get("updated", ""))):
            if str(fm["updated"]) < str(fm["created"]):
                self.add("E-FM", rel, "updated is earlier than created")
        for k in ("title", "summary"):
            if k in fm and not (isinstance(fm[k], str) and fm[k].strip()):
                self.add("E-FM", rel, "%s is empty" % k)
        for k in LIST_KEYS:
            if k in fm and fm[k] is not None and not isinstance(fm[k], list):
                self.add("E-FM", rel, "%s is not a list" % k)
        if "evidence_basis" in fm:
            if fm["evidence_basis"] != "single-source":
                self.add("E-FM", rel, "evidence_basis %r is not single-source" % fm["evidence_basis"])
            elif fm.get("type") not in ("concept", "entity"):
                self.add("E-FM", rel, "evidence_basis is defined only for Concept and Entity pages")
        if "question_status" in fm and fm["question_status"] not in ("open", "provisional", "answered", "closed"):
            self.add("E-FM", rel, "question_status %r is not a defined value" % fm["question_status"])

    def lst(self, rel, key):
        v = self.meta.get(rel, {}).get(key)
        return [str(x) for x in v] if isinstance(v, list) else []

    # ---------- links and footnotes ----------

    @staticmethod
    def strip_code(text):
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        return re.sub(r"`[^`\n]*`", "", text)

    @staticmethod
    def norm_heading(s):
        s = re.sub(r"[#|^:\[\]]|%%", " ", nfc(s))
        return re.sub(r"\s+", " ", s).strip().casefold()

    def headings(self, rel, cache={}):
        if rel not in cache:
            cache[rel] = {
                self.norm_heading(m.group(1))
                for m in re.finditer(r"^#{1,6}\s+(.*?)\s*#*\s*$", self.read(rel), re.M)
            }
        return cache[rel]

    def resolve(self, target, stems):
        t = nfc(target).strip()
        if not t:
            return "", None
        for cand in (t, t + ".md"):
            if cand in self.files:
                return cand, None
        if "/" not in t:
            hits = stems.get(t[:-3] if t.endswith(".md") else t, [])
            if len(hits) == 1:
                return hits[0], None
            if len(hits) > 1:
                return None, "ambiguous basename (%d candidates)" % len(hits)
        return None, "target not found"

    def check_links(self):
        stems = defaultdict(list)
        for rel in self.files:
            if rel.endswith(".md"):
                stems[rel.rsplit("/", 1)[-1][:-3]].append(rel)
        wiki_stems = Counter(r.rsplit("/", 1)[-1] for r in self.files if r.startswith("wiki/") and r.endswith(".md"))
        for name, n in sorted(wiki_stems.items()):
            if n > 1:
                self.add("E-NAME", name, "%d pages share this basename" % n)

        self.out = defaultdict(set)
        self.inn = defaultdict(set)
        for rel in ["wiki/Home.md"] + self.pages:
            if rel not in self.body:
                continue
            text = self.strip_code(self.body[rel])
            for m in re.finditer(r"\[\[([^\[\]]+?)\]\]", text):
                raw = m.group(1)
                target = re.split(r"\\?\|", raw, maxsplit=1)[0]
                path, _, anchor = target.partition("#")
                hit, why = self.resolve(path, stems)
                if hit is None:
                    self.add("E-LINK", rel, "[[%s]] — %s" % (raw[:120], why))
                    continue
                if hit == "":
                    hit = rel
                if anchor and not anchor.startswith("^") and hit.endswith(".md"):
                    if self.norm_heading(anchor) not in self.headings(hit):
                        self.add("W-ANCHOR", rel, "[[%s]]" % raw[:120])
                if hit != rel and hit.startswith("wiki/") and hit.endswith(".md"):
                    self.out[rel].add(hit)
                    self.inn[hit].add(rel)

            refs = set(re.findall(r"\[\^([^\]\s]+)\](?!:)", text))
            defs = set(re.findall(r"^\[\^([^\]\s]+)\]:", text, re.M))
            for r in sorted(refs - defs):
                self.add("E-FOOTNOTE", rel, "[^%s] has no definition" % r)
            for d in sorted(defs - refs):
                self.add("W-FOOTNOTE", rel, "[^%s] is defined but never referenced" % d)

        for rel in self.pages:
            if self.meta[rel].get("type") not in ("concept", "entity"):
                continue
            for tgt in sorted(self.out[rel]):
                if self.meta.get(tgt, {}).get("type") == "source" and rel not in self.out[tgt]:
                    self.add("E-TWOWAY", rel, "-> %s" % tgt)

    # ---------- index ----------

    def check_index(self):
        if "_system/index.md" not in self.files:
            self.add("E-INDEX", "_system/index.md", "file is missing")
            return
        text = self.read("_system/index.md")
        entries = {}
        for line in text.splitlines():
            m = re.match(r"^- \[\[([^\]]+)\]\]\s*—\s*(.*)$", line)
            if not m:
                continue
            rel = nfc(m.group(1).split("|")[0].strip())
            rel = rel if rel.endswith(".md") else rel + ".md"
            if rel in entries:
                self.add("E-INDEX", rel, "listed more than once")
            d = re.search(r"updated (\d{4}-\d{2}-\d{2})\s*$", m.group(2))
            entries[rel] = d.group(1) if d else None
        for rel in self.pages:
            if rel not in entries:
                self.add("E-INDEX", rel, "page is missing from the index")
            elif entries[rel] is None:
                self.add("W-INDEX", rel, "index entry has no trailing 'updated YYYY-MM-DD'")
            elif entries[rel] != str(self.meta[rel].get("updated")):
                self.add("E-INDEX", rel, "index date %s != page updated %s" % (entries[rel], self.meta[rel].get("updated")))
        for rel in entries:
            if rel not in self.files:
                self.add("E-INDEX", rel, "index entry has no page")
        m = re.search(r"^Knowledge pages:\s*(\d+)", text, re.M)
        if m and int(m.group(1)) != len(self.pages):
            self.add("E-INDEX", "_system/index.md", "declares %s knowledge pages, found %d" % (m.group(1), len(self.pages)))

    # ---------- manifest ----------

    def collection_config(self):
        rel = "_system/zotero-collections.md"
        if rel not in self.files:
            return None
        text = self.read(rel)
        inbox, protected, keyed = set(), set(), set()
        # Bullet form: "- Inbox: `KEY` — 00 Inbox", "- Protected Projects root: `KEY` — ..."
        for label, key in re.findall(r"^- ([^:\n`]+):\s*`([A-Z0-9]{8})`", text, re.M):
            if label.strip().lower() == "inbox":
                inbox.add(key)
            elif label.strip().lower().startswith("protected"):
                protected.add(key)
        # Table form: "| Inbox | KEY | 00 Inbox |" (role tables) or "| Name | KEY | PARENT | ... |" (managed tree)
        for label, key in re.findall(r"^\|\s*([^|\n]*?)\s*\|\s*([A-Z0-9]{8})\s*\|", text, re.M):
            low = label.lower()
            if low == "inbox":
                inbox.add(key)
            elif low.startswith("protected"):
                protected.add(key)
            else:
                keyed.add(key)
        managed = keyed - inbox - protected
        if not managed and not inbox:
            return None
        return {"managed": managed, "inbox": inbox, "protected": protected}

    def check_manifest(self):
        rel = "_system/manifest.json"
        if rel not in self.files:
            self.add("E-MANIFEST", rel, "file is missing")
            self.S, self.E, self.Z = {}, {}, {}
            return
        try:
            M = json.loads(self.read(rel))
        except ValueError as e:
            self.add("E-MANIFEST", rel, "invalid JSON: %s" % e)
            self.S, self.E, self.Z = {}, {}, {}
            return
        if M.get("version") not in (1, 2):
            self.add("E-MANIFEST", rel, "version %r is not 1 or 2" % M.get("version"))
        S = self.S = M.get("sources") or {}
        E = self.E = M.get("external_sources") or {}
        Z = self.Z = M.get("zotero_items") or {}
        if LOCAL_PATH_RE.search(self.read(rel)):
            self.add("E-LOCALPATH", rel, "contains a machine-local path")

        def date_ok(v, nullable=False):
            return (v is None and nullable) or (isinstance(v, str) and bool(DATE_RE.match(v)))

        def missing(key, rec, fields):
            gone = [f for f in fields if f not in rec]
            if gone:
                self.add("E-MANIFEST", key, "missing field(s): %s" % ", ".join(gone))

        def pages_ok(key, rec):
            for field in ("pages_created", "pages_updated"):
                for p in rec.get(field) or []:
                    if nfc(p) not in self.files:
                        self.add("E-MANIFEST", key, "%s points to a missing page: %s" % (field, p))

        def completed(key):
            if key in S:
                return S[key].get("ingested_at") is not None
            return key in E and E[key].get("ingest_status") == "complete"

        def dup_ok(key, rec):
            tgt = rec.get("duplicate_of")
            if not tgt:
                return
            seen, cur = {key}, tgt
            while cur:
                if cur in seen:
                    self.add("E-MANIFEST", key, "duplicate_of forms a cycle or self-reference")
                    return
                seen.add(cur)
                nxt = S.get(cur) or E.get(cur)
                if nxt is None:
                    self.add("E-MANIFEST", key, "duplicate_of target is not registered: %s" % cur)
                    return
                cur = nxt.get("duplicate_of")
            target = S.get(tgt) or E.get(tgt)
            if target.get("content_hash") != rec.get("content_hash"):
                self.add("E-MANIFEST", key, "duplicate_of target has a different content_hash")
            if not completed(tgt):
                self.add("E-MANIFEST", key, "duplicate_of target is not a completed record")

        # Vault raw records
        for key, rec in S.items():
            missing(key, rec, SOURCE_FIELDS)
            if nfc(key) not in self.files:
                self.add("E-MANIFEST", key, "registered raw file is missing on disk")
            elif self.check_hash and HASH_RE.match(str(rec.get("content_hash"))):
                actual = "sha256:" + hashlib.sha256(self.files[nfc(key)].read_bytes()).hexdigest()
                if actual != rec["content_hash"]:
                    self.add("E-RAWHASH", key, "registered %s…, actual %s…" % (rec["content_hash"][:19], actual[:19]))
            if not HASH_RE.match(str(rec.get("content_hash"))):
                self.add("E-MANIFEST", key, "content_hash is not sha256:<64 hex>")
            if rec.get("disposition") not in ("new", "update", "disputed", "no_material", "duplicate", None):
                self.add("E-MANIFEST", key, "disposition %r is not a defined value" % rec.get("disposition"))
            if not date_ok(rec.get("captured_at")) or not date_ok(rec.get("ingested_at"), True):
                self.add("E-MANIFEST", key, "captured_at/ingested_at is not YYYY-MM-DD")
            if rec.get("ingested_at") is None:
                self.add("W-PENDING", key, "raw record has no ingested_at")
            pages_ok(key, rec)
            dup_ok(key, rec)
            if rec.get("snapshot_kind") is not None:
                if rec["snapshot_kind"] != "zotero_annotations":
                    self.add("E-MANIFEST", key, "snapshot_kind %r is not zotero_annotations" % rec["snapshot_kind"])
                if rec.get("source_ref") not in E:
                    self.add("E-MANIFEST", key, "snapshot source_ref is not a registered external source")
                if not HASH_RE.match(str(rec.get("payload_hash"))):
                    self.add("E-MANIFEST", key, "snapshot payload_hash is not sha256:<64 hex>")

        # External (Zotero) records
        for key, rec in E.items():
            m = EXT_KEY_RE.match(key)
            if not m:
                self.add("E-MANIFEST", key, "key is not zotero:user:<id>:<attachment>:<sha256>")
            missing(key, rec, EXTERNAL_FIELDS)
            if m:
                uid, att, digest = m.groups()
                if rec.get("content_hash") != "sha256:" + digest:
                    self.add("E-MANIFEST", key, "content_hash does not match the key digest")
                if rec.get("attachment_key") != att:
                    self.add("E-MANIFEST", key, "attachment_key does not match the key")
                if str((rec.get("library") or {}).get("id")) != uid:
                    self.add("E-MANIFEST", key, "library.id does not match the key")
                if rec.get("open_uri") != "zotero://open-pdf/library/items/" + att:
                    self.add("E-MANIFEST", key, "open_uri does not open the registered attachment")
            status, disp = rec.get("ingest_status"), rec.get("disposition")
            if status not in ("incomplete", "complete"):
                self.add("E-MANIFEST", key, "ingest_status %r is not incomplete|complete" % status)
            if disp not in ("new", "update", "disputed", "no_material", "duplicate", None):
                self.add("E-MANIFEST", key, "disposition %r is not a defined value" % disp)
            if status == "complete" and (disp is None or rec.get("ingested_at") is None):
                self.add("E-MANIFEST", key, "complete record lacks disposition or ingested_at")
            if status == "incomplete":
                self.add("W-PENDING", key, "ingest incomplete: %s" % str(rec.get("title"))[:60])
                if rec.get("ingested_at") is not None:
                    self.add("E-MANIFEST", key, "incomplete record already has ingested_at")
            if (disp == "duplicate") != bool(rec.get("duplicate_of")):
                self.add("E-MANIFEST", key, "disposition duplicate and duplicate_of must appear together")
            if not date_ok(rec.get("captured_at")) or not date_ok(rec.get("ingested_at"), True):
                self.add("E-MANIFEST", key, "captured_at/ingested_at is not YYYY-MM-DD")
            cov = rec.get("coverage") or {}
            if cov.get("mode") not in ("standard", "deep", "exhaustive"):
                self.add("E-MANIFEST", key, "coverage.mode %r is not standard|deep|exhaustive" % cov.get("mode"))
            for f in ("text_pages", "visual_pages"):
                v = cov.get(f)
                if not isinstance(v, list) or any(not isinstance(x, int) or isinstance(x, bool) or x < 1 for x in v):
                    self.add("E-MANIFEST", key, "coverage.%s is not a list of 1-based page numbers" % f)
            ann = rec.get("annotations") or {}
            if ann.get("status") not in ("not_checked", "complete", "failed"):
                self.add("E-MANIFEST", key, "annotations.status %r is not a defined value" % ann.get("status"))
            elif ann["status"] != "complete":
                self.add("W-PENDING", key, "annotations %s: %s" % (ann["status"], str(rec.get("title"))[:60]))
            for sp in ann.get("snapshot_paths") or []:
                if nfc(sp) not in self.files:
                    self.add("E-MANIFEST", key, "annotation snapshot is missing on disk: %s" % sp)
                elif S.get(sp, {}).get("source_ref") != key:
                    self.add("E-MANIFEST", key, "annotation snapshot is not registered back to this source: %s" % sp)
            pages_ok(key, rec)
            dup_ok(key, rec)

        by_hash = defaultdict(list)
        for mp in (S, E):
            for key, rec in mp.items():
                if not rec.get("duplicate_of"):
                    by_hash[rec.get("content_hash")].append(key)
        for h, keys in by_hash.items():
            if h and len(keys) > 1:
                self.add("W-DUPHASH", str(h)[:19] + "…", "; ".join(k[-40:] for k in keys))

        # Item classification records
        cfg = self.collection_config()
        item_keys = set()
        for key, rec in Z.items():
            m = ITEM_KEY_RE.match(key)
            if not m:
                self.add("E-MANIFEST", key, "key is not zotero:user:<id>:<item>")
            else:
                item_keys.add(m.group(2))
            missing(key, rec, ITEM_FIELDS)
            for r in rec.get("source_refs") or []:
                if r not in E:
                    self.add("E-MANIFEST", key, "source_refs entry is not a registered external source")
            cs, ib = rec.get("classification_status"), rec.get("inbox_status")
            if cs not in ("pending", "complete", "needs_review", "failed"):
                self.add("E-MANIFEST", key, "classification_status %r is not a defined value" % cs)
            elif cs != "complete":
                self.add("W-PENDING", key, "classification %s" % cs)
            if ib not in ("present", "removed", "not_applicable"):
                self.add("E-MANIFEST", key, "inbox_status %r is not a defined value" % ib)
            add = set(rec.get("planned_add") or [])
            rem = set(rec.get("planned_remove") or [])
            after = set(rec.get("memberships_after") or [])
            if cs == "complete":
                if add - after:
                    self.add("E-MANIFEST", key, "complete but planned_add not in memberships_after: %s" % sorted(add - after))
                if ib == "removed" and rem & after:
                    self.add("E-MANIFEST", key, "Inbox removed but planned_remove still in memberships_after: %s" % sorted(rem & after))
            if cfg:
                if (add | rem) & cfg["protected"]:
                    self.add("E-MANIFEST", key, "planned change touches a protected collection root")
                if add - cfg["managed"]:
                    self.add("W-SCOPE", key, "planned_add outside the managed tree: %s" % sorted(add - cfg["managed"]))
                if rem - cfg["managed"] - cfg["inbox"]:
                    self.add("W-SCOPE", key, "planned_remove outside Inbox/managed tree: %s" % sorted(rem - cfg["managed"] - cfg["inbox"]))
        for key, rec in E.items():
            if rec.get("item_key") and rec["item_key"] not in item_keys:
                self.add("W-PENDING", key, "no zotero_items record for item %s" % rec["item_key"])

        for r in sorted(self.files):
            if r.startswith("raw/") and r.rsplit("/", 1)[-1] not in (".gitkeep", ".DS_Store", "Thumbs.db") and r not in S:
                self.add("W-RAW", r, "raw file is not registered in the manifest")

    # ---------- page evidence ----------

    def check_evidence(self):
        state = self.read("_system/STATE.md") if "_system/STATE.md" in self.files else ""
        for rel in self.pages:
            fm = self.meta[rel]
            srcs, refs = self.lst(rel, "sources"), self.lst(rel, "source_refs")
            for s in srcs:
                if nfc(s) not in self.files:
                    self.add("E-REF", rel, "sources path is missing on disk: %s" % s)
                elif s not in self.S:
                    self.add("W-RAW", rel, "sources path is not registered in the manifest: %s" % s)
            for r in refs:
                if r not in self.E:
                    self.add("E-REF", rel, "source_refs key is not in external_sources: %s…" % r[:44])
            if LOCAL_PATH_RE.search(self.body.get(rel, "")):
                self.add("E-LOCALPATH", rel, "page body contains a machine-local path")
            n = len(set(srcs) | set(refs))
            if n == 0:
                self.add("W-EVIDENCE", rel, "neither sources nor source_refs is set")
            if fm.get("evidence_basis") == "single-source" and n > 1:
                self.add("W-EVIDENCE", rel, "marked single-source but lists %d evidence records" % n)
            if fm.get("type") in ("concept", "entity") and n == 1 and "evidence_basis" not in fm:
                self.add("W-EVIDENCE", rel, "one evidence record but evidence_basis is not set")
            if fm.get("needs_review") is True:
                stem = rel.rsplit("/", 1)[-1][:-3]
                note = "" if stem in state else " (not linked from STATE.md)"
                self.add("W-REVIEW", rel, "needs_review: true" + note)

    # ---------- statistics ----------

    def collect_stats(self):
        types = Counter(self.meta[r].get("type") for r in self.pages)
        self.stats = {
            "pages": len(self.pages),
            "by_type": {t: types.get(t, 0) for t in PAGE_DIRS.values()},
            "raw_records": len(self.S),
            "external_records": len(self.E),
            "zotero_items": len(self.Z),
        }
        for rel in self.pages:
            fm = self.meta[rel]
            s = fm.get("summary")
            if isinstance(s, str) and len(s) > SUMMARY_SOFT_LIMIT:
                self.add("I-SUMMARY", rel, "%d characters" % len(s))
            if fm.get("type") != "source" and not (self.inn[rel] - {"wiki/Home.md"}):
                self.add("I-ORPHAN", rel, "no inbound link from another knowledge page")
            if fm.get("type") in ("concept", "entity"):
                if not re.search(r"zotero://open-pdf|\[\[raw/|\[\^", self.body.get(rel, "")):
                    self.add("I-LOCATOR", rel, "no PDF page link, raw link, or footnote")

    def run(self):
        self.scan()
        self.load_pages()
        self.check_links()
        self.check_index()
        self.check_manifest()
        self.check_evidence()
        self.collect_stats()


def main():
    ap = argparse.ArgumentParser(description="Offline, read-only lint for a Knowledge_Wiki Vault.")
    ap.add_argument("--root", default=None, help="Vault root (default: parent of this script's directory)")
    ap.add_argument("--no-hash", action="store_true", help="skip re-hashing raw files")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings as well as errors")
    ap.add_argument("--verbose", "-v", action="store_true", help="list INFO items instead of counts")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    if not (root / "wiki").is_dir() or not (root / "_system").is_dir():
        print("Not a Knowledge_Wiki Vault root: %s" % root, file=sys.stderr)
        return 2

    lint = Lint(root, check_hash=not args.no_hash)
    lint.run()
    counts = Counter(f[0] for f in lint.findings)
    failed = bool(counts["ERROR"] or (args.strict and counts["WARN"]))

    if args.json:
        print(json.dumps({
            "stats": lint.stats,
            "counts": dict(counts),
            "findings": [dict(zip(("severity", "code", "where", "message"), f)) for f in lint.findings],
        }, ensure_ascii=False, indent=2))
        return 1 if failed else 0

    s = lint.stats
    print("Knowledge_Wiki lint (offline, read-only)")
    print("Pages: %d (%s) | raw records %d | external records %d | zotero_items %d%s" % (
        s["pages"], ", ".join("%s %d" % kv for kv in s["by_type"].items()),
        s["raw_records"], s["external_records"], s["zotero_items"],
        "" if lint.check_hash else " | raw hashes not rechecked"))
    grouped = defaultdict(list)
    for sev, code, where, msg in lint.findings:
        grouped[(sev, code)].append((where, msg))
    for sev in ("ERROR", "WARN", "INFO"):
        for (gs, code), items in sorted(grouped.items()):
            if gs != sev:
                continue
            print("\n%s %s (%d) — %s" % (sev, code, len(items), TITLES.get(code, "")))
            if sev == "INFO" and not args.verbose:
                continue
            for where, msg in items:
                print("  %s: %s" % (where, msg))
    print("\nResult: %d error(s), %d warning(s), %d info item(s)." % (counts["ERROR"], counts["WARN"], counts["INFO"]))
    if not counts["ERROR"] and not counts["WARN"]:
        print("Offline checks pass. Live Zotero availability and semantic review are not covered.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
