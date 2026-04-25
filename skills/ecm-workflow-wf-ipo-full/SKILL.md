---
name: ecm-workflow-wf-ipo-full
description: >
  完整 IPO 项目工作流 Skill。从项目启动、路径选择、尽职调查、文书输出到内核审查的端到端编排，覆盖境内 A 股（主板 / 科创板 / 创业板 / 北交所）+ 港股 + 美股 + 红筹 / VIE 全场景。当用户提到以下场景时触发：新接 IPO 项目 / IPO 全流程 / 上市全流程 / 端到端 IPO / IPO kickoff / 完整 IPO 项目 / IPO 走一遍 / 帮我安排 IPO / IPO 工作流 / 上市工作流 / IPO 项目编排 / 上市项目编排 / 一个 IPO 项目从头做到尾。也包括用户已经决定要 IPO 但不知道从哪里开始、或者希望全流程指引下一步该做什么的场景。本 skill **不直接做任何具体业务**——它输出**6 阶段清单 + 下一步指引**，由用户在每个阶段实际触发对应原子 skill / 子 workflow（尽调阶段嵌套调用 wf-ipo-dd-full）。即使用户未明确说"workflow"或"全流程"，只要表达"我要做个 IPO""帮我接一个 IPO 项目"也应触发。
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
    - ecm-draft-report-assembly
    - ecm-draft-opinion-letter
    - ecm-draft-disclosure-review
    - ecm-draft-meeting-docs
    - ecm-draft-format-adjust
    - ecm-qc-opinion-letter-review
    - ecm-qc-work-report-review
    - ecm-qc-disclosure-review
    - ecm-qc-meeting-docs-review
    - ecm-research-case-search
    - ecm-research-reg-search
    - ecm-research-reg-study
---

# 完整 IPO 项目 工作流 Skill

## 定位与边界

本 skill **负责**：
- 为 IPO 项目（A 股主板 / 科创板 / 创业板 / 北交所；港股；美股；红筹 / VIE 回归）提供**端到端 6 阶段编排**：项目启动 → 方案设计 → 尽职调查 → 文书输出 → 内核审查 → 申报 / 反馈支持
- 在每个阶段完成后给出"下一步应调用的 skill"提示
- 在尽调阶段**嵌套调用** `ecm-workflow:wf-ipo-dd-full`（17 章尽调子工作流）

本 skill **不负责**：
- 任何具体业务工作（路径论证 / 17 章尽调 / 文书撰写 / 内核审查）——交给被编排的原子 skill 与子 workflow
- 改写或简化各原子 skill 的输出契约
- 自动化执行——本 skill 输出**阶段清单 + 提示**，由用户 / 项目组在每一步按需触发对应 skill

## 免责声明

本 skill 仅为 IPO 项目流程管理辅助工具，被嵌套触发的所有原子 skill 输出**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 与原子 skill 的边界

| 维度 | 各 `ecm-setup-*` / `ecm-design-*` / `ecm-dd-*` / `ecm-draft-*` / `ecm-qc-*` / `ecm-research-*` skill | `ecm-workflow:wf-ipo-full`（本 skill） |
|------|----------------------------------|-----------------------------|
| 角色 | "做事的人"——产出业务产物（项目目录 / 备忘录 / Memo / 文书 / 修订稿） | "总指挥官"——输出 6 阶段清单 + 进度提示 |
| 输出 | 业务产物（Markdown / DOCX / Excel） | 阶段清单 + 下一步指引（不落客户文件） |
| 触发频次 | 单点触发，一项任务一次调用 | 整个 IPO 项目周期内被反复参考 |
| 上下文使用 | 加载本任务所需的法规 / checklist / 模板 | 不加载具体业务上下文，只 reference 6 阶段编排和已有 SoT |
| 失败影响域 | 仅影响该步产物 | 失败不阻塞——用户随时可绕过本 workflow 直接调原子 skill |

⚠️ 防触发污染：
- 用户问"主板和科创板有什么区别"——触发 `ecm-design:ipo-path`，**不触发本 workflow**
- 用户问"股东核查需要哪些材料"——触发 `ecm-dd:dd-shareholders`
- 用户问"IPO 整个项目有哪些阶段"或"我要从头开始做一个 IPO 项目"——触发**本 workflow**

## 配置项

**项目类型识别**：本 workflow 默认场景为 IPO（含红筹回归 / 借壳上市的标的公司视角）。若用户实际是再融资 / 并购 / 跨境 / 新三板，请改用 `wf-issuance` / `wf-ma-full` / `wf-cross-border-ma` / `wf-nto-listing`。

