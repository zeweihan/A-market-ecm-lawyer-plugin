---
name: ecm-workflow-wf-nto-listing
description: >
  新三板挂牌项目工作流 Skill。从项目启动、挂牌路径分析、尽职调查、文书输出到内核审查的端到端编排，覆盖新三板基础层 / 创新层挂牌、北交所上市衔接、新三板定增、做市商安排等场景。当用户提到以下场景时触发：新三板 / NEEQ / 全国中小企业股份转让系统 / 三板挂牌 / 挂牌新三板 / 三板项目 / 创新层挂牌 / 北交所衔接 / 北交所 IPO（从新三板创新层转板）/ 新三板挂牌工作流 / 三板挂牌全流程 / 帮我接一个新三板挂牌项目 / 客户要去新三板。也包括用户已经决定挂牌新三板但不知从何开始、或希望全流程指引下一步应做什么的场景。本 skill **不直接做任何具体业务**——它输出**6 阶段清单 + 下一步指引**，特别强调"新三板尽调标准与 IPO 高度重合"的实务认知（嵌套调用 wf-ipo-dd-full），以及新三板特殊文书（公开转让说明书 / 主办券商推荐报告等）的法律相关章节。如是 A 股 IPO（首发，含北交所首发上市）请用 wf-ipo-full；如是再融资请用 wf-issuance。
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
    - ecm-design-ipo-path
    - ecm-workflow-wf-ipo-dd-full
    - ecm-dd-data-verify
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

# 新三板挂牌项目 工作流 Skill

## 定位与边界

本 skill **负责**：
- 为新三板挂牌项目（基础层 / 创新层挂牌、北交所上市衔接、新三板定增、做市商安排）提供**端到端 6 阶段编排**
- 在阶段 2 帮助用户论证**挂牌路径**（基础层直接挂牌 / 创新层挂牌 / 创新层 → 北交所 IPO 衔接路径）
- 在阶段 3 **嵌套调用 `ecm-workflow:wf-ipo-dd-full`**——新三板尽调标准与 IPO 高度重合，复用编排
- 在阶段 4 强调**公开转让说明书 / 主办券商推荐报告法律相关章节**等新三板特殊文书

本 skill **不负责**：
- A 股 IPO（首发上市，含北交所直接首发上市）的编排——见 `wf-ipo-full`
- 上市公司再融资——见 `wf-issuance`
- 自动化执行——本 skill 输出阶段清单 + 提示

## 免责声明

本 skill 仅为新三板挂牌项目流程管理辅助工具，被嵌套触发的所有原子 skill 输出**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 资深律师执行标准

执行本 skill 时，必须同时遵循 [senior-lawyer-execution-standards.md](../../shared/templates/senior-lawyer-execution-standards.md)。本 skill 的任何输出不得突破四条底线：事实可追溯、法源可核验、风险可分级、建议可落地；无法核验时必须显式标注。

## 本 skill 的实务加固点

- **挂牌与北交所分流**：基础层/创新层挂牌、创新层进层、北交所 IPO 衔接必须先分类。
- **公众公司规则**：股转业务规则、信息披露、公司治理、定向发行和主办券商内核节点必须进入流程。
- **IPO 标准提前看**：有北交所预期的项目，DD 标准应前置对齐 IPO，而不是仅满足挂牌底线。
- **路径切换提示**：已满足北交所申报条件或目标转为上市时，应提示切换 `wf-ipo-full`。

## 与原子 skill 的边界

| 维度 | 各 `ecm-design-*` / `ecm-dd-*` / `ecm-draft-*` skill | `ecm-workflow:wf-nto-listing`（本 skill） |
|------|----------------------------------|-----------------------------|
| 角色 | "做事的人" | "总指挥官"——输出 6 阶段清单 + 进度提示 |
| 输出 | 业务产物 | 阶段清单 + 下一步指引 |
| 触发频次 | 单点触发 | 整个新三板项目周期内被反复参考 |
| 上下文使用 | 加载本任务所需法规 / checklist | 不加载具体业务上下文，但记忆"新三板 ≈ IPO 尽调"的实务认知 |
| 失败影响域 | 仅影响该步产物 | 失败不阻塞——用户可绕过本 workflow 直接调原子 skill |

