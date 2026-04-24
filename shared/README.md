# 共享资源 / Shared Resources

本目录放置**跨 skill 复用**的资料。单个 skill 才用的资料不放在这里，而是放在该 skill 的 `references/` 下。

## 子目录

### `regulations/`

法律法规、监管规则、自律规则的条文节选。命名规范：

```
<规则名>-<版本年份>.md        # 例：公司法-2024.md、上市公司股东会规则-2025.md
```

每份规则文件的开头必须注明：

```markdown
# 《xxx》

- **发布机构**：
- **当前有效版本**：
- **本文节选日期**：
- **节选范围**：<只摘了哪些条？全文还是部分？>
- **原文链接**：
```

### `terminology/`

A 股 ECM 业务的术语词汇表，解决中英文混用、简称歧义、不同文件里叫法不一的问题。

建议的文件：
- `a-share-listing-terms.md`：上市基础术语
- `due-diligence-terms.md`：尽调专用术语
- `corporate-governance-terms.md`：公司治理术语

### `templates/`

文书片段模板，如 letterhead、落款、声明段落等。命名规范：

```
<模板用途>.md                 # 例：law-firm-letterhead.md
```

## 在 skill 里引用共享资源

```markdown
<!-- 在 SKILL.md 或 references 的 .md 里 -->
见 [《公司法》第 109 条](../../shared/regulations/公司法-2024.md#第109条)
```

## 维护

- **新增**：直接 PR，在 PR 描述里说明用途和预期被哪些 skill 引用
- **修改**：列出所有引用该文件的 skill，review 时需确认改动不会破坏引用
- **删除**：删除前必须 grep 确认没有 skill 还在引用

## 命名规则

- 中文名优先用规则本身的正式名称（《公司法》《上市公司股东会规则》）
- 文件名用中文没问题（GitHub 支持 UTF-8），但要保持一致：规则名用中文、模板/术语可以用英文 kebab-case
