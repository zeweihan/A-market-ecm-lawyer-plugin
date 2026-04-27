# skill 编写规范 / Skill Authoring Guide

本仓库对所有 skill 有统一的目录结构、frontmatter 字段和文档规范。在动手新建 skill 之前请先读完本文。

## 两个模块：项目 skill 和 QC skill

本仓库的 skill 按**使用者角色**分成两个模块，写新 skill 前先确定归属：

| 模块 | 使用者 | 类别 | 设计要点 |
|------|--------|------|---------|
| **项目 skill** | 项目组律师（经办律师、签字律师、团队成员） | `setup` / `design` / `dd` / `draft` / `research` / `workflow` | 主动推进业务、产生底稿/文书；输入可以是客户材料或既有 skill 输出；输出可以是分析备忘、checklist 结论、文书初稿等 |
| **QC skill** | 内核/QC 团队（独立于项目组的审核团队） | `qc` | 输入恒为"项目组已交付的文书"；输出恒为"带 Track Changes + Comments 的修订稿"；修订痕迹的 `w:author` 恒为"内核"或 QC 自定义名；语气是独立审阅、不替代签字律师判断 |

两者的关键区别：

- **触发链条不同**：项目 skill 被"做什么事"触发（写报告、做尽调），QC skill 被"审什么文书"触发（看一下这份意见书对不对）。
- **输入假设不同**：项目 skill 可以接受不完整的客户资料，自行判断缺口；QC skill 假设收到的文书"已经有一稿了"，重点是挑错。
- **输出格式不同**：项目 skill 的输出形式多样；QC skill 的输出恒为 docx + tracked changes + comments。
- **不要混用**：一个 skill 只能归属一个模块，避免"既起草又审查"这种角色混淆。如果业务场景是"起草同时自查"，拆成两个 skill：`ecm-draft:xxx` 起草，`ecm-qc:xxx-review` 审查。

## 命名约定

所有 skill 采用**两级命名空间**：

```
ecm-<category>:<function>
```

其中 `<category>` 取自七大类：`setup` / `design` / `dd` / `draft` / `research` / `workflow`（项目 skill）/ `qc`（QC skill）。

### 三种书写形式

| 场景 | 格式 | 例子 |
|------|------|------|
| 目录名 | kebab-case，`-` 替代 `:` | `skills/ecm-setup-project-init/` |
| SKILL.md frontmatter 的 `name` 字段 | 同目录名 | `name: ecm-setup-project-init` |
| 文档/路线图/README 表格（人类可读） | 保留冒号 | `ecm-setup:project-init` |

### 为什么同时用两种写法

文件系统和 Git 对冒号兼容性不佳（Windows 路径里是保留字符），所以磁盘上统一用 `-`。但冒号形式更贴近 Claude Code 官方 skill 命名（如 `productivity:task-management`），对人类更可读，所以文档里保留。

### 新建 category 的门槛

目前 6 大类已经覆盖大部分业务场景。新增类别（如 `ecm-review` 内核审查类）需要在 PR 里说明：

- 新类别和既有 6 大类的关系/边界
- 预计该类别下会有多少 skill
- 为何不能归入既有类别

## 标准目录结构

```
skills/<skill-name>/
├── SKILL.md                   # 必需：主文件（YAML frontmatter + 正文）
├── README.md                  # 可选：面向开发者的说明（使用场景、样例）
├── references/                # 可选：skill 自用的参考资料（checklist、模板、术语）
│   └── *.md
├── scripts/                   # 可选：skill 自用的脚本（Python、shell）
│   └── *.py
└── assets/                    # 可选：图片、字体等静态资源
    └── *
```

**重要**：skill 目录下**不要**放单独的 `LICENSE`。全仓库统一用顶层 `LICENSE`（MIT）。在 `SKILL.md` 的 frontmatter 里通过 `license: MIT` 字段声明即可。

## SKILL.md 的 YAML frontmatter 规范