⚠️ 防触发污染：
- 用户问 "新三板挂牌条件是什么"——触发 `ecm-design:ipo-path`（pathway-rules 含新三板规则），不触发本 workflow
- 用户问 "从创新层到北交所怎么转板"——触发 `ecm-design:ipo-path`
- 用户问 "我要做个新三板挂牌"——触发**本 workflow**

## 配置项

**项目子类型识别**（**强制在阶段 2 之前**确认；影响阶段 2 主导论证 + 阶段 3 / 4 重点）：

| 子类型 | 阶段 2 重点 | 阶段 3 重点 | 阶段 4 文书重点 |
|-------|----------|----------|--------------|
| 基础层直接挂牌 | 满足《全国中小企业股份转让系统业务规则（试行）》挂牌条件 | 全套 17 章（IPO 等同标准；本 workflow 调 `wf-ipo-dd-full`）| 公开转让说明书法律相关章节 + 主办券商推荐报告 + 法律意见书 |
| 创新层挂牌（直接申请创新层 or 基础层升创新层）| 满足创新层进入条件（市值 / 净资产 / 净利润 / 营业收入等多套指标二选一）| 同基础层 + 创新层进入指标核查 | 同基础层 + 创新层资格申请文件 |
| 创新层 → 北交所 IPO 衔接 | 论证创新层挂牌 12 个月以上 + 北交所发行条件衔接 | **此时改用 `wf-ipo-full`**——北交所 IPO 是"首发上市"，与本 workflow 的"挂牌"性质不同 | （归入 wf-ipo-full）|
| 新三板定增 | 不在本 workflow 范围 | （归入 wf-issuance 或单独触发原子 skill）| （归入 wf-issuance）|

> **创新层 → 北交所 IPO 路径切换提示**：当用户表达"我们想从创新层去北交所"且**已挂牌**——重点是**北交所 IPO 的发行条件**而非新三板挂牌——此时本 workflow 提示"切换到 `wf-ipo-full`"。当用户表达"我们想挂新三板，将来去北交所"且**尚未挂牌**——本 workflow 处理"先挂创新层"的部分，"将来去北交所"由后续启动的新一轮 `wf-ipo-full` 项目处理。

**跳过策略（Skip Policy）**：
- `strict` / `loose`（默认 loose）

**回滚策略**：见 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认。

---

## 阶段编排

### 阶段 1 — 项目启动

| 项 | 内容 |
|----|------|
| **目标** | 建立项目目录 + 客户文件归位 |
| **调用 skill**（按序）| `ecm-setup:project-init`（项目类型选 "新三板挂牌"）→ `ecm-setup:file-classify` → `ecm-setup:file-organize` |
| **阶段产物** | `{项目根}/` 目录树 + `02-NN-*/文件索引表.md` |
| **进入下一阶段判定** | 项目根已建 + 至少 80% 客户文件归位 |
| **可跳过** | 否 |

### 阶段 2 — 方案设计（挂牌路径论证）

| 项 | 内容 |
|----|------|
| **目标** | 论证新三板挂牌路径（基础层 vs 创新层 vs 后续北交所 IPO 衔接）+ 确认股份制改造完成 + 评估北交所衔接可行性 |
| **调用 skill** | `ecm-design:ipo-path`（**含新三板 / 北交所规则速查**；该 skill 的 `references/pathway-rules.md` 涵盖新三板基础层 / 创新层进入条件 + 北交所衔接路径）|
| **阶段产物** | `01-方案设计/挂牌路径论证-备忘录-{YYYYMMDD}.md`（遵循 [`shared/templates/legal-memo-format.md`](../../shared/templates/legal-memo-format.md)）|
| **进入下一阶段判定** | 路径备忘录初稿完成 + 确定基础层 / 创新层目标 + 北交所衔接可行性已评估（如适用） |
| **可跳过** | 否 |

### 阶段 3 — 尽职调查（**嵌套调用 `wf-ipo-dd-full`**）

新三板挂牌的尽调标准与 IPO 高度重合（《全国中小企业股份转让系统挂牌公司业务规则》借鉴《首次公开发行股票注册管理办法》框架）。

