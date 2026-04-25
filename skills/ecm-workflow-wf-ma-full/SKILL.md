---
name: ecm-workflow-wf-ma-full
description: >
  完整并购重组项目工作流 Skill。从项目启动、交易结构设计、定向尽职调查、文书输出到内核审查的端到端编排，覆盖一般并购 / 重大资产重组 / 借壳上市 / 上市公司收购 / 控制权变更 / 私募基金收购等多场景。当用户提到以下场景时触发：并购项目 / 重组项目 / M&A / 收购项目 / 资产收购 / 股权收购 / 整体收购 / 借壳 / 上市公司收购 / 控制权交易 / 重大资产重组 / 完整并购流程 / 并购全流程 / 并购工作流 / 并购编排 / 并购 kickoff / 帮我接一个并购项目 / 我要做并购 / 客户要并购了。也包括用户已经决定要做并购但不知道从哪里开始、或者希望全流程指引下一步应该做什么的场景。本 skill **不直接做任何具体业务**——它输出**6 阶段清单 + 下一步指引**，由用户在每个阶段实际触发对应原子 skill。即使用户未明确说"workflow"或"全流程"，只要表达"我要做个并购""客户要并购了"也应触发。如涉及跨境因素，请改用 wf-cross-border-ma；如是上市公司再融资（定增 / 配股 / 可转债）请用 wf-issuance。
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
    - ecm-design-deal-structure
    - ecm-design-ma-structure
    - ecm-design-control-rights
    - ecm-dd-approval
    - ecm-dd-entity
    - ecm-dd-shareholders
    - ecm-dd-history
    - ecm-dd-business
    - ecm-dd-related-party
    - ecm-dd-assets
    - ecm-dd-debt
    - ecm-dd-litigation
    - ecm-dd-compliance
    - ecm-dd-data-verify
    - ecm-dd-file-review
    - ecm-draft-report-assembly
    - ecm-draft-opinion-letter
    - ecm-draft-meeting-docs
    - ecm-draft-disclosure-review
    - ecm-draft-format-adjust
    - ecm-qc-opinion-letter-review
    - ecm-qc-work-report-review
    - ecm-qc-meeting-docs-review
    - ecm-qc-disclosure-review
    - ecm-research-case-search
    - ecm-research-reg-search
    - ecm-research-reg-study
---

# 完整并购重组项目 工作流 Skill

## 定位与边界

本 skill **负责**：
- 为并购项目（一般并购 / 重大资产重组 / 借壳上市 / 上市公司收购 / 控制权变更）提供**端到端 6 阶段编排**
- 在尽调阶段提供**定向 DD 子集编排**（与 IPO 全 17 章不同，并购项目按交易性质 / 标的属性选取必查章节）
- 在每个阶段完成后给出"下一步应调用的 skill"提示

本 skill **不负责**：
- 具体业务工作（交易结构设计 / 定向尽调 / 文书撰写 / 内核审查）——交给被编排的原子 skill
- 跨境并购的特殊编排——见 `wf-cross-border-ma`（境内外法律框架、ODI / FDI / 反垄断 / 国安审查另立编排）
- 自动化执行——本 skill 输出阶段清单 + 提示

## 免责声明

本 skill 仅为并购项目流程管理辅助工具，被嵌套触发的所有原子 skill 输出**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 与原子 skill 的边界

| 维度 | 各 `ecm-design-*` / `ecm-dd-*` / `ecm-draft-*` / `ecm-qc-*` skill | `ecm-workflow:wf-ma-full`（本 skill） |
|------|----------------------------------|-----------------------------|
| 角色 | "做事的人"——产出业务产物 | "总指挥官"——输出 6 阶段清单 + 进度提示 |
| 输出 | 业务产物（Markdown / DOCX） | 阶段清单 + 下一步指引（不落客户文件） |
| 触发频次 | 单点触发 | 整个并购项目周期内被反复参考 |
| 上下文使用 | 加载本任务所需法规 / checklist | 不加载具体业务上下文 |
| 失败影响域 | 仅影响该步产物 | 失败不阻塞——用户可绕过本 workflow 直接调原子 skill |

