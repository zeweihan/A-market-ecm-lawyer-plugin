---
name: ecm-qc-opinion-letter-review
description: >
  法律意见书（法律意见书 / legal opinion / opinion letter / IPO 法律意见书 / 发行律师意见书 /
  再融资 / 定增 / 配股 / 可转债 / 并购重组 / 重大资产重组 / 发行股份购买资产 / 股份回购 /
  新三板挂牌 等情形的法律意见书）的内核独立审查 skill。当用户上传一份律师事务所出具的《法律意见书》，
  要求内核、内核审查、内核复核、质检、审阅、挑错、出修订意见、出批注意见、review、check，或说
  "这份意见书能过内核吗" / "意见书内核" / "发给监管前先审一下" / "帮我看下这份法律意见书有没有问题"
  时触发本 skill。Skill 按三级工作流审查：(1) 与同项目的律师工作报告、17 份 DD Memo 做**形式配套**
  + **结论口径**的双向交叉比对（律所 / 签字律师 / 日期 / 文号是否一致；意见书结论是否超出工作报告
  所载发现；特别事项提示是否遗漏 DD "高"级风险事项）；(2) 按 shared/templates/legal-opinion-format.md
  做形式审查（五段骨架是否完整、事实-核查-意见三步法是否逐章到位、签字律师是否 ≥ 2 人 + 律所盖章 +
  律所负责人签字、含糊措辞 / 保留意见格式 / 法规引用版本等 14 项清单）；(3) 按内部实质清单 + 常见
  错误库做实质审查（结论超越工作报告、特别事项遗漏、释义不一致、章节漏发意见、法规条号过时、
  独立性意见口径等）。最终输出一份带"内核"作者修订痕迹（Track Changes）+ 批注（Comments）的 Word
  文档。与 ecm-draft-opinion-letter 配对但视角不同：draft 是起草，qc 是内核审查。即使用户只说
  "帮我看下这份法律意见书" / "这份意见书能不能过内核"，也应触发本 skill。
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
    - ecm-draft-opinion-letter
    - ecm-draft-report-assembly
---

# 法律意见书内核审查 Skill

## 定位与边界

本 skill **负责**：
- 对项目组提交的《法律意见书》（IPO / 再融资 / 并购重组 / 股份回购 / 新三板挂牌等）进行**内核独立审查**
- 按三级工作流（交叉比对 + 形式 + 实质 + 常见错误扫描）产出带 tracked changes + comments 的 Word 文件
- **参考坐标**：
  - [`shared/templates/legal-opinion-format.md`](../../shared/templates/legal-opinion-format.md) —— 意见书排版规范（5 段骨架 / 事实-核查-意见三步法 / 字体字号 / 签字页要求）
  - [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) —— DD → Draft 契约（用于校验意见书的特别事项提示是否注入了全部 `级别=高` 事项）
  - 同项目的 **《律师工作报告》**（`04-文件输出/律师工作报告/`）—— 意见书与工作报告的形式配套 + 结论不得超出工作报告认定范围

本 skill **不负责**：
- 起草意见书 → `ecm-draft-opinion-letter`
- 拼接工作报告 → `ecm-draft-report-assembly`
- 信披文件审查 → `ecm-qc-disclosure-review`
- 会议文件审查 → `ecm-qc-meeting-docs-review`
- 见证意见审查 → `ecm-qc-shareholders-meeting-witness`
- Word 最终排版（章节自动编号 / 交叉引用 / 目录）→ `ecm-draft-format-adjust`

本 skill 的骨架抽象自 [`shared/templates/qc-skill-template.md`](../../shared/templates/qc-skill-template.md)。

## 与 ecm-draft-opinion-letter 的边界

| 维度 | ecm-draft-opinion-letter（起草） | ecm-qc-opinion-letter-review（内核审查） |
|------|-------------------------------|-------------------------------------|
| 使用者 | 项目组起草人 | 内核 / QC 团队 |
| 视角 | "从 DD Memo 生成意见书初稿" | "项目组交上来的意见书能不能过内核 / 发给监管" |
| 输入 | DD Memo 17 份 + 项目元信息 | 意见书 docx + 同项目工作报告 + DD Memo |
| 输出 | Markdown 初稿 + 形式配套校验报告 | 带 tracked changes + comments 的 Word（`w:author="内核"`） |
| 修订方式 | 按 legal-opinion-format 模板直接生成 | 标记偏差、提建议、不越俎代庖 |
| 典型触发语 | "起草意见书" / "把 DD 转成意见书" | "内核" / "审阅" / "挑错" / "出批注" |
| 后续流程 | 起草人复核后送内核 | 内核意见发回起草人修改 |

