---
name: ecm-qc-disclosure-review
description: >
  信息披露文件内核独立审查 skill。当用户上传一份招股说明书 / 招股书 / 重大资产重组报告书 /
  重组报告书 / 权益变动报告书 / 收购报告书 / 上市公告书 / 募集说明书 / 年报 / 半年报 的**法律
  相关章节**（docx / pdf），要求内核、内核审查、内核复核、质检、审阅、挑错、出修订意见、出批注
  意见、review、check，或说"这份招股书能过内核吗" / "招股书 / 重组报告书内核" / "发给监管前审
  一下" / "帮我看下这份披露文件的法律章节有没有问题" 时触发本 skill。与 ecm-draft-disclosure-review
  配对但**视角完全不同**：ecm-draft-disclosure-review 是起草人自查（输出 Markdown 自查报告），
  本 skill 是内核独立审查（输出带 tracked changes + comments 的 Word 文件，w:author 默认"内核"）。
  Skill 按三级工作流审查：(1) 与同项目《律师工作报告》+ 17 份 DD Memo + 《法律意见书》做**双向
  交叉比对**（方向一：披露文件 → 工作报告，核对披露的事实是否有工作报告 / DD 底稿支撑；方向二：
  工作报告 → 披露文件，核对工作报告识别的"高 / 中"级风险是否在披露文件中充分披露）；(2) 按信披
  文件类型的法律相关章节清单做形式审查（重大事项提示段 / 发行人基本情况 / 股权结构 / 关联交易 /
  主要财产 / 诉讼仲裁 / 募集资金运用 / 公司治理等章节的结构完整性）；(3) 按内部实质清单 + 常见
  错误库做实质审查（披露遗漏 / 披露夸大 / 避重就轻 / 措辞模糊 / 结论与事实不符 / 未定义缩写 /
  引用过时法规 / 重大事项提示未涵盖"高"级风险）。最终输出一份带"内核"作者修订痕迹 + 批注的 Word
  文档。即使用户只说"帮我看下这份招股书 / 重组报告书的法律章节" / "这份披露文件能不能过内核"，
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
    - pdf
  internal_skills:
    - ecm-draft-disclosure-review
    - ecm-draft-report-assembly
    - ecm-draft-opinion-letter
    - ecm-research-reg-search
---

# 信息披露文件内核审查 Skill

## 定位与边界

本 skill **负责**：
- 对项目组提交的信息披露文件（招股书 / 重组报告书 / 权益变动报告书 / 收购报告书 / 上市公告书 / 募集说明书 / 年报法律章节等）的**法律相关章节**进行**内核独立审查**
- 按三级工作流（双向交叉比对 + 形式 + 实质 + 常见错误扫描）产出带 tracked changes + comments 的 Word 文件
- **参考坐标**：
  - `ecm-draft-disclosure-review` 自带的 [`references/disclosure-chapter-map.md`](../ecm-draft-disclosure-review/references/disclosure-chapter-map.md) —— 法律相关章节清单（按信披文件类型划分）
  - [`shared/templates/work-report-format.md`](../../shared/templates/work-report-format.md) —— 律师工作报告形式配套参照
  - [`shared/templates/legal-opinion-format.md`](../../shared/templates/legal-opinion-format.md) —— 法律意见书结论口径参照
  - [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) —— DD → Draft 契约
  - 同项目的 **《律师工作报告》**（`04-文件输出/律师工作报告/`）+ **17 份 DD Memo**（`02-尽职调查/`）+ **《法律意见书》**（`04-文件输出/法律意见书/`）—— 权威事实源 / 口径源

本 skill **不负责**：
- 起草披露文件（那是发行人 / 保荐人 / 中介机构共同起草，律师只审核；本 skill 不参与起草）
- 起草人自查 → `ecm-draft-disclosure-review`
- 拼接工作报告 → `ecm-draft-report-assembly`
- 起草意见书 → `ecm-draft-opinion-letter`
- 工作报告内核审查 → `ecm-qc-work-report-review`
- 意见书内核审查 → `ecm-qc-opinion-letter-review`
- 非法律相关章节（管理层讨论 / 财务分析 / 募投项目可行性分析等）

