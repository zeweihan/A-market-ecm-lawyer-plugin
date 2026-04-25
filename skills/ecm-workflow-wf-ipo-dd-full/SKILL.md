---
name: ecm-workflow-wf-ipo-dd-full
description: >
  完整 IPO 尽职调查工作流 Skill。按编报规则第 12 号顺序串联 17 个业务性 ecm-dd-* skill + 2 个工具类 dd-data-verify / dd-file-review，提供"从批准授权到其他合规事项"端到端尽调指引。当用户提到以下场景时触发：完整 IPO 尽调 / 17 章尽调 / 全套尽职调查 / 编报规则 12 号尽调 / 上市尽调全流程 / IPO due diligence / 走一遍尽调 / 帮我把尽调过一遍 / 尽调 checklist 全过一遍 / 尽调编排 / 尽调工作流。也包括用户已经在跑某个 IPO 项目、希望按部就班完成 17 章尽调，或希望由本 skill 提示"上一章完成了，下一章应调用什么"的场景。本 skill **不直接做尽调**——它输出**阶段清单和下一步指引**，由用户在每章实际触发对应 ecm-dd-* skill。即使用户未明确说"完整尽调"，只要表达"把尽调全过一遍""按编报规则 12 号顺序走"，也应触发。本 skill 是叶节点 workflow，被 wf-ipo-full / wf-nto-listing 嵌套调用。
version: 0.1.0
license: MIT
module: ecm-workflow
user_role: 项目组律师
phase:
  - 尽调阶段
  - 申报阶段
category:
  - 工作流编排
depends_on:
  internal_skills:
    - ecm-dd-approval
    - ecm-dd-entity
    - ecm-dd-establishment
    - ecm-dd-independence
    - ecm-dd-shareholders
    - ecm-dd-history
    - ecm-dd-business
    - ecm-dd-related-party
    - ecm-dd-assets
    - ecm-dd-debt
    - ecm-dd-charter
    - ecm-dd-directors
    - ecm-dd-tax
    - ecm-dd-environment
    - ecm-dd-fundraising
    - ecm-dd-litigation
    - ecm-dd-compliance
    - ecm-dd-data-verify
    - ecm-dd-file-review
---

# 完整 IPO 尽职调查 工作流 Skill

## 定位与边界

本 skill **负责**：
- 按《编报规则第 12 号》（2001）的章节顺序，提供 IPO 尽调 17 章的**编排指引**
- 在每章完成后提示"下一章应调用 `ecm-dd:<...>`"，给出建议执行顺序
- 在尽调完成后提示进入 `ecm-draft:report-assembly`（拼接报告）/ `ecm-draft:opinion-letter`（起草意见书）

本 skill **不负责**：
- 任何具体章节的尽调实质工作（17 章每一章交给对应 `ecm-dd-*` skill；本 skill 不重复 checklist）
- 改写或简化各 DD skill 的输出契约（17 份 Memo 必须遵循 [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) 五段式骨架，本 skill 不得自行精简）
- 项目启动 / 文件归位（前置由 `ecm-setup:project-init` / `ecm-setup:file-classify` / `ecm-setup:file-organize` 完成）
- 文书输出（后续交给 `ecm-draft:*`）和内核审查（交给 `ecm-qc:*`）

## 免责声明

本 skill 仅为 IPO 尽调流程管理辅助工具，被嵌套触发的 17 个 DD skill 输出**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 与原子 skill 的边界

| 维度 | 17 个 `ecm-dd-*` 业务性 skill | `ecm-workflow:wf-ipo-dd-full`（本 skill） |
|------|----------------------------|-----------------------------|
| 角色 | "做事的人"——出 17 份 DD Memo | "指挥官"——按编报规则第 12 号顺序提示用户走完 17 章 |
| 输出 | DD Memo（Markdown，五段式，落到 `02-尽职调查/02-NN-*/`） | 阶段清单 / 进度提示文本（不落客户文件） |
| 触发频次 | 每章 1 次（17 次累计触发） | 整个尽调期内反复参考（"我做到第几章了，下一章是什么"） |
| 上下文使用 | 加载本章的法规节选 / checklist / 客户文件 | 不加载具体章节上下文，只 reference 17 章顺序 |
| 失败影响域 | 本章 Memo 不可用 | 失败不阻塞——用户可绕过本 workflow 直接调任意一个 `ecm-dd-*` skill |

