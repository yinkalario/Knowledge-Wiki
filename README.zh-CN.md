[English](README.md) | **简体中文**

<h1 align="center">
  <img src="assets/knowledge-wiki-logo.png" alt="Knowledge Wiki logo" width="72" align="absmiddle">
  Knowledge Wiki
</h1>

<p align="center"><strong>一个由可替换 LLM agent 维护、vendor-neutral、source-grounded 的长期知识库。</strong></p>

一个基于 Andrej Karpathy LLM Wiki 理念的个人长期研究知识库：你选择资料、提出问题和做最终判断；可替换的 LLM agent 负责把 raw evidence 持续编译成 coherent、可检索、可追溯的 Wiki。

> [!IMPORTANT]
> **当前状态：** v2 支持可选 Zotero ingest、精确附件溯源和 Topics／Methods 分类，同时兼容 Vault-only 工作流。使用 Zotero 前先配置个人绑定；具体核验状态见 STATE。

## 为什么使用 Knowledge Wiki？

假设你已经读了几十篇论文，也收藏了几百个有用的网页。普通文件问答或 RAG 工具可以搜索这些文件并回答一次问题，但答案通常留在聊天记录里。下次提问又要从同一堆文件重新搜索，不同资料之间的关系也仍然是分散的。

Karpathy-style LLM Wiki 的核心想法是改变这个循环：让 LLM 把新资料持续编译进一个会被维护的 Wiki。Knowledge Wiki 在此基础上，把它做成了一套可以日常使用、source-grounded 的 Obsidian workflow。

### 这个项目主要增加了什么

- **知识会累积，而不是只堆积摘要。** 新论文不会默认变成又一篇孤立总结。Agent 会先搜索 Wiki 已有内容，更新现有 Concept 和 Entity，记录值得长期追踪的 Question，只在真正形成跨来源比较或结论时创建 Synthesis。
- **重要结论都可以回去核对。** 从 Vault 导入的 PDF、网页快照和其他证据保留在 `raw/`；从 Zotero 导入的 PDF 留在 Zotero，并登记可核验的来源关联。关键数字、引语、实验结果和时效性事实可以定位到具体 page、section、figure、table 或 snapshot。
- **你可以决定读多深。** Standard Ingest 高效处理日常资料；Deep Ingest 深入跟踪核心论证和证据链；Exhaustive Ingest 用于复现、审稿或逐节完整技术分析。
- **提问不会自动污染 Wiki。** Query 默认只读。当讨论产生值得保留的内容时，Promote 只会编译 durable conclusion，而不是把整段 conversation 存起来。
- **Agent 可以随时替换。** Codex、Claude Code 或其他 file-based agent 都可以仅依靠 Vault 接管。真正持久的 memory 是普通 Markdown、raw evidence 和少量 bookkeeping 文件，而不是某个产品的聊天历史或隐藏 memory。
- **跨设备工作仍然可审计。** Hash 防止重复 ingest，manifest 记录每个来源影响了什么，Git 审阅文本历史，raw evidence 则可以单独同步和备份。
- **系统始终可以被人看懂。** v2 仍只使用五种页面、Obsidian links、Search、Graph 和普通文件。只有真实 retrieval problem 出现后，才增加 database、embeddings 或复杂 plugins。

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

## 仓库与 Vault 目录结构

应把整个仓库根目录作为 Obsidian Vault 打开，而不是只打开 `wiki/`。各个顶层目录承担不同职责：

