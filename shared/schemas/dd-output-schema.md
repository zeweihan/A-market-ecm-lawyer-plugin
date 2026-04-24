---
文件类型: DD → Draft 数据交接契约
维护者: BATCH-02 ~ 05（DD skill 侧）+ BATCH-06（ecm-draft 侧）共同遵守
被哪些 skill 引用:
  上游（必须产出符合本契约的 Markdown）:
    - ecm-dd-approval / ecm-dd-entity / ecm-dd-establishment / ecm-dd-history
    - ecm-dd-shareholders / ecm-dd-charter / ecm-dd-directors / ecm-dd-independence
    - ecm-dd-business / ecm-dd-related-party / ecm-dd-assets / ecm-dd-debt
    - ecm-dd-tax / ecm-dd-environment / ecm-dd-fundraising / ecm-dd-litigation / ecm-dd-compliance
    （即 17 个业务性 DD skill；dd-data-verify / dd-file-review 两个工具类不走本契约）
  下游（按本契约解析 DD Memo，拼接 / 提取）:
    - ecm-draft-report-assembly（按一级标题拼接律师工作报告 / 尽职调查报告对应章节）
    - ecm-draft-opinion-letter（提取风险分级汇总的"高"级事项，注入意见书"特别事项提示"段）
    - ecm-qc-work-report-review（BATCH-09；反向定位到原 Memo 做审查）
本版编制日期: 2026-04-24
version: 1.0.0
---

# DD → Draft 数据交接契约（Single Source of Truth）

本 schema 约定 17 个业务性 DD skill 的 Markdown 输出**结构**和**字段**，供下游 `ecm-draft:report-assembly` / `ecm-draft:opinion-letter` 按稳定契约解析。没有本契约，`report-assembly` 必须对每个 DD skill 单独写 parser；有本契约，一个 parser 通吃 17 个 DD skill，且未来新增 DD skill 自动兼容。

本契约**不取代** [`shared/templates/dd-skill-template.md`](../templates/dd-skill-template.md)——后者是给人（DD skill 作者）看的"怎么写 SKILL.md 和 DD Memo"；本文件是给 Claude（draft skill 的执行者）看的"怎么稳定解析 DD Memo"。两者必须保持一致，任何一侧变更都要同步改另一侧。

---

## 0. 落地文件路径契约

每个 DD skill 的最终 Memo 文件**必须**落到以下路径：

```
{项目根}/02-尽职调查/02-{NN}-{章节名}/DD-Memo-{章节名}-{YYYYMMDD}.md
```

其中：

| 字段 | 取值 | 说明 |
|------|------|------|
| `NN` | 01-17 | 对应 `shared/templates/project-folder-structure.md` 的目录编号（严格对齐） |
| `章节名` | 见下表 | 与目录名末段保持一致，避免出现空格 / 特殊字符 |
| `YYYYMMDD` | 8 位日期 | Memo 出具日期；同一 skill 多次出具时保留最近版本，老版归档到 `05-底稿和附件/DD-Memo-历史版本/` |

### skill → 目录 → 章节名 对照（硬契约）

| skill | NN | 目录 | 章节名（Memo 文件名） | 一级标题 |
|-------|----|------|--------------------|---------|
| `ecm-dd-approval` | 01 | `02-01-批准和授权/` | `批准和授权` | `# DD Memo：本次交易的批准和授权` |
| `ecm-dd-entity` | 02 | `02-02-主体资格/` | `主体资格` | `# DD Memo：发行人主体资格` |
| `ecm-dd-establishment` | 03 | `02-03-历史沿革/` | `设立` | `# DD Memo：发行人设立` |
| `ecm-dd-history` | 03 | `02-03-历史沿革/` | `历史沿革` | `# DD Memo：股本及其演变` |
| `ecm-dd-independence` | 04 | `02-04-独立性/` | `独立性` | `# DD Memo：发行人独立性` |
| `ecm-dd-shareholders` | 05 | `02-05-股东及实控人/` | `股东及实控人` | `# DD Memo：股东与实际控制人` |
| `ecm-dd-business` | 06 | `02-06-业务资质/` | `业务` | `# DD Memo：发行人业务` |
| `ecm-dd-related-party` | 07 | `02-07-关联交易与同业竞争/` | `关联交易与同业竞争` | `# DD Memo：关联交易与同业竞争` |
| `ecm-dd-assets` | 08 | `02-08-主要财产/` | `主要财产` | `# DD Memo：主要财产` |
| `ecm-dd-debt` | 09 | `02-09-重大债权债务/` | `重大债权债务` | `# DD Memo：重大债权债务` |
| `ecm-dd-charter` | 10 | `02-10-公司治理/` | `公司章程与治理` | `# DD Memo：公司章程与组织机构` |
| `ecm-dd-directors` | 11 | `02-11-董监高/` | `董监高` | `# DD Memo：董事、监事及高级管理人员` |
| `ecm-dd-tax` | 12 | `02-12-税务/` | `税务` | `# DD Memo：税务` |
| `ecm-dd-environment` | 13 | `02-13-环保与安全生产/` | `环保与安全生产` | `# DD Memo：环境保护、产品质量、安全生产` |
| `ecm-dd-fundraising` | 14 | `02-14-募集资金运用/` | `募集资金运用` | `# DD Memo：募集资金运用` |
| `ecm-dd-litigation` | 15 | `02-15-诉讼仲裁处罚/` | `诉讼仲裁处罚` | `# DD Memo：诉讼、仲裁、行政处罚` |
| `ecm-dd-compliance` | 16 | `02-16-其他合规事项/` | `其他合规事项` | `# DD Memo：其他合规事项` |

