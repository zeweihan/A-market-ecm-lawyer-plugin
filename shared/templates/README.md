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

## 已建立

- [x] `project-folder-structure.md` — 项目标准目录结构 + 标签→目录映射（`ecm-setup` 三件套共用）
- [x] `legal-memo-format.md` — 法律备忘录排版规范（`ecm-design` 五件套共用；未来其他备忘录类输出亦可复用）
- [x] `dd-skill-template.md` — DD 业务性 skill 统一编写模板（BATCH-02 建立；所有 `ecm-dd-*` 业务性 skill 必须套用。BATCH-03 / BATCH-04 / BATCH-05 三路并行交付的 12 个 `ecm-dd-*` skill 均已按该模板产出；至此 `ecm-dd` 17 个业务性 skill 统一契约覆盖完毕，工具类 2 个 skill（`dd-data-verify` / `dd-file-review`）按 BATCH-05 窗口单独的"工具契约"出）
- [x] `research-output-format.md` — 法律研究类 skill 统一输出格式（BATCH-08 建立；所有 `ecm-research-*` 输出必须遵循：可靠性 A/B/C/D 分级、法规 / 案例引证规范、四段外层结构、三层 fallback）

## 待补充（占位）

- [ ] `law-firm-letterhead.md` — 律所抬头
- [ ] `law-firm-signature-block.md` — 律所 + 签字律师落款
- [ ] `legal-opinion-declaration.md` — 声明事项标准段
- [ ] `witness-opinion-conclusion.md` — 见证意见结论措辞模板
- [ ] `tracked-changes-author-config.md` — 修订痕迹的 author 字段统一约定（当前约定：默认 "内核"）
- [ ] `work-report-format.md` — 律师工作报告排版规范（随 BATCH-06 建立）
- [ ] `legal-opinion-format.md` — 法律意见书排版规范（随 BATCH-06 建立）
- [ ] `qc-skill-template.md` — QC skill 统一模板（随 BATCH-09 建立）
