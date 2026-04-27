---
name: ecm-qc-work-report-review
description: >
  律师工作报告 / 尽职调查报告的内核独立审查 skill。当用户上传一份律师事务所出具的《律师工作报告》
  或《尽职调查报告》（IPO 律师工作报告 / 再融资律师工作报告 / 并购重组律师工作报告 / 重大资产重组
  律师工作报告 / 尽调报告 / 尽职调查报告 / work report / due diligence report），要求内核、内核审查、
  内核复核、质检、审阅、挑错、出修订意见、出批注意见、review、check，或说"这份工作报告能过内核吗" /
  "工作报告内核" / "发给监管前先审一下" / "帮我看下这份律师工作报告有没有问题"时触发本 skill。
  Skill 按三级工作流审查：(1) 与同项目 17 份 DD Memo 做**拼接完整性**+ **字段契约**的交叉比对（17 章
  是否齐全、五段式结构是否保留、风险分级汇总表列定义是否符合 dd-output-schema.md、"高"级事项是否
  全部进入全项目风险汇总表、skill_version / 编制日期 / 编制人跨 Memo 是否一致），并与同项目《法律
  意见书》做形式配套比对（律所 / 签字律师 / 日期 / 文号）；(2) 按 shared/templates/work-report-format.md
  做形式审查（封面 / 目录 / 引言 / 17 章章节号 / 字体字号 / 附件结构 / 签字页 / 页眉页脚）；(3) 按内部
  实质清单 + 常见错误库做实质审查（章节内部五段式完整、专属表是否原样保留、跨章节交叉引用断链、全
  项目风险汇总表列定义、缺章处理的占位说明、编制说明段的 DD 违约提示等）。最终输出一份带"内核"作者
  修订痕迹（Track Changes）+ 批注（Comments）的 Word 文档。与 ecm-draft-report-assembly 配对但视角
  不同：draft 是拼装，qc 是内核审查。即使用户只说"帮我看下这份工作报告" / "这份工作报告能不能过内核"，
  也应触发本 skill。
version: 0.1.0
license: MIT
module: ecm-qc
user_role: 内核 / QC 团队
phase:
  - 申报阶段
  - 反馈阶段
category:
  - 文书审核
depends_on:
  external_skills:
    - docx
  internal_skills:
    - ecm-draft-report-assembly
    - ecm-draft-opinion-letter
---

# 律师工作报告内核审查 Skill

## 定位与边界

本 skill **负责**：
- 对项目组提交的《律师工作报告》或《尽职调查报告》进行**内核独立审查**
- 按三级工作流（交叉比对 + 形式 + 实质 + 常见错误扫描）产出带 tracked changes + comments 的 Word 文件
- **参考坐标**：
  - [`shared/templates/work-report-format.md`](../../shared/templates/work-report-format.md) —— 律师工作报告排版规范（封面 / 目录 / 引言 / 17 章 / 附件 / 签字页 / 字体字号 / 编号规则 / 全项目风险汇总表 7 列定义）
  - [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) —— DD → Draft 契约（验证 17 份 Memo 的五段式骨架是否原样进入报告、风险分级汇总表合并是否合规、缺章占位说明格式）
  - 同项目的 **17 份 DD Memo**（`02-尽职调查/02-*/DD-Memo-*.md`）—— 工作报告的数据源
  - 同项目的 **《法律意见书》**（如已出）—— 工作报告与意见书形式配套

本 skill **不负责**：
- 拼接工作报告 → `ecm-draft-report-assembly`
- 各章节 DD 内容核查 → 各 `ecm-dd-*` skill
- 法律意见书审查 → `ecm-qc-opinion-letter-review`
- 信披文件审查 → `ecm-qc-disclosure-review`
- Word 最终排版（章节自动编号 / 交叉引用 / 目录生成）→ `ecm-draft-format-adjust`

本 skill 的骨架抽象自 [`shared/templates/qc-skill-template.md`](../../shared/templates/qc-skill-template.md)。

## 与 ecm-draft-report-assembly 的边界