> **跨章节备注**：`establishment` 和 `history` 共用 `02-03-历史沿革/` 目录但各自独立 Memo；`independence` 是横向 skill，依赖其他 5 个 DD skill 的输出做综合评估，所以 Memo 里会交叉引用其他 Memo 文件。
> **report-assembly 章节顺序**严格按本表 NN 升序拼接（先设立后历史沿革的实务习惯由 NN=03 两个 skill 的小节内顺序体现，见 § 4）。

---

## 1. 顶部元信息（必填块）

DD Memo 文件的一级标题下必须紧跟**引用块**（`>` 开头），包含以下结构化字段（顺序固定，字段间用 ` | ` 分隔）：

```markdown
# DD Memo：{章节标题}

> 项目：{company_short_name} | 对应章节：编报规则第 {chapter_no} 章 | 编制日期：{YYYY-MM-DD} | 编制人：{lawyer_name} | skill 版本：{skill_version}
```

### 字段说明

| 字段 | 类型 | 强制 | 说明 | 示例 |
|------|------|:---:|------|------|
| `company_short_name` | string | 是 | 客户简称，与 `ecm-setup:project-init` 约定的简称一致 | `某某科技` |
| `chapter_no` | int | 是 | 编报规则第 12 号章节号（1-17） | `1` |
| `编制日期` | YYYY-MM-DD | 是 | 本 Memo 的出具日期 | `2026-04-24` |
| `lawyer_name` | string | 是 | 经办律师姓名；多人时以顿号分隔 | `张三、李四` |
| `skill_version` | semver | 是 | 生成该 Memo 的 DD skill 版本号（供下游 Diff 定位契约版本） | `0.1.0` |

> **下游解析锚点**：report-assembly 从第 1 行一级标题识别章节，从第 2 行元信息引用块提取项目元数据，把 17 个 Memo 的项目 / 日期 / 律师字段做**一致性校验**（不一致时在拼接结论里起红旗提示"DD Memo 之间元信息冲突"）。

---

## 2. 二级标题骨架（强制五段式）

每份 DD Memo 必须含且仅含下列五个二级标题，顺序固定：

```markdown
## 一、核查要点清单
## 二、审阅发现
## 三、风险分级汇总
## 四、结论与建议
## 五、参考资料
```

**不得**增删、改名、改序号。额外字段追加到各段末尾，不得另起二级标题。

### 2.1 "一、核查要点清单" 段

- 以 GitHub 风格 `- [ ]` / `- [x]` 清单列示
- 每条要点格式：`- [x/空] {要点描述}（法规依据：{《xx 法》第 yy 条} / 见 [regulations-index](...)）`
- 空 checkbox 表示"本项目未核查 / 资料缺失"；勾选表示"已完成核查"

### 2.2 "二、审阅发现" 段

每条发现必须用三级标题独立一条：

```markdown
### 发现 1：{简短标题}
- **相关文件**：{文件名 1}；{文件名 2}
- **具体问题**：{问题描述}
- **风险级别**：高 / 中 / 低
- **法规依据**：{《xx 法》第 yy 条}
```

**硬字段**（供 report-assembly 精确定位）：
- 三级标题必须以 `### 发现 N：` 开头，N 为连续正整数
- 四个 bullet（`**相关文件**` / `**具体问题**` / `**风险级别**` / `**法规依据**`）顺序固定
- "风险级别" 取值**限定为** `高` / `中` / `低` 三选一（不接受 `红/黄/蓝`、`严重/一般/轻微` 等别名）

### 2.3 "三、风险分级汇总" 段（report-assembly / opinion-letter 的主消费段）

必须是**单张 Markdown 表格**，列定义如下（列顺序、列名、列数固定）：

```markdown
| 编号 | 问题 | 级别 | 所涉文件 | 法规依据 |
|------|------|------|---------|---------|
| 1    | ...  | 高   | ...     | ...     |
| 2    | ...  | 中   | ...     | ...     |
```

