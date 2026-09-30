# Knowledge_Wiki Schema v2

> This file is the authoritative knowledge model for Knowledge_Wiki. If a README, agent adapter, or historical design document conflicts with this file, this file and `WORKFLOW.md` take precedence.

## 1. System boundary

Knowledge_Wiki stores durable, reusable, and traceable knowledge. It is not a task manager, diary, chat archive, bookmark pile, or PDF filing cabinet.

There are three classes of durable assets:

- `raw/`: original evidence that must not be silently overwritten. It establishes what a source said at a particular time; it does not by itself establish truth.
- `wiki/`: current knowledge compiled and continuously maintained by an agent.
- `_system/`: vendor-neutral protocol, state, and bookkeeping.

Registered Zotero PDF attachments are an additional evidence location. They stay in Zotero and are not copied into raw by default. The Vault owns portable protocol, source identities, hashes, coverage, and compiled knowledge; it does not own the external bytes. Machine-local paths, agent history, caches, hidden memory, embeddings, and derived indexes are not authoritative state.

## 2. Page types

v2 retains only five ordinary knowledge page types.

| Type | Directory | Purpose |
|---|---|---|
| `source` | `wiki/sources/` | A reusable reading note for one source; it is not raw evidence |
| `concept` | `wiki/concepts/` | A definition, mechanism, method, or theory accumulated across sources |
| `entity` | `wiki/entities/` | A persistently important model, dataset, tool, person, or organization |
| `question` | `wiki/questions/` | A durable research question worth accumulating evidence around |
| `synthesis` | `wiki/syntheses/` | Cross-source comparison, overall judgment, or higher-level understanding |

`wiki/Home.md` is a reserved semantic navigation page, not a sixth knowledge type. Separate Project, Decision, Comparison, or other page types remain deferred until real usage justifies them.

## 3. Required frontmatter

Every ordinary Wiki page must contain:

```yaml
---
title: Canonical Page Title
type: source | concept | entity | question | synthesis
summary: One or two sentences that establish relevance without opening the body.
aliases: []
tags: []
sources: []
status: active | archived
needs_review: false
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Field semantics:

- `title`: the most common canonical term in the domain.
- `summary`: supports low-token candidate selection; it is not a duplicate of the body abstract.
- `aliases`: only real names, abbreviations, and common variants in English, Chinese, or another relevant language. Never invent aliases to fill the field.
- `tags`: a small number of broad topic labels. Wiki tags have no controlled taxonomy; Zotero collection rules are separate.
- `sources`: Vault-relative raw paths such as `raw/papers/example.pdf`, including preserved annotation snapshots. This supports discovery but does not replace claim-level citations.
- Optional `source_refs`: a list of exact keys in the manifest `external_sources` map. Use it on any page whose claims depend on external evidence, including Concepts and Syntheses. An absent field means an empty list; legacy pages remain valid.
- `status`: ordinary pages are `active`; pages that have been merged or no longer participate in current navigation are `archived`.
- `needs_review`: set to `true` only for a genuine conflict, material uncertainty, or issue requiring human scientific judgment.
- `created` / `updated`: creation date and most recent semantic edit date. `updated` does not mean that all facts were reverified.

Type-specific optional fields are allowed, such as a DOI on a Source page or `question_status` on a Question page. Do not duplicate in frontmatter information that is better expressed in the body.

## 4. Language, naming, and links

### Control-plane language

- Authoritative protocol and operational prose use English. This includes `SCHEMA.md`, `WORKFLOW.md`, `DECISIONS.md`, agent adapters, templates, `STATE.md`, and new `log.md` entries.
- `README.md` is the canonical English human guide. `README.zh-CN.md` is the complete Chinese counterpart.
- System framing, headings, comments, and machine-readable keys use English. Data values such as original titles, names, quotations, aliases, URLs, and paths remain in their canonical or source language.
- `_system/index.md` may retain the language of a page title or summary because those entries are knowledge-derived retrieval data rather than protocol prose.

### Wiki language

- An explicit user language request takes precedence.
- Otherwise, determine the language of body text created or modified in the current operation only from the current user prompt: if the prompt contains any Chinese Han character, write in Chinese; if the prompt is entirely English, write in English.
- This rule applies to both page creation and page updates. It does not require preserving the existing page language. Mixed English and Chinese within one page is allowed, and unrelated content must not be rewritten merely for language consistency.
- Regardless of body language, preserve canonical English technical terms, paper titles, model names, dataset names, equations, code identifiers, and necessary quotations in their original form.
- `aliases` should continue to capture real English and Chinese names and common variants for cross-language retrieval. Do not invent aliases merely to create bilingual symmetry.

### Naming and links

- Keep the filename and `title` aligned where practical, and keep basenames unique across `wiki/`.
- Use Obsidian `[[wikilinks]]` only when a connection materially helps understanding or navigation.
- There is no required link count. A legitimate orphan is better than a fabricated relationship.
- Do not create pages that contain only one or two sentences and cannot be reused independently.
- Rename, merge, and delete require user confirmation and corresponding updates to links, index, manifest, and log. The only exception is verified inbox cleanup as defined in `WORKFLOW.md`; it removes only a verified, Git-untracked delivery copy.

## 5. Create, update, and page boundaries

### Update before create

Before creating a page, search titles, aliases, key terms, and synonyms. If an appropriate page already exists, merge the material knowledge into it.

A new page must satisfy at least one of these conditions:

- It represents a durable and reusable concept, entity, or research question.
- It is likely to be referenced from multiple pages.
- It has enough independent content that separation clearly improves navigation or reasoning.
- It is a genuine cross-source synthesis that would be costly to reconstruct later.

Do not create an Entity merely because a source mentions a noun, and do not split every paragraph into a page.

### Source and Raw

- Raw stores Vault-owned evidence; a registered Zotero attachment supplies external original evidence.
- A Source page stores the compiled understanding of one source.
- Not every registered source needs a Source page. Do not create empty pages just to represent a link.
- A Source page is not final evidence for other pages; material claims must remain traceable to the registered original evidence.

### Academic or research paper Source page

A paper with continuing research value should usually receive its own Source page. Exact duplicates, `no_material` sources, or papers that add only minor support to an existing conclusion are exceptions. A paper Source page is a reusable research reading note, not a rewritten abstract. Coverage depth is determined by Standard, Deep, or Exhaustive Ingest, but every mode should address the following when the paper contains material information about them:

- research question, context, contribution, and scope;
- core definitions, assumptions, method or architecture, and key design choices;
- datasets, splits, preprocessing, baselines, metrics, and experimental setup;
- key results, ablations, sensitivity, negative results, and threats to validity;
- author-stated limitations, reproducibility information, open questions, and relationships to existing Wiki knowledge.

There is no fixed equation quota. Standard and Deep retain enough equations and derivations to understand the central contribution, interpret experiments, compare methods, and assess reproduction requirements. Exhaustive covers every equation and derivation with material value. Every mode omits textbook, decorative, or repetitive equations that add no practical understanding. For every retained equation, record:

- readable LaTeX;
- symbols, inputs, outputs, and units where applicable;
- assumptions, the equation's role in the method, and necessary derivation logic;
- an equation, section, or page locator.

Apply the same principle to figures and tables. Standard and Deep selectively compile visual evidence that carries a central claim, experimental comparison, failure mode, or method structure. Exhaustive covers all material visual evidence. Do not truncate at a fixed count or mechanically copy decorative material.

The ingest mode changes reading coverage and compilation granularity, not page type, frontmatter, or provenance requirements. Details not compiled into a Source page remain locatable in registered original evidence through locators, subject to its availability. Never present "recoverable on demand" as if it had already been verified.

### Concept and Synthesis

- A Concept is the best current explanation of a topic and is updated as sources accumulate.
- A Synthesis is a cross-source analysis with a clear question, comparison dimension, scope, or conclusion.
- If the content merely explains a topic, update the Concept. Create a Synthesis only when there is an independent argument or comparison.

### Question

Use Question pages only for durable research questions, not one-off queries. The recommended optional field is:

```yaml
question_status: open | provisional | answered | closed
```

## 6. Provenance

The following require a nearby original-evidence citation:

- exact numbers, dates, and benchmarks;
- direct quotations;
- current product, software, organization, or policy status;
- key experimental results;
- contested conclusions or claims that are easy to misinterpret.

Prefer Markdown footnotes that point to Vault-relative raw paths:

```markdown
The experiment reports a score of 12.3 on Dataset X.[^paper-p7]

