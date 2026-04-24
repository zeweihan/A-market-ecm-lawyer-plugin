---
目录用途: 跨 skill 数据交接的字段契约
维护者: 需要"上游 skill 输出 → 下游 skill 读取"的所有 batch
本版编制日期: 2026-04-24
---

# shared/schemas/ — 跨 skill 数据交接契约

本目录放置"上游 skill 输出 → 下游 skill 读取"的字段契约。当两个 skill 之间存在数据流（上游的产出是下游的输入），就应当把数据形状在本目录固化一份，避免：

- 上游改了字段名 / 拆合字段，下游失效
- 同一语义被多个 skill 起了不同名字（如 `company_short_name` vs `short_name` vs `ticker_name`）
- 拼接阶段临时做"格式归一"——成本极高

## 命名规范

```
<上游到下游的契约主题>-schema.md
```

例：`dd-output-schema.md`（DD skill → report-assembly / opinion-letter）。

## 为什么用 Markdown 而不是 JSON Schema

本仓库 skill 多数产出 Markdown，而非纯 JSON。契约既要约束"输出 Markdown 的结构"（一级 / 二级标题、表格列名、表格取值），又要约束"结构化字段"（日期、风险级别、文件路径），JSON Schema 覆盖不了前者。因此约定：

- **骨架用 Markdown 描述**（含示例片段）
- **结构化字段可在附录附 JSON 片段**（供脚本解析时做校验锚点）

每个 schema 文件都应当能被 Claude 直接读懂、能被律师直接看懂，而不是需要 jsonschema-cli 才能理解。

## 已建立

- [x] [`dd-output-schema.md`](./dd-output-schema.md) — DD skill 统一输出 → `ecm-draft:report-assembly` / `ecm-draft:opinion-letter` 的结构化输入契约（BATCH-06 建立）

## 待补充（占位）

- [ ] `research-output-schema.md` — ecm-research:* 输出 → 其他 skill 引用法规 / 案例的字段契约（当前 `shared/templates/research-output-format.md` 已承担部分职责；后续评估是否拆出独立 schema）
- [ ] `design-memo-schema.md` — ecm-design:* 备忘录 → 后续文书引用"方案结论"的字段契约
- [ ] `qc-output-schema.md` — QC skill 输出 Word 修订稿的 `w:author` / 批注分类 / 处置建议等字段契约（随 BATCH-09 建立）

## 变更规则

- 契约的字段增删改均属 **MAJOR 变更**——必须同步通知所有引用本契约的 skill（在 schema 顶部 `被哪些 skill 引用` 清单里逐一核对），并在 `CHANGELOG.md` 专门记录
- 契约的**可选字段新增**可以是 MINOR（上游新发字段，下游可忽略）
- 仅澄清措辞、补充示例属 PATCH
