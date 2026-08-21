# Knowledge_Wiki Design Handoff

> [!note] Historical design input
> Knowledge_Wiki v1 has now been specified in `_system/SCHEMA.md` and `_system/WORKFLOW.md`. This BOOTSTRAP remains valuable design history, but it is no longer the operational authority. If rules conflict, follow SCHEMA and WORKFLOW.

> **Purpose:** This file is the bootstrap handoff for building a personal, long-term, LLM-maintained Knowledge Wiki in Obsidian.
>
> **Current maintainer:** Codex
>
> **Portability requirement:** The Wiki must remain model- and vendor-agnostic. Claude Code, Gemini, or another capable agent should be able to take over later using only the files in the vault.
>
> **Status:** Top-level design is mostly agreed. Do **not** blindly implement everything below. First review the architecture, identify weaknesses or unnecessary complexity, and help finalize the design. Then implement it step by step.

---

# 1. Objective

Build a personal **Knowledge_Wiki** in Obsidian using the core philosophy of Andrej Karpathy's LLM Wiki:

- The human selects sources, explores, asks questions, and makes judgments.
- The LLM maintains and evolves the Wiki.
- Knowledge is **compiled once and kept current**, rather than re-derived from raw sources on every query.
- The Wiki is a **persistent, compounding artifact**.
- Obsidian is the human-facing knowledge IDE/viewer.
- The active LLM agent is replaceable infrastructure, not the source of truth.

The Wiki is intended primarily for research and technical knowledge, but it is **not limited to research**. It may contain durable knowledge from AI, audio, speech, computing, tools, systems, mathematics, organizations, people, methods, and other long-term domains.

The Wiki should not become a task manager, daily journal, inbox archive, or general file dump.

---

# 2. Existing Personal Vault Separation

There are two distinct Obsidian vault roles:

## General operational vault

`Vault2026`

Use for:

- daily notes
- meetings
- administrative work
- temporary notes
- reminders
- task-oriented information
- transient project operations
- short-lived working memory

## Long-term knowledge vault

`Knowledge_Wiki`

Use for:

- durable concepts
- research knowledge
- paper understanding
- methods
- models
- systems
- datasets
- tools
- long-term project knowledge
- open research questions
- synthesized understanding
- durable technical or conceptual knowledge outside research

The split is:

> `Vault2026 = working / operational memory`
> `Knowledge_Wiki = durable / long-term knowledge`

Do **not** split Knowledge_Wiki into separate vaults by research topic or domain. Cross-domain knowledge links are valuable and should remain inside one graph.

---

# 3. Reference Implementations and Sources

The design should be informed by the following references.

## Core idea

Andrej Karpathy LLM Wiki gist:

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Key ideas to preserve:

- raw sources
- LLM-maintained Wiki
- schema/instructions
- ingest / query / lint
- human chooses sources and asks questions
- LLM writes and maintains
- persistent compounding knowledge
- Obsidian as IDE
- avoid re-synthesizing from scratch on every question

## Obsidian Karpathy Wiki plugin

https://community.obsidian.md/plugins/karpathywiki

Important ideas:

- Obsidian-native Wiki usage
- lexical retrieval
- alias / keyword expansion
- graph retrieval
- Personalized PageRank over wikilinks
- possible future retrieval enhancement

Do **not** make the plugin a second independent Wiki maintainer in v1.

## Hermes Research LLM Wiki

https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-llm-wiki

Important ideas:

- schema-first operation
- provenance
- index
- log
- session recovery
- ingest / query / lint
- cascade updates
- page creation thresholds
- contradiction and freshness awareness

## Astro-Han Karpathy LLM Wiki

https://github.com/Astro-Han/karpathy-llm-wiki

Important ideas:

- `raw/` immutable source material
- `wiki/` compiled knowledge
- Ingest / Query / Lint
- triage:
  - New
  - Update
  - Disputed
  - No material
- Grounding Invariant
- cascade updates
- query is read-only by default
- do not force every source to produce a page
- avoid unnecessary vector/graph infrastructure until needed
- avoid uncalibrated numeric confidence scores

## ar9av Obsidian Wiki

https://github.com/ar9av/obsidian-wiki

Important ideas:

- agent-agnostic skills
- one Wiki usable by Claude Code, Codex, Gemini, Cursor, etc.
- `.manifest.json` for source/delta tracking
- summary-first retrieval
- bounded `hot.md` / session state
- update existing pages rather than accumulating duplicates
- deduplication and cross-linking
- separation between bookkeeping files and semantic graph
- optional later graph tooling

## obsidian-second-brain

https://github.com/eugeniughelbur/obsidian-second-brain

Important ideas:

- AI-first notes
- knowledge should be understandable by a future agent in isolation
- facts should not silently rot
- freshness model:
  - timeless
  - dated snapshot
  - pointer to live source
- update existing knowledge instead of append-only accumulation
- agent portability
- derived caches should not be authoritative

Do **not** automatically adopt:
- large command surface
- scheduled agents
- automatic reconciliation of every contradiction
- task management features
- calendar/daily operating system behavior

## claude-obsidian

https://github.com/AgriciDaniel/claude-obsidian

Important ideas:

- user vault is the durable asset
- product/plugin/runtime are separate
- runtime caches/indexes are disposable and regenerable
- source provenance
- explicit inbox and immutable raw layer
- single logical operation / single-writer principle
- safe, inspectable changes
- one agent/orchestrator should apply canonical writes

Do **not** copy the full heavy transaction system into v1 unless real usage proves it necessary.

## Additional overview

https://medium.com/@urvvil08/andrej-karpathys-llm-wiki-create-your-own-knowledge-base-8779014accd5

Useful as explanatory context, but not authoritative over the original gist or actual implementations.

---

# 4. Core System Definition

The Knowledge_Wiki should be treated as:

> A personal, long-term, source-grounded external memory system in which raw evidence is continuously compiled by an LLM into coherent, interconnected, updatable knowledge.

The system is **not**:

- a generic notes folder
- a PDF library
- a RAG database
- a task manager
- a chat history archive
- a daily journal
- a bookmark dump

The primary quality metric is not page count.

The primary quality metric is:

> **The Wiki should become more coherent, connected, useful, and epistemically reliable as it grows — not merely larger.**

---

# 5. Roles

## Human

Role: Editor-in-Chief / final epistemic authority.

Responsibilities:

- choose what is worth reading
- decide what is important
- ask questions
- inspect synthesis
- judge scientific disagreement
- approve major ontology/schema changes
- decide when evidence is genuinely ambiguous
- correct the agent when necessary

## ChatGPT

Role: research and thinking partner.

Typical use:

- reading papers
- explaining concepts
- brainstorming
- comparing methods
- developing hypotheses
- deep research
- discussing research directions
- generating durable conclusions worth promoting

ChatGPT conversation history is **not** authoritative Wiki state.

Useful conclusions from conversations should be distilled into the Wiki.

## Codex

Role: current canonical Wiki maintainer / knowledge compiler.

Responsibilities:

- ingest
- triage
- retrieve existing related knowledge
- compile
- merge
- update
- cross-link
- cascade update
- maintain metadata
- maintain manifest
- maintain index/state/log
- lint
- deduplicate
- propose structural improvements
- inspect changes
- preserve provenance

Codex is the current maintainer, but must **not** become an architectural dependency.

## Obsidian

Role: knowledge IDE / viewer.

Use for:

- reading
- browsing
- backlinks
- wikilinks
- search
- Graph View
- manual review
- selective editing
- later optional Canvas/Bases usage

## Synology Drive

Role: file synchronization only.

It is not part of the knowledge model.

---

# 6. Ten Core Principles

These principles should become the constitutional basis of the Wiki.

## 1. Raw is immutable evidence

Once material becomes canonical raw evidence, do not silently rewrite it.

If a web page changes, save a new snapshot rather than overwriting historical evidence.

## 2. Wiki is compiled knowledge

The Wiki is not a source dump.

Raw materials are transformed into durable understanding.

## 3. Update before create

When appropriate, update an existing concept/entity/question/synthesis page instead of creating another near-duplicate page.

New sources should improve existing knowledge whenever possible.

## 4. Every important claim must remain traceable

Load-bearing claims should ultimately be traceable to raw evidence.

Wiki pages may reference other Wiki pages for context/navigation, but the Wiki must not become circular self-evidence.

## 5. Human judges; LLM maintains

The agent performs knowledge maintenance.

