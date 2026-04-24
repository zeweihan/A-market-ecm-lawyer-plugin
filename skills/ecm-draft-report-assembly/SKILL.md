---
name: ecm-draft-report-assembly
description: >
  律师工作报告 / 尽职调查报告 拼接 skill。当用户要求把各章节 DD Memo 拼成完整的律师工作报告、
  尽职调查报告、法律尽职调查报告、全面 DD 报告、DD Memo 整合、律师报告汇编、legal DD report、
  work report assembly，或说"把 17 章 DD 合成一份报告"/"把尽调 memo 拼起来"/"出具工作报告"
  /"起草律师工作报告"/"把各 DD 章节汇编"等场景时触发。
  典型输入：02-尽职调查/ 目录下 17 份 DD Memo（按 dd-output-schema.md 格式）、项目元信息、
  律所 / 签字律师清单、报告类型（律师工作报告 / 尽职调查报告）。
  典型输出：按 shared/templates/work-report-format.md 套版的完整 Markdown 报告初稿 + Word 套版（委托 docx
  skill）+ 全项目风险汇总表 + 未完成章节清单 + 元信息一致性校验提示。
  非触发边界：本 skill 不起草法律意见书（归 ecm-draft-opinion-letter）、不负责 DD 内容核查
  （归各 ecm-dd-* skill）、不负责 Word 最终排版细节（归 ecm-draft-format-adjust）、不做内核审查
  （归 ecm-qc-work-report-review，BATCH-09）。
  即使用户未说"拼接"一词，只要涉及"整合 DD 成报告""出 work report""汇编工作底稿"也应触发。
version: 0.1.0
license: MIT
module: ecm-draft
user_role: 项目组律师
phase:
  - 申报阶段
  - 反馈阶段
category:
  - 文书起草
depends_on:
  external_skills:
    - docx
  internal_skills:
    - ecm-dd-approval
    - ecm-dd-entity
    - ecm-dd-establishment
    - ecm-dd-history
    - ecm-dd-shareholders
    - ecm-dd-charter
    - ecm-dd-directors
    - ecm-dd-independence
    - ecm-dd-business
    - ecm-dd-related-party
    - ecm-dd-assets
    - ecm-dd-debt
    - ecm-dd-tax
    - ecm-dd-environment
    - ecm-dd-fundraising
    - ecm-dd-litigation
    - ecm-dd-compliance
    - ecm-draft-format-adjust
---

# ecm-draft-report-assembly

## 定位与边界

本 skill **负责**：
- 按 [`shared/templates/work-report-format.md`](../../shared/templates/work-report-format.md)
  的章节结构，把 17 份 DD Memo 拼接成**《律师工作报告》**或**《尽职调查报告》**完整 Markdown 初稿
- 按 [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) §0 章节顺序和
  §4 拼接层语义执行聚合
- 聚合全项目风险（遍历 17 份 Memo 的"三、风险分级汇总"表 → 合并成末尾"全项目风险分级汇总表"）
- 元信息一致性校验（`company_short_name` / `lawyer_name` / `issue_date` / `skill_version`
  跨 Memo 是否一致；不一致时在报告"编制说明"段起红旗）
- 缺章处理（某 DD skill 的 Memo 不存在时插入占位，在首页"未完成章节"清单列出）
- 起草引言段（本次发行 / 交易概况、核查范围、编制依据）

本 skill **不负责**：
- 法律意见书的起草 → `ecm-draft-opinion-letter`
- 单章 DD 内容核查 → 各 `ecm-dd-*` skill
- Word 最终排版（自动编号、页眉页脚、交叉引用、目录生成） → `ecm-draft-format-adjust`
- 信息披露文件（招股书等）的起草与自查 → `ecm-draft-disclosure-review`
- 内核独立审查 → `ecm-qc-work-report-review`（BATCH-09）

## 免责声明

本 skill 产出的律师工作报告 / 尽职调查报告**初稿**不构成最终法律意见，需经签字律师复核、律所内核审查后方可对外使用。完整免责声明见 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 前置依赖

- 上游 skill：至少有 1 份符合 `dd-output-schema.md` 契约的 DD Memo。最佳情形是 17 份全部齐备
- 项目根目录结构：见 [`shared/templates/project-folder-structure.md`](../../shared/templates/project-folder-structure.md)
- 项目元信息：`company_short_name` / 律所 / 签字律师清单 / 律所文号 / 报告日期（默认今天）
  （未提供时 skill 主动追问）
