---
name: ecm-workflow-wf-cross-border-ma
description: >
  跨境并购项目工作流 Skill。从项目启动、跨境交易框架设计、涉外尽职调查、文书输出到内核审查的端到端编排，覆盖境内主体出境收购（ODI）/ 境外主体入境收购（FDI）/ 红筹回归 / VIE 收购 / 中概股私有化 / 跨境换股等场景。当用户提到以下场景时触发：跨境并购 / 跨境收购 / cross-border M&A / ODI 项目 / FDI 项目 / 出海收购 / 海外收购 / 境外收购 / 境外主体收购境内 / 红筹回归 / 中概股私有化 / 跨境换股 / VIE 收购 / 跨境项目工作流 / 涉外并购流程 / 跨境并购 kickoff / 帮我接一个跨境并购项目。也包括用户已经决定做跨境并购但不知从何开始、或希望全流程指引下一步应做什么的场景。本 skill **不直接做任何具体业务**——它输出**6 阶段清单 + 下一步指引**，特别强调 7 大跨境主管部门、外汇 / 反垄断 / 国家安全 / 数据出境 / 出口管制等专项合规节点。如不涉及跨境因素，请改用 wf-ma-full（境内并购）或 wf-issuance（再融资）/ wf-ipo-full（IPO）。
version: 0.1.0
license: MIT
module: ecm-workflow
user_role: 项目组律师
phase:
  - 启动阶段
  - 研究阶段
  - 尽调阶段
  - 申报阶段
  - 反馈阶段
category:
  - 工作流编排
depends_on:
  internal_skills:
    - ecm-setup-project-init
    - ecm-setup-file-classify
    - ecm-setup-file-organize
    - ecm-design-cross-border
    - ecm-design-ma-structure
    - ecm-design-control-rights
    - ecm-design-deal-structure
    - ecm-dd-approval
    - ecm-dd-entity
    - ecm-dd-shareholders
    - ecm-dd-business
    - ecm-dd-assets
    - ecm-dd-debt
    - ecm-dd-litigation
    - ecm-dd-compliance
    - ecm-dd-tax
    - ecm-dd-data-verify
    - ecm-dd-file-review
    - ecm-research-case-search
    - ecm-research-reg-search
    - ecm-research-reg-study
    - ecm-draft-report-assembly
    - ecm-draft-opinion-letter
    - ecm-draft-meeting-docs
    - ecm-draft-disclosure-review
    - ecm-draft-format-adjust
    - ecm-qc-opinion-letter-review
    - ecm-qc-work-report-review
    - ecm-qc-meeting-docs-review
    - ecm-qc-disclosure-review
---

# 跨境并购项目 工作流 Skill

## 定位与边界

本 skill **负责**：
- 为跨境并购项目（境内主体出境收购 / 境外主体入境收购 / 红筹回归 / 中概股私有化 / 跨境换股 / VIE 收购）提供**端到端 6 阶段编排**
- 在阶段 2 强调**七大跨境主管部门 + 多重监管路径并行**（发改委 / 商务部 / 外汇 / 国资 / 反垄断 / 国安 / 行业主管 + 数据出境）
- 在阶段 3 优先调用 `ecm-research:reg-search` 梳理境内外法规清单（特别是境外法律意见的依据）
- 显式提示需**境外律师配合**的环节（境外尽调 / 境外法律意见 / 反垄断申报境外部分）

本 skill **不负责**：
- 境内并购的标准编排——见 `wf-ma-full`
- 境外法律工作的实质开展（本仓库 skill 限于中国法律视角；境外法律意见、境外尽调由境外当地律师出具，本 workflow 仅在阶段清单里提示需要境外律师配合的节点）
- 自动化执行——本 skill 输出阶段清单 + 提示

## 免责声明

