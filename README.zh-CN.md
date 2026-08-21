[English](README.md) | **简体中文**

<h1 align="center">
  <img src="assets/knowledge-wiki-logo.png" alt="Knowledge Wiki logo" width="72" align="absmiddle">
  Knowledge Wiki
</h1>

<p align="center"><strong>一个由可替换 LLM agent 维护、vendor-neutral、source-grounded 的长期知识库。</strong></p>

一个基于 Andrej Karpathy LLM Wiki 理念的个人长期研究知识库：你选择资料、提出问题和做最终判断；可替换的 LLM agent 负责把 raw evidence 持续编译成 coherent、可检索、可追溯的 Wiki。

> [!important] 当前状态
> 这是一个干净、尚未使用的 starter template。v1 结构、真实来源 workflow 和 Codex/Claude Code fresh handoff 已在独立的私有 pilot 中验证；本仓库不包含 pilot 来源、compiled knowledge、个人 STATE 或操作历史。

## 为什么使用 Knowledge Wiki？

假设你已经读了几十篇论文，也收藏了几百个有用的网页。普通文件问答或 RAG 工具可以搜索这些文件并回答一次问题，但答案通常留在聊天记录里。下次提问又要从同一堆文件重新搜索，不同资料之间的关系也仍然是分散的。

Karpathy-style LLM Wiki 的核心想法是改变这个循环：让 LLM 把新资料持续编译进一个会被维护的 Wiki。Knowledge Wiki 在此基础上，把它做成了一套可以日常使用、source-grounded 的 Obsidian workflow。

### 这个项目主要增加了什么

- **知识会累积，而不是只堆积摘要。** 新论文不会默认变成又一篇孤立总结。Agent 会先搜索 Wiki 已有内容，更新现有 Concept 和 Entity，记录值得长期追踪的 Question，只在真正形成跨来源比较或结论时创建 Synthesis。
- **重要结论都可以回去核对。** 原始 PDF、网页快照和其他证据保留在 `raw/`。关键数字、引语、实验结果和时效性事实可以定位到具体 page、section、figure、table 或 snapshot。
- **你可以决定读多深。** Standard Ingest 高效处理日常资料；Deep Ingest 深入跟踪核心论证和证据链；Exhaustive Ingest 用于复现、审稿或逐节完整技术分析。
- **提问不会自动污染 Wiki。** Query 默认只读。当讨论产生值得保留的内容时，Promote 只会编译 durable conclusion，而不是把整段 conversation 存起来。
- **Agent 可以随时替换。** Codex、Claude Code 或其他 file-based agent 都可以仅依靠 Vault 接管。真正持久的 memory 是普通 Markdown、raw evidence 和少量 bookkeeping 文件，而不是某个产品的聊天历史或隐藏 memory。
- **跨设备工作仍然可审计。** Hash 防止重复 ingest，manifest 记录每个来源影响了什么，Git 审阅文本历史，raw evidence 则可以单独同步和备份。
- **系统始终可以被人看懂。** v1 只使用五种页面、Obsidian links、Search、Graph 和普通文件。只有真实 retrieval problem 出现后，才增加 database、embeddings 或复杂 plugins。

实际使用时，你可以直接问：“我的 Wiki 现在对这个主题的理解是什么，为什么，哪些来源存在分歧？”回答来自一个持续维护的知识体系，而不是一堆互不相干的摘要。

## 适合保存什么

- 学术论文、技术报告和标准；
- Blog、官方文档和重要网页；
- 持久概念、方法、模型、数据集和工具知识；
- 开放研究问题、hypotheses 和跨来源 synthesis；
- 经过明确 Promote 的 durable conversation conclusions。

不适合保存：

- Daily notes、会议提醒、任务和 deadline；
- 临时 working notes；
- Email 或聊天全文归档；
- 没有筛选的 bookmark/PDF dump；
- Secrets、API keys 或不应发送给当前模型的私人资料。

这些内容应留在你的 operational vault 或其他专用系统中。

## 五分钟 Quick Start

### 1. 安装 Obsidian 和 Web Clipper

