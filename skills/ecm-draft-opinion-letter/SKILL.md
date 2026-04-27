---
name: ecm-draft-opinion-letter
description: >
  法律意见书起草 skill。当用户要求起草 / 出具 / 写 / 撰写 A 股首次公开发行法律意见书、
  IPO 法律意见书、发行律师意见书、再融资法律意见书、定增法律意见书、配股法律意见书、
  可转债法律意见书、并购重组法律意见书、重大资产重组法律意见书、发行股份购买资产法律意见书、
  股份回购法律意见书、新三板挂牌法律意见书、legal opinion、opinion letter，或说"把 DD 结论
  转成意见书""出一份意见书初稿""把工作报告转意见书""按 dd 结论写法律意见书"时触发。
  典型输入：已完成的 DD Memo 17 份（或部分）、律师工作报告（若已生成）、项目元信息
  （律所 / 签字律师 / 日期 / 项目类型）、释义表（可选，若无则自动生成）。
  典型输出：按 shared/templates/legal-opinion-format.md 套版的完整法律意见书 Markdown 初稿、
  特别事项提示段（从风险汇总表"高"级事项自动注入）、释义表、与工作报告形式配套校验报告。
  非触发边界：本 skill 不拼接工作报告（归 ecm-draft-report-assembly）、不核查 DD 内容
  （归各 ecm-dd-* skill）、不审阅披露文件（归 ecm-draft-disclosure-review）、不做内核审查
  （归 ecm-qc-opinion-letter-review）。
  即使用户未明确说"意见书"，只要涉及"基于 DD 发表意见""IPO 法律意见""撰写对 xx 事项的法律意见"
  也应触发。
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
    - ecm-draft-report-assembly
    - ecm-draft-format-adjust
---

# ecm-draft-opinion-letter

## 定位与边界

本 skill **负责**：
- 按 [`shared/templates/legal-opinion-format.md`](../../shared/templates/legal-opinion-format.md)
  的 5 段骨架起草**法律意见书**完整 Markdown 初稿
- 从 [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) §5
  定义的消费规则，从 17 份 DD Memo 的"三、风险分级汇总"表提取 `级别=高` 事项，注入
  意见书的"特别事项提示"段
- 从 `ecm-dd-independence` 的"五独立对照评估表"原样转写成《关于发行人独立性的意见》专段
- 按项目类型（IPO / 再融资 / 并购 / 重组 / 新三板挂牌）选用标准法规清单 + 结论句式
- 与同项目的**律师工作报告**形式配套（律所、签字律师、日期、文号、编制依据一致），由本 skill
  主动做跨文书一致性校验
- 每章节意见按"**事实陈述 → 核查工作 → 法律意见**"三步法组织（见 legal-opinion-format.md §3.3）

本 skill **不负责**：
- 拼接律师工作报告 → `ecm-draft-report-assembly`
- 单章 DD 内容核查 → 各 `ecm-dd-*` skill
- 招股书 / 重组报告书的披露自查 → `ecm-draft-disclosure-review`
- Word 套版和最终排版 → `ecm-draft-format-adjust`
- 内核独立审查 → `ecm-qc-opinion-letter-review`

## 免责声明

本 skill 产出的法律意见书**初稿**不构成最终法律意见，需经签字律师复核、律所内核审查后方可对外使用。完整免责声明见 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 资深律师执行标准

执行本 skill 时，必须同时遵循 [senior-lawyer-execution-standards.md](../../shared/templates/senior-lawyer-execution-standards.md)。本 skill 的任何输出不得突破四条底线：事实可追溯、法源可核验、风险可分级、建议可落地；无法核验时必须显式标注。

## 本 skill 的实务加固点

- **意见来源限定**：正式法律意见只能来自已核验 DD Memo、工作报告、法规检索和用户确认事实，不得新增未核验事实。
- **肯定结论门槛**：材料缺失、重大风险未关闭、法规未核验时，不得写“符合条件”“合法有效”等无保留结论。
- **特别事项提示**：高风险、重大不确定、需依赖第三方专项意见事项必须进入特别提示或保留说明。
- **口径一致**：意见书、工作报告、信披文件、会议文件中的项目名称、主体、法规依据和结论必须一致。

## 前置依赖

- 至少有 1 份符合 `dd-output-schema.md` 契约的 DD Memo
- 若同项目已生成律师工作报告（来自 `ecm-draft-report-assembly`），优先读取工作报告的元信息、释义、编制依据，保证形式配套
- 项目元信息：律所 / 签字律师 / 律所文号 / 出具日期 / 项目类型 / 客户全称与简称

## 核心工作流（六步）

### Step 1：元信息与形式配套校验

