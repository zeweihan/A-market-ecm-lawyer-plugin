---
name: ecm-dd-entity
description: >
  资本市场尽职调查 Skill：发行人 / 目标公司的主体资格核查（对应《编报规则第 12 号》第 2 章）。
  当用户提到以下场景时触发：核查营业执照、工商登记档案、企业信用信息公示、存续状态、经营异常
  名录、税务非正常户、年报异常、经营范围与实际业务的匹配、外商投资企业批准证书、组织机构代码证、
  主体资格合法性、36 个月内违法违规排查、公司名称 / 住所 / 注册资本 / 法定代表人 / 营业期限、
  特殊行业经营许可证（金融、医疗、教育、出版、烟草、危化品、建筑、电信增值等）、entity DD、
  existence check、subject qualification 等。
  典型输入：营业执照、工商登记档案、企业信用报告、特殊行业许可证、历年年报。
  非触发边界：历史沿革（增资 / 股转）归 ecm-dd-history；设立时的出资 / 验资归 ecm-dd-establishment；
  公司章程本身归 ecm-dd-charter；业务经营资质归 ecm-dd-business。
  即使用户只说"帮我看看这家公司有没有问题"，只要针对主体身份合法性，也应触发本 skill。
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
    - ecm-dd-data-verify
---

# ecm-dd-entity

## 定位与边界

本 skill **负责**：
- 核查发行人 / 目标公司的合法存续状态（营业执照、工商登记、经营异常 / 税务非正常户等）
- 核查基本工商信息与申报文件 / 实际经营的一致性
- 核查 36 个月内未擅自发行证券、未受交易所公开谴责、未被立案调查的消极条件（《注册办法》第 10 条）
- 核查从事现有业务所需的基础特许经营资质是否齐备（仅限"主体身份"层面的资质；具体业务合规核查归 `ecm-dd-business`）

本 skill **不负责**：
- 历次股权变动（归 `ecm-dd-history`）
- 设立时的出资 / 验资 / 评估（归 `ecm-dd-establishment`）
- 公司章程条款合规性（归 `ecm-dd-charter`）
- 业务 / 资质的深度合规（归 `ecm-dd-business`）
- 分支机构和子公司的单独核查（并表范围内的主要子公司另行调用本 skill 做子维度核查）

## 免责声明

本 skill 产出的 DD Memo 为工作底稿，不构成最终法律意见。完整免责声明见
[DISCLAIMER.md](../../DISCLAIMER.md)。

## 资深律师执行标准

执行本 skill 时，必须同时遵循 [senior-lawyer-execution-standards.md](../../shared/templates/senior-lawyer-execution-standards.md)。本 skill 的任何输出不得突破四条底线：事实可追溯、法源可核验、风险可分级、建议可落地；无法核验时必须显式标注。

## 本 skill 的实务加固点

- **主体存续核验**：营业执照、工商档案、章程、信用信息和监管状态必须交叉验证主体是否依法有效存续。
- **资格边界**：区分发行人主体资格、业务资质、股东资格和董监高资格，发现邻近问题应转对应 DD skill。
- **高风险触发器**：吊销/注销风险、经营异常未消除、主体类型不符合发行条件、历史改制主体承继不清，应列高风险。
- **结论约束**：未拿到完整工商档案或章程现行版时，不得出具“主体资格合法有效”的肯定结论。

## 前置依赖

- 上游：`ecm-setup-file-organize` 已完成
- 对应目录：`02-尽职调查/02-02-主体资格/`
- 对应标签：`entity`

## 核心工作流（四步）

1. **生成核查要点清单**：照 [references/checklist.md](./references/checklist.md) 输出本项目的核查清单
2. **文件审阅与标注**：按清单审阅营业执照、工商登记档案、企查查 / 企业信用报告等；
   建议调用 `ecm-dd-data-verify` 交叉验证工商字段
3. **风险分级**
4. **结论与建议**

## 统一风险分级口径

| 级别 | 定义 | 本 skill 场景的典型例子 |
|------|------|------------------------|
| **高（红）** | 足以构成发行 / 交易的实质性障碍 | 被吊销 / 注销 / 列入严重违法失信名单；经营范围完全不覆盖主要收入来源的特许业务；36 个月内擅自公开发行证券 |
| **中（黄）** | 可通过补正解决 | 经营异常名录待移除、年报未及时申报、经营范围表述与实际业务部分不匹配、营业期限即将到期 |
| **低（蓝）** | 形式瑕疵 | 工商登记住所与实际办公地稍有差异但无实质影响、营业执照副本个别信息笔误 |

## 输出格式契约（强制）

严格遵循 [shared/templates/dd-skill-template.md](../../shared/templates/dd-skill-template.md)。
落地路径：`02-尽职调查/02-02-主体资格/DD-Memo-主体资格-{YYYYMMDD}.md`

## 参考资料索引

- [references/checklist.md](./references/checklist.md)
- [references/regulations-index.md](./references/regulations-index.md)

## 变更规则

- 输出契约变动 → MAJOR
- checklist 条目增删 → MINOR
- 法规版本更新 → PATCH