- 输出目录：`04-文件输出/律师工作报告/`（由 `ecm-setup-project-init` 预先创建）

## 核心工作流（六步）

### Step 1：收集与校验 DD Memo

1. 扫描 `02-尽职调查/02-{01..17}-*/` 目录下形如 `DD-Memo-*-{YYYYMMDD}.md` 的文件（每目录取最新日期的一份）
2. 对每份 Memo 按 [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) 做结构校验：
   - 一级标题存在且符合 §0 映射表
   - 元信息引用块（`> 项目：... | 对应章节：编报规则第 N 章 | ...`）完整
   - 五个二级标题齐全且顺序正确
   - "三、风险分级汇总" 表头列定义正确、级别取值在 `高 / 中 / 低` 范围内
3. 对校验失败的 Memo **不得静默纠正**，按 `dd-output-schema.md` §7 "违约处理"执行：
   - 跳过该 Memo 不拼接
   - 在报告"编制说明"段列明违约点

### Step 2：项目元信息一致性校验

- 把 17 份 Memo 的 `company_short_name` / `lawyer_name` / `issue_date` / `skill_version` 提取为矩阵
- 跨 Memo 比对，不一致时记录到"元信息冲突"清单
- 若存在冲突，**不自行决策**，在报告"编制说明"段起红旗提示并列出冲突详情

### Step 3：起草首尾固定件

按 [`shared/templates/work-report-format.md`](../../shared/templates/work-report-format.md) §四 生成：

- **封面**：律所名、主标题、事由、客户、文号、日期
- **目录**（Markdown 初稿阶段用 `[TOC]` 或占位，由 format-adjust 生成真目录）
- **引言**：
  - "（一）本次发行 / 交易概况" → 从项目元信息和用户输入生成
  - "（二）本所及经办律师承办概况" → 律所资质、签字律师信息
  - "（三）编制依据" → 默认清单（见 [references/editorial-basis-template.md](./references/editorial-basis-template.md)）
  - "（四）核查范围与方法" → 汇总 17 份 Memo 的"核查要点清单"覆盖面
  - "（五）关于本报告的使用" → 标准措辞（见 [references/editorial-basis-template.md](./references/editorial-basis-template.md)）
- **附件框架**：附件一（核查文件清单）、附件二（律师人员清单）、附件三（律所资质）、附件四（全项目风险汇总表）、附件五（底稿索引，可选）
- **签字盖章页**：按模板 §四.3

### Step 4：拼接正文 17 章

对每份合规的 Memo：

1. 读取 Memo 的一级标题 → 查 `dd-output-schema.md` §0 映射表 → 生成报告对应章节标题（形如 `第N部分  {章节标题}`）
2. 将 Memo 元信息引用块**丢弃**（报告首页已统一呈现）
3. 将 Memo 的五个二级标题（"一、核查要点清单" 等）**原样保留**，作为该部分的内部结构
4. 将 Memo 中 skill 专属表（如"股本演变时间线表"）**原样嵌入**，不做字段解析
5. 各部分之间**不插入过渡段**（第三稿可由律师人工增加；report-assembly 初稿保持克制）

### Step 5：聚合全项目风险分级汇总表

遍历 17 份 Memo 的"三、风险分级汇总" 表：

- 为每行新增"所属章节"列（取 Memo 对应章节名），格式 `第N部分  {章节标题}`
- 合并成一张汇总表；"序号" 跨章节连续编号（1, 2, 3, ...）
- 按 "级别" 降序排序（高 → 中 → 低）；同级别内按章节 NN 升序
- 保留五列 + 新增"所属章节"列 + 新增"建议措施"列（后者从各 Memo "四、结论与建议"段抽取简化措辞）
- 在表上方加导读段（详见 work-report-format.md §七）
- 落到报告**附件四**

### Step 6：输出 + Word 套版

- Markdown 初稿落到：`04-文件输出/律师工作报告/律师工作报告-{company_short_name}-{YYYYMMDD}.md`
- 把 Markdown 交给外部 `docx` skill 或 `ecm-draft-format-adjust` 做 Word 套版
- 输出一份**编制说明**（随报告 Markdown 同目录，文件名 `编制说明-{YYYYMMDD}.md`）列明：
  - 合规拼接的 Memo 清单（对应 17 章中的几章，哪个 skill 出的，skill_version）
  - 违约跳过的 Memo 清单及违约点
  - 元信息冲突清单
  - 缺章清单（未出 Memo 的 DD skill）
  - 报告首页已标注上述四项

