# 安装 / Installation

本仓库同时支持两种安装形态：

1. 作为 Claude 插件整体安装（推荐）
2. 按需下载单个 `.skill` 文件

## 方式 1：作为插件整体安装（推荐）

### Claude Code

```bash
claude plugin install zeweihan/A-market-ecm-lawyer-plugin
```

或手动从 GitHub 克隆后本地安装：

```bash
git clone https://github.com/zeweihan/A-market-ecm-lawyer-plugin.git
cd A-market-ecm-lawyer-plugin
claude plugin install .
```

### Cowork

在 Cowork 的 Plugins 面板里：

1. 打开 "Add from GitHub"
2. 输入 `zeweihan/A-market-ecm-lawyer-plugin`
3. 点击 Install

### 安装后确认

```bash
claude skill list | grep -E "ecm-qc-shareholders-meeting-witness|listing-pathway-selection"
```

## 方式 2：按需下载单个 `.skill` 文件

适合只需要某个特定 skill 的情况。

1. 打开 [GitHub Releases 页面](https://github.com/zeweihan/A-market-ecm-lawyer-plugin/releases)
2. 下载你需要的 `.skill` 文件（每个 release 会附 zip 包）
3. 把 `.skill` 文件拖入 Claude 的 skill 安装界面，或者解压到：
   - Claude Code：`~/.claude/skills/`
   - Cowork：在 Skills 面板里导入

`.skill` 文件就是 skill 目录的 zip 压缩包。你也可以自己从源码打包：

```bash
./scripts/package-skill.sh skills/ecm-qc-shareholders-meeting-witness
# 产出：dist/ecm-qc-shareholders-meeting-witness.skill
```

## 外部依赖

部分 skill 需要 Anthropic 官方的 `docx` / `pdf` / `xlsx` skill。这些 skill **不随本仓库分发**，安装方法见 [dependencies.md](./dependencies.md)。

## 验证安装

任选一个 skill 尝试触发。例如：

> 帮我审一下这份股东大会见证意见。

如果 Claude 回复里提到"按照见证意见内核审查 skill 的三级工作流……"，说明 `ecm-qc-shareholders-meeting-witness` 已安装成功。

## 卸载

### Claude Code

```bash
claude plugin uninstall a-share-ecm-lawyer
```

### Cowork

在 Plugins 面板里点击 "Uninstall"。

## 升级

```bash
claude plugin update a-share-ecm-lawyer
```

升级前建议看一眼 [CHANGELOG.md](../CHANGELOG.md) 里的变更记录。
