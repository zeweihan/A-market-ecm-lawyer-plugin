---
name: ecm-workflow-wf-issuance
description: >
  上市公司再融资项目工作流 Skill。从项目启动、融资工具比选、定向尽职调查、文书输出到内核审查的端到端编排，覆盖向特定对象发行（定增）/ 配股 / 可转债 / 优先股 / 公开发行 等再融资工具。当用户提到以下场景时触发：再融资 / 上市公司定增 / 向特定对象发行 / 非公开发行 / 配股 / 可转债 / 转债 / CB / 优先股 / 公开增发 / SPO / 上市公司再融资项目 / 再融资工作流 / 再融资 kickoff / 帮我接一个定增项目 / 客户要做可转债。也包括用户已经决定再融资但不知从何开始、或希望全流程指引下一步应做什么的场景。本 skill **不直接做任何具体业务**——它输出**6 阶段清单 + 下一步指引**，特别强调"上市公司视角的定向 DD"（不同于 IPO 全 17 章），重点关注最近 3 年信披合规、关联交易、募集资金运用合规。如是 IPO（首发）请用 wf-ipo-full；如是并购请用 wf-ma-full；如涉及跨境请用 wf-cross-border-ma；如是新三板挂牌请用 wf-nto-listing。
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
    - ecm-dd-approval
    - ecm-dd-entity
    - ecm-dd-shareholders
    - ecm-dd-history
    - ecm-dd-business
    - ecm-dd-related-party
    - ecm-dd-assets
    - ecm-dd-debt
    - ecm-dd-charter
    - ecm-dd-directors
    - ecm-dd-fundraising
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

# 上市公司再融资项目 工作流 Skill

## 定位与边界

本 skill **负责**：
- 为上市公司再融资项目（向特定对象发行 / 配股 / 可转债 / 优先股 / 公开增发）提供**端到端 6 阶段编排**
- 在阶段 2 帮助用户**比选融资工具**（不同工具的适用条件 / 发行难度 / 对老股东影响 / 募投合规要求差异极大）
- 在阶段 3 提供**上市公司视角的定向 DD 子集**（不同于 IPO 的 17 章基础尽调，再融资重点是最近 3 年信披合规 + 关联交易 + 募集资金运用 + 实控人占用违规担保等 IPO 红线再核查）
- 在阶段 4 强调**募集说明书 / 发行公告 / 募投可行性论证报告**等再融资特殊文书的法律相关章节

本 skill **不负责**：
- IPO（首发）的编排——见 `wf-ipo-full`
- 跨境再融资（如 H 股配股 / GDR）—— 涉及外汇 / 反垄断时建议组合 `wf-cross-border-ma` 元素或单独触发 `ecm-design:cross-border`
- 自动化执行——本 skill 输出阶段清单 + 提示

## 免责声明

本 skill 仅为再融资项目流程管理辅助工具，被嵌套触发的所有原子 skill 输出**不构成法律意见**，不替代签字律师的专业判断。完整免责声明见本仓库顶层 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 与原子 skill 的边界

| 维度 | 各 `ecm-design-*` / `ecm-dd-*` / `ecm-draft-*` skill | `ecm-workflow:wf-issuance`（本 skill） |
|------|----------------------------------|-----------------------------|
| 角色 | "做事的人" | "总指挥官"——输出 6 阶段清单 + 进度提示 |
| 输出 | 业务产物 | 阶段清单 + 下一步指引 |
| 触发频次 | 单点触发 | 整个再融资项目周期内被反复参考 |
| 上下文使用 | 加载本任务所需法规 / checklist | 不加载具体业务上下文 |
| 失败影响域 | 仅影响该步产物 | 失败不阻塞——用户可绕过本 workflow 直接调原子 skill |

