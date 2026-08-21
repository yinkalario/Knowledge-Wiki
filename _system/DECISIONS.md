# Knowledge_Wiki Architecture Decisions

> This file is a curated statement of the current accepted architecture and its rationale. It is not a patch log or discussion transcript. Normative rules live in `SCHEMA.md` and `WORKFLOW.md`; operational history lives in `log.md`, and exact change history lives in Git.

## 1. Human-authoritative compiled knowledge

**Decision**

- Separate raw evidence from compiled Wiki knowledge.
- Prefer updating existing knowledge over creating additional pages.
- Treat the user as the final epistemic authority and the LLM agent as a replaceable maintainer.

**Rationale**

Raw evidence preserves what a source said, while compiled knowledge should remain coherent as new sources arrive. Separating the two makes claims auditable without turning the Wiki into a source dump.

**Consequences**

- Material claims remain traceable to raw.
- Source pages compile understanding but do not replace raw evidence.
- Agent memory, cache, session history, and embeddings are disposable.

## 2. Portable control plane and language

**Decision**

- Keep the vendor-neutral protocol inside the Vault.
- Use `_system/SCHEMA.md` and `_system/WORKFLOW.md` as the authoritative control plane; keep `AGENTS.md` and `CLAUDE.md` as thin adapters.
- Use English for system protocol and operational prose.
- Let the current user prompt determine Wiki body language: a prompt containing Chinese uses Chinese, while an English-only prompt uses English, unless the user explicitly requests another language.
- Preserve canonical English technical terms, identifiers, paper titles, model names, dataset names, and genuine multilingual aliases.

**Rationale**

Any capable agent should be able to maintain the Vault from files alone, without vendor-specific memory or conversation context. English provides one portable control language, while prompt-directed Wiki language preserves usability for multilingual research.

**Consequences**

- `README.md` is the canonical English human guide, with `README.zh-CN.md` as the complete Chinese counterpart.
- System structure and keys remain English; original titles, names, paths, quotations, and knowledge-derived index data may retain their canonical language.
- A public starter contains generic protocol and a clean skeleton, not a maintainer's personal raw, Wiki, state, manifest records, log history, or conversations.

## 3. Minimal knowledge model and viewer-independent format

**Decision**

- Keep the v1 page model to Source, Concept, Entity, Question, and Synthesis.
- Treat `wiki/Home.md` as a human dashboard and `_system/index.md` as the compact machine candidate catalog.
- Use portable Markdown, YAML, raw paths, and wikilinks as durable representation.
- Treat Obsidian as a viewer rather than an authoritative runtime.

**Rationale**

A small page model and plain files are easier to search, audit, migrate, and maintain across agents. Additional ontology or runtime infrastructure should solve an observed problem rather than an anticipated one.

**Consequences**

- Project, Decision, Comparison, numeric confidence, typed relationships, claim ledgers, and complex taxonomy remain deferred.
- Dataview, vector databases, graph databases, embeddings, PPR, BM25, background watchers, and multi-writer coordination are not required by v1.
- New page types or infrastructure require a demonstrated need and explicit approval.

## 4. Three ingest modes with shared epistemic standards

**Decision**

- Standard Ingest is the default and remains token-aware while producing research-usable notes.
- Deep Ingest requires an explicit request and targets deep understanding of the central argument and evidence chain with selective durable compilation.
- Exhaustive Ingest requires an explicit request and targets material-complete coverage for reproduction, peer review, or section-by-section technical analysis.
- Equations, derivations, figures, tables, and experiments are selected by material value and ingest mode, not fixed quotas.

**Rationale**

Research tasks need different reading depths, but depth should not create incompatible page types or weaken evidence standards. A three-level model separates ordinary efficiency, central-depth analysis, and material completeness.

**Consequences**

- All modes share the same page schema, provenance, update-before-create rule, and confirmation boundaries.
- Standard opens no more than 5 candidate pages in full during the first pass; this is a reading bound, not a hard cap on legitimate updates.
- 1–10 material page changes are within ordinary ingest authority; more than 10 require a proposed change list and user confirmation.
- Long Exhaustive work may be batched, with coverage and remaining work recorded in portable STATE until completion.

