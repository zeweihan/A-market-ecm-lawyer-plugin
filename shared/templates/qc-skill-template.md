---
文件类型: ecm-qc 内核审查 skill 统一模板
维护者: BATCH-09 建立（ecm-qc 系列）
被哪些 skill 引用:
  - ecm-qc-opinion-letter-review
  - ecm-qc-work-report-review
  - ecm-qc-disclosure-review
  - ecm-qc-meeting-docs-review
  - （参考样板）ecm-qc-shareholders-meeting-witness（BATCH-00.5 样板；实务上已稳定运行，本模板的共性抽象自该 skill）
本版编制日期: 2026-04-24
version: 0.1.0
---

# ecm-qc 内核审查 skill 统一模板（Single Source of Truth）

本文件是 `ecm-qc-*-review` 系列 skill 的**骨架模板**。本仓库内所有"内核独立审查"类 skill（对项目组已完成的法律文书做修订与批注）必须复用本模板的结构、输出契约、工作流骨架与批注话术规范；不得在各自 SKILL.md 里另立一套。

**本模板不适用于**：
- `ecm-draft-*` 起草类 skill（那是起草人视角，输出 Markdown 初稿）
- `ecm-draft-disclosure-review`（起草人自查，不输出带修订痕迹的 Word）
- `ecm-qc-shareholders-meeting-witness`（业务是"股东大会见证"，不是对 draft 产物的内核——其独立工作流由该 skill 自身 SKILL.md 定义；本模板抽象自它，但它作为第一个 ecm-qc skill 保留自有结构）

---

## 一、SKILL.md frontmatter 规范

```yaml
---
name: ecm-qc-<function>
description: >
  一段触发关键词密集的中文描述，必须包含：
  （1）审查对象的全部同义词（法律意见书 / 意见书 / legal opinion / opinion letter / …）；
  （2）触发动词（内核 / 内核审查 / 内核复核 / 质检 / 审阅 / review / check / 挑错 / 出批注 / 出修订意见）；
  （3）与 ecm-draft-<function>（若有）的触发语区分（如 meeting-docs 的起草 vs meeting-docs-review 的内核审查）；
  （4）输出形式（带修订痕迹和批注的 Word 文档）；
  （5）即使用户只说"帮我看一下这份 xx 有没有问题"也应触发。
version: 0.1.0
license: MIT
module: ecm-qc
user_role: 内核 / QC 团队
phase:
  - 申报阶段       # 按审查对象决定：意见书 / 工作报告 / 招股书 → 申报阶段 + 反馈阶段
  - 反馈阶段
category:
  - 文书审核
depends_on:
  external_skills:
    - docx         # tracked changes / comments 核心依赖
  internal_skills:
    - ecm-draft-<对应的 draft skill>   # 用于定位项目组起草 skill 的输出契约作为参考坐标
---
```

**命名**：目录 `ecm-qc-<function>`（kebab-case），文档引用 `ecm-qc:<function>`（冒号形式）。

---

## 二、SKILL.md 正文骨架（硬性）