⚠️ 防触发污染：如果用户问"我这个项目股东穿透到 PE 一层就停吗""股东核查要做哪些工作"——这是**单章实质问题**，触发 `ecm-dd-shareholders` 而**非**本 workflow。

## 配置项

**项目类型识别**：本 skill 默认目标场景为 IPO（含主板 / 科创板 / 创业板 / 北交所 / 港股的境内尽调；红筹回归 / 借壳上市的标的公司尽调）。如项目类型为再融资 / 并购 / 跨境 / 新三板，请改用 `wf-issuance` / `wf-ma-full` / `wf-cross-border-ma` / `wf-nto-listing`。

**尽调子集（Subset）**：默认调用全 17 章；如用户明确"只做 X 章 / 不做 X 章"（例如已完成可不重复），workflow 在阶段清单里给"⤵ 已跳过"标记。但 `ecm-dd-independence` 是横向 skill，依赖 5 个上游 DD skill 的输出，**不得**在 `dd-related-party` / `dd-directors` / `dd-assets` / `dd-business` / `dd-debt` 都缺失的情况下单独跑。

**跳过策略（Skip Policy）**：
- `strict`：每章必须完成才能继续（适合冲刺申报阶段）
- `loose`（默认）：缺资料的章节标"待补"继续，最后给"未完成清单"

**回滚策略**：见 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4，本 skill 沿用默认（不删客户文件、历史版本归档、配置回滚 ≠ 数据回滚）。

---

## 阶段编排

本 skill 是**单阶段 workflow**——只覆盖"尽职调查"一个阶段（即整体六阶段编排里的阶段 3）。前置阶段（启动 / 设计）和后续阶段（文书 / 内核 / 申报）由父 workflow（`wf-ipo-full` / `wf-nto-listing`）或用户显式触发。

### 阶段 3 — 尽职调查（17 章 + 2 工具）

| 项 | 内容 |
|----|------|
| **目标** | 按编报规则第 12 号顺序完成 17 章核查；每章产出一份符合 `dd-output-schema.md` 的 DD Memo |
| **阶段产物** | `{项目根}/02-尽职调查/02-NN-{章节名}/DD-Memo-{章节名}-{YYYYMMDD}.md`（17 份；横向 skill `dd-independence` 落 `02-04-独立性/`） |
| **进入下一阶段** | 17 份 Memo 全部出具，且每份的"三、风险分级汇总"表已填 |

### 推荐执行顺序

按编报规则第 12 号原文章节顺序，但根据**章节间依赖关系**做了实务习惯调整（独立性放在主体资格之后但实质评估**留到全部其他章节完成后做最后一遍**）：

| 顺序 | skill | 编报规则章节 | 目录 | Memo 文件名锚 |
|----:|-------|-------------|------|--------------|
| 1 | `ecm-dd:dd-approval` | 第 1 章 本次交易的批准和授权 | `02-01-批准和授权/` | `批准和授权` |
| 2 | `ecm-dd:dd-entity` | 第 2 章 发行人主体资格 | `02-02-主体资格/` | `主体资格` |
| 3 | `ecm-dd:dd-establishment` | 第 3 章 发行人设立 | `02-03-历史沿革/` | `设立` |
| 4 | `ecm-dd:dd-shareholders` | 第 5 章 发起人和主要股东（含实控人） | `02-05-股东及实控人/` | `股东及实控人` |
| 5 | `ecm-dd:dd-history` | 第 6 章 股本及其演变 | `02-03-历史沿革/` | `历史沿革` |
| 6 | `ecm-dd:dd-business` | 第 7 章 发行人业务 | `02-06-业务资质/` | `业务` |
| 7 | `ecm-dd:dd-related-party` | 第 8 章 关联交易和同业竞争 | `02-07-关联交易与同业竞争/` | `关联交易与同业竞争` |
| 8 | `ecm-dd:dd-assets` | 第 9 章 主要财产 | `02-08-主要财产/` | `主要财产` |
| 9 | `ecm-dd:dd-debt` | 第 10 章 重大债权债务 | `02-09-重大债权债务/` | `重大债权债务` |
| 10 | `ecm-dd:dd-charter` | 第 11 章 公司章程及组织机构 | `02-10-公司治理/` | `公司章程与治理` |
| 11 | `ecm-dd:dd-directors` | 第 12 章 董监高 | `02-11-董监高/` | `董监高` |
| 12 | `ecm-dd:dd-tax` | 第 13 章 税务 | `02-12-税务/` | `税务` |
| 13 | `ecm-dd:dd-environment` | 第 14 章 环境保护、产品质量、安全生产 | `02-13-环保与安全生产/` | `环保与安全生产` |
| 14 | `ecm-dd:dd-fundraising` | 第 15 章 募集资金运用 | `02-14-募集资金运用/` | `募集资金运用` |
| 15 | `ecm-dd:dd-litigation` | 第 16 章 诉讼、仲裁、行政处罚 | `02-15-诉讼仲裁处罚/` | `诉讼仲裁处罚` |
| 16 | `ecm-dd:dd-compliance` | 第 17 章 其他合规事项（兜底） | `02-16-其他合规事项/` | `其他合规事项` |
| 17 | `ecm-dd:dd-independence` | 第 4 章 发行人独立性（横向 skill，**实务上最后跑**） | `02-04-独立性/` | `独立性` |