- 为当前操作系统安装 [Obsidian](https://obsidian.md/download)。
- 在 Chromium-based 浏览器、Firefox、Safari 或 Edge 中安装官方 [Obsidian Web Clipper](https://obsidian.md/clipper) 扩展。

Web Clipper 是把文章和选中段落以 Markdown 形式送进 Wiki 的最简单方式。建议用它 capture 网页，但它不是 runtime dependency：PDF、本地文件、粘贴文本和直接 URL 同样可以使用。

### 2. 把整个仓库作为一个 Vault 打开

Clone、下载或找到 `Knowledge_Wiki` 文件夹。在 Obsidian 中选择 **Open folder as vault**，然后选择仓库根目录，也就是同时包含 `AGENTS.md`、`_system/`、`wiki/`、`raw/` 和 `inbox/` 的那个文件夹。

不要只把 `wiki/` 打开为 Vault。Agent 需要同时看到 protocol、evidence、inbox 和 bookkeeping 目录。如果准备 ingest 私人或受版权保护的资料，请使用 private personal copy，而不是公开 fork。

### 3. 连接一个 file-based agent

以 Vault 根目录为 working directory，启动 Codex、Claude Code 或其他 file-based coding agent。

- Codex 通过 `AGENTS.md` 进入系统；
- Claude Code 通过 `CLAUDE.md` 进入系统；
- 两者都遵循相同的 `_system/SCHEMA.md` 和 `_system/WORKFLOW.md`，不需要之前的聊天 context。

第一次可以先做只读检查：

```text
请读取仓库指引，了解这个 Knowledge Wiki，准备好后告诉我。先不要修改文件。
```

不要让两个 agent 同时写入 Vault。没有 `.git/` 的设备可以 ingest 和 lint，但应由指定提交机稍后审阅并提交已同步的变更。

### 4. 把第一份来源放进 `inbox/`

选择任意一种方式：

- **网页文章：** 打开 Web Clipper，选择这个 Vault，将目标 Folder 设为 `inbox/`，检查抓取的文章，然后点击 **Add to Obsidian**。
- **PDF、Markdown 或文本文件：** 通过 Finder、File Explorer 或 file-sync service 把文件复制到 `inbox/`。
- **直接 URL 或粘贴文本：** 直接提供给 agent，并明确要求 Ingest。

`inbox/` 是资料投递区。不要手动把尚未处理的 source 放进 `wiki/`；agent 会在正确位置创建 canonical raw evidence 和 compiled pages。

### 5. 执行第一次 Ingest

普通资料默认使用 Standard Ingest：

```text
请用 Standard Ingest 处理 inbox 里的新资料。
```

Agent 会通过 manifest 和 hash 识别未处理文件，保留 canonical raw evidence，检查重复，搜索已有知识，先更新后创建，验证 links 和 provenance，并报告每个 created/updated file。如果 inbox 里有多个新来源，会先列出再依次处理。只有所有 cleanup 条件都通过后才会删除 inbox 投递副本；否则会保留并说明原因。

### 6. 打开结果并开始提问

从 `wiki/Home.md` 开始，再打开新 Source page 以及它更新的 Concept 或 Entity page。然后试一次只读 Query：

```text
根据我的 Wiki，Flow Matching 和 Diffusion 的核心区别是什么？
```

Query 默认不会修改 Vault。如果答案中有值得保留的 durable conclusion，agent 会提出 Promote 建议。

## 主要操作方式

### Standard Ingest（默认）

适合普通论文、Blog、文章和官方文档。Agent 先通过 index、summary、aliases 和 targeted search 筛选候选页，优先更新已有知识。对于论文，Standard 仍会保存 research question、方法、必要公式、实验设置、主要结果和 limitations；token-aware 是减少无效读取，不是把论文压缩成 abstract。

```text
请处理 inbox 里的新资料。
```

### Deep Ingest

适合 foundational paper、准备认真引用的工作，或需要深入理解方法、证据和限制的来源。它会先建立论文地图，覆盖核心论证与证据链，再选择性保存以后值得理解、比较、引用或复用的细节。未保存的低频细节通过 locator 在 Query 时按需回到 raw。Deep 会消耗更多 token，必须显式要求，但不默认逐页穷尽附录。

```text
请对 inbox 里的新论文做 Deep Ingest。
```

### Exhaustive Ingest

适合复现、审稿、逐节技术审查，或你明确需要完整检查正文、附录、公式、图表、实验和复现细节的论文。它以 material completeness 为目标，必要时分批处理，是 token 成本最高的模式。必须显式要求。

```text
请对 inbox 里的新论文做 Exhaustive Ingest。
```

## 论文应该怎样读和保存

论文有四种互补用法：

| 需求 | 推荐方式 | 结果 |
|---|---|---|
| 先建立可靠、可复用的研究笔记 | Standard Ingest | 结构化 Source page，并按需更新相关知识页 |
| foundational paper 或需要深入研究理解 | Deep Ingest | 覆盖核心论证和证据链，选择性编译 durable details |
| 复现、审稿或逐节完整技术分析 | Exhaustive Ingest | 覆盖所有 material 方法、公式、实验、附录、限制与复现信息 |
| 临时追问某个公式、图表或实验 | Query | 只打开对应 raw 页面和必要上下文，默认不写回 |

公式没有“必须保留 1–3 个”之类的配额。没有关键公式的 empirical paper 不应硬塞公式；高度数学化的论文则可能需要保留很多公式。Standard 和 Deep 判断的是：缺少它是否会妨碍理解核心贡献、解释结果、比较方法或判断复现要求；Exhaustive 则覆盖所有 material equations。保留时应同时解释 symbols、assumptions、作用、必要推导逻辑和原文 locator。

Deep Ingest 的“深入”指核心理解和证据链完整，不是把所有细节写入 Wiki。Agent 必须报告实际阅读范围和主动延后的附录，后续问题再按 locator 定向读取。Exhaustive Ingest 也不是复制全文：参考文献列表、通用背景和重复表述可以压缩，但所有会改变研究判断或复现结果的重要细节都应检查；长文用 section/chapter 分批处理，在 STATE 中保留可接管的进度，全部批次完成后再报告最终覆盖范围并清理 inbox 副本。

### Promote

当一次 query 或讨论产生 durable knowledge 时，可以将结论编译回 Wiki：

```text
这个答案值得保存。请保留 raw provenance，并优先更新已有页面，不要保存完整聊天。
```

### Research Mode

一次研究会话中，可以授权 agent 自动保存稳定、有来源、可复用的结论：

```text
本次会话开启 Research Mode。把稳定、有来源、可复用的研究结论自动编译进 Wiki；不要保存完整 conversation。
```

Research Mode 只对当前会话有效。Merge、rename、delete、重大冲突和 schema change 仍需确认；唯一例外是成功 ingest 后按权威 Workflow 执行的 verified inbox cleanup。

## 更多可复制 prompts

### 查看 Wiki 已知内容

```text
根据我的 Wiki，总结目前关于 target speaker extraction 的理解，并指出证据不足的部分。
```

### 比较方法

```text
根据 Wiki 中已有证据比较方法 A 和方法 B。区分论文报告的事实与我们的 inference。
```

### 保存研究问题

```text
这个问题值得长期追踪。请先检查是否已有相关 Question 页面，再决定更新或创建。
```

### 健康检查

```text
请按 v1 WORKFLOW lint 这个 Wiki，报告 broken links、manifest/raw 问题、exact duplicates 和 needs_review 页面。不要自动处理科学冲突。
```

### 查看当前维护状态

```text
读取 _system/STATE.md 和最近的 log，告诉我 Wiki 当前最值得做什么。
```

## 一次 Ingest 会发生什么

```text
Source / inbox / URL
        ↓
Capture immutable raw + SHA-256 duplicate gate
        ↓
按所选深度读取 source
        ↓
Index + summary + aliases + targeted search
        ↓
New / Update / Disputed / No material
        ↓
Targeted Wiki changes + bounded cascade
        ↓
Validate provenance, links and metadata
        ↓
Update index, manifest, log and (only if needed) STATE
        ↓
Commit, then remove only hash-verified untracked inbox copies
```

修改 1–10 个真正受到影响的页面属于普通 ingest 范围。预计超过 10 页时，agent 会先列出 affected pages 和具体理由，等待确认。页数不是质量目标；每页都必须有 material change。

## 在 Obsidian 中浏览

- 从 `wiki/Home.md` 开始；
- 使用 Search 查找正文；
- 使用 Backlinks 和 Outgoing Links 理解关系；
- 经过几次 ingest 后，使用 global Graph 查看 topic clusters、bridge pages 和孤立区域。Graph View 已排除 `_system`、`raw` 和 `inbox`；
- 只在想看某个已连接页面的直接邻域时使用 Local Graph；新 Wiki 中 Local Graph 很稀疏是正常的；
- 新附件默认进入 `inbox/attachments/`，在 ingest 后再进入正式 raw layer。

`_system/index.md` 是 agent 的 compact catalog，不是语义知识页，也不应被当作证据。

### Properties 在哪里？

`wiki/Home.md` 是导航页，没有普通知识页的 frontmatter，因此它不会显示知识 Properties。第一次 ingest 后，打开任意 Concept、Source、Entity、Question 或 Synthesis 页面，页面顶部应显示 `title`、`type`、`summary`、`sources`、`needs_review` 等字段。

如果知识页顶部仍然看不到：

1. 打开 **Settings → Editor**；
2. 将 **Properties in document** 设为 **Visible**；
3. 如果显示的是 `---` 包围的 YAML 文本，则当前设置是 **Source**，改为 **Visible** 即可。

也可以启用 Obsidian 的 **Properties view** core plugin，在侧边栏集中查看整个 Vault 使用了哪些 property；这不是 Knowledge_Wiki 的运行依赖。

### Global Graph 和 Local Graph

**Graph view** 是 Obsidian core plugin。如果找不到 Graph 命令，先在 **Settings → Core plugins → Graph view** 中启用它。

- 打开 global Graph：使用 ribbon 中的 **Open graph view** 按钮，或在 Command Palette 中执行 **Open graph view**。它显示整个 Vault，当几份来源已建立足够关系后，可以用来观察 clusters 和 knowledge gaps。
- 打开 Local Graph：先打开一个知识页，再在 Command Palette（macOS 通常为 `Cmd+P`，Windows/Linux 通常为 `Ctrl+P`）中执行 **Open local graph**。它只显示与当前页相连的 notes，并可以调整 depth。

对新建或连接较少的 Wiki，Search、Backlinks、Outgoing Links 和 global Graph 通常比 Local Graph 更有信息量。Graph 稀疏很正常；不要为了让图看起来更丰富而制造链接。

## 查看和恢复修改

每次重要写入后先查看：

```bash
git status --short
git diff
git log --oneline
```

一个 ingest 应形成一个逻辑 diff。不要在不理解影响时执行 destructive Git 命令；如需撤销，让 agent 先说明目标文件和可恢复方式。

## Codex、Claude Code 与其他 agent

Codex 和 Claude Code 都可以维护本 Wiki，但同一时间只能有一个 canonical writer。切换时：

1. 等待当前 agent 完成并检查 diff；
2. 如果使用 file-sync service，先确认同步完成；
3. 在另一 agent 中打开同一 Vault；
4. 让它读取自己的 adapter 和 `_system` 权威文件；
5. 不需要迁移旧 conversation、cache、memory 或 embeddings。

未来 agent 只要能读写普通文件、搜索 Markdown 并遵守 `_system` 协议，也可以接管。

## 文件同步与 single-writer

Synology Drive、iCloud Drive、Dropbox 等 file-sync service 只负责文件同步，不负责协调并发写入。不要在两台机器、两个 agent 或 Obsidian 与自动工具之间同时修改同一组文件。切换前确认同步已完成。

Git 历史用于审计 `wiki/`、`_system/`、文档和目录标记。`raw/` 与 `inbox/` 的实际内容留在 Vault 中由文件同步服务跨设备同步，但不进入 Git；raw evidence 必须另有独立、版本化的备份，因为 manifest hash 不能恢复缺失文件。

`.git/` 只保留在指定提交机本地，并从 Synology Drive 或其他文件同步服务中排除。其他设备可以编辑同步后的普通 Vault 文件，不需要携带 Git metadata。

## FAQ

### 为什么这份来源没有产生 Source page？

Source page 不是每次 ingest 的必然产物。如果来源只强化已有 Concept 或没有独立复用价值，更新现有页面更符合 compounding 原则。

### 什么是 No material？

来源已保存到 raw，但没有给当前 Wiki 增加值得写入的新知识。Manifest 和 log 会记录这一结果，不创建空洞页面。

### Ingest 后需要手动删除 inbox 文件吗？

通常不需要。Agent 只有在 canonical raw 已存在、SHA-256 完全一致、manifest/bookkeeping/lint 正常、本次 commit 已完成，而且附件也已妥善处理时，才会删除那个未被 Git 跟踪的 inbox 临时副本。条件不满足时它会保留文件并说明原因；`raw/` 中的 canonical evidence 不会因此删除。

本规则只对今后的已验证 ingest 生效，不会为了“清空 inbox”而批量删除历史或归属不明文件。

### 为什么 agent 要确认修改 10 多页？

跨很多页面可能是合理 cascade，也可能是弱关联扩散。确认步骤让你先看到每页的 material reason。

### 为什么 Query 没有自动保存？

普通 Query 默认只读，防止聊天答案污染 Wiki。Durable conclusion 会触发 Promote 建议；也可以显式启用 Research Mode。

### 编译后的 Wiki 内容会使用什么语言？

用户明确指定 output language 时，以明确要求为准。否则由当前 prompt 决定本次修改的语言：只要出现任何中文汉字就使用中文；纯英文 prompt 使用英文。该规则同时适用于新页面和更新，因此同一页面长期出现中英文混用是正常的。Canonical technical terms 和有实际用途的中英文 aliases 会保留，以支持 retrieval。

### System 文件会自动归档吗？

没有 background watcher。Agent 会在用户触发的 Maintenance、Lint、Ingest、schema review 或 handoff 中检查文件增长是否已经造成真实的导航或审阅成本。Durable outcome 已记录后，它可以自动整理 bounded `STATE.md`；但创建 archive 目录、移动历史、拆分权威协议或分片 index 都必须先提出具体方案并得到确认。真实需要出现前不会预建 archive 结构。

### 是否需要 embeddings、vector DB 或 Wiki plugin？

v1 不需要。先使用 index、summary、aliases、`rg`、wikilinks 和 Obsidian search。只有 pilot 后出现可重复的 retrieval failure 才增加工具。

### 如何处理很长的书或报告？

超过约 100,000 字符或 40 页时，先按 section/chapter 分批 ingest。不要一次深度处理整本书。

### 论文应该选择 Standard、Deep 还是 Exhaustive？

大多数论文先用 Standard，已经足够形成研究可用的 structured reading note。对 foundational paper、准备认真引用或需要深入理解证据链的工作使用 Deep。只有准备复现、审稿或确实要求逐节与附录完整覆盖时才使用 Exhaustive。也可以先 Standard，之后升级为 Deep，或针对某个 equation、table、appendix 或 section 按需细读，不必每次重新处理全文。

## 分享、版权与隐私

本仓库特意不包含 raw sources、compiled knowledge、个人 STATE 或操作历史。开始使用以后，不要直接公开正在使用的个人 Vault：其中可能包含受版权保护的 PDF、网页快照、私人 conversation、研究方向和 personal knowledge。

对外分享时，应从个人 Vault 导出独立 starter template，仅包含：

- `README.md` 与 `README.zh-CN.md`；
- `AGENTS.md` / `CLAUDE.md`；
- `_system` protocol 和 templates；
- 空目录；
- 自有、合成或明确允许分享的示例。

不要分享个人 `raw/`、`wiki/`、STATE、manifest、log、conversation、credentials 或 secrets。如果要重新发布自己修改过的 starter，请检查 diff 并重新导出一份干净副本。

Starter protocol 和文档采用本仓库的 [MIT License](LICENSE)。用户自行 ingest 的来源仍受各自版权和许可证约束。敏感文件一旦 commit，之后再加入 `.gitignore` 也不会从 Git 历史中消失，因此有需要时应在第一次 ingest 前把个人仓库设为 private。

## 权威文档

- [Schema](_system/SCHEMA.md)：页面模型、metadata、provenance 和 lifecycle。
- [Workflow](_system/WORKFLOW.md)：Ingest、Query、Promote、Research Mode 和 Lint。
- [Decisions](_system/DECISIONS.md)：当前已接受的架构决定与理由，不是修改流水。
- [Current State](_system/STATE.md)：当前 focus 和维护 backlog。
- [Templates](_system/templates/)：五种页面模板。
- [Historical Bootstrap](_system/BOOTSTRAP.md)：设计历史，不再是 operational authority。
