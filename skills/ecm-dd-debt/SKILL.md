---
name: ecm-dd-debt
description: >
  资本市场尽职调查 Skill：发行人重大债权债务核查（对应《编报规则第 12 号》第 10 章）。
  当用户提到以下场景时触发：重大债权、重大债务、借款合同、流动资金贷款、项目贷款、
  银行授信、综合授信协议、授信额度、表内融资、表外融资、债券、公司债、企业债、中票、
  短融、超短融、PPN、永续债、可转债、ABS、应收账款融资、保理、对外担保、担保合同、
  连带责任保证、一般保证、抵押担保、质押担保、反担保、保证金、大额应收账款、大额应付账款、
  往来款、其他应收、其他应付、资金占用、非经营性资金往来、或有负债、未决诉讼负债、
  重大销售合同、重大采购合同、长期合同、履约风险、违约风险、交叉违约、change of control、
  debt DD、liability DD、contingent liability、off-balance-sheet 等。
  典型输入：借款合同 / 授信协议、对外担保合同、应收 / 应付账款清单、往来款确认函、
  大额债权债务清单、银行流水、或有负债披露、诉讼涉及的债权债务文件、对外投资承诺函、
  或有对价安排（earn-out）、回售条款、优先股 / 带回售权投资协议等。
  非触发边界：应收 / 应付背后的业务合同条款（归 ecm-dd-business）；债权债务涉及的关联方
  （归 ecm-dd-related-party，但本 skill 关注其对外担保额度和资金占用红线）；资产抵押 /
  质押的标的物权属（归 ecm-dd-assets，本 skill 关注主债权合同和担保决策）；债券发行本身
  作为募资手段（归 ecm-design 路径设计）；诉讼 / 仲裁涉及的债权债务（归 ecm-dd-litigation，
  本 skill 关注或有负债金额和会计披露）；债务违约引发的违法行为（归 ecm-dd-compliance）。
  即使用户只说"帮我看看这家公司有没有大额担保"或"应收账款怎么样"，也应触发本 skill。
version: 0.1.0
license: MIT
module: ecm-dd
user_role: 项目组律师
phase:
  - 尽调阶段
  - 申报阶段
  - 反馈阶段
category:
  - 合规核查
depends_on:
  internal_skills:
    - ecm-setup-file-organize
    - ecm-dd-file-review
---

# ecm-dd-debt

## 定位与边界

本 skill **负责**：
- 核查发行人重大借款 / 授信 / 债券 / 其他融资的合同合法性、关键条款（金额、期限、利率、
  担保、违约、加速到期、交叉违约、change of control）
- 核查发行人对外担保的决策程序合规性（阈值触发、股东大会审议）、对外担保的反担保安排、
  担保余额占比
- 核查重大应收 / 应付账款的账龄、坏账准备、争议风险、关联方属性
- 核查银行授信使用情况和可动用额度
- 核查或有负债（未决诉讼负债、对外担保 / 质押 / 抵押、回购 / 回售 / 补偿安排等）
- 核查重大合同对发行人上市 / 并购 / 控制权变更的限制性约束（change of control / 禁止转让）
- 出具编报规则第 10 章对应的 DD Memo

本 skill **不负责**：
- 资产抵押 / 质押的标的物权属本身（归 `ecm-dd-assets`；本 skill 关注主债权合同和担保决策程序）
- 应收 / 应付背后的销售 / 采购业务合同商业条款（归 `ecm-dd-business`）
- 非经营性资金占用 / 违规担保的**关联属性**（归 `ecm-dd-related-party`；本 skill 关注
  额度、决策和红线）
- 涉及诉讼 / 仲裁的债权债务纠纷案件本身（归 `ecm-dd-litigation`，BATCH-04；本 skill 只关注
  或有负债金额与会计披露）
- 债务违约引发的行政处罚（归 `ecm-dd-compliance`，BATCH-04）
- 对赌 / 回购 / 业绩补偿对股权结构的影响（归 `ecm-dd-shareholders`）
- 税务筹划（归 `ecm-dd-tax`）
- 文件读取 / 搬运（归 `ecm-dd-file-review` / `ecm-setup-file-organize`）

## 免责声明

本 skill 产出的 DD Memo 为工作底稿，不构成最终法律意见。完整免责声明见
[DISCLAIMER.md](../../DISCLAIMER.md)。

## 前置依赖

- 上游：`ecm-setup-file-organize` 已完成，`文件索引表.md` 可用
- 对应目录：`02-尽职调查/02-09-重大债权债务/`
- 对应标签：`debt`（见
  [shared/terminology/classification-labels.md](../../shared/terminology/classification-labels.md)）

## 核心工作流（四步）

1. **生成核查要点清单**：照 [references/checklist.md](./references/checklist.md) 输出本项目的核查清单
2. **文件审阅与标注**：对照清单审阅 `02-09-重大债权债务/` 目录下的借款合同、担保合同、
   授信协议、应收 / 应付明细、或有负债清单；重点比对主体适格、金额、期限、利率、担保 /
   反担保、违约条款、change of control 条款、交叉违约条款；必要时调用
   `ecm-dd-data-verify` 对企查查 / 人民银行征信做交叉验证