## 免责声明

本 skill 产出的修订意见和批注**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 配置项

**修订者名称（Reviewer Name）**

所有 `<w:ins>` / `<w:del>` / `<w:comment>` 的 `w:author` 属性默认写为 **`内核`**。用户在对话开始时可覆盖（如 `质控`、`合规`、`DC`、某律所特定审查团队名）。

**审查深度（Review Depth）**
- `form-only`：仅形式审查（意见书骨架 / 字号 / 签字页 / 法规清单 —— 1 小时内过一版）
- `standard`（默认）：形式 + 实质 + 交叉比对
- `deep`：含 standard + 常见错误库扫描 + 逐句措辞审（适合提交申报前最后一版）

**交叉比对严格度（Cross-check Strictness）**
- `strict`：工作报告任一字段与意见书文字不完全一致即标记（适合申报稿前最后一版）
- `normal`（默认）：事实性差异（律所 / 律师 / 日期 / 文号 / 特别事项 `级别=高` 完整性 / 结论句式）必改；措辞差异仅在影响含义时标记
- `loose`：只校验数据、法规条号、特别事项完整性

---

## 工作流（五步）

### Step 1 — 定位和预读入文件

```bash
ls /mnt/user-data/uploads/
```

找到待审意见书（`.docx` 主路径；`.doc` 先用 `scripts/office/soffice.py --headless --convert-to docx` 转换）。通读全文，形成整体理解：

- 客户是哪家？项目类型（IPO / 再融资 / 并购重组 / 股份回购 / 其他）？
- 意见书类型（正式稿 / 补充稿 / 第 N 次补充）？
- 出具律所、签字律师、律所负责人、出具日期、律所文号分别是？
- 五段骨架是否完整（引言 / 释义 / 正文 / 结论性意见 / 特别事项提示）？
- 正文涉及的章节数（理想 17 章；可能是精简版）？
- 是否声称发表"保留意见" / "限定意见" / "无保留意见"？

```bash
extract-text /mnt/user-data/uploads/xxx.docx > /tmp/review-input.md
```

提取 Step 1.5 所需的锚点：**客户简称 / 客户全称 / 项目类型 / 工作报告文号（如在意见书"编制依据"段已引用）**。

### Step 1.5 — 拉取参考坐标（三级降级）

这一步是内核审查价值的核心。意见书的几乎所有潜在问题都围绕"**形式配套**"（与工作报告不一致）和"**结论口径**"（超出 DD 认定范围）。没有工作报告 / DD Memo 做参照坐标，审查会退化成纯粹的形式审，价值大打折扣。

**目标获取物**（按优先级）：

1. 同项目《律师工作报告》（首选；最全面）
2. 同项目 17 份 DD Memo（兜底；如工作报告未出）
3. 同项目更早版本的法律意见书（次选；用于跨版本 Diff）

#### Level 1 — 从项目目录自动读取

```bash
# 扫描项目目录找工作报告
ls "${PROJECT_ROOT}/04-文件输出/律师工作报告/"
# 扫描项目目录找 DD Memo
ls "${PROJECT_ROOT}/02-尽职调查/" | grep "^02-[0-9]"
```

找到后：
- 读取工作报告的封面 / 引言段 / "（二）本所及经办律师承办概况" / 全项目风险分级汇总表
- 读取 17 份 DD Memo 的元信息块 + "三、风险分级汇总" 表

成功 → 进入 Step 2 的交叉比对。

#### Level 2 — 提示用户上传

如 Level 1 因路径未约定、项目目录不存在、或文件不存在而失败：

> 【内核提示】自动从本项目目录读取参考文件未成功。为了做形式配套 + 结论口径的交叉比对，请上传以下文件之一：
>
> - 《律师工作报告》正文（首选）
> - 同项目 17 份 DD Memo 的压缩包
>
> 上传后我会继续审查。如果暂时无法提供，请回复"跳过比对"，我将继续审查但不做交叉核对。

#### Level 3 — 跳过交叉比对，显式告知

如果用户确认无法提供，在**最终输出文档的开头插入一条整体性批注**（位置：文档标题或"致：xxx"段首）：

> 【内核综合意见】本次内核审查**未进行与律师工作报告、DD Memo 的交叉核对**（因参考文件未能获取 / 提供）。因此：
>
> - 形式配套（律所 / 律师 / 日期 / 文号）**未经外部文件核对**
> - 结论口径（是否超出工作报告认定范围、特别事项是否遗漏 `级别=高` 事项）**未经外部文件核对**
> - 本次批注仅基于意见书文本自身的形式审查和实质审查完成
>
> 如需完整内核，请补充工作报告或 DD Memo 后重新提交。

