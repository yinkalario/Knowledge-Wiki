[English](README.md) | **简体中文**

<h1 align="center">
  <img src="assets/knowledge-wiki-logo.png" alt="Knowledge Wiki logo" width="72" align="absmiddle">
  Knowledge Wiki
</h1>

<p align="center"><strong>用 Zotero 阅读文献，用 Markdown 积累知识，让 agent 始终可以替换。</strong></p>

Knowledge Wiki 把论文、文章和研究讨论编译成持续维护、可以回到原文核验的知识库。它借鉴 LLM Wiki 的方式：让 agent 优先更新已有理解、连接相关发现、保留分歧与证据，而不是每导入一个文件就孤立地生成一份摘要。

> [!IMPORTANT]
> **V2 同时支持 Zotero 和纯 Vault 工作流。** Zotero 是可选组件。下面覆盖 Mac／Windows 本机和 Zotero 个人文献库；群组库自动化不属于当前 Wiki 协议范围。安装说明于 **2026-09-30** 对照上游文档和本机 `zotero-mcp` 0.13.1 核对，不代表每种客户端／操作系统组合均已实测。

## 从这里开始

- [V2 把什么保存在哪里](#v2-把什么保存在哪里)
- [让 agent 帮你配置](#让-agent-帮你配置)
- [1. 准备 Vault 和 agent](#1-准备-vault-和-agent)
- [2. 准备 Zotero 和 PDF 同步](#2-准备-zotero-和-pdf-同步)
- [3. 安装 Zotero MCP](#3-安装-zotero-mcp)
- [4. 连接 Codex](#4-连接-codex)
- [5. 连接 Claude](#5-连接-claude)
- [6. 开启分类写入权限](#6-开启分类写入权限)
- [7. 绑定个人文献库和 collections](#7-绑定个人文献库和-collections)
- [8. 核验连接](#8-核验连接)
- [9. 第一次 ingest](#9-第一次-ingest)
- [故障排查](#故障排查)
- [日常操作](#主要操作方式)、[Obsidian 浏览](#在-obsidian-中浏览)、[同步与备份](#文件同步与-single-writer)

## V2 把什么保存在哪里

| 内容 | 由谁保存、保存在哪里 | Wiki 保留什么 |
|---|---|---|
| 从 Zotero 导入的 PDF | Zotero 的 stored attachment；通过 Zotero Storage 或 WebDAV 同步 | 精确附件身份、文件 hash、版本、页码链接、阅读范围、编译笔记；**不在 Vault raw 再复制一份 PDF** |
| 投递到 Vault `inbox/` 的 PDF | canonical 原件保存在 `raw/papers/` | 继续支持原有 Vault-only ingest 与引用 |
| Web Clipper Markdown、本地文本、网页快照 | Vault `inbox/` → 对应 `raw/` 目录 | 原始证据及编译后的知识 |
| 编译时实际使用的 Zotero 高亮、评论、子 note | 原件在 Zotero；所选内容的不可覆盖快照在 `raw/other/`，必要图片在 `raw/assets/` | 实际使用内容、原始 key／定位与 hash；不是完整 PDF 备份 |
| 编译后的知识 | `wiki/` | Source、Concept、Entity、Question、Synthesis，仍然只有五种页面 |
| 协议和接管状态 | `_system/` | 普通 Markdown／YAML／JSON，不依赖特定模型的聊天历史 |

Zotero 管理文献 metadata、阅读、批注和附件；Obsidian 展示 Markdown Wiki，并可抓取非 PDF 来源；agent 维护知识并在需要时核查原文。Collection 是文章的组织归属，不是 PDF 副本，同一篇文章可以属于多个 collection。

Source note 会包含 `zotero://open-pdf/library/items/ATTACHMENT_KEY?page=7` 这样的链接，Obsidian 可交给已安装的 Zotero 打开。链接打开的是**当前附件**；记录的 SHA-256 才能让 agent 判断实际文件是否与引用版本一致。被引用的旧版本应保留为独立附件。Collection 的变化不参与 PDF hash 计算。Obsidian Graph 使用 Wiki 内部链接，外部 Zotero URL 本身不是 graph 节点。

不要求向量数据库、embedding 订阅、watcher 或定时 ingest。Standard Ingest 先检索已有摘要与知识页，再读取任务所需原文；Deep 和 Exhaustive 必须明确选择。

## 让 agent 帮你配置

把[这份中文 README](https://github.com/yinkalario/Knowledge-Wiki/blob/main/README.zh-CN.md) 或[英文 README](https://github.com/yinkalario/Knowledge-Wiki/blob/main/README.md) 交给 **ChatGPT、Codex 或 Claude** 都可以，说明与配置提示词不绑定某一家客户端。助手不能打开网页时，粘贴 README 正文；本地 agent 也可以直接读取文件。这是手动步骤的替代入口，不需要再安装一遍。

**先确认 agent 实际拥有的权限。** 没有本机工具的聊天只能解释步骤、生成适合你的命令，不能安装软件、修改 Vault 或访问本地 Zotero。需要直接配置时，使用本地 Codex／Claude Code workspace，或另一个已明确连接并授权本机能力的环境。仅接入 Zotero MCP 不会同时授予 Vault 文件访问权。

| 当前使用环境 | 怎样使用本指南 |
|---|---|
| 没有本机工具的 ChatGPT／Claude 聊天 | 读取／粘贴 README，生成适合你的步骤，由你执行本机操作。 |
| 本地 Codex 桌面版／CLI | 授予 workspace 和执行权限，通过 `AGENTS.md` 接入；按第 4 步配置 MCP，执行共同验收。 |
| 本地 Claude Code | 授予 workspace 和执行权限，通过 `CLAUDE.md` 接入；按第 5 步配置 MCP，执行同一套验收。 |
| Claude Desktop | 按第 5 步连接 Zotero；写 Wiki 和安装程序还需要相应的本机文件／执行工具，委托前先确认权限。 |

Codex 和 Claude Code 是平等的维护入口，共用 `_system/` 协议、来源身份、模板和 manifest，不需要互相移交聊天历史。客户端配置格式不同：不要把 Codex TOML 粘进 Claude JSON，反之亦然。参见 [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp) 和 [Claude Code MCP](https://code.claude.com/docs/en/mcp)。

复制下面的提示词，填写四个字段：

```text
请依据这份 README 帮我配置 Knowledge Wiki v2：
https://github.com/yinkalario/Knowledge-Wiki/blob/main/README.zh-CN.md

操作系统：<macOS / Windows>
目标本地客户端：<Codex 桌面版 / Codex CLI / Claude Code / Claude Desktop / 其他>
Vault：<现有文件夹或希望新建的位置>
是否使用 Zotero：<是 / 否>

先确认你是否能访问本机文件、终端和 MCP。没有这些权限时，给我准确的手动步骤，
不要声称已经执行。Codex 读取 AGENTS.md，Claude Code 读取 CLAUDE.md，均遵守
_system 权威协议。按 README 中目标客户端的对应章节配置，不要把当前解释步骤的聊天
客户端与目标客户端混淆。若要求同时配置两者，分别注册并验收，无需重复安装 tool。
修改前检查已安装程序与现有配置，复用可用组件。修改客户端配置前先备份，再定向合并，
保留其他 MCP。新 Vault 使用公开 starter，不要覆盖已有个人 Wiki。

如果可以直接操作本机，请安装缺少的前置工具和 zotero-mcp-server[pdf]，使用真实的
可执行文件绝对路径注册一个本地 STDIO server，并验证连接。优先本地 Zotero 读取；
需要自动 Topics/Methods 分类时，检查 Zotero 版本并配置相应写入方式。账号登录、
密钥输入和 Zotero 授权弹窗由我在本机完成，不要输出 secrets。客户端配置与凭据放在
Vault 外，不要运行 install-skill、覆盖 Wiki adapters、建立 embedding 索引或公开 tunnel。

解析我的稳定个人账号 user ID 和 collection keys，只把绑定写入本 Vault 的
_system/zotero-collections.md。复用已有 roots；缺失或含义不明时先提出具体的最小
初始化方案，再创建。Projects 和 Archive 由我管理，属于保护范围。
按下文完成只读验收，不要为测试而 ingest、移动文章或重构 collections。报告哪些检查
通过、实际改了什么、仍需我手动完成什么，并给出下一步可用的首次 ingest 提示词。
```

普通 ChatGPT 网页 developer mode 使用远程 MCP endpoint，不能直接填入下文的本地 STDIO 命令。具体能力取决于账号和环境；远程 MCP 也不会自动获得 Vault 文件访问权。本指南采用本地客户端，不通过无认证 tunnel 公开 Zotero。若确实需要独立的远程部署，请另行查看 [OpenAI developer-mode 文档](https://developers.openai.com/api/docs/guides/developer-mode)。

## 1. 准备 Vault 和 agent

1. 安装 [Obsidian](https://obsidian.md/download)。需要把网页抓成 Markdown 时，可选装 [Obsidian Web Clipper](https://obsidian.md/clipper)。
2. 获取**公开 starter**，而不是其他人的在用 Vault。在[仓库页面](https://github.com/yinkalario/Knowledge-Wiki) 选择 **Code → Download ZIP**，解压到个人工作目录。已安装 Git 时也可以执行：

   ```bash
   git clone https://github.com/yinkalario/Knowledge-Wiki.git Knowledge_Wiki
   ```

   Clone 后的 `origin` 仍指向公开 starter，并不是你的个人备份仓库。推送个人内容前，先配置自己的 private repository。ZIP 用户也可以先不使用 Git，以后再初始化私有仓库。
3. 在 Obsidian 中选择 **Open folder as vault**，打开同时包含 `_system/`、`wiki/`、`raw/`、`inbox/` 和 adapters 的整个根目录。
4. 安装并登录本地客户端：[Codex](https://learn.chatgpt.com/docs/quickstart) 或 [Claude Code](https://code.claude.com/docs/en/overview)。把 Vault 根目录添加／打开为本地 workspace。云端 checkout 不会自动连接到你电脑上的 Zotero。
5. 对 agent 说：“读取仓库 instructions，了解这个 Wiki，先不要修改文件。”Codex 通过 `AGENTS.md`，Claude Code 通过 `CLAUDE.md` 接入，共同遵守 `_system/`。

已有 Vault 不要直接用 starter 全量覆盖，必须保留原有知识、raw、manifest 和状态。**不使用 Zotero 时，跳过第 2–8 步，直接使用第 9 步的 Vault 入口。**

版本通过 Git **分支**区分：`main` 是最新维护版本，`v1` 保留引入 Zotero 前的版本，`v2` 是 V2 发布分支。新用户从 `main` 开始。分支不会自行同步，由维护者把 V2 更新发布到 `main` 和 `v2`。

## 2. 准备 Zotero 和 PDF 同步

安装 [Zotero，可选安装 Zotero Connector](https://www.zotero.org/download/)。本地访问使用 Zotero 7+，写入方式在第 6 步确定。Better BibTeX 可用于 citation keys，但**不是本 Wiki 或 MCP 的必要依赖**。

1. 各设备在 **Zotero Settings → Sync** 登录账号。Metadata 和批注通过 Zotero 账号同步；附件选择 Zotero Storage 或 WebDAV。使用 WebDAV 时在 Zotero 填写服务商／NAS 的 URL、用户名和密码，并完成 **Verify Server**。WebDAV 同步的是附件，不是正在运行的 Zotero 数据库。参见 [Zotero 同步说明](https://www.zotero.org/support/sync)和[同步设置](https://www.zotero.org/support/preferences/sync)。
2. 导入一份 PDF，使用 Zotero 管理的 **stored attachment**，有文献 metadata 时挂在对应条目下。实际打开一次，确认 PDF 已下载且可读。位于 Zotero storage 外的 linked file 不属于通常的 Zotero 文件同步路线。参见[导入文献](https://www.zotero.org/support/adding_items_to_zotero)。
3. 开启 **Settings → Advanced → Miscellaneous → Allow other applications on this computer to communicate with Zotero**。macOS 在 Zotero 菜单进入 Settings，Windows 在 Edit 菜单进入。使用本地 MCP 时保持 Zotero 运行。参见[上游本地设置](https://github.com/54yyyu/zotero-mcp/blob/main/docs/getting-started.md#configure-zotero)。

本地读取和计算 hash 需要 Zotero 管理／下载的那份 PDF；“PDF 留在 Zotero”不等于电脑完全没有 PDF 文件。不要把 `zotero.sqlite` 移进 NAS／Obsidian 的同步文件夹。iPad、iPhone、Android 继续用 Zotero 阅读和批注；只有需要 agent 读原文的电脑才安装 MCP。

## 3. 安装 Zotero MCP

本指南采用第三方 [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)，不是 OpenAI 或 Zotero 官方开发的 server。插件目录中名称相近的产品可能使用其他实现，不要无意配置两份。

只选择**一种安装方式**。下文用 `uv` 管理隔离的 Python tool 环境；`pdf` extra 提供页面图片支持。Wiki 的普通工作流无需 semantic search。包依赖和 extras 见项目的[包配置](https://github.com/54yyyu/zotero-mcp/blob/main/pyproject.toml)。

### macOS：Terminal

如果 `uv --version` 已正常输出，跳过 uv 安装。否则使用 [uv 官方安装器](https://docs.astral.sh/uv/getting-started/installation/)：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

关闭并重新打开 Terminal，然后执行：

```bash
uv --version
uv python install 3.12
uv tool install --python 3.12 "zotero-mcp-server[pdf]"
uv tool update-shell
```

再开一个新 Terminal，检查：

```bash
zotero-mcp version
command -v zotero-mcp
uv tool dir --bin
```

记下真实路径，例如 `/Users/YOUR_NAME/.local/bin/zotero-mcp`。你的安装目录可能不同。

### Windows：原生 PowerShell

初次安装且 Zotero 运行在 Windows 时，建议使用原生 PowerShell 和原生客户端。WSL 是另一个可选运行环境，不是必需，也不代表本地集成会更简单。

如果 `uv --version` 失败，执行 [uv 官方 Windows 安装命令](https://docs.astral.sh/uv/getting-started/installation/)：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

关闭并重新打开 PowerShell，然后执行：

```powershell
uv --version
uv python install 3.12
uv tool install --python 3.12 "zotero-mcp-server[pdf]"
uv tool update-shell
```

再开一个新 PowerShell 窗口，检查：

```powershell
zotero-mcp version
(Get-Command zotero-mcp).Source
uv tool dir --bin
```

记下真实 `.exe` 路径，例如 `C:\Users\YOUR_NAME\.local\bin\zotero-mcp.exe`。仍找不到时，检查 `uv tool dir --bin` 输出的目录；更新 PATH 后也要重启客户端。不要把 Mac 路径填进 Windows。

已经通过 uv 安装、但缺 PDF 支持时，先记录 `zotero-mcp version`，再执行 `uv tool install --force "zotero-mcp-server[pdf]"` 并重连客户端；这可能同时升级包。如果原来用 pipx／pip 安装，应在原环境添加依赖，不要叠加一套安装。参见 [uv tool 环境](https://docs.astral.sh/uv/guides/tools/)。

**本流程不要运行 `zotero-mcp install-skill`**，因为它可能改写 agent 入口文件。这里使用 MCP，保留 Wiki 自己的 adapters。`zotero-mcp setup` 是另一种客户端配置器，不是前置步骤，不必在手动配置完成后再运行。基础流程也不需要 `update-db`、embedding model 或 OpenAI API key。

## 4. 连接 Codex

GUI、配置文件、CLI **选择一种即可**。程序路径来自第 3 步的真实输出，不是包名 `zotero-mcp-server`。使用桌面 GUI 不要求终端已经能运行 `codex`。

### 桌面 GUI

进入 **Settings → MCP servers → Add server**。部分版本入口是 **Plugins → Add → Add MCP server**。填写：

| 字段 | 填写内容 |
|---|---|
| Name | `zotero` |
| Type | `STDIO` |
| Command to launch | `zotero-mcp`／`zotero-mcp.exe` 的真实绝对路径 |
| Arguments | 无参数；删除空参数行 |
| Environment variable name | `ZOTERO_LOCAL`，必须全部大写 |
| Environment variable value | `true` |
| Environment passthrough | 基础配置留空 |
| Working directory | 不设置 |

保存、启用并重启／重连 server；工具列表未刷新时再开新聊天。该程序无参数启动时默认使用 STDIO。参见 [Codex 官方 MCP 配置](https://learn.chatgpt.com/docs/extend/mcp)。

### 配置文件方式

合并到当前生效的用户级 `~/.codex/config.toml`。Windows 通常在 `%USERPROFILE%\.codex\config.toml`，自定义 `CODEX_HOME` 会改变位置。保留现有配置，不要重复创建 `[mcp_servers.zotero]`。不确定时从 GUI 打开当前配置。

macOS 示例：

```toml
[mcp_servers.zotero]
command = "/Users/YOUR_NAME/.local/bin/zotero-mcp"

[mcp_servers.zotero.env]
ZOTERO_LOCAL = "true"
```

Windows 示例，TOML 使用单引号原样保留反斜杠：

```toml
[mcp_servers.zotero]
command = 'C:\Users\YOUR_NAME\.local\bin\zotero-mcp.exe'

[mcp_servers.zotero.env]
ZOTERO_LOCAL = "true"
```

这些机器专属设置放在共享 Vault 之外。参见[配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)。

### 可选 CLI 方式

仅当已经安装 Codex CLI，且 `codex --version` 能运行时使用：

```bash
codex mcp add zotero --env ZOTERO_LOCAL=true -- "/ABSOLUTE/PATH/TO/zotero-mcp"
codex mcp list
```

原生 PowerShell 中命令形式相同，把路径换成真实 Windows `.exe` 路径。出现 `command not found: codex` 代表当前不能使用这条 CLI 路线，改用桌面 GUI 或配置文件即可。参见[官方 CLI 命令](https://learn.chatgpt.com/docs/developer-commands)。

## 5. 连接 Claude

只使用 Codex 时跳过。本机可以同时配置多个客户端，但同一时间只能有一个 agent 写 Wiki。

### Claude Code

安装并登录 Claude Code 后，把实际程序路径填入下面的一行命令：

```bash
claude mcp add --scope user --env ZOTERO_LOCAL=true --transport stdio zotero -- "/ABSOLUTE/PATH/TO/zotero-mcp"
claude mcp get zotero
```

原生 Windows 填写 `.exe` 路径。在 Vault 文件夹重启 Claude Code，通过 `/mcp` 检查连接。User scope 将机器配置保存在共享仓库之外。如果已存在 `zotero`，先检查并编辑原条目，不要重复添加。参见 [Claude Code MCP 文档](https://code.claude.com/docs/en/mcp)。

### Claude Desktop

若当前版本提供 **Settings → Developer → Edit Config**，通过它找到生效的 `claude_desktop_config.json`。常见位置是 macOS 的 `~/Library/Application Support/Claude/` 和 Windows 的 `%APPDATA%\Claude\`，不同构建可能有区别。合并下面的条目，保留其他 `mcpServers`，完全退出并重新打开 Claude Desktop：

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

Windows 替换 `command`，注意 **JSON 反斜杠需要写两次**，例如 `"C:\\Users\\YOUR_NAME\\.local\\bin\\zotero-mcp.exe"`。参见[上游 Claude 配置步骤](https://github.com/54yyyu/zotero-mcp/blob/main/docs/getting-started.md#integrating-with-claude-desktop-and-claude-code)。

Claude Desktop 接通 Zotero server 后获得文献工具；维护 Wiki 还需要另外明确授权 Vault 文件访问并读取协议。没有这项能力时，使用 Claude Code 执行 Wiki 写入。

## 6. 开启分类写入权限

本地可读不代表可以自动分类。Wiki 需要增量修改 collection 成员关系，并在合理情况下创建分类；普通 ingest 不需要顺便重写所有文献 metadata。

### Zotero 10+：本地授权

保持 Zotero 打开，运行：

```bash
zotero-mcp authorize-local
```

由你本人处理 Zotero 弹窗；需要持久授权时选择 **Always Allow**。工具把本地授权保存在 Vault 之外的用户配置中。重启／重连 MCP 后检查：

```bash
zotero-mcp authorize-local --status
```

也可以让已连接的 agent 检查 `zotero_write_capabilities`，必要时调用 `zotero_authorize_local_writes`。能力检查通过不等于已完成真实写入，首次 ingest 的回读会验证实际效果。参见[本地写入授权](https://github.com/54yyyu/zotero-mcp/blob/main/docs/configuration.md#local-write-support)。

### 较旧 Zotero：本地读取＋Web API 写入

1. 登录 [Zotero API keys 页面](https://www.zotero.org/settings/keys)，为个人库创建具备所需 library read/write 权限的 key，记下页面显示的数字 **user ID**。
2. 保留 `ZOTERO_LOCAL=true`，在所选 MCP 客户端的私有环境变量配置中添加 `ZOTERO_API_KEY`（该 key）、`ZOTERO_LIBRARY_ID`（该数字 user ID）、`ZOTERO_LIBRARY_TYPE=user`。Secret 在本机输入，不要放进聊天、README 或 Vault 文件。
3. 重连 MCP，让 agent 检查写入能力。通过 Web API 写入后，等待 Zotero 同步完成，再核对桌面状态。

NAS 密码、Zotero 账号密码、Web API key 和本地写入授权是不同的东西。本地读取不需要 Web API key；Zotero 10 完成本地授权后通常也不需要它来写入。没有写入权限时仍可编译知识，但分类／Inbox 收尾必须保留为 pending。参见[连接模式](https://github.com/54yyyu/zotero-mcp/blob/main/docs/configuration.md#connection-modes)。

## 7. 绑定个人文献库和 collections

客户端连接与 Wiki 绑定是两件事。修改**个人副本**里的 [`_system/zotero-collections.md`](_system/zotero-collections.md)，公开 starter 故意保留为 unconfigured。

建议的根分类：

```text
00 Inbox
10 Topics         研究什么
20 Methods        核心方法怎么做
30 Projects       由你管理
90 Archive        由你管理
```

已有分类能承担这些角色时直接复用。Roots 缺失时，确认最小初始化方案，或在 Zotero 手动创建；不必导入别人整套 taxonomy。例如 `10 Topics/Music & Musical Audio` 与 `20 Methods/Generative Modeling` 是两个独立维度。Topics／Methods 使用稳定、描述性的名称，避免每篇论文一个类别或随意加入年份前缀。

对 agent 说：

```text
请配置本 Vault 的 Zotero 绑定。读取个人库的实际 collection tree，确认稳定账号
user ID 以及 Inbox、Topics、Methods 的 keys。把它们、规则版本／日期、受管理分类的
name/key/parent tree 和简明边界写入 _system/zotero-collections.md，并标记
Projects／Archive 受保护。复用已有 roots；缺失或含义不明确时先提方案再创建。
本次只做设置，不 ingest，不改变已有文章的分类关系。
```

手动设置时，在 [Zotero keys 页面](https://www.zotero.org/settings/keys) 取得账号 user ID，用已连接 MCP 的 collection listing 获取 keys／parents，再填入配置文件对应字段。本地 API 的 `0`、SQLite library number `1`、collection 名称和稳定账号 ID 不是同一个东西。不要猜 key，也不要把本机 PDF 目录写进配置。

普通 ingest 可以添加合适的 Topics／Methods 归属，必要时创建含义明确、可复用的新类别。**Projects 和 Archive 受保护。** 对已有类别重命名、移动、合并、拆分或删除，需要先确认具体方案，再复核所有受影响旧文章。可以明确要求全库发现，但不因此自动授权全库重分类。

## 8. 核验连接

在 Zotero 保留一份已下载的已知 PDF，要求执行**只读**验收：

```text
请核验 Knowledge Wiki v2 配置，不 ingest、不修改 Zotero、不保存笔记。
确认能读取 Vault 协议，并识别当前个人文献库。列出绑定的 collection roots，定位我指定
的一篇论文、parent key 和精确 PDF attachment key。解析本机 PDF，计算 SHA-256，读取
指定物理页的文本和一页图片，检查其批注。区分真实零批注与 API 错误。检查写入能力，
但不要实际写入。逐项报告通过／失败，以及实际测试的客户端和操作系统。
不要暴露 credentials，也不要建立索引。
```

各项应分别验收：

- **客户端：** MCP 已连接且工具可调用；仅保存了配置不算成功。
- **原文：** 实际 PDF 文件可访问，已计算 hash，指定页文本／图片可读；只有 metadata 或 abstract 不算完成 PDF ingest。
- **批注：** 取得真实批注或确认空结果；缺失能力需保留为待处理。
- **绑定：** 稳定库身份和 collection keys 与实时数据一致。
- **写入：** 写入路线可用；首次真实 ingest 再测试增量增删与回读。
- **Wiki 访问：** agent 具备 Vault 本机文件读写能力；只读验收不必创建测试文件。

如果同时使用 Codex 和 Claude Code，在两个客户端分别对同一文献库／PDF 执行这份验收，确认 attachment key 和 SHA-256 一致。一边通过不代表另一边已连接。随后在另一客户端开启新会话，只依靠 adapter 和 Wiki 文件查询已有 Source，不重新 ingest，也不修改文件。每个结果单独记录；文档支持不等于已经完成端到端实测。

首次 Source note 出现后，在**每台桌面设备**从 Obsidian 点击一个页码链接，确认打开正确 PDF 和页码。这项检查验证系统链接处理程序，与 MCP 读取和文件 hash 核验分别进行。

## 9. 第一次 ingest

### Zotero 入口

把**选定的一篇论文**放进已配置的 `00 Inbox`，确认 PDF 在本机可打开，然后说：

```text
请对 Zotero 00 Inbox 中的 <论文标题或 item key> 做 Standard Ingest，PDF 留在 Zotero。
先检索已有知识，再决定更新或创建。记录精确附件身份、SHA-256、论文版本、物理页码链接
和实际阅读范围，只快照编译中实际使用的批注／notes。仅分类 Topics／Methods，保留
Projects／Archive。先添加并核验目标归属，只有编译、批注处理、记账和 lint 成功后，
才移除 Inbox 归属。报告修改文件、分类差异和任何未完成步骤。
```

打开 `wiki/Home.md` 和生成的知识页。有持续价值的论文通常会获得 Source note；精确重复或无新材料的来源不必创建空页面。小试点通过后，日常说“请处理 Zotero Inbox”，即可处理待入库论文。

### Vault 入口：可以完全不使用 Zotero

通过 Obsidian Web Clipper 把网页保存到 `inbox/`，或把 PDF／Markdown／文本放进去，再说：“请对 Vault inbox 的新资料做 Standard Ingest。”Agent 保留 canonical raw、核对 hash、更新已有知识，并在协议条件全部通过后清理投递副本。从 Vault 投递的 PDF 仍支持留在 Vault，不会被静默搬到 Zotero。

### 提问与失败续接

可以问：“根据 Wiki 解释这篇论文的公式 3，并回到引用页核验。”Query 默认只读，根据 raw 路径或精确外部来源引用找到原文并核对 hash。Zotero 不可用时，必须区分已有 compiled coverage 与无法重新核验的细节。

PDF hash 在 Vault 与 Zotero 来源间统一查重。已完成 ingest 的重复文件复用知识；待完成分类或新使用批注仍可处理。未完成 ingest 续接剩余工作，分类变化不触发 PDF 重新 ingest。分类成功和 Inbox 移除分别记账，失败重试不必全部重来。

实际使用的批注快照位于 `raw/other/`，包含来源身份、PDF hash、annotation／note keys、定位和内容。Payload hash 不含捕获时间，内容变化时创建新快照。这些快照遵循 Vault raw 的文件同步／备份，**不进入 Git**，也不能恢复丢失的 PDF。详见 [SCHEMA 第 11 节](_system/SCHEMA.md#11-external-evidence-and-backward-compatible-manifest-v2) 和 [WORKFLOW 第 15–17 节](_system/WORKFLOW.md#15-zotero-connection-discovery-and-ingest)。

## 故障排查

| 现象 | 下一步检查 |
|---|---|
| `codex: command not found` | 改用桌面 GUI／配置文件；GUI 配置不要求另外安装 CLI。 |
| 找不到 `zotero-mcp` | 重开终端，查看 `uv tool dir --bin`，客户端填写真实绝对路径。 |
| 保存了 MCP 但连不上 | 确认 Zotero 运行、允许本地通信、`ZOTERO_LOCAL=true` 全大写；删除空参数行，重连并检查客户端错误。 |
| 搜索成功但 PDF 读取失败 | 在 Zotero 打开／下载精确附件。只有 WebDAV 上的远程文件或 metadata 不等于本机有 PDF。 |
| 缺 `fitz`／PyMuPDF，图片读取失败 | 给**同一 tool 环境**补 `pdf` extra，再重连；也可用已核验的本地 PDF reader，报告实际采用的路线。 |
| 可读但分类失败 | 检查本地授权或 hybrid key 权限、write capabilities；不要标记 Inbox 已完成。 |
| 找不到文章、库错误或 key 不存在 | 核对 active personal library、同步状态和实际 root keys。另一台电脑未同步不是重新 ingest 的理由。 |
| Obsidian 链接打不开或内容不对 | 检查 Zotero 已安装、账号／附件对应、PDF 已下载及 `zotero://` 关联，再核对当前文件 hash。 |
| PDF hash 改变 | 登记新快照并调查差异，不静默替换旧引用；必要时从 Zotero 备份恢复旧文件。 |
| Windows Zotero＋WSL agent 失败 | 确认 MCP 究竟在哪个系统运行、怎样连接 Zotero 和解析附件路径。本指南优先原生 Windows，不假设 localhost／路径跨环境通用。 |
| 同名 server 出现两次 | 每客户端保留一份明确配置，安装前检查同名 plugin 的实际实现。 |
| 设置时不断建议 embeddings | 基础检索使用 index、summary 和定向搜索，不用 semantic indexing 修复连接问题。 |

更多实现相关问题见 [Zotero MCP troubleshooting](https://github.com/54yyyu/zotero-mcp/blob/main/docs/troubleshooting.md)。不要把未脱敏的客户端配置或授权文件贴到公开 issue。

## 仓库与 Vault 目录结构

```text
Knowledge_Wiki/
├── wiki/                 编译后的知识
│   ├── Home.md           人类导航首页
│   ├── sources/          单一来源的可复用笔记
│   ├── concepts/         跨来源累积的概念解释
│   ├── entities/         模型、数据集、工具、人物、组织
│   ├── questions/        持久研究问题
│   └── syntheses/        跨来源比较与论证
├── _system/              Vendor-neutral 协议与可接管状态
│   ├── SCHEMA.md / WORKFLOW.md / DECISIONS.md
│   ├── zotero-collections.md   个人绑定；starter 未预配置
│   ├── templates/        五种页面模板
│   └── index.md / manifest.json / STATE.md / log.md
├── raw/                  Vault 证据；文件同步与备份，不进入 Git
│   ├── papers/           从 Vault 投递的 PDF
│   ├── web/              网页／Markdown captures
│   ├── conversations/    明确要求保留的对话证据
│   ├── other/            其他来源和实际使用的 Zotero note 快照
│   └── assets/           来源附属图片
├── inbox/                Vault 投递区，含 attachments/
├── assets/               Wiki 自身的品牌／素材
├── .obsidian/            共用浏览设置
├── AGENTS.md / CLAUDE.md  客户端薄入口
└── README*.md            人类设置与使用指南
```

Zotero 数据库／PDF storage 及客户端凭据留在此目录之外。`_system/BOOTSTRAP.md` 是历史设计输入；当前权威次序为 SCHEMA → WORKFLOW → DECISIONS。维护时读取 STATE，通过 compact index 筛选知识页。README 负责说明怎样开始使用，不取代权威协议。

这里保存持久研究知识，不保存任务、提醒、完整聊天档案或未经筛选的文件堆。持续维护的解释和可追溯证据才是 Wiki 的价值。

## 主要操作方式

### Standard Ingest（默认）

适合普通论文、Blog、文章和官方文档。Agent 先通过 index、summary、aliases 和 targeted search 筛选候选页，优先更新已有知识。对于论文，Standard 仍会保存 research question、方法、必要公式、实验设置、主要结果和 limitations；token-aware 是减少无效读取，不是把论文压缩成 abstract。

```text
请处理 inbox 里的新资料。
```

### Deep Ingest

适合 foundational paper、准备认真引用的工作，或需要深入理解方法、证据和限制的来源。它会先建立论文地图，覆盖核心论证与证据链，再选择性保存以后值得理解、比较、引用或复用的细节。未保存的低频细节通过 locator 在 Query 时按需回到原文。Deep 会消耗更多 token，必须显式要求，但不默认逐页穷尽附录。

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
| 临时追问某个公式、图表或实验 | Query | 只打开对应原文页面和必要上下文，默认不写回 |

公式没有“必须保留 1–3 个”之类的配额。没有关键公式的 empirical paper 不应硬塞公式；高度数学化的论文则可能需要保留很多公式。Standard 和 Deep 判断的是：缺少它是否会妨碍理解核心贡献、解释结果、比较方法或判断复现要求；Exhaustive 则覆盖所有 material equations。保留时应同时解释 symbols、assumptions、作用、必要推导逻辑和原文 locator。

Deep Ingest 的“深入”指核心理解和证据链完整，不是把所有细节写入 Wiki。Agent 必须报告实际阅读范围和主动延后的附录，后续问题再按 locator 定向读取。Exhaustive Ingest 也不是复制全文：参考文献列表、通用背景和重复表述可以压缩，但所有会改变研究判断或复现结果的重要细节都应检查；长文用 section/chapter 分批处理，在 STATE 中保留可接管的进度，全部批次完成后再报告最终覆盖范围并清理 inbox 副本。

### Promote

当一次 query 或讨论产生 durable knowledge 时，可以将结论编译回 Wiki：

```text
这个答案值得保存。请保留原文 provenance，并优先更新已有页面，不要保存完整聊天。
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
- 通过 Obsidian 添加的附件默认进入 `inbox/attachments/`；Zotero 附件继续留在 Zotero。

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

来源已保存到 Vault raw 或登记为外部附件，但没有给当前 Wiki 增加值得写入的新知识。Manifest 和 log 会记录这一结果，不创建空洞页面。

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