## 配置项

### 报告类型（Report Type）

用户可指定报告类型为 `律师工作报告` 或 `尽职调查报告`（默认：`律师工作报告`）。两者的结构 / 字体 / 字号按 [`work-report-format.md`](../../shared/templates/work-report-format.md) §一 规定处理，差异仅在封面措辞与首页脚注。

### 报告版本（Version Tag）

用户可指定报告版本：
- `初稿` —— 本 skill 默认输出级别
- `第 N 稿` —— 供迭代时标注；本 skill 不自行递增，需用户明确指定
- `申报稿` / `定稿` / `签字稿` —— 最终稿类型，本 skill 不产出，需签字律师复核后人工定版

### 项目类型参数（Project Type）

用户指定项目类型（IPO / 再融资 / 并购 / 重组 / 新三板挂牌 / 其他），影响：
- 引言段"（一）本次发行 / 交易概况" 的模板句式
- 编制依据的法规清单（见 [references/editorial-basis-template.md](./references/editorial-basis-template.md)）

## 输出格式契约（强制）

1. **文件路径**：`04-文件输出/律师工作报告/律师工作报告-{company_short_name}-{YYYYMMDD}.md`
2. **首页结构**：按 [`work-report-format.md`](../../shared/templates/work-report-format.md) §二、§四.1
3. **正文章节**：按 [`dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) §0 NN 升序 + §4 拼接语义
4. **附件框架**：附件一至附件四为必需；附件四必须是自动生成的全项目风险汇总表
5. **编制说明**：独立 Markdown 文件，列出 Step 6 四项清单
6. **违约处理**：遵守 [`dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) §7

## 与邻近 skill 的边界

- 与 `ecm-draft-opinion-letter`：本 skill 不发法律意见；但二者共享项目元信息（同一律所、签字律师、日期），建议串行调用
- 与 `ecm-draft-format-adjust`：本 skill 输出 Markdown 初稿，format-adjust 负责 Word 套版和最终排版调整
- 与 `ecm-draft-disclosure-review`：本 skill 与 disclosure-review 共享 DD 核心结论，但后者面向招股书自查，不做拼接
- 与 `ecm-qc-work-report-review`（BATCH-09）：后者对**本 skill 的输出**做独立审查，不改变本 skill 行为

## 参考资料索引

- [references/editorial-basis-template.md](./references/editorial-basis-template.md) —— 引言段和编制依据的标准模板片段（按项目类型分）
- [references/assembly-checklist.md](./references/assembly-checklist.md) —— 拼接前 / 拼接后的自检清单
- [references/risk-aggregation-rules.md](./references/risk-aggregation-rules.md) —— 风险聚合、去重、排序的细节规则

## 常见误用 / FAQ

1. **"能不能只拼接 5 份 Memo 就先出个初稿？"**：可以。本 skill 支持部分拼接，但会在首页"未完成章节"清单显著标注缺的 12 章，提示律师该版本不得作为申报材料。
2. **"DD Memo 格式有点不规范，skill 能不能帮我自动纠正？"**：不能。按 `dd-output-schema.md` §7，本 skill 不做静默纠正，必须回到对应 ecm-dd-* skill 重新出具 Memo。强制这样做是为了避免 draft 层做"格式归一"造成上游失焦。
3. **"报告末尾的风险汇总表可以手工编辑吗？"**：强烈不建议。汇总表是对 17 份 Memo 的自动聚合，手工编辑会造成"报告说 3 个高风险、工作报告汇总表说 5 个高风险"的冲突；如确需修改，应回到对应 DD skill 调整"风险分级汇总"段重新出 Memo。
4. **"律师工作报告和尽职调查报告有什么区别？"**：见 `work-report-format.md` §一。本 skill 通过配置项切换；默认出律师工作报告。

## 变更规则

- 输出契约变动 → MAJOR（同步更新 `shared/templates/work-report-format.md` 和 `shared/schemas/dd-output-schema.md`）
- 配置项扩展 → MINOR
- 引言 / 编制依据模板调整 → PATCH
