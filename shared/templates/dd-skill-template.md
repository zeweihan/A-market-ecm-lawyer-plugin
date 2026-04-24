---
文件类型: DD skill 编写模板
维护者: ecm-dd 系列（BATCH-02 建立）
被哪些 skill 引用:
  - 所有 ecm-dd-* 业务性 skill（dd-approval / dd-entity / dd-establishment / dd-history /
    dd-shareholders / dd-charter / dd-directors / dd-independence / dd-business /
    dd-related-party / dd-assets / dd-debt / dd-tax / dd-environment / dd-fundraising /
    dd-litigation / dd-compliance）
  - 不适用于工具类 DD skill（dd-data-verify / dd-file-review）——它们走不同契约
本版编制日期: 2026-04-24
---

# ECM DD Skill 统一模板（Single Source of Truth）

本文件是**所有业务性 DD skill** 的统一编写模板。新建 DD skill 时照此结构填空，**不要另起炉灶**。
本模板不覆盖工具类 DD skill（`dd-data-verify`、`dd-file-review`），它们走不同的输入/输出契约。

## 为什么要有这个模板

17 个业务性 DD skill 每一个都要做"核查点 → 审阅发现 → 风险分级 → 建议"这套动作，下游的
`ecm-draft:report-assembly` 要把它们拼成完整律师工作报告。如果每个 skill 自由发挥输出结构，
拼接阶段就要做一次"格式归一"，成本极高。所以**强制所有 DD skill 用同一输出契约**。

---

## 一、frontmatter 规范

```yaml
---
name: ecm-dd-<function>                     # 例：ecm-dd-approval
description: >
  一段密集的中文描述，必须包含：
  1. 本 skill 对应编报规则第 12 号的哪一章（例："第 1 章 本次交易的批准和授权"）
  2. 典型触发关键词（中文 + 英文 + 同义词 + 简称）
  3. 典型输入（哪些客户文件会触发本 skill）
  4. 非触发边界（明确不属于本 skill 的情形，避免与邻近 DD skill 误触发）
  5. 一句话总结触发宽度："即使用户未明确使用 'xxx' 一词，只要涉及 yyy 也应触发"
version: 0.1.0
license: MIT
module: ecm-dd                              # 必填，固定为 ecm-dd
user_role: 项目组律师                        # 必填，业务性 DD skill 固定为"项目组律师"
phase:
  - 尽调阶段                                 # 主要阶段
  - 申报阶段                                 # 很多 DD skill 在反馈阶段还要补充
category:
  - 合规核查                                 # 所有业务性 DD skill 共同类别
depends_on:
  internal_skills:
    - ecm-setup-file-organize               # 所有 DD skill 依赖上游文件归位输出
    - ecm-dd-file-review                    # 如需批量读取 PDF/Word 建议显式依赖（可选）
---
```

### description 写法要点

- **关键词密度**：罗列所有用户可能的中文说法、监管术语、同义词、英文对应、简称
- **明确触发边界**：本 skill 管什么、不管什么（避免把应归 tax 的请求触发到 compliance）
- **不要在 description 里写操作步骤**——那是正文的事

---

## 二、目录结构

```
skills/ecm-dd-<function>/
├── SKILL.md                        # 主文件
├── README.md                       # 可选：面向开发者的简介
├── references/
│   ├── checklist.md                # 【必需】该章节的详细核查要点清单（对标编报规则 + 监管指引）
│   ├── regulations-index.md        # 【必需】本 skill 引用的 shared/regulations/ 条文索引
│   ├── risk-examples.md            # 【可选】典型高/中/低风险案例摘录
│   └── output-sample.md            # 【可选】标准 DD Memo 输出样例
└── scripts/                        # 可选，DD 业务性 skill 通常不需要脚本
```

**重点**：详细法规条文放 `shared/regulations/`，本 skill 只在 `references/regulations-index.md`
里列"引用了哪几条"——不要把长条文拷进 skill 目录。

---

## 三、SKILL.md 正文章节（顺序固定）

```markdown
# ecm-dd-<function>

## 定位与边界

本 skill **负责**：
- {对应编报规则第 N 章的 M 个核查维度}
- 输出统一格式的 DD Memo（核查要点 + 审阅发现 + 风险分级 + 建议）

本 skill **不负责**：
- {明确列出与邻近 DD skill 的边界——例如 dd-shareholders 不管公司章程里的股东权益条款，那归 dd-charter}
- 读取 / 移动客户文件（由 ecm-dd-file-review 和 ecm-setup-file-organize 处理）
- 数据自动化比对（由 ecm-dd-data-verify 处理）

## 免责声明

本 skill 产出的 DD Memo 为工作底稿，不构成最终法律意见。完整免责声明见
[DISCLAIMER.md](../../DISCLAIMER.md)。

## 前置依赖

- 上游 skill：`ecm-setup-file-organize` 已完成（本 skill 读取对应章节目录下的文件）
- 对应目录：`02-尽职调查/02-NN-xxx/` 和 `02-尽职调查/02-17-财务资料/`（如涉及财务数据）
- 对应标签：`{列出本 skill 读取的分类标签}`（见
  [shared/terminology/classification-labels.md](../../shared/terminology/classification-labels.md)）

## 核心工作流（四步）

1. **生成核查要点清单**：照 [references/checklist.md](./references/checklist.md) 生成本项目的核查要点
2. **文件审阅与标注**：对照清单逐一审阅客户文件，记录发现的问题
3. **风险分级**：按下方"统一风险分级口径"给每个问题打高/中/低
4. **结论与建议**：汇总结论，列出待补正事项和建议措施

## 统一风险分级口径

| 级别 | 定义 | 典型情形 |
|------|------|---------|
| **高（红）** | 足以构成发行上市实质性障碍 / 需监管反馈重点回应 / 可能被否决的事项 | {本 skill 场景下的具体例子} |
| **中（黄）** | 程序或文件存在瑕疵，但可通过补充材料、追补决议、出具承诺函等方式整改 | {具体例子} |
| **低（蓝）** | 文件形式瑕疵、笔误、日期小差异、格式不统一等不影响实质的问题 | {具体例子} |

## 输出格式契约（强制）

所有 DD 业务性 skill 必须输出下列结构的 Markdown（后续由 `ecm-draft:report-assembly` 读取拼接）：

```markdown
# DD Memo：{章节标题}