The human remains responsible for scientific judgment, ambiguity, and important interpretation.

## 6. Preserve disagreement and historical state

Do not silently rewrite contested or superseded knowledge as if prior understanding never existed.

Use explicit states such as:

- disputed
- outdated
- superseded
- unresolved

when needed.

## 7. Knowledge must have freshness semantics

Facts should be one of:

- **Timeless** — stable knowledge
- **Snapshot** — true at a dated point in time
- **Pointer** — current truth lives in an external authoritative system/source

Do not store volatile present-tense facts without dates.

## 8. Agent and model are replaceable

The system must work if Codex is replaced by Claude Code, Gemini, or another capable agent.

No vendor-specific hidden state may be required to operate the Wiki.

## 9. Agent memory is disposable

The following are non-authoritative and disposable:

- Codex session history
- Claude Code session history
- ChatGPT conversation history
- agent caches
- hidden scratchpads
- embeddings
- search indexes
- proprietary memory
- local session state

If a piece of information is required to continue maintaining the Wiki correctly, it must exist in vendor-neutral files in the Wiki.

## 10. Complexity must be earned

Start simple.

Prefer:

- Markdown
- YAML
- wikilinks
- index
- summaries
- aliases
- grep/ripgrep
- manifest
- Obsidian search

Only add:

- BM25
- embeddings
- graph retrieval
- vector DB
- graph DB
- complex ontologies

when observed retrieval problems justify them.

---

# 7. Proposed Layered Architecture

Use five conceptual layers.

## Layer 0 — Inbox

Temporary intake.

May contain:

- PDFs
- web captures
- pasted text
- rough notes
- ChatGPT/Claude/Codex distilled outputs
- screenshots
- ideas
- documents

Inbox may be messy.

Inbox is not authoritative knowledge.

## Layer 1 — Raw

Immutable source evidence.

Examples:

- papers
- saved web pages
- source notes
- conversation snapshots
- images
- imported documents

Raw is authoritative evidence.

## Layer 2 — Wiki

LLM-maintained compiled knowledge.

This is the actual long-term knowledge graph.

## Layer 3 — System

Vendor-neutral protocol and persistent operational memory.

Contains:

- schema
- workflows
- style
- preferences
- design decisions
- current state
- index
- log
- manifest
- taxonomy

## Layer 4 — Runtime

Disposable derived state.

Examples:

- search index
- embeddings
- transaction journal
- agent cache
- temporary generated files

Runtime must be regenerable from the durable vault.

---

# 8. Proposed Top-Level Directory

Current proposed v1 layout:

```text
Knowledge_Wiki/
│
├── AGENTS.md
├── CLAUDE.md
│
├── _system/
│   ├── SCHEMA.md
│   ├── WORKFLOW.md
│   ├── STYLE.md
│   ├── PREFERENCES.md
│   ├── DECISIONS.md
│   ├── STATE.md
│   ├── index.md
│   ├── log.md
│   ├── manifest.json
│   └── taxonomy.md
│
├── inbox/
│
├── raw/
│   ├── papers/
│   ├── web/
│   ├── conversations/
│   ├── notes/
│   └── assets/
│
├── wiki/
│   ├── sources/
│   ├── concepts/
│   ├── entities/
│   ├── questions/
│   ├── syntheses/
│   └── projects/
│
├── _staging/
│
├── .obsidian/
└── .gitignore
```

This is still a proposal. Review before implementing.

---

# 9. Meaning of the System Files

## `_system/SCHEMA.md`

Defines what the Wiki contains.

Should eventually specify:

- page types
- page creation thresholds
- merge/split rules
- naming
- required metadata
- provenance rules
- link rules
- lifecycle/status semantics
- freshness semantics
- contradiction handling
- relationship conventions

This should be the main knowledge-model specification.

## `_system/WORKFLOW.md`

Defines operations.

At minimum:

- Capture
- Ingest
- Query
- Save/Promote
- Lint
- Dedup
- Cascade Update
- Archive/Rebuild if ever needed

## `_system/STYLE.md`

Defines writing conventions.

Potential topics:

- concise but technically complete
- preserve equations
- research-oriented tone
- avoid unnecessary repetition
- terminology consistency
- link style
- headings
- source citation style
- how to mark inferred/disputed/outdated content