| 维度 | ecm-draft-report-assembly（起草 / 拼接） | ecm-qc-work-report-review（内核审查） |
|------|------------------------------------|--------------------------------|
| 使用者 | 项目组起草人 | 内核 / QC 团队 |
| 视角 | "把 17 份 DD Memo 拼成工作报告" | "团队交上来的报告能不能过内核 / 发给监管" |
| 输入 | DD Memo 17 份 + 项目元信息 | 工作报告 docx + 同项目 DD Memo + 法律意见书（如有） |
| 输出 | Markdown 初稿 + 全项目风险汇总表 + 编制说明（含 DD 违约清单） | 带 tracked changes + comments 的 Word（`w:author="内核"`） |
| 修订方式 | 按 work-report-format 模板直接拼装 | 标记偏差、提建议、不越俎代庖 |
| 典型触发语 | "拼工作报告" / "把 DD 拼成报告" | "内核" / "审阅" / "挑错" / "出批注" |
| 后续流程 | 起草人复核后送内核 | 内核意见发回起草人修改 |

## 免责声明

本 skill 产出的修订意见和批注**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 资深律师执行标准

执行本 skill 时，必须同时遵循 [senior-lawyer-execution-standards.md](../../shared/templates/senior-lawyer-execution-standards.md)。本 skill 的任何输出不得突破四条底线：事实可追溯、法源可核验、风险可分级、建议可落地；无法核验时必须显式标注。

## 本 skill 的实务加固点

- **DD 溯源审查**：工作报告每章必须能定位到对应 DD Memo、底稿附件或缺章占位说明。
- **风险汇总完整性**：各 DD Memo 的高/中风险事项不得在工作报告汇总表中遗漏、降级或改写。
- **附件闭环**：重大结论引用的附件必须存在、编号一致、签章/日期可核验。
- **高风险触发器**：章节缺失无说明、事实与底稿冲突、发行障碍未进入汇总，应列必改。

## 配置项

**修订者名称（Reviewer Name）**

所有 `<w:ins>` / `<w:del>` / `<w:comment>` 的 `w:author` 默认 **`内核`**。用户可在对话开始时覆盖。

**审查深度（Review Depth）**
- `form-only`：仅形式审查（封面 / 目录 / 章节号 / 字体 / 签字页 —— 1-2 小时过一版）
- `standard`（默认）：形式 + 实质 + 交叉比对
- `deep`：含 standard + 常见错误库扫描 + 逐章内容抽样审（适合申报稿前最后一版）

**交叉比对严格度（Cross-check Strictness）**
- `strict`：DD Memo 原文与工作报告任一字段不完全一致即标记
- `normal`（默认）：字段缺漏 / 结构偏离 / "高"级事项遗漏 必改；措辞差异仅在影响含义时标记
- `loose`：只校验章节完整性、风险汇总表合并正确性、签字页一致性

---

## 工作流（五步）

### Step 1 — 定位和预读入文件

```bash
ls /mnt/user-data/uploads/
```

找到待审报告（`.docx`）。通读全文，形成整体理解：

- 报告类型：律师工作报告 / 尽职调查报告（律师工作报告对外披露 / 尽调报告仅对客户）
- 项目类型（IPO / 再融资 / 并购 / 其他）
- 律所 / 签字律师 / 律所负责人 / 出具日期 / 律所文号
- 章节数（理想 17 章；精简版可能合并章节）
- 附件清单（核查文件清单 / 律师出具人员清单 / 律所资质 / 全项目风险分级汇总表 / 工作底稿索引）

```bash
extract-text /mnt/user-data/uploads/xxx.docx > /tmp/review-input.md
```

提取 Step 1.5 所需锚点：**客户简称 / 客户全称 / 项目类型 / 律所文号**。

### Step 1.5 — 拉取参考坐标（三级降级）

内核审查本报告的核心价值是**"反向校验 DD → Report 拼接契约"**。没有 DD Memo 作参照，只能退化为形式审。

**目标获取物**（按优先级）：
1. 同项目 17 份 DD Memo（首选；最直接的拼接源）
2. 同项目《法律意见书》（次选；用于形式配套校验）
3. 同项目更早版本的工作报告（兜底；用于跨版本 Diff）

