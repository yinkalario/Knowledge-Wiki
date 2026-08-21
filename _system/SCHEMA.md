# Knowledge_Wiki Schema v1

> 本文件是 Knowledge_Wiki 的权威知识模型。若 README、agent adapter 或旧设计材料与本文件冲突，以本文件和 `WORKFLOW.md` 为准。

## 1. 系统边界

Knowledge_Wiki 保存长期、可复用、可追溯的知识。它不是任务管理器、日记、聊天记录仓库、书签堆或 PDF 文件柜。

长期资产分为三类：

- `raw/`：不可静默覆盖的原始证据；它证明“某来源当时说了什么”，不等于世界事实。
- `wiki/`：由 agent 编译、持续更新的当前知识。
- `_system/`：vendor-neutral 的协议、状态和 bookkeeping。

Agent history、cache、hidden memory、embeddings 和派生索引均不是权威状态。

## 2. 页面类型

v1 只有五种普通知识页面。

| Type | 目录 | 用途 |
|---|---|---|
| `source` | `wiki/sources/` | 值得独立保留的单一来源 reading note；不是 raw evidence |
| `concept` | `wiki/concepts/` | 跨来源累积的定义、机制、方法或理论 |
| `entity` | `wiki/entities/` | 持续重要的模型、数据集、工具、人物或组织 |
| `question` | `wiki/questions/` | 持续存在、值得积累证据的研究问题 |
| `synthesis` | `wiki/syntheses/` | 跨来源比较、总体判断和高层理解 |

`wiki/Home.md` 是保留的语义导航页，不属于第六种知识类型。Project、Decision、Comparison 等独立类型延后到真实需求出现后再评估。

## 3. 必需 frontmatter

每个普通 Wiki 页面必须包含：

```yaml
---
title: Canonical Page Title
type: source | concept | entity | question | synthesis
summary: 一到两句、脱离正文仍可判断相关性的摘要。
aliases: []
tags: []
sources: []
status: active | archived
needs_review: false
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

字段语义：

- `title`：领域内最常用的 canonical term。
- `summary`：用于低 token 候选筛选，不是正文摘要的重复。
- `aliases`：只记录真实存在的中英文名称、缩写和常见变体；不得为满足字段而编造。
- `tags`：少量宽泛主题标签。v1 没有受控 taxonomy。
- `sources`：Vault-relative raw paths，例如 `raw/papers/example.pdf`。它用于发现，不能替代正文中的重要 claim citation。
- `status`：正常页面为 `active`；合并或不再参与当前导航的页面为 `archived`。
- `needs_review`：仅在真实冲突、重要不确定性或需要人类科学判断时设为 `true`。
- `created` / `updated`：页面建立日期与最后一次语义修改日期；`updated` 不表示事实已重新验证。

允许 type-specific optional fields，例如 Source 的 DOI、Question 的 `question_status`，但不要将可由正文表达的信息重复堆进 frontmatter。

## 4. 语言、命名与链接

- 用户明确指定 output language 时，以该要求为准。
- 未明确指定时，只根据当前 user prompt 判定本次新增或修改正文的语言：prompt 中出现任何中文汉字则使用中文；prompt 为纯英文则使用英文。
- 该规则同时适用于新建页面和更新已有页面，不要求延续页面原有语言。同一页面中英文混用是允许的，不应为统一语言而改写未受本次任务影响的内容。
- 无论正文语言为何，都保留 canonical English technical terms、论文标题、模型名、数据集名、equations、code identifiers 和必要的原文引语。
- `aliases` 继续记录真实存在的中英文名称和常见变体，以支持跨语言检索；不得为追求双语对称而编造名称。
- 文件名与 `title` 尽量一致，并在整个 `wiki/` 中保持 basename 唯一。
- 使用 Obsidian `[[wikilinks]]` 连接真正有助于理解或导航的页面。
- 不要求每页达到固定链接数量；合法 orphan 优于虚假关系。
- 不创建只包含一两句话、无法独立复用的页面。
- Rename、merge、delete 前必须获得用户确认，并同步更新链接、index、manifest 和 log；唯一例外是 `WORKFLOW.md` 定义的 verified inbox cleanup，它只删除已验证、未被 Git 跟踪的投递副本。

## 5. Create、Update 与页面边界

### Update before create

创建页面前必须搜索 title、aliases、关键术语和同义词。主题已有合适页面时，将 material knowledge 合并进去。

新页面至少满足一项：

- 是持久且可复用的概念、实体或研究问题；
- 预计会从多个页面被引用；
- 有足够独立内容，分离后明显改善导航或推理；
- 是真正跨来源、以后重建成本较高的 synthesis。

不要因为来源提到一个名词就创建 Entity，也不要把每个段落拆成页面。

### Source 与 Raw

- Raw 保存来源本身。
- Source page 保存对单一来源的编译理解。
- 并非每个 raw source 都需要 Source page。
- Source page 不可作为其他页面的最终证据；重要 claim 仍应能回到 raw。

### Academic / research paper Source page

对研究有持续价值的论文通常应建立独立 Source page；exact duplicate、`no_material` 或只为现有结论增加轻微支持的论文可以例外。论文 Source page 是可复用的 research reading note，不是 abstract 的改写。覆盖深度由 Standard、Deep 或 Exhaustive Ingest 决定，但任何模式都应按论文实际内容交代：

- research question、背景、贡献和适用范围；
- 核心定义、assumptions、method / architecture 与关键设计选择；
- datasets、splits、preprocessing、baselines、metrics 和 experimental setup；
- 关键结果、ablations、sensitivity、negative results 与 threats to validity；
- 作者明确陈述的 limitations、可复现性信息、开放问题和与已有 Wiki 的关系。

公式没有固定数量配额。Standard 与 Deep 应保留足以理解核心贡献、解释实验、比较方法和判断复现要求的 equations / derivations；Exhaustive 应覆盖所有具有 material value 的公式与推导。任何模式都省略不会增加实际理解的教科书式、装饰性或重复公式。保留公式时同时记录：

- 可读的 LaTeX 表达；
- symbols、输入输出和单位（若适用）；
- assumptions、该公式在方法中的作用及必要的推导逻辑；
- equation、section 或 page locator。

Figures 和 tables 采用相同原则：Standard 与 Deep 选择性编译承载核心 claim、实验比较、failure mode 或方法结构的 visual evidence；Exhaustive 覆盖所有 material visual evidence。不按固定数量截断，也不为完整而机械复制装饰性内容。

Ingest mode 改变的是阅读覆盖与编译粒度，不改变 page type、frontmatter 或 provenance 标准。未编译进 Source page 的细节仍保留在 raw，后续可以按 locator 定向读取；不能把“可按需恢复”写成已经验证的结论。

### Concept 与 Synthesis

- Concept 是一个主题的最佳当前解释，随着来源加入持续更新。
- Synthesis 是有明确问题、比较维度、范围或结论的跨来源分析。
- 如果内容只是解释一个主题，应更新 Concept；只有形成独立论证或比较时才创建 Synthesis。

### Question

Question 只用于持续研究问题，不用于保存一次性 query。建议使用可选字段：

```yaml
question_status: open | provisional | answered | closed
```

## 6. Provenance

以下内容必须在靠近 claim 的位置引用 raw evidence：

- 精确数字、日期和 benchmark；
- 直接引语；
- 当前产品、软件、组织或政策状态；
- 关键实验结果；
- 争议性或可能被误解的结论。

推荐使用 Markdown footnote，指向 Vault-relative raw path：

```markdown
该实验在 Dataset X 上报告了 12.3 的结果。[^paper-p7]