本 skill 的骨架抽象自 [`shared/templates/qc-skill-template.md`](../../shared/templates/qc-skill-template.md)。

## 与 ecm-draft-disclosure-review 的边界（⚠️ 重点，触发区分）

这两个 skill 的**视角完全不同**，容易混淆。请严格按下表区分：

| 维度 | ecm-draft-disclosure-review（起草人自查） | ecm-qc-disclosure-review（内核独立审查 ← **本 skill**） |
|------|-------------------------------------|--------------------------------------|
| 使用者 | 项目组起草人律师 | 内核 / QC 团队 |
| 视角 | "我写的对不对、跟工作报告对得上吗" | "团队交上来了，能不能过内核 / 能发给监管吗" |
| 阶段 | 起草时 / 送内核前自检 | 送内核后的独立审查 |
| 输入 | 披露文件 + 工作报告 + DD Memo | 披露文件 + 工作报告 + DD Memo + 意见书（若已出） |
| 输出 | Markdown 自查报告（8 段式：自查范围 / 冲突 / 重大遗漏 / 表述差异 / 披露风格 / 版本 Diff / 自查结论 / 后续流程） | **带 tracked changes + comments 的 Word 文件**（`w:author="内核"`） |
| 修订方式 | 提建议，律师自己改 | 直接改原文 + 批注 |
| 典型触发语 | "招股书自查" / "送内核前自己先过一遍" / "预审" / "起草人自核" | "内核" / "审阅" / "挑错" / "出批注" / "能过内核吗" |
| 后续流程 | 起草人按建议修改后送内核 | 内核意见发回起草人修改 |
| 检查清单 | 两者可复用 `disclosure-chapter-map.md` / `disclosure-style-checklist.md` 的内容；但视角不同 | 两者可复用同一清单；但本 skill 额外有"批注话术"、"修订痕迹输出"要求 |

**触发区分规则**（供自动路由参考）：
- 用户说 "自查 / 自审 / 自核 / 自查自纠 / 预审 / 预检 / 内部校对 / 起草人复核 / 送内核前…" → `ecm-draft-disclosure-review`
- 用户说 "内核 / 内核审查 / 内核复核 / 挑错 / 出批注 / 出修订意见 / review / check / 这份能过内核吗…" → **本 skill**（`ecm-qc-disclosure-review`）
- 模糊场景（如"帮我看下这份招股书法律部分"）：询问用户 "是作为起草人自查，还是内核独立审查？"

## 免责声明

本 skill 产出的修订意见和批注**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 配置项

**修订者名称（Reviewer Name）**

所有 `<w:ins>` / `<w:del>` / `<w:comment>` 的 `w:author` 默认 **`内核`**。用户可在对话开始时覆盖。

**审查深度（Review Depth）**
- `form-only`：仅形式审查（章节结构 / 必备段 / 重大事项提示格式）
- `standard`（默认）：形式 + 实质 + 双向交叉比对
- `deep`：含 standard + 披露风格逐句审 + 版本 Diff

**双向比对严格度（Cross-check Strictness）**
- `strict`：披露文件任一法律事实与工作报告不一致即标记
- `normal`（默认）：事实性冲突（数据 / 日期 / 定性）必改；表述差异仅在影响含义时标记
- `loose`：只校验重大事实冲突 + "高"级风险披露完整性

**披露风格审查**
- `on`（默认）：执行"夸大表述 / 避重就轻 / 措辞模糊 / 未定义缩写 / 过时法规"扫描
- `off`：跳过风格审查（只做交叉比对）

---

## 工作流（五步）

### Step 1 — 定位和预读入文件

```bash
ls /mnt/user-data/uploads/
```

找到披露文件（`.docx` 或 `.pdf`）。PDF 走外部 `pdf` skill 提取文本 + 表格。