#### Level 1 — 从项目目录自动读取

```bash
ls "${PROJECT_ROOT}/02-尽职调查/" | grep "^02-[0-9]"
ls "${PROJECT_ROOT}/04-文件输出/法律意见书/"
```

读取：
- 17 份 DD Memo 的元信息块、五段式标题、"三、风险分级汇总"表（全部 `级别=高` 行）、"四、结论与建议"段
- 法律意见书封面的律所 / 律师 / 日期 / 文号（用于形式配套核对）

成功 → 进入 Step 2。

#### Level 2 — 提示用户上传

Level 1 失败时：

> 【内核提示】自动从本项目目录读取参考文件未成功。为了做拼接契约 + 形式配套的交叉比对，请上传以下文件之一：
>
> - 同项目 17 份 DD Memo（推荐压缩包）
> - 同项目《法律意见书》
>
> 上传后我会继续审查。如果暂时无法提供，请回复"跳过比对"，我将继续审查但不做交叉核对。

#### Level 3 — 跳过交叉比对，显式告知

在输出文档开头插入整体性批注：

> 【内核综合意见】本次内核审查**未进行与 DD Memo、法律意见书的交叉核对**（参考文件未能获取 / 提供）。因此：
> - 拼接契约（五段式是否保留 / 风险表合并是否合规 / "高"级事项是否齐全）**未经外部文件核对**
> - 形式配套（与意见书的律所 / 律师 / 日期 / 文号是否一致）**未经外部文件核对**
> - 本次批注仅基于工作报告文本自身的形式审查和实质审查完成
>
> 如需完整内核，请补充 DD Memo 或法律意见书后重新提交。

只做形式 + 实质 + 常见错误扫描。

---

### Step 2 — 三维度审查（同步记录 issues）

**按优先级顺序过一遍**：

0. **交叉比对审查**（Step 1.5 成功时执行）— 阅读 [`references/cross-check-matrix.md`](./references/cross-check-matrix.md)，按 14 项核心字段对照：
   - 17 章是否齐全（缺章是否有 `dd-output-schema §7` 规定的占位说明）
   - 每章内部是否保留 DD Memo 的五段式（"一、核查要点清单" / "二、审阅发现" / "三、风险分级汇总" / "四、结论与建议" / "五、参考资料"）
   - 各章的**专属表**（如股本演变时间线 / 董监高花名册 / 五独立对照评估表）是否原样保留
   - **全项目风险分级汇总表**是否聚合了 17 份 Memo 的"三、风险分级汇总"表的全部行；7 列定义（序号 / 所属章节 / 问题 / 级别 / 所涉文件 / 法规依据 / 建议措施）是否正确；序号是否跨章节连续
   - **元信息一致性**：17 份 Memo 的 `company_short_name` / `skill_version` / `lawyer_name` 跨 Memo 是否一致（不一致时工作报告"编制说明"段应有提示）
   - **与法律意见书形式配套**：律所 / 律师 / 日期 / 文号

1. **形式审查** — 阅读 [`references/form-requirements.md`](./references/form-requirements.md)，按 13 项清单逐条勾对：
   - 封面元素 / 目录 / 引言段 5 个子节 / 17 章章节号（"第一部分、第二部分……"）/ 章节内小节编号（一、（一）、1、）/ 字体字号 / 附件 5 个 / 签字页 / 页眉页脚 / 页码规则

2. **实质审查** — 阅读 [`references/substantive-checklist.md`](./references/substantive-checklist.md)，按 8 类审查项逐项过：
   - 章节完整性 / 五段式保留 / 专属表保留 / 风险汇总聚合 / 缺章占位 / 编制说明 DD 违约提示 / 附件完整性 / 跨章节交叉引用

3. **常见错误扫描** — 阅读 [`references/common-errors.md`](./references/common-errors.md)，按 A-I 类扫一遍。

**跨字段一致性检查**：
- 封面日期 / 签字页日期 / 引言段 "本报告出具日期" — 全文一致
- 客户简称：释义段定义 → 正文使用 → 签字页收件人 — 一致
- 报告期：引言段列明的期间 vs 各章 DD Memo 元信息中的期间 — 一致
- 章节编号：目录 → 一级标题 → 附件一"核查文件清单"分组 — 一致

