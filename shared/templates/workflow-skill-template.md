---
文件类型: ecm-workflow 编排层 skill 统一模板
维护者: BATCH-10 建立（ecm-workflow 系列）
被哪些 skill 引用:
  - ecm-workflow-wf-ipo-full
  - ecm-workflow-wf-ipo-dd-full
  - ecm-workflow-wf-ma-full
  - ecm-workflow-wf-cross-border-ma
  - ecm-workflow-wf-issuance
  - ecm-workflow-wf-nto-listing
本版编制日期: 2026-04-25
version: 0.1.0
---

# ecm-workflow 编排层 skill 统一模板（Single Source of Truth）

本文件是 `ecm-workflow-wf-*` 系列 skill 的**骨架模板**。本仓库内所有"工作流编排"类 skill 必须复用本模板的结构、步骤序列 schema、skill 间数据传递契约、失败 / 跳过 / 回滚处理与原子 skill 的边界声明；不得在各自 SKILL.md 里另立一套。

**本模板适用范围**：
- ✅ 编排层 skill：本身**不做业务逻辑**，只负责**有序触发**其他 skill 的工作流（IPO 全流程 / 并购全流程 / 再融资 / 跨境 / 新三板等）
- ❌ 不适用于原子 skill（`ecm-setup-*` / `ecm-design-*` / `ecm-dd-*` / `ecm-draft-*` / `ecm-research-*` / `ecm-qc-*`）——这些是"做事的人"，而 workflow 是"指挥官"
- ❌ 不适用于工具型组合（如批量数据比对脚本）——那是 `ecm-dd-*` 工具类 skill 的范畴

---

## 一、SKILL.md frontmatter 规范

```yaml
---
name: ecm-workflow-wf-<function>
description: >
  一段触发关键词密集的中文描述，必须包含：
  （1）覆盖业务场景（IPO 项目 / 并购 / 跨境 / 再融资 / 新三板等）的全部同义词；
  （2）触发动词（启动项目 / 全流程 / 端到端 / 走一遍 / kickoff / 完整流程 / 工作流 / 编排）；
  （3）与原子 skill 的触发语区分（如 ecm-setup:project-init 仅做"建文件夹"；workflow 是"建文件夹 → 路径选择 → 尽调 → 文书 → 内核"全程指引）；
  （4）输出形式（**输出阶段清单 + 下一步指引**，不直接产生底稿 / 文书）；
  （5）即使用户只说"我要做个 IPO 项目"或"客户要并购了，从头到尾给我安排一下"也应触发。
version: 0.1.0
license: MIT
module: ecm-workflow
user_role: 项目组律师
phase:
  # workflow 通常贯穿全部阶段；按主导阶段勾选，最少含"启动阶段"
  - 启动阶段
  - 研究阶段
  - 尽调阶段
  - 申报阶段
  - 反馈阶段     # 可选，按 workflow 是否覆盖反馈阶段决定
category:
  - 工作流编排
depends_on:
  internal_skills:
    # 列出本 workflow 会触发的所有原子 skill（连字符形式，与目录名一致）
    - ecm-setup-project-init
    - ecm-setup-file-classify
    - ecm-setup-file-organize
    # ... 按本 workflow 的实际编排清单列全
  external_skills:
    # workflow 本身不直接调用外部 skill；外部依赖由被嵌套的原子 skill 自行声明。
    # 仅当本 workflow 需要在阶段交接处直接用 docx/pdf/xlsx 时才在此列出。
---
```

**命名**：目录 `ecm-workflow-wf-<function>`（kebab-case），文档引用 `ecm-workflow:wf-<function>`（冒号形式）。

**`wf-` 前缀强制**：所有 ecm-workflow skill 的 function 段都以 `wf-` 开头（workflow 的缩写），便于人类一眼分辨"这是编排层而非原子层"。

---

## 二、SKILL.md 正文骨架（硬性）

