---
文件类型: 项目目录结构模板
维护者: ecm-setup 系列
被哪些 skill 引用:
  - ecm-setup-project-init（创建目录时照此模板 mkdir）
  - ecm-setup-file-organize（按标签→目录映射归位文件）
  - 所有 ecm-dd-* skill（输出工作底稿时落到对应 DD 章节目录）
  - ecm-draft-* skill（输出文书时落到 04-文件输出/ 下）
本版编制日期: 2026-04-24
---

# ECM 项目标准目录结构（Single Source of Truth）

本文件是所有 ECM 项目的**标准文件夹结构**定义。`ecm-setup-project-init` 照此 `mkdir -p`；`ecm-setup-file-organize` 照此做标签→目录映射；下游所有 skill 输出时按对应子目录存放。

## 基础结构（所有项目类型通用）

```
ECM-{客户简称}/
├── 00-项目管理和沟通/
│   ├── （尽调清单、工作日志、往来邮件、访谈纪要）
│   └── （`internal` 标签文件落这里）
│
├── 01-方案设计/
│   └── （路径选择、交易结构、控制权安排等 design 类 skill 输出落这里）
│   └── （按项目类型会有变体子目录，见下方）
│
├── 02-尽职调查/
│   ├── 02-01-批准和授权/              ← 对应 approval 标签，ecm-dd-approval 输出
│   ├── 02-02-主体资格/                ← entity，ecm-dd-entity
│   ├── 02-03-历史沿革/                ← history / establishment，ecm-dd-history / ecm-dd-establishment
│   ├── 02-04-独立性/                  ← independence，ecm-dd-independence
│   ├── 02-05-股东及实控人/            ← shareholders，ecm-dd-shareholders
│   ├── 02-06-业务资质/                ← business，ecm-dd-business
│   ├── 02-07-关联交易与同业竞争/      ← related-party，ecm-dd-related-party
│   ├── 02-08-主要财产/                ← assets，ecm-dd-assets
│   ├── 02-09-重大债权债务/            ← debt，ecm-dd-debt
│   ├── 02-10-公司治理/                ← charter，ecm-dd-charter
│   ├── 02-11-董监高/                  ← directors，ecm-dd-directors
│   ├── 02-12-税务/                    ← tax，ecm-dd-tax
│   ├── 02-13-环保与安全生产/          ← environment，ecm-dd-environment
│   ├── 02-14-募集资金运用/            ← fundraising，ecm-dd-fundraising
│   ├── 02-15-诉讼仲裁处罚/            ← litigation，ecm-dd-litigation
│   ├── 02-16-其他合规事项/            ← compliance，ecm-dd-compliance
│   ├── 02-17-财务资料/                ← financial
│   └── 02-99-未分类文件/              ← 客户原始文件暂存处，等待 file-classify 处理
│
├── 03-法律研究/
│   └── （ecm-research-* 的输出、案例摘录、法规研究备忘录）
│
├── 04-文件输出/
│   ├── 律师工作报告/                  ← ecm-draft-report-assembly 输出
│   ├── 法律意见书/                    ← ecm-draft-opinion-letter 输出
│   ├── 会议文件/                      ← ecm-draft-meeting-docs 输出
│   └── 信息披露文件/                  ← ecm-draft-disclosure-review 审阅的招股书等
│
└── 05-底稿和附件/
    ├── 文件审阅/                      ← ecm-dd-file-review 输出摘要和抽取缓存
    ├── 数据比对/                      ← ecm-dd-data-verify 输出报告和 API 原始响应
    ├── DD-Memo-历史版本/              ← DD Memo 重跑时的旧版归档
    └── 原始文件备份/                  ← 客户原始文件备份
```

> **注意**：
> - `02-*` 是**项目目录序号**，不是《编报规则第 12 号》的章节号；DD Memo 顶部元信息中的 `chapter_no` 仍应填写《编报规则》的章节号。
> - `02-03` 同时承载"发行人的设立"（编报第 3 章）和"股本及其演变"（编报第 6 章），但两份 Memo 独立命名；`02-17-财务资料/` 是辅助目录，不对应编报第 17 章。
> - `02-99-未分类文件/` 是客户文件的默认落脚点，`ecm-setup-file-classify` 扫描这个目录来打标签。
> - 编号有间隙（如 `02-17` 后跳到 `02-99`）是有意的，留给将来新增 DD 章节。

## 标签 → 目录映射表

这张表是 `ecm-setup-file-organize` 在做归位时的唯一参考表。标签定义见 [classification-labels.md](../terminology/classification-labels.md)。