### Step 3 — 准备修订工作目录

```bash
cd /home/claude
cp /mnt/user-data/uploads/xxx.docx ./input.docx
python /mnt/skills/public/docx/scripts/office/unpack.py input.docx unpacked/
```

### Step 4 — 写入修订痕迹和批注

遵循 `shared/templates/qc-skill-template.md` 的三条硬性要求。典型操作：

- **章节号跨度错误**（"第一部分、第三部分、第三部分"）：tracked change 改序号 + 【必改】批注说明原因（拼接时出错 / 删章未更新编号）
- **五段式缺失**（某章少了"三、风险分级汇总"表）：【必改】批注要求补齐；**不自行补表**
- **专属表被误删 / 替换为文字摘要**：【必改】批注要求恢复原表
- **全项目风险汇总表列定义不对**：tracked change 改表头 + 【必改】批注引用 `work-report-format §七`
- **与意见书律所 / 律师不一致**：tracked change + 【必改】批注

**批注调用示例**：

```bash
python /mnt/skills/public/docx/scripts/comment.py unpacked/ 0 \
  "【必改】经核对 DD-Memo-股东及实控人-20260301.md&#x201C;三、风险分级汇总&#x201D;表，该章共 3 项&#x201C;高&#x201D;级风险事项，本报告 &#x201C;附件四&#xFF1A;全项目风险分级汇总表&#x201D; 仅聚合 1 项。请按 dd-output-schema.md 要求补齐聚合。" \
  --author "内核"
```

### Step 5 — 打包、输出、呈递

```bash
python /mnt/skills/public/docx/scripts/office/pack.py \
  unpacked/ /mnt/user-data/outputs/reviewed.docx \
  --original input.docx
```

输出文件命名：`律师工作报告_<客户简称>_<项目类型>_内核后_<YYYYMMDD>.docx`。

`present_files` 呈递 + 简短总结（tracked change 数 / comment 数 / 主要问题类别）。

---

## 输出格式契约（三条硬性要求）

完全沿用 `shared/templates/qc-skill-template.md` 的 3 条：
1. **修订者 = "内核"**
2. **最小显示改动原则**
3. **解释文字只进批注**

批注分类前缀：**【必改】【核实】【建议】【底稿】**。

---

## 引用的参考文件

- [`references/cross-check-matrix.md`](./references/cross-check-matrix.md) —— 交叉比对矩阵（14 项核心字段，覆盖拼接契约 + 形式配套）
- [`references/form-requirements.md`](./references/form-requirements.md) —— 形式要件 13 项清单
- [`references/substantive-checklist.md`](./references/substantive-checklist.md) —— 实质审查 8 类要点
- [`references/common-errors.md`](./references/common-errors.md) —— 常见错误 A-I 类
- [`references/comment-templates.md`](./references/comment-templates.md) —— 标准批注话术模板

---

## 边界与谨慎处理

**本 skill 不做**：
- 不替项目组补章、补表、补段（五段式缺段、全项目风险表列缺失、专属表缺失等一律【必改】批注）
- 不修改项目组已发表的结论性意见（除非与 DD Memo 冲突；有疑虑走【核实】）
- 不自行汇总 DD Memo 重算风险表（那是起草人 / `ecm-draft-report-assembly` 的职责）
- 不访问公开信息核查法规时效 / 律所资质 —— 走【核实】批注

**遇到 DD Memo 违反 `dd-output-schema.md` 契约**（级别取值超出枚举 / 表头列不对 / 缺段）：报告应在"编制说明"段给出提示（按 `dd-output-schema §7`）。如果工作报告未提示，【必改】批注要求补充编制说明，**不自行补拼接**。

**遇到工作报告与 DD Memo 事实冲突**：不做判断，【必改】批注要求项目组回源 DD Memo 核对后统一。

---

## 变更规则

- 输出契约变动 → MAJOR（同步 `qc-skill-template.md`）
- references/ 新增审查项 / 法规更新 → MINOR
- 批注 typo / 示例补充 → PATCH