## `_system/PREFERENCES.md`

Portable user/agent collaboration preferences.

Examples:

- preserve technical detail
- avoid shallow summaries
- update before create
- do not silently resolve scientific disagreement
- prefer durable knowledge over transient facts
- minimize unnecessary page creation

## `_system/DECISIONS.md`

Records important design decisions and rationale.

Examples:

- use one Knowledge_Wiki vault
- separate Vault2026 and Knowledge_Wiki
- Codex is current maintainer
- agent portability is mandatory
- no vector DB in v1
- raw is immutable
- query is read-only by default

Persist decisions, not conversation transcripts.

## `_system/STATE.md`

Bounded current semantic state.

Target size: roughly 500–1000 words.

Possible content:

- recently ingested
- recently updated
- active research questions
- unresolved conflicts
- pending review
- current focus
- important open maintenance issues

This acts like portable "hot context".

It is derived and regenerable, but very useful for session continuity.

## `_system/index.md`

Compact knowledge map.

Should allow an agent to identify candidate Wiki pages without opening everything.

Potential fields per entry:

- page link
- type
- short summary
- tags
- updated date

Do not treat index links as semantic graph edges.

## `_system/log.md`

Append-only semantic operation log.

Examples:

- ingest
- update
- lint
- merge
- split
- promote
- archive
- major schema change

## `_system/manifest.json`

Machine-readable ingest ledger.

Purpose:

- avoid duplicate ingestion
- track raw identity
- track pages affected by each source
- identify unprocessed raw material
- support delta operations

Potential fields:

```json
{
  "source_id": "...",
  "raw_path": "...",
  "content_hash": "...",
  "collected_at": "...",
  "published_at": "...",
  "disposition": "new|update|disputed|no_material",
  "pages_created": [],
  "pages_updated": [],
  "ingested_at": "..."
}
```

Keep it simple.

## `_system/taxonomy.md`

Controlled vocabulary only where useful.

Avoid premature ontology design.

---

# 10. Agent Adapters

## `AGENTS.md`

Codex adapter only.

It should be thin.

It should instruct Codex to read the vendor-neutral system files before modifying the Wiki.

It must not become the authoritative protocol.

## `CLAUDE.md`

Claude Code adapter only.

It should point to the same vendor-neutral system files.

The Wiki must remain operable if the active agent changes.

Conceptually:

```text
                authoritative protocol
                         │
                 _system/*.md
                         │
             ┌───────────┴───────────┐
             │                       │
         AGENTS.md               CLAUDE.md
             │                       │
           Codex                Claude Code
```

---

# 11. Proposed Core Wiki Page Types

Keep v1 limited to six types.

## 1. Source

Directory:

`wiki/sources/`

Purpose:

A knowledge-oriented page for a specific source when that source deserves a dedicated page.

Examples:

- research paper
- important technical article
- foundational blog
- major document

A source page is not simply a raw copy.

For academic papers, source pages may include:

- Problem & Motivation
- Method
- Architecture
- Key Equations
- Results
- Limitations
- Relationship to prior work
- My interpretation
- Research implications
- Related Wiki pages

Important:

Not every raw source must generate a source page.

`No material` is a valid disposition.

## 2. Concept

Directory:

`wiki/concepts/`

Purpose:

Durable conceptual knowledge that compounds across sources.

Examples:

- Flow Matching
- Diffusion Transformer
- Representation Alignment
- Multi-ACCDOA
- Target Speaker Extraction
- LLM Scaffolding

A concept page should represent the **best current Wiki understanding**, not one source's definition.

## 3. Entity

Directory:

`wiki/entities/`

Purpose:

Concrete real-world entities.

Possible subtypes in metadata:

- person
- organization
- model
- dataset
- benchmark
- software
- tool
- product
- institution
- system

Do not create separate folders for each subtype unless future usage proves necessary.

## 4. Question

Directory:

`wiki/questions/`

Purpose:

Persistent open questions, especially research questions.

A question page may contain:

- Question
- Motivation
- Hypotheses
- Evidence For
- Evidence Against
- Experiments
- Related Concepts
- Current View
- Open Issues

This is one of the most important page types for research.

The Wiki should store not only:

> What do I know?

but also:

> What am I trying to know?

## 5. Synthesis