> **为何把独立性挪到最后**：`dd-independence` 是综合评估 skill，按 `shared/schemas/dd-output-schema.md` § 3 的"五独立对照评估表 + 独立性重大依赖汇总表"消费 `dd-related-party` / `dd-directors` / `dd-assets` / `dd-business` / `dd-debt` 五个上游 Memo 的字段。提前跑会导致"五独立"评估有空白格——按编报规则原序号是第 4 章，但实务执行序号是第 17 章。Memo 写明"对应编报规则第 4 章"即可。

### 工具类 skill（按需穿插，不入主序列）

| skill | 何时调用 |
|-------|---------|
| `ecm-dd:dd-data-verify` | 在主体资格 / 股东 / 历史沿革 / 主要财产 / 董监高 等高数据密度章节前，先跑一遍工商 + 财务数据自动比对（节省 manual 比对工时） |
| `ecm-dd:dd-file-review` | 项目文件量大（>50 份 PDF / Word / Excel）时，先批量提取关键字段供各 DD skill 引用 |

### 同章节并行触发

`dd-establishment`（第 3 章）和 `dd-history`（第 6 章）共用 `02-03-历史沿革/` 目录，**Memo 名不冲突**（一个 `DD-Memo-设立-{date}.md`、一个 `DD-Memo-历史沿革-{date}.md`）。可在尽调阶段早期并行起草。

类似可并行：`dd-tax` / `dd-environment` / `dd-fundraising` / `dd-litigation` / `dd-compliance`（第 13-17 章合规事项簇）——彼此无依赖，团队多人时可分头跑。

---

## skill 间数据传递契约

本 skill 输出阶段清单 + 进度文本，自身不维护任何状态文件。它依赖**已经存在的两个 SoT** 让上下游对齐：

| 契约 SoT | 引用方式 |
|---------|---------|
| [`shared/templates/project-folder-structure.md`](../../shared/templates/project-folder-structure.md) | 17 份 Memo 的落地路径模式 |
| [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md) | 17 份 Memo 的五段式骨架、风险级别枚举、风险汇总表列定义；下游 `ecm-draft:report-assembly` / `opinion-letter` 据此消费 |

### 进度判断

workflow 不需要状态文件——直接 `ls` 项目目录即可知道走到哪一步：

```bash
# 在项目根目录：
ls 02-尽职调查/02-*/DD-Memo-*.md 2>/dev/null | wc -l
# 应得到 17（或 0-17 之间的当前进度）
```

阶段清单里**显示**类似：

```
阶段 3 进度（13/17）：
  ✅ 02-01-批准和授权/DD-Memo-批准和授权-20260420.md
  ✅ 02-02-主体资格/DD-Memo-主体资格-20260420.md
  ...
  ⛔ 02-13-环保与安全生产/  尚未出具
  ⛔ 02-15-诉讼仲裁处罚/    尚未出具
  ⤵ 02-16-其他合规事项/    已跳过：用户确认本项目无 17 章兜底事项
  ⛔ 02-04-独立性/         待 5 个上游章节完成后触发
下一步建议：调用 `ecm-dd:dd-environment`
```

---

## 失败 / 跳过 / 回滚处理

### 失败

某 DD skill 触发后未返回 Memo（用户中断 / 客户资料缺失 / 外部 API 不通）：本 workflow 在阶段清单里标 `⛔ 失败: <原因>`，**strict 模式停下来追问"是否补资料后重跑该章"**；**loose 模式继续往后推但记入"未完成清单"**。