```markdown
# <业务场景中文名> 工作流 Skill

## 定位与边界

本 skill **负责**：
- 为 <业务场景> 项目提供**端到端的阶段编排**：从项目启动到文书输出的全流程指引
- **触发并按顺序串联**本仓库已存在的原子 skill（不重新实现业务逻辑）
- 在每个阶段完成后给出"下一步应调用的 skill"提示，并沉淀阶段产物的存放位置约定

本 skill **不负责**：
- 任何具体的业务工作（路径论证 / 尽调 / 文书撰写 / 内核审查）——交给被编排的原子 skill
- 改写或干涉被嵌套 skill 的输出契约（如 DD Memo 五段式骨架由 `shared/schemas/dd-output-schema.md` 锁定，workflow 不得自行简化）
- 自动化执行（不会自己跑一遍流程；workflow 输出的是**阶段清单 + 提示**，由用户 / 项目组在每一步按需触发对应 skill）

## 免责声明

本 skill 输出的工作流仅为项目流程管理辅助工具，被嵌套的原子 skill 输出**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 配置项

**项目类型识别（如适用）**
- 工作流可能存在场景变体（如 wf-issuance 区分 定增 / 配股 / 可转债；wf-nto-listing 区分 一般挂牌 / 创新层 / 拟北交所）
- 如未指定，先调用 `ecm-setup:project-init` 收集，再回到本 workflow

**跳过策略（Skip Policy）**
- `strict`：每一步必须完成才能进入下一步；中途缺数据时停下来追问
- `loose`（默认）：阶段间允许"占位继续"；缺失数据写入"未完成清单"，但不阻塞流程

**回滚策略（Rollback Policy）**
- 默认**不回滚已落地的客户数据**（项目目录、文件归位结果、已生成 Memo）
- 仅允许用户通过显式重跑某个原子 skill 来覆盖输出（例：重跑 `ecm-dd-shareholders` 会覆盖最新 Memo，但不删历史版本）
- 历史版本归档到 `05-底稿和附件/历史版本/`（见 `shared/templates/project-folder-structure.md`）

---

## 阶段编排（Stage Schema）

本 skill 的阶段编排遵循统一 schema：每个阶段含 **阶段名 / 目标 / 调用 skill 清单 / 阶段产物 / 进入下一阶段的判定**。

### 阶段 1 — 项目启动

| 项 | 内容 |
|----|------|
| **目标** | 建立项目目录结构 + 客户文件分类归位 |
| **调用 skill**（按序）| `ecm-setup:project-init` → `ecm-setup:file-classify` → `ecm-setup:file-organize` |
| **阶段产物** | `{项目根}/` 目录树 + `02-99-未分类文件/分类结果.md` + `02-NN-*/文件索引表.md` |
| **进入下一阶段** | 项目根目录已建立 + 至少 80% 客户文件已归位 |

### 阶段 2 — 方案设计

| 项 | 内容 |
|----|------|
| **目标** | 论证 / 确定本项目的核心交易结构 |
| **调用 skill**（按序）| 依本 workflow 业务场景而异 |
| **阶段产物** | `01-方案设计/` 下的法律备忘录（遵循 `shared/templates/legal-memo-format.md`） |
| **进入下一阶段** | 备忘录初稿完成 + 客户 / 项目组对核心结构有共识 |

### 阶段 3 — 尽职调查

| 项 | 内容 |
|----|------|
| **目标** | 按编报规则第 12 号完成 17 章 / 选定子集的尽调 |
| **调用 skill**（按序 / 嵌套）| **优先嵌套 `ecm-workflow:wf-ipo-dd-full`**（IPO / 新三板等全套场景），或显式列出本 workflow 需要的 DD skill 子集（再融资 / 并购等定向场景） |
| **阶段产物** | `02-尽职调查/02-NN-*/DD-Memo-*.md`（17 份或子集；遵循 `shared/schemas/dd-output-schema.md`） |
| **进入下一阶段** | 全部 DD Memo 出具完毕 + 高风险事项已与项目组对齐处置方向 |

### 阶段 4 — 文书输出

| 项 | 内容 |
|----|------|
| **目标** | 按 DD 结论拼接律师工作报告 + 起草法律意见书 + 整理会议文件 + 格式套版 |
| **调用 skill**（按序）| `ecm-draft:report-assembly` → `ecm-draft:opinion-letter` →（按需）`ecm-draft:meeting-docs` → `ecm-draft:format-adjust` |
| **阶段产物** | `04-文件输出/律师工作报告/` / `04-文件输出/法律意见书/` / `04-文件输出/会议文件/`（最终 .docx） |
| **进入下一阶段** | 起草人自查（`ecm-draft:disclosure-review`）已过 / 已记录 |

### 阶段 5 — 内核审查（**强烈建议**，非可选）

| 项 | 内容 |
|----|------|
| **目标** | 项目组提交内核团队前的独立审查 |
| **调用 skill**（按序）| `ecm-qc:opinion-letter-review` / `ecm-qc:work-report-review` / `ecm-qc:meeting-docs-review` /（如涉及信披）`ecm-qc:disclosure-review` /（如涉及股东大会见证）`ecm-qc:shareholders-meeting-witness` |
| **阶段产物** | 带 tracked changes + comments 的 `.docx`（`w:author="内核"` 默认） |
| **进入下一阶段** | 内核意见已回到项目组 + 修订完毕 |

### 阶段 6 — 申报 / 持续督导支持（按需）

| 项 | 内容 |
|----|------|
| **目标** | 反馈回复 / 法规与案例检索 / 后续会议文件起草 |
| **调用 skill**（按需）| `ecm-research:case-search` / `ecm-research:reg-search` / `ecm-research:reg-study` / `ecm-draft:disclosure-review`（继续起草人自查迭代） |
| **阶段产物** | `06-反馈回复/` 下的研究备忘录 / 反馈回复初稿 |
| **进入下一阶段** | — |

> 各 workflow 可在本骨架基础上**精简或替换某个阶段**（如 `wf-ipo-dd-full` 仅含阶段 3；`wf-issuance` 不含阶段 5 之外的部分流程），但**不得新增**未经此 schema 定义的阶段类别——遇到新场景应推动本模板升级而不是单点扩展。

---

## 三、skill 间数据传递契约

workflow 不直接处理业务数据；它依赖**已经存在的两个 SoT** 让上下游 skill 自动对话：

| 契约 SoT | 路径 | 用途 |
|---------|------|------|
| 项目目录结构 | [`shared/templates/project-folder-structure.md`](../templates/project-folder-structure.md) | 定义 `{项目根}/01-方案设计/` / `02-尽职调查/02-NN-*/` / `04-文件输出/` 等子目录；workflow 各阶段产物**必须落到这些目录**，下游 skill 才能稳定找到上游产物 |
| DD → Draft 数据交接契约 | [`shared/schemas/dd-output-schema.md`](../schemas/dd-output-schema.md) | 17 份 DD Memo 的统一结构、五段式二级标题、风险级别枚举（`高 / 中 / 低`）、风险汇总表 5 列定义、Memo 落地路径模式；workflow 在阶段 3 / 4 之间的数据交接**完全靠这份契约** |

### 阶段间数据流（以 IPO 全流程为例）

```
阶段 1 产物 → 阶段 2 输入：
  - {项目根}/02-NN-*/文件索引表.md（file-organize 产出）→ ipo-path 用作"客户基础信息读取入口"