| 项 | 内容 |
|----|------|
| **目标** | 按编报规则第 12 号完成 17 章尽调 + 创新层 / 北交所衔接的额外指标核查 |
| **调用 skill**（嵌套）| `ecm-workflow:wf-ipo-dd-full`（包含 17 个 `ecm-dd-*` 业务 skill + 2 个工具 skill；具体执行顺序由该子 workflow 锁定） |
| **追加 skill**（按需）| `ecm-dd:dd-data-verify`（财务数据自动比对核验创新层进入指标）|
| **阶段产物** | `02-尽职调查/02-NN-{章节}/DD-Memo-{章节}-{YYYYMMDD}.md`（17 份） |
| **进入下一阶段判定** | 17 份 Memo 全部出具 + 创新层进入指标已核验（如适用） |
| **可跳过** | 否（IPO 等同标准；不可裁剪） |

> **嵌套规则**（依据 `shared/templates/workflow-skill-template.md` § 6）：本 skill 在此阶段**只写一行 "调用 `ecm-workflow:wf-ipo-dd-full`"**，**不复制** 17 章清单。子 workflow 的进度由其阶段产物（Memo 是否齐备）独立判定。

### 阶段 4 — 文书输出

| 项 | 内容 |
|----|------|
| **目标** | 拼接律师工作报告（新三板版）+ 起草法律意见书（新三板版）+ 起草董事会 / 股东大会决议 + 公开转让说明书 / 主办券商推荐报告法律相关章节自查 + 格式套版 |
| **调用 skill**（按序）| `ecm-draft:report-assembly`（按 dd-output-schema 拼接，**报告类型选 "尽职调查报告"** 或 "律师工作报告" 与新三板申报要求衔接） → `ecm-draft:opinion-letter`（事实-核查-意见三步法 + 自动注入"特别事项提示"） →（按需）`ecm-draft:meeting-docs`（股改完成后的董事会 / 股东大会决议）→ `ecm-draft:disclosure-review`（**起草人自查**公开转让说明书法律相关章节）→ `ecm-draft:format-adjust` |
| **阶段产物** | `04-文件输出/律师工作报告/`、`04-文件输出/法律意见书/`、`04-文件输出/会议文件/`、`04-文件输出/公开转让说明书法律相关章节-自查报告/` |
| **进入下一阶段判定** | 工作报告 + 意见书 + 公开转让说明书法律章节自查通过 |
| **可跳过** | 否 |

> **新三板特殊文书**：除律师工作报告 + 法律意见书外，新三板挂牌涉及《公开转让说明书》——其中法律相关章节（主体资格、设立沿革、股权结构、董监高、关联交易、规范运作等）需起草人自查；本 workflow 通过 `ecm-draft:disclosure-review` 实现。`disclosure-review` 的 `references/disclosure-chapter-map.md` 已含新三板《公开转让说明书》章节映射。

### 阶段 5 — 内核审查（**强烈建议，不可跳过**）

| 项 | 内容 |
|----|------|
| **目标** | 项目组提交内核团队前的独立审查 |
| **调用 skill**（按序）| `ecm-qc:work-report-review` → `ecm-qc:opinion-letter-review` →（如有）`ecm-qc:meeting-docs-review` → `ecm-qc:disclosure-review`（公开转让说明书法律相关章节） |
| **阶段产物** | 带 tracked changes + comments 的 `.docx`（`w:author="内核"`） |
| **进入下一阶段判定** | 内核【必改】项已全部落实 |
| **可跳过** | 否 |

### 阶段 6 — 申报 / 反馈支持（按需）

| 项 | 内容 |
|----|------|
| **目标** | 全国股转公司反馈回复 / 类似挂牌案例检索 / 法规深度研究 |
| **调用 skill**（按需）| `ecm-research:case-search`（类似新三板挂牌案例 / 全国股转公司挂牌问询案例 / 创新层资格审查案例）/ `ecm-research:reg-search`（最新新三板规则）/ `ecm-research:reg-study` / `ecm-draft:disclosure-review`（持续起草人自查）|
| **阶段产物** | `06-反馈回复/{反馈批次}/{研究主题}-备忘录-{YYYYMMDD}.md` |
| **可跳过** | 是（按申报推进决定） |

---

## skill 间数据传递契约

阶段间数据流完全靠**已经存在的 SoT**，无 workflow 私有状态：