- 收集项目元信息（若同目录已有律师工作报告，优先读取其封面和"（二）本所及经办律师承办概况" 段）
- **强制校验**：律所名、签字律师、日期、律所文号规则是否与工作报告一致
- 不一致时**不得自行决定**，暂停主流程并主动追问用户："本 skill 检测到意见书的 {字段} 与律师工作报告不一致，请确认以哪个为准"
- 若工作报告不存在，记录为"单独出意见书，不做配套校验"，后续交付物中明示

### Step 2：扫描与校验 DD Memo

- 读取 `02-尽职调查/02-{01..17}-*/DD-Memo-*.md`
- 按 [`dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) 做结构校验
- 对违约的 Memo 按 §7 处理：
  - 不提取高风险事项（跳过该 Memo 的风险注入）
  - 不起草该章意见书正文（该章用占位说明"本所尚未完成本章核查，本次意见书中相关部分暂缺；详见工作报告编制说明"）

### Step 3：起草"一、引言" + "二、释义"

按 [`legal-opinion-format.md`](../../shared/templates/legal-opinion-format.md) §3.1-3.2：

- **引言段的 5 个小节**：律所简况 / 经办律师简况 / 身份授权 / 发行交易概况 / 核查范围
- **释义段**：
  - 若同项目律师工作报告已生成 → 从工作报告抽取释义表作为基础，opinion-letter 只扫描正文补充新的专有名词
  - 若无 → 从 [references/default-definitions.md](./references/default-definitions.md) 用默认 15 条基础释义起步 + 扫描 DD Memo 抽取补充
  - 释义条目数一般 15-30 条，少于 15 或多于 35 会触发告警

### Step 4：起草"三、正文"17 章意见

对每份合规的 DD Memo，在意见书正文生成对应小节（顺序按 dd-output-schema.md §0 NN 升序），每小节遵循"事实陈述 → 核查工作 → 法律意见"三步法：

1. **1、事实陈述**：从 Memo "四、结论与建议" → "总体结论" 段抽取 + 从 skill 专属表（如股本演变时间线）抽取
2. **2、核查工作**：从 Memo "一、核查要点清单" 抽取，简化为"本所律师核查了……"句式
3. **3、法律意见**：
   - 按句式模板（见 [references/opinion-statements-template.md](./references/opinion-statements-template.md)）组织
   - 结论措辞分 3 级：
     - **肯定（绿）**：`本所认为，{事项} 合法有效，符合 {《xx 法》第 yy 条} 的规定`
     - **有条件肯定（黄）**：`除 {瑕疵说明} 外，本所认为 {事项} 合法有效`，或 `{事项} 履行了 {程序}，但 {具体瑕疵}，建议 {整改措施}`
     - **保留 / 限定（红）**：`本所对 {事项} 保留意见 / 暂无法发表肯定性意见，理由是 {具体原因}`
   - 结论级别依据 Memo 的"风险分级汇总"：该章若无"高"级 → 肯定；有"中"级 → 有条件肯定；有"高"级 → 必须保留或限定
   - **不得**超出 Memo 核查范围自行发表意见；Memo 未做核查的事项，在此小节省略或标注"依赖 xx 方出具专业意见"

### Step 5：起草"四、结论性意见" + "五、特别事项提示"

- **结论性意见**：按 `legal-opinion-format.md` §3.4 固定措辞模板填充项目类型对应的法规清单
- **特别事项提示**：按 [`dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) §5 规则自动注入：
  - 遍历 17 份 Memo 的"三、风险分级汇总" 表
  - 提取 `级别=高` 的全部行
  - 去重（按"问题"列全文匹配，跨章节完全相同时合并）
  - 按章节 NN 升序排列
  - 每条按固定句式组织：
    ```
    特别事项 {N}：{章节名}
    经核查，发行人 {问题简述}。
    法规依据：{法规条文}。
    本所意见：{是否构成发行障碍；是否需整改 / 补充披露}。
    ```
  - "本所意见"由 opinion-letter 根据问题类型选择模板句式（见 [references/opinion-statements-template.md](./references/opinion-statements-template.md)）

### Step 6：起草签字页 + 输出

- 签字页按 `legal-opinion-format.md` §八：律所盖章、律所负责人签字、至少 2 名经办律师签字、日期与封面一致
- Markdown 初稿落到：`04-文件输出/法律意见书/法律意见书-{company_short_name}-{YYYYMMDD}.md`
- 生成**形式配套校验报告**（同目录，`形式配套校验-{YYYYMMDD}.md`），列明：
  - 意见书与工作报告的元信息一致性
  - 意见书发表意见的章节 vs 工作报告覆盖的章节（应一致）
  - 意见书"特别事项提示" vs 工作报告"全项目风险汇总表"`级别=高` 事项（应完全一致）
  - 意见书内所有缩写是否都在"二、释义"段定义

