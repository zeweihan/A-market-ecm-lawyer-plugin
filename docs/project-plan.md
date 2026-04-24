# 项目工作计划 / Project Plan

> 本文档是建设本仓库全部 skill 的总协调文件。开新窗口时请先读本文件再开始具体 batch 工作。

## 当前状态快照（最后更新：2026-04-24）

**仓库位置**：`/Users/zewei/Documents/2024-2044/0-个人事项/0-aplugin`
**GitHub**：https://github.com/zeweihan/A-market-ecm-lawyer-plugin
**本地 git 分支**：`main`（领先 GitHub 3 个 commit，等用户 push）

**已完成**（4 个 skill 可用）：
- ✅ BATCH-00 仓库框架
- ✅ BATCH-00.5 `ecm-qc:shareholders-meeting-witness`
- ✅ BATCH-01 `ecm-setup` 三件套（project-init / file-classify / file-organize）
  - 附带产出：`shared/terminology/classification-labels.md`（19 个标签的权威定义）
  - 附带产出：`shared/templates/project-folder-structure.md`（目录结构 + 标签→目录映射）

**下一步推荐**：BATCH-02（`ecm-dd` 公司基础面 7 个 skill）。BATCH-02 完成后会产出 `shared/templates/dd-skill-template.md`，供 BATCH-03/04/05 复用。

**并行可开**：BATCH-07（ecm-design）和 BATCH-08（ecm-research）与 BATCH-02 无硬依赖，可以同时开独立窗口推进。

**源材料位置**：`/Users/zewei/Documents/2024-2044/0-个人事项/54-ecm_skills/`
- 新窗口需先用 `request_cowork_directory` 请求访问
- 部分文件是 iCloud 仅云端状态——Bash 读取会遇到 `Resource deadlock avoided`，改用 Read 工具即可（Read 经由 host 读，绕开 iCloud 锁）

**已建立的跨 skill 共享资源**（新 skill 必须通过相对路径引用，不要重复定义）：
- `shared/terminology/classification-labels.md`——19 个分类标签
- `shared/templates/project-folder-structure.md`——目录结构和标签映射

## 整体策略

把 40+ 个 skill 的建设工作切成 **11 个 batch**。每个 batch 满足：

- **一次 commit 的工作量**：一个窗口一次对话可以完整交付
- **独立可并行**：不同 batch 之间不共享未完成依赖，可在独立窗口同时推进
- **自包含的启动包**：仅凭本文件 + `skill-authoring-guide.md` + 已有样板 skill，新窗口即可冷启动

## 已完成

| Batch | 内容 | 状态 |
|-------|------|------|
| BATCH-00 | 仓库框架（LICENSE / README / DISCLAIMER / CONTRIBUTING / CHANGELOG / docs / shared / scripts / plugin.json / .github） | ✅ |
| BATCH-00.5 | `ecm-qc:shareholders-meeting-witness` 迁入 + ecm-qc 模块成立 | ✅ |
| BATCH-01 | `ecm-setup` 三件套（project-init / file-classify / file-organize）+ 抽出 shared/terminology/classification-labels.md + shared/templates/project-folder-structure.md | ✅ |

## Batch 清单

| Batch | 类别 | skill 数 | 依赖 | 推荐执行窗口 |
|-------|------|---------:|------|-------------|
| ~~BATCH-01~~ | ~~`ecm-setup` 三件套~~ | ~~3~~ | ~~无~~ | ✅ 已完成 |
| BATCH-02 | `ecm-dd` 公司基础面 | 7 | 建议 BATCH-01 先完成 | 独立窗口 |
| BATCH-03 | `ecm-dd` 业务与资产 | 5 | BATCH-01 | 独立窗口 |
| BATCH-04 | `ecm-dd` 合规事项 | 5 | BATCH-01 | 独立窗口 |
| BATCH-05 | `ecm-dd` 工具类 | 2 | BATCH-01 | 独立窗口 |
| BATCH-06 | `ecm-draft` | 5 | 建议 BATCH-02~05 先完成（需知道 DD 输出格式） | 独立窗口 |
| BATCH-07 | `ecm-design` | 5 | 无硬依赖 | 独立窗口 |
| BATCH-08 | `ecm-research` | 3 | 无硬依赖 | 独立窗口 |
| BATCH-09 | `ecm-qc` 剩余 | 4 | BATCH-06 先完成（需要起草侧的对应 skill） | 独立窗口 |
| BATCH-10 | `ecm-workflow` | 6 | 前述所有 batch 都需完成 | 独立窗口（编排层） |
| BATCH-11 | 数据连接器脚本 | — | BATCH-05 完成 | 独立窗口（纯 Python 代码） |

