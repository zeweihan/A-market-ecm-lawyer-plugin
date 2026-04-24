# skill 规划路线图 / Skill Roadmap

本文档跟踪本仓库 skill 的规划和进度，对齐《ECM Skills 项目说明》定稿的完整 taxonomy。

## 两个模块 + 命名规范

本仓库的 skill 按**使用者角色**分为两个模块：

- **项目 skill**（6 类：setup/design/dd/draft/research/workflow）——项目组律师做项目时用
- **QC skill**（1 类：qc）——内核/QC 团队做独立审查时用

所有 skill 采用两级命名空间：

```
ecm-<category>:<function>
```

- **目录名**用 `ecm-<category>-<function>` 格式（kebab-case，用连字符替代冒号），例：`skills/ecm-setup-project-init/`
- **SKILL.md frontmatter 的 `name` 字段**同目录名（例：`ecm-setup-project-init`）
- **SKILL.md frontmatter 的 `module` 字段**标注所属模块（`ecm-setup/design/dd/draft/research/workflow/qc`）
- **文档/路线图/README 表格**里统一用带冒号的人类可读形式（例：`ecm-setup:project-init`）

## 两个维度

**业务阶段**（单项目可能跨多阶段）：研究阶段 / 启动阶段 / 尽调阶段 / 申报阶段 / 反馈阶段 / 发行阶段 / 持续督导阶段

**功能类别**（对应 7 大 skill 类）：setup / design / dd / draft / research / workflow / qc

## 完整 skill 清单（7 大类 / 36 项项目 skill + 1 项已实现 QC skill）

### 1. ecm-setup — 项目初始化与文件管理

| skill | 说明 | 阶段 | 状态 |
|-------|------|------|------|
| `ecm-setup:project-init` | 根据项目类型初始化文件夹结构、生成 Skill roadmap | 启动阶段 | ✅ v0.1.0 可用 |
| `ecm-setup:file-classify` | 批量阅读客户提供的文件，输出多维标签 | 启动阶段 | ✅ v0.1.0 可用 |
| `ecm-setup:file-organize` | 根据分类标签将文件移入对应目录，生成文件索引 | 启动阶段 | ✅ v0.1.0 可用 |

### 2. ecm-design — 方案设计

| skill | 说明 | 阶段 | 状态 |
|-------|------|------|------|
| `ecm-design:ipo-path` | IPO 路径选择（主板/科创板/创业板/北交所/港股/红筹对比） | 研究阶段 | ✅ v0.1.0 可用 |
| `ecm-design:deal-structure` | 通用交易结构设计（股权/资产/增资/合并） | 研究阶段 | ✅ v0.1.0 可用 |
| `ecm-design:control-rights` | 控制权交易结构（收购方式、对赌、表决权、一致行动） | 研究阶段 | ✅ v0.1.0 可用 |
| `ecm-design:ma-structure` | 上市公司并购（发行股份购买资产/现金/混合/借壳） | 研究阶段 | ✅ v0.1.0 可用 |
| `ecm-design:cross-border` | 跨境交易方案（ODI/FDI/外商投资/外汇/反垄断/国安审查） | 研究阶段 | ✅ v0.1.0 可用 |

### 3. ecm-dd — 尽职调查（按编报规则第 12 号拆分）

| skill | 对应章节 | 说明 | 状态 |
|-------|---------|------|------|
| `ecm-dd:dd-approval` | 第 1 章 | 本次交易的批准和授权 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-entity` | 第 2 章 | 发行人的主体资格 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-establishment` | 第 3 章 | 发行人的设立 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-independence` | 第 4 章 | 发行人的独立性 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-shareholders` | 第 5 章 | 发起人和主要股东（含实控人） | ✅ v0.1.0 可用 |
| `ecm-dd:dd-history` | 第 6 章 | 发行人的股本及其演变（历史沿革） | ✅ v0.1.0 可用 |
| `ecm-dd:dd-business` | 第 7 章 | 发行人的业务 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-related-party` | 第 8 章 | 关联交易和同业竞争 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-assets` | 第 9 章 | 发行人的主要财产 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-debt` | 第 10 章 | 重大债权债务 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-charter` | 第 11 章 | 公司章程及组织机构（三会运作） | ✅ v0.1.0 可用 |
| `ecm-dd:dd-directors` | 第 12 章 | 董事、监事、高管及其变化 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-tax` | 第 13 章 | 税务 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-environment` | 第 14 章 | 环境保护、产品质量、安全生产 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-fundraising` | 第 15 章 | 募集资金运用 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-litigation` | 第 16 章 | 诉讼、仲裁或行政处罚 | ✅ v0.1.0 可用 |
| `ecm-dd:dd-compliance` | 第 17 章 | 其他合规事项（兜底） | ✅ v0.1.0 可用 |
| `ecm-dd:dd-data-verify` | — | 数据自动化比对（Tushare / 企查查 API 交叉验证） | ✅ v0.1.0 可用 |
| `ecm-dd:dd-file-review` | — | 本地文件批量审阅（读取项目文件夹 PDF/Word/Excel） | ✅ v0.1.0 可用 |

