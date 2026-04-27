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
- [x] `dd-skill-template.md` — DD 业务性 skill 统一编写模板；所有 `ecm-dd-*` 业务性 skill 必须套用，工具类 2 个 skill（`dd-data-verify` / `dd-file-review`）按工具契约输出
- [x] `research-output-format.md` — 法律研究类 skill 统一输出格式；所有 `ecm-research-*` 输出必须遵循可靠性 A/B/C/D 分级、法规 / 案例引证规范、四段外层结构、三层 fallback
- [x] `work-report-format.md` — **律师工作报告 / 尽职调查报告排版规范**。首页封面 / 目录 / 引言 / 17 章正文 / 附件 / 签字页；`ecm-draft-report-assembly` 输出必遵循；`ecm-qc-work-report-review` 以此为参考坐标
- [x] `legal-opinion-format.md` — **法律意见书排版规范**。5 段骨架（引言 / 释义 / 正文 / 结论性意见 / 特别事项提示）；事实 - 核查 - 意见三步法；`ecm-draft-opinion-letter` 输出必遵循；`ecm-qc-opinion-letter-review` 参考
- [x] `meeting-docs-format.md` — **会议文件批量起草规范**。三类会议 + 8 种会议文件结构；通知期限硬校验；特别决议 / 关联回避 / 中小投资者单独计票识别；`ecm-draft-meeting-docs` 输出必遵循；`ecm-qc-meeting-docs-review` 参考
- [x] `qc-skill-template.md` — **ecm-qc-*-review 系列统一骨架**。五步工作流 / 三条硬性输出契约 / 批注分类前缀 / references 目录结构 / 与 ecm-draft-* 的边界声明格式
- [x] `workflow-skill-template.md` — **ecm-workflow-* 编排层 skill 统一骨架**。6 阶段 schema / skill 间数据传递契约 / 失败-跳过-回滚处理 / workflow 嵌套规则 / 与原子 skill 边界声明
- [x] `senior-lawyer-execution-standards.md` — **资深 A 股资本市场律师执行标准**。所有 skill 共同遵循事实证据、法源时效、风险判断、交付质量四类底线

## 待补充（占位）

- [ ] `law-firm-letterhead.md` — 律所抬头
- [ ] `law-firm-signature-block.md` — 律所 + 签字律师落款
- [ ] `legal-opinion-declaration.md` — 声明事项标准段
- [ ] `witness-opinion-conclusion.md` — 见证意见结论措辞模板
- [ ] `tracked-changes-author-config.md` — 修订痕迹的 author 字段统一约定（当前约定：默认 "内核"）
