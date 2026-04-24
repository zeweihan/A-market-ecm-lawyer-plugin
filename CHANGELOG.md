# Changelog

本仓库遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 约定，版本号遵循 [SemVer 2.0](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- 新增 `ecm-qc` 模块（第 7 个 skill 类），用于承载内核 / QC 团队使用的审查类 skill。模块和既有 6 类项目 skill（setup/design/dd/draft/research/workflow）并列但语义独立——项目组 skill 是"做事"，QC skill 是"审事"。
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