本 skill 仅为跨境并购项目流程管理辅助工具，被嵌套触发的所有原子 skill 输出**不构成法律意见**，不替代签字律师的专业判断。**境外法律分析需由当地合格律师出具**——本 skill 不替代外国法律意见。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 资深律师执行标准

执行本 skill 时，必须同时遵循 [senior-lawyer-execution-standards.md](../../shared/templates/senior-lawyer-execution-standards.md)。本 skill 的任何输出不得突破四条底线：事实可追溯、法源可核验、风险可分级、建议可落地；无法核验时必须显式标注。

## 本 skill 的实务加固点

- **多线审批图**：必须把境内审批、境外审批、外汇资金、税务、反垄断、数据和制裁节点并列排程。
- **条件先决清单**：SPA/交割条件应映射到每个审批或第三方同意，不得只输出法律研究摘要。
- **境外律师接口**：需明确哪些问题必须由境外律师确认，以及确认意见如何进入项目底稿。
- **strict 原则**：关键审批或资金路径不明时，不提示进入交割文件定稿。

## 与原子 skill 的边界

| 维度 | 各 `ecm-design-*` / `ecm-dd-*` / `ecm-research-*` skill | `ecm-workflow:wf-cross-border-ma`（本 skill） |
|------|----------------------------------|-----------------------------|
| 角色 | "做事的人" | "总指挥官"——输出 6 阶段清单 + 跨境特殊节点提示 |
| 输出 | 业务产物 | 阶段清单 + 下一步指引 + 境外律师配合节点 |
| 触发频次 | 单点触发 | 整个跨境项目周期内被反复参考 |
| 上下文使用 | 加载本任务所需法规 / checklist | 不加载具体业务上下文，但记忆"跨境 = 多线程合规"的 7 部门 + 10 法规速查 |
| 失败影响域 | 仅影响该步产物 | 跨境项目某个监管路径失败可能导致整个交易方案重设——本 workflow 在阶段清单里硬性提示 |

⚠️ 防触发污染：
- 用户问 "ODI 怎么备案" / "37 号文怎么登记"——触发 `ecm-design:cross-border`，不触发本 workflow
- 用户问 "VIE 架构怎么搭"——触发 `ecm-design:cross-border`
- 用户问 "我要做个跨境并购"——触发**本 workflow**

## 配置项

**项目子类型识别**（**强制在阶段 2 之前**确认；影响阶段 2 主导 design skill + 阶段 3 DD 子集 + 阶段 6 监管申报路径）：

| 子类型 | 主导监管线 | 触发的特殊合规事项 |
|-------|---------|------------------|
| 境内主体出境收购（ODI）| 发改委 / 商务部 / 外汇 / 国资 / 行业主管 | 发改委备案或核准、商务部 ODI 证书、银行外汇登记、国资委（如国企）、敏感行业 / 敏感国家加重审查 |
| 境外主体入境收购（FDI）| 商务部 / 发改委 / 外汇 / 反垄断 / 国安 | 外商投资准入负面清单、安全审查（《外商投资安全审查办法》）、反垄断经营者集中、外汇登记 |
| 红筹回归（H 股 / N 股回归 A 股）| 反垄断 / 国安 / 商务部 / 外汇 / 证监会 | 红筹拆除、新设境内主体重新装入、原境外股权处置、税务结构重构 |
| 中概股私有化 | 境内监管 + 境外（开曼 / BVI 法律 + SEC / 美国证券法）| 私有化方案、PIPE 安排、境内 ODI 配合、退市路径 |
| 跨境换股 | 商务部 / 反垄断 / 证监会（如涉及上市公司）| 商务部审查、反垄断申报、境内股东外汇登记 |
| VIE 收购 | 外汇 / 反垄断 / 国安 / 行业主管 | VIE 架构识别、合并报表关系认定、协议控制安排 |

**跳过策略（Skip Policy）**：本 workflow 强制 `strict`（跨境项目监管路径多、容错率低；不允许阶段间占位继续）。