然后只做形式 + 实质 + 常见错误扫描，不写依赖参考文件证据的批注（即 `cross-check-matrix.md` 里"带参考文件证据版"的话术都不用）。

---

### Step 2 — 三维度审查（同步记录 issues）

**按优先级顺序过一遍**：

0. **交叉比对审查**（Step 1.5 成功时执行）— 阅读 [`references/cross-check-matrix.md`](./references/cross-check-matrix.md)，按 11 项核心字段对照：
   - 律所 / 签字律师 / 律所负责人 / 律所文号 / 出具日期（5 项元信息，与工作报告必须一致）
   - 编制依据（法规清单） / 释义条目（与工作报告共用）
   - **特别事项提示完整性**（意见书"五、特别事项提示"段必须包含 17 份 DD Memo "三、风险分级汇总" 中全部 `级别=高` 的事项；按 `dd-output-schema.md §5`）
   - **结论口径**（意见书各章结论句 "本所认为……" 不得超出工作报告对应部分的发现；若工作报告识别了"高"级风险，意见书必须以"特别事项提示"或"保留 / 限定意见"体现）
   - **独立性章节引用**（意见书的独立性专段必须原样转写 `ecm-dd-independence` 的"五独立对照评估表"）

1. **形式审查** — 阅读 [`references/form-requirements.md`](./references/form-requirements.md)，按 12 项清单逐条勾对：
   - 标题格式 / 收件人 / 法规清单 / 声明事项段 / 五段骨架完整 / 事实-核查-意见三步法 / 签字律师 ≥ 2 + 律所盖章 + 律所负责人 / 签署日期 / 律所地址 / 释义结构 / 特别事项结构 / 保留意见格式（如有）

2. **实质审查** — 阅读 [`references/substantive-checklist.md`](./references/substantive-checklist.md)，按 8 类审查项逐项过：
   - 各章意见结构 / 结论三级措辞 / 法规引用版本 / 释义闭环 / 保留意见情形 / 项目类型对应法规清单 / 意见书与工作报告结论口径 / 补充意见书的 "承上启下"

3. **常见错误扫描** — 阅读 [`references/common-errors.md`](./references/common-errors.md)，按 A-I 类行业高频错误扫一遍：
   - A 基础信息类 / B 五段骨架类 / C 三步法结构类 / D 结论口径类 / E 特别事项类 / F 释义类 / G 签字页类 / H 法规引用类 / I 模板残留类

**跨字段一致性检查**（很关键，常见扣分点，即使无工作报告也能查）：
- 封面日期 / 签字页日期 / 文首"出具日期" — 全文一致
- 客户简称：释义段定义 → 正文使用 → 签字页收件人 — 一致
- 章节编号：引言段第（五）"核查范围" 列出的章节 = 正文实际发表意见的章节 — 覆盖一致
- 年份：跨年错误高发（2025 年意见书出现 2024 年字样）

### Step 3 — 准备修订工作目录

```bash
cd /home/claude
cp /mnt/user-data/uploads/xxx.docx ./input.docx
python /mnt/skills/public/docx/scripts/office/unpack.py input.docx unpacked/
```

`unpack.py` 会自动美化 XML、合并相邻 run、转换智能引号。解包后主要编辑 `unpacked/word/document.xml`。

### Step 4 — 写入修订痕迹和批注

**(A) 修订痕迹（tracked changes）**

严格遵循"最小显示改动"原则（详见"输出格式契约"）。典型模式：

**替换几个字**（如"2024 年" → "2025 年"）：

```xml
<w:r><w:t>截至</w:t></w:r>
<w:del w:id="1" w:author="内核" w:date="2026-04-24T00:00:00Z">
  <w:r><w:delText>2024</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="内核" w:date="2026-04-24T00:00:00Z">
  <w:r><w:t>2025</w:t></w:r>
</w:ins>
<w:r><w:t>年</w:t></w:r>
```

**删除一句**（如非 IPO 项目残留了"《首次公开发行股票注册管理办法》"表述）：把该句所在 `<w:r>` 替换成 `<w:del>` 包裹的 `<w:delText>`。删整段时还要在 `<w:pPr><w:rPr>` 里加 `<w:del/>` 标记段落标记被删。

**插入新内容**：极少用。几乎所有新增建议都应放批注里（律师决定是否采纳）。仅在缺漏必要模板文字且没有替代表达时才用 `<w:ins>` 补进正文。