阶段 2 产物 → 阶段 3 输入：
  - {项目根}/01-方案设计/IPO 路径选择备忘录.md（ipo-path 产出）→ DD skill 用作"目标板块识别"，影响 dd-entity / dd-charter 的部分核查口径

阶段 3 产物 → 阶段 4 输入（由 dd-output-schema 锁定）：
  - {项目根}/02-尽职调查/02-NN-*/DD-Memo-*-{YYYYMMDD}.md（17 份）
  - report-assembly 按 dd-output-schema § 4 拼接顺序读取
  - opinion-letter 按 dd-output-schema § 5 抽取"级别 = 高"事项注入"特别事项提示"

阶段 4 产物 → 阶段 5 输入：
  - {项目根}/04-文件输出/律师工作报告/律师工作报告-{版本}-{YYYYMMDD}.docx
  - ecm-qc:work-report-review 按 shared/templates/qc-skill-template.md 锁定的"参考坐标 + 五步工作流"做内核审查
```

### workflow 自身**不引入**新数据契约

- 不要在 workflow 的 SKILL.md 里定义"workflow 状态机字段""阶段流转日志格式"等**新结构化字段**
- 阶段间状态由"客户项目目录里有没有该产物"自然表达（`ls` 项目目录即可知道走到哪一步），无需中央化的 workflow 状态文件
- 这条原则保证 workflow 是**无状态指挥官**，便于多 workflow 嵌套（例：`wf-nto-listing` 可以无缝嵌套 `wf-ipo-dd-full`，因为两者都不维护私有状态）

---

## 四、失败 / 跳过 / 回滚处理

### 失败处理

| 失败类型 | 处理方式 |
|---------|---------|
| 某原子 skill 触发后**未返回输出**（用户中断 / 外部依赖缺失） | workflow 在阶段清单里标 `⛔ 失败`，提示用户"请查看 [skill 名] 的失败原因；本阶段必须完成才能进入下一阶段（strict 模式）/ 可标占位继续（loose 模式）" |
| 某原子 skill **返回的输出违约**（如 DD Memo 不符合 dd-output-schema） | 不自行修复；按 `dd-output-schema.md § 7` 处理：把该违约 Memo 整体跳过，在 workflow 阶段清单里附"违约提示 + 推荐重跑命令" |
| 多个原子 skill **触发顺序冲突**（用户在阶段 2 之前就直接调阶段 4） | workflow 提示"按当前项目目录推断你跳过了 [阶段名]；继续或回到 [前置阶段]？" |

### 跳过处理

某些 workflow 允许阶段跳过（见各 SKILL.md "阶段编排"段的"是否可跳过"列）：

- 一般规则：**阶段 5（内核审查）不可跳过**；阶段 4（文书输出）的子阶段可视项目类型跳过（再融资可能不需要 `meeting-docs`）；阶段 6（申报支持）整体可选
- 跳过时 workflow 在阶段清单里加 `⤵ 已跳过：<原因>`，便于事后回溯

### 回滚处理

workflow **不主动回滚已落地的客户数据**。三条硬规则：

1. **不删客户文件**：项目目录里的客户原件、归位结果、已生成 Memo 一律保留
2. **历史版本归档**：用户重跑某个 DD skill 时，原有 Memo 会被新版本覆盖，但 workflow 提示"老版本已自动归档到 `05-底稿和附件/历史版本/DD-Memo-xxx-{YYYYMMDD}-vN.md`"
3. **配置回滚 ≠ 数据回滚**：workflow 配置项（跳过策略 / 严格度）的变更只影响**后续**阶段的判定，不追溯重写已有产物

---

## 五、与原子 skill 的边界（强制声明）

每个 ecm-workflow skill 必须含一节"与原子 skill 的边界"，至少说明 5 项区别：

| 维度 | 原子 skill（`ecm-setup-*` / `ecm-design-*` / `ecm-dd-*` / `ecm-draft-*` / `ecm-research-*` / `ecm-qc-*`）| workflow skill（`ecm-workflow-*`） |
|------|----------------------------------|-----------------------------|
| 角色 | "做事的人"——产生具体业务产物（备忘录 / Memo / 文书 / 修订稿） | "指挥官"——产生**阶段清单 + 下一步指引**，自身不产业务产物 |
| 输出 | 业务产物（Markdown / DOCX / Excel 等） | 阶段清单 / 流程图 / 提示文本（不落客户文件） |
| 触发频次 | 单点触发，一项任务一次调用 | 整个项目周期内被反复参考（"我现在走到哪一步了"） |
| 上下文使用 | 只加载本任务所需上下文 | 不加载具体业务上下文，只 reference 本仓库的 skill 清单 + 项目目录结构 |
| 失败影响域 | 仅影响该步产物 | 失败不阻塞其他原子 skill 的独立调用——用户随时可绕过 workflow 直接调原子 skill |

⚠️ 边界说明**必须放在 SKILL.md 最前面**（定位与边界段下），便于防触发污染——避免 Claude 误把"客户问尽调具体问题"触发到 workflow，或把"客户问完整流程是什么"触发到原子 skill。

---

## 六、workflow 嵌套的统一规则

本仓库当前存在**一处合法嵌套**：

- `ecm-workflow:wf-ipo-full` 在阶段 3 内**嵌套调用** `ecm-workflow:wf-ipo-dd-full`
- `ecm-workflow:wf-nto-listing` 在阶段 3 内**嵌套调用** `ecm-workflow:wf-ipo-dd-full`（新三板尽调与 IPO 高度重合）

嵌套规则：

1. **声明嵌套**：嵌套的 workflow 在自己 frontmatter 的 `depends_on.internal_skills` 中显式列出被嵌套 workflow（如 `wf-ipo-full` 列出 `ecm-workflow-wf-ipo-dd-full`）
2. **不重复展开**：被嵌套 workflow 的内部清单**不要**复制到外层 workflow 的 SKILL.md；外层只写"调用 `ecm-workflow:wf-ipo-dd-full`"一行
3. **状态独立**：被嵌套 workflow 的"是否完成"由其阶段产物（17 份 DD Memo 是否齐备）独立判定，外层 workflow 不维护额外状态
4. **禁止双向嵌套**：A 嵌套 B 时，B 不得反过来嵌套 A（避免无限递归）；目前 6 个 workflow 中只有 wf-ipo-dd-full 是被嵌套对象（叶节点），其他都是父节点

---

## 七、SKILL.md 正文章节的硬性顺序

每个 ecm-workflow skill 必须按以下顺序组织 SKILL.md（防止内容散乱、便于 grep）：

```
# <业务场景中文名> 工作流 Skill
## 定位与边界
## 免责声明
## 与原子 skill 的边界                          # 强制声明，节五项区别表
## 配置项                                       # 项目类型识别 / 跳过 / 回滚
## 阶段编排
  ### 阶段 1 — 项目启动
  ### 阶段 2 — 方案设计
  ### 阶段 3 — 尽职调查
  ### 阶段 4 — 文书输出
  ### 阶段 5 — 内核审查
  ### 阶段 6 — 申报 / 持续督导支持（按需）
