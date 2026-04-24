---
name: ecm-setup-project-init
description: >
  资本市场项目初始化 Skill。适用于接到任何资本市场法律服务项目（IPO、并购重组、再融资、新三板挂牌、债券发行等）后的第一步：建立标准化项目文件夹结构、输出项目类型判断与建议调用的 Skill roadmap。当用户提到以下场景时必须触发：新建项目、项目初始化、接到一个 IPO/并购项目、开始做一个资本市场项目、帮我搭一下项目结构、建立项目文件夹、新项目 kickoff、项目立项、ECM 项目启动、新增客户项目等。即使用户只说"我准备做个并购项目""帮我开个新项目""客户要 IPO 了"等，也应立即调用本 Skill。
version: 0.1.0
license: MIT
module: ecm-setup
user_role: 项目组律师
phase:
  - 启动阶段
category:
  - 项目管理
depends_on:
  internal_skills:
    - ecm-setup-file-classify
    - ecm-setup-file-organize
---

# ecm-setup-project-init

## 定位与边界

本 skill **负责**：
- 通过最多 4 轮追问确认项目关键属性（类型、境内/跨境、板块、客户简称）
- **物理创建**标准项目文件夹结构
- 根据项目类型生成本项目的 skill 调用 roadmap
- 输出标准化的"项目初始化报告"

本 skill **不负责**：
- 做路径选择的实质论证（由 `ecm-setup:ipo-path` 等 design 类 skill 做）
- 读或移动客户文件（由 `ecm-setup:file-classify` 和 `ecm-setup:file-organize` 做）
- 做尽调（由 `ecm-dd:*` 系列做）

## 免责声明

本 skill 产出的初始化报告和 roadmap 仅为项目管理辅助工具，不构成法律意见。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 前置依赖

- 本 skill 引用：
  - [shared/templates/project-folder-structure.md](../../shared/templates/project-folder-structure.md)（目录结构与变体）
  - [shared/terminology/classification-labels.md](../../shared/terminology/classification-labels.md)（标签体系，仅在报告里提及）
- 外部 skill：无硬依赖

---

## 核心任务

接到项目后**立即完成**四件事：

1. **Phase 1**：信息收集（最多 4 轮追问）
2. **Phase 2**：确定项目配置（根目录名、变体子目录、roadmap）
3. **Phase 3**：**物理创建**文件夹（`mkdir -p`）
4. **Phase 4**：输出标准化"项目初始化报告"

---

## Phase 1 — 信息收集

解析用户输入，尽量映射到以下字段：

| 字段 | 重要性 | 常见取值 |
|------|-------|---------|
| 项目类型 | 必填 | IPO / 并购重组 / 再融资 / 新三板挂牌 / 债券发行 / 其他 |
| 交易标的属性 | 高 | 境内 / 跨境；上市公司 / 非上市公司；国有 / 民营 |
| 适用板块/市场 | 高 | 主板 / 科创板 / 创业板 / 北交所 / 港股 / 美股 / 不适用 |
| 当前阶段 | 中 | 初步接触 / 尽职调查 / 申报前 / 反馈回复 / 其他 |
| 客户简称 | 中 | 用于命名项目根目录 |
| 目标路径 | 低 | 默认使用 `./ECM-{客户简称}/` |

### 追问规则

- 若项目类型不明确："请问这是什么类型的项目？（IPO / 并购重组 / 再融资 / 新三板挂牌 / 其他）"
- 若客户简称未提供："请问客户公司简称是什么？用于命名项目文件夹。"
- 若涉及并购但未说明是否跨境："该并购项目是否涉及跨境因素？"
- 若涉及 IPO 但未说明板块："贵司倾向或适用哪个上市板块？（主板 / 科创板 / 创业板 / 北交所 / 港股）"

**硬性限制**：不得追问超过 4 个问题。信息不全时在报告中标注"待补充"并继续执行。

---

## Phase 2 — 项目配置

### 项目根目录

- 默认命名：`ECM-{客户简称}`
- 用户若指定路径则优先使用用户路径
- 如目录已存在，**不覆盖**已有内容，在报告中标注"目录已存在，跳过创建"

### 基础文件夹结构

统一照 [shared/templates/project-folder-structure.md](../../shared/templates/project-folder-structure.md) 的结构创建——**不要在本 SKILL.md 内维护第二份定义**。

### 项目类型变体子目录