⚠️ 防触发污染：
- 用户问 "定增和可转债哪个发行难度低"——触发 `ecm-design:deal-structure`，不触发本 workflow
- 用户问 "募集资金运用怎么核查"——触发 `ecm-dd:dd-fundraising`
- 用户问 "我要做个定增"——触发**本 workflow**

## 配置项

**融资工具识别**（**强制在阶段 2 之前**确认；影响阶段 2 比选维度 + 阶段 3 DD 重点 + 阶段 4 文书清单）：

| 工具 | 关键再融资规则 | DD 重点 | 阶段 4 必含文书 |
|------|--------------|--------|--------------|
| 向特定对象发行（定增）| 《上市公司证券发行注册管理办法》§ 38 起；折扣定价 80%、限售 6 个月（普通投资者）/ 18 个月（控股股东） | 关联交易、最近 36 月信披合规、最近 12 月发行后募投使用情况、是否存在违规担保 / 资金占用 | 法律意见书 + 律师工作报告 + 募集说明书法律意见 + 董事会 / 股东大会决议 |
| 配股 | 《上市公司证券发行注册管理办法》§ 33；最近 3 年加权 ROE ≥ 6% 等条件 | 同上 + 老股东信披一致性 + 配售比例不超过原股本 30% | 法律意见书 + 律师工作报告 + 募集说明书 + 配售方案 |
| 可转债 | 《上市公司证券发行注册管理办法》§ 41 起；最近 3 年净利润 + 现金流 + 期末资产负债率 等综合财务指标 | 重点核查最近 3 年财务真实性、关联交易、是否触发"重大违法行为" | 法律意见书 + 律师工作报告 + 可转债募集说明书 + 转股 / 回售 / 强赎条款 |
| 优先股 | 《优先股试点管理办法》| 普通股股东保护、表决权恢复条款 | 法律意见书 + 律师工作报告 + 募集说明书 |
| 公开增发 | 《上市公司证券发行注册管理办法》§ 49 等；最近 3 年加权 ROE ≥ 6% | 同定增 + 公开发行额外披露要件 | 法律意见书 + 律师工作报告 + 募集说明书 |

**跳过策略（Skip Policy）**：
- `strict` / `loose`（默认 loose）

**回滚策略**：见 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认。

---

## 阶段编排

### 阶段 1 — 项目启动

| 项 | 内容 |
|----|------|
| **目标** | 建立项目目录 + 客户文件归位 |
| **调用 skill**（按序）| `ecm-setup:project-init`（项目类型选 "再融资"）→ `ecm-setup:file-classify` → `ecm-setup:file-organize` |
| **阶段产物** | `{项目根}/` 目录树 + `02-NN-*/文件索引表.md` |
| **进入下一阶段判定** | 项目根已建 + 至少 80% 客户文件归位（特别是最近 3 年定期报告 / 临时公告需齐备） |
| **可跳过** | 否 |

### 阶段 2 — 方案设计（融资工具比选）

| 项 | 内容 |
|----|------|
| **目标** | 比选定增 vs 配股 vs 可转债 vs 优先股 vs 公开增发；确定发行规模、发行对象、定价机制、募投项目 |
| **调用 skill** | `ecm-design:deal-structure`（覆盖再融资工具比选维度：发行条件 / 发行难度 / 对老股东摊薄 / 监管审核周期 / 募投合规要求）|
| **阶段产物** | `01-方案设计/再融资工具比选-备忘录-{YYYYMMDD}.md`（遵循 [`shared/templates/legal-memo-format.md`](../../shared/templates/legal-memo-format.md)）；多工具比较表强制 |
| **进入下一阶段判定** | 工具初步定 + 发行规模框架 + 募投项目方向锁定 |
| **可跳过** | 否（不同工具的尽调重点和文书清单差异大；不能跳过比选直接进尽调） |

### 阶段 3 — 尽职调查（**上市公司视角的定向 DD**）

#### 3.1 必查 DD 子集