```markdown
# <审查对象中文名> 内核审查 Skill

## 定位与边界

本 skill **负责**：
- 对项目组提交的《<审查对象>》进行**内核独立审查**
- 按三级工作流（见 § 工作流）产出带 tracked changes + comments 的 Word 文件
- 参考坐标：[`shared/templates/<审查对象的格式规范>.md`](../../shared/templates/<xxx>.md) + [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md)（如涉及 DD → Draft 契约）

本 skill **不负责**：
- 起草 → `ecm-draft-<function>`
- 起草人自查 → 见下方"与 ecm-draft-* 的边界"
- 修改项目组的结论性意见（除非存在明显事实冲突；疑虑用【核实】批注）
- 替代签字律师的专业判断

## 免责声明

本 skill 产出的修订意见和批注**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 配置项

**修订者名称（Reviewer Name）**

所有 tracked change 和 comment 的 `w:author` 属性默认写为 **`内核`**。
用户在对话开始时可覆盖（如 `质控`、`合规`、`DC`、某律所特定审查团队名）。

**审查深度（Review Depth）**
- `form-only`：仅形式审查（1 小时内快速过一版）
- `standard`（默认）：形式 + 实质 + 交叉比对
- `deep`：含 standard + 常见错误库扫描 + 逐句措辞审

**交叉比对严格度（Cross-check Strictness）**
- `strict`：任何文字差异即标记
- `normal`（默认）：事实性差异（日期 / 届次 / 金额 / 股数 / 法规条号）必改；措辞差异仅在影响含义时标记
- `loose`：只校验数据和法规条号

---

## 工作流（五步）

### Step 1 — 定位和预读入文件

- `ls /mnt/user-data/uploads/` 找到待审文件（`.docx` 主路径；`.doc` / `.pdf` 先转换）
- `extract-text` 通读全文，形成整体理解（审查对象是什么？项目属于 IPO / 再融资 / 并购 / 其他？起草方是谁？）
- 在这一步提取后续交叉比对所需的锚点（如客户简称、项目编号、会议届次、意见书编号等）

### Step 1.5 — 拉取 / 读取参考坐标（三级降级）

内核审查的**价值来自"拿着参考坐标找偏差"**。参考坐标因 skill 而异：

| skill | 主参考坐标 | 兼容的次级参考 | Level 1 自动获取方式 |
|-------|----------|-------------|------------------|
| opinion-letter-review | `shared/templates/legal-opinion-format.md` + 同项目律师工作报告 + 17 份 DD Memo | 项目申报稿、签字律师出具的其他意见书 | 读本仓库 shared 文件 + 扫描项目目录 `04-文件输出/律师工作报告/` / `02-尽职调查/02-*` |
| work-report-review | `shared/templates/work-report-format.md` + 17 份 DD Memo | 法律意见书（形式配套） | 扫描项目目录 `04-文件输出/律师工作报告/` / `02-尽职调查/02-*` |
| disclosure-review | `shared/templates/work-report-format.md` + 法律意见书 + 17 份 DD Memo（作"权威事实源"） | 历史版本信披文件 | 扫描项目目录 `04-文件输出/律师工作报告/` / `04-文件输出/法律意见书/` / `02-尽职调查/` |
| meeting-docs-review | `shared/templates/meeting-docs-format.md` + 同项目其他会议文件（通知 / 议案 / 决议 / 记录 互为参考） | `ecm-dd-approval` / `ecm-dd-charter` 的 DD Memo（用于核对公司性质、章程约定的通知期限） | 扫描项目目录 `04-文件输出/会议文件/` 下其他文件 |

**三级降级**：

- **Level 1 — 自动拉取**：从项目目录 / `shared/` 读参考坐标；读到后作为后续交叉比对的依据
- **Level 2 — 提示用户上传**：Level 1 缺失时，向用户明确发出上传请求
- **Level 3 — 跳过交叉比对 + 显式告知**：用户确认无法提供时，在输出文档**开头插入一条整体性批注**，明确告知"本次内核审查未进行与 xx 的交叉核对"，然后只做本文件自身的形式 + 实质审查

### Step 2 — 三维度审查（同步记录 issues）

建一个 issue 清单，每条记录：**位置** / **原文摘录** / **问题类型**（形式 / 实质 / 常见错误 / 交叉比对）/ **处理方式**（tracked change 改正文 / comment 加批注 / 两者并用）/ **修改后正文 or 批注文案**。

**按优先级顺序过一遍**：

0. **交叉比对**（仅 Step 1.5 拿到参考坐标时执行）— 按本 skill 的 `references/cross-check-matrix.md`（每个 qc skill 自备一份）逐项核对
1. **形式审查** — 按本 skill 的 `references/form-requirements.md`（每个 qc skill 自备一份）逐条勾对
2. **实质审查** — 按本 skill 的 `references/substantive-checklist.md`（每个 qc skill 自备一份）逐项过
3. **常见错误扫描** — 按本 skill 的 `references/common-errors.md`（每个 qc skill 自备一份）筛查

### Step 3 — 准备修订工作目录

```bash
cd /home/claude
cp /mnt/user-data/uploads/<xxx>.docx ./input.docx
python /mnt/skills/public/docx/scripts/office/unpack.py input.docx unpacked/
```

### Step 4 — 写入修订痕迹和批注

遵循下方"输出格式契约（三条硬性要求）"。每条 issue 根据其性质决定：
- 事实 / 数据 / 法规条号 / 明确模板残留 → **tracked change** 直接改正文
- 需落实底稿 / 需核实 / 需补充模板段 / 结论性措辞优化建议 → **comment** 批注提示

### Step 5 — 打包、输出、呈递

```bash
python /mnt/skills/public/docx/scripts/office/pack.py \
  unpacked/ /mnt/user-data/outputs/reviewed.docx \
  --original input.docx
