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
    └── shareholders-meeting-witness-review/
```

## skill 清单

本仓库按六大类组织 skill，整体规划 36 项 + 若干独立 skill。详细路线图见 [docs/skill-roadmap.md](./docs/skill-roadmap.md)。

### 概览

| 类别 | 数量 | 覆盖工作 |
|------|-----:|---------|
| `ecm-setup` | 3 | 项目初始化、文件分类与整理 |
| `ecm-design` | 5 | 路径选择、交易结构、控制权、并购、跨境 |
| `ecm-dd` | 19 | 按编报规则第 12 号拆分的 17 章 + 数据比对 + 文件审阅 |
| `ecm-draft` | 5 | 报告拼接、格式调整、会议文件、意见书、披露文件 |
| `ecm-research` | 3 | 案例检索、法规查询、法规深度研究 |
| `ecm-workflow` | 6 | IPO 全流程、并购、跨境并购、再融资、新三板等 |
| 独立 skill | 1+ | 不属于上述命名空间的特例（如内核审查类） |

### 当前可用

| skill | 状态 | 简介 |
|-------|------|------|
| [`shareholders-meeting-witness-review`](./skills/shareholders-meeting-witness-review/) | ✅ v0.1.0 | 股东（大）会法律见证意见内核审查 |

### 命名约定

所有规划中的 skill 采用 `ecm-<category>:<function>` 两级命名空间，例如：

```
ecm-setup:project-init
ecm-dd:dd-shareholders
ecm-workflow:wf-ipo-full
```

目录名使用 kebab-case（用 `-` 替代 `:`），例：`skills/ecm-setup-project-init/`。详见 [skill-authoring-guide.md](./docs/skill-authoring-guide.md#命名约定)。

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