## 5. Query is read-only unless knowledge is promoted

**Decision**

- Keep ordinary Query read-only.
- Propose Promotion when an answer produces durable, reusable knowledge that would be costly to reconstruct.
- Allow explicit Promote and session-scoped Research Mode without automatically preserving the full conversation.

**Rationale**

Most questions do not justify durable writes. Separating retrieval from compilation prevents temporary answers and brainstorming from accumulating as authoritative knowledge.

**Consequences**

- Query does not modify Wiki, index, manifest, STATE, or log.
- Promoted claims return to raw evidence, preserve provenance, and mark inference.
- Research Mode never becomes a hidden persistent preference and retains high-risk confirmation boundaries.

## 6. Simple provenance and bookkeeping

**Decision**

- Use immutable dated raw snapshots as canonical evidence.
- Use a simple `manifest.json` keyed by Vault-relative raw path, with SHA-256, source identifiers, disposition, and affected pages.
- Use exact hashes as the duplicate gate.
- Defer event ledgers, source/version IDs, and more complex databases until the simple manifest causes a real operational problem.

**Rationale**

The system needs reproducible provenance and duplicate detection without introducing a database or hidden runtime dependency.

**Consequences**

- Identical hashes do not produce duplicate Wiki knowledge.
- Changed content at the same URL or DOI becomes a new retained snapshot.
- A hash verifies integrity but cannot recover missing raw evidence.
- Load-bearing numbers, quotations, current claims, and experimental results cite raw near the claim.

## 7. Single writer, separated synchronization, and recoverable evidence

**Decision**

- Allow only one canonical writer at a time.
- Use file synchronization to move ordinary Vault files across devices, Git for text diff, audit, and rollback, and an independent versioned backup for raw disaster recovery.
- Keep `.git/` local to the designated commit machine and never copy it through the file-sync service.
- Keep actual `raw/` and `inbox/` content in the Vault but outside Git; track their directory markers and keep `_system/manifest.json` in Git.
- Prefer OS temporary storage for intermediate processing; use Git-ignored `_runtime/` only when workspace-local scratch is required. Runtime artifacts are never authoritative.

**Rationale**

File synchronization and Git maintain different state and cannot safely coordinate concurrent writers. Raw evidence may grow large and needs reliable recovery, but Git is not the appropriate recovery layer for it.

**Consequences**

- A device without `.git/` may ingest and lint, but retains inbox delivery copies and reports exact pending changes. The commit machine rechecks synchronization, diff, manifest-to-raw consistency, and lint before committing.
- Switching devices or agents requires waiting for file synchronization and preserving the single-writer boundary.
- Verified inbox cleanup is the only narrow delete exception: it occurs only after canonical raw, matching SHA-256, manifest, bookkeeping, lint, attachments, and commit state are all verified.
- Runtime scratch must never be the only copy of durable evidence or knowledge.

## 8. Curated governance and bounded operational state

**Decision**

- Keep `SCHEMA.md` and `WORKFLOW.md` as current truth and edit superseded rules in place.
- Keep `DECISIONS.md` curated by architectural topic rather than appending every patch.
- Keep `STATE.md` bounded to current focus, pending human review, maintenance backlog, and handoff needs.
- Keep `log.md` as append-only semantic operation history and Git as exact file history.

**Rationale**

Each file should answer one question without duplicating the same history. Current rules must remain easy to locate, while operational and exact change history remain recoverable at the appropriate layer.

**Consequences**

- Maintenance outcomes and one-time migrations belong in `log.md` or Git, not in architecture decisions.
- Completed STATE items may be compressed after their durable outcomes are captured.
- Merge, rename, delete, major epistemic conflict, schema change, and more than 10 planned page changes require user confirmation, except verified inbox cleanup.
- Archive structures, protocol splits, index or manifest sharding, adapter read-order changes, and durable path changes require a concrete proposal and prior approval.
- No archive or lifecycle infrastructure is introduced before a real need appears.