⚠️ 防触发污染：
- 用户问"上市公司发行股份购买资产怎么算重大资产重组"——触发 `ecm-design:ma-structure`，不触发本 workflow
- 用户问"控制权稳定性怎么核查"——触发 `ecm-dd:dd-shareholders` + `ecm-design:control-rights`
- 用户问"我要接个并购项目，从头到尾给我安排一下"——触发**本 workflow**

## 配置项

**项目类型识别**（**强制在阶段 2 之前**确认；影响阶段 2 的 design skill 选择和阶段 3 的 DD 子集）：

| 子类型 | 主导 design skill | DD 子集要点 |
|-------|------------------|------------|
| 一般并购（非上市公司收购非上市公司） | `ecm-design:deal-structure` | 全套（除募集资金运用）|
| 重大资产重组 / 借壳（上市公司主导） | `ecm-design:ma-structure` + `ecm-design:control-rights` | 必含 `dd-shareholders` / `dd-related-party` / `dd-business` / `dd-litigation`；上市公司方还要做"信披合规" |
| 上市公司收购（要约 / 协议 / 间接）| `ecm-design:control-rights` + `ecm-design:ma-structure` | 必含 `dd-shareholders`（穿透至最终自然人）+ `dd-related-party` + `dd-history`（控制权稳定性） |
| 控制权交易（非要约触发） | `ecm-design:control-rights` | 必含 `dd-shareholders` + `dd-history` + `dd-charter`（章程反收购条款）+ `dd-related-party` |

**跳过策略（Skip Policy）**：
- `strict` / `loose`（默认 loose）

**回滚策略**：见 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4，沿用默认。

---

## 阶段编排

### 阶段 1 — 项目启动

| 项 | 内容 |
|----|------|
| **目标** | 建立项目目录 + 客户文件归位 |
| **调用 skill**（按序）| `ecm-setup:project-init`（项目类型选 "并购重组"）→ `ecm-setup:file-classify` → `ecm-setup:file-organize` |
| **阶段产物** | `{项目根}/` 目录树 + `02-NN-*/文件索引表.md` |
| **进入下一阶段判定** | 项目根已建 + 至少 80% 客户文件归位 |
| **可跳过** | 否 |

### 阶段 2 — 方案设计

| 项 | 内容 |
|----|------|
| **目标** | 确定交易结构（股权 vs 资产 vs 增资 vs 合并）+ 支付方式 + 控制权安排 + 监管路径 |
| **调用 skill**（按子类型）|<br>**一般并购**：`ecm-design:deal-structure`<br>**重大资产重组 / 借壳**：`ecm-design:ma-structure` → `ecm-design:control-rights`（如涉及控制权变更）→（可回到 `ecm-design:deal-structure` 优化股权 vs 资产路径）<br>**上市公司收购**：`ecm-design:control-rights`（要约 / 协议 / 间接）→ `ecm-design:ma-structure`（如同时构成发行股份购买资产）<br>**控制权交易**：`ecm-design:control-rights` |
| **阶段产物** | `01-方案设计/{方案名}-备忘录-{YYYYMMDD}.md`（遵循 [`shared/templates/legal-memo-format.md`](../../shared/templates/legal-memo-format.md)）；多方案比较时产出多份 |
| **进入下一阶段判定** | 主案备忘录初稿完成 + 项目组对核心结构有共识 + 监管路径已识别（是否触发要约 / 是否构成借壳 / 是否需反垄断申报） |
| **可跳过** | 否 |

### 阶段 3 — 尽职调查（**定向子集**，不调 wf-ipo-dd-full）

并购项目的尽调与 IPO 的 17 章不同——**只覆盖与本次交易相关的章节**，且按交易方向分目标公司 vs 收购方两套（视项目情况）。

#### 3.1 标的公司核心 DD 子集（**必查**）