**硬字段**：
- 表头必须是 `| 编号 | 问题 | 级别 | 所涉文件 | 法规依据 |`（五列，不多不少，顺序锁定）
- "级别" 列取值严格限 `高` / `中` / `低`
- "编号" 列与"二、审阅发现"中的 `### 发现 N` 一一对应（`N` 即"编号"）
- 表格之前 / 之后**不得**插入其他内容（表格要紧跟二级标题；表格结束后留一空行进入下一节）

> **下游 opinion-letter 消费规则**：扫描所有 17 份 Memo 的"三、风险分级汇总"表；抽取"级别 = 高"的所有行 → 去重合并 → 注入《法律意见书》的"特别事项提示"专段。因此**本表的"问题"列措辞应当独立成句、不依赖上下文**（opinion-letter 会把这句话原样引用，不做复杂改写）。

### 2.4 "四、结论与建议" 段

固定三个小节（三级标题）：

```markdown
### 总体结论
{一段话：对照发行 / 交易条件，本章节层面是否具备条件；若否，说明短板}

### 待补正事项
1. {补正事项 1}
2. {补正事项 2}

### 建议措施
- 补充材料：...
- 程序整改：...
- 披露安排：...
- 获取承诺函：...
```

### 2.5 "五、参考资料" 段

两个小节（三级标题），指向本 Memo 出具过程中引用的资源：

```markdown
### 法规引用
- `../../shared/regulations/公司法-2024.md`（第 X 条）
- ...

### 客户文件清单
- {相对于项目根的路径}
- ...
```

---

## 3. 章节专属字段（各 skill 扩展区）

部分 DD skill 依据 `dd-skill-template.md` 允许在"二、审阅发现" **之后**、"三、风险分级汇总" **之前**插入**专属表格**（如股本演变时间线、董监高花名册、关联方清单等）。这些表由各 skill 在自己的 SKILL.md "输出格式契约"段落里显式声明，`report-assembly` 默认**原样保留**这些表格，不解析其字段。

下表列出当前已声明的 skill 专属表（供 report-assembly 调试 parser 时做白名单识别）：

| skill | 专属表标题（二级标题下的三级标题 / 或小节前的 bold） | 是否为 opinion-letter 消费 |
|-------|-----------------------------------------------|:--------------------:|
| `ecm-dd-history` | **股本演变时间线表** | 否（原样保留） |
| `ecm-dd-shareholders` | **股权结构图 + 实控人穿透图** | 否（原样保留） |
| `ecm-dd-directors` | **董监高花名册** | 否（原样保留） |
| `ecm-dd-business` | **业务资质清单表** / **前五大客户/供应商集中度表** | 否 |
| `ecm-dd-related-party` | **关联方清单表** / **关联交易汇总表** / **同业竞争情况表** | 否 |
| `ecm-dd-assets` | **不动产清单表** / **知识产权清单表** / **重大设备清单表** / **承租资产清单表** | 否 |
| `ecm-dd-debt` | **重大借款清单表** / **对外担保清单表** / **大额应收应付清单表** / **或有负债清单表** | 否 |
| `ecm-dd-independence` | **五独立对照评估表** / **独立性重大依赖汇总表** | 是（`opinion-letter` 引用五独立结论作为《关于独立性的意见》段） |

> 随新 DD skill 增加本表会扩展；每个新增 skill 的 SKILL.md 必须同步维护本表的对应行。

---

## 4. 拼接层语义（report-assembly 用）

`report-assembly` 把 17 份 Memo 拼成**《律师工作报告》**或**《尽职调查报告》**时遵循：

1. **章节顺序**：严格按 § 0 表格 NN 升序。在 NN=03 共用目录内，先 `establishment`（设立）后 `history`（历史沿革），对应律师工作报告惯例。
2. **一级标题→报告章节名映射**：Memo 的 `# DD Memo：{章节标题}` 拼入报告时替换为"第 N 部分 / {章节标题}"（报告章编号从《编报规则第 12 号》继承，1→1、5→5、11→11……；合并 NN=03 时设立作主标题、历史沿革作子标题）。
3. **二级标题提升**：Memo 的五个二级标题（"一、核查要点清单"等）在报告里作为章节内部的次级结构保留，不提升为章。
4. **元信息引用块**：17 份 Memo 各自的元信息**不**重复进报告正文；报告首页单独生成一次"项目元信息"块（来自 `ecm-setup:project-init` 或用户提供），report-assembly 负责做**一致性校验**（发现 skill_version 跨 Memo 不一致时，在报告开头的"编制说明"段落给出提示）。
5. **风险汇总聚合**：17 份 Memo 的"三、风险分级汇总"表合并为报告末尾的"全项目风险分级汇总表"，新增一列"所属章节"（取该 Memo 的章节名）。
6. **缺章处理**：某个 DD skill 对应的 Memo 不存在时，在报告该章插入占位说明"本章 Memo 尚未出具（对应 skill: `ecm-dd-{xxx}`）"，并在报告首页的"未完成章节"清单里列出。

