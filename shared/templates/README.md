# 文书模板片段

跨 skill 复用的文书片段。例如所有 skill 生成的法律文书都可能用到统一的 letterhead、落款、免责声明段。

## 命名规范

```
<用途>.md                     # 例：law-firm-letterhead.md
```

## 每份文件的建议结构

```markdown
---
模板名: 律师事务所 letterhead
适用场景: 法律意见书首页、律师工作报告首页
填充变量:
  - {{律所名}}
  - {{律所地址}}
  - {{电话}}
  - {{传真}}
  - {{文号}}
依赖外部 skill: docx（用于套版）
---

# 律师事务所 Letterhead 模板

## Word 段落结构

1. 律所中文名（居中，四号，宋体，加粗）
2. 律所英文名（居中，小四，Times New Roman）
3. 分割线
4. 地址 / 电话 / 传真（小五号）

## Python-docx 伪代码（给 docx-legal-formatting skill 用）

...
```

## 待补充（占位）

- [ ] `law-firm-letterhead.md` — 律所抬头
- [ ] `law-firm-signature-block.md` — 律所 + 签字律师落款
- [ ] `legal-opinion-declaration.md` — 声明事项标准段
- [ ] `witness-opinion-conclusion.md` — 见证意见结论措辞模板
- [ ] `tracked-changes-author-config.md` — 修订痕迹的 author 字段统一约定（当前约定：默认 "内核"）
