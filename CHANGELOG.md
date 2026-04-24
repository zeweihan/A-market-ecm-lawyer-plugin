# Changelog

本仓库遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 约定，版本号遵循 [SemVer 2.0](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added — BATCH-06（ecm-draft 五件套 + DD→Draft 契约 + 3 份格式规范）
- `shared/schemas/dd-output-schema.md`：**DD → Draft 数据交接契约 Single Source of Truth**。冻结 17 份 DD Memo 的五段式二级标题、风险级别枚举（`高 / 中 / 低`）、风险汇总表 5 列定义、一级标题 → 章节号映射（NN=01-17 + skill 对应关系）、Memo 落地路径模式（`02-尽职调查/02-NN-xxx/DD-Memo-{章节}-{YYYYMMDD}.md`）、元信息引用块字段（company_short_name / chapter_no / issue_date / lawyer_name / skill_version）、拼接层语义（章节顺序、章节号转换、风险聚合、缺章处理）、opinion-letter 消费规则（`级别=高` 事项自动注入"特别事项提示"）、违约处理（不得静默纠正）；17 个业务性 `ecm-dd-*` skill + 2 个 `ecm-draft-*` 消费方 skill 共同遵守。**契约的字段增删改均为 MAJOR 变更**。
- `shared/schemas/README.md`：schemas/ 目录的使用规范，说明用 Markdown 而非 JSON Schema 的原因（需同时约束"输出 Markdown 结构"和"结构化字段"）。
- `shared/templates/work-report-format.md`：**律师工作报告 / 尽职调查报告排版规范 SoT**。覆盖首页封面 / 目录 / 引言 / 17 章正文 / 附件 / 签字页；字体字号（封面三号宋体、主标题二号黑体、章标题四号黑体、正文小四宋体）、段落行距 1.5 倍、首行缩进 2 字符；自动章节编号（"第一部分"Heading 1 绑定）、交叉引用规则（禁用"上文 / 下文"）、全项目风险汇总表的 7 列定义（序号 / 所属章节 / 问题 / 级别 / 所涉文件 / 法规依据 / 建议措施）、Markdown → DOCX 映射表、12 类常见踩坑。
- `shared/templates/legal-opinion-format.md`：**法律意见书排版规范 SoT**。强制 5 段骨架（引言 / 释义 / 正文 / 结论性意见 / 特别事项提示）；正文每章节"事实陈述 → 核查工作 → 法律意见"三步法；结论三级（肯定 / 有条件肯定 / 保留）；与工作报告的 11 项强制形式配套要求（律所 / 签字律师 / 日期 / 文号规则 / 编制依据等）；opinion-letter 自动填充指南。
- `shared/templates/meeting-docs-format.md`：**会议文件（通知 / 议案 / 决议 / 记录 / 签到表 / 授权委托书）起草规范 SoT**。覆盖三类会议（股东（大）会 / 董事会 / 监事会）、8 种会议文件结构；通知期限硬校验表（上市公司年会 20 日 / 临时 15 日 / 股份公司股东大会 20 日 / 有限公司章程或 15 日 / 董事会章程或 10 日）；特别决议 / 关联股东回避 / 中小投资者单独计票识别规则；跨文件一致性校验 6 项（通知议案 = 议案文本 = 决议审议 = 表决统计）；表决基数计算规则（区分"占总股本"vs"占出席股东表决权股份总数"vs"扣除关联回避"）；2024 新《公司法》新情况（监事会可选配 / 书面决议制度）。
- `skills/ecm-draft-report-assembly/`：按 dd-output-schema 契约拼接 17 份 DD Memo 成完整《律师工作报告》或《尽职调查报告》。六步工作流：收集校验 Memo → 元信息一致性校验 → 首尾件起草 → 正文拼接 → 全项目风险聚合 → 输出 + 编制说明。配置项：报告类型 / 版本标签 / 项目类型。`references/editorial-basis-template.md`（按项目类型的编制依据标准清单）、`references/assembly-checklist.md`、`references/risk-aggregation-rules.md`（聚合去重排序规则）。
- `skills/ecm-draft-opinion-letter/`：基于 DD Memo 生成法律意见书。六步工作流：形式配套校验 → 扫描 Memo → 起草引言释义 → 起草 17 章意见（事实 - 核查 - 意见三步法）→ 特别事项提示自动注入 + 结论性意见 → 签字页 + 输出。strict / advisory / none 三级形式配套策略。`references/default-definitions.md`（15 条基础释义）、`references/opinion-statements-template.md`（按 17 章分的标准句式模板 + 结论三级措辞）、`references/consistency-checklist.md`。
- `skills/ecm-draft-disclosure-review/`：**起草人自查 skill**（**非**内核审查）。对招股书 / 重组报告书 / 权益变动 / 收购报告书 / 募集说明书等信披文件的法律相关章节做自查：双向交叉比对（信披 → 工作报告、工作报告 → 信披）+ 披露风格审查（夸大 / 避重就轻 / 措辞模糊 / 结论与事实不符 / 未定义缩写 / 引用过时法规）+ 版本 Diff。与 `ecm-qc:disclosure-review`（BATCH-09）视角不同（自查 vs 内核独立审查），输出也不同（Markdown 自查报告 vs 带 tracked changes 的 Word）。`references/disclosure-chapter-map.md`（7 类信披文件的法律相关章节映射）、`references/disclosure-style-checklist.md`（12 类披露风格问题识别规则）、`references/self-review-vs-qc-review.md`（与 QC 边界说明）。
- `skills/ecm-draft-meeting-docs/`：批量起草会议文件（股东（大）会 / 董事会 / 监事会）。六步工作流：追问会议基本信息 → 识别会议属性（通知期、特别决议、关联回避、单独计票）→ 起草各文件 → 跨文件一致性校验 → 通知期限合规校验 → 输出。"议案母版"一致性保证：通知中的议案清单是全套文件的唯一议案源。`references/motion-templates.md`（董事会 / 监事会 / 股东（大）会常见议案模板：年度财报 / 利润分配 / IPO / 再融资 / 修改章程 / 关联交易 / 增减资 / 选举董监事等）、`references/special-resolution-rules.md`（特别决议 / 关联回避 / 中小投资者识别规则）、`references/voting-calc-rules.md`（表决基数计算规则 + 6 类常见错误）。
- `skills/ecm-draft-format-adjust/`：Word 格式调整 skill（Markdown → Word 套版、目录生成 / 更新、页眉页脚、自动编号、交叉引用、表格样式、签字页）。七步工作流。支持四类文档（work-report / legal-opinion / legal-memo / meeting-docs）和 custom 律所模板。所有 Word 操作委托给外部 `docx` skill。`references/markdown-to-word-mapping.md`（段落 / 行内 / 列表 / 表格 / 分页 / 页眉页脚 / 目录 / 交叉引用 / 图片 / 代码块的完整映射表）、`references/format-check-checklist.md`（按文档类型的格式检查 checklist）、`references/docx-skill-invocation-patterns.md`（docx skill 调用模式 + python-docx 兜底脚本示例）。

### Changed — BATCH-06 相关
- `.claude-plugin/plugin.json`：`skills` 数组新增 5 个 `ecm-draft-*` 路径；`dependencies.external_skills.docx.required_by` 追加 5 个 `ecm-draft-*`；`pdf.required_by` 追加 `ecm-draft-disclosure-review`（用于读取信披文件 PDF）。
- `docs/skill-roadmap.md`：5 个 `ecm-draft:*` 状态从 🟡 草稿 改为 ✅ v0.1.0 可用；P3 优先级标注完成；P7 `ecm-qc` 剩余 4 个 skill 状态标注 "BATCH-09 窗口建设中"。
- `docs/project-plan.md`：BATCH-06 标记 ✅；"已建立的跨 skill 共享资源" 清单新增 `work-report-format.md` / `legal-opinion-format.md` / `meeting-docs-format.md` / `dd-output-schema.md`；更新日志追加 BATCH-06 + 09 并行完成记录。
- `shared/templates/README.md`：已建立列表新增 `work-report-format.md` / `legal-opinion-format.md` / `meeting-docs-format.md`；待补充列表中对应三项划勾。

### Added — BATCH-09 占位登记（cross-batch aggregator 代发；实际内容由 BATCH-09 窗口交付）
- `skills/ecm-qc-opinion-letter-review/`（法律意见书内核审查；配对 `ecm-draft:opinion-letter`；BATCH-09 窗口建设中）
- `skills/ecm-qc-work-report-review/`（律师工作报告内核审查；配对 `ecm-draft:report-assembly`；BATCH-09 窗口建设中）
- `skills/ecm-qc-disclosure-review/`（信披文件内核审查；配对 `ecm-draft:disclosure-review`，视角为独立审查而非起草人自查；BATCH-09 窗口建设中）
- `skills/ecm-qc-meeting-docs-review/`（会议文件内核审查；配对 `ecm-draft:meeting-docs`；BATCH-09 窗口建设中）

> **BATCH-09 索引占位说明**：上述 4 个 qc skill 的路径、名称、配对关系已在 README / skill-roadmap 中登记；实际 `skills/ecm-qc-*/` 目录和 SKILL.md 正文由 BATCH-09 独立窗口交付。BATCH-06 作为 aggregator 只为其占位，不动 qc 窗口的 skill 目录。**BATCH-09 窗口在 commit 时不要再碰本 batch 的 6 份共用索引文件**（README / CHANGELOG / plugin.json / skill-roadmap / project-plan / shared/templates/README.md），只改自己的 `skills/ecm-qc-*/` 目录和本批专属 shared 资源（如 `shared/templates/qc-skill-template.md`）。qc skill 目录建好后，`plugin.json` 的 `skills` 数组和 README 的"当前可用"表由 BATCH-09 窗口追加条目即可（本 batch 未提前加 plugin.json 的 qc 路径，避免目录不存在时 plugin 加载失败）。

### Added — BATCH-03（ecm-dd 业务与资产 5 个 skill）
- `skills/ecm-dd-business/`：发行人业务核查（编报规则第 7 章）。覆盖经营范围 / 业务资质 / 特许经营、重大业务合同（签约主体 + change of control + 违约）、前五大客户 / 供应商集中度、业务合规（反垄断 / 数据合规 / 网络安全 / 国家安全审查 / 外资准入 / 产业政策）、业务完整性与连续性。Memo 含**业务资质清单表**和**前五大客户/供应商集中度表**强制字段。
- `skills/ecm-dd-related-party/`：关联交易和同业竞争核查（第 8 章）。双主线工作流：关联方范围认定（关联自然人 + 关联法人 + 12 个月回溯）+ 关联交易公允性 / 决策程序 / 占比 / 重大依赖；同业竞争识别（相同相似业务 + 重大不利影响判断）+ 解决方案（注销 / 转让 / 置入 / 分割 / 承诺）。专门应对 IPO 红线：非经营性资金占用 + 违规担保。Memo 含**关联方清单表 + 关联交易汇总表 + 同业竞争情况表**三张强制表。
- `skills/ecm-dd-assets/`：主要财产核查（第 9 章）。覆盖不动产（国有出让 vs 划拨 vs 集体土地 + 建筑合法性 + 违建识别 + 权利受限）、知识产权（专利 / 商标 / 著作权 / 软著 / 域名 / 商业秘密 / 特许经营权，含职务发明 / 开源合规 / 商标撤三等专项）、重大设备（含融资租赁）、承租资产（含"二房东"与租赁备案）。Memo 含**不动产清单表 + 知识产权清单表 + 重大设备清单表 + 承租资产清单表**四张强制表。
- `skills/ecm-dd-debt/`：重大债权债务核查（第 10 章）。覆盖银行借款 / 授信 / 债券 / 融资租赁 / 保理、对外担保（决策程序 / 反担保 / 占净资产比例 / 违规担保识别）、应收应付账款、或有负债（未决诉讼 + 对赌回购 + 业绩补偿 + 补缴款项）、change of control / 交叉违约 / 财务契约等限制性条款。应对 IPO 红线：非经营性资金占用 + 违规担保。Memo 含**重大借款清单表 + 对外担保清单表 + 大额应收应付清单表 + 或有负债清单表**四张强制表。
- `skills/ecm-dd-independence/`：发行人独立性综合评估（第 4 章）。作为**横向 skill**，依赖 related-party / directors / assets / business / debt 五个上游 DD skill 的输出做五独立评估（资产完整 / 业务独立 / 人员独立 / 财务独立 / 机构独立）。输出与《注册办法》第 12 条逐款对照。Memo 含**五独立对照评估表 + 独立性重大依赖汇总表**两张强制表。

### Changed — BATCH-03 相关
- `.claude-plugin/plugin.json`：`skills` 数组新增 5 个 `ecm-dd-*`（BATCH-03）路径。
- `docs/skill-roadmap.md`：5 个 BATCH-03 `ecm-dd:*` 状态从 🟡 草稿 改为 ✅ v0.1.0 可用。
- `docs/project-plan.md`：BATCH-03 标记 ✅。

### Added — BATCH-04（ecm-dd 合规事项 5 个 skill）
（由 BATCH-04 并行窗口于 2026-04-24 交付；skill 目录位于 `skills/ecm-dd-tax/` / `skills/ecm-dd-environment/` / `skills/ecm-dd-fundraising/` / `skills/ecm-dd-litigation/` / `skills/ecm-dd-compliance/`。完整 skill 清单详述由该窗口在本段补充。）

### Changed — BATCH-04 相关
- `.claude-plugin/plugin.json`：`skills` 数组新增 5 个 `ecm-dd-*`（BATCH-04）路径。
- `docs/skill-roadmap.md`：5 个 BATCH-04 `ecm-dd:*` 状态从 🟡 草稿 改为 ✅ v0.1.0 可用。
- `docs/project-plan.md`：BATCH-04 标记 ✅。

### Added — BATCH-05（ecm-dd 工具类 2 个 skill）
（由 BATCH-05 并行窗口于 2026-04-24 交付；skill 目录位于 `skills/ecm-dd-data-verify/`（Tushare / 企查查 API 交叉验证）和 `skills/ecm-dd-file-review/`（本地文件批量审阅）。完整 skill 清单详述由该窗口在本段补充。）

### Changed — BATCH-05 相关
- `.claude-plugin/plugin.json`：`skills` 数组新增 2 个 `ecm-dd-*`（BATCH-05）路径。
- `docs/skill-roadmap.md`：2 个 BATCH-05 `ecm-dd:*` 状态从 🟡 草稿 改为 ✅ v0.1.0 可用。
- `docs/project-plan.md`：BATCH-05 标记 ✅。
- `docs/skill-roadmap.md`：P2 优先级标注"ecm-dd 19 章 / 19 个 skill 全部完成"。

### Added — BATCH-08（ecm-research 三件套）
- `skills/ecm-research-case-search/`：案例检索 skill。覆盖五类权威数据源（中国裁判文书网 / 证监会行政处罚 / 三大交易所及新三板纪律处分 / 并购重组委审议 / 上市委审议与 IPO 审核问询），4-Phase 工作流（澄清 → 策略制定 → 执行检索 → 结构化输出）；内含 `references/case-source-registry.md`（数据源登记 + 已知坑）、`references/case-card-template.md`（裁判 / 处罚 / 纪律处分 / 审议意见四类案例卡片字段模板）、`references/search-keyword-patterns.md`（20 个高频 ECM 主题的关键词矩阵预设）。
- `skills/ecm-research-reg-search/`：法规检索 skill。按**五级效力层级**（法律 / 行政法规 / 部门规章 / 规范性文件 / 交易所业务规则）分层检索 + Phase 3 时效性核验（现行有效 / 已修订 / 已废止 / 事实失效 / 部分修订）。内含 `references/regulation-source-registry.md`（flk.npc.gov.cn、证监会规章库、各交易所规则专区）、`references/effect-status-rules.md`（时效性判断方法 + 常见陷阱 + 五级标注格式）、`references/citation-format.md`（规范引证格式）、`references/core-regulations-map.md`（20 个 ECM 高频主题的法规速查表）。
- `skills/ecm-research-reg-study/`：法规深度研究 skill。在已有法规清单基础上做**效力层级图 + 一般 / 特别 / 新 / 旧关系分析 + 冲突识别与解决 + 新旧衔接 + 适用性结论**五段式 5-Phase 工作流；支持在需要时回调 `ecm-research-reg-search` 和 `ecm-research-case-search`。内含 `references/hierarchy-framework.md`（中国法律规范效力层级完整框架）、`references/conflict-resolution-rules.md`（8 类典型冲突的解决规则库）、`references/transition-analysis-framework.md`（新旧衔接分析 + 年份标志速查）、`references/applicability-analysis-template.md`（单一条款 / 法律框架 / 新旧衔接三类研究主题的分析模板）。
- `shared/templates/research-output-format.md`：**全仓唯一权威**的法律研究类 skill 统一输出格式。规定：(1) 可靠性四级分类（A 官方原始 / B 官方汇编 / C 公开二手 / D 模型记忆）；(2) 法规引证格式（全称 + 文号 + 生效日期 + 效力状态）和案例引证格式（案号 + 当事人 + 审级 + 终审状态）；(3) 四段式外层结构（检索策略 / 核心结论 / 支撑材料 / 时效性局限 / 下一步建议）；(4) 三层 fallback 规则（shared/regulations/ 节选 → 用户上传 → 模型记忆 D 级标注，绝不编造）；(5) 跨 skill 数据交接 JSON schema。所有 `ecm-research-*` skill 和下游引用 research 结果的 skill 必须遵循。

### Changed — BATCH-08 相关
- `.claude-plugin/plugin.json`：`skills` 数组新增 3 个 `ecm-research-*` 路径。
- `docs/skill-roadmap.md`：3 个 `ecm-research:*` 状态从 🟡 草稿 改为 ✅ v0.1.0 可用；P5 优先级标注完成。
- `docs/project-plan.md`：BATCH-08 标记 ✅；"跨 skill 共享资源"清单新增 `shared/templates/research-output-format.md`。
- `shared/templates/README.md`：已建立列表新增 `research-output-format.md`。

### Added — BATCH-07（ecm-design 五件套）
- `skills/ecm-design-ipo-path/`：IPO 路径选择 skill。完整迁入 54-ecm_skills 中 271 行的成熟源稿，含三维影响分析（股东利益 / 管理层 / 公司发展）、12 个比较维度、6 阶段工作流、外部检索优先级（企查查 MCP → Tavily → Web Search）、6 种典型场景处理指引；内含 `references/pathway-rules.md`（A 股各板块 + 港股 18A/18C + 美股 + 红筹 / VIE + 借壳 + 被并购 + SPAC 的规则速查）。
- `skills/ecm-design-deal-structure/`：通用交易结构设计 skill。覆盖股权 / 资产 / 增资 / 合并 / 分立五类交易的结构选型、一步 vs 分步、现金 / 股权 / 混合对价、CP 清单、风险缓释工具（对赌、锁定期、Escrow、W&I）。
- `skills/ecm-design-control-rights/`：控制权交易结构 skill。四类目标识别（获取 / 巩固 / 分配 / 退出）、股权穿透、要约豁免、一致行动 / 表决权委托 / AB 股 / 反收购条款、多股东共建治理。
- `skills/ecm-design-ma-structure/`：上市公司并购 skill。交易性质判定三分叉（一般 / 重大 / 借壳）、支付工具对比、配套融资、锁定期分层（36 / 12 月 / 业绩承诺期）、业绩承诺与补偿公式、近年监管关注点。
- `skills/ecm-design-cross-border/`：跨境交易 skill。六跨境维度识别、7 个主管部门 + 10 部核心法规总览、红筹 / VIE 搭建与拆除、ODI / FDI / 37 号文 / 境外上市备案 / 反垄断 / 国安 / 数据出境的触发点与时间线。
- `shared/templates/legal-memo-format.md`：**全仓唯一权威**的法律备忘录排版规范（首页元信息、主标题与各级标题、正文段落、表格样式、数字格式、法规引用、Markdown → DOCX 映射、常见踩坑清单）。所有 `ecm-design:*` 输出的备忘录必须遵循；未来其他备忘录类输出亦可复用。

### Changed — BATCH-07 相关
- `docs/dependencies.md`：`docx` 外部 skill 的 `required_by` 列表追加 5 个 `ecm-design-*`（用于最终套版为 `.docx` 终稿）。
- `.claude-plugin/plugin.json`：`skills` 数组新增 5 个 `ecm-design-*` 路径；`dependencies.external_skills.docx.required_by` 同步更新。
- `docs/skill-roadmap.md`：5 个 `ecm-design:*` 状态从 🟡 草稿 改为 ✅ v0.1.0 可用。
- `docs/project-plan.md`：BATCH-07 标记 ✅；跨 skill 共享资源清单新增 `shared/templates/legal-memo-format.md`。
- `shared/templates/README.md`：已建立列表新增 `legal-memo-format.md`；待补充列表新增 `work-report-format.md` / `legal-opinion-format.md` / `dd-skill-template.md` / `qc-skill-template.md` 占位。

### Added — BATCH-02（ecm-dd 公司基础面 7 个 skill）
- `skills/ecm-dd-approval/`：本次发行 / 交易的批准和授权核查（编报规则第 1 章）。覆盖董事会 / 股东（大）会决议、独立董事事前认可、国资 / 发改 / 商务 / 反垄断 / 国安审查等外部批准、授权有效期与授权范围。
- `skills/ecm-dd-entity/`：发行人主体资格核查（第 2 章）。覆盖营业执照、工商登记、经营异常 / 失信黑名单、36 个月未擅自发行 / 未被交易所谴责 / 未被立案的《注册办法》第 10 条消极条件、特殊行业基础资质。
- `skills/ecm-dd-establishment/`：发行人设立核查（第 3 章）。覆盖发起人资格、出资方式、验资、非货币出资评估 / 权属转移、整体变更（有限变股份）的净资产折股与税务处理、设立环节历史瑕疵识别与补正。
- `skills/ecm-dd-history/`：股本及其演变核查（第 6 章）。按时间线复原历次增资 / 股转 / 回购 / 员工持股 / 激励，每次变动核查六要素（决议 / 协议 / 定价 / 付款 / 工商 / 税务）；国资审批、外汇登记、代持清理专章。Memo 含"股本演变时间线表"强制字段。
- `skills/ecm-dd-shareholders/`：股东与实控人核查（第 5 章）。持股 5% 以上股东身份穿透、出资来源、代持清理、三类股东专项、股权质押冻结、实控人认定（单一自然人 / 共同控制 / 一致行动 / 国资 / 无实控）、近 2 年控制权稳定。Memo 含"股权结构图 + 实控人穿透图"强制字段。
- `skills/ecm-dd-charter/`：公司章程及组织机构核查（第 11 章）。章程本体合法性、三会议事规则、近 3 年三会召开规范性、独立董事和董事会专门委员会运行、内控制度完备性；特别关注 2024 新《公司法》衔接。
- `skills/ecm-dd-directors/`：董监高核查（第 12 章）。《公司法》第 146 条消极条件、证监会市场禁入、36 个月 / 12 个月监管处分、兼职与对外投资、近亲属关系、报告期内变化、承诺事项。Memo 含"董监高花名册"强制字段。
- `shared/templates/dd-skill-template.md`：**DD 业务性 skill 统一编写模板**。规定 frontmatter 字段、目录结构、"核查要点 + 审阅发现 + 风险分级 + 结论建议 + 参考资料"五段式输出契约（强制）、checklist 编写规范、与上下游 skill 的交互约定。**BATCH-03 / 04 的 10 个 DD skill 必须套用本模板**。
- `shared/regulations/编报规则第12号-2001.md`：17 章大纲索引，建立 DD skill 与各章节的映射关系；与《公司法》《注册办法》交叉条文标注。
- `shared/regulations/公司法-2024.md`：2024 年 7 月 1 日施行版本的高频条款节选（第 4/7/8/46/47/48/49/56/66/84/92/94/97/112/116/119/130/140/146/180/181/265 条）。
- `shared/regulations/首次公开发行股票注册管理办法-2023.md`：第二章"发行条件"的第 7–15 条节选，建立发行条件与 DD skill 的映射索引。

### Changed — BATCH-02 相关
- `.claude-plugin/plugin.json`：`skills` 数组新增 7 个 `ecm-dd-*` 路径。
- `docs/skill-roadmap.md`：7 个 `ecm-dd:*` 状态从 🟡 草稿 改为 ✅ v0.1.0 可用；P2 优先级注明部分完成。
- `docs/project-plan.md`：BATCH-02 标记 ✅；"跨 skill 共享资源"清单新增 `dd-skill-template.md` 和 3 份法规节选。
- `docs/skill-authoring-guide.md`：新增"DD skill 专用模板"一节，指向 `shared/templates/dd-skill-template.md`。
- `shared/regulations/README.md`：待补充清单中《公司法》《首次公开发行股票注册管理办法》《编报规则第 12 号》勾选完成。

### Added — BATCH-01（ecm-setup 三件套）
- `skills/ecm-setup-project-init/`：项目初始化 skill。追问最多 4 轮确认项目类型/境内跨境/板块/客户简称；物理创建标准项目目录；根据项目类型输出 skill 调用 roadmap。内含 `references/project-roadmaps.md`（IPO/并购/再融资/新三板/债券 5 种类型 + 通用 roadmap）。
- `skills/ecm-setup-file-classify/`：文件批量分类 skill。扫描 `02-99-未分类文件/` 目录，调用 `pdf`/`docx`/`xlsx` 外部 skill 读取内容，为每个文件打 1-3 个标签（many-to-many），主动提示版本重复/类别缺失/标签过多。
- `skills/ecm-setup-file-organize/`：文件归位 skill。按 classify 结果默认 `copy` 到对应 DD 章节目录（多标签文件复制到多个目录），生成 `文件索引表.md` 作为下游 DD skill 的统一入口；支持 `move`/`symlink` 备选策略但需显式确认。
- `shared/terminology/classification-labels.md`：**全仓唯一权威**的 19 个分类标签定义。未来所有 ecm-dd-* skill、file-classify、file-organize 统一引用本文件，不得自行定义。
- `shared/templates/project-folder-structure.md`：**全仓唯一权威**的项目目录结构 + 标签→目录映射表 + 项目类型变体目录 + 可直接执行的 `mkdir -p` 命令段。

### Added — 其他
- `docs/project-plan.md`：总工作计划。把 40+ 个 skill 的建设切成 11 个可独立完成的 batch，每个 batch 自带依赖清单、输入输出、验收标准和独立窗口启动模板，支持并行推进。
- 新增 `ecm-qc` 模块（第 7 个 skill 类），用于承载内核 / QC 团队使用的审查类 skill。模块和既有 6 类项目 skill（setup/design/dd/draft/research/workflow）并列但语义独立——项目组 skill 是"做事"，QC skill 是"审事"。

### Changed
- `docs/dependencies.md`：更新 `docx` / `pdf` / `xlsx` 三个外部 skill 的 `required_by` 列表，登记 `ecm-setup-file-classify` 新引入的依赖。
- `.claude-plugin/plugin.json`：`skills` 数组新增 3 个 ecm-setup 路径，`dependencies.external_skills` 同步更新。
- 在 `docs/skill-authoring-guide.md` 和 `README.md` 顶部明确划出**项目 skill / QC skill** 的使用者边界。
- SKILL.md frontmatter 增加 `module` 和 `user_role` 两个必填字段，防止角色混淆。
- `ecm-qc` 类下规划了 4 个未来 skill：`opinion-letter-review`、`work-report-review`、`disclosure-review`、`meeting-docs-review`。

### Changed
- 把首个 skill `shareholders-meeting-witness-review` 重命名为 `ecm-qc-shareholders-meeting-witness`（`git mv` 方式保留历史），归入新的 `ecm-qc` 模块。
- 同步更新 `plugin.json` / `README` / `skill-roadmap` / `skill-authoring-guide` / `CONTRIBUTING` / `docs/dependencies` / `docs/installation` / `scripts/package-skill.sh` / `.github/` 模板中对该 skill 的所有引用。
- `docs/skill-roadmap.md` 里移除"命名统一化待办"章节（决定已落地）。

---

## [0.1.0] - 2026-04-24

### Added
- 仓库初始框架：
  - 顶层 `LICENSE` (MIT)、`README.md`、`DISCLAIMER.md`、`CONTRIBUTING.md`、`CHANGELOG.md`、`VERSION`
  - `.claude-plugin/plugin.json` 插件元数据
  - `.github/` Issue 与 PR 模板
  - `docs/` 文档（依赖说明、安装指引、skill 编写规范、规划路线图）
  - `shared/` 跨 skill 共享资源目录（regulations / terminology / templates）
  - `scripts/package-skill.sh` 打包工具
- 首个 skill：`shareholders-meeting-witness-review`（股东大会见证意见内核审查）

[Unreleased]: https://github.com/zeweihan/A-market-ecm-lawyer-plugin/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/zeweihan/A-market-ecm-lawyer-plugin/releases/tag/v0.1.0
