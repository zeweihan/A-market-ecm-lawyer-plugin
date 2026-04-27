---
name: ecm-dd-approval
description: >
  资本市场尽职调查 Skill：本次发行 / 交易的批准和授权核查（对应《编报规则第 12 号》第 1 章）。
  当用户提到以下场景时触发：核查发行决议、股东会 / 股东大会决议、董事会决议、审议程序、
  表决比例、召集通知、授权期限、发改委立项、商务部批文、国资委批复、外商投资审批、反垄断申报、
  国家安全审查、本次交易是否合规、批准文件是否齐全、审批流程合规性、IPO 发行决议合法性核查、
  再融资 / 并购 / 重组的批准授权 DD、approval DD、authorization check、审议程序瑕疵等。
  典型输入：董事会决议、股东（大）会决议、政府批文、国资备案、外商投资审批、立项批复等文件。
  非触发边界：本 skill 只管"本次发行 / 交易"的批准和授权，不管历次股本变动的批准（归
  ecm-dd-history）、不管设立时的发起人协议和创立大会（归 ecm-dd-establishment）、
  不管三会日常运作（归 ecm-dd-charter）。
  即使用户未明确说"批准和授权"，只要涉及本次发行 / 交易决议合法性的问题，也应触发本 skill。
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

# ecm-dd-approval

## 定位与边界

本 skill **负责**：
- 核查本次发行 / 交易的内部决议（董事会、股东会 / 股东大会）的召集通知、召开程序、表决比例、决议内容
- 核查外部批准（发改委立项 / 备案、商务部门批复、国资备案、反垄断申报、国家安全审查等）
- 核查授权的有效期和授权范围是否覆盖实际发行 / 交易方案
- 出具编报规则第 1 章对应的 DD Memo

本 skill **不负责**：
- 历次股本变动所涉决议（归 `ecm-dd-history`）
- 设立时的发起人协议、创立大会决议（归 `ecm-dd-establishment`）
- 三会日常运作的规范性（归 `ecm-dd-charter`）
- 政府处罚决定书（归 `ecm-dd-litigation`）
- 文件读取和搬运（归 `ecm-dd-file-review` / `ecm-setup-file-organize`）

## 免责声明

本 skill 产出的 DD Memo 为工作底稿，不构成最终法律意见。完整免责声明见
[DISCLAIMER.md](../../DISCLAIMER.md)。

## 资深律师执行标准

执行本 skill 时，必须同时遵循 [senior-lawyer-execution-standards.md](../../shared/templates/senior-lawyer-execution-standards.md)。本 skill 的任何输出不得突破四条底线：事实可追溯、法源可核验、风险可分级、建议可落地；无法核验时必须显式标注。

## 本 skill 的实务加固点

- **决策链闭环**：必须按董事会/股东会/国资或外部主管审批/授权有效期四层核对，不得只看最终决议。
- **方案一致性**：决议中的发行对象、数量、价格、募集资金、交易对方、标的资产必须与申报方案逐项比对。
- **高风险触发器**：缺少特别决议、关联方未回避、授权过期、审批主体错误或国资/外资审批缺失，应直接列为高风险。
- **补正路径**：每项瑕疵必须说明可否重新开会、补充授权、取得主管确认或只能作为发行障碍处理。

## 前置依赖

- 上游：`ecm-setup-file-organize` 已完成，`文件索引表.md` 可用
- 对应目录：`02-尽职调查/02-01-批准和授权/`
- 对应标签：`approval`（见
  [shared/terminology/classification-labels.md](../../shared/terminology/classification-labels.md)）

## 核心工作流（四步）

1. **生成核查要点清单**：照 [references/checklist.md](./references/checklist.md) 输出本项目的核查清单
2. **文件审阅与标注**：对照清单逐一审阅 `02-01-批准和授权/` 目录下的决议、批文，重点比对
   召集通知日期、决议内容、表决比例、签字盖章、日期逻辑
3. **风险分级**：按下方口径给每个问题打高 / 中 / 低
4. **结论与建议**：汇总已取得的批准授权，列明缺失事项及补正建议

## 统一风险分级口径

| 级别 | 定义 | 本 skill 场景的典型例子 |
|------|------|------------------------|
| **高（红）** | 足以构成发行 / 交易的实质性障碍 | 缺少必需的股东大会特别决议、重大资产重组未经股东大会批准、涉及国有资产未履行国资审批、决议授权范围明显不覆盖实际发行方案 |
| **中（黄）** | 程序或文件存在瑕疵但可补正 | 召集通知期限不足（股份公司股东大会应 20 日前通知，临时会议 15 日前）、独立董事事前认可未记载、关联董事 / 股东未回避表决 |
| **低（蓝）** | 不影响实质的形式瑕疵 | 决议签字页个别董事签字位置错误、附件编号与正文不一致、盖章稍有模糊 |

## 输出格式契约（强制）

严格遵循 [shared/templates/dd-skill-template.md](../../shared/templates/dd-skill-template.md) 的
"输出格式契约"五段式结构：

1. 一级标题：`# DD Memo：本次交易的批准和授权`
2. 二级标题：`一、核查要点清单` / `二、审阅发现` / `三、风险分级汇总` / `四、结论与建议` / `五、参考资料`
3. 风险等级列取值限"高 / 中 / 低"
4. 输出落地：`02-尽职调查/02-01-批准和授权/DD-Memo-批准和授权-{YYYYMMDD}.md`

## 参考资料索引

- [references/checklist.md](./references/checklist.md)——核查要点详细清单
- [references/regulations-index.md](./references/regulations-index.md)——本 skill 引用的法规条文索引

## 变更规则

- 输出契约变动 → MAJOR（同步改 `shared/templates/dd-skill-template.md` 和 `ecm-draft:report-assembly`）
- checklist 条目增删 → MINOR
- 法规版本更新 → PATCH（仅改 `shared/regulations/`）