识别**信披文件类型**（影响法律相关章节清单）：
- 招股说明书（IPO）
- 重大资产重组报告书
- 简式 / 详式权益变动报告书
- 收购报告书
- 上市公告书
- 募集说明书（公司债）
- 年报 / 半年报的法律章节

通读法律相关章节，形成整体理解：
- 发行人 / 交易对方 / 标的资产（如涉及）
- 报告期
- 是否声称"无重大风险"？
- 重大事项提示段覆盖了哪些事项？

### Step 1.5 — 拉取参考坐标（三级降级）

本 skill 的核心价值是"双向交叉比对"：披露文件 ↔ 工作报告 / DD Memo / 意见书。

**目标获取物**：
1. 同项目《律师工作报告》（首选，最全面）+ 17 份 DD Memo（兜底）
2. 同项目《法律意见书》（用于披露口径一致性）
3. 同项目历史版本披露文件（用于 Diff）

#### Level 1 — 从项目目录自动读取

```bash
ls "${PROJECT_ROOT}/04-文件输出/律师工作报告/"
ls "${PROJECT_ROOT}/04-文件输出/法律意见书/"
ls "${PROJECT_ROOT}/02-尽职调查/" | grep "^02-[0-9]"
```

读取：
- 工作报告 "附件四：全项目风险分级汇总表"（完整 `高/中/低` 行）
- 意见书 "五、特别事项提示" 段
- 17 份 DD Memo 的"三、风险分级汇总"表 + "四、结论与建议"

#### Level 2 — 提示用户上传

Level 1 失败时：

> 【内核提示】自动从本项目目录读取参考文件未成功。为了做双向交叉比对，请上传以下文件（至少一项）：
>
> - 同项目《律师工作报告》（首选）
> - 同项目 17 份 DD Memo
> - 同项目《法律意见书》
>
> 上传后我会继续审查。如无法提供，请回复"跳过比对"。

#### Level 3 — 跳过交叉比对，显式告知

在输出文档开头插入整体性批注：

> 【内核综合意见】本次内核审查**未进行与律师工作报告、DD Memo、法律意见书的双向交叉核对**（参考文件未能获取 / 提供）。因此：
> - "披露文件 → 工作报告"方向（披露的法律事实是否有底稿支撑）**未经外部文件核对**
> - "工作报告 → 披露文件"方向（工作报告识别的"高 / 中"级风险是否充分披露）**未经外部文件核对**
> - 本次批注仅基于披露文件文本自身的形式审查和披露风格审查完成
>
> 如需完整内核，请补充工作报告 / DD Memo / 意见书后重新提交。

---

### Step 2 — 三维度审查（同步记录 issues）

**按优先级顺序过一遍**：

0. **双向交叉比对审查**（Step 1.5 成功时执行）— 阅读 [`references/cross-check-matrix.md`](./references/cross-check-matrix.md)：
   - **方向一（披露 → 工作报告）**：披露的每项法律事实（日期 / 股数 / 比例 / 金额 / 决议届次 / 事件经过 / 结论性表述）必须能在工作报告中找到依据
     - ✅ 一致
     - ⚠️ 表述差异（同一事实不同措辞）
     - ❌ 无依据（新增项；可能超出工作报告范围）
     - 🔴 冲突（数据 / 日期 / 定性直接冲突，必改）
   - **方向二（工作报告 → 披露）**：工作报告"全项目风险分级汇总表"每条事项应在披露文件有对应披露
     - ✅ 已披露
     - 🔴 "高"级风险未披露 / 披露不充分（**重大遗漏，必改**）
     - ⚠️ "中"级风险未披露（建议披露）
     - ℹ️ "低"级风险未披露（可选披露）
   - **与意见书口径**：披露文件的结论性表述与法律意见书一致（披露不得比意见书更乐观）