[^paper-p7]: [[raw/papers/example.pdf#page=7]], Table 2.
```

Web snapshots may link to headings. For papers, retain page, section, figure, table, or equation locators when readily available. Ordinary stable paraphrases may rely on the page-level `sources` or `source_refs` fields and do not require a footnote on every sentence.

Links between Wiki pages support navigation and explanation; they do not create circular evidence. When derived synthesis is written back to the Wiki, retain the underlying raw sources or exact external source references.

## 7. Inference, disagreement, and freshness

### Inference

Mark conclusions not directly stated by a source and derived by an agent or user:

```markdown
**[Inference]** This result may imply...
```

### Disagreement

- Present competing claims, scopes, and sources side by side in the relevant page's `Evidence and disagreement` section.
- Do not assume that a newer source or a larger number of sources is necessarily correct.
- First check for differences in dataset, split, metric, version, population, assumption, and evaluation protocol.
- When human judgment is required, set `needs_review: true` and add a link in `_system/STATE.md`.

### Freshness

- Timeless: no freshness metadata is required.
- Snapshot: use `as of YYYY-MM-DD` in the body.
- Pointer: retain the authoritative URL and add `last checked: YYYY-MM-DD`.
- Do not apply a universal rule such as "90 days without an update means stale."

## 8. Lifecycle and structural changes

- An agent may create and update `active` pages.
- Ordinary additive ingest does not require review of every edit.
- When merging pages, move unique content and sources into the canonical page, repair links, mark the old page `archived`, and point it clearly to the canonical page.
- Raw evidence is never deleted because a Wiki page is merged or archived.
- Schema changes require user confirmation and a `log.md` entry. Update `DECISIONS.md` only when the accepted architecture or its rationale changes.

## 9. Token-aware invariants

- Use the index, summaries, aliases, and targeted search to filter candidates before reading full pages.
- In the first Standard Ingest pass, open no more than 5 candidate pages in full. For later candidates, prefer frontmatter, summaries, or matching sections.
- Prefer targeted patches over full-page rewrites.
- Page count is a risk signal, not a hard limit on legitimate knowledge updates.
- Do not expand the cascade on weak relationships or traverse the entire Wiki graph.

## 10. Explicitly excluded from v2

- Numeric confidence or source-quality scoring;
- typed relationship ontology;
- claim ledger or contradiction database;
- Project page type;
- vector DB, graph DB, embeddings, PPR, or BM25;
- background watcher, scheduled ingest, or unattended reconciliation;
- staging transactions, locks, or multiple writers.

## 11. External evidence and backward-compatible manifest v2

The root object has `version: 2`, `last_updated`, `sources`, `external_sources`, and `zotero_items`. Keep all v1 `sources` records and raw-path keys intact. Missing v2 maps in a v1 manifest are read as empty; upgrade the root before writing external records. Never invent historical coverage for legacy records.

- `sources` keeps Vault-relative raw keys and the existing fields from WORKFLOW section 12. Optional `duplicate_of` points to an already registered raw key or external reference with the same hash. Annotation snapshot records also carry `snapshot_kind: zotero_annotations`, `source_ref`, and `payload_hash`.
- `external_sources` is keyed by `zotero:user:<user-id>:<attachment-key>:<sha256-hex>` (the last component is the full 64-character digest without the `sha256:` prefix). Personal libraries only in v2; other libraries require an explicit scope extension. The stable Zotero account user ID is not a local SQLite libraryID (often 1) or an API alias (often 0). Resolve and verify it without saving credentials. If identity cannot be established, report the blocker rather than register a guessed identity.
- `zotero_items` is keyed by `zotero:user:<user-id>:<item-key>`. It holds resumable classification state for a parent item, or the attachment itself for a standalone PDF. This state is separate from file snapshots.

External record fields:

```json
{
  "provider": "zotero",
  "library": {"type": "user", "id": "<stable-account-user-id>"},
  "item_key": "<parent-or-standalone-key>",
  "attachment_key": "<attachment-key>",
  "title": "<source title>",
  "canonical_id": null,
  "source_url": null,
  "paper_version": null,
  "content_hash": "sha256:<64-hex>",
  "open_uri": "zotero://open-pdf/library/items/<attachment-key>",
  "captured_at": "YYYY-MM-DD",
  "ingested_at": null,
  "ingest_status": "incomplete",
  "disposition": null,
  "duplicate_of": null,
  "pages_created": [],
  "pages_updated": [],
  "coverage": {
    "mode": "standard",
    "text_pages": [],
    "visual_pages": [],
    "sections": [],
    "deferred": []
  },
  "annotations": {"status": "not_checked", "checked_at": null, "snapshot_paths": []}
}
```

`ingest_status` is `incomplete|complete`; set `ingested_at` only after durable compilation or a verified duplicate/no-material outcome. `disposition` is `new|update|disputed|no_material|duplicate`, or null while incomplete. Coverage mode is `standard|deep|exhaustive`; page arrays contain actual 1-based physical PDF pages. Duplicate registration may have empty new coverage and inherit evidence only through the verified `duplicate_of` record. `annotations.status` is `not_checked|complete|failed`; complete with no snapshots is valid when nothing was used. A failed annotation read is not an empty annotation set and prevents finishing the combined Inbox workflow unless the user explicitly waives it. A waiver must name the failed/unavailable scope and user decision in the log; retain the failed annotation status rather than marking unread content complete.

Item classification record fields:

```json
{
  "source_refs": [],
  "classification_status": "pending",
  "rules_revision": null,
  "memberships_before": [],
  "planned_add": [],
  "planned_remove": [],
  "memberships_after": [],
  "inbox_status": "present",
  "reason": "",
  "updated_at": "YYYY-MM-DD"
}
```

Classification status is `pending|complete|needs_review|failed`; Inbox status is `present|removed|not_applicable`. Membership values are collection keys. Persist the intended delta and pre-write membership before external changes; append completed before/after deltas to the log before replacing a record for a later operation. `source_refs` names the explicitly selected attachment scope, not every historical attachment under a paper. STATE holds unfinished multi-item migrations, selected item keys, and remaining work; it is not a second manifest.

### Version, citation, and graph semantics

- SHA-256 hashes the actual PDF bytes mechanically. Collection names, hierarchy, membership, metadata, and Zotero record revision counters do not define a PDF hash or a paper version.
- Different bytes create a separate immutable source identity even for the same attachment key. Do not assume that byte differences imply a scientific revision. Preserve previous records and flag unavailable historic bytes; a hash cannot restore them.
- Keep used old attachments in Zotero. Never overwrite, delete, merge, or reparent them as an ingest side effect. When versions are materially different, retain claim-to-version distinctions within the existing Source note unless a separate note has independent value.
- Provide a human-readable attachment link in the Source page and nearby claim citations, e.g. `[PDF p.7](zotero://open-pdf/library/items/ATTACHMENT?page=7)`, together with the exact source reference and section/figure/equation locator. Printed page labels may supplement, never replace, physical page numbers. The external reference can be defined once in a named provenance block and referenced by footnotes.
- The URI opens the current attachment; it does not verify historical bytes. An agent must resolve and hash the attachment before attributing new answers to the registered snapshot. Changed or unavailable bytes must be reported.
- Obsidian graph relationships use meaningful Wiki-to-Wiki links. External Zotero URIs are not Wiki graph nodes. Classification changes alone do not change a page's semantic `updated` date or compiled content.

### Annotation evidence

Read annotations for the selected attachment, filter any parent-wide result by attachment, and distinguish author text, user comments, and agent inference. Preserve only annotations/notes actually used in compilation, as immutable Markdown under `raw/other/`; put necessary image evidence under `raw/assets/`. Do not copy the PDF or mechanically mirror all Zotero notes.

A snapshot records the exact source reference and PDF hash, capture time, annotation/note keys, text, comment, color when present, physical page and original position/page label when available, and any preserved assets. Missing fields remain unknown. Imported notes without a page are labeled as such. They cannot establish paper facts without checking the PDF.

For deduplication, compute `payload_hash` from UTF-8 JSON with sorted object keys, compact separators, and records sorted by stable key. Include the source reference, actual selected content, positions, and asset content hashes; exclude capture time and volatile sync counters. Preserve the actual normalized payload in the snapshot for recomputation. The raw file gets its own `content_hash` over its complete bytes. Unchanged payload reuses the existing snapshot; changed content creates a new file. Query never persists snapshots unless explicitly promoted.
