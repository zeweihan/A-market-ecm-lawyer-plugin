# Changelog

本仓库遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 约定，版本号遵循 [SemVer 2.0](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added — BATCH-01（ecm-setup 三件套）
- `skills/ecm-setup-project-init/`：项目初始化 skill。追问最多 4 轮确认项目类型/境内跨境/板块/客户简称；物理创建标准项目目录；根据项目类型输出 skill 调用 roadmap。内含 `references/project-roadmaps.md`（IPO/并购/再融资/新三板/债券 5 种类型 + 通用 roadmap）。
- `skills/ecm-setup-file-classify/`：文件批量分类 skill。扫描 `02-99-未分类文件/` 目录，调用 `pdf`/`docx`/`xlsx` 外部 skill 读取内容，为每个文件打 1-3 个标签（many-to-many），主动提示版本重复/类别缺失/标签过多。
- `skills/ecm-setup-file-organize/`：文件归位 skill。按 classify 结果默认 `copy` 到对应 DD 章节目录（多标签文件复制到多个目录），生成 `文件索引表.md` 作为下游 DD skill 的统一入口；支持 `move`/`symlink` 备选策略但需显式确认。
- `shared/terminology/classification-labels.md`：**全仓唯一权威**的 19 个分类标签定义。未来所有 ecm-dd-* skill、file-classify、file-organize 统一引用本文件，不得自行定义。
- `shared/templates/project-folder-structure.md`：**全仓唯一权威**的项目目录结构 + 标签→目录映射表 + 项目类型变体目录 + 可直接执行的 `mkdir -p` 命令段。

### Added — 其他
- `docs/project-plan.md`：总工作计划。把 40+ 个 skill 的建设切成 11 个可独立完成的 batch，每个 batch 自带依赖清单、输入输出、验收标准和独立窗口启动模板，支持并行推进。
- 新增 `ecm-qc` 模块（第 7 个 skill 类），用于承载内核 / QC 团队使用的审查类 skill。模块和既有 6 类项目 skill（setup/design/dd/draft/research/workflow）并列但语义独立——项目组 skill 是"做事"，QC skill 是"审事"。

### Changed
- `docs/dependencies.md`：更新 `docx` / `pdf` / `xlsx` 三个外部 skill 的 `required_by` 列表，登记 `ecm-setup-file-classify` 新引入的依赖。
- `.claude-plugin/plugin.json`：`skills` 数组新增 3 个 ecm-setup 路径，`dependencies.external_skills` 同步更新。
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