**目标板块识别**：本 workflow 不强制阶段 1 之前确定板块——板块论证由阶段 2 的 `ecm-design:ipo-path` 完成。但若用户已明确板块（如 "做科创板"），workflow 在阶段 2 处直接传入该上下文。

**跳过策略（Skip Policy）**：
- `strict`：每个阶段必须完成才能进入下一阶段
- `loose`（默认）：阶段间允许"占位继续"（例如 IPO 路径备忘录初稿尚未完成时，可先触发部分尽调章节）
- 阶段 5（内核审查）**不可跳过**——任何 IPO 项目正式申报前都必须经内核

**回滚策略**：见 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4，本 skill 沿用默认。

---

## 阶段编排

### 阶段 1 — 项目启动

| 项 | 内容 |
|----|------|
| **目标** | 建立项目目录结构 + 客户文件分类归位 |
| **调用 skill**（按序）| `ecm-setup:project-init` → `ecm-setup:file-classify` → `ecm-setup:file-organize` |
| **阶段产物** | `{项目根}/` 目录树（按 `shared/templates/project-folder-structure.md`）+ `02-99-未分类文件/分类结果.md` + `02-NN-*/文件索引表.md` |
| **进入下一阶段判定** | 项目根目录已建立 + 至少 80% 客户文件已归位 |
| **可跳过** | 否（项目目录是后续所有阶段产物的落地基础） |

### 阶段 2 — 方案设计

| 项 | 内容 |
|----|------|
| **目标** | 论证并确定本 IPO 项目的板块路径（A 股主板 vs 科创板 vs 创业板 vs 北交所 vs 港股 vs 美股 vs 红筹 vs VIE） |
| **调用 skill** | `ecm-design:ipo-path`（核心；含 12 维度比较 + 三维影响分析）|
| **阶段产物** | `01-方案设计/IPO 路径选择备忘录-{YYYYMMDD}.md`（遵循 [`shared/templates/legal-memo-format.md`](../../shared/templates/legal-memo-format.md)） |
| **进入下一阶段判定** | 板块路径备忘录初稿完成 + 客户 / 项目组对目标板块达成共识（即使共识为"先开两条线并行准备"也可继续） |
| **可跳过** | 否（板块决定 dd-entity / dd-charter / dd-fundraising 等多个 DD skill 的核查口径） |

### 阶段 3 — 尽职调查（嵌套子 workflow）

| 项 | 内容 |
|----|------|
| **目标** | 按编报规则第 12 号完成 17 章尽调，每章产出 DD Memo |
| **调用 skill**（嵌套）| `ecm-workflow:wf-ipo-dd-full`（包含 17 个 `ecm-dd-*` 业务 skill + 2 个工具 skill；具体执行顺序、并行规则、独立性留最后的实务习惯由该子 workflow 锁定） |
| **阶段产物** | `02-尽职调查/02-NN-{章节}/DD-Memo-{章节}-{YYYYMMDD}.md`（17 份；遵循 [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md)） |
| **进入下一阶段判定** | 17 份 Memo 全部出具 + 每份"三、风险分级汇总"表已填 |
| **可跳过** | 否（IPO 必经环节） |

> **嵌套规则**（依据 `shared/templates/workflow-skill-template.md` § 6）：本 skill 在此阶段**只写一行 "调用 `ecm-workflow:wf-ipo-dd-full`"**，**不复制** 17 章清单。子 workflow 的进度由其阶段产物（Memo 是否齐备）独立判定。

### 阶段 4 — 文书输出

| 项 | 内容 |
|----|------|
| **目标** | 按 DD 结论拼接律师工作报告 + 起草法律意见书 + 准备申报相关会议文件 + 格式套版 |
| **调用 skill**（按序）| `ecm-draft:report-assembly`（按 dd-output-schema 拼接 17 份 Memo） → `ecm-draft:opinion-letter`（事实-核查-意见三步法 + 自动注入"特别事项提示"） → `ecm-draft:meeting-docs`（董事会 / 股东大会决议、申报议案）→ `ecm-draft:disclosure-review`（**起草人自查**信披文件法律相关章节）→ `ecm-draft:format-adjust`（最终套版）|
| **阶段产物** | `04-文件输出/律师工作报告/律师工作报告-{版本}-{YYYYMMDD}.docx`、`04-文件输出/法律意见书/法律意见书-{版本}-{YYYYMMDD}.docx`、`04-文件输出/会议文件/{会议名}-{文件类型}-{YYYYMMDD}.docx` |
| **进入下一阶段判定** | 律师工作报告 + 法律意见书初稿完成 + 起草人自查通过 |
| **可跳过** | 否；但子步骤 `ecm-draft:meeting-docs` 在 IPO 项目尚未到上会节点时可后置 |

