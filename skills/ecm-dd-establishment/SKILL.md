---
name: ecm-dd-establishment
description: >
  资本市场尽职调查 Skill：发行人的设立核查（对应《编报规则第 12 号》第 3 章）。
  当用户提到以下场景时触发：发起人协议、出资协议、出资方式、货币出资、非货币出资、实物出资、
  知识产权出资、土地使用权出资、股权出资、债权出资、验资报告、资产评估报告、创立大会、
  设立时章程、整体变更、有限变股份、净资产折股、股份公司设立、发起设立、募集设立、
  establishment DD、incorporation check、历史出资瑕疵、出资不实、抽逃出资、虚假出资、
  出资纠正、已补缴出资证明等。
  典型输入：发起人协议、出资凭证、验资报告、评估报告、创立大会决议、设立时工商档案、
  整体变更时的审计基准日报告、净资产折股方案。
  非触发边界：设立后的历次股本变动归 ecm-dd-history；现行章程合规性归 ecm-dd-charter；
  股东身份穿透归 ecm-dd-shareholders。
  即使用户只说"这家公司当年是怎么设立的"，只要涉及设立合法性与出资真实性，也应触发本 skill。
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

# ecm-dd-establishment

## 定位与边界

本 skill **负责**：
- 发起人 / 股东资格核查
- 设立协议 / 发起人协议 / 设立决议
- 出资方式、出资比例、出资真实性、实缴到位（含验资报告审阅）
- 非货币出资的权属转移和评估合规性
- 创立大会程序（股份公司）
- 有限责任公司整体变更为股份有限公司的净资产折股、审计评估、税务处理
- 设立环节历史瑕疵的识别和补正方案

本 skill **不负责**：
- 设立后的股本变动（增资 / 减资 / 股权转让）（归 `ecm-dd-history`）
- 现行公司章程的合规性（归 `ecm-dd-charter`）
- 股东 / 实际控制人穿透（归 `ecm-dd-shareholders`）
- 设立时的税务（归 `ecm-dd-tax`，BATCH-04；本 skill 仅记"是否有税务处理"，不深核）

## 免责声明

见 [DISCLAIMER.md](../../DISCLAIMER.md)。

## 前置依赖

- 上游：`ecm-setup-file-organize`
- 对应目录：`02-尽职调查/02-03-历史沿革/`（与 history 合并目录，但 Memo 独立）
- 对应标签：`establishment`

## 核心工作流（四步）

1. **生成核查要点清单**
2. **文件审阅与标注**（按时间线复原设立过程；核对出资、验资、评估、工商设立四条轨迹）
3. **风险分级**
4. **结论与建议**

## 统一风险分级口径

| 级别 | 定义 | 本 skill 场景的典型例子 |
|------|------|------------------------|
| **高（红）** | 实质性障碍 | 虚假出资、抽逃出资、关键非货币出资未办权属转移、整体变更时净资产为负、发起人人数不足 2 人或超过 200 人（股份公司）、创立大会未召开 / 未形成有效决议 |
| **中（黄）** | 瑕疵但可补正 | 验资报告未盖章 / 签字不全、非货币出资评估报告使用期限届满、出资期限超过 5 年（2024 新法）、工商设立登记时间滞后于决议 |
| **低（蓝）** | 形式瑕疵 | 发起人协议个别页缺签字、设立时章程版本表述与工商档案版本小差异、验资报告附件顺序错乱 |

## 输出格式契约（强制）

严格遵循 [shared/templates/dd-skill-template.md](../../shared/templates/dd-skill-template.md)。
落地：`02-尽职调查/02-03-历史沿革/DD-Memo-发行人设立-{YYYYMMDD}.md`

（与 `ecm-dd-history` 各自独立 Memo，都落到同一章节目录下）

## 参考资料索引

- [references/checklist.md](./references/checklist.md)
- [references/regulations-index.md](./references/regulations-index.md)

## 变更规则

- 输出契约变动 → MAJOR
- checklist 条目增删 → MINOR
- 法规版本更新 → PATCH
