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
- [x] `work-report-format.md` — **律师工作报告 / 尽职调查报告排版规范**（BATCH-06 建立）。首页封面 / 目录 / 引言 / 17 章正文 / 附件 / 签字页；字体字号 / 行距 / 首行缩进；自动章节编号；交叉引用规则；全项目风险汇总表 7 列定义；Markdown → DOCX 映射；12 类常见踩坑。`ecm-draft-report-assembly` 输出必遵循；`ecm-qc-work-report-review`（BATCH-09）以此为参考坐标
- [x] `legal-opinion-format.md` — **法律意见书排版规范**（BATCH-06 建立）。5 段骨架（引言 / 释义 / 正文 / 结论性意见 / 特别事项提示）；事实 - 核查 - 意见三步法；结论三级措辞；与工作报告的 11 项形式配套要求。`ecm-draft-opinion-letter` 输出必遵循；`ecm-qc-opinion-letter-review`（BATCH-09）参考
- [x] `meeting-docs-format.md` — **会议文件批量起草规范**（BATCH-06 建立）。三类会议 + 8 种会议文件结构；通知期限硬校验表；特别决议 / 关联回避 / 中小投资者单独计票识别规则；跨文件一致性校验；表决基数计算规则；2024 新《公司法》新情况。`ecm-draft-meeting-docs` 输出必遵循；`ecm-qc-meeting-docs-review`（BATCH-09）参考
- [x] `qc-skill-template.md` — **ecm-qc-*-review 系列统一骨架**（BATCH-09 建立）。SKILL.md frontmatter / 五步工作流 / 三条硬性输出契约（w:author="内核" / 最小显示改动 / 解释入批注）/ 批注分类前缀（【必改】【核实】【建议】【底稿】）/ references 目录结构（cross-check-matrix / form-requirements / substantive-checklist / common-errors / comment-templates）/ 与 ecm-draft-* 的边界声明格式。`ecm-qc:opinion-letter-review` / `work-report-review` / `disclosure-review` / `meeting-docs-review` 必须套用（`shareholders-meeting-witness` 作为样板保留自有结构）
- [x] `workflow-skill-template.md` — **ecm-workflow-* 编排层 skill 统一骨架**（BATCH-10 建立）。SKILL.md frontmatter（含 `wf-` 前缀强制 + module=ecm-workflow + category=工作流编排）/ 正文 9 节硬性顺序 / 6 阶段 schema（启动 / 设计 / 尽调 / 文书 / 内核 / 申报）/ skill 间数据传递契约（无私有状态，引用 project-folder-structure + dd-output-schema 两份既有 SoT）/ 失败-跳过-回滚处理 / workflow 嵌套规则（声明嵌套 + 不重复展开 + 状态独立 + 禁止双向）/ 与原子 skill 五项边界声明。`wf-ipo-full` / `wf-ipo-dd-full` / `wf-ma-full` / `wf-cross-border-ma` / `wf-issuance` / `wf-nto-listing` 必须套用

## 待补充（占位）

- [ ] `law-firm-letterhead.md` — 律所抬头
- [ ] `law-firm-signature-block.md` — 律所 + 签字律师落款
- [ ] `legal-opinion-declaration.md` — 声明事项标准段
- [ ] `witness-opinion-conclusion.md` — 见证意见结论措辞模板
- [ ] `tracked-changes-author-config.md` — 修订痕迹的 author 字段统一约定（当前约定：默认 "内核"）
