**English** | [简体中文](README.zh-CN.md)

<h1 align="center">
  <img src="assets/knowledge-wiki-logo.png" alt="Knowledge Wiki logo" width="72" align="absmiddle">
  Knowledge Wiki
</h1>

<p align="center"><strong>Read in Zotero. Build reusable knowledge in Markdown. Keep the agent replaceable.</strong></p>

Knowledge Wiki turns papers, articles, and research discussions into an evolving, source-grounded knowledge base. Inspired by the LLM Wiki approach, it asks an agent to update existing understanding, connect related findings, preserve disagreements, and retain evidence—not merely generate a new summary for every file.

> [!IMPORTANT]
> **V2 supports both Zotero and Vault-only workflows.** Zotero is optional. The setup below covers a local Mac or Windows computer and a personal Zotero library. Shared/group-library automation is outside the current Wiki protocol. Setup instructions were checked on **2026-09-30** against upstream documentation and a local `zotero-mcp` 0.13.1 installation; this is not a claim that every client/OS combination has been tested.

## Start here

- [What v2 stores and where](#what-v2-stores-and-where)
- [Ask an agent to set it up](#ask-an-agent-to-set-it-up)
- [1. Prepare your Vault and agent](#1-prepare-your-vault-and-agent)
- [2. Prepare Zotero and PDF sync](#2-prepare-zotero-and-pdf-sync)
- [3. Install Zotero MCP](#3-install-zotero-mcp)
- [4. Connect Codex](#4-connect-codex)
- [5. Connect Claude](#5-connect-claude)
- [6. Enable collection writes](#6-enable-collection-writes)
- [7. Bind your library and collections](#7-bind-your-library-and-collections)
- [8. Verify the connection](#8-verify-the-connection)
- [9. Ingest your first source](#9-ingest-your-first-source)
- [Troubleshooting](#troubleshooting)
- [Everyday operations](#main-operating-modes), [Obsidian](#browsing-in-obsidian), [sync and backup](#file-synchronization-and-the-single-writer-rule)

## What v2 stores and where

| Material | Owner and location | What the Wiki retains |
|---|---|---|
| PDF imported through Zotero | Zotero stored attachment; Zotero Storage or WebDAV sync | Exact attachment identity, file hash, version, page links, reading coverage, compiled notes; **no second PDF in Vault raw** |
| PDF delivered to Vault `inbox/` | Canonical copy in `raw/papers/` | Existing Vault-only ingest and citations remain supported |
| Web Clipper Markdown, local text, web captures | Vault `inbox/` → appropriate `raw/` directory | Original evidence plus compiled knowledge |
| Zotero highlights/comments/child notes used in compilation | Originals in Zotero; immutable selected snapshots in `raw/other/`, necessary images in `raw/assets/` | What was actually used, original keys/locators and hashes; not a complete PDF backup |
| Compiled knowledge | `wiki/` | Source, Concept, Entity, Question, Synthesis—still only five page types |
| Protocol and handoff | `_system/` | Plain Markdown/YAML/JSON; no dependency on a particular model's chat history |

Zotero manages literature metadata, reading, annotations and attachments. Obsidian displays the Markdown Wiki and captures non-PDF sources. The agent maintains the knowledge and checks the originals when needed. A Zotero collection is an organizational membership, not a second PDF copy; a paper can belong to several collections.

Source notes include links such as `zotero://open-pdf/library/items/ATTACHMENT_KEY?page=7`. Obsidian can hand these to the installed Zotero app. The link opens the **current attachment**; the recorded SHA-256 is what lets an agent check that its bytes match the cited version. Keep cited old versions as separate attachments. Collection changes never alter the definition of the PDF hash. Obsidian Graph uses internal Wiki links; external Zotero URLs are not graph nodes.

There is no required vector database, embedding subscription, watcher, or scheduled ingest. Standard Ingest first searches existing summaries and pages, then reads enough original evidence for the task. Deep and Exhaustive are explicit choices.

## Ask an agent to set it up

You can give [this English README](https://github.com/yinkalario/Knowledge-Wiki/blob/main/README.md) or the [Chinese README](https://github.com/yinkalario/Knowledge-Wiki/blob/main/README.zh-CN.md) to **ChatGPT, Codex, or Claude**. The instructions and setup prompt are client-neutral. If the assistant cannot fetch the page, paste the README text; a local agent can read the file directly. This is an alternative to following the manual steps below, not an additional installation.

**Check the agent's actual access first.** A chat with no local tools can explain and tailor commands but cannot install software, edit your Vault, or access local Zotero. Use a local Codex/Claude Code workspace, or another explicitly connected environment with the necessary permissions, for direct setup. Zotero MCP alone does not grant access to your Vault files.

| Your current environment | How to use this guide |
|---|---|
| ChatGPT or Claude chat without local tools | Read/paste the README, ask for tailored instructions, and perform local steps yourself. |
| Local Codex desktop/CLI | Grant workspace and execution access; use `AGENTS.md`, step 4 for MCP, and the common acceptance checks. |
| Local Claude Code | Grant workspace and execution access; use `CLAUDE.md`, step 5 for MCP, and the same acceptance checks. |
| Claude Desktop | Connect Zotero using step 5. Wiki writes and installation additionally require suitable local file/execution tools; verify access before delegating. |

Codex and Claude Code are equal maintenance entrypoints: both use the same `_system/` protocol, source identities, templates and manifest. They do not need each other's chat history. Their client configurations differ; do not paste Codex TOML into Claude JSON or vice versa. See [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp) and [Claude Code MCP](https://code.claude.com/docs/en/mcp).

Copy this prompt and fill the four fields:

```text
Help me set up Knowledge Wiki v2 using this README:
https://github.com/yinkalario/Knowledge-Wiki/blob/main/README.md

OS: <macOS / Windows>
Target local client: <Codex desktop / Codex CLI / Claude Code / Claude Desktop / other>
Vault: <existing folder or desired new folder>
Use Zotero: <yes / no>

First establish whether you have local filesystem, terminal, and MCP access. If not,
give me the exact manual steps and do not claim to have performed them.
For Codex read AGENTS.md; for Claude Code read CLAUDE.md. Both must follow the
authoritative _system files. Configure the target client using its own instructions
in this README, not the client currently explaining them. If both local clients
are requested, register and verify each independently; do not install the tool twice.
Inspect existing installations/configuration before making changes. Reuse working
components. Back up a client config before a targeted merge; preserve other servers.
For a new Vault use the public starter; never overwrite an existing personal Wiki.

If you can execute locally, install missing prerequisites and zotero-mcp-server[pdf],
register one local STDIO server using its actual absolute executable path, and verify
it. Use local Zotero reads. For automatic Topics/Methods filing, check the installed
Zotero version and configure its supported write route. Let me complete account
sign-in, secret entry, and Zotero authorization dialogs locally; never print secrets.
Keep client config/credentials outside the Vault. Do not run install-skill, overwrite
Wiki adapters, build an embedding index, or expose a public tunnel as setup shortcuts.

Resolve my stable personal-library user ID and collection keys, then update only
_system/zotero-collections.md for this binding. Reuse existing roots. If required
roots do not exist or meanings are ambiguous, propose the exact minimal structure
before creating it. Projects and Archive are user-managed and protected.
Run the read-only acceptance checks below. Do not ingest, move papers, or rewrite
existing collections merely to test setup. Report what passed, what was actually
changed, remaining manual actions, and the exact first-ingest prompt I can use.
```

Ordinary ChatGPT web developer-mode connections use a remote MCP endpoint, not the local STDIO command below. Account capabilities vary. Remote MCP also does not by itself provide local Vault access. This guide uses local clients; it does not publish Zotero through an unauthenticated tunnel. See [OpenAI's developer-mode guide](https://developers.openai.com/api/docs/guides/developer-mode) if you intentionally need a separate remote deployment.

<a id="five-minute-quick-start"></a>

## 1. Prepare your Vault and agent

1. Install [Obsidian](https://obsidian.md/download). For web-to-Markdown capture, optionally install [Obsidian Web Clipper](https://obsidian.md/clipper).
2. Get the **public starter**, not another person's active Vault. Download **Code → Download ZIP** from [the repository](https://github.com/yinkalario/Knowledge-Wiki), extract it, and choose a private working folder. With Git installed, the equivalent is:

   ```bash
   git clone https://github.com/yinkalario/Knowledge-Wiki.git Knowledge_Wiki
   ```

   A clone still has the public starter as `origin`; it is not your personal backup remote. Before publishing your own commits, configure your own private repository. ZIP users can work without Git and initialize a private repository later.
3. In Obsidian choose **Open folder as vault**, selecting the whole folder containing `_system/`, `wiki/`, `raw/`, `inbox/`, and the adapters.
4. Install/sign in to your chosen local client: [Codex](https://learn.chatgpt.com/docs/quickstart) or [Claude Code](https://code.claude.com/docs/en/overview). Add/open the Vault root as the local workspace. A cloud checkout is not automatically connected to the Zotero running on your computer.
5. Ask: “Read the repository instructions and orient yourself to this Wiki. Do not modify files yet.” Codex uses `AGENTS.md`; Claude Code uses `CLAUDE.md`; both obey `_system/`.

Do not copy starter files wholesale over an existing Vault: keep its knowledge, raw, manifest and state. **Without Zotero, skip steps 2–8 and use the Vault entry in step 9.**

Versions are Git **branches**: `main` is the latest maintained version; `v1` preserves the pre-Zotero edition; `v2` is the V2 release line. New users start with `main`. Branches do not synchronize themselves; repository maintainers publish V2 updates to both `main` and `v2`.

<a id="zotero-in-v2-optional"></a>

## 2. Prepare Zotero and PDF sync

Install [Zotero and, optionally, Zotero Connector](https://www.zotero.org/download/). Use Zotero 7+ for local access; the write route is chosen in step 6. Better BibTeX is optional for citation keys and is **not required** by this Wiki or MCP setup.

1. Sign in under **Zotero Settings → Sync** on each device. Metadata and annotations use Zotero account sync. Choose Zotero Storage or WebDAV for attachments; for WebDAV enter your provider/NAS URL and credentials in Zotero and complete **Verify Server**. WebDAV syncs attachment files, not the live Zotero database. See [Zotero syncing](https://www.zotero.org/support/sync) and [Sync settings](https://www.zotero.org/support/preferences/sync).
2. Import one PDF as a **stored attachment**, using a paper's metadata record when available. Open it in Zotero to ensure it is downloaded and readable. A linked file outside Zotero storage is not the ordinary Zotero file-sync route. See [adding items](https://www.zotero.org/support/adding_items_to_zotero).
3. Enable **Settings → Advanced → Miscellaneous → Allow other applications on this computer to communicate with Zotero**. On macOS Settings is in the Zotero menu; on Windows it is under Edit. Keep Zotero running during local MCP use. See [upstream local setup](https://github.com/54yyyu/zotero-mcp/blob/main/docs/getting-started.md#configure-zotero).

The local managed/downloaded PDF is necessary for local reading and hashing; keeping PDFs in Zotero does not mean the computer has no PDF bytes. Do not move `zotero.sqlite` into your NAS/Obsidian sync folder. iPad/iPhone/Android can continue reading and annotating in Zotero; install MCP only on computers where the agent will read originals.

## 3. Install Zotero MCP

This guide uses the third-party [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) project. It is not an OpenAI- or Zotero-official server. A similarly named plugin in a directory may use another implementation: do not configure two copies accidentally.

Use **one installation method**. Below, `uv` manages an isolated Python tool environment. The `pdf` extra supplies page-image support; semantic search is unnecessary for the Wiki's normal workflow. Package extras and requirements are defined in the project's [package configuration](https://github.com/54yyyu/zotero-mcp/blob/main/pyproject.toml).

### macOS: Terminal

If `uv --version` works, skip its installation. Otherwise use the [official uv installer](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen Terminal, then run:

```bash
uv --version
uv python install 3.12
uv tool install --python 3.12 "zotero-mcp-server[pdf]"
uv tool update-shell
```

Open a new Terminal again and verify:

```bash
zotero-mcp version
command -v zotero-mcp
uv tool dir --bin
```

Record the actual executable path, for example `/Users/YOUR_NAME/.local/bin/zotero-mcp`. Your installation may use a different directory.

### Windows: native PowerShell

For a beginner using native Windows Zotero, use native PowerShell and a native client. WSL is an optional separate environment; it is not required and is not automatically simpler for this local integration.

If `uv --version` fails, run the [official Windows installer](https://docs.astral.sh/uv/getting-started/installation/):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen PowerShell, then run:

```powershell
uv --version
uv python install 3.12
uv tool install --python 3.12 "zotero-mcp-server[pdf]"
uv tool update-shell
```

Open a new PowerShell window and verify:

```powershell
zotero-mcp version
(Get-Command zotero-mcp).Source
uv tool dir --bin
```

Record the real `.exe` path, for example `C:\Users\YOUR_NAME\.local\bin\zotero-mcp.exe`. If lookup still fails, inspect the directory printed by `uv tool dir --bin` and restart the client after updating PATH. Do not paste a Mac path into Windows.

If the package is already installed with uv but lacks PDF support, record `zotero-mcp version` and use `uv tool install --force "zotero-mcp-server[pdf]"`, then reconnect the client. This may update the package. If it was installed with pipx/pip, use that same environment instead of layering another installation. See [uv tool environments](https://docs.astral.sh/uv/guides/tools/).

**Do not run `zotero-mcp install-skill` for this setup:** it may modify agent entrypoints. We use MCP and retain this Wiki's adapters. `zotero-mcp setup` is an alternative client configurator, not a prerequisite; avoid running it on top of a working manual configuration. No `update-db`, embedding model, or OpenAI API key is needed for the baseline route.

## 4. Connect Codex

Choose **one** of GUI, config file, or CLI. The program path is the actual output from step 3, not the package name `zotero-mcp-server`. Codex's GUI works without a `codex` executable on your shell PATH.

### Desktop GUI

Open **Settings → MCP servers → Add server**. Some builds expose this as **Plugins → Add → Add MCP server**. Set:

| Field | Value |
|---|---|
| Name | `zotero` |
| Type | `STDIO` |
| Command to launch | Absolute `zotero-mcp` / `zotero-mcp.exe` path |
| Arguments | No arguments; remove empty argument rows |
| Environment variable name | `ZOTERO_LOCAL` — all uppercase |
| Environment variable value | `true` |
| Environment passthrough | Empty for this baseline |
| Working directory | Leave unset |

Save, enable the server, restart/reconnect it, and start a new chat if the tool list has not refreshed. The installed server defaults to STDIO when invoked without arguments. [Official Codex MCP setup](https://learn.chatgpt.com/docs/extend/mcp).

### Config file alternative

Merge into the active user-level `~/.codex/config.toml` (Windows normally `%USERPROFILE%\.codex\config.toml`; a custom `CODEX_HOME` changes the location). Preserve existing settings and avoid a duplicate `[mcp_servers.zotero]` table. Use the GUI's active configuration if unsure.

macOS example:

```toml
[mcp_servers.zotero]
command = "/Users/YOUR_NAME/.local/bin/zotero-mcp"

[mcp_servers.zotero.env]
ZOTERO_LOCAL = "true"
```

Windows example—TOML literal quotes preserve backslashes:

```toml
[mcp_servers.zotero]
command = 'C:\Users\YOUR_NAME\.local\bin\zotero-mcp.exe'

[mcp_servers.zotero.env]
ZOTERO_LOCAL = "true"
```

Keep these machine-specific settings outside the shared Vault. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

### CLI alternative

Only if the Codex CLI is installed and `codex --version` works:

```bash
codex mcp add zotero --env ZOTERO_LOCAL=true -- "/ABSOLUTE/PATH/TO/zotero-mcp"
codex mcp list
```

The same command works in native PowerShell with the actual Windows `.exe` path. `command not found: codex` means this CLI route is unavailable; use the desktop GUI or config-file route. [Official CLI commands](https://learn.chatgpt.com/docs/developer-commands).

## 5. Connect Claude

Skip this step if you only use Codex. Multiple configured clients are fine; only one may write the Wiki at a time.

### Claude Code

After installing/signing in to Claude Code, run this one-line command with your real executable path:

```bash
claude mcp add --scope user --env ZOTERO_LOCAL=true --transport stdio zotero -- "/ABSOLUTE/PATH/TO/zotero-mcp"
claude mcp get zotero
```

On native Windows use the `.exe` path. Restart Claude Code in the Vault folder and run `/mcp` to check the connection. User scope keeps machine configuration outside the shared repository. If `zotero` already exists, inspect/edit it instead of adding a duplicate. [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp).

### Claude Desktop

Use **Settings → Developer → Edit Config**, where available, to locate the active `claude_desktop_config.json`. Typical locations are `~/Library/Application Support/Claude/` on macOS and `%APPDATA%\Claude\` on Windows; alternate builds may differ. Merge this entry with any existing `mcpServers` and fully restart Claude Desktop:

```json
{
  "mcpServers": {
    "zotero": {
      "command": "/Users/YOUR_NAME/.local/bin/zotero-mcp",
      "env": { "ZOTERO_LOCAL": "true" }
    }
  }
}
```

For Windows replace `command` with your path and **double backslashes in JSON**, for example `"C:\\Users\\YOUR_NAME\\.local\\bin\\zotero-mcp.exe"`. [Upstream Claude client setup](https://github.com/54yyyu/zotero-mcp/blob/main/docs/getting-started.md#integrating-with-claude-desktop-and-claude-code).

A connected Claude Desktop Zotero server enables literature tools. Maintaining this Wiki additionally requires explicitly granted access to the Vault files and its protocol. If that is absent, use Claude Code for Wiki writes.

## 6. Enable collection writes

Local reads alone cannot guarantee automatic filing. The Wiki needs incremental collection membership writes and, when justified, category creation. It does **not** need permission to rewrite every paper's metadata as part of ingest.

### Zotero 10+: local authorization

With Zotero open, run:

```bash
zotero-mcp authorize-local
```

Approve the Zotero dialog yourself; choose **Always Allow** if you want persistent access. The tool stores the local authorization in its user configuration outside the Vault. Restart/reconnect the MCP server, then check:

```bash
zotero-mcp authorize-local --status
```

Alternatively ask the connected agent to inspect `zotero_write_capabilities` and, if needed, invoke `zotero_authorize_local_writes`. A configured capability is not proof a real write succeeded; first-ingest read-back provides that verification. [Local write authorization](https://github.com/54yyyu/zotero-mcp/blob/main/docs/configuration.md#local-write-support).

### Older Zotero: local reads + web writes

1. Sign in at [Zotero API keys](https://www.zotero.org/settings/keys). Create a key for your personal library with the required library read/write access. Record the numeric **user ID** shown there.
2. Keep `ZOTERO_LOCAL=true`. In the chosen MCP client's private environment settings add `ZOTERO_API_KEY` (the key), `ZOTERO_LIBRARY_ID` (that numeric user ID), and `ZOTERO_LIBRARY_TYPE=user`. Enter the secret locally; do not paste it into chats, README, or Vault files.
3. Reconnect MCP. Ask it to inspect write capabilities. Allow Zotero sync to finish after web writes before verifying desktop state.

A NAS password, a Zotero account password, a web API key, and a local-write authorization are different credentials. Web API credentials are unnecessary for local reads and normally unnecessary for authorized Zotero 10 local writes. No write access means compilation can still work, but classification/Inbox completion must remain pending. [Connection modes](https://github.com/54yyyu/zotero-mcp/blob/main/docs/configuration.md#connection-modes).

## 7. Bind your library and collections

Client connection and Wiki configuration are separate. Update the **personal copy** of [`_system/zotero-collections.md`](_system/zotero-collections.md); the public starter intentionally leaves it unconfigured.

Suggested roots:

```text
00 Inbox
10 Topics         What the research is about
20 Methods        How the central method works
30 Projects       Managed by you
90 Archive        Managed by you
```

Reuse existing roots if they serve these roles. When roots are missing, approve a minimal initialization or create them manually in Zotero; there is no need to import someone else's entire taxonomy. For example, `10 Topics/Music & Musical Audio` and `20 Methods/Generative Modeling` are separate axes. Prefer stable, descriptive names over per-paper categories or year prefixes in Topics/Methods.

Ask the agent:

```text
Configure this Vault's Zotero binding. Read the live personal-library collection tree
and resolve the stable account user ID and actual Inbox/Topics/Methods keys. Record
them, the rule revision/date, managed name/key/parent tree and concise assignment
boundaries in _system/zotero-collections.md. Record Projects/Archive as protected.
Reuse existing roots. Propose missing or ambiguous roots before creating anything.
Do not ingest or change existing paper memberships during this setup.
```

For manual setup, obtain the account user ID from [Zotero's keys page](https://www.zotero.org/settings/keys), use the connected MCP's collection listing to get keys/parents, and fill the matching fields in the configuration file. A local API alias such as `0`, a SQLite library number such as `1`, a collection name, and a stable account ID are not interchangeable. Do not invent keys or put the local attachment directory here.

Ordinary ingest adds suitable Topics/Methods memberships and may create an unambiguous reusable missing category. **Projects and Archive are protected.** Renaming, moving, merging, splitting, or deleting an existing category requires a concrete approved plan and reevaluation of all affected older items. Whole-library discovery is supported when requested; it does not authorize whole-library reclassification.

## 8. Verify the connection

Keep one known PDF downloaded in Zotero. Ask for a **read-only** check:

```text
Verify Knowledge Wiki v2 setup without ingesting, modifying Zotero, or saving notes.
Confirm the Vault protocol is readable and identify the active personal library.
List the configured collection roots; locate one paper I identify, its parent key,
and its exact PDF attachment key. Resolve the local PDF, calculate SHA-256, read
one specified physical page as text and one page as an image, and inspect its
annotations. Distinguish zero annotations from an API error. Check write capability
without performing a write. Report pass/fail separately for every capability and
which client/OS you actually tested. Do not expose credentials or build an index.
```

Accept these results separately:

- **Client:** the MCP is connected and tools can be called; a saved configuration alone is insufficient.
- **Original evidence:** actual PDF bytes are accessible, a hash was calculated, selected-page text/image reading works. Metadata or an abstract alone does not pass PDF ingest.
- **Annotations:** actual records or a verified empty response; missing capabilities remain pending.
- **Binding:** stable library identity and collection keys match the live tree.
- **Writes:** the route is available; the first real ingest will test incremental add/remove and read-back.
- **Wiki access:** the agent has local file read/write capability for the Vault; a read-only check does not need to create a test file.

If using both Codex and Claude Code, run this checklist in each client against the same library/PDF; confirm the same attachment key and SHA-256. A pass in one client does not prove the other is connected. Then open a fresh session in the other client, read its adapter and the Wiki files, and query the existing Source without re-ingesting or changing files. Record each result separately; documentation support is not an end-to-end test result.

After the first Source note exists, click one page link from Obsidian on **each desktop** and verify the correct PDF/page opens. This checks the OS link handler, separately from MCP reading and byte-hash verification.

## 9. Ingest your first source

### Zotero entry

Put **one selected paper** into the configured `00 Inbox` and ensure its PDF opens locally. Then ask:

```text
Standard Ingest the paper <title or item key> from Zotero 00 Inbox. Keep its PDF in
Zotero. Search existing knowledge before creating pages. Record exact attachment
identity, SHA-256, paper version, physical-page links and actual reading coverage.
Snapshot only annotations/notes used in compilation. Classify only Topics/Methods;
preserve Projects and Archive. Add and verify target memberships first. Remove
only Inbox membership after compilation, annotation handling, bookkeeping and lint
succeed. Report files changed, classification deltas and any unfinished stage.
```

Open `wiki/Home.md` and the resulting knowledge pages. A worthwhile paper usually gets a Source note; exact duplicates or sources with no new material need no empty page. Once this pilot works, request “Process Zotero Inbox” for the pending papers.

### Vault entry: works with or without Zotero

Clip a web page to `inbox/` with Obsidian Web Clipper, or place a PDF/Markdown/text file there. Ask: “Standard Ingest the new material in Vault inbox.” The agent preserves canonical raw, checks hashes, updates existing knowledge, and performs verified delivery-copy cleanup when all protocol conditions pass. Vault-delivered PDFs remain supported; they are not silently moved to Zotero.

### Ask questions and resume failures

Ask: “According to my Wiki, explain this paper's Equation 3 and verify the cited page.” Query is read-only; it resolves the original by raw path or exact external reference and checks the hash. If Zotero is unavailable, the answer must distinguish existing compiled coverage from details it cannot reverify.

Exact hashes are compared across Vault and Zotero sources. A completed duplicate reuses compiled knowledge; pending classification or newly used annotations can still be handled. An incomplete ingest resumes its unfinished work. Classification does not trigger PDF re-ingest. Successful filing and Inbox removal are separately recorded so a retry does not start over.

Used annotation snapshots live in `raw/other/`, with source identity, PDF hash, annotation/note keys, locators and content. Their payload hash excludes capture time; changes produce a new snapshot. These snapshots follow Vault raw synchronization/backup, **not Git**, and do not recover a missing PDF. See [SCHEMA §11](_system/SCHEMA.md#11-external-evidence-and-backward-compatible-manifest-v2) and [WORKFLOW §§15–17](_system/WORKFLOW.md#15-zotero-connection-discovery-and-ingest).

## Troubleshooting

| Symptom | Next check |
|---|---|
| `codex: command not found` | Use the desktop GUI/config file; CLI installation is optional for GUI setup. |
| `zotero-mcp` not found | Reopen terminal; inspect `uv tool dir --bin`; use the actual absolute executable path in the client. |
| MCP saved but disconnected | Start Zotero, enable local communication, verify uppercase `ZOTERO_LOCAL=true`, remove empty argument rows, reconnect and inspect client errors. |
| Searching works but PDF reading fails | Open/download the exact attachment in Zotero. WebDAV-only remote bytes and metadata are not a local PDF. |
| `fitz` / PyMuPDF missing, or page image fails | Add the `pdf` extra to the **same** tool environment, then reconnect. A verified local PDF reader is a valid fallback; report which route worked. |
| Reading works but classification fails | Check local authorization or hybrid key permissions using write capabilities; do not mark Inbox complete. |
| Tool says no items, wrong library, or key missing | Verify active personal library, sync state and actual root keys. Do not re-ingest solely because another computer has not synced. |
| Obsidian link opens nothing/wrong content | Verify installed Zotero, matching account/attachment, downloaded PDF and `zotero://` association; compare current bytes with the recorded hash. |
| PDF hash changed | Register a new snapshot and investigate; do not silently replace old citations. Restore old bytes from Zotero backup if necessary. |
| Windows Zotero + WSL agent fails | Check which OS runs the MCP, how it reaches Zotero and resolves attachment paths. Prefer a native Windows stack for this guide; never assume localhost/paths cross environments. |
| Same server appears twice | Keep one deliberate registration per client; inspect a similarly named plugin before adding another server. |
| Setup keeps proposing embeddings | Baseline Wiki retrieval uses index, summaries and targeted search. Do not run semantic indexing to fix a connection problem. |

More implementation-specific diagnostics: [Zotero MCP troubleshooting](https://github.com/54yyyu/zotero-mcp/blob/main/docs/troubleshooting.md). Never attach an unredacted client config or authorization file to a public issue.

## Repository and Vault layout

```text
Knowledge_Wiki/
├── wiki/                 Compiled knowledge
│   ├── Home.md           Human dashboard
│   ├── sources/          Reusable notes about individual sources
│   ├── concepts/         Explanations accumulated across sources
│   ├── entities/         Models, datasets, tools, people, organizations
│   ├── questions/        Durable research questions
│   └── syntheses/        Cross-source comparisons and arguments
├── _system/              Vendor-neutral protocol and portable state
│   ├── SCHEMA.md / WORKFLOW.md / DECISIONS.md
│   ├── zotero-collections.md   Personal binding; unconfigured in starter
│   ├── templates/        Five page templates
│   └── index.md / manifest.json / STATE.md / log.md
├── raw/                  Vault-owned evidence; file sync/backup, not Git
│   ├── papers/           Vault-delivered PDFs
│   ├── web/              Web/Markdown captures
│   ├── conversations/    Explicitly preserved conversation evidence
│   ├── other/            Other sources and used Zotero note snapshots
│   └── assets/           Source-owned images
├── inbox/                Vault delivery area, including attachments/
├── assets/               Wiki branding/assets
├── .obsidian/            Shared viewer configuration
├── AGENTS.md / CLAUDE.md  Thin client adapters
└── README*.md            Human setup and usage guides
```

Zotero's database/PDF storage and client credentials stay outside this tree. `_system/BOOTSTRAP.md` is historical design input; current authority is SCHEMA → WORKFLOW → DECISIONS. Agents read STATE for maintenance and the compact index for candidate selection. The human README explains how to start; it does not supersede that protocol.

Keep durable research here, not tasks, reminders, a whole chat archive, or an uncurated file dump. The Wiki becomes useful through maintained explanations and traceable evidence.

## Main operating modes

### Standard Ingest (default)

Use Standard Ingest for ordinary papers, blogs, articles, and official documentation. The agent uses the index, summaries, aliases, and targeted search to select candidate pages, then updates existing knowledge whenever possible. For papers, Standard still records the research question, method, necessary equations, experimental setup, main results, and limitations. Token-aware means avoiding wasteful reading, not reducing a paper to its abstract.

```text
Process the new material in inbox.
```

### Deep Ingest

Use Deep Ingest for foundational papers, work you expect to cite seriously, or sources whose method, evidence, and limitations need close study. It first maps the paper, covers the core argument and evidence chain, and selectively compiles details that will be useful for future understanding, comparison, citation, or reuse. Low-frequency details that are not compiled remain accessible through locators and can be read from registered original evidence during a later Query. Deep costs more tokens, must be requested explicitly, and does not exhaustively inspect every appendix page by default.

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
| Inspect a particular equation, figure, or experiment | Query | Open only the relevant original pages and necessary context; do not write by default |

There is no rule such as “keep exactly one to three equations.” An empirical paper with no important equation should not be forced to include one, while a mathematical paper may require many. In Standard and Deep, the question is whether omitting an equation would obstruct understanding the central contribution, explaining results, comparing methods, or judging reproducibility. Exhaustive covers every material equation. When an equation is retained, explain its symbols, assumptions, role, necessary derivation logic, and source locator.

The “deep” in Deep Ingest means complete understanding of the core argument and evidence chain, not copying every detail into the Wiki. The agent must report what it read, what it inspected visually, and which appendices were deliberately deferred. Later questions can follow locators back to the registered original. Exhaustive Ingest is also not a verbatim copy: references, generic background, and repetition may be compressed, but every detail that could change a research judgment or reproduction result must be examined. Long exhaustive work is processed by section or chapter, with resumable progress recorded in `STATE.md` until all planned coverage is complete.

### Promote

When a query or discussion produces durable knowledge, compile it back into the Wiki:

```text
This answer is worth keeping. Compile it into the Wiki, preserve original-evidence provenance, update existing pages before creating new ones, and do not save the full conversation.
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
Lint this Wiki according to the v2 WORKFLOW. Report broken links, manifest/raw problems, exact duplicates, and needs_review pages. Do not automatically resolve scientific conflicts.
```

### Inspect current maintenance state

```text
Read _system/STATE.md and the recent log, then tell me what is most worth doing next in this Wiki.
```

## What happens during an Ingest?

```text
Vault source / inbox / URL OR Zotero attachment
        ↓
Capture Vault raw OR register exact Zotero attachment; SHA-256 duplicate gate
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
Vault: commit, then verified delivery-copy cleanup
Zotero: verify Topics/Methods filing, then remove Inbox membership
```

One to ten material page changes are within ordinary ingest authority. If more than ten pages are expected to change, the agent first lists the affected pages and the material reason for each, then waits for confirmation. Page count is not a quality target; every changed page must receive a material update.

## Browsing in Obsidian

- Start from `wiki/Home.md`.
- Use Search to find text.
- Use Backlinks and Outgoing Links to understand relationships.
- Use the global Graph after several ingests to see topic clusters, bridge pages, and isolated areas. Graph View excludes `_system`, `raw`, and `inbox`.
- Use Local Graph only when you want the immediate neighborhood of one connected page; it is expected to be sparse in a new Wiki.
- Attachments added through Obsidian default to `inbox/attachments/`; Zotero attachments remain in Zotero.

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

The source is preserved in Vault raw or registered as an external attachment, but it did not add knowledge worth compiling into the current Wiki. The manifest and log record the result without creating an empty page.

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

Not in v2. Start with the index, summaries, aliases, `rg`, wikilinks, and Obsidian Search. Add retrieval infrastructure only after repeated, documented retrieval failures.

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