### 阶段 5 — 内核审查（**强烈建议，不可跳过**）

| 项 | 内容 |
|----|------|
| **目标** | 项目组提交内核团队前的独立审查 |
| **调用 skill**（按序）| `ecm-qc:work-report-review`（律师工作报告） → `ecm-qc:opinion-letter-review`（法律意见书）→（如已起草信披章节）`ecm-qc:disclosure-review` →（如已起草股东大会 / 董事会议案）`ecm-qc:meeting-docs-review` |
| **阶段产物** | 带 tracked changes + comments 的 `.docx`（`w:author="内核"` 默认；用户可覆盖） |
| **进入下一阶段判定** | 内核意见已回到项目组 + 修订完毕 + 项目组对内核【必改】项已全部落实 |
| **可跳过** | **否**——任何 IPO 项目正式申报前都必须经内核 |

> **角色边界提示**：本阶段使用者是**内核 / QC 团队**（与项目组律师在身份上分离）。如果用户身份只是项目组律师，本 workflow 在此阶段会提示"内核环节由内核团队触发；项目组提交后请等内核反馈"。

### 阶段 6 — 申报 / 反馈支持（按需）

| 项 | 内容 |
|----|------|
| **目标** | 反馈回复起草、专项法律研究、新增议案文件 |
| **调用 skill**（按需）| `ecm-research:case-search`（类似 IPO 案例 / 监管处罚 / 上市委审议关注点）/ `ecm-research:reg-search`（最新法规 / 交易所规则）/ `ecm-research:reg-study`（重大法律问题深度研究）/ `ecm-draft:disclosure-review`（信披自查迭代）/ `ecm-draft:meeting-docs`（持续督导阶段股东会议案） |
| **阶段产物** | `06-反馈回复/{反馈批次}/{研究主题}-备忘录-{YYYYMMDD}.md`（遵循 [`shared/templates/research-output-format.md`](../../shared/templates/research-output-format.md)） |
| **进入下一阶段判定** | — |
| **可跳过** | 是（本阶段按申报推进节奏触发，IPO 申报前不强制执行） |

---

## skill 间数据传递契约

本 skill 不引入新数据契约；阶段间数据流完全靠**已经存在的 SoT**：

| 阶段衔接 | 依赖 SoT |
|---------|---------|
| 阶段 1 → 阶段 2 | `shared/templates/project-folder-structure.md`（项目目录里的 `02-NN-*/文件索引表.md` 由 file-organize 产出，被 ipo-path 用作"客户基础信息读取入口"） |
| 阶段 2 → 阶段 3 | `01-方案设计/IPO 路径选择备忘录.md`（ipo-path 输出）影响 `dd-entity` / `dd-charter` / `dd-fundraising` 的核查口径；通过项目目录传递，无需 workflow 维护中间状态 |
| 阶段 3 → 阶段 4 | `shared/schemas/dd-output-schema.md` § 4 / § 5（17 份 Memo 拼接顺序 / opinion-letter 消费规则）；report-assembly / opinion-letter 直接按契约消费 |
| 阶段 4 → 阶段 5 | `shared/templates/qc-skill-template.md`（4 个 ecm-qc-* skill 的统一工作流；自动从 `04-文件输出/` 读取项目组提交的文件） |
| 阶段 5 → 阶段 6 | 内核反馈意见纸质 / 电子件由项目组手工接收；无 workflow 中间状态 |

### 进度判断（无状态）

```bash
# 在项目根目录：
ls -d 01-方案设计/ 2>/dev/null && echo "阶段 2 已启动"
ls 02-尽职调查/02-*/DD-Memo-*.md 2>/dev/null | wc -l   # 17 表示阶段 3 完成
ls 04-文件输出/律师工作报告/*.docx 2>/dev/null         # 表示阶段 4 进行中或完成
ls 04-文件输出/*-内核后-*.docx 2>/dev/null             # 表示阶段 5 完成
```

---

## 失败 / 跳过 / 回滚处理

依据 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认。