Directory:

`wiki/syntheses/`

Purpose:

Cross-source, cross-concept higher-level understanding.

Examples:

- State of Spatial Audio Generation
- Flow Matching vs Diffusion for Audio Generation
- Open Problems in Animal Sound Generation
- Current Approaches to Audio-Language Alignment

Synthesis pages should be among the highest-value Wiki artifacts.

## 6. Project

Directory:

`wiki/projects/`

Purpose:

Durable project-level knowledge.

Store:

- research objective
- assumptions
- architecture
- important decisions
- rationale
- findings
- lessons
- related questions
- related concepts

Do not store:

- tomorrow's tasks
- meeting reminders
- weekly deadlines
- transient execution details

Those belong in Vault2026.

---

# 12. Why There Is No Separate `decisions/` Type in v1

Project-specific decisions should initially live in Project or Question pages.

Example:

```markdown
## Decisions

### 2026-08-17 — Use TangoFlux as baseline
Reason:
Alternatives:
Consequences:
```

Knowledge_Wiki architecture decisions belong in:

`_system/DECISIONS.md`

Only introduce `wiki/decisions/` later if actual usage shows a need for cross-project durable decision objects.

---

# 13. Page Creation Philosophy

Page creation should be conservative.

Create a new page only when at least one of these holds:

- the subject is a durable concept/entity/question/project
- it is likely to be referenced from multiple places
- it has enough independent substance to stand alone
- it represents a reusable unit of knowledge
- separating it improves navigation or reasoning
- a synthesis genuinely spans multiple sources/pages

Do not create pages simply because a new source mentions a noun.

Prefer updating an existing page when the core subject already exists.

Avoid:

- one paper → one automatic note as a mandatory rule
- one paragraph → one page
- excessive Zettelkasten atomization
- duplicate synonyms as separate pages

---

# 14. Ingest Workflow

Target workflow:

```text
SOURCE
   │
   ▼
INBOX
   │
   ▼
CAPTURE
   │
   ▼
RAW + manifest
   │
   ▼
TRIAGE
   │
   ├── No material ───────────────→ log
   │
   ├── New
   ├── Update
   └── Disputed
          │
          ▼
     RETRIEVE EXISTING
          │
   STATE + index + aliases
   + grep/ripgrep + links
          │
          ▼
        PLAN
          │
   pages to create/update
          │
          ▼
       COMPILE
          │
          ▼
    CASCADE UPDATE
          │
          ▼
       VALIDATE
          │
  links / provenance / freshness
          │
          ▼
 index + manifest + STATE + log
          │
          ▼
       inspect diff
          │
          ▼
      Git checkpoint
```

Important behavior:

A single paper may:

- create one source page
- update multiple concept pages
- update an entity
- update a research question
- update a synthesis
- update a project

That is desirable.

---

# 15. Triage States

Every ingest should classify the source before canonical Wiki writes.

## New

Creates one or more genuinely new Wiki objects.

## Update

Adds material knowledge to existing Wiki pages.

## Disputed

Introduces evidence that conflicts with existing knowledge.

May coexist with New or Update.

## No material

The source adds nothing worth changing in the compiled Wiki.

Keep the raw source and manifest/log record.

Do not force page creation.

---

# 16. Cascade Update

After the primary update, search for ripple effects.

Do not only update the obvious page.

Check:

- aliases
- synonyms
- related concepts
- related questions
- relevant projects
- syntheses
- outdated statements
- claims touched by the new source

The Wiki should behave like a compiled knowledge graph, not a folder of isolated notes.

---

# 17. Query Workflow

Query should be **read-only by default**.

Suggested retrieval sequence:

```text
STATE.md
   ↓
index.md
   ↓
titles / aliases / summaries
   ↓
grep/ripgrep
   ↓
open relevant pages
   ↓
follow wikilinks
   ↓
answer
```

Do not write new Wiki pages during ordinary questions.

If a conversation produces durable knowledge, promote it only when:

- explicitly requested by the user, or
- the agent proposes promotion and the user agrees

Avoid turning every useful chat answer into a new page.

---

# 18. Conversation Handling

ChatGPT/Codex/Claude conversations should not automatically become Wiki knowledge.

Preferred pattern:

```text
conversation
    │
    ├── optional raw snapshot
    │
    └── distilled durable result
             ↓
       appropriate Wiki/System page
```

Persist:

- decisions
- conclusions
- important research insights
- durable open questions

Do not persist entire transcripts unless provenance/history is genuinely useful.

Principle:

> **Persist decisions and knowledge, not conversations.**

---

# 19. Provenance / Grounding

Use a lightweight but strict model.

Conceptually:

```text
Raw Source
    ↑
Source Page
    ↑
Concept / Entity / Question
    ↑
Synthesis / Project interpretation
```

Important load-bearing content should remain traceable to raw evidence.

Especially:

- numbers
- dates
- benchmark values
- experimental results
- direct quotes
- paper claims
- current software/model capabilities

Derived Wiki pages may provide navigation and synthesis, but should not become circular proof.

---

# 20. Inference / Disagreement Marking

Avoid fake numerical confidence.

Do not use uncalibrated fields like:

```yaml
confidence: 0.73
```

unless a real future calibration system exists.

Prefer qualitative markers where necessary:

- `[inferred]`
- `[ambiguous]`
- `[disputed]`
- `[outdated]`
- `[superseded]`

Exact syntax should be defined later in `SCHEMA.md` and `STYLE.md`.

---

# 21. Freshness Policy

Adopt the following semantic model.

## Timeless

Stable knowledge.

Example:

> Flow Matching defines a continuous-time transport objective...

## Snapshot

Historical observation tied to a date/source.

Example:

> As of 2026-08-20, model X supports...

## Pointer

Current volatile truth lives elsewhere.

Example:

> Current model availability: see the official provider documentation.
> Last observed: ... (as of YYYY-MM-DD)

Never store volatile present-tense facts without dates.

This matters for:

- model availability
- software versions
- pricing
- benchmarks claimed as SOTA
- organization leadership
- product capabilities
- current APIs
- current policies

---

# 22. Metadata Philosophy

Keep metadata minimal in v1.

Possible baseline:

```yaml
---
title: Flow Matching
type: concept
aliases:
  - FM
summary: ...
tags:
  - generative-model
sources:
  - raw/papers/...
created: 2026-08-20
updated: 2026-08-20
status: active
---
```

Do not prematurely create a large rigid ontology.

Prefer evolution from real use.

---

# 23. `summary` Field

Every Wiki page should probably have a concise summary field.

Reason:

- cheap relevance screening
- bounded context
- index generation
- future tiered retrieval
- easier agent handoff

Target:

1–2 sentences, useful without opening the full page.

The exact length limit can be decided later.

---

# 24. Index and Semantic Graph Separation

`_system/index.md` is bookkeeping/navigation.

Its links should **not** be treated as semantic knowledge edges.

Graph View should focus on `wiki/`.

Recommended later Obsidian graph exclusions:

```text
path:_system
path:raw
path:inbox
path:_staging
```

The meaningful graph is the relationship structure inside `wiki/`.

---

# 25. Lint Design

Use three authority levels.

## Mechanical Lint — safe auto-fix

Examples:

- broken links with unambiguous replacement
- missing index entry
- manifest inconsistency
- missing required metadata
- wrong path
- obvious alias normalization
- stale bookkeeping metadata

## Semantic Lint — suggest, do not silently fix

Examples:

- possible duplicate pages
- missing cross-links
- orphan concepts
- pages that may need split/merge
- weakly connected topics
- missing synthesis opportunity
- potentially stale claims

## Epistemic Lint — human decision required

Examples:

- scientific disagreement
- conflicting evidence
- research interpretation
- hypothesis status
- whether evidence is strong enough
- important conceptual restructuring

---

# 26. Single Writer Principle

Canonical Wiki writes should be coordinated by one maintainer at a time.

Do not allow multiple parallel agents to independently mutate the same Wiki pages/index/manifest.

Parallel workers may:

- read
- search
- analyze
- return drafts

But one canonical writer/orchestrator should apply the final coherent change.

This prevents:

- race conditions
- divergent schema
- inconsistent index state
- conflicting cascade updates

---

# 27. Safe Write Philosophy

For meaningful multi-page changes:

1. read current relevant files
2. formulate one logical change plan
3. apply changes
4. lint
5. inspect diff
6. checkpoint with Git

A full transaction engine is not required in v1.