## 配置项

### 意见书类型（Opinion Type）

用户可指定意见书类型（影响封面标题、法规清单、结论措辞）：
- `首次公开发行法律意见书`（默认）
- `补充法律意见书（第 N 次）`
- `定增 / 配股 / 可转债法律意见书`
- `并购重组法律意见书`
- `重大资产重组法律意见书`
- `发行股份购买资产法律意见书`
- `股份回购法律意见书`
- `新三板挂牌法律意见书`

### 形式配套策略（Consistency Strategy）

指定与律师工作报告的形式配套方式：
- `strict`（默认）：强制与 report-assembly 的输出完全一致，不一致时阻塞流程
- `advisory`：不一致时生成警告但继续流程（仅调试或拆分出具时使用）
- `none`：不与工作报告配套（单独出意见书）

### 意见书版本（Version Tag）

- `初稿`（默认）
- `第 N 稿`
- `申报稿` / `定稿` / `签字稿`（签字律师复核后人工定版，本 skill 不自动产出）

## 输出格式契约（强制）

1. **文件路径**：`04-文件输出/法律意见书/法律意见书-{company_short_name}-{YYYYMMDD}.md`
2. **骨架**：严格按 [`legal-opinion-format.md`](../../shared/templates/legal-opinion-format.md) §三 的 5 段结构（引言 / 释义 / 正文 / 结论性意见 / 特别事项提示）
3. **正文三步法**：每章节意见书小节必须含"事实陈述 / 核查工作 / 法律意见" 3 个三级标题
4. **特别事项提示**：按 `dd-output-schema.md` §5 规则自动注入，不得遗漏任何 `级别=高` 事项
5. **与工作报告配套**：strict 模式下若有不一致必须阻塞；产出**形式配套校验报告**
6. **签字页**：至少 2 名经办律师 + 律所负责人；日期与封面一致

## 与邻近 skill 的边界

- 与 `ecm-draft-report-assembly`：两者共享 DD Memo 输入；本 skill 依赖工作报告（若已生成）做形式配套
- 与 `ecm-draft-disclosure-review`：本 skill 发表意见，disclosure-review 审阅招股书披露；两者不冲突，按业务场景先后调用
- 与 `ecm-draft-format-adjust`：本 skill 输出 Markdown 初稿，format-adjust 负责 Word 套版
- 与 `ecm-qc-opinion-letter-review`：后者对本 skill 的输出做独立审查，不改变本 skill 行为
- 与 `ecm-qc-shareholders-meeting-witness`：见证意见是另一类产品，不走本 skill，不冲突

## 参考资料索引

- [references/default-definitions.md](./references/default-definitions.md) —— 意见书释义段的 15 条基础释义模板
- [references/opinion-statements-template.md](./references/opinion-statements-template.md) —— "法律意见"小节的标准句式模板（肯定 / 有条件肯定 / 保留 3 级）
- [references/consistency-checklist.md](./references/consistency-checklist.md) —— 与律师工作报告的形式配套校验清单

## 常见误用 / FAQ

1. **"发行人的 DD 只做了 10 章，能直接出意见书吗？"**：可以出初稿，但 opinion-letter 会在首页编制说明和形式配套校验报告中显著标注"本意见书仅覆盖已完成核查的 10 章；未完成的 7 章意见待补出"。**不可作为申报材料使用**。
2. **"特别事项提示能手工删除吗？"**：不建议。特别事项来自 17 份 Memo 的"高"级风险，删除会造成意见书与工作报告的风险口径不一致。如确需删除某条，应回到对应 DD skill 重新评估风险等级（降级到"中"或"低"）后重新出 Memo，再重跑本 skill。
3. **"意见书能不能比工作报告发表更乐观的结论？"**：不能。按 `legal-opinion-format.md` §一，意见书结论"不得超出工作报告所载发现"。若工作报告识别了"高"风险，意见书必须以"特别事项提示"或"保留意见"形式体现。
4. **"跨项目能复用释义表吗？"**：本 skill 不支持自动跨项目复用（避免项目间污染）；用户可手工拷贝 `default-definitions.md` 扩充后传入。
5. **"意见书的 Markdown 初稿能直接给客户吗？"**：**不能**。必须经 Word 套版（format-adjust）+ 签字律师复核 + 内核审查后方可交付。

## 变更规则

- 输出契约变动 → MAJOR（同步 `legal-opinion-format.md`、`dd-output-schema.md`、`report-assembly` 的一致性校验逻辑）
- 意见书类型 / 标准句式扩展 → MINOR
- 默认释义 / 法规引用版本更新 → PATCH