| 顺序 | skill | 编报规则章节 | 并购语境下的核查重点 |
|----:|-------|-------------|------------------|
| 1 | `ecm-dd:dd-approval` | 第 1 章 | 标的公司本次交易的内部审议 + 外部批准（国资 / 反垄断 / 国安）|
| 2 | `ecm-dd:dd-entity` | 第 2 章 | 标的主体资格、经营范围、特殊行业资质 |
| 3 | `ecm-dd:dd-shareholders` | 第 5 章 | 持股穿透到最终自然人 + 一致行动 + 代持清理 + 是否存在国有股权 |
| 4 | `ecm-dd:dd-history` | 第 6 章 | 标的设立到本次交易前的股本演变（每次出资 / 转让的合规性 + 税务处理） |
| 5 | `ecm-dd:dd-business` | 第 7 章 | 主营业务 / 资质 / 重大合同（**特别关注 change of control 条款**） |
| 6 | `ecm-dd:dd-related-party` | 第 8 章 | 标的与收购方 / 第三方的关联交易（影响交易公允性） |
| 7 | `ecm-dd:dd-assets` | 第 9 章 | 主要财产权属（不动产 / 知识产权 / 重大设备）；交易标的为资产时尤为关键 |
| 8 | `ecm-dd:dd-debt` | 第 10 章 | 重大债权债务、对外担保、或有负债（**对赌 / 业绩承诺 / change of control 触发**）|
| 9 | `ecm-dd:dd-litigation` | 第 16 章 | 诉讼仲裁处罚（影响估值 / 是否需买方陈述与保证）|
| 10 | `ecm-dd:dd-compliance` | 第 17 章 | 社保 / 公积金 / 海关 / 外汇 / 劳动等兜底事项 |

#### 3.2 按交易子类型追加（**按需**）

| 子类型 | 追加 DD skill | 理由 |
|-------|------------|------|
| 上市公司收购 / 重大资产重组 | `ecm-dd:dd-charter`（标的章程反收购条款）；上市公司方的 `ecm-dd:dd-charter` + `ecm-dd:dd-directors` | 上市公司方需做最近 36 个月信披合规自查 |
| 借壳上市 | 全 17 章（标的公司视角，等同 IPO 尽调）——此时**回退调用 `wf-ipo-dd-full`**，不在本 workflow 内重复编排 | 借壳本质是借壳方上市，与 IPO 等同标准 |
| 国资标的 | `ecm-dd:dd-approval`（侧重国资审批）+ `ecm-dd:dd-history`（国资股权演变特殊程序）| 国资委 / 财政部审批是硬要件 |

#### 3.3 工具 skill（按需穿插）

- `ecm-dd:dd-data-verify`（工商 / 财务数据自动比对，节省 manual 工时）
- `ecm-dd:dd-file-review`（文件量大时批量提取关键字段）

#### 3.4 阶段产物 + 进入下一阶段

- **阶段产物**：`02-尽职调查/02-NN-*/DD-Memo-*-{YYYYMMDD}.md`（核心 10 章 + 子类型追加章节；遵循 [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md)）
- **进入下一阶段判定**：必查子集 10 份 Memo 出具完毕 + 子类型追加章节按需出具完毕 + "三、风险分级汇总"表已填
- **可跳过**：否；但**不查**的章节（如 dd-fundraising 募集资金运用——并购项目除非交易支付涉及发行股份配套融资，否则不触发；dd-tax / dd-environment 仅在标的有重大税务 / 环保历史问题时触发）需要在阶段清单里标 `⤵ 已跳过：本子类型不适用`

### 阶段 4 — 文书输出