```yaml
---
name: ecm-<category>-<function>           # 与目录名一致；例：ecm-setup-project-init
description: >                            # 用来触发 skill 的描述，关键词要密集
  一段中文描述……包含所有可能的触发关键词、同义词、简称、英文对照。
  当用户提到 xxx、yyy、zzz 时触发。
version: 0.1.0                            # SemVer
license: MIT                              # 全仓统一 MIT，见顶层 LICENSE
module: ecm-setup                         # 必填；取值：ecm-{setup,design,dd,draft,research,workflow,qc}
user_role: 项目组律师                     # 必填；典型取值："项目组律师" / "内核 / QC 团队"
phase:                                    # 业务阶段（多选）
  - 研究阶段
  - 启动阶段
  - 尽调阶段
  - 申报阶段
  - 反馈阶段
  - 发行阶段
  - 持续督导阶段
category:                                 # 功能类别（多选，自然语言描述）
  - 方案设计
  - 合规核查
  - 文书起草
  - 文书审核
  - 格式处理
  - 法律研究
  - 案例检索
depends_on:                               # 依赖声明（可选）
  external_skills:                        # 外部 skill 依赖
    - docx
  internal_skills:                        # 本仓库其他 skill
    - ecm-design-ipo-path
---
```

### description 字段的写法要点

Claude 是靠 description 字段判断是否触发该 skill 的。好的 description：

- **触发关键词密集**：列出所有可能的中文说法、同义词、缩写、英文对应词
- **给出明确的触发场景**："当用户上传 xxx 并要求 yyy 时触发"
- **覆盖非明确的触发情形**："即使用户未明确使用 'xxx' 一词，只要涉及 zzz 也应触发"
- **避免与其他 skill 重叠**：如果两个 skill 的 description 触发范围有冲突，会导致误触发

可以直接参照 `skills/ecm-qc-shareholders-meeting-witness/SKILL.md` 的 frontmatter 作为样板。

## SKILL.md 正文的标准章节

建议按以下顺序组织，但不是硬性要求：

1. **用途概述** / 标题说明该 skill 做什么
2. **配置项**（可选）：比如"作者名"这种运行时可由用户覆盖的变量
3. **免责声明**（引用顶层 DISCLAIMER.md，不要复制全文）
4. **资深律师执行标准**：引用 `shared/templates/senior-lawyer-execution-standards.md`
5. **本 skill 的实务加固点**：写本 skill 独有的必查事项、高风险触发器、边界和补正路径
6. **输出格式契约**（如果有强格式要求）
7. **工作流**：分步骤说明 Claude 该怎么做
8. **参考资料索引**：列出 `references/` 下各文件的用途
9. **脚本索引**：列出 `scripts/` 下各脚本的用途
10. **常见误用 / FAQ**（可选）

### 资深律师执行标准段（强制）

所有 skill 的 `SKILL.md` 必须在免责声明后加入以下段落，确保任何业务输出都不低于资深 A 股资本市场律师的证据、法源、风险判断和交付底线：

```markdown
## 资深律师执行标准

执行本 skill 时，必须同时遵循 [senior-lawyer-execution-standards.md](../../shared/templates/senior-lawyer-execution-standards.md)。本 skill 的任何输出不得突破四条底线：事实可追溯、法源可核验、风险可分级、建议可落地；无法核验时必须显式标注。
```

### 本 skill 的实务加固点（强制）

所有 skill 还必须在通用执行标准后写一个**本 skill 独有**的小节，不能只复制通用标准。该小节应控制在 3-5 条，每条必须能体现本 skill 的具体业务风险，例如：

```markdown
## 本 skill 的实务加固点

- **必查事实**：列出本 skill 独有的关键事实和证据链。
- **高风险触发器**：列出一旦出现即需标红或升级的事项。
- **边界/分流**：说明哪些事项应转给相邻 skill 或专项机构。
- **补正路径**：说明常见瑕疵如何补正，不能补正时如何定性。
```

