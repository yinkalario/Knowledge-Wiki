# Knowledge_Wiki Decisions

> 保存已确认的架构决定和理由，不保存讨论 transcript。新决定按日期追加。

## 2026-08-20 — 采用 Karpathy-style compiled Wiki

- Raw evidence 与 compiled knowledge 分离。
- 新来源优先更新已有知识，使 Wiki 变得更 coherent，而非只增加页数。
- 人是最终 epistemic authority，LLM agent 是可替换 maintainer。

## 2026-08-20 — Vendor-neutral protocol 位于 Vault 内

- `_system/SCHEMA.md` 与 `_system/WORKFLOW.md` 是权威协议。
- `AGENTS.md` 和 `CLAUDE.md` 仅作为薄 adapter。
- Agent history、cache、memory、hooks 和 embeddings 可丢弃。

## 2026-08-20 — v1 保持最小页面模型

- 普通知识页面只有 Source、Concept、Entity、Question、Synthesis 五类。
- Project、Decision、Comparison 等独立类型等真实需求出现后再评估。
- 不采用 numeric confidence、typed graph、claim ledger 或复杂 ontology。

## 2026-08-20 — Standard Ingest 默认 token-aware

- 使用 index、summary、aliases、`rg` 和 section-level reads。
- 首轮最多完整打开 5 个候选页，但不将 5 页作为最终更新硬上限。
- 1–10 个 material changes 属于普通 ingest 范围；超过 10 页先确认。
- Deep Ingest 必须由用户明确要求。

## 2026-08-20 — Query 默认只读，支持显式写回

- Agent 对 durable query output 主动提出 Promotion proposal。
- 用户可显式 Promote，或为当前会话启用 Research Mode。
- 不自动保存普通答案或完整 conversation。

## 2026-08-20 — 使用简单 manifest.json

- v1 通过 Vault-relative raw path、SHA-256、URL/DOI 和 affected pages 防止重复 ingest。
- JSONL event ledger、source/version IDs 等在简单 manifest 真正成为瓶颈后再考虑。

## 2026-08-20 — Obsidian 是 viewer，不是权威 runtime

- v1 只依赖 Markdown、YAML、wikilinks、backlinks、search、Graph 和 templates。
- 不安装 Wiki maintainer、Dataview、PPR、BM25 或 embedding 插件。
- `wiki/Home.md` 作为简短的人类 dashboard，展示 current research、needs review、recent updates 和知识导航；完整机器候选目录仍由 `_system/index.md` 承担。

## 2026-08-20 — Single writer、Git 与文件同步

- Codex 和 Claude Code 可以交替维护，但不能同时写。
- Git 用于 diff、审计和回滚；任何 file-sync service 都只负责文件同步，不提供并发写入协调。
- Merge、rename、delete、重大冲突和 schema change 必须先获得用户确认；后续确认的 verified inbox cleanup 是唯一狭窄例外。

## 2026-08-20 — 人类文档与个人分享边界

- 根目录 `README.md` 是面向人的 Quick Start，不复制权威协议。
- 正文与 README 默认中文，保留 canonical English terms。
- 将来分享时导出独立、干净的 starter template，不公开个人 raw、wiki、STATE、manifest、log 或 conversations。

## 2026-08-20 — Verified inbox cleanup 是狭窄删除例外

- 成功 ingest 和 commit 后，只有当 canonical raw、SHA-256、manifest、bookkeeping、lint 与附件状态全部验证通过，agent 才可自动删除未被 Git 跟踪的 inbox 临时副本。
- 任一条件不满足、附件归属不明或 inbox 文件可能是唯一副本时必须保留并报告。
- 此例外不授权删除 raw、Wiki、被 Git 跟踪的文件或任何未验证内容。

## 2026-08-20 — 论文深度按 material information 自适应

- Standard Paper Ingest 也必须产生研究可用的 reading note，token-aware 不等于 abstract-only summary。
- Equations、derivations、figures 和 tables 不设固定数量配额；保留所有影响理解、比较、判断或复现的 material details。
- Deep Ingest 追求 material completeness。长论文可以按 section/chapter 分批，但不得以节省 token 为由降低最终分析深度。
- 跨批次 Deep Ingest 必须把 section coverage 和剩余工作写入 portable STATE；全部计划覆盖完成前不得宣称完成或清理 inbox 副本。
- “完整”不要求逐字复制参考文献、通用背景或重复表述。