---

## 5. opinion-letter 消费规则（特别事项提示段的生成）

`opinion-letter` 只消费两段固定内容：

1. **所有 Memo 的"三、风险分级汇总"表**：提取 `级别 = 高` 的全部行 → 去重（按 `问题` 列全文匹配）→ 按章节 NN 升序排列 → 注入《法律意见书》的"特别事项提示 / 限定性意见"段落。每条形如：
   ```
   经核查，发行人存在以下需提请注意事项：第 N 部分（{章节标题}）：{问题}。
   ```

2. **`ecm-dd-independence` 的"五独立对照评估表"**：原样转写为《关于发行人独立性的意见》专段，并以表下的"总体结论"作为独立性意见的结论性表述。

`opinion-letter` **不**消费：
- "一、核查要点清单" 段（那是工作底稿，不进意见书）
- "二、审阅发现" 段的三级标题细节（太底稿；意见书用的是"三、风险分级汇总"里的措辞）
- "五、参考资料" 段（意见书另建"法律依据"段统一起草）

---

## 6. 字段类型与校验（供下游 parser 参考）

附一份等价 JSON 片段，供 draft skill 做字段校验时的锚点：

```json
{
  "dd_memo": {
    "chapter_title": "string (非空)",
    "meta": {
      "company_short_name": "string (非空)",
      "chapter_no": "integer (1-17)",
      "issue_date": "string (YYYY-MM-DD)",
      "lawyer_name": "string (非空，多人以顿号分隔)",
      "skill_version": "string (SemVer, 例: 0.1.0)"
    },
    "checkpoints": [
      {"checked": "boolean", "description": "string", "legal_basis": "string"}
    ],
    "findings": [
      {
        "id": "integer (从 1 起)",
        "title": "string",
        "related_files": ["string"],
        "description": "string",
        "risk_level": "enum('高','中','低')",
        "legal_basis": "string"
      }
    ],
    "risk_summary_table": [
      {"id": "integer", "issue": "string", "level": "enum('高','中','低')", "related_files": "string", "legal_basis": "string"}
    ],
    "conclusion": {
      "overall": "string",
      "to_be_corrected": ["string"],
      "recommended_actions": {
        "supplement": "string",
        "procedural_fix": "string",
        "disclosure": "string",
        "letter_of_commitment": "string"
      }
    },
    "references": {
      "regulations": ["string (路径)"],
      "client_files": ["string (路径)"]
    },
    "skill_specific_tables": "object (skill 专属表，原样保留)"
  }
}
```

> 实现时 draft skill 不强制实现完整 JSON 序列化；常规路径是**正则 + 启发式**解析 Markdown。JSON 片段只作字段类型的权威定义，便于校验器脚本（未来 `scripts/validate-dd-memo.py`）对齐。

---

## 7. 违约处理

`report-assembly` / `opinion-letter` 解析某份 Memo 时若发现违约（缺段 / 表头列名不对 / 级别取值超出枚举），**不得自行猜测补全**。处理方式：

1. 把该 Memo 整体跳过，不进入拼接 / 意见注入
2. 在《律师工作报告》首页的"编制说明"段给出明确提示：
   ```
   注：下列章节对应 DD Memo 因格式不符合 shared/schemas/dd-output-schema.md 契约 vX.Y.Z，未能纳入本次拼接。请回到对应 skill 重新出具：
   - ecm-dd-{xxx}：Memo 文件路径，具体违约点（例："缺少'三、风险分级汇总'表格" / "级别列出现'严重'非法取值"）
   ```
3. 不污染其他合规 Memo 的拼接结果

---

## 8. 变更规则

| 变更类型 | 分类 | 要求 |
|---------|------|------|
| 删除必选字段 / 改字段名 / 改枚举取值 | **MAJOR** | 同步改 `shared/templates/dd-skill-template.md` + 17 个 DD skill 的 `输出格式契约` 段 + 2 个消费方 draft skill 的解析逻辑 |
| 新增可选字段 / 新增 skill 专属表 | MINOR | 仅更新本文件 § 3 表格；上游 skill 可选发，下游消费方忽略未知字段 |
| 澄清措辞 / 示例补充 / typo 修正 | PATCH | 仅改本文件 |

每次变更必须写入本文件底部"更新日志"表。

---

## 9. 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-24 | 首版（BATCH-06 建立）。冻结：五段式二级标题、风险级别枚举、风险汇总表列定义、一级标题→章节号映射、Memo 落地路径模式 |
