**English** | [简体中文](README.zh-CN.md)

<p align="center">
  <img src="assets/knowledge-wiki-logo.png" alt="Knowledge Wiki logo" width="180">
</p>

# Knowledge_Wiki

A long-lived personal research knowledge base inspired by Andrej Karpathy's LLM Wiki idea. You choose sources, ask questions, and make final judgments; a replaceable LLM agent continuously compiles raw evidence into a coherent, searchable, and traceable Wiki.

> [!important] Current status
> This repository is a clean, unused starter template. The v1 structure, real-source workflow, and fresh Codex/Claude Code handoff were validated in a separate private pilot; no pilot sources, compiled knowledge, personal state, or operation history are included here.

## What problem does it solve?

Ordinary RAG and file-chat systems repeatedly search the original material for every question. Knowledge_Wiki performs a compilation step during ingest: a new source updates existing Concepts, Entities, Questions, and Syntheses instead of merely adding another isolated summary. Later queries read the compiled Wiki first and return to raw evidence only when needed.

Core principles:

- Separate raw evidence from compiled knowledge.
- Update before create.
- Keep Query read-only by default.
- Make important claims traceable to raw sources.
- Treat agents as replaceable and Vault files as durable memory.
- Start simple and add tooling only after real failures appear.

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

## Five-minute Quick Start

### 1. Open the Vault

Clone or download this repository, then open its root directory as an Obsidian Vault. Every file also remains usable in an ordinary Markdown editor. If you will add private or copyrighted sources, use a private personal repository rather than a public fork.

### 2. Start a file-based agent

Launch Codex or Claude Code from the Vault root:

- Codex enters through `AGENTS.md`.
- Claude Code enters through `CLAUDE.md`.
- Both ultimately follow the same `_system/SCHEMA.md` and `_system/WORKFLOW.md`.

Never let two agents write to the Vault at the same time.

### 3. Provide the first source

You can:

- place a PDF, Markdown file, or text file in `inbox/`;
- give the agent a URL directly;
- paste text and explicitly ask the agent to ingest it.

Then say:

```text
Process the new material in inbox.
```

You do not need to find or type the filename. The agent compares inbox files with the manifest and hashes to find unprocessed material. If several new sources are present, it lists and processes them in sequence. After a successful ingest and commit, it removes an untracked inbox delivery copy only when the canonical raw file and inbox file have identical hashes. Anything ambiguous or insufficiently verified stays in the inbox and is reported.

Alternatively:

```text
Use Standard Ingest for this blog:
https://example.com/article
```

The agent captures the raw source, checks for duplicates, searches existing knowledge, updates or creates the necessary pages, and reports every change.

### 4. Ask a question

```text
According to my Wiki, what are the main differences between Flow Matching and Diffusion?
```

Query does not modify the Vault by default. If an answer produces durable knowledge, the agent proposes a Promote operation.

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
- Graph View excludes `_system`, `raw`, and `inbox`.
- New attachments default to `inbox/attachments/` before ingest moves them into the appropriate raw layer.

`_system/index.md` is a compact candidate catalog for agents. It is not a semantic knowledge page and must not be treated as evidence.

### Where are Properties?

`wiki/Home.md` is a navigation page and has no ordinary knowledge-page frontmatter, so it does not display knowledge Properties. After your first ingest, open any Concept, Source, Entity, Question, or Synthesis page. Its header should display fields including `title`, `type`, `summary`, `sources`, and `needs_review`.

If Properties are still not visible:

1. Open **Settings → Editor**.
2. Set **Properties in document** to **Visible**.
3. If you see raw YAML between `---` delimiters, the current setting is **Source**; change it to **Visible**.

You can also enable Obsidian's **Properties view** core plugin to inspect properties used across the Vault. It is not a Knowledge_Wiki runtime dependency.

### How do I open the Local Graph?

1. Open the knowledge page you want to inspect.
2. Open the Command Palette (`Cmd+P` on macOS, usually `Ctrl+P` on Windows and Linux).
3. Search for and run **Open local graph**.

If the command is missing, verify that **Graph view** is enabled under **Settings → Core plugins**. Local Graph shows only pages connected to the current page. A sparse graph is normal when the Wiki is small; never manufacture links merely to improve its appearance.

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

Git history is a local audit mechanism. Do not assume that the hidden `.git` directory is automatically synchronized or backed up by your file-sync service.

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
- [Decisions](_system/DECISIONS.md): accepted architecture decisions.
- [Current State](_system/STATE.md): current focus and maintenance backlog.
- [Templates](_system/templates/): the five page templates.
- [Historical Bootstrap](_system/BOOTSTRAP.md): design history, not operational authority.