**特殊提示**：
- 阶段 3（尽调）失败时，由子 workflow `wf-ipo-dd-full` 处理失败逻辑（17 章中某章 Memo 违约时按 `dd-output-schema.md § 7` 跳过 + 提示）；本 workflow 不重复处理
- 阶段 5（内核）失败 = 内核反馈【必改】项未全部落实——本 workflow 提示用户"回到阶段 4 修订相应文书后，重新触发对应 ecm-qc-* skill 复核"
- 任何阶段都允许用户**显式重跑**——本 workflow 不阻止；旧产物自动归档到 `05-底稿和附件/历史版本/`

---

## 嵌套关系

本 workflow **嵌套调用**：

- `ecm-workflow:wf-ipo-dd-full`（在阶段 3 整段调用）

本 workflow **不被任何其他 workflow 嵌套**（顶层节点）。

---

## 端到端示例（脑内测试）

**场景**：律师团队某天接到客户委托，"我们想做 A 股科创板 IPO"。

```
用户："新接一个客户，做科创板 IPO，从头开始安排"

本 skill 输出：
  阶段 1（启动）：
    立即调用 `ecm-setup:project-init`，建议参数：
      项目类型 = IPO；板块 = 科创板；境内/跨境 = 境内；客户简称 = ?（待用户确认）
    完成后调用 `ecm-setup:file-classify`、`ecm-setup:file-organize`

  阶段 2（设计）：
    调用 `ecm-design:ipo-path`，重点核对客户研发投入占比、营收增速、最近一期净利润等是否符合科创板属性

  阶段 3（尽调）：
    调用子 workflow `ecm-workflow:wf-ipo-dd-full`，按 17 章顺序产出 DD Memo
    （17 章细则由该子 workflow 自带，本 workflow 不展开）

  阶段 4（文书）：
    调用 `ecm-draft:report-assembly` → `opinion-letter` → `meeting-docs`（董事会决议）
    → `disclosure-review`（起草人自查招股书法律相关章节）→ `format-adjust`

  阶段 5（内核）：
    交给内核团队触发 `ecm-qc:work-report-review` / `ecm-qc:opinion-letter-review` / 
    `ecm-qc:disclosure-review` / `ecm-qc:meeting-docs-review`

  阶段 6（申报支持，按需）：
    收到交易所反馈后，调用 `ecm-research:case-search` 检索类似审核问询案例

  下一步：先告诉我客户简称，我去触发 `ecm-setup:project-init`

用户：（提供简称）"某某科技"
本 skill：（触发 `ecm-setup:project-init`，进入阶段 1）
...

中途用户："尽调走到第 8 章，先看看类似案例"
本 skill：
  当前进度：阶段 3，子 workflow wf-ipo-dd-full 进度 7/17
  允许跨阶段触发 `ecm-research:case-search`（research 类 skill 全程可用）
  完成研究后回到阶段 3 继续

最终用户："17 章尽调完了，开始拼报告"
本 skill：
  ✅ 阶段 3 完成（子 workflow 报告 17/17）
  下一步：触发 `ecm-draft:report-assembly`，预计产出《律师工作报告》初稿
  并行可触发 `ecm-draft:opinion-letter`（两者都消费 dd-output-schema）
```

---

## 参考资料索引

本 skill 不自带 references/ 目录——所有参考资料由各原子 skill 自带。

跨 skill SoT 引用：

- [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md)（本 skill 编写所遵循的骨架模板）
- [`shared/templates/project-folder-structure.md`](../../shared/templates/project-folder-structure.md)（阶段产物落地路径）
- [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md)（阶段 3 → 阶段 4 数据交接）
- [`shared/templates/work-report-format.md`](../../shared/templates/work-report-format.md) / [`legal-opinion-format.md`](../../shared/templates/legal-opinion-format.md) / [`legal-memo-format.md`](../../shared/templates/legal-memo-format.md) / [`meeting-docs-format.md`](../../shared/templates/meeting-docs-format.md) / [`research-output-format.md`](../../shared/templates/research-output-format.md)（各类输出格式 SoT）
- [`shared/templates/qc-skill-template.md`](../../shared/templates/qc-skill-template.md)（阶段 5 内核 skill 工作流参考）

---

## 版本

| 日期 | 变更 |
|------|------|
| 2026-04-25 | 初版（BATCH-10）。锁定 6 阶段编排（启动 / 设计 / 尽调 / 文书 / 内核 / 申报）+ 阶段 3 嵌套调用 wf-ipo-dd-full（不复制 17 章）+ 阶段 5 不可跳过 + 阶段 6 按需 + 内核环节角色边界提示 |
