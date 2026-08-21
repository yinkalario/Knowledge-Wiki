**English** | [简体中文](README.zh-CN.md)

<h1 align="center">
  <img src="assets/knowledge-wiki-logo.png" alt="Knowledge Wiki logo" width="72" align="absmiddle">
  Knowledge Wiki
</h1>

<p align="center"><strong>A vendor-neutral, source-grounded knowledge base maintained by replaceable LLM agents.</strong></p>

A long-lived personal research knowledge base inspired by Andrej Karpathy's LLM Wiki idea. You choose sources, ask questions, and make final judgments; a replaceable LLM agent continuously compiles raw evidence into a coherent, searchable, and traceable Wiki.

> [!important] Current status
> This repository is a clean, unused starter template. The v1 structure, real-source workflow, and fresh Codex/Claude Code handoff were validated in a separate private pilot; no pilot sources, compiled knowledge, personal state, or operation history are included here.

## Why use Knowledge Wiki?

Imagine that you have read dozens of papers and saved hundreds of useful web pages. A normal file-chat or RAG tool can search those files and answer one question, but the answer usually disappears into chat history. The next question starts by searching the same pile again, and important connections remain scattered across separate documents.

The Karpathy-style LLM Wiki idea changes that loop: let an LLM continually compile new material into a maintained Wiki. Knowledge Wiki turns that idea into a practical, source-grounded Obsidian workflow that can be used every day.

### What this project adds

- **Knowledge compounds instead of piling up.** A new paper does not automatically become one more isolated summary. The agent searches what the Wiki already knows, updates existing Concepts and Entities, records durable Questions, and creates a cross-source Synthesis only when it adds a real comparison or conclusion.
- **Every important claim can be checked.** Original PDFs, web snapshots, and other evidence remain under `raw/`. Important numbers, quotations, results, and current facts point back to an exact page, section, figure, table, or snapshot.
- **You choose how deeply a source is read.** Standard Ingest handles everyday material efficiently, Deep Ingest follows the central argument and evidence chain closely, and Exhaustive Ingest supports reproduction, peer review, or section-by-section analysis.
- **You can ask without polluting the Wiki.** Query is read-only by default. If a discussion produces something worth keeping, Promote compiles only the durable conclusion rather than saving the whole conversation.
- **The agent is replaceable.** Codex, Claude Code, or another file-based agent can take over from the Vault itself. The durable memory is ordinary Markdown, raw evidence, and small bookkeeping files—not one vendor's chat history or hidden memory.
- **Cross-device work remains auditable.** Hashes prevent duplicate ingest, the manifest records what each source changed, Git reviews the text history, and raw evidence can be synchronized and backed up separately.
- **The system stays understandable.** It starts with five page types, Obsidian links, Search, Graph, and plain files. Databases, embeddings, and complex plugins are added only after a real retrieval problem appears.

In practice, this means you can ask, "What does my Wiki currently believe about this topic, why, and which sources disagree?" and receive an answer from one maintained body of knowledge rather than a stack of unrelated summaries.

## What belongs here?

Good candidates include:

- academic papers, technical reports, and standards;
- blogs, official documentation, and important web pages;
- durable concepts, methods, models, datasets, and tools;
- open research questions, hypotheses, and cross-source syntheses;
- durable conclusions from conversations that you explicitly Promote.

Poor candidates include:

- daily notes, reminders, tasks, and deadlines;
- temporary working notes;
- full email or chat archives;
- uncurated bookmark or PDF dumps;
- secrets, API keys, or private material that should not be sent to the active model.

Keep those in an operational vault or another purpose-built system.

## Repository and Vault layout

Open the repository root—not just `wiki/`—as the Obsidian Vault. Each top-level directory has a distinct role:

```text
Knowledge_Wiki/
├── wiki/                 Compiled, human-readable knowledge
│   ├── Home.md           Starting page and navigation
│   ├── concepts/         Ideas, mechanisms, and methods
│   ├── entities/         Models, tools, datasets, people, and organizations
│   ├── sources/          Reusable notes about individual sources
│   ├── questions/        Open questions and hypotheses
│   └── syntheses/        Cross-source comparisons and conclusions
├── _system/              Agent protocol and durable bookkeeping
│   ├── SCHEMA.md         Knowledge model and page rules
│   ├── WORKFLOW.md       Ingest, Query, Promote, and Lint procedures
│   ├── DECISIONS.md      Accepted architecture decisions and rationale
│   ├── templates/        Templates for the five knowledge-page types
│   └── index, manifest, STATE, and log files
├── raw/                  Canonical evidence retained for verification
│   ├── papers/           Original papers and reports
│   ├── web/              Captured web pages and snapshots
│   ├── conversations/    Promoted conversation evidence
│   ├── assets/           Attachments owned by raw sources
│   └── other/            Other canonical evidence
├── inbox/                Delivery area for material awaiting Ingest
│   └── attachments/      Attachments delivered with inbox sources
├── assets/               Images and other files owned by the Wiki itself
├── .obsidian/            Shared Obsidian configuration for this Vault
├── AGENTS.md             Codex entrypoint
├── CLAUDE.md             Claude Code entrypoint
├── README*.md            User documentation
└── .git/                 Local Git history on the designated commit machine
```

The separation is deliberate: `inbox/` receives material, `raw/` preserves the evidence, and `wiki/` contains the knowledge compiled from that evidence. `_system/` tells a fresh agent how to perform that work without relying on previous chat context. Actual files under `raw/` and `inbox/` are excluded from Git but remain inside the Vault for file synchronization; their directory markers remain in Git so a new clone has the expected structure. `.git/` is local to the designated commit machine and should not be synchronized by a file-sync service.

## Five-minute Quick Start

### 1. Install Obsidian and the Web Clipper