1. **形式审查** — 阅读 [`references/form-requirements.md`](./references/form-requirements.md)，按信披文件类型的 10 项清单逐条勾对：
   - 按类型确认法律相关章节清单是否齐全
   - "重大事项提示"段结构（是否按"高"级风险逐条列示）
   - "风险因素"段结构
   - 发行人基本情况段结构
   - 股权结构 / 公司治理段结构
   - 关联交易 / 同业竞争段结构
   - 主要财产 / 重大合同段结构
   - 诉讼仲裁 / 行政处罚段结构
   - 募集资金运用段结构
   - 编报规则所要求的其他法律披露项

2. **披露风格审查** — 阅读 [`references/disclosure-style-checklist.md`](./references/disclosure-style-checklist.md)，按 6 类筛查：
   - 夸大表述（"国内领先" / "行业第一" / "技术领先"等无客观依据的宣传语）
   - 避重就轻（风险披露段过笼统）
   - 措辞模糊（"基本符合" / "大致遵循" / "相关规定"等信披禁用语）
   - 结论与事实不符（结论性表述与详情段的具体事实矛盾）
   - 未定义缩写（首次出现未在前文或释义段定义）
   - 引用过时法规

3. **常见错误扫描** — 阅读 [`references/common-errors.md`](./references/common-errors.md)，按 A-I 类扫一遍。

**跨字段一致性检查**：
- 报告期：各章使用一致
- 发行人简称：全文统一
- 股权结构数据：股权结构章节 vs 重大事项提示 vs 关联交易章节 — 一致
- 董监高信息：董监高章节 vs 关联交易章节（董监高控制的其他企业） — 一致

### Step 3 — 准备修订工作目录

```bash
cd /home/claude
cp /mnt/user-data/uploads/xxx.docx ./input.docx
python /mnt/skills/public/docx/scripts/office/unpack.py input.docx unpacked/
```

如果上传的是 PDF：
```bash
# 走 pdf skill 提取文本并转 docx（保留格式大致结构）
# 若原稿仅 PDF，向用户回复提示："仅 PDF 源稿无法做 tracked change；请提供 Word 源稿以便出修订痕迹版"
```

如果用户只能提供 PDF，输出降级为 Markdown 格式的"内核审查备忘录"（Step 4 B 选项）。

### Step 4 — 写入修订痕迹和批注（主路径）/ 生成审查备忘录（降级）

**主路径（A）**：`.docx` 源稿 → tracked changes + comments（按 `qc-skill-template.md` 的三条硬契约）

批注调用示例：

```bash
python /mnt/skills/public/docx/scripts/comment.py unpacked/ 0 \
  "【必改】经核对同项目&#x300A;律师工作报告&#x300B;附件四&#x201C;全项目风险分级汇总表&#x201D;，&#x7B2C;3 项&#x201C;高&#x201D;级风险 &#x201C;控股股东&#x00d7;&#x00d7;曾被行政处罚&#x201D; 未在本招股书&#x201C;重大事项提示&#x201D;段披露。按信披规则属重大遗漏，请补充披露。" \
  --author "内核"
```

**降级路径（B）**：仅 PDF 源稿 → 输出 Markdown 格式的"内核审查备忘录"，按 8 段式组织（同 `ecm-draft-disclosure-review` 的自查报告骨架，但措辞更直接、作者身份为"内核"）。向用户说明："因源稿为 PDF，无法出 tracked changes；本次以内核审查备忘录形式呈递。请提供 Word 源稿以便出修订痕迹版"。

### Step 5 — 打包、输出、呈递

**主路径**：

```bash
python /mnt/skills/public/docx/scripts/office/pack.py \
  unpacked/ /mnt/user-data/outputs/reviewed.docx \
  --original input.docx
```

输出文件命名：`{信披文件类型}_{发行人简称}_法律章节_内核后_{YYYYMMDD}.docx`。

**降级路径**：输出为 `{信披文件类型}_{发行人简称}_法律章节_内核审查备忘录_{YYYYMMDD}.md`。

`present_files` 呈递 + 简短总结（tracked change 数 / comment 数 / 主要问题类别，如 "3 条冲突事项、5 条重大遗漏（"高"级风险未披露）、8 条披露风格问题"）。