## 2026-08-20 — 论文 Ingest 分为 Standard、Deep 与 Exhaustive

- 本决定取代上一决定中“Deep Ingest 追求 material completeness”以及跨批次 Deep coverage 的表述；旧记录保留用于说明设计演化。
- Standard 是默认模式，生成研究可用但 token-aware 的 reading note。
- Deep 必须显式要求，目标是核心论证和证据链的深入理解；先建立 section map，再选择性编译 durable details，未写入细节保留 locator 供 Query 按需读取。
- Exhaustive 必须显式要求，承接原 Deep 的 material-completeness 职责，用于复现、审稿和逐节技术审查；跨批次进度必须写入 portable STATE。
- 三种模式共享相同 page schema、provenance、update-before-create 与高风险确认边界；差别仅在阅读覆盖和编译粒度。
- 公式、图表和实验仍不设固定数量配额，由 material value 与所选 ingest mode 决定。

## 2026-08-21 — 人类 README 改为英文默认、中文并行

- 本决定取代先前“README 默认中文”的表述；Wiki 正文仍默认中文并保留 canonical English technical terms。
- GitHub 默认入口 `README.md` 使用英文，完整中文版本位于 `README.zh-CN.md`。
- 两个版本顶部提供双向 language switch，并保持相同的用户操作、权限边界、隐私提醒和权威协议链接。
- `_system/SCHEMA.md` 与 `_system/WORKFLOW.md` 仍是唯一权威协议；双语 README 只提供人类 Quick Start，不复制或替代完整 protocol。

## 2026-08-21 — Wiki 写入语言由当前 Prompt 决定

- 本决定取代早期“正文默认中文”以及上一项决定中“Wiki 正文仍默认中文”的表述；README 的英文默认、中文并行策略不变。
- 用户明确指定 output language 时，以明确要求为准；否则，当前 user prompt 出现任何中文汉字时，本次新增或修改的正文使用中文，纯英文 prompt 使用英文。
- 该规则适用于 create 和 update，不要求沿用已有页面的语言。同一文件允许中英文混用，也不为统一语言而重写无关内容。
- Canonical English terms、论文标题、模型名、数据集名、equations、code identifiers 和必要原文引语保持原样；真实中英文 aliases 继续支持跨语言 retrieval。

## 2026-08-21 — System 文件自动检查、确认后归档

- v1 没有 background watcher；agent 在用户触发的维护、Lint、Ingest、schema review 或 handoff 中自动留意 system-file growth 和无关读取成本。
- `STATE.md` 保持 bounded；durable outcome 已写入 log 或 decision 后，已完成的临时状态可在正常维护中自动压缩，并留下记录。
- `SCHEMA.md` 与 `WORKFLOW.md` 维护 current truth；`DECISIONS.md` 与 `log.md` 保留历史，Git 提供完整 diff 和恢复能力。
- 创建 archive 目录、移动历史记录、拆分权威协议、分片 index/manifest 或改变 read order 前，agent 必须先提供具体方案并获得用户确认。
- 当前没有真实归档需求，因此不创建 archive 目录，也不引入 lifecycle scripts 或额外基础设施。

## 2026-08-21 — Raw 与 inbox 不由 Git 跟踪

- Git 跟踪 compiled Wiki、`_system/`、文档和用于保留目录结构的 `.gitkeep`，不跟踪 `raw/` 与 `inbox/` 的实际内容。
- `raw/` 仍是 Vault 内的 canonical evidence，由 file-sync service 保持跨设备可用，并由独立、版本化、最好异地的备份提供灾难恢复。
- `_system/manifest.json` 继续进入 Git，保存 raw path、来源标识和 SHA-256；hash 只能验证内容，不能恢复缺失 raw。
- `.git/` 保持在指定提交机本地，不通过 Synology Drive 或其他 file-sync service 跨设备复制。
- 用户自行 ingest 的 raw/inbox 内容从首次创建起即被 `.gitignore` 排除；starter 只保留目录 `.gitkeep`。