- Install [Obsidian](https://obsidian.md/download) for your operating system.
- Install the official [Obsidian Web Clipper](https://obsidian.md/clipper) browser extension for Chromium-based browsers, Firefox, Safari, or Edge.

Web Clipper is the easiest way to send articles and selected passages into the Wiki as Markdown. It is recommended for capture, but it is not a runtime dependency: PDFs, local files, pasted text, and direct URLs also work.

### 2. Open the entire repository as one Vault

Clone, download, or locate the `Knowledge_Wiki` folder. In Obsidian, choose **Open folder as vault** and select the repository root—the folder that contains `AGENTS.md`, `_system/`, `wiki/`, `raw/`, and `inbox/`.

Do not open only `wiki/` as the Vault. The agent needs the protocol, evidence, inbox, and bookkeeping directories together. If you plan to ingest private or copyrighted material, work from a private personal copy rather than a public fork.

### 3. Connect a file-based agent

Start Codex, Claude Code, or another file-based coding agent with the Vault root as its working directory.

- Codex enters through `AGENTS.md`.
- Claude Code enters through `CLAUDE.md`.
- Both follow the same `_system/SCHEMA.md` and `_system/WORKFLOW.md` without needing earlier chat context.

For a first read-only check, ask:

```text
Read the repository instructions, orient yourself to this Knowledge Wiki, and tell me when you are ready. Do not modify files yet.
```

Never let two agents write to the Vault at the same time. A device without `.git/` may ingest and lint, but the designated commit machine should review and commit the synchronized changes later.

### 4. Put the first source in `inbox/`

Choose one of these paths:

- **Web article:** open Web Clipper, select this Vault, set the destination folder to `inbox/`, review the captured article, and click **Add to Obsidian**.
- **PDF, Markdown, or text file:** copy the file into `inbox/` with Finder, File Explorer, or your file-sync service.
- **Direct URL or pasted text:** give it to the agent and explicitly request Ingest.

Use `inbox/` as the delivery area. Do not manually place unprocessed sources under `wiki/`; the agent will create canonical raw evidence and compiled pages in the correct locations.

### 5. Run the first Ingest

For ordinary material, Standard Ingest is the default:

```text
Process the new material in inbox using Standard Ingest.
```

The agent identifies unprocessed files by manifest and hash, preserves canonical raw evidence, checks for duplicates, searches existing knowledge, updates before creating, validates links and provenance, and reports every created or updated file. If several new sources are present, it lists and processes them in sequence. An inbox delivery copy is removed only after all cleanup conditions pass; otherwise it remains in place with an explanation.

### 6. Open the result and ask a question

Start at `wiki/Home.md`, then open the new Source page and any Concept or Entity pages it updated. Try a read-only Query:

```text
According to my Wiki, what are the main differences between Flow Matching and Diffusion?
```

Query does not modify the Vault by default. If the answer contains a durable conclusion worth keeping, the agent proposes a Promote operation.

## Main operating modes

### Standard Ingest (default)

Use Standard Ingest for ordinary papers, blogs, articles, and official documentation. The agent uses the index, summaries, aliases, and targeted search to select candidate pages, then updates existing knowledge whenever possible. For papers, Standard still records the research question, method, necessary equations, experimental setup, main results, and limitations. Token-aware means avoiding wasteful reading, not reducing a paper to its abstract.

```text
Process the new material in inbox.
```

### Deep Ingest

Use Deep Ingest for foundational papers, work you expect to cite seriously, or sources whose method, evidence, and limitations need close study. It first maps the paper, covers the core argument and evidence chain, and selectively compiles details that will be useful for future understanding, comparison, citation, or reuse. Low-frequency details that are not compiled remain accessible through locators and can be read from raw evidence during a later Query. Deep costs more tokens, must be requested explicitly, and does not exhaustively inspect every appendix page by default.

```text
Use Deep Ingest for the new paper in inbox.
```

### Exhaustive Ingest

Use Exhaustive Ingest for reproduction, peer review, section-by-section technical examination, or any case where you explicitly need complete coverage of the main text, appendices, equations, figures, experiments, and reproducibility details. It targets material completeness, may run in batches, and is the most token-intensive mode. It must be requested explicitly.

```text
Use Exhaustive Ingest for the new paper in inbox.
```

## How papers are read and stored

These four approaches complement one another:

| Need | Recommended mode | Result |
|---|---|---|
| Build a reliable, reusable research note | Standard Ingest | A structured Source page plus targeted updates to related knowledge |
| Understand a foundational paper in depth | Deep Ingest | Core argument and evidence-chain coverage with selective durable compilation |
| Reproduce, review, or examine every material section | Exhaustive Ingest | Material-complete coverage of methods, equations, experiments, appendices, limitations, and reproducibility details |
| Inspect a particular equation, figure, or experiment | Query | Open only the relevant raw pages and necessary context; do not write by default |

There is no rule such as “keep exactly one to three equations.” An empirical paper with no important equation should not be forced to include one, while a mathematical paper may require many. In Standard and Deep, the question is whether omitting an equation would obstruct understanding the central contribution, explaining results, comparing methods, or judging reproducibility. Exhaustive covers every material equation. When an equation is retained, explain its symbols, assumptions, role, necessary derivation logic, and source locator.

The “deep” in Deep Ingest means complete understanding of the core argument and evidence chain, not copying every detail into the Wiki. The agent must report what it read, what it inspected visually, and which appendices were deliberately deferred. Later questions can follow locators back to the raw source. Exhaustive Ingest is also not a verbatim copy: references, generic background, and repetition may be compressed, but every detail that could change a research judgment or reproduction result must be examined. Long exhaustive work is processed by section or chapter, with resumable progress recorded in `STATE.md` until all planned coverage is complete.

### Promote

When a query or discussion produces durable knowledge, compile it back into the Wiki:

```text
This answer is worth keeping. Compile it into the Wiki, preserve raw provenance, update existing pages before creating new ones, and do not save the full conversation.
```

### Research Mode

During a research session, you can authorize the agent to save stable, sourced, reusable conclusions automatically:

```text
Enable Research Mode for this session. Automatically compile stable, sourced, reusable research conclusions into the Wiki. Do not save the full conversation.
```

Research Mode lasts only for the current session. Merge, rename, delete, major conflict, and schema changes still require confirmation. The only narrow exception is verified cleanup of an untracked inbox delivery copy after a successful ingest, as defined by the authoritative Workflow.

## More copyable prompts

### Review what the Wiki already knows

```text
According to my Wiki, summarize the current understanding of target speaker extraction and identify areas where the evidence is weak.
```

### Compare methods

```text
Compare method A and method B using evidence already in the Wiki. Separate claims reported by sources from our own inference.
```

### Save a research question

```text
This question is worth tracking over time. Check whether a related Question page already exists before deciding whether to update or create one.
```

### Run a health check

```text
Lint this Wiki according to the v1 WORKFLOW. Report broken links, manifest/raw problems, exact duplicates, and needs_review pages. Do not automatically resolve scientific conflicts.
```

### Inspect current maintenance state

```text
Read _system/STATE.md and the recent log, then tell me what is most worth doing next in this Wiki.
```

## What happens during an Ingest?

```text
Source / inbox / URL
        ↓
Capture immutable raw + SHA-256 duplicate gate
        ↓
Read source at the selected depth
        ↓
Index + summary + aliases + targeted search
        ↓
New / Update / Disputed / No material
        ↓
Targeted Wiki changes + bounded cascade
        ↓
Validate provenance, links, and metadata
        ↓
Update index, manifest, log, and (only if needed) STATE
        ↓
Commit, then remove only hash-verified untracked inbox copies
```

One to ten material page changes are within ordinary ingest authority. If more than ten pages are expected to change, the agent first lists the affected pages and the material reason for each, then waits for confirmation. Page count is not a quality target; every changed page must receive a material update.

## Browsing in Obsidian

- Start from `wiki/Home.md`.
- Use Search to find text.
- Use Backlinks and Outgoing Links to understand relationships.
- Use the global Graph after several ingests to see topic clusters, bridge pages, and isolated areas. Graph View excludes `_system`, `raw`, and `inbox`.
- Use Local Graph only when you want the immediate neighborhood of one connected page; it is expected to be sparse in a new Wiki.
- New attachments default to `inbox/attachments/` before ingest moves them into the appropriate raw layer.

`_system/index.md` is a compact candidate catalog for agents. It is not a semantic knowledge page and must not be treated as evidence.

### Where are Properties?

`wiki/Home.md` is a navigation page and has no ordinary knowledge-page frontmatter, so it does not display knowledge Properties. After your first ingest, open any Concept, Source, Entity, Question, or Synthesis page. Its header should display fields including `title`, `type`, `summary`, `sources`, and `needs_review`.

If Properties are still not visible:

1. Open **Settings → Editor**.
2. Set **Properties in document** to **Visible**.
3. If you see raw YAML between `---` delimiters, the current setting is **Source**; change it to **Visible**.

You can also enable Obsidian's **Properties view** core plugin to inspect properties used across the Vault. It is not a Knowledge_Wiki runtime dependency.

### Global Graph and Local Graph

**Graph view** is an Obsidian core plugin. If graph commands are missing, enable it under **Settings → Core plugins → Graph view**.

- To open the global Graph, use the ribbon's **Open graph view** button or run **Open graph view** from the Command Palette. It shows the whole Vault and becomes useful once several sources have created enough relationships to reveal clusters and gaps.
- To open a Local Graph, first open a knowledge page and run **Open local graph** from the Command Palette (`Cmd+P` on macOS, usually `Ctrl+P` on Windows and Linux). It shows only notes connected to the active page and can expand by depth.

For a new or lightly connected Wiki, Search, Backlinks, Outgoing Links, and the global Graph are usually more informative than Local Graph. A sparse graph is normal; never manufacture links merely to make either graph look richer.

## Reviewing and recovering changes

After important writes, inspect:

```bash
git status --short
git diff
git log --oneline
```

One ingest should produce one logical diff. Do not run destructive Git commands without understanding their effect. If you need to undo something, ask the agent to identify the exact target files and explain the recovery path first.

## Codex, Claude Code, and other agents

Codex and Claude Code can both maintain this Wiki, but only one may act as the canonical writer at a time. When switching:

1. Let the current agent finish and inspect its diff.
2. Wait for your file-sync service, if any, to finish syncing.
3. Open the same Vault with the other agent.
4. Let it read its adapter and the authoritative `_system` files.
5. Do not migrate old conversation history, cache, memory, or embeddings.

A future agent can take over as long as it can read and write ordinary files, search Markdown, and follow the `_system` protocol.

## File synchronization and the single-writer rule

File-sync services such as Synology Drive, iCloud Drive, or Dropbox synchronize files but do not coordinate concurrent writers. Do not edit the same set of files simultaneously from two computers, two agents, or Obsidian and an automation tool. Before switching, verify that synchronization has completed.

Git history is a local audit mechanism for `wiki/`, `_system/`, documentation, and directory markers. Actual `raw/` and `inbox/` content stays in the Vault for file synchronization but is excluded from Git; keep an independent, versioned backup of raw evidence because manifest hashes cannot restore missing files.

Keep `.git/` local to the designated commit machine and exclude it from Synology Drive or any other file-sync service. Other devices may edit the synchronized ordinary Vault files without carrying Git metadata.

## FAQ

### Why did this source not produce a Source page?

A Source page is not mandatory for every ingest. If a source only strengthens an existing Concept or has little independent reuse value, updating the existing page better supports compounding knowledge.

### What does No material mean?

The source is preserved in raw, but it did not add knowledge worth compiling into the current Wiki. The manifest and log record the result without creating an empty page.

### Must I delete inbox files manually after Ingest?

Usually not. The agent may remove an untracked inbox delivery copy only after the canonical raw exists, its SHA-256 is identical, manifest/bookkeeping/lint checks pass, the logical commit succeeds, and source-owned attachments are handled. If any condition fails, the file remains in the inbox and the agent explains why. Canonical evidence under `raw/` is never removed by this cleanup.

This applies only to future, verified ingests. It does not authorize bulk deletion of historical or ambiguous inbox content.

### Why does the agent ask before changing more than ten pages?

A broad cascade may be justified, but it may also be weak-association expansion. Confirmation lets you inspect the material reason for every affected page first.

### Why does Query not save automatically?

Ordinary Query is read-only to prevent chat answers from polluting the Wiki. A durable conclusion triggers a Promote proposal; you can also enable Research Mode explicitly.

### What language will compiled Wiki content use?

An explicit output-language request takes priority. Otherwise, the current prompt determines the language of the current changes: if it contains any Chinese character, the agent writes in Chinese; if it is entirely English, the agent writes in English. This applies to both new pages and updates, so one page may legitimately contain both languages over time. Canonical technical terms and useful Chinese/English aliases are preserved for retrieval.

### Will system files be archived automatically?

There is no background watcher. During user-triggered maintenance, Lint, Ingest, schema review, or handoff, the agent checks whether system-file growth is causing real navigation or review cost. It may keep the bounded `STATE.md` tidy after durable outcomes are recorded, but creating archive directories, moving history, splitting authoritative protocols, or sharding indexes always requires a concrete proposal and your confirmation. No archive structure is created before it is needed.

### Do I need embeddings, a vector database, or a Wiki plugin?

Not in v1. Start with the index, summaries, aliases, `rg`, wikilinks, and Obsidian Search. Add retrieval infrastructure only after repeated, documented retrieval failures.

### How should I handle a long book or report?

For material longer than roughly 100,000 characters or 40 pages, build a section or chapter map first. Process books, long reports, and transcripts in batches rather than attempting one enormous deep pass.

### Should a paper use Standard, Deep, or Exhaustive?

Use Standard for most papers; it already produces a research-usable structured reading note. Use Deep for foundational work, serious citation, or close examination of the evidence chain. Use Exhaustive only for reproduction, peer review, or explicit section-and-appendix completeness. You can also begin with Standard and later upgrade to Deep, or inspect a particular equation, table, appendix, or section on demand without reprocessing the whole paper.

## Sharing, copyright, and privacy

This repository intentionally ships without raw sources, compiled knowledge, personal `STATE`, or operation history. Once you begin using it, do not publish the live personal Vault directly: it may contain copyrighted PDFs, web snapshots, private conversations, research directions, and personal knowledge.

For public sharing, export a separate starter template containing only:

- `README.md` and `README.zh-CN.md`;
- `AGENTS.md` and `CLAUDE.md`;
- the `_system` protocol and templates;
- empty directories;
- self-authored, synthetic, or clearly redistributable examples.

Do not publish personal `raw/`, `wiki/`, `STATE`, manifest, log, conversations, credentials, or secrets. If you customize the starter for redistribution, review the diff and export a fresh clean copy.

The starter protocol and documentation are released under the repository's [MIT License](LICENSE). Sources you ingest keep their own copyright and license terms. Adding a sensitive file to `.gitignore` after committing it does not remove it from Git history, so make the personal repository private before the first ingest when appropriate.

## Authoritative documentation

- [Schema](_system/SCHEMA.md): page model, metadata, provenance, and lifecycle.
- [Workflow](_system/WORKFLOW.md): Ingest, Query, Promote, Research Mode, and Lint.
- [Decisions](_system/DECISIONS.md): curated current architecture and rationale, not a change log.
- [Current State](_system/STATE.md): current focus and maintenance backlog.
- [Templates](_system/templates/): the five page templates.
- [Historical Bootstrap](_system/BOOTSTRAP.md): design history, not operational authority.