不同于 IPO 全 17 章——再融资**已经是上市公司**，主体资格 / 设立 / 早期股本演变等已在 IPO 时核查过；本阶段重点是**最近 36 个月（部分指标 12 个月）的合规性 + IPO 红线再核查**。

| 顺序 | skill | 编报规则章节 | 再融资语境下的核查重点 |
|----:|-------|-------------|------------------|
| 1 | `ecm-dd:dd-approval` | 第 1 章 | 本次发行的内部决策（董事会 + 股东大会，特别决议比例 + 关联股东回避 + 中小投资者单独计票）+ 外部批准（行业 / 国资 / 发改 / 反垄断 / 国安）|
| 2 | `ecm-dd:dd-entity` | 第 2 章 | 上市公司主体资格（最近 36 月未擅自发行 / 未被交易所谴责 / 未被立案；持续经营能力）|
| 3 | `ecm-dd:dd-shareholders` | 第 5 章 | 现有股权结构 + 实控人稳定（最近 36 月）+ 一致行动 + 是否存在《上市公司证券发行注册管理办法》§ 11 / § 12 的发行人 / 控股股东 / 实控人不诚信情形 |
| 4 | `ecm-dd:dd-history` | 第 6 章 | 上市后股本演变（限售解禁 / 减持合规 / 股权激励 / 重大资产重组）|
| 5 | `ecm-dd:dd-business` | 第 7 章 | 主营业务、行业政策、重大合同变化、最近 12 月业务合规 |
| 6 | `ecm-dd:dd-related-party` | 第 8 章 | **最近 36 月关联交易合规**（重点：是否存在违规关联交易、是否构成同业竞争、控股股东 / 实控人非经营性资金占用 / 违规担保——**IPO 红线再核查**）|
| 7 | `ecm-dd:dd-assets` | 第 9 章 | 主要财产权属（如募投涉及不动产 / 知识产权获取 / 现有资产置换）|
| 8 | `ecm-dd:dd-debt` | 第 10 章 | **重大债权债务 + 对外担保 + 或有负债 + 财务契约 / change of control 触发**（再融资发行后是否触发交叉违约或债权人控制权条款）|
| 9 | `ecm-dd:dd-charter` | 第 11 章 | 公司章程 + 三会运作 + 内控制度（最近 36 月召开规范性）|
| 10 | `ecm-dd:dd-directors` | 第 12 章 | 董监高（最近 36 月任职合规 + 监管处分 + 兼职 + 承诺事项履行）|
| 11 | `ecm-dd:dd-fundraising` | 第 15 章 | **本次募集资金运用**（募投项目立项 / 用地 / 备案 / 环评 / 节能 / 行业准入）+ **前次募集资金使用情况报告**（再融资必查；是否变更投向 / 是否使用违规） |
| 12 | `ecm-dd:dd-litigation` | 第 16 章 | 最近 36 月诉讼仲裁 + 行政处罚（**特别关注证监会 / 交易所处罚——影响发行条件**）|
| 13 | `ecm-dd:dd-compliance` | 第 17 章 | 最近 36 月信披合规自查 + 社保 / 公积金 / 海关 / 外汇 / 劳动等兜底事项 |

#### 3.2 工具 skill（按需穿插）

- `ecm-dd:dd-data-verify`（工商 / 财务自动比对，节省工时）
- `ecm-dd:dd-file-review`（最近 36 月定期报告 / 临时公告批量提取）

#### 3.3 不查的章节

| 不查的 DD skill | 理由 |
|---------------|------|
| `ecm-dd:dd-establishment` | 设立环节已在 IPO 时核查过；除非本次再融资涉及"整体变更"等特殊情形 |
| `ecm-dd:dd-tax` | 通常不必专门做（如非募投涉及税务优惠 / 税收筹划，可触发）|
| `ecm-dd:dd-environment` | 通常不必专门做（如非高耗能 / 高排放行业；如募投涉及新建项目则触发） |
| `ecm-dd:dd-independence` | 上市公司已经是独立运营主体；除非最近发生过资产重组导致独立性变化，否则不查 |