**回滚策略**：见 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认。

---

## 阶段编排

### 阶段 1 — 项目启动

| 项 | 内容 |
|----|------|
| **目标** | 建立项目目录 + 客户文件归位（含境外文件） |
| **调用 skill**（按序）| `ecm-setup:project-init`（项目类型选 "并购重组"，跨境标记）→ `ecm-setup:file-classify`（特别识别境外尽调材料 / 境外律师意见 / 翻译件）→ `ecm-setup:file-organize` |
| **阶段产物** | `{项目根}/` 目录树 + `02-NN-*/文件索引表.md`；额外建议子目录 `04-文件输出/境外律师意见/` |
| **进入下一阶段判定** | 项目根已建 + 至少 80% 客户文件归位 + 已识别"哪些资料需向境外律师索取" |
| **可跳过** | 否 |

### 阶段 2 — 跨境方案设计（**多线程合规识别**）

| 项 | 内容 |
|----|------|
| **目标** | 搭建跨境交易框架；识别全部触发的监管路径；识别境外律师配合节点 |
| **调用 skill**（按序）| `ecm-design:cross-border`（**主导**；6 跨境维度识别 + 7 个主管部门 + 10 部核心法规总览 + 红筹 / VIE 搭拆 + ODI / FDI / 37 号文 / 境外上市备案 / 反垄断 / 国安 / 数据出境的触发点与时间线）→ `ecm-design:ma-structure`（如同时构成 A 股上市公司主导收购）→ `ecm-design:control-rights`（如涉及控制权变更）→ `ecm-design:deal-structure`（通用结构优化） |
| **阶段产物** | `01-方案设计/跨境方案-备忘录-{YYYYMMDD}.md`（遵循 [`shared/templates/legal-memo-format.md`](../../shared/templates/legal-memo-format.md)）；监管路径与时间线表强制；境外律师配合节点清单强制 |
| **进入下一阶段判定** | 方案备忘录初稿完成 + 全部触发的监管路径已识别 + 时间线已与客户对齐 + 境外律师已开始介入 |
| **可跳过** | 否 |

> **触发监管路径识别清单**（阶段 2 强制核对）：
> - ☐ 是否触发发改委备案 / 核准（《境外投资管理办法》）
> - ☐ 是否触发商务部 ODI 证书 /（FDI 时）外商投资负面清单 / 安全审查
> - ☐ 是否触发外汇登记（37 号文 / 9 号文 / ODI 外汇）
> - ☐ 是否触发反垄断经营者集中申报（境内外双线）
> - ☐ 是否触发国家安全审查（外资 / 国资）
> - ☐ 是否触发数据出境（数据出境安全评估办法）
> - ☐ 是否涉及国资（国资委审批）
> - ☐ 是否涉及行业主管部门（金融 / 电信 / 媒体 / 文化 / 教育 / 医疗 / 军工等）
> - ☐ 是否涉及上市公司信披（A 股上市公司收购方 / 标的）
> - ☐ 是否涉及税务结构（境外控股层税务 / VAT / 转让定价）

### 阶段 3 — 涉外尽职调查（**先做研究后做尽调**）

#### 3.1 法规研究先行

跨境项目尽调的前置工作是**先把适用法规清单梳理出来**——境内外法规并行，本仓库 skill 限境内视角，境外部分由境外律师出具。

| 顺序 | skill | 用途 |
|----:|-------|------|
| 1 | `ecm-research:reg-search` | 梳理境内法规清单（发改委 / 商务部 / 外汇 / 反垄断 / 国安 / 数据 / 行业主管 + 上市公司信披）|
| 2 | `ecm-research:reg-study` | 对核心法规做深度研究（如反垄断申报标准、ODI 敏感行业判定）|
| 3 | `ecm-research:case-search` | 检索类似跨境案例（反垄断申报案例、国安审查案例、ODI 拒批案例）|