| 阶段衔接 | 依赖 SoT |
|---------|---------|
| 阶段 1 → 阶段 2 | `shared/templates/project-folder-structure.md` |
| 阶段 2 → 阶段 3 | `01-方案设计/挂牌路径论证-备忘录.md` 影响 wf-ipo-dd-full 内部各章节核查重点（如基础层标准 vs 创新层标准）|
| 阶段 3 → 阶段 4 | `shared/schemas/dd-output-schema.md` § 4 / § 5 |
| 阶段 4 → 阶段 5 | `shared/templates/qc-skill-template.md` |

### 进度判断（无状态）

```bash
ls -d 01-方案设计/ 2>/dev/null
ls 02-尽职调查/02-*/DD-Memo-*.md 2>/dev/null | wc -l   # 目标 17（嵌套调用 wf-ipo-dd-full）
ls 04-文件输出/律师工作报告/*.docx 2>/dev/null
ls 04-文件输出/公开转让说明书法律相关章节-自查报告/ 2>/dev/null
ls 04-文件输出/*-内核后-*.docx 2>/dev/null
```

---

## 失败 / 跳过 / 回滚处理

依据 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认。

**特殊提示**：
- 阶段 3 失败时由子 workflow `wf-ipo-dd-full` 处理（17 章中某章 Memo 违约时按 `dd-output-schema.md § 7` 跳过 + 提示）；本 workflow 不重复处理
- 阶段 4 公开转让说明书法律章节自查发现重大问题——回到阶段 3 补充尽调
- 阶段 5（内核）失败 = 内核【必改】项未全部落实——回到阶段 4 修订

---

## 嵌套关系

本 workflow **嵌套调用**：

- `ecm-workflow:wf-ipo-dd-full`（在阶段 3 整段调用）

本 workflow **不被任何其他 workflow 嵌套**（顶层节点）。

---

## 端到端示例（脑内测试）

**场景：某科技公司挂牌创新层 + 后续考虑北交所**

```
用户："我们公司想挂牌新三板创新层，将来争取去北交所"

本 skill：
  项目类型识别：新三板挂牌（创新层；将来去北交所属于后续独立项目）
  阶段 1：建项目目录（项目类型 = 新三板挂牌）
  阶段 2：触发 `ecm-design:ipo-path`，论证：
    ☑ 创新层进入条件二选一（市值 + 营收增速 / 净利润 + 营收 / 净资产 + 净利润 等套餐）
    ☑ 北交所衔接条件（创新层挂牌满 12 个月 + 北交所发行条件）
    输出：路径论证备忘录
  阶段 3：**嵌套调用 `ecm-workflow:wf-ipo-dd-full`**（17 章尽调）+ dd-data-verify 核验
        创新层进入指标
  阶段 4：report-assembly + opinion-letter + meeting-docs（股改决议）+ disclosure-review
        （公开转让说明书法律相关章节）+ format-adjust
  阶段 5：四个 ecm-qc-* 全部触发
  阶段 6：全国股转公司反馈来时按需触发 ecm-research-* / disclosure-review
  
  挂牌完成后，"将来去北交所"由独立的 `wf-ipo-full` 项目（北交所首发）处理；
  本 workflow 终止于挂牌成功 + 持续督导阶段开始
```

**场景：客户已经在创新层，要去北交所**

```
用户："我们已经在创新层挂牌 18 个月了，准备去北交所"

本 skill 提示：
  您的需求是"创新层 → 北交所 IPO 衔接"——本质是北交所首发上市，
  请改用 `ecm-workflow:wf-ipo-full`（项目类型选 "IPO"，板块选 "北交所"）。
  本 workflow（wf-nto-listing）只覆盖"挂牌新三板"环节，不覆盖"从新三板转北交所首发"。
```

---

## 参考资料索引

本 skill 不自带 references/ 目录——所有参考资料由各原子 skill 自带，特别是：

- `ecm-design-ipo-path/references/pathway-rules.md`（含新三板基础层 / 创新层进入条件 + 北交所衔接路径速查）
- `ecm-draft-disclosure-review/references/disclosure-chapter-map.md`（含新三板《公开转让说明书》章节映射）

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
| 2026-04-25 | 初版。锁定 6 阶段编排 + 阶段 2 子类型识别（基础层 / 创新层 / 北交所衔接路径切换提示）+ 阶段 3 嵌套调用 wf-ipo-dd-full（新三板 ≈ IPO 尽调标准）+ 阶段 4 公开转让说明书法律相关章节自查 + 创新层指标核验追加 |