**并行建议**：BATCH-01、BATCH-07、BATCH-08 之间无硬依赖，可以同时开三个窗口推进。BATCH-02~05 在 BATCH-01 完成后可四个窗口并行。

---

## 每个 Batch 的详细说明

### BATCH-01 — `ecm-setup` 三件套

**skill 清单**：
- `ecm-setup:project-init` — 项目初始化 + 建文件夹 + 输出 skill roadmap
- `ecm-setup:file-classify` — 客户文件批量打标签（many-to-many）
- `ecm-setup:file-organize` — 按标签归位 + 生成索引表

**源材料**：`/Users/zewei/Documents/2024-2044/0-个人事项/54-ecm_skills/.claude/skills/ecm-setup/` 下同名 .md（project-init 271 行较成熟，其余两个较简短）。

**输入**：三份源 .md 文件、本仓库的 skill-authoring-guide。

**输出**：
- `skills/ecm-setup-project-init/`（完整目录，含 SKILL.md + references/ + 可选 scripts/）
- `skills/ecm-setup-file-classify/`
- `skills/ecm-setup-file-organize/`
- 三者共用的标签体系抽到 `shared/terminology/classification-labels.md`
- 三者共用的标准项目目录结构抽到 `shared/templates/project-folder-structure.md`

**特殊要求**：
- `file-classify` 的 19 个标签和 `file-organize` 的目录映射**必须从同一份 shared 文件取值**——避免将来改标签时两边不同步
- `project-init` 的 Skill Roadmap 里引用的 skill 名称使用本仓库规范（`ecm-setup-project-init` 带连字符的形式，而非 `ecm-setup:project-init`）

**验收**：
- [ ] 三个 skill 的 SKILL.md 都有完整 frontmatter（含 module / user_role / phase / category）
- [ ] 三个 skill 的 description 密集，能触发"帮我开个新项目""客户给了一堆文件帮我分类""文件归位"等典型请求
- [ ] shared/terminology/classification-labels.md 和 shared/templates/project-folder-structure.md 已建立
- [ ] 根 README.md 和 docs/skill-roadmap.md 状态表更新
- [ ] CHANGELOG 记录本 batch
- [ ] `scripts/package-skill.sh` 对三个 skill 都能成功打包

---

### BATCH-02 — `ecm-dd` 公司基础面（7 个）

**skill 清单**：
- `ecm-dd:dd-approval` — 批准和授权（编报规则第 1 章）
- `ecm-dd:dd-entity` — 主体资格（第 2 章）
- `ecm-dd:dd-establishment` — 设立（第 3 章）
- `ecm-dd:dd-history` — 历史沿革（第 6 章）
- `ecm-dd:dd-shareholders` — 股东及实控人（第 5 章）
- `ecm-dd:dd-charter` — 公司章程与组织机构（第 11 章）
- `ecm-dd:dd-directors` — 董监高（第 12 章）

**源材料**：`54-ecm_skills/.claude/skills/ecm-dd/` 下的同名 .md（多数 50 行左右，为基础框架）。

**为何同一批**：7 个都是"公司主体本身"的尽调维度（谁批准、谁设立、谁控制、谁治理、谁管理），文件来源重叠度高（章程/工商/股东会决议会被 4 个以上 skill 共同引用），适合一批里建立统一的 DD skill 模板。

**必须共同遵守的 DD skill 统一输出格式**：
```
1. 核查要点清单（法规依据）
2. 审阅发现（对照客户文件的具体问题）
3. 风险分级（高/中/低）
4. 建议措施（补充资料 / 整改 / 披露 / 获取承诺函）
```

**输出**：
- 7 个 `skills/ecm-dd-xxx/` 目录
- `shared/regulations/` 下补齐本批次引用到的法规节选（《公司法》《首次公开发行股票注册管理办法》对应条文）
- **DD skill 模板文件**：`shared/templates/dd-skill-template.md`——供 BATCH-03/04 直接复用