阶段产物：`06-反馈回复/00-跨境法规清单与案例研究/`（**前置到阶段 3 之前**，作为尽调和后续意见书的基础）

#### 3.2 标的公司核心 DD 子集

| 顺序 | skill | 跨境语境下的核查重点 |
|----:|-------|------------------|
| 1 | `ecm-dd:dd-approval` | 境内 + 境外双向批准；ODI / FDI 备案文件齐备性 |
| 2 | `ecm-dd:dd-entity` | 境内 / 境外主体资格双向核查；境外主体由境外律师出具 |
| 3 | `ecm-dd:dd-shareholders` | 持股穿透到最终自然人 / 实益所有人（**KYC**）；外资持股比例核算（防触发负面清单）|
| 4 | `ecm-dd:dd-business` | 业务资质 / 市场准入 / 出口管制 / 双重用途物项 |
| 5 | `ecm-dd:dd-assets` | 境内外财产权属（双线核查）；含品牌 / 技术等知识产权的跨境处置 |
| 6 | `ecm-dd:dd-debt` | 重大债权债务、跨境担保 / 内保外贷登记、外汇额度 |
| 7 | `ecm-dd:dd-litigation` | 境内外诉讼仲裁（含境外仲裁机构案件）；监管处罚（境外 FCPA / 反贿赂 / 制裁名单）|
| 8 | `ecm-dd:dd-compliance` | 外汇 / 海关 / 税务跨境合规；含 OFAC / EU / UN 制裁筛查、CFIUS（如美国资产）|
| 9 | `ecm-dd:dd-tax` | 跨境税务（特别关注境外 PE 风险、转让定价、CFC 规则、协定优惠适用）|

#### 3.3 工具 skill（按需穿插）

- `ecm-dd:dd-data-verify`（境内工商 / 财务核对；境外部分需用其他境外数据源，本 skill 不直接对接）
- `ecm-dd:dd-file-review`（境内外文件批量审阅；翻译件需特别识别）

#### 3.4 阶段产物 + 进入下一阶段

- **阶段产物**：`02-尽职调查/02-NN-*/DD-Memo-*-{YYYYMMDD}.md`（核心 9 章；遵循 [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md)）+ `06-反馈回复/00-跨境法规清单与案例研究/` 法规备忘录（前置）
- **进入下一阶段判定**：核心 9 章 Memo 出具完毕 + 法规研究备忘录完成 + 境外律师对应章节已交付（标记为"由境外律师 [律所名] 出具，签发日期 [日期]"）
- **可跳过**：第 3.1 法规研究**前置必做**；第 3.2 各章节按子类型可有选择跳过（如纯境内主体出境收购的境内尽调可裁剪 dd-business 中"市场准入"项）

### 阶段 4 — 文书输出

| 项 | 内容 |
|----|------|
| **目标** | 拼接律师工作报告（跨境版）+ 起草法律意见书 + 境外律师意见整合 + 申报文书起草 + 格式套版 |
| **调用 skill**（按序）| `ecm-draft:report-assembly`（按 dd-output-schema 拼接，**境外律师章节作为附件附着**）→ `ecm-draft:opinion-letter`（境内法律意见书；明确"境外法律事项以境外律师意见为准"）→（如涉上市公司）`ecm-draft:meeting-docs` →（如涉信披）`ecm-draft:disclosure-review` → `ecm-draft:format-adjust` |
| **阶段产物** | `04-文件输出/律师工作报告/`、`04-文件输出/法律意见书/`、`04-文件输出/境外律师意见/`（境外律师交付，本 workflow 仅引用）、（如适用）`04-文件输出/重组报告书/` 或 `04-文件输出/收购报告书/` |
| **进入下一阶段判定** | 工作报告 + 意见书 + 境外律师意见整合完成 + 起草人自查通过 |
| **可跳过** | 否 |