```text
Knowledge_Wiki/
├── wiki/                 编译后、可供人直接阅读的知识
│   ├── Home.md           起始页和导航入口
│   ├── concepts/         概念、机制和方法
│   ├── entities/         模型、工具、数据集、人物和组织
│   ├── sources/          针对单个来源的可复用笔记
│   ├── questions/        开放问题和 hypotheses
│   └── syntheses/        跨来源比较和结论
├── _system/              Agent protocol 和 durable bookkeeping
│   ├── SCHEMA.md         知识模型与页面规则
│   ├── WORKFLOW.md       Ingest、Query、Promote 和 Lint 流程
│   ├── DECISIONS.md      已接受的架构决定及其理由
│   ├── templates/        五种知识页面的模板
│   └── index、manifest、STATE 和 log 文件
├── raw/                  为核验而保留的 canonical evidence
│   ├── papers/           原始论文和报告
│   ├── web/              抓取的网页和 snapshots
│   ├── conversations/    Promote 后的 conversation evidence
│   ├── assets/           归属于 raw source 的附件
│   └── other/            其他 canonical evidence
├── inbox/                等待 Ingest 的资料投递区
│   └── attachments/      随 inbox source 投递的附件
├── assets/               Wiki 自身使用的图片和其他文件
├── .obsidian/            这个 Vault 共用的 Obsidian 配置
├── AGENTS.md             Codex 入口文件
├── CLAUDE.md             Claude Code 入口文件
├── README*.md            用户文档
└── .git/                 指定提交机上的本地 Git 历史
```

这种分离是有意设计的：`inbox/` 接收资料，`raw/` 保存证据，`wiki/` 保存从证据编译出的知识；`_system/` 让没有旧聊天 context 的新 agent 也能正确接管。`raw/` 和 `inbox/` 中的实际文件不进入 Git，但仍留在 Vault 中由 file-sync service 同步；Git 会保留目录标记，使新 clone 仍具有预期结构。`.git/` 只属于指定提交机本地，不应由文件同步服务同步。

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

### 4. 选择来源入口

选择任意一种方式：

- **网页文章：** 打开 Web Clipper，选择这个 Vault，将目标 Folder 设为 `inbox/`，检查抓取的文章，然后点击 **Add to Obsidian**。
- **PDF、Markdown 或文本文件：** 通过 Finder、File Explorer 或 file-sync service 把文件复制到 `inbox/`。
- **Zotero PDF：** 保留在 Zotero `00 Inbox`，使用下方 Zotero 工作流。
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

## v2 的 Zotero 工作流（可选）

保留两种入口：PDF／Markdown／文本继续放进 Vault `inbox/`；也可以让 PDF 一直保存在 Zotero，再要求 Zotero ingest。Zotero 管理自己的 PDF 附件，Wiki 管理 compiled notes 和可跨设备使用的来源记录。Web Clipper 的 Markdown 与其他本地 raw 仍在 Vault。五种页面类型及 Standard／Deep／Exhaustive 阅读要求不变。

### 连接与初始化

Mac、Windows 各自配置本机 Zotero adapter。首个接入实现是 [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)，采用 `ZOTERO_LOCAL=true`；PDF 扩展支持页面图片。保持 Zotero 打开、允许本地通信，并确保所选附件已下载。电脑上的这份文件属于 Zotero 管理，不是另存到 Vault 的 PDF。移动设备继续用 Zotero 阅读和批注。WebDAV 同步附件、Zotero 账号同步 metadata／批注，都不会替其他电脑安装 MCP。

按照各客户端当前说明注册本地程序，不要顺手运行会修改 Vault `AGENTS.md`／`CLAUDE.md` 的 skill 安装器。Query 只需要读取权限；自动分类另需 Zotero 写入授权。凭据和机器绝对路径不写入 Vault。首次使用前，在 [`_system/zotero-collections.md`](_system/zotero-collections.md) 绑定稳定账号 ID 与实际 collection keys。公开 starter 故意不预填个人绑定；不使用 Zotero 仍可正常运行。

### 日常使用

```text
请用 Standard Ingest 处理 Zotero 00 Inbox 中的新论文。PDF 留在 Zotero。只分类 Topics 和 Methods，必要时创建含义明确、可复用的新类别；保留 Projects 和 Archive。报告原文链接、hash、实际阅读范围、批注快照、分类变更和未完成事项。
```

也支持指定论文、collection 或全库发现；全库发现不等于自动全库重分类。PDF hash 在 Zotero 和 Vault 来源之间统一查重。重复 ingest 复用已有知识，但可以补做分类或保存新使用的批注；标题或 DOI 相同不等于文件相同。全库检查先分页读取精简 metadata，再选取需要读原文的文章。