**验收**：
- [ ] 7 个 skill 遵守统一 DD 输出格式
- [ ] 共用的 shared 资源抽齐
- [ ] dd-skill-template.md 建立并在 authoring-guide 里引用
- [ ] 无重复的法规条文节选（全部通过 `shared/regulations/` 引用）

---

### BATCH-03 — `ecm-dd` 业务与资产（5 个）

**skill 清单**：
- `ecm-dd:dd-business` — 业务（第 7 章）
- `ecm-dd:dd-related-party` — 关联交易和同业竞争（第 8 章）
- `ecm-dd:dd-assets` — 主要财产（第 9 章）
- `ecm-dd:dd-debt` — 重大债权债务（第 10 章）
- `ecm-dd:dd-independence` — 独立性（第 4 章）

**为何同一批**：这 5 个是"公司经营侧"的尽调——业务怎么做、资产是什么、欠谁的钱、关联方谁、是否独立。文件引用重叠（业务合同、担保协议、资产清单、关联方清单相互交织）。

**依赖**：BATCH-02 的 `dd-skill-template.md` 必须先建立。

**输出**：5 个 DD skill 目录 + 补齐 shared/regulations/ 相关条文。

**验收**：同 BATCH-02 验收标准。

---

### BATCH-04 — `ecm-dd` 合规事项（5 个）

**skill 清单**：
- `ecm-dd:dd-tax` — 税务（第 13 章）
- `ecm-dd:dd-environment` — 环保与安全生产（第 14 章）
- `ecm-dd:dd-fundraising` — 募集资金运用（第 15 章）
- `ecm-dd:dd-litigation` — 诉讼、仲裁、行政处罚（第 16 章）
- `ecm-dd:dd-compliance` — 其他合规事项（第 17 章）

**为何同一批**：这 5 个是外部合规性核查，共性是对政府/司法文件的核验（批文/许可证/判决书/处罚决定书），文件类型相似。

**依赖**：BATCH-02 的 `dd-skill-template.md`。

**输出**：5 个 DD skill 目录 + 法规节选。

**特别提示**：`dd-compliance` 是兜底章（第 17 章"其他合规事项"），description 写法要区别于其他具体章节，避免把本该归到 tax/environment 的请求误触发到 compliance。

**验收**：同 BATCH-02。

---

### BATCH-05 — `ecm-dd` 工具类（2 个）

**skill 清单**：
- `ecm-dd:dd-data-verify` — 数据自动化比对（调用 Tushare / 企查查 API 做工商、财务数据交叉验证）
- `ecm-dd:dd-file-review` — 本地文件批量审阅（读取项目文件夹里 PDF/Word/Excel，提取关键字段）

**为何单独一批**：这两个不走"核查+分级+建议"的 DD 标准输出，而是为其他 DD skill 提供底层工具能力。写法更偏技术：需要 Python 脚本和 API 封装。

**依赖**：BATCH-01（它们要读的项目文件夹结构由 setup 建立）；BATCH-11（数据连接器脚本本身可以放这一批里写）。

**输出**：
- `skills/ecm-dd-data-verify/`（含 `scripts/tushare_query.py`、`scripts/qcc_query.py`——从 `54-ecm_skills/scripts/` 迁入并改造）
- `skills/ecm-dd-file-review/`（含通用文件读取脚本）
- 这两个 skill 的 SKILL.md 重点写：**如何被其他 DD skill 调用**、**如何处理 API 缺失情况**（降级为人工核对清单）

**验收**：
- [ ] scripts 可独立运行（带 `--help` 和简单 smoke test）
- [ ] API 密钥通过环境变量注入，不硬编码
- [ ] 无 API 时的 fallback 行为明确

---

### BATCH-06 — `ecm-draft` 文书起草（5 个）

**skill 清单**：
- `ecm-draft:report-assembly` — 拼接 DD 各章节 → 完整尽调报告/律师工作报告
- `ecm-draft:opinion-letter` — 基于 DD 结论生成标准化法律意见书
- `ecm-draft:disclosure-review` — 招股书/重组报告书/权益变动报告书**起草人自查**
- `ecm-draft:meeting-docs` — 会议文件批量起草（通知/议案/决议/记录/签到表）
- `ecm-draft:format-adjust` — Word 格式调整（排版/编号/交叉引用/页眉页脚/目录）