| 标签 | 目标目录 | 备注 |
|------|---------|------|
| `approval` | `02-尽职调查/02-01-批准和授权/` | |
| `entity` | `02-尽职调查/02-02-主体资格/` | |
| `establishment` | `02-尽职调查/02-03-历史沿革/` | 与 history 合并，但索引表保留各自标签 |
| `history` | `02-尽职调查/02-03-历史沿革/` | |
| `independence` | `02-尽职调查/02-04-独立性/` | |
| `shareholders` | `02-尽职调查/02-05-股东及实控人/` | |
| `business` | `02-尽职调查/02-06-业务资质/` | |
| `related-party` | `02-尽职调查/02-07-关联交易与同业竞争/` | |
| `assets` | `02-尽职调查/02-08-主要财产/` | |
| `debt` | `02-尽职调查/02-09-重大债权债务/` | |
| `charter` | `02-尽职调查/02-10-公司治理/` | |
| `directors` | `02-尽职调查/02-11-董监高/` | |
| `tax` | `02-尽职调查/02-12-税务/` | |
| `environment` | `02-尽职调查/02-13-环保与安全生产/` | |
| `fundraising` | `02-尽职调查/02-14-募集资金运用/` | |
| `litigation` | `02-尽职调查/02-15-诉讼仲裁处罚/` | |
| `compliance` | `02-尽职调查/02-16-其他合规事项/` | |
| `financial` | `02-尽职调查/02-17-财务资料/` | |
| `internal` | `00-项目管理和沟通/` | 不进 02-* 任何子目录 |

## 项目类型变体子目录

`ecm-setup-project-init` 根据项目类型额外创建的子目录：

| 项目类型 | 额外创建目录 |
|---------|-------------|
| IPO | `01-方案设计/01-01-IPO路径对比/` |
| 并购重组 | `01-方案设计/01-01-交易结构/`、`01-方案设计/01-02-控制权安排/` |
| 跨境交易（适用于任何类型） | `02-尽职调查/02-18-跨境合规/` |
| 再融资 | `01-方案设计/01-01-融资方案对比/` |
| 新三板挂牌 | `01-方案设计/01-01-挂牌路径对比/` |
| 债券发行 | `01-方案设计/01-01-发行方案/` |

## mkdir 命令（可直接被 ecm-setup-project-init 引用）

```bash
# 基础结构（所有项目通用）
mkdir -p "{ROOT}/00-项目管理和沟通"
mkdir -p "{ROOT}/01-方案设计"
mkdir -p "{ROOT}/02-尽职调查/02-01-批准和授权"
mkdir -p "{ROOT}/02-尽职调查/02-02-主体资格"
mkdir -p "{ROOT}/02-尽职调查/02-03-历史沿革"
mkdir -p "{ROOT}/02-尽职调查/02-04-独立性"
mkdir -p "{ROOT}/02-尽职调查/02-05-股东及实控人"
mkdir -p "{ROOT}/02-尽职调查/02-06-业务资质"
mkdir -p "{ROOT}/02-尽职调查/02-07-关联交易与同业竞争"
mkdir -p "{ROOT}/02-尽职调查/02-08-主要财产"
mkdir -p "{ROOT}/02-尽职调查/02-09-重大债权债务"
mkdir -p "{ROOT}/02-尽职调查/02-10-公司治理"
mkdir -p "{ROOT}/02-尽职调查/02-11-董监高"
mkdir -p "{ROOT}/02-尽职调查/02-12-税务"
mkdir -p "{ROOT}/02-尽职调查/02-13-环保与安全生产"
mkdir -p "{ROOT}/02-尽职调查/02-14-募集资金运用"
mkdir -p "{ROOT}/02-尽职调查/02-15-诉讼仲裁处罚"
mkdir -p "{ROOT}/02-尽职调查/02-16-其他合规事项"
mkdir -p "{ROOT}/02-尽职调查/02-17-财务资料"
mkdir -p "{ROOT}/02-尽职调查/02-99-未分类文件"
mkdir -p "{ROOT}/03-法律研究"
mkdir -p "{ROOT}/04-文件输出/律师工作报告"
mkdir -p "{ROOT}/04-文件输出/法律意见书"
mkdir -p "{ROOT}/04-文件输出/会议文件"
mkdir -p "{ROOT}/04-文件输出/信息披露文件"
mkdir -p "{ROOT}/05-底稿和附件"
mkdir -p "{ROOT}/05-底稿和附件/文件审阅"
mkdir -p "{ROOT}/05-底稿和附件/数据比对"
mkdir -p "{ROOT}/05-底稿和附件/DD-Memo-历史版本"
mkdir -p "{ROOT}/05-底稿和附件/原始文件备份"
```

## 变更规则

目录编号或名称的变更会波及**所有** ecm-dd-* 和 ecm-draft-* skill。变更前必须：

1. 开 issue 并标记 `folder-schema`
2. 列出受影响 skill
3. 同步更新：本文件 + `classification-labels.md`（如涉及映射）+ 各 skill SKILL.md
4. `CHANGELOG.md` 记为 **Changed**