如果某个 skill 只能写出通用表述，说明该 skill 的边界没有定义清楚，应先重写定位与边界。

## 跨 skill 数据约定

当一个 skill 的输出会作为另一个 skill 的输入时，使用 **JSON schema**（放在 `shared/schemas/` 目录，后续建立）约定字段。当前阶段优先用以下共识字段名：

| 字段名 | 类型 | 含义 |
|--------|------|------|
| `company_short_name` | string | 公司简称（证券简称） |
| `stock_code` | string | 证券代码（6 位数字，新三板 8 位） |
| `listing_board` | enum | 主板 / 创业板 / 科创板 / 北交所 / 新三板 / 港股 / 美股 |
| `meeting_session` | string | 如 "2025 年第一次临时股东大会" |
| `record_date` | string (YYYY-MM-DD) | 股权登记日 |

随着 skill 增多，此表会扩展。

## 共享资源使用规则

- 法规条文节选 → `shared/regulations/`（例：`公司法-2024.md`、`上市公司股东会规则-2025.md`）
- 术语词汇表 → `shared/terminology/`（例：`a-share-listing-terms.md`）
- 文书模板片段 → `shared/templates/`（例：`law-firm-letterhead.md`）

skill 需要引用时，用相对路径：`../../shared/regulations/公司法-2024.md`。

**不要**在 skill 内部重复共享资源的内容；共享资源更新后所有 skill 自动拿到新版本。

## DD skill 专用模板

所有业务性 `ecm-dd-*` skill（不含工具类 `dd-data-verify` / `dd-file-review`）必须套用
[shared/templates/dd-skill-template.md](../shared/templates/dd-skill-template.md) 的统一结构：

- 统一的 frontmatter 字段（module / user_role / phase / category / depends_on）
- 统一的正文章节（定位与边界 / 前置依赖 / 核心工作流 / 统一风险分级口径 / 输出格式契约 / 参考资料索引 / 变更规则）
- 统一的 DD Memo 输出契约（"核查要点 + 审阅发现 + 风险分级汇总 + 结论与建议 + 参考资料"五段式）
- 强制的输出落地路径（`02-尽职调查/02-NN-xxx/DD-Memo-xxx-{YYYYMMDD}.md`）

新建 DD skill 时严禁另起炉灶；确需扩展输出结构（如增加"时间线表""花名册"等专属字段）时，
在该 skill 内部"输出格式契约"章节追加"额外要求"段落，但五段式骨架不得破坏。

## 版本号规则（SemVer）

- **MAJOR**：输出契约破坏性变更（例如改变 JSON 输出字段结构、改变工作流的硬性要求）
- **MINOR**：新增能力但不破坏既有用法（例如新增可选输入、新增一种输出模式）
- **PATCH**：bug 修复、描述文字调整、法规文本更新

skill 的版本号独立于仓库整体版本号（顶层 `VERSION` 文件）。

## 打包成 .skill 文件

本仓库提供 `scripts/package-skill.sh`：

```bash
./scripts/package-skill.sh skills/ecm-qc-shareholders-meeting-witness
# 产出：dist/ecm-qc-shareholders-meeting-witness.skill
```

打包产物会在每次 release 时附到 GitHub Releases 页面。

## 本地测试 checklist

开发新 skill 或修改既有 skill 时建议跑一遍：

- [ ] SKILL.md 的 frontmatter YAML 可解析（无语法错误）
- [ ] description 能触发预期场景（手动测 3-5 个 prompt）
- [ ] description 不会误触发其他场景（反向测 3-5 个 prompt）
- [ ] 依赖的外部 skill 都已列在 frontmatter 的 `depends_on` 和 `docs/dependencies.md`
- [ ] `references/` 下的资料在 SKILL.md 正文里都被引用
- [ ] `scripts/` 下的脚本可以独立运行（或在 SKILL.md 里说明依赖）
- [ ] 打包脚本能正确生成 `.skill` 文件，解压后结构完整