[^paper-p7]: [[raw/papers/example.pdf#page=7]]，Table 2。
```

Web snapshot 可链接到 heading；论文在容易取得时保留 page、section、figure、table 或 equation locator。普通稳定 paraphrase 可以依赖页面 `sources`，无需给每句话添加 footnote。

Wiki 页面之间的链接用于导航和解释，不构成循环证据。Derived synthesis 写回 Wiki 时必须保留原始 raw sources。

## 7. Inference、Disagreement 与 Freshness

### Inference

来源没有直接表达、由 agent 或用户推导的结论使用明确标记：

```markdown
**[Inference]** 该结果可能意味着……
```

### Disagreement

- 在相关页面的 `Evidence and disagreement` 小节并列呈现不同主张、范围和来源。
- 不自动假定较新来源或更多来源一定正确。
- 先检查 dataset、split、metric、version、population、assumption 和 evaluation protocol 是否不同。
- 需要用户判断时设置 `needs_review: true` 并在 `_system/STATE.md` 添加链接。

### Freshness

- Timeless：不需要 freshness metadata。
- Snapshot：正文使用 `as of YYYY-MM-DD`。
- Pointer：保存权威 URL，并注明 `last checked: YYYY-MM-DD`。
- 不使用统一的“90 天未更新即 stale”规则。

## 8. Lifecycle 与结构变更

- Agent 可以创建和更新 `active` 页面。
- 不要求用户审阅每次普通 additive ingest。
- 合并页面时，将独有内容和 sources 转入 canonical page，修复链接，将旧页设为 `archived` 并明确指向 canonical page。
- Raw evidence 永不因 Wiki merge/archive 被删除。
- Schema change 必须获得用户确认并记录在 `DECISIONS.md` 和 `log.md`。

## 9. Token-aware invariants

- 使用 index、summary、aliases 和 targeted search 先筛选，再读取全文。
- Standard Ingest 首轮最多完整打开 5 个候选页面；后续候选优先读取 frontmatter、summary 或命中 section。
- Targeted patch 优先于整页重写。
- 页面数量是风险提示，不是知识更新的硬上限。
- 不因弱关联扩大 cascade，也不遍历整个 Wiki graph。

## 10. v1 明确不包含

- Numeric confidence 或 source-quality scoring；
- Typed relationship ontology；
- Claim ledger 或 contradiction database；
- Project page type；
- Vector DB、graph DB、embeddings、PPR 或 BM25；
- Background watcher、scheduled ingest 或 automatic reconciliation；
- Staging transaction、locks 或多 writer。