### 4. ecm-draft — 文书起草与处理

| skill | 说明 | 阶段 | 状态 |
|-------|------|------|------|
| `ecm-draft:report-assembly` | 拼接 DD 各章节 → 完整尽调报告/律师工作报告 | 申报阶段 | ✅ v0.1.0 可用 |
| `ecm-draft:format-adjust` | Word 格式调整（排版/编号/交叉引用/页眉页脚/目录） | 全阶段 | ✅ v0.1.0 可用 |
| `ecm-draft:meeting-docs` | 批量起草会议文件（通知/议案/决议/记录/签到表） | 全阶段 | ✅ v0.1.0 可用 |
| `ecm-draft:opinion-letter` | 基于 DD 结论生成标准化法律意见书 | 申报阶段 | ✅ v0.1.0 可用 |
| `ecm-draft:disclosure-review` | 信息披露文件起草人自查（招股书/重组报告书/权益变动；与 `ecm-qc:disclosure-review` 配对但视角不同） | 申报阶段 / 反馈阶段 | ✅ v0.1.0 可用 |

### 5. ecm-research — 法律研究

| skill | 说明 | 阶段 | 状态 |
|-------|------|------|------|
| `ecm-research:case-search` | 案例检索（裁判文书/证监会处罚/交易所纪律处分/并购重组委/上市委案例） | 全阶段 | ✅ v0.1.0 可用 |
| `ecm-research:reg-search` | 法规查询（法律/行政法规/部门规章/证监会规范性文件/交易所业务规则） | 全阶段 | ✅ v0.1.0 可用 |
| `ecm-research:reg-study` | 法规深度研究（适用性/效力层级/冲突解决/新旧衔接） | 全阶段 | ✅ v0.1.0 可用 |

### 6. ecm-workflow — 工作流编排

| skill | 说明 | 状态 |
|-------|------|------|
| `ecm-workflow:wf-ipo-full` | 完整 IPO 项目流程（init → design → dd → draft） | 🟡 草稿 |
| `ecm-workflow:wf-ipo-dd-full` | 完整 IPO 尽调流程（自动顺序调用 17 个 DD skill） | 🟡 草稿 |
| `ecm-workflow:wf-ma-full` | 完整并购项目流程 | 🟡 草稿 |
| `ecm-workflow:wf-cross-border-ma` | 跨境并购工作流 | 🟡 草稿 |
| `ecm-workflow:wf-issuance` | 上市公司再融资流程（定增/配股/可转债） | 🟡 草稿 |
| `ecm-workflow:wf-nto-listing` | 新三板挂牌流程 | 🟡 草稿 |

### 7. ecm-qc — 内核/QC 审查（QC 模块）

> **使用者角色**：内核团队/QC 团队。调用场景：项目组提交的文书需要独立审阅环节。输出形式统一为**带修订痕迹（Track Changes）+ 批注（Comments）的 Word 文档**，作者（w:author）统一为"内核"或 QC 团队自定义名。

| skill | 说明 | 阶段 | 状态 |
|-------|------|------|------|
| `ecm-qc:shareholders-meeting-witness` | 股东（大）会法律见证意见内核审查 | 持续督导阶段 | ✅ v0.1.0 可用 |
| `ecm-qc:opinion-letter-review` | 法律意见书内核审查（配对 `ecm-draft:opinion-letter`） | 申报阶段 | ⏳ BATCH-09 规划中 |
| `ecm-qc:work-report-review` | 律师工作报告内核审查（配对 `ecm-draft:report-assembly`） | 申报阶段 | ⏳ BATCH-09 规划中 |
| `ecm-qc:disclosure-review` | 招股书/重组报告书/权益变动报告书内核审查（和 `ecm-draft:disclosure-review` 的区别见下方注） | 申报阶段 / 反馈阶段 | ⏳ BATCH-09 规划中 |
| `ecm-qc:meeting-docs-review` | 会议文件（通知/议案/决议/记录）内核审查（配对 `ecm-draft:meeting-docs`） | 全阶段 | ⏳ BATCH-09 规划中 |