```

文件命名建议：`<审查对象简称>_<项目简称>_内核后_<YYYYMMDD>.docx`。

最后用 `present_files` 呈递，附一段简短总结：**用了几条 tracked change、几条 comment，发现的主要问题类别是什么**。不要罗列全部修改内容。

---

## 输出格式契约（三条硬性要求）

**这三条是 ecm-qc-* skill 的共同硬契约，来自用户长期积累的实务经验，不得偏离**：

### 1. 修订者 = "内核"（或用户覆盖值）

所有 `<w:ins>` / `<w:del>` 和 `<w:comment>` 的 `w:author` 属性**必须**统一写为 `内核`（不是默认的 "Claude"、"Anthropic" 或签字律师姓名）。

- 插入 `comment.py` 时必须加 `--author "内核"`
- 直接编辑 document.xml 写 `<w:ins>` `<w:del>` 时必须用 `w:author="内核"`

### 2. 修订模式开启 + 最小显示改动原则

打开 Word 修订模式，让律师能直接看到删/增痕迹。
**关键原则**：只标记真正变动的字符，不要"整段删除 + 整段重写"。

正确示例（原句"我爱你" → 新句"我恨你"）：

```xml
<w:r><w:t>我</w:t></w:r>
<w:del w:author="内核" w:date="..."><w:r><w:delText>爱</w:delText></w:r></w:del>
<w:ins w:author="内核" w:date="..."><w:r><w:t>恨</w:t></w:r></w:ins>
<w:r><w:t>你</w:t></w:r>
```

实务中高频场景：
- "2024 年" → "2025 年"：只删/增 "4" → "5"
- "第一次" → "第二次"：只删/增 "一" → "二"
- "9:30" → "14:30"：只删/增 "9" → "14"
- 删除不适用的模板话（如网络投票描述）：只删除该句，保留其他

### 3. 解释文字只进批注，不进正文

**正文里禁止出现任何解释性 / 说明性文字**。所有疑问、要求落实底稿、提醒项目组核查、法规依据、建议全部通过 `<w:comment>` 批注呈现。

✅ 批注里写："内核提示：该议案为特别决议事项，请补充'本项议案为股东（大）会特别决议事项，已经出席本次股东（大）会的股东及股东代理人所持表决权的三分之二以上同意通过'"
❌ 不要直接把这句话用 `<w:ins>` 插进正文中

### 批注分类前缀（便于项目组分诊）

| 前缀 | 用途 |
|------|------|
| **【必改】** | 硬性错误（事实错、法规错、模板残留、基础信息错） |
| **【核实】** | 需与公司 / 项目组确认再定的问题 |
| **【建议】** | 措辞优化、行文一致性、体例统一 |
| **【底稿】** | 需落实底稿或更新查验计划的事项 |

批注一般以 `内核提示：` 开头；分类前缀可替代 `内核提示：` 使用（两者二选一，不同时出现）。

---

## 边界与谨慎处理

**本 skill 不做的事情**（共用约束）：
- 不主动替代律师做法律判断——拿不准的事项一律用【核实】类批注提示
- 不修改项目组已写明的结论性意见（"合法合规" / "真实有效" 等），除非存在明显事实冲突；有疑虑的一律批注提示
- 不访问公开信息做事实核查（除非有专用脚本）——无法查证的一律用【核实】批注
- 不替项目组补整段话（声明段缺失 / 核查工作段缺失 等）——用【必改】批注提示补充

**遇到原文与本 skill 规则不匹配的"可能疏漏"**：以【必改】批注提示补充，不自行在正文里补写整段内容。

---

## 与 ecm-draft-* 的边界（强制在每个 ecm-qc-* skill 的 SKILL.md 里单独列一节）

每个 ecm-qc-* skill 必须含一节"与 ecm-draft-<对应 skill> 的边界"，至少说明 5 项区别：

| 维度 | ecm-draft-<function>（起草 / 自查） | ecm-qc-<function>（内核独立审查） |
|------|-------------------------------|-----------------------------|
| 使用者 | 项目组起草人律师 | 内核 / QC 团队 |
| 视角 | "我写的对不对 / 有没有错" | "团队交上来的有没有错、能不能过内核" |
| 输出 | Markdown 初稿 / 自查报告 | 带 tracked changes + comments 的 Word（`w:author="内核"`） |
| 修订方式 | 提建议 / 律师自己改 | 直接改原文 + 批注 |
| 后续流程 | 律师按建议修改后再送内核 | 内核意见发回起草人修改 |

⚠️ 边界说明**必须放在 SKILL.md 最前面**（定位与边界段下），便于防触发污染。

---

## references/ 目录结构（每个 qc skill 必须齐备）

每个 `ecm-qc-<function>` skill 目录下 `references/` 至少含以下 5 份（基于 qc-witness 样板抽象）：

```
skills/ecm-qc-<function>/
├── SKILL.md
├── references/
│   ├── cross-check-matrix.md          # 交叉比对矩阵（列出与参考坐标对照的核心字段）
│   ├── form-requirements.md           # 形式要件清单（按 N 项勾对）
│   ├── substantive-checklist.md       # 实质审查清单（按业务类别组织）
│   ├── common-errors.md               # 行业常见错误模式库（A/B/C... 类别编号）
│   └── comment-templates.md           # 标准批注话术模板
```

**各 reference 文档的通用写作约定**：
- 每条审查点以"典型错误 / 核对方法 / 批注模板"三要素组织
- 批注模板里的核心话术使用 `> ` 引用块（便于 Claude 在工作时直接引用）
- 引用法规时用完整名称（《xxx 办法》第 xx 条），不用简称
- 如涉及字段交叉核对，明确"以哪个文件为权威源"

---

## 与 `shared/schemas/dd-output-schema.md` 的关系

当审查对象依赖 DD Memo 的结构化字段（opinion-letter-review 的特别事项注入、work-report-review 的风险汇总表校验、disclosure-review 的"工作报告是否披露了高风险"交叉核对），qc skill 必须通过 dd-output-schema 的契约访问 Memo 字段，**不得**对 DD Memo 自定义字段结构（会破坏 DD → Draft 与 DD → QC 的两路契约一致）。

具体消费规则：

- **风险分级汇总表**：按 dd-output-schema §2.3 五列表格（编号 / 问题 / 级别 / 所涉文件 / 法规依据）；级别枚举 `高 / 中 / 低`
- **元信息块**：按 dd-output-schema §1 `项目 / 对应章节 / 编制日期 / 编制人 / skill 版本` 五字段
- **落地路径**：按 dd-output-schema §0 `02-尽职调查/02-NN-{章节名}/DD-Memo-{章节名}-{YYYYMMDD}.md`

---

## 版本

| 日期 | 变更 |
|------|------|
| 2026-04-24 | 初版（BATCH-09 建立）。锁定：SKILL.md frontmatter / 正文骨架 / 三大输出契约（w:author / 最小改动 / 解释入批注）/ 批注分类前缀 / references 目录结构 / 与 ecm-draft-* 的边界声明格式 |