| 项 | 内容 |
|----|------|
| **目标** | 拼接律师工作报告（并购版）+ 起草法律意见书（并购版）+ 起草交易文件相关会议文件 + 信披自查（上市公司 / 借壳 / 重大资产重组）+ 格式套版 |
| **调用 skill**（按序）| `ecm-draft:report-assembly`（按 dd-output-schema 拼接，缺章节按违约处理）→ `ecm-draft:opinion-letter`（结论性意见 + 特别事项提示自动注入）→ `ecm-draft:meeting-docs`（董事会决议 / 股东（大）会决议 / 关联股东回避 / 中小投资者单独计票）→（如适用）`ecm-draft:disclosure-review`（**起草人自查**重组报告书 / 收购报告书 / 权益变动报告书的法律相关章节）→ `ecm-draft:format-adjust` |
| **阶段产物** | `04-文件输出/律师工作报告/`、`04-文件输出/法律意见书/`、`04-文件输出/会议文件/`、（如涉及上市公司）`04-文件输出/重组报告书/` 或 `04-文件输出/收购报告书/` |
| **进入下一阶段判定** | 工作报告 + 意见书 + 关键会议文件初稿完成 + 起草人自查通过 |
| **可跳过** | 否；但子步骤 `meeting-docs` / `disclosure-review` 按交易是否上市公司主导 + 是否到上会 / 披露节点决定 |

> **重大资产重组 / 借壳的信披要求**：上市公司主导的并购涉及《上市公司重大资产重组管理办法》要求的信披文件（重组报告书、独立财务顾问报告等的法律相关章节）。如本项目涉及，阶段 4 必须包含 `ecm-draft:disclosure-review`。

### 阶段 5 — 内核审查（**强烈建议，不可跳过**）

| 项 | 内容 |
|----|------|
| **目标** | 项目组提交内核团队前的独立审查 |
| **调用 skill**（按序）| `ecm-qc:work-report-review`（律师工作报告）→ `ecm-qc:opinion-letter-review`（法律意见书）→（如有）`ecm-qc:meeting-docs-review`（关键会议文件）→（如有）`ecm-qc:disclosure-review`（重组 / 收购报告书）|
| **阶段产物** | 带 tracked changes + comments 的 `.docx`（`w:author="内核"`） |
| **进入下一阶段判定** | 内核【必改】项已全部落实 |
| **可跳过** | 否 |

### 阶段 6 — 申报 / 反馈支持（按需）

| 项 | 内容 |
|----|------|
| **目标** | 反馈回复 / 类似交易案例检索 / 监管沟通法律研究 |
| **调用 skill**（按需）| `ecm-research:case-search`（类似并购案例 / 重组委审议关注点 / 上市公司收购处罚案例）/ `ecm-research:reg-search` / `ecm-research:reg-study` |
| **阶段产物** | `06-反馈回复/{反馈批次}/{研究主题}-备忘录-{YYYYMMDD}.md` |
| **可跳过** | 是（按申报推进决定） |

---

## skill 间数据传递契约

阶段间数据流完全靠**已经存在的 SoT**：

| 阶段衔接 | 依赖 SoT |
|---------|---------|
| 阶段 1 → 阶段 2 | `shared/templates/project-folder-structure.md` |
| 阶段 2 → 阶段 3 | `01-方案设计/{方案名}-备忘录.md` 影响 DD 子集选取（如借壳即触发全 17 章） |
| 阶段 3 → 阶段 4 | `shared/schemas/dd-output-schema.md` § 4 / § 5（拼接 + 意见书消费规则；缺章节按违约处理） |
| 阶段 4 → 阶段 5 | `shared/templates/qc-skill-template.md`（4 个 ecm-qc-* skill 的统一工作流） |

### 进度判断（无状态）

```bash
ls -d 01-方案设计/ 2>/dev/null
ls 02-尽职调查/02-*/DD-Memo-*.md 2>/dev/null | wc -l   # 并购定向子集，目标值视子类型
ls 04-文件输出/律师工作报告/*.docx 2>/dev/null
ls 04-文件输出/*-内核后-*.docx 2>/dev/null
```

---

## 失败 / 跳过 / 回滚处理

依据 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认。

**特殊提示**：
- 阶段 3 的"必查子集"若有任何章节失败，本 workflow 提示"该章节关系并购交易合规性，建议补资料后重跑；strict 模式禁止跳过"
- 阶段 4 信披文件缺失（重组 / 借壳 / 上市公司收购场景）= **本项目无法正常向交易所申报**——本 workflow 在阶段清单里硬性提示
- 阶段 5（内核）失败 = 内核反馈【必改】项未全部落实——回到阶段 4 修订