**依赖**：BATCH-02~05 的 DD skill 全部有标准输出格式后再做——因为 `report-assembly` 要知道从哪里拿数据拼接。

**关键设计**：
- `report-assembly` 和 `opinion-letter` 都要定义**结构化输入**（从 DD skill 的输出中读哪些字段），字段定义写进 `shared/schemas/dd-output-schema.json`
- `format-adjust` 是所有 skill 都会用到的末端工具——优先实现好

**输出**：5 个 skill 目录 + `shared/templates/legal-opinion/`（法律意见书模板片段）+ `shared/templates/work-report/`（律师工作报告模板）+ `shared/schemas/dd-output-schema.json`。

**注意事项**：
- `ecm-draft:disclosure-review`（起草人自查）和 `ecm-qc:disclosure-review`（内核独立审查）要互相引用 + 写清边界
- 所有 draft skill 依赖外部 `docx` skill（在 docs/dependencies.md 里已有声明）

**验收**：
- [ ] 5 个 skill 的输入/输出契约与上游 DD skill 对齐
- [ ] 共用的模板片段抽到 shared/templates/
- [ ] `shared/schemas/dd-output-schema.json` 建立
- [ ] `format-adjust` 能被其他 skill 调用

---

### BATCH-07 — `ecm-design` 方案设计（5 个）

**skill 清单**：
- `ecm-design:ipo-path` — IPO 路径选择（源材料较成熟，271 行）
- `ecm-design:deal-structure` — 通用交易结构
- `ecm-design:control-rights` — 控制权交易结构
- `ecm-design:ma-structure` — 上市公司并购
- `ecm-design:cross-border` — 跨境交易方案

**依赖**：无硬依赖，可与其他 batch 并行。

**源材料**：`54-ecm_skills/.claude/skills/ecm-design/` 下同名 .md（其中 ipo-path 最成熟；另外 /var/folders/.../listing-pathway-selection/SKILL.md 是 ipo-path 的同源拷贝，可以参考）。

**关键设计**：
- 5 个 skill 的输出都偏"分析备忘录"格式（不是 checklist），所以要单独约定统一格式（法律备忘录标准排版：楷体_GB2312、小四、段后 18 磅、首行缩进 2 字符——ipo-path 源稿里已有规范）
- 共用的备忘录格式规范抽到 `shared/templates/legal-memo-format.md`

**输出**：5 个 skill 目录 + `shared/templates/legal-memo-format.md`。

**验收**：
- [ ] 5 个 skill 的输出都遵守统一的法律备忘录排版规范
- [ ] ipo-path 的详细源材料完整迁入（不要在迁移过程中精简内容）

---

### BATCH-08 — `ecm-research` 法律研究（3 个）

**skill 清单**：
- `ecm-research:case-search` — 案例检索（裁判文书网/证监会处罚/交易所纪律处分/并购重组委/上市委案例）
- `ecm-research:reg-search` — 法规查询（法律/行政法规/部门规章/规范性文件/交易所业务规则）
- `ecm-research:reg-study` — 法规深度研究（适用性/效力层级/冲突解决/新旧衔接）

**依赖**：无硬依赖。

**源材料**：`54-ecm_skills/.claude/skills/ecm-research/` 下同名 .md（均较简短）。

**关键设计**：
- 三者都是"其他 skill 的辅助工具"，会被 DD skill、design skill、draft skill 反复调用
- description 要把触发关键词做全（否则主 skill 不会自动调用它们）
- 考虑集成 WebSearch 或外部法规检索 API

**输出**：3 个 skill 目录，可能带外部 API 封装脚本。

**验收**：
- [ ] description 能被其他 skill 内的 "先检索一下 xx 案例" 这种请求触发
- [ ] 输出格式（引用、出处、摘要）统一
- [ ] 无法访问外部 API 时的 fallback 明确

---

### BATCH-09 — `ecm-qc` 剩余 4 个 skill