3. **风险分级**：按下方口径给每个问题打高 / 中 / 低
4. **结论与建议**：汇总重大债权债务状况，评估对本次发行 / 交易的影响，列出清理 / 补正建议

## 统一风险分级口径

| 级别 | 定义 | 本 skill 场景的典型例子 |
|------|------|------------------------|
| **高（红）** | 足以构成发行 / 交易的实质性障碍 | 存在大额逾期债务且形成重大偿债风险；对外担保金额巨大（远超净资产合理比例，如超 50%）且无有效反担保；存在控股股东 / 实控人非经营性资金占用未清理（IPO 红线，零容忍）；存在为控股股东 / 实控人 / 关联方违规担保未清理；重大合同存在触发 change of control 且可能终止；或有负债可能转化为实际负债并对持续经营构成重大影响 |
| **中（黄）** | 程序或文件存在瑕疵但可补正 | 部分借款合同存在限制性条款可能影响本次交易（需取得债权人同意函）；对外担保比例较高但有反担保；大额应收账款账龄偏长但有坏账准备；融资租赁 / 保理合同存在披露缺口；对关联方资金拆借历史存在但已清理并出具承诺函 |
| **低（蓝）** | 不影响实质的形式瑕疵 | 合同文件缺少部分附件；债权债务确认函未全部回函（小额）；合同签字页个别签字位置错误；合同编号 / 印章有形式瑕疵 |

## 输出格式契约（强制）

严格遵循 [shared/templates/dd-skill-template.md](../../shared/templates/dd-skill-template.md) 的
"输出格式契约"五段式结构：

1. 一级标题：`# DD Memo：重大债权债务`
2. 二级标题：`一、核查要点清单` / `二、审阅发现` / `三、风险分级汇总` / `四、结论与建议` / `五、参考资料`
3. 风险等级列取值限"高 / 中 / 低"
4. 输出落地：`02-尽职调查/02-09-重大债权债务/DD-Memo-重大债权债务-{YYYYMMDD}.md`

**额外要求**（本 skill 专属）：

1. Memo 中必须附**重大借款 / 融资清单表**：债权人 / 类型（银行贷款 / 债券 / 融资租赁 /
   保理 / 其他）/ 金额 / 期限 / 利率 / 担保 / 到期日 / 是否逾期 / 限制性条款（特别是
   change of control、禁止转让、交叉违约、财务指标维持约束）
2. Memo 中必须附**对外担保清单表**：被担保人 / 关系（关联 / 子公司 / 第三方）/ 类型
   （保证 / 抵押 / 质押）/ 担保金额 / 期限 / 反担保 / 决策程序 / 占净资产比例
3. Memo 中必须附**大额应收 / 应付账款清单表**（按金额 + 账龄排序）：对手方 / 关系 / 金额 /
   账龄 / 是否计提坏账 / 是否争议 / 是否关联方
4. Memo 中必须附**或有负债清单表**：类型（未决诉讼 / 对外担保 / 回购义务 / 业绩补偿 /
   其他）/ 潜在金额 / 触发条件 / 转化概率 / 会计处理

## 与邻近 DD skill 的边界

| 场景 | 归属 skill | 分工说明 |
|------|-----------|---------|
| 主债权合同 + 担保合同 + 决策程序 | **本 skill** | 本 skill 的核心 |
| 资产抵押 / 质押的标的物权属 | `ecm-dd-assets` | 本 skill 关注主债权；标的物权属归 assets |
| 债权债务的关联属性 | `ecm-dd-related-party` | 本 skill 记录非经营性资金占用红线；关联属性归 related-party |
| 应收 / 应付对应的业务合同条款 | `ecm-dd-business` | 本 skill 关注账龄 / 坏账 / 争议；合同条款归 business |
| 涉及诉讼 / 仲裁的债权债务 | `ecm-dd-litigation`（BATCH-04）| 本 skill 关注或有负债金额；诉讼本体归 litigation |
| 债券发行本身作为融资手段 | `ecm-design-deal-structure` / `ecm-design-ipo-path` | 本 skill 审已发行债券的合同条款；债券发行方案归 design |
| 对赌 / 回购对股权影响 | `ecm-dd-shareholders` | 本 skill 关注或有负债；对股权的影响归 shareholders |

## 参考资料索引

- [references/checklist.md](./references/checklist.md)——核查要点详细清单
- [references/regulations-index.md](./references/regulations-index.md)——本 skill 引用的法规条文索引

## 变更规则

- 输出契约变动 → MAJOR（同步改 `shared/templates/dd-skill-template.md` 和 `ecm-draft:report-assembly`）
- checklist 条目增删 → MINOR
- 法规版本更新 → PATCH（仅改 `shared/regulations/`）