> **境外律师意见整合规则**：本 workflow 不撰写境外律师意见的实体内容；只在律师工作报告 / 法律意见书的特定章节插入"境外法律事项以 [境外律所名] 于 [日期] 出具的法律意见为准（见附件 X）"，并把境外文书作为附件归档。

### 阶段 5 — 内核审查（**强烈建议，不可跳过**）

| 项 | 内容 |
|----|------|
| **目标** | 项目组提交内核团队前的独立审查 |
| **调用 skill**（按序）| `ecm-qc:work-report-review` → `ecm-qc:opinion-letter-review` →（如有）`ecm-qc:meeting-docs-review` →（如有）`ecm-qc:disclosure-review` |
| **阶段产物** | 带 tracked changes + comments 的 `.docx`（`w:author="内核"`） |
| **进入下一阶段判定** | 内核【必改】项已全部落实；内核特别关注"境内法律意见与境外律师意见的衔接是否清晰" |
| **可跳过** | 否 |

### 阶段 6 — 申报 / 反馈支持（按需，但跨境项目通常会触发）

| 项 | 内容 |
|----|------|
| **目标** | 监管反馈回复（发改委 / 商务部 / 反垄断 / 证监会等任一线）；持续法律研究 |
| **调用 skill**（按需）| `ecm-research:case-search` / `ecm-research:reg-search` / `ecm-research:reg-study` / `ecm-draft:disclosure-review`（持续起草人自查） |
| **阶段产物** | `06-反馈回复/{监管线}-{反馈批次}/{研究主题}-备忘录-{YYYYMMDD}.md` |
| **可跳过** | 跨境项目**几乎必触发**——多线申报必有反馈 |

---

## skill 间数据传递契约

阶段间数据流完全靠**已经存在的 SoT**，无 workflow 私有状态：

| 阶段衔接 | 依赖 SoT |
|---------|---------|
| 阶段 1 → 阶段 2 | `shared/templates/project-folder-structure.md` |
| 阶段 2 → 阶段 3 | `01-方案设计/跨境方案-备忘录.md` 中的"触发监管路径清单"决定阶段 3 法规研究范围 |
| 阶段 3 → 阶段 4 | `shared/schemas/dd-output-schema.md` § 4 / § 5；境外律师意见作为附件归档（不进入 dd-output-schema 的解析范围）|
| 阶段 4 → 阶段 5 | `shared/templates/qc-skill-template.md` |
| 阶段 5 → 阶段 6 | 监管反馈意见纸质 / 电子件由项目组手工接收 |

### 进度判断（无状态）

```bash
ls -d 01-方案设计/ 2>/dev/null
ls 06-反馈回复/00-跨境法规清单与案例研究/*.md 2>/dev/null  # 阶段 3 前置完成标志
ls 02-尽职调查/02-*/DD-Memo-*.md 2>/dev/null | wc -l  # 跨境定向子集，目标值视子类型
ls 04-文件输出/律师工作报告/*.docx 2>/dev/null
ls 04-文件输出/境外律师意见/*.pdf 2>/dev/null  # 境外律师交付到位
ls 04-文件输出/*-内核后-*.docx 2>/dev/null
```

---

## 失败 / 跳过 / 回滚处理

依据 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认；**跨境项目特殊规则**：

- **任何监管路径申报失败**（发改委备案被退、商务部 ODI 不予批准、反垄断申报被立案审查、国安审查被否）= **整个交易方案需重设**——本 workflow 提示用户"回到阶段 2 重新设计交易结构"，并归档失败批文 / 通知到 `06-反馈回复/{监管线}-不予批准/`
- **境外律师意见拖延** = 阶段 4 不可推进——本 workflow 在阶段清单里给"⛔ 等境外律师"标记
- **strict 模式禁止**阶段间占位继续

---

## 嵌套关系

本 workflow **不嵌套**任何其他 workflow，**也不被任何其他 workflow 嵌套**。