---

## 嵌套关系

本 workflow **可选嵌套**：

- 当项目子类型为 "借壳上市" 时，阶段 3 的标的公司尽调建议**回退调用 `wf-ipo-dd-full`**（借壳 = 标的公司用借壳方式上市，DD 标准与 IPO 等同）
- 嵌套时阶段 3 处只写一行 "调用 `ecm-workflow:wf-ipo-dd-full`（借壳 = IPO 等同尽调）"，不复制 17 章清单

本 workflow **不被任何其他 workflow 嵌套**。

如项目同时具有跨境因素（如标的为境外公司、收购方为境内主体的 ODI 收购），不嵌套本 skill 而是改用 `wf-cross-border-ma`。

---

## 端到端示例（脑内测试）

**场景 1：上市公司发行股份购买资产**

```
用户："上市公司发股份购买一家民营科技公司，控制权不变"

本 skill：
  项目类型识别：重大资产重组（非借壳；控制权不变意味着不触发借壳标准）
  阶段 1：建项目目录（项目类型 = 并购重组）
  阶段 2：触发 `ecm-design:ma-structure`（确认是否构成重大资产重组、配套融资安排）
        + `ecm-design:deal-structure`（如需优化股权 vs 资产路径）
  阶段 3 必查 10 章 + 追加：dd-charter（标的章程）；上市公司方做 dd-charter + dd-directors
        （上市公司近 36 个月信披合规自查）
  阶段 4：report-assembly + opinion-letter + meeting-docs（董事会 + 股东大会决议 + 中小投
        资者单独计票）+ disclosure-review（重组报告书法律相关章节）+ format-adjust
  阶段 5：四个 ecm-qc-* 全部触发
  阶段 6：交易所反馈来时按需触发 ecm-research-*
```

**场景 2：A 收购 B（非上市公司）股权 51%**

```
用户："我是 A 公司，要收购 B 公司 51% 股权，B 是民营科技公司"

本 skill：
  项目类型识别：一般并购 + 控制权交易
  阶段 1：建项目目录
  阶段 2：触发 `ecm-design:deal-structure`（股权收购方式）+ `ecm-design:control-rights`
        （控制权获取策略 + 锁定条款 + 反稀释 + 业绩对赌）
  阶段 3 必查 10 章（标的视角）+ 追加：dd-charter（B 公司章程反收购条款）
  阶段 4：report-assembly + opinion-letter + meeting-docs（A 公司董事会决议）+ format-adjust
        无 disclosure-review（非上市公司，无信披文件）
  阶段 5：work-report-review + opinion-letter-review + meeting-docs-review
  阶段 6：按需
```

**场景 3：借壳上市**

```
用户："我们是借壳方，把资产装进一家壳公司"

本 skill：
  项目类型识别：借壳上市（标的公司方视角等同 IPO）
  阶段 1：建项目目录
  阶段 2：触发 `ecm-design:ma-structure`（借壳判定 + 同步发行股份购买资产 + 配套融资）+
        `ecm-design:control-rights`（壳公司控制权变更）
  阶段 3：**回退嵌套调用 `ecm-workflow:wf-ipo-dd-full`**（借壳标的视角 = IPO 全 17 章尽调）
  阶段 4-5-6：同 IPO
```

---

## 参考资料索引

本 skill 不自带 references/ 目录——所有参考资料由各原子 skill 自带。

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
| 2026-04-25 | 初版（BATCH-10）。锁定 6 阶段编排 + 阶段 2 按子类型分流（一般并购 / 重大资产重组 / 上市公司收购 / 借壳）+ 阶段 3 定向 DD 子集（必查 10 章 + 子类型追加）+ 借壳场景回退嵌套 wf-ipo-dd-full + 上市公司主导项目的信披自查必含 |