**(B) 批注（comments）**

```bash
python /mnt/skills/public/docx/scripts/comment.py unpacked/ <N> \
  "批注文本（XML 实体已转义的）" \
  --author "内核"
```

XML 实体转义：`&` → `&amp;`、`'` → `&#x2019;`、`"` → `&#x201C;` / `&#x201D;`。

插入位置遵循 commentRangeStart / commentRangeEnd / commentReference 三标记结构（`<w:p>` 直接子节点，**不能**套在 `<w:r>` 里）。

**(C) 批注撰写风格** — 参考 [`references/comment-templates.md`](./references/comment-templates.md)。核心原则：
- 明确指向问题，给出修改方向或落实要求
- 必要时引用法规依据（《管理办法》第 xx 条、《执业规则》第 xx 条、《12 号规则》第 xx 条）
- 动词开头的行动项："请补充……"、"请核查……"、"请与工作报告第 X 部分统一……"

### Step 5 — 打包、输出、呈递

```bash
python /mnt/skills/public/docx/scripts/office/pack.py \
  unpacked/ /mnt/user-data/outputs/reviewed.docx \
  --original input.docx
```

输出文件命名建议：`法律意见书_<客户简称>_<项目类型>_内核后_<YYYYMMDD>.docx`。

最后用 `present_files` 呈递，附一段简短总结：**用了几条 tracked change、几条 comment，发现的主要问题类别是什么**（如 "3 条律所 / 日期 / 文号与工作报告不一致、2 条特别事项提示遗漏高风险事项、4 条章节结论句超出工作报告认定范围"），**不要**罗列全部修改内容。

---

## 输出格式契约（三条硬性要求）

（与 `shared/templates/qc-skill-template.md` 完全一致，此处简化引用）

1. **修订者 = "内核"**（所有 `<w:ins>` / `<w:del>` / `<w:comment>` 的 `w:author` 强制为 `内核`；用户可覆盖）
2. **最小显示改动原则**（只删 / 增变动的字符，不整段替换）
3. **解释文字只进批注，不进正文**（正文只做事实 / 数据 / 法规条号修改；所有解释、疑问、建议走 `<w:comment>`）

**批注分类前缀**（便于项目组分诊）：
- **【必改】** 硬性错误（事实错、法规错、特别事项遗漏、与工作报告冲突、模板残留）
- **【核实】** 需与项目组 / 签字律师确认再定的问题（如某事项风险等级是否为"高"）
- **【建议】** 措辞优化、行文一致性、体例统一
- **【底稿】** 需落实底稿或更新查验计划的事项

---

## 引用的参考文件

- [`references/cross-check-matrix.md`](./references/cross-check-matrix.md) —— 交叉比对矩阵（11 项核心字段 + 特别事项完整性校验 + 结论口径校验）【Step 1.5 成功后使用】
- [`references/form-requirements.md`](./references/form-requirements.md) —— 形式要件 12 项清单
- [`references/substantive-checklist.md`](./references/substantive-checklist.md) —— 内核实质审查 8 类要点详解
- [`references/common-errors.md`](./references/common-errors.md) —— 行业常见错误模式汇总（A-I 类）
- [`references/comment-templates.md`](./references/comment-templates.md) —— 内核批注标准话术模板

---

## 边界与谨慎处理

**本 skill 不做的事情**：
- 不主动替代律师做法律判断——拿不准的事项一律用【核实】类批注提示
- 不修改项目组已写明的结论性意见（"合法合规" / "真实有效" / "符合《xx 法》规定"），除非存在明显事实冲突或与工作报告认定范围明显不符；有疑虑的一律批注提示
- 不自行调用外部 API 核查事实 —— 法规条号是否现行有效、律所资质是否变化等一律用【核实】批注提示
- 不替项目组补整段话（如声明段缺失、核查工作段缺失）—— 用【必改】批注提示补充

**遇到原文与本 skill 规则不匹配的"可能疏漏"**（例如意见书里根本没有"五、特别事项提示"段）：以【必改】批注提示补充，不自行在正文里补写整段。

**遇到原文与工作报告冲突**（同一事实不同措辞 / 同一风险不同级别）：不做判断，以【必改】批注提示，要求项目组与工作报告编制人协调后统一。

---

## 变更规则

- 输出契约变动（w:author / 批注前缀 / 三级降级规则变化） → MAJOR（同步 `qc-skill-template.md`）
- references/ 新增审查项 / 法规条号更新 → MINOR
- 批注话术 typo / 示例补充 → PATCH