> 项目：{客户简称} | 对应章节：编报规则第 N 章 | 编制日期：YYYY-MM-DD | 编制人：{律师姓名}

## 一、核查要点清单

- [x/空] 要点 1（对应法规依据）
- [x/空] 要点 2（对应法规依据）
- ...

## 二、审阅发现

（逐条列示，每条格式）：

### 发现 1：{简短标题}
- **相关文件**：{文件名}
- **具体问题**：{描述}
- **风险级别**：高 / 中 / 低
- **法规依据**：{《xx法》第 yy 条}

## 三、风险分级汇总

| 编号 | 问题 | 级别 | 所涉文件 | 法规依据 |
|------|------|------|---------|---------|
| 1 | ... | 高 | ... | ... |

## 四、结论与建议

- **总体结论**：{一段话，是否具备本章节层面的发行条件}
- **待补正事项**：
  1. ...
  2. ...
- **建议措施**：
  - 补充材料：...
  - 程序整改：...
  - 披露安排：...
  - 获取承诺函：...

## 五、参考资料

- 本 skill 引用的法规条文：{列出 shared/regulations/ 下的引用文件}
- 本 skill 读取的客户文件：{列出分类标签对应目录下本次审阅的文件}
```

**契约硬性要求**：
1. 一级标题必须是"DD Memo：{章节标题}"——拼接时按一级标题识别章节
2. 必有"核查要点 / 审阅发现 / 风险分级汇总 / 结论与建议 / 参考资料"五个二级标题
3. "风险分级汇总"表格的"级别"列取值必须是"高 / 中 / 低"三选一（拼接时按此聚合风险）
4. 输出文件放到 `02-尽职调查/02-NN-xxx/DD-Memo-{章节}-{YYYYMMDD}.md`

## 与邻近 DD skill 的边界

（每个 skill 自己写一段，说明与相近 skill 的分工。见"定位与边界"章节的"不负责"部分。）

## 常见误用 / FAQ

（可选）

## 变更规则

- **输出契约变动**：MAJOR，要同步更新 `shared/templates/dd-skill-template.md` 和
  `ecm-draft:report-assembly` 的输入解析逻辑
- **checklist 条目变动**：MINOR，在本 skill 的 CHANGELOG 段落记录
- **法规引用版本更新**：PATCH，仅在 `shared/regulations/` 改动即可
```

---

## 四、checklist.md 编写规范

每个 DD skill 的 `references/checklist.md` 必须包含：

1. **核查要点逐条列出**，格式：`- [ ] 要点描述（法规依据：xxx）`
2. **核查要点分组**：一般按"程序合法性 / 文件齐备性 / 实质合规性"三个维度分组
3. **每个要点对应 `shared/regulations/` 的具体条文锚点**（如 `../../../shared/regulations/公司法-2024.md#第N条`）

---

## 五、与其他 skill 的交互约定

### 输入端（来自上游 skill）

- 通过 `文件索引表.md`（由 `ecm-setup-file-organize` 生成）找到本章节应审阅的文件清单
- 通过 `02-尽职调查/02-NN-xxx/` 目录直接读取文件（优先 PDF/Word/Excel）
- 若缺少特定文件，**不要自行臆造**，在"审阅发现"里记一条"文件缺失，建议客户补充：xxx"

### 输出端（交给下游 skill）

- `ecm-draft:report-assembly` 读取本 skill 输出的 DD Memo，按一级标题拼接成《律师工作报告》的对应章节
- `ecm-draft:opinion-letter` 读取风险分级汇总表，提取"高"风险事项纳入意见书的"特别事项提示"
- `ecm-qc:work-report-review` 审阅拼接后的报告时，会反向定位到本 skill 生成的 Memo

---

## 六、开发 checklist（新建或修改 DD skill 时过一遍）

- [ ] frontmatter 的 9 个字段（name/description/version/license/module/user_role/phase/category/depends_on）完整
- [ ] description 含本章节号、触发关键词、非触发边界
- [ ] "定位与边界"的"不负责"段列出与邻近 DD skill 的分工
- [ ] 输出契约的五个二级标题齐全
- [ ] 风险分级口径里有本 skill 场景的具体例子（不要照抄模板里的占位文字）
- [ ] `references/checklist.md` 已建立，条目带法规依据
- [ ] `references/regulations-index.md` 已建立，列出引用的 `shared/regulations/` 文件
- [ ] 所有法规条文长文本都在 `shared/regulations/` 下，本 skill 目录不重复存
- [ ] `scripts/package-skill.sh` 打包成功

---

## 七、版本

| 日期 | 变更 |
|------|------|
| 2026-04-24 | 模板初版（BATCH-02 建立） |