**skill 清单**：
- `ecm-qc:opinion-letter-review` — 法律意见书内核审查
- `ecm-qc:work-report-review` — 律师工作报告内核审查
- `ecm-qc:disclosure-review` — 招股书/重组报告书/权益变动报告书内核审查（和 `ecm-draft:disclosure-review` 边界见下）
- `ecm-qc:meeting-docs-review` — 会议文件内核审查（通知/议案/决议/记录）

**依赖**：BATCH-06 先完成——因为 QC 是对 draft 产物的审查，要知道 draft 输出什么格式。

**模板**：直接参考已有的 `ecm-qc-shareholders-meeting-witness/`——它定义了这一类 skill 的标准样式：
- 三级工作流（交叉比对 / 形式审查 / 实质审查）
- 输出 Word 带 tracked changes + comments
- `w:author` 配置项
- 免责声明引用根 DISCLAIMER

**关键设计**：
- 这 4 个 skill 的 SKILL.md 结构应当高度一致——可以先写一个 `shared/templates/qc-skill-template.md` 抽出共性
- 和 `ecm-draft:disclosure-review` 的边界：draft 版是起草人自查、QC 版是内核独立审查；checklist 重叠但视角、输出声明、修订痕迹的作者名都不同

**输出**：4 个 qc skill 目录 + `shared/templates/qc-skill-template.md`。

**验收**：
- [ ] 4 个 skill 都产出带 tracked changes 的 Word
- [ ] 都统一支持 `w:author` 可配置
- [ ] QC skill 模板文件建立并在 authoring-guide 引用

---

### BATCH-10 — `ecm-workflow` 工作流编排（6 个）

**skill 清单**：
- `ecm-workflow:wf-ipo-full` — 完整 IPO 项目流程
- `ecm-workflow:wf-ipo-dd-full` — 完整 IPO 尽调流程（调用 17 个 DD skill）
- `ecm-workflow:wf-ma-full` — 完整并购流程
- `ecm-workflow:wf-cross-border-ma` — 跨境并购工作流
- `ecm-workflow:wf-issuance` — 再融资流程（定增/配股/可转债）
- `ecm-workflow:wf-nto-listing` — 新三板挂牌流程

**依赖**：**前述所有 batch 都需完成**——workflow 是对其他 skill 的顺序编排，所有被调用的 skill 必须先存在。

**关键设计**：
- workflow 本身不做业务逻辑，只做编排
- 每个 workflow 的 SKILL.md 内容主要是：步骤序列 + 每一步调用哪个 skill + 如何在 skill 之间传递数据
- 不同 workflow 之间有共性（都有 setup → design → dd → draft 骨架），可考虑抽 `shared/workflows/` 里的共用片段

**输出**：6 个 workflow skill 目录。

**验收**：
- [ ] 6 个 workflow 引用到的每个 skill 都已存在（grep 验证）
- [ ] 每个 workflow 都能跑通一个端到端的脑内测试

---

### BATCH-11 — 数据连接器脚本

**内容**：
- `scripts/tushare_connector.py`
- `scripts/qcc_connector.py`
- `scripts/requirements.txt`

**源材料**：`54-ecm_skills/scripts/` 下已有初版。

**依赖**：可与 BATCH-05 合并（dd-data-verify 用这些脚本）。

**输出**：测试过的 Python 脚本 + 文档 `docs/data-connectors.md`。

**验收**：
- [ ] 两个脚本能独立跑通 smoke test
- [ ] API key 走环境变量
- [ ] `requirements.txt` pin 住依赖版本

---

## 独立窗口启动模板（copy-paste 用）

开新窗口做某个 batch 时，把下面这段话发给新窗口的 Claude（把 `<编号>` 替换成实际 batch 编号）：

