# A-market-ecm-lawyer-plugin

> 面向中国 A 股股权资本市场（ECM）律师的 Claude 插件 —— 把上市业务从路径选择、尽调、文书撰写、文书审核到 DOCX 格式处理的每个环节沉淀成可复用的 skill。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Status](https://img.shields.io/badge/status-early%20development-orange)

## 这是什么

一个给 A 股 ECM 业务律师用的 Claude 插件（plugin）仓库。它把律师日常业务里反复出现的工作环节——

- 上市路径比较与选择
- 尽职调查
- 法律意见书起草
- 法律意见书内核审查
- 律师工作底稿整理
- Word 文书的格式处理（letterhead、骑缝章位、甲乙方对齐等）

——拆成一组独立的 skill，每个 skill 封装一套参考资料 + 检查清单 + 脚本，给 Claude 作为上下文触发使用。

## 两个模块：项目 skill 和 QC skill

本仓库的 skill 按**使用者角色**分为两个模块：

```
┌─────────────────────────────────────────────┬──────────────────────────────┐
│ 项目 skill（6 类）                          │ QC skill（1 类）             │
│ ── 项目组律师做项目时使用                   │ ── 内核/QC 团队使用          │
├─────────────────────────────────────────────┼──────────────────────────────┤
│ ecm-setup  项目初始化 / 文件管理            │ ecm-qc  内核审查系列         │
│ ecm-design 方案设计                         │   - 见证意见内核审查         │
│ ecm-dd     尽职调查（17 章 + 2 工具）       │   - 法律意见书内核审查（规划）│
│ ecm-draft  文书起草 / 格式                  │   - 工作报告内核审查（规划）  │
│ ecm-research 法律研究 / 案例检索            │   - 披露文件内核审查（规划）  │
│ ecm-workflow 工作流编排                     │                              │
└─────────────────────────────────────────────┴──────────────────────────────┘
```

**项目 skill** 和 **QC skill** 的典型工作关系：项目组用项目 skill 推进业务、生成底稿和文书；文书交给内核团队前，内核用 QC skill 做独立审阅，输出带修订痕迹（Track Changes）和批注（Comments）的修订稿。两套 skill 语义上并列、互不替代。

## 仓库架构

```
A-market-ecm-lawyer-plugin/
├── LICENSE                     # 整仓统一 MIT 许可证
├── README.md                   # 本文件
├── DISCLAIMER.md               # 通用法律免责声明
├── CONTRIBUTING.md             # 贡献指南
├── CHANGELOG.md                # 版本更新记录
├── VERSION                     # 当前版本号
├── .claude-plugin/
│   └── plugin.json             # 插件元数据（供 /plugin install 使用）
├── .github/                    # Issue / PR 模板
├── docs/
│   ├── dependencies.md         # 外部 skill 依赖说明（docx / pdf / xlsx 等）
│   ├── installation.md         # 两种安装方式
│   ├── skill-authoring-guide.md  # 本仓库统一的 skill 编写规范
│   └── skill-roadmap.md        # skill 规划路线图
├── shared/                     # 跨 skill 共用的资料
│   ├── regulations/            # 法规条文节选
│   ├── terminology/            # 术语词汇表
│   └── templates/              # 文书模板片段
├── scripts/
│   └── package-skill.sh        # 把单个 skill 目录打包成 .skill zip 的工具
└── skills/                     # 各个 skill（每个是独立子目录）
    └── ecm-qc-shareholders-meeting-witness/
```

## skill 清单

本仓库整体规划 36 项项目 skill（6 类）+ 若干 QC skill（1 类）。详细路线图见 [docs/skill-roadmap.md](./docs/skill-roadmap.md)，建设工作计划（含 11 个可并行 batch）见 [docs/project-plan.md](./docs/project-plan.md)。

### 项目 skill 概览

| 类别 | 数量 | 覆盖工作 |
|------|-----:|---------|
| `ecm-setup` | 3 | 项目初始化、文件分类与整理 |
| `ecm-design` | 5 | 路径选择、交易结构、控制权、并购、跨境 |
| `ecm-dd` | 19 | 按编报规则第 12 号拆分的 17 章 + 数据比对 + 文件审阅 |
| `ecm-draft` | 5 | 报告拼接、格式调整、会议文件、意见书、披露文件 |
| `ecm-research` | 3 | 案例检索、法规查询、法规深度研究 |
| `ecm-workflow` | 6 | IPO 全流程、并购、跨境并购、再融资、新三板等 |

### QC skill 概览

| 类别 | 规划 | 覆盖工作 |
|------|-----:|---------|
| `ecm-qc` | 1 + 规划中 | 内核团队对见证意见、法律意见书、工作报告、披露文件的独立审阅 |

### 当前可用

| skill | 模块 | 状态 | 简介 |
|-------|------|------|------|
| [`ecm-setup:project-init`](./skills/ecm-setup-project-init/) | 项目 | ✅ v0.1.0 | 项目初始化、建文件夹、生成 skill roadmap |
| [`ecm-setup:file-classify`](./skills/ecm-setup-file-classify/) | 项目 | ✅ v0.1.0 | 批量阅读客户文件、打多标签分类 |
| [`ecm-setup:file-organize`](./skills/ecm-setup-file-organize/) | 项目 | ✅ v0.1.0 | 按标签归位 + 生成文件索引表 |
| [`ecm-dd:dd-approval`](./skills/ecm-dd-approval/) | 项目 | ✅ v0.1.0 | 本次发行 / 交易的批准和授权核查（编报规则第 1 章） |
| [`ecm-dd:dd-entity`](./skills/ecm-dd-entity/) | 项目 | ✅ v0.1.0 | 发行人主体资格核查（编报规则第 2 章） |
| [`ecm-dd:dd-establishment`](./skills/ecm-dd-establishment/) | 项目 | ✅ v0.1.0 | 发行人设立 / 出资 / 整体变更核查（编报规则第 3 章） |
| [`ecm-dd:dd-shareholders`](./skills/ecm-dd-shareholders/) | 项目 | ✅ v0.1.0 | 股东 / 实控人穿透、代持清理、三类股东核查（编报规则第 5 章） |
| [`ecm-dd:dd-history`](./skills/ecm-dd-history/) | 项目 | ✅ v0.1.0 | 股本及其演变（历史沿革）核查（编报规则第 6 章） |
| [`ecm-dd:dd-charter`](./skills/ecm-dd-charter/) | 项目 | ✅ v0.1.0 | 公司章程、三会运作、内控制度核查（编报规则第 11 章） |
| [`ecm-dd:dd-directors`](./skills/ecm-dd-directors/) | 项目 | ✅ v0.1.0 | 董监高任职资格 / 兼职 / 变化核查（编报规则第 12 章） |
| [`ecm-design:ipo-path`](./skills/ecm-design-ipo-path/) | 项目 | ✅ v0.1.0 | IPO 路径选择（A 股 / 港股 / 美股 / 红筹 / VIE / 借壳 / 被并购）三维影响分析 |
| [`ecm-design:deal-structure`](./skills/ecm-design-deal-structure/) | 项目 | ✅ v0.1.0 | 通用交易结构设计（股权 / 资产 / 增资 / 合并 / 分立） |
| [`ecm-design:control-rights`](./skills/ecm-design-control-rights/) | 项目 | ✅ v0.1.0 | 控制权获取 / 巩固 / 分配 / 退出（要约、一致行动、AB 股、反收购） |
| [`ecm-design:ma-structure`](./skills/ecm-design-ma-structure/) | 项目 | ✅ v0.1.0 | 上市公司并购（发行股份购买资产 / 重大资产重组 / 借壳 / 配套融资） |
| [`ecm-design:cross-border`](./skills/ecm-design-cross-border/) | 项目 | ✅ v0.1.0 | 跨境方案（红筹 / VIE / ODI / FDI / 境外上市备案 / 反垄断 / 国安 / 数据出境） |
| [`ecm-research:case-search`](./skills/ecm-research-case-search/) | 项目 | ✅ v0.1.0 | 多源案例检索（裁判文书 / 证监会处罚 / 交易所纪律处分 / 重组委 / 上市委审议） |
| [`ecm-research:reg-search`](./skills/ecm-research-reg-search/) | 项目 | ✅ v0.1.0 | 五级法规检索 + 时效性核验（法律 / 行政法规 / 部门规章 / 规范性文件 / 交易所规则） |
| [`ecm-research:reg-study`](./skills/ecm-research-reg-study/) | 项目 | ✅ v0.1.0 | 法规深度研究（效力层级 / 冲突解决 / 新旧衔接 / 适用性分析） |
| [`ecm-qc:shareholders-meeting-witness`](./skills/ecm-qc-shareholders-meeting-witness/) | QC | ✅ v0.1.0 | 股东（大）会法律见证意见内核审查 |

### 命名约定

所有 skill 采用 `ecm-<category>:<function>` 两级命名空间，例如：

```
ecm-setup:project-init           # 项目 skill
ecm-dd:dd-shareholders           # 项目 skill
ecm-qc:shareholders-meeting-witness  # QC skill
```

目录名使用 kebab-case（用 `-` 替代 `:`），例：`skills/ecm-qc-shareholders-meeting-witness/`。详见 [skill-authoring-guide.md](./docs/skill-authoring-guide.md#命名约定)。

## 安装使用

本仓库同时支持两种安装形态：

### 1. 作为 Claude 插件整体安装（推荐）

```bash
# 通过 Claude Code / Cowork 的 plugin 管理命令安装
/plugin install zeweihan/A-market-ecm-lawyer-plugin
```

详见 [docs/installation.md](./docs/installation.md)。

### 2. 按需下载单个 skill

每次 release 会在 GitHub Releases 页面提供每个 skill 的独立 `.skill` 文件（zip 格式）。下载后：

```
把 .skill 文件放入 Claude 的 skills 目录（或 Cowork 的对应路径）
```

### 外部依赖

部分 skill 依赖 Anthropic 官方的通用 skill（如 `docx`、`pdf`、`xlsx`）。由于这些 skill 使用专有许可，不随本仓库分发。安装方法见 [docs/dependencies.md](./docs/dependencies.md)。

## 免责声明

本仓库产出的任何内容**不构成法律意见**，不替代签字律师的专业判断。详见 [DISCLAIMER.md](./DISCLAIMER.md)。

## 贡献

欢迎提交新的 skill、改进既有 skill、修正参考资料错误。提交前请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 许可证

[MIT](./LICENSE) © 2026 zeweihan and contributors
