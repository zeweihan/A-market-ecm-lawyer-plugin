# 外部依赖 / External Dependencies

本仓库内部分 skill 需要依赖 Anthropic 官方发布的通用 skill（典型的如 `docx`、`pdf`、`xlsx`）。由于这些 skill 使用**专有许可证**，**不随本仓库分发**，请按下方说明自行安装。

## 为什么不能打包进本仓库

Anthropic 官方 skill 的 `LICENSE.txt` 明确限制：

> Users may not:
> - Extract these materials from the Services or retain copies outside the Services
> - Reproduce or copy these materials
> - Create derivative works based on these materials

本仓库以 MIT 许可证开源，打包 Anthropic 专有 skill 会违反其许可。因此我们只提供**依赖列表 + 安装路径说明**，让使用者在自己的 Claude 环境里独立安装。

## 依赖清单

| 外部 skill | 被哪些 skill 依赖 | 功能 | 获取路径 |
|-----------|------------------|------|---------|
| `docx` | ecm-qc-shareholders-meeting-witness、ecm-setup-file-classify、ecm-design-ipo-path / deal-structure / control-rights / ma-structure / cross-border、ecm-draft-report-assembly、ecm-draft-opinion-letter、ecm-draft-disclosure-review、ecm-draft-meeting-docs、ecm-draft-format-adjust、ecm-qc-opinion-letter-review、ecm-qc-work-report-review、ecm-qc-disclosure-review、ecm-qc-meeting-docs-review | Word 文档读写、tracked changes、批注 | Claude Code / Cowork 内置 |
| `pdf` | ecm-setup-file-classify、ecm-draft-disclosure-review（起草人自查读 PDF 信披文件）、ecm-qc-disclosure-review（内核审查读 PDF 信披文件）；（未来）案例检索、意见书扫描件处理 | PDF 文本提取、表单填写、合并切分 | Claude Code / Cowork 内置 |
| `xlsx` | ecm-setup-file-classify；（未来）尽调清单管理、股东名册处理 | Excel 读写、公式、图表 | Claude Code / Cowork 内置 |

## 如何确认你已经有这些 skill

### Claude Code

```bash
claude skill list
```

如果输出里包含 `docx`、`pdf`、`xlsx`，就已经安装。这三个 skill 通常随 `anthropic-skills` 插件一起发布。

### Cowork

在 Cowork 设置 → Skills 面板，查看是否有 `docx`、`pdf`、`xlsx`。

## 如果缺失怎么办

这三个 skill 是 Anthropic 官方随官方产品分发的（目前通常打包在 `anthropic-skills` 插件里）。升级到最新版 Claude Code / Cowork，或安装官方 `anthropic-skills` 插件即可获得：

```bash
# Claude Code 示例（具体命令以官方文档为准）
claude plugin install anthropic-skills
```

如果使用 Anthropic API（非 Claude Code / Cowork）：这些 skill 不可用，需要使用者自行实现对应能力，或重构本仓库的 skill 以直接调用 `python-docx`、`pypdf`、`openpyxl` 等开源库。

## 本仓库内部的 skill 间依赖

除了外部依赖，本仓库的某些 skill 会接受其他 skill 的结构化输出作为输入。例如：

- `ecm-setup:file-organize` 的文件索引表 → 17 个 `ecm-dd:*` 业务性尽调 skill
- 17 个 `ecm-dd:*` 输出的 DD Memo → `ecm-draft:report-assembly` / `ecm-draft:opinion-letter`
- `ecm-draft:*` 输出的文书初稿 → 对应 `ecm-qc:*` 内核审查 skill

跨 skill 的数据格式约定在 [skill-authoring-guide.md](./skill-authoring-guide.md#跨-skill-数据约定) 和 [dd-output-schema.md](../shared/schemas/dd-output-schema.md) 里维护。

## 更新此文档

新增 skill 时如果引入新的外部依赖，请在本文档的"依赖清单"表格里加一行，并在 PR 里勾选对应项。