---

## 输出格式契约（三条硬性要求）

完全沿用 `shared/templates/qc-skill-template.md` 的 3 条：
1. **修订者 = "内核"**（用户可覆盖）
2. **最小显示改动原则**
3. **解释文字只进批注**

**批注分类前缀**：
- **【必改】** 冲突事项 / 重大遗漏 / 法规引用错 / 含糊措辞
- **【核实】** 需与起草人 / 发行人 / 保荐人确认再定的问题
- **【建议】** 披露风格优化
- **【底稿】** 需补充底稿或更新查验计划的事项
- **【风险提示】** 该处披露可能触发监管问询 / 行政处罚风险，请特别关注

---

## 引用的参考文件

- [`references/cross-check-matrix.md`](./references/cross-check-matrix.md) —— 双向交叉比对矩阵（方向一 + 方向二 + 口径一致性）
- [`references/form-requirements.md`](./references/form-requirements.md) —— 形式要件 10 项清单（按信披文件类型的法律相关章节）
- [`references/disclosure-style-checklist.md`](./references/disclosure-style-checklist.md) —— 披露风格审查清单（6 类问题）
- [`references/common-errors.md`](./references/common-errors.md) —— 常见错误库（A-I 类）
- [`references/comment-templates.md`](./references/comment-templates.md) —— 标准批注话术模板

---

## 边界与谨慎处理

**本 skill 不做**：
- 不替发行人 / 起草人重写披露段（所有补披露建议走【必改】批注，建议具体措辞但让起草人自己采纳）
- 不修改发行人的经营性披露（业务 / 财务部分；只审法律相关章节）
- 不自行评估业务数据真实性（除非与工作报告冲突）—— 走【核实】批注
- 不做披露合规性的终局判断（例"本次重组披露是否达到 2 号准则要求" —— 这是签字律师与保荐人的综合判断，内核只能做识别 + 提示）

**遇到披露文件与工作报告冲突**：事实类冲突走【必改】；表述差异走【建议】（示例建议措辞）；发行人特别要求的措辞走【核实】。

**遇到"高"级风险未披露**：走【必改】；批注列出工作报告 / DD Memo 的原文依据。

**遇到披露文件引用法规过时**：tracked change 改版本 + 【必改】批注（可参考 `ecm-research-reg-search` 核验最新版本）。

---

## 常见误用 / FAQ

1. **"PDF 源稿能出修订痕迹吗？"**：原则上不能。建议回复发行人 / 保荐人索要 Word 源稿。如果时间紧迫，可走降级路径输出 Markdown 内核审查备忘录。

2. **"披露文件是合并披露稿（法律 + 财务 + 业务章节一份文件），怎么处理？"**：只审法律相关章节（按 `disclosure-chapter-map.md`）；非法律章节（管理层讨论 / 业务与技术 / 财务会计信息中的财务分析）走【核实】批注："该段涉及非法律专业判断，请相关部门复核"。

3. **"同项目工作报告还没出，能用本 skill 吗？"**：可以退化到"仅形式审查 + 披露风格审查"，跳过双向交叉比对。但这会大幅降低内核含金量，建议等工作报告出具后重跑。

4. **"重大事项提示是发行人写的还是律师写的？"**：发行人写，律师审核。内核审查发现"高"级风险未披露时，批注要求发行人和起草律师协商补充，不自行补写。

5. **"和 `ecm-draft-disclosure-review` 都能读同样的 checklist，有必要分成两个 skill 吗？"**：必要。两者**视角不同 / 输出不同 / 后续流程不同**，合成一个会把触发语搞乱（起草人说"自查"时不希望出 Word 修订稿；内核说"审阅"时不希望只得到 Markdown 自查报告）。checklist 共享但 SKILL.md 分开。

---

## 变更规则

- 输出契约变动 → MAJOR
- references/ 新增审查项 / 信披规则更新 → MINOR
- 批注 typo / 示例补充 → PATCH