Git + careful single-writer workflow is likely sufficient initially.

---

# 28. Git

Use Git locally for the Knowledge_Wiki.

Purpose:

- inspect agent changes
- rollback bad edits
- compare Codex vs Claude behavior
- audit major restructuring
- protect long-term knowledge

GitHub hosting is optional.

Synology Drive remains the synchronization layer.

Consider interactions between Git and Synology carefully during implementation.

---

# 29. Retrieval Roadmap

## Phase 1 — v1

Use:

- STATE.md
- index.md
- title
- aliases
- summary
- grep/ripgrep
- wikilinks
- backlinks
- Obsidian search

## Phase 2 — only when needed

Add:

- BM25 or similar local lexical search
- better page ranking

## Phase 3 — only after measured recall failures

Consider:

- graph retrieval
- Personalized PageRank
- hybrid search
- embeddings
- semantic reranking

Do not add vector DB / graph DB by default.

---

# 30. Obsidian Philosophy

Keep Obsidian simple in v1.

Core features:

- Markdown
- wikilinks
- backlinks
- search
- Graph View

Potential later additions:

- Bases
- Canvas
- Karpathy Wiki plugin
- Dataview
- other visualization/query plugins

Plugins must not become the authoritative storage model.

The vault should remain fully understandable as normal files without Obsidian.

---

# 31. Memory and Agent Portability

The Wiki itself is the portable memory.

The authoritative state must be reconstructible from:

```text
_system/
raw/
wiki/
```

Codex memory is not required.

Claude memory is not required.

ChatGPT memory is not required.

When switching agent:

```text
New agent
   ↓
read adapter
   ↓
read SCHEMA
read WORKFLOW
read STYLE
read PREFERENCES
read DECISIONS
read STATE
read index
read recent log
   ↓
continue maintenance
```

No migration of hidden agent caches or sessions should be necessary.

---

# 32. Desired Future Agent Compatibility

Current:

- ChatGPT for research thinking
- Codex for local canonical maintenance

Future possibilities:

- Claude Code
- Gemini CLI
- other Agent Skills-compatible tools
- future local agents

Design every core file as vendor-neutral Markdown/YAML/JSON.

Do not use proprietary metadata as source of truth.

---

# 33. What Should Remain Disposable

Examples:

```text
~/.codex/
~/.claude/
agent session logs
embedding databases
search indexes
runtime caches
temporary extracted chunks
temporary agent plans
```

These may improve performance, but deleting them must not destroy durable knowledge.

---

# 34. What Should Be Durable

There are only three real long-term asset classes.

## Evidence

`raw/`

## Knowledge

`wiki/`

## Protocol + persistent reasoning state

`_system/`

Everything else is infrastructure.

---

# 35. Important Research-Oriented Requirements

This Knowledge_Wiki is heavily research-oriented.

The system must work well for:

- academic papers
- equations
- figures
- architecture descriptions
- datasets
- benchmarks
- research comparisons
- evolving hypotheses
- open research questions
- experimental findings
- method relationships
- limitations
- contradictions between papers
- synthesis across literature
- project-specific research reasoning

Avoid shallow "paper summary" behavior.

Paper pages should preserve the technical details needed for future research reasoning.

---

# 36. Important Design Boundaries

Do not let Knowledge_Wiki become:

- daily operating system
- calendar
- task tracker
- email archive
- full chat archive
- general backup folder
- PDF dumping ground
- automatic "save everything" system
- model-specific memory

The Wiki should contain **durable knowledge**.

---

# 37. Open Questions — Do Not Assume These Are Final

These need to be designed next.

## Schema

- exact required metadata
- page creation threshold
- merge rules
- split rules
- status lifecycle
- alias rules
- contradiction syntax
- freshness syntax
- provenance syntax
- source-page vs concept-page boundary
- project-page structure
- question-page lifecycle

## Workflow

- exact Capture behavior
- exact Ingest sequence
- how to handle PDFs
- how to preserve source snapshots
- whether raw paper PDF and extracted Markdown coexist
- how to ingest web pages
- how to ingest ChatGPT discussions
- how to promote conversation output
- how cascade update is bounded
- whether the agent must propose a write plan before large changes

## Manifest