某 DD skill 返回的 Memo 不符合 `dd-output-schema.md`（缺段 / 表头列名不对 / 级别取值超枚举）：本 workflow **不自行修复**——按 `dd-output-schema.md § 7` 把该违约 Memo 标记，提示"重跑该 skill 或手动按契约修订"。

### 跳过

允许跳过的章节：

- 第 14 章 募集资金运用（**仅 IPO 必填**；本场景不跳）
- 第 17 章 其他合规事项（兜底章；如用户明确"无社保 / 公积金 / 海关 / 外汇 / 劳动等其他事项"可跳，但默认不跳）

不允许跳过：第 1 章（批准和授权）、第 2 章（主体资格）、第 5 章（股东实控人）、第 11 章（公司章程及治理）、第 12 章（董监高）——这些是上市基本盘。

### 回滚

依据 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4：本 workflow 不删客户文件；用户重跑某章时旧 Memo 自动归档到 `05-底稿和附件/历史版本/`。

---

## 嵌套关系

本 workflow 是**叶节点**，被以下父 workflow 嵌套调用：

- `ecm-workflow:wf-ipo-full`（IPO 全流程的"阶段 3 尽调"内嵌本 skill）
- `ecm-workflow:wf-nto-listing`（新三板挂牌的"阶段 3 尽调"内嵌本 skill；新三板尽调标准与 IPO 高度重合，复用本编排）

**本 workflow 不嵌套任何其他 workflow**（避免双向嵌套）。

如果父 workflow 已嵌套本 skill，则父 workflow 的 SKILL.md 在阶段 3 处只写一行 "调用 `ecm-workflow:wf-ipo-dd-full`"，**不复制 17 章清单**。

---

## 端到端示例（脑内测试）

**场景**：某 A 股科创板 IPO 项目，客户 "某某科技"，已完成项目启动（项目根 `./ECM-某某科技/` 已建）和文件归位，现在进入尽调阶段。

```
用户："开始尽调"
本 skill：
  当前进度：0/17
  推荐顺序：第 1 章 批准和授权 → 第 2 章 主体资格 → ... → 第 4 章 独立性（最后跑）
  下一步：请触发 `ecm-dd:dd-approval`，把董事会 / 股东会决议、外部批文（国资 / 发改 / 商务 / 反垄断）整理后投喂给该 skill
  预计该 skill 产出 `02-01-批准和授权/DD-Memo-批准和授权-{今天}.md`

用户：（触发 dd-approval，完成第 1 章 Memo）

用户："下一章"
本 skill：
  当前进度：1/17
  下一步：请触发 `ecm-dd:dd-entity`
  ...

用户："第 7 章和第 13 章 我团队两个人分头跑"
本 skill：
  ✅ 业务（第 7 章）和 税务（第 13 章）无依赖，可并行
  注意：业务做完后，关联交易（第 8 章）会用到业务清单——建议第 7 章先于第 8 章
  分头跑两份 Memo 都符合契约即可，本 workflow 等两份齐了再继续

用户："17 章都跑完了"
本 skill：
  当前进度：17/17 ✅
  下一步：进入阶段 4 文书输出，先触发 `ecm-draft:report-assembly`（按 dd-output-schema 拼接 17 份 Memo 成《律师工作报告》）
  随后 `ecm-draft:opinion-letter`（自动注入"特别事项提示"段）
  本 workflow（wf-ipo-dd-full）已完成；如全流程则回到 `wf-ipo-full` 继续阶段 4
```

---

## 参考资料索引

本 skill 不自带 references/ 目录——所有参考资料由各 `ecm-dd-*` skill 自带（每个 DD skill 有 `references/checklist.md` 和 `references/regulations-index.md`）。

跨 skill SoT 引用：

- [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md)（本 skill 编写所遵循的骨架模板）
- [`shared/schemas/dd-output-schema.md`](../../shared/schemas/dd-output-schema.md)（17 份 Memo 的统一契约）
- [`shared/templates/project-folder-structure.md`](../../shared/templates/project-folder-structure.md)（项目目录 + Memo 落地路径）
- [`shared/regulations/编报规则第12号-2001.md`](../../shared/regulations/编报规则第12号-2001.md)（17 章原始章节顺序）

---

## 版本

| 日期 | 变更 |
|------|------|
| 2026-04-25 | 初版（BATCH-10）。锁定 17 章执行顺序（含独立性留最后的实务习惯）+ 2 个工具 skill 穿插规则 + 同章节并行触发规则 + 父 workflow 嵌套规则（被 wf-ipo-full / wf-nto-listing 调用） |