```
我要做 A-market-ecm-lawyer-plugin 仓库的 BATCH-<编号>。
仓库路径：/Users/zewei/Documents/2024-2044/0-个人事项/0-aplugin

请按顺序工作：

1. 读这 5 个文件了解现状（顺序重要）：
   - docs/project-plan.md                         （头部"当前状态快照"+ BATCH-<编号> 章节）
   - docs/skill-authoring-guide.md                （命名/frontmatter/项目 vs QC 模块约定）
   - shared/terminology/classification-labels.md  （标签体系 single source of truth）
   - shared/templates/project-folder-structure.md （目录结构 single source of truth）
   - skills/ecm-setup-project-init/SKILL.md       （可参考的标准 skill 样板）

2. 源材料位置：/Users/zewei/Documents/2024-2044/0-个人事项/54-ecm_skills/
   - 先用 request_cowork_directory 请求访问
   - iCloud 仅云端文件遇到 "Resource deadlock avoided" 时，改用 Read 工具（host 读取
     绕开 iCloud 锁），不要让用户先手动下载

3. 做 BATCH-<编号> 对应章节里列出的全部 skill，严格遵守：
   - 目录名用 ecm-<category>-<function> 格式
   - SKILL.md frontmatter 含 module / user_role / phase / category / depends_on
   - 跨 skill 共用的东西抽到 shared/，不要在每个 skill 内部重复
   - 不要放单独的 LICENSE（用顶层的）
   - 免责声明引用 ../../DISCLAIMER.md，不复制全文

4. 做完统一更新（不要漏）：
   - docs/project-plan.md 里该 batch 标 ✅
   - README.md 的"当前可用"表格加新行
   - docs/skill-roadmap.md 的状态标 ✅
   - CHANGELOG.md 的 [Unreleased] 段记录
   - .claude-plugin/plugin.json 的 skills 数组 + dependencies（如有新外部依赖）
   - docs/dependencies.md 的 required_by 列表（如有新外部依赖）

5. git commit，message 格式：Add BATCH-<编号>: <简要描述>
   （用户自己 push，你不用 push）

6. 验收：对照 BATCH-<编号> 章节的"验收"checklist 逐条打勾，对照文档尾部
   "每个 batch 的标准交付清单"通用 checklist 再过一遍。
```

## Master 窗口（当前这个窗口）的协调职责

为避免冲突，以下工作**只在 master 窗口做**：

1. **合并 batch 产出**：如果多个 batch 并行，它们都会改 `README.md` / `plugin.json` / `CHANGELOG.md` / `docs/skill-roadmap.md` 这四个文件——可能产生合并冲突。用户把 push 过的 batch commit 回到 master 窗口后，我来统一 resolve。
2. **维护本文件 `docs/project-plan.md`**：状态表、整体节奏、batch 之间的界面调整。
3. **维护 `shared/`**：跨 batch 共用的模板、schema、术语——任何 batch 觉得"这东西好像别人也要用"时，都抛回 master 窗口来放进 shared。
4. **整体测试**：所有 batch 完成后跑一次打包测试（`scripts/package-skill.sh` 遍历所有 skill）、README 的 skill 表和 plugin.json 的 skills 清单对齐、CHANGELOG 汇总出 v1.0.0 发布说明。

## 每个 batch 的标准交付清单（所有 batch 通用）

每个 batch 结束时，必须检查：

- [ ] 新增 skill 目录结构符合 skill-authoring-guide.md
- [ ] SKILL.md frontmatter 完整（name / description / version / license / module / user_role / phase / category / depends_on）
- [ ] description 字段触发关键词密集、覆盖典型请求
- [ ] 若依赖外部 skill（docx/pdf/xlsx），已在 `docs/dependencies.md` 登记
- [ ] 若抽了新的 shared 资源，shared/ 下对应子目录的 README.md 已更新
- [ ] 根 README.md 的"当前可用"表和 skill-roadmap.md 状态表都更新
- [ ] CHANGELOG.md 的 `[Unreleased]` 记录本批变更
- [ ] plugin.json 的 `skills` 数组加上新 skill 路径
- [ ] 本 project-plan.md 里该 batch 标记为 ✅
- [ ] 提交 commit（message：`Add BATCH-<编号>: <简要描述>`）

## 版本发布节奏

| 版本 | 包含内容 | 对应状态 |
|------|---------|---------|
| v0.1.0 | BATCH-00 + BATCH-00.5 | ✅ 已 commit |
| v0.2.0 | BATCH-01（setup 完成） | 待办 |
| v0.5.0 | BATCH-02~05（dd 全部完成） | 待办 |
| v0.7.0 | BATCH-06~09（draft / design / research / qc 完成） | 待办 |
| v1.0.0 | BATCH-10~11（workflow + 连接器完成，全部就绪） | 待办 |

## 更新日志

| 日期 | 变更 |
|------|------|
| 2026-04-24 | 文档初始化，确定 11 个 batch 的划分 |