- exact JSON schema
- whether one file or JSONL
- content hash policy
- source identity
- duplicate detection
- how to track source-to-page many-to-many relations
- how to track `No material`

## State

- exact contents of STATE.md
- update frequency
- whether STATE is generated after every write or only major operations

## Index

- exact structure
- one global index vs type sections
- whether index should be generated from metadata

## Git

- commit granularity
- automatic vs explicit commit
- how Git interacts with Synology Drive
- backup strategy

## Obsidian

- initial settings
- graph filters
- attachment handling
- whether to install Karpathy Wiki plugin
- whether to use Bases
- whether to use Canvas
- whether raw files should appear in Obsidian navigation

## Agent portability

- canonical Agent Skill location
- thin AGENTS.md / CLAUDE.md format
- whether to create a vendor-neutral `skills/knowledge-wiki/`
- how Codex and Claude Code should discover the same skill

---

# 38. Recommended Implementation Order

Do not start with plugins.

Recommended sequence:

```text
1. Review and finalize top-level architecture
        ↓
2. Design _system/SCHEMA.md
        ↓
3. Design page templates
        ↓
4. Design _system/WORKFLOW.md
        ↓
5. Design _system/STYLE.md
        ↓
6. Design _system/PREFERENCES.md
        ↓
7. Initialize _system/DECISIONS.md
        ↓
8. Design AGENTS.md / CLAUDE.md adapters
        ↓
9. Design manifest schema
        ↓
10. Create directory structure
        ↓
11. Configure Git
        ↓
12. Configure Obsidian
        ↓
13. Configure Codex
        ↓
14. Pilot with 3–5 real sources
        ↓
15. Evaluate failure modes
        ↓
16. Revise schema
        ↓
17. Only then consider extra plugins/retrieval tooling
```

---

# 39. What Codex Should Do Next

## First task

Do **not** immediately build the full vault.

First:

1. Read this entire BOOTSTRAP file.
2. Review the referenced implementations where useful.
3. Critique the proposed architecture.
4. Identify:
   - unnecessary complexity
   - missing failure modes
   - hidden vendor lock-in
   - contradictions
   - issues specific to long-term academic research use
5. Preserve the design goals:
   - durable knowledge
   - source grounding
   - agent portability
   - minimal complexity
   - long-term maintainability
6. Propose a finalized top-level architecture.

Only after the top-level architecture is accepted should implementation begin.

## Second task

Design `_system/SCHEMA.md`.

The schema design should focus on:

- six page types
- page creation thresholds
- metadata
- lifecycle
- provenance
- freshness
- update vs create
- merge/split
- relationships
- research-specific requirements
- how disagreement is preserved

Do not over-engineer.

---

# 40. First Prompt to Use in Codex

Suggested initial prompt:

```text
Read _system/BOOTSTRAP.md carefully.

This file contains the distilled design decisions from a prior ChatGPT discussion about building my personal Karpathy-style Knowledge_Wiki in Obsidian.

Treat the design as a strong starting point, not immutable truth.

Do not create or modify the Wiki structure yet.

First:
1. Review the architecture critically.
2. Inspect the referenced LLM-Wiki implementations where useful.
3. Identify missing failure modes, unnecessary complexity, or portability problems.
4. Pay special attention to long-term academic research use, provenance, knowledge compounding, agent replaceability, and keeping the system simple.
5. Propose a finalized top-level architecture.

The system must remain model- and vendor-agnostic. Codex is the current maintainer, but Claude Code or another capable agent must be able to take over later using only the files in this vault.

After we finalize the top-level architecture, we will design _system/SCHEMA.md and implement the system step by step.
```

---

# 41. Current Design Summary in One Sentence

> **Knowledge_Wiki is a vendor-neutral, Obsidian-based, source-grounded external long-term memory where replaceable LLM agents continuously compile raw evidence into coherent, interconnected, updatable knowledge while the human retains epistemic control.**

---

# 42. Final Reminder to Future Agents

The most important invariant is not any specific folder or metadata field.

It is this:

> **The knowledge should compound.**

A successful ingest does not merely create another note.

It improves the existing knowledge graph:

- clearer concepts
- stronger connections
- explicit disagreement
- better questions
- better synthesis
- less duplication
- better provenance
- better future retrieval

If the Wiki only grows in file count, the design has failed.