> **注**：`ecm-draft:disclosure-review` 是项目组起草人自查自纠；`ecm-qc:disclosure-review` 是内核独立审查。二者 checklist 重叠但视角不同：前者关注"我写的对不对"，后者关注"团队交上来的有没有错"。

## 状态说明

- ✅ **可用**：SKILL.md 完整、references/scripts 齐全、本地测试通过
- 🟡 **草稿**：54-ecm_skills 仓库里存在初稿，但尚未按本仓库规范迁入
- ⏳ **规划**：只有名字和大致定位，未开始写
- 🔴 **弃用**：已被其他 skill 替代

## 开发优先级

| 阶段 | 内容 | 优先级 |
|------|------|--------|
| P0 | 仓库框架 + 模板 + 统一规范 | ✅ 已完成（v0.1.0） |
| P0.5 | `ecm-qc:shareholders-meeting-witness` 迁入 | ✅ 已完成（v0.1.0） |
| P1 | `ecm-setup` 系列（3 项，前置依赖） | ✅ 已完成（BATCH-01） |
| P2 | `ecm-dd` 系列（19 项，律师最高频工作） | ✅ 全部完成：BATCH-02 公司基础面 7 项 + BATCH-03 业务与资产 5 项 + BATCH-04 合规事项 5 项 + BATCH-05 工具类 2 项 |
| P3 | `ecm-draft` 系列（5 项，report-assembly 最优先） | ✅ 已完成（BATCH-06：report-assembly / opinion-letter / disclosure-review / meeting-docs / format-adjust 全部就绪；`shared/schemas/dd-output-schema.md` 和 `work-report-format.md` / `legal-opinion-format.md` / `meeting-docs-format.md` 三份模板同批建立） |
| P4 | `ecm-design` 系列（5 项） | ✅ 已完成（BATCH-07） |
| P5 | `ecm-research` 系列（3 项） | ✅ 已完成（BATCH-08） |
| P6 | `ecm-workflow` 系列（6 项） | 全流程打通 |
| P7 | `ecm-qc` 其余 skill（opinion-letter-review / work-report-review / disclosure-review / meeting-docs-review） | BATCH-09 窗口建设（与 BATCH-06 并行触发） |
| P8 | 数据连接器（Tushare / 企查查） | 自动化增强 |

## 标准工作流示例（IPO 项目）

```
1. ecm-setup:project-init          # 建立项目文件夹，生成 Skill 清单
2. ecm-setup:file-classify         # 客户文件批量打标签
3. ecm-setup:file-organize         # 按标签移入目录
4. ecm-design:ipo-path             # 论证 A 股/港股/红筹路径
5. ecm-workflow:wf-ipo-dd-full     # 调用 17 个 DD skill 逐章完成
6. ecm-draft:report-assembly       # 拼接律师工作报告
7. ecm-draft:opinion-letter        # 生成法律意见书
8. ecm-draft:format-adjust         # 统一排版格式
```

## 关键设计约束（沿用）

1. **上下文隔离**：每个原子 skill 只加载其工作所需的最小上下文。
2. **输入输出标准化**：每个 DD skill 输出统一为「核查要点清单 + 审阅发现 + 风险分级（高/中/低）+ 建议措施」。
3. **标签多对多**：文件分类阶段一个文件可对应多个标签，不简单放进唯一文件夹。
4. **组合调用**：复杂项目通过 workflow 组合多个原子 skill，不在单个 skill 中硬编码。

## 源材料出处

本 roadmap 的设计 taxonomy 来自 `/Users/zewei/Documents/2024-2044/0-个人事项/54-ecm_skills/CLAUDE.md`（作者：zeweihan）。该仓库里另有 36 份 skill 草稿（位于 `.claude/skills/` 下），将来逐步按本仓库规范迁入。

## 维护

新增 skill 时：
1. 在上方表格相应分组加一行
2. 在根目录 `README.md` 的 skill 清单表格加一行
3. 在 `CHANGELOG.md` 的 `[Unreleased]` 段记录
4. 状态从"规划"→"草稿"→"可用"跟随开发进度变更

废弃 skill 时：标 `🔴 弃用`，在 `CHANGELOG.md` 说明迁移路径。