跨境并购的复杂度高、监管路径多——直接调本 workflow，不要套娃。如项目同时是"上市公司主导的跨境并购"，**仍用本 workflow**（不要在 `wf-ma-full` 中加跨境补丁，也不要嵌套 `wf-ma-full`）；上市公司信披环节由本 workflow 在阶段 4 / 阶段 5 中触发对应的 `ecm-draft:disclosure-review` / `ecm-qc:disclosure-review`。

---

## 端到端示例（脑内测试）

**场景：境内 A 公司收购德国 B 公司 100% 股权（ODI）**

```
用户："我们要收购一家德国汽车零部件公司，全资收购"

本 skill：
  项目类型识别：境内主体出境收购（ODI）
  阶段 1：建项目目录 + 文件归位（识别 B 公司德国子公司材料、英德文翻译件）
  阶段 2：触发 `ecm-design:cross-border`（核对监管路径清单）：
    ☑ 发改委备案（核心；汽车零部件是非敏感，备案制）
    ☑ 商务部 ODI 证书
    ☑ 外汇登记
    ☐ 国资委（A 公司非国企，不触发）
    ☐ 反垄断（年度营业额低于申报门槛，不触发）
    ☐ 国安审查（汽车零部件不属于敏感产业）
    ☐ 数据出境（如涉及德国客户数据出境则触发）
    ☑ 行业主管：工信部（汽车产业政策）
    境外律师配合节点：B 公司德国法律意见、德国劳动法（员工权益）、欧盟反垄断
  阶段 2 输出：跨境方案备忘录 + 触发清单 + 时间线
  
  阶段 3.1（前置法规研究）：触发 `ecm-research:reg-search` + `ecm-research:reg-study`
    + `ecm-research:case-search`（类似德国汽车并购案例）
  阶段 3.2（境内 DD）：dd-approval（A 公司董事会决议 + 发改委备案文件 + 商务部 ODI 证书
    + 银行外汇登记）+ dd-entity（A 公司）+ dd-shareholders（穿透）+ dd-business
    + dd-assets + dd-debt（含跨境担保）+ dd-litigation + dd-compliance（外汇 / 海关 / 税务）
    + dd-tax（CFC + 转让定价 + 中德税收协定）
    境外 DD：由德国律师出具 B 公司尽调报告
  
  阶段 4：report-assembly + opinion-letter（境内法律意见，境外事项以德国律师意见为准）
    + format-adjust
  阶段 5：work-report-review + opinion-letter-review
  阶段 6：发改委 / 商务部反馈来时按需触发 ecm-research-* / disclosure-review
```

---

## 参考资料索引

本 skill 不自带 references/ 目录——所有参考资料由各原子 skill 自带，特别是 `ecm-design:cross-border` 的 7 大主管部门 + 10 部核心法规总览。

跨 skill SoT 引用：

- [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md)
- [`shared/templates/project-folder-structure.md`](../../shared/templates/project-folder-structure.md)
- [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md)
- [`shared/templates/work-report-format.md`](../../shared/templates/work-report-format.md) / [`legal-opinion-format.md`](../../shared/templates/legal-opinion-format.md) / [`legal-memo-format.md`](../../shared/templates/legal-memo-format.md) / [`meeting-docs-format.md`](../../shared/templates/meeting-docs-format.md) / [`research-output-format.md`](../../shared/templates/research-output-format.md)
- [`shared/templates/qc-skill-template.md`](../../shared/templates/qc-skill-template.md)

---

## 版本

| 日期 | 变更 |
|------|------|
| 2026-04-25 | 初版。锁定 6 阶段编排 + 阶段 2 强制 10 项监管路径清单核对 + 阶段 3 法规研究前置（先做研究后做尽调）+ 境外律师配合节点显式提示 + 境外律师意见作为附件整合规则 + 阶段 6 反馈支持几乎必触发的实务认知 + strict 模式强制 |