提问时可指定论文、公式、章节或页码。Agent 解析具体附件、校验 hash，然后只读必要上下文；普通 Query 不修改 Vault 或 Zotero。Zotero 不可用时，必须区分此前已编译的内容与尚未重新核验的原文细节。

### 原文链接、快照和版本

Source note 保留附件链接、稳定来源引用、PDF 物理页码、SHA-256 和实际文本／视觉阅读范围。`sources` 继续保存 Vault raw 路径，可选 `source_refs` 引用外部 manifest 记录。点击 Zotero 链接会打开当前附件，但只有 hash 检查才能确认与历史文件快照一致。曾引用的旧版本应作为不同附件保留；Zotero metadata 修订编号不是论文版本。旧附件被覆盖或丢失时，Wiki 能发现问题，但恢复需要原文件或备份。

只把实际用于编译的批注或子 note 保存为 `raw/other/` 下不可覆盖的 Markdown，必要图片保存在 `raw/assets/`。快照区分论文原文、用户评论和 agent 推断；所选内容的查重 hash 不包含捕获时间。快照不等于完整 PDF 备份。Obsidian graph 仍通过 Source 与 Concept／Entity 等知识页的内部链接形成，不需要为了 graph 复制 PDF 或新造页面。

### 分类与失败恢复

Topics 表达研究问题，Methods 表达核心方法。Projects 完全由用户管理，agent 不增删其成员关系或修改其结构；Archive 同样受保护。优先复用既有分类、保留手工归属，允许合理的多重分类。重命名／移动／合并／拆分／删除既有类别，需要先确认具体方案，并复核所有受影响旧文章和子分类。手工结构变更在下次用户触发的 ingest／维护时检查，没有后台 watcher。

编译和分类分别记录状态。先加入并核验目标分类，再移除 Inbox 归属。只有 ingest、批注处理、分类、记账和 lint 均完成，才移除 Inbox；某一步失败就保留待处理状态，重试只补未完成步骤。Zotero Inbox 移除不删除文件，不要求当前设备有 Git；删除 Vault inbox 投递副本仍须满足原有严格条件。非 Git 设备报告待提交状态。分类变化不改变 PDF hash，也不要求重新编译笔记。

Git 只能恢复 Wiki 文本，不能自动撤销 Zotero 分类。操作记录修改前后差异，恢复前核对当前状态并保留其间的人为修改。Vault raw 和 Zotero 原文件都需要独立备份。精确执行条件见 WORKFLOW 第 15–17 节。

### 升级与验收

Manifest v2 保留 v1 raw 记录，新增 `external_sources` 和 `zotero_items`。旧笔记无需批量重写，缺失 `source_refs` 视为空列表。同一篇文章后来进入 Zotero 时，保留旧 raw PDF，建立相同内容的关联，不自动搬迁或删除证据。不伪造历史阅读范围。

本地 hash／链接／manifest 一致性检查与 Zotero 在线可读性分开验收。先做一个小规模真实 Inbox 试点，再扩大使用；明确报告缺失依赖和未实测设备。公开 starter 只含通用协议及空状态。协议可跨 agent 使用，MCP 是可替换访问层，不是持久记忆。

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
请按 v2 WORKFLOW lint 这个 Wiki，报告 broken links、manifest/raw 问题、exact duplicates 和 needs_review 页面。不要自动处理科学冲突。
```

### 查看当前维护状态

```text
读取 _system/STATE.md 和最近的 log，告诉我 Wiki 当前最值得做什么。
```

## 一次 Ingest 会发生什么

```text
Vault source / inbox / URL OR Zotero attachment
        ↓
Capture Vault raw OR register exact Zotero attachment; SHA-256 duplicate gate
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
Vault: commit, then verified delivery-copy cleanup
Zotero: verify Topics/Methods filing, then remove Inbox membership
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

v2 不需要。先使用 index、summary、aliases、`rg`、wikilinks 和 Obsidian search。只有 pilot 后出现可重复的 retrieval failure 才增加工具。

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