#### 3.4 阶段产物 + 进入下一阶段

- **阶段产物**：`02-尽职调查/02-NN-*/DD-Memo-*-{YYYYMMDD}.md`（必查 13 章）
- **进入下一阶段判定**：必查 13 章 Memo 出具完毕 + 关键 IPO 红线（关联交易 / 资金占用 / 违规担保）已确认无重大瑕疵
- **可跳过**：必查章节默认不跳过；不查的 4 章见 § 3.3

### 阶段 4 — 文书输出

| 项 | 内容 |
|----|------|
| **目标** | 拼接律师工作报告（再融资版）+ 起草法律意见书（再融资版）+ 起草董事会 / 股东大会决议 + 募集说明书法律相关章节自查 + 格式套版 |
| **调用 skill**（按序）| `ecm-draft:report-assembly`（按 dd-output-schema 拼接，缺章节按违约处理）→ `ecm-draft:opinion-letter`（**事实-核查-意见三步法 + 自动注入"特别事项提示" + 结论性意见**）→ `ecm-draft:meeting-docs`（**特别决议比例 + 关联股东回避 + 中小投资者单独计票** 三项硬规则严格执行）→ `ecm-draft:disclosure-review`（**起草人自查**募集说明书法律相关章节）→ `ecm-draft:format-adjust` |
| **阶段产物** | `04-文件输出/律师工作报告/`、`04-文件输出/法律意见书/`、`04-文件输出/会议文件/`、`04-文件输出/募集说明书法律相关章节-自查报告/` |
| **进入下一阶段判定** | 工作报告 + 意见书 + 关键决议 + 募集说明书法律章节自查通过 |
| **可跳过** | 否 |

> **再融资特别决议提示**：再融资几乎必触发股东大会**特别决议**（出席表决权 2/3 以上通过）+ 关联股东回避 + 中小投资者单独计票——`ecm-draft:meeting-docs` 在再融资语境下应严格执行这三项；阶段 5 的 `ecm-qc:meeting-docs-review` 同样要核对。

### 阶段 5 — 内核审查（**强烈建议，不可跳过**）

| 项 | 内容 |
|----|------|
| **目标** | 项目组提交内核团队前的独立审查 |
| **调用 skill**（按序）| `ecm-qc:work-report-review` → `ecm-qc:opinion-letter-review` → `ecm-qc:meeting-docs-review`（特别决议 / 回避 / 单独计票核对）→ `ecm-qc:disclosure-review`（募集说明书法律相关章节） |
| **阶段产物** | 带 tracked changes + comments 的 `.docx`（`w:author="内核"`） |
| **进入下一阶段判定** | 内核【必改】项已全部落实 |
| **可跳过** | 否 |

### 阶段 6 — 申报 / 反馈支持（按需）

| 项 | 内容 |
|----|------|
| **目标** | 交易所 / 证监会反馈回复 / 类似案例检索 / 法规深度研究 |
| **调用 skill**（按需）| `ecm-research:case-search`（再融资类似案例 / 上市委 / 发审委审议关注点）/ `ecm-research:reg-search`（最新再融资规则）/ `ecm-research:reg-study` / `ecm-draft:disclosure-review`（持续起草人自查）|
| **阶段产物** | `06-反馈回复/{反馈批次}/{研究主题}-备忘录-{YYYYMMDD}.md` |
| **可跳过** | 是（按申报推进决定） |

---

## skill 间数据传递契约

阶段间数据流完全靠**已经存在的 SoT**，无 workflow 私有状态：