见 [shared/templates/project-folder-structure.md 的"项目类型变体子目录"章节](../../shared/templates/project-folder-structure.md#项目类型变体子目录)。

---

## Phase 3 — 物理创建

**必须使用 Bash 工具的 `mkdir -p` 命令实际创建文件夹**。不得只输出文字说明。

工作步骤：

1. 先用 `ls` 确认当前工作目录
2. 照 shared 模板 `mkdir -p` 一次性创建基础结构
3. 按项目类型追加变体子目录的 `mkdir -p`
4. 用 `find {ROOT} -type d` 验证创建成功，记录到报告中

---

## Phase 4 — 项目初始化报告

使用以下**固定模板**输出，不得省略任何章节。

```markdown
# 项目初始化报告

## 1. 项目概况

- **项目类型**：{IPO / 并购重组 / 再融资 / 新三板挂牌 / 债券发行 / 其他}
- **交易标的**：{境内 / 跨境} | {上市公司 / 非上市公司} | {国有 / 民营}
- **适用板块/市场**：{主板 / 科创板 / 创业板 / 北交所 / 港股 / 不适用}
- **当前阶段**：{初步接触 / 尽职调查 / 申报前 / 反馈回复 / 其他}
- **客户简称**：{简称}
- **信息完整度**：{完整 / 部分信息待补充，详见第 5 节}

## 2. 项目文件夹结构

项目根目录：`{绝对路径}`

已在该路径下创建以下文件夹（如目录已存在，标注"已存在 - 跳过创建"）：

### 基础结构（所有项目通用）
- [x] 00-项目管理和沟通
- [x] 01-方案设计
- [x] 02-尽职调查/02-01-批准和授权
- [x] 02-尽职调查/02-02-主体资格
- [x] 02-尽职调查/02-03-历史沿革
- [x] 02-尽职调查/02-04-独立性
- [x] 02-尽职调查/02-05-股东及实控人
- [x] 02-尽职调查/02-06-业务资质
- [x] 02-尽职调查/02-07-关联交易与同业竞争
- [x] 02-尽职调查/02-08-主要财产
- [x] 02-尽职调查/02-09-重大债权债务
- [x] 02-尽职调查/02-10-公司治理
- [x] 02-尽职调查/02-11-董监高
- [x] 02-尽职调查/02-12-税务
- [x] 02-尽职调查/02-13-环保与安全生产
- [x] 02-尽职调查/02-14-募集资金运用
- [x] 02-尽职调查/02-15-诉讼仲裁处罚
- [x] 02-尽职调查/02-16-其他合规事项
- [x] 02-尽职调查/02-17-财务资料
- [x] 02-尽职调查/02-99-未分类文件
- [x] 03-法律研究
- [x] 04-文件输出/律师工作报告
- [x] 04-文件输出/法律意见书
- [x] 04-文件输出/会议文件
- [x] 04-文件输出/信息披露文件
- [x] 05-底稿和附件

### 项目类型变体目录（如有）
- [x] {变体目录 1}
- [x] {变体目录 2}

## 3. 建议 Skill 调用 Roadmap

{按项目类型输出对应的 roadmap——见 references/project-roadmaps.md}

## 4. 下一步行动

**建议立即调用**：`{下一个 Skill 名称}`

原因：{1-2 句话说明原因}

目标文件夹：`{项目根目录}/02-尽职调查/02-99-未分类文件/`（通常是 file-classify 的起点）

## 5. 待补充信息（如有）

{若存在 Phase 1 中未能确认的信息，在此列出}
```

---

## 项目类型 Roadmap

详细的各项目类型 roadmap 见 [references/project-roadmaps.md](./references/project-roadmaps.md)。

简要版：

- **IPO**：`setup 三件套 → ecm-design:ipo-path → ecm-workflow:wf-ipo-dd-full → ecm-draft:report-assembly + opinion-letter + disclosure-review → ecm-draft:format-adjust`
- **并购重组**：`setup 三件套 → ecm-design:ma-structure + control-rights (+ cross-border) → ecm-dd:entity + history + business + assets + litigation + compliance → ecm-draft:report-assembly + meeting-docs + disclosure-review`
- **再融资**：`setup 三件套 → ecm-design:deal-structure → ecm-dd:approval + entity + history + compliance + fundraising → ecm-draft:opinion-letter + disclosure-review`
- **新三板**：`setup 三件套 → ecm-design:ipo-path → ecm-workflow:wf-nto-listing → ecm-draft:report-assembly`

---

## 硬性输出要求

1. **必须实际创建文件夹**（`mkdir -p`），不能只输出说明
2. **必须输出完整报告**，使用上述固定模板，不省略章节
3. **Roadmap 必须按项目类型匹配**（不要给并购项目输出 IPO 的 17 章尽调流程）
4. **下一步行动必须明确**（给出具体 skill 名称 + 原因）
5. **使用绝对路径**（报告里列出的 ROOT 必须是绝对路径）
6. **已存在目录不覆盖**（标注"已存在 - 跳过"，报告中保留 checklist 标记）
