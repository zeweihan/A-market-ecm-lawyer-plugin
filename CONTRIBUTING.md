# 贡献指南 / Contributing

欢迎以任何形式贡献，包括：新增 skill、改进既有 skill、修正参考资料错误、提出 issue、补全术语词汇表等。

## 在开始之前

1. **先开 issue 讨论**：在动手写新 skill 之前，强烈建议先用 `new_skill_proposal` issue 模板说明 skill 的定位、触发场景、输入输出契约。这能避免两人同时写同一个 skill，也便于在早期对齐设计。

2. **阅读现有参考实现**：`skills/shareholders-meeting-witness-review/` 是第一个成熟 skill，目录结构、SKILL.md 写法、参考资料组织方式都可以直接抄。

3. **阅读 [docs/skill-authoring-guide.md](./docs/skill-authoring-guide.md)**：本仓库对 skill 的 YAML frontmatter、目录结构、命名规范有统一约定。

## 提交流程

1. Fork 本仓库
2. 从 `main` 切出分支：`git checkout -b add-skill/xxx` 或 `fix/xxx`
3. 开发并本地测试（至少跑通 skill 的一个完整工作流）
4. 更新 `CHANGELOG.md` 的 `[Unreleased]` 段
5. 如果新增 skill，在根目录 `README.md` 的 skill 清单表格里加一行
6. 提交 PR 并填写 PR 模板

## 新增 skill 的硬性要求

每个新 skill 必须满足：

- [ ] 目录结构符合 [skill-authoring-guide](./docs/skill-authoring-guide.md)
- [ ] `SKILL.md` 的 YAML frontmatter 完整（`name`/`description`/`version`/`license`/`phase`/`category`）
- [ ] `description` 字段触发关键词密集、能被 Claude 正确匹配
- [ ] 如果产出法律文书类内容，必须在 SKILL.md 里引用仓库顶层 `DISCLAIMER.md`
- [ ] 如果依赖外部 skill（docx/pdf/xlsx 等），在 SKILL.md 顶部的"前置依赖"段明确列出，并更新 `docs/dependencies.md`
- [ ] 不得内嵌任何专有许可的代码或素材（例如 Anthropic 官方 docx skill 的 script/reference）

## 跨 skill 共享资料的原则

- 法规条文节选、术语词汇表、文书模板片段——**抽到 `shared/` 目录**，各 skill 通过路径引用，不要在 skill 内部重复
- 如果某份资料只被一个 skill 使用，放在该 skill 的 `references/` 下即可
- 共享资料的变动可能影响多个 skill，PR 里须列出受影响的 skill 清单

## 命名规范

| 项 | 规范 | 例子 |
|----|------|------|
| skill 目录名 | `ecm-<category>-<function>` kebab-case | `ecm-setup-project-init` |
| SKILL.md 的 `name` 字段 | 与目录名一致 | `ecm-setup-project-init` |
| 文档 / 路线图里的 skill 引用 | 带冒号的人类可读形式 | `ecm-setup:project-init` |
| 分支名 | `add-skill/xxx`、`fix/xxx`、`docs/xxx` | `add-skill/ecm-dd-approval` |
| commit 信息 | 中文或英文均可，但同一 PR 内保持一致 | `新增尽调 skill 框架` |

## 行为准则

本项目面向专业律师使用，但欢迎任何背景的贡献者参与。请保持讨论的专业性与建设性。

## 许可证

你提交的代码和文档将以本仓库的 [MIT 许可证](./LICENSE) 发布。提交 PR 即表示你同意此授权。