| 阶段衔接 | 依赖 SoT |
|---------|---------|
| 阶段 1 → 阶段 2 | `shared/templates/project-folder-structure.md` |
| 阶段 2 → 阶段 3 | `01-方案设计/再融资工具比选-备忘录.md` 决定阶段 3 必查章节 + 阶段 4 文书清单 |
| 阶段 3 → 阶段 4 | `shared/schemas/dd-output-schema.md` § 4 / § 5 |
| 阶段 4 → 阶段 5 | `shared/templates/qc-skill-template.md` |

### 进度判断（无状态）

```bash
ls -d 01-方案设计/ 2>/dev/null
ls 02-尽职调查/02-*/DD-Memo-*.md 2>/dev/null | wc -l   # 目标 13（必查子集）
ls 04-文件输出/律师工作报告/*.docx 2>/dev/null
ls 04-文件输出/募集说明书法律相关章节-自查报告/ 2>/dev/null
ls 04-文件输出/*-内核后-*.docx 2>/dev/null
```

---

## 失败 / 跳过 / 回滚处理

依据 [`shared/templates/workflow-skill-template.md`](../../shared/templates/workflow-skill-template.md) § 4 沿用默认。

**特殊提示**：
- **如发现违规担保 / 资金占用 / 重大财务造假等 IPO 红线问题**：本 workflow 在阶段清单里硬性提示"该问题影响《上市公司证券发行注册管理办法》§ 11 / § 12 发行条件——本次发行可能不被受理；建议回到阶段 2 重新评估方案 / 时间窗"
- 阶段 4 募集说明书法律章节自查发现重大问题——回到阶段 3 补充尽调
- 阶段 5（内核）失败 = 内核【必改】项未全部落实——回到阶段 4 修订

---

## 嵌套关系

本 workflow **不嵌套**任何其他 workflow，**也不被任何其他 workflow 嵌套**。

如再融资项目伴随重大资产重组（"再融资 + 并购"组合），不嵌套 `wf-ma-full`，建议**两个 workflow 并行**——再融资部分用本 workflow，重组部分用 `wf-ma-full`，两者共享同一项目目录但分别落地各自的方案备忘录和 DD Memo。

---

## 端到端示例（脑内测试）

**场景：上市公司向特定对象发行（定增）**

```
用户："我们公司是 A 股主板上市公司，要做一次 50 亿定增"

本 skill：
  项目类型识别：再融资（向特定对象发行 / 定增）
  阶段 1：建项目目录（项目类型 = 再融资）
  阶段 2：触发 `ecm-design:deal-structure`（比选定增 vs 可转债 vs 公开增发）
        + 确定发行对象（不超过 35 名特定投资者）+ 定价机制（询价 / 锁价）
        + 募投项目（论证必要性 / 可行性）
  阶段 3 必查 13 章（不查 establishment / tax / environment / independence）：
    重点：dd-related-party 最近 36 月关联交易；dd-debt 违规担保；
         dd-fundraising 前次募投使用 + 本次募投合规；dd-litigation 监管处罚
  阶段 4：report-assembly + opinion-letter + meeting-docs（特别决议 + 关联股东回避
         + 中小投资者单独计票）+ disclosure-review（募集说明书法律相关章节）+ format-adjust
  阶段 5：四个 ecm-qc-* 全部触发；meeting-docs-review 重点核对三项硬规则
  阶段 6：交易所 / 证监会反馈来时按需触发 ecm-research-* / disclosure-review
```

---

## 参考资料索引

本 skill 不自带 references/ 目录——所有参考资料由各原子 skill 自带，特别是 `ecm-dd-fundraising` 的募集资金运用核查清单。

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
| 2026-04-25 | 初版（BATCH-10）。锁定 6 阶段编排 + 阶段 2 强制工具比选（5 类）+ 阶段 3 上市公司视角的 13 章必查子集（不查 establishment / tax / environment / independence）+ 阶段 4 三项硬规则（特别决议 + 关联股东回避 + 中小投资者单独计票）+ IPO 红线再核查（关联交易 / 资金占用 / 违规担保） |