## skill 间数据传递契约（引用 SoT，不重写）
## 失败 / 跳过 / 回滚处理
## 嵌套关系（如有）
## 端到端示例（脑内测试）                       # 强制；按典型项目走一遍流程，验证编排可执行
## 参考资料索引
```

---

## 八、references/ 目录结构（可选）

ecm-workflow skill 通常**不需要** references/ 目录（本身不做业务逻辑、不嵌大量参考资料）。

如确有必要（例如 wf-cross-border-ma 需要"7 个跨境主管部门 + 10 部核心法规"快速速查），允许添加但**不得**与原子 skill 的 references/ 重复——应在自己的 references/ 里**只列出"在哪个原子 skill 里能找到该资源"**，引导用户跳转，不复制内容。

---

## 九、与既有 SoT 的对应关系

workflow skill 在编写时引用的所有 SoT：

| SoT | 路径 | 引用场景 |
|-----|------|---------|
| 项目目录结构 | `shared/templates/project-folder-structure.md` | 阶段产物落地路径 |
| DD → Draft 契约 | `shared/schemas/dd-output-schema.md` | 阶段 3 → 阶段 4 数据交接 |
| 工作报告格式 | `shared/templates/work-report-format.md` | 阶段 4 `report-assembly` 的输出参考坐标 |
| 法律意见书格式 | `shared/templates/legal-opinion-format.md` | 阶段 4 `opinion-letter` 的输出参考坐标 |
| 法律备忘录格式 | `shared/templates/legal-memo-format.md` | 阶段 2 `ecm-design-*` 的输出参考坐标 |
| 会议文件格式 | `shared/templates/meeting-docs-format.md` | 阶段 4 `meeting-docs` 的输出参考坐标 |
| 法律研究输出格式 | `shared/templates/research-output-format.md` | 阶段 6 `ecm-research-*` 的输出参考坐标 |
| QC skill 模板 | `shared/templates/qc-skill-template.md` | 阶段 5 `ecm-qc-*` 的工作流参考坐标 |
| DD skill 模板 | `shared/templates/dd-skill-template.md` | 阶段 3 各 `ecm-dd-*` skill 的写作模板（workflow 不直接消费，但提及一致性时引用） |
| 分类标签 | `shared/terminology/classification-labels.md` | 阶段 1 `file-classify` 用的标签体系 |

⚠️ workflow skill **只引用**这些 SoT 的相对路径，**不复制**其内容（更新 SoT 不应触发 6 个 workflow 跟改）。

---

## 版本

| 日期 | 变更 |
|------|------|
| 2026-04-25 | 初版（BATCH-10 建立）。锁定：SKILL.md frontmatter（含 `wf-` 前缀强制 + module=ecm-workflow + category=工作流编排）/ 正文骨架 9 节 / 6 阶段 schema（启动 / 设计 / 尽调 / 文书 / 内核 / 申报）/ 三层契约（项目目录 SoT + DD-output schema + 各类格式 SoT）/ 失败-跳过-回滚处理规则 / workflow 嵌套规则（声明嵌套 + 不重复展开 + 状态独立 + 禁止双向）/ 与原子 skill 五项边界声明 |
