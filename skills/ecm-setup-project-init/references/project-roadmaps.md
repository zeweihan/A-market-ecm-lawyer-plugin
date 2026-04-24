# 各项目类型的 Skill Roadmap 明细

本文件是 `ecm-setup-project-init` 的详细 roadmap 参考——根据项目类型输出"这个项目接下来要调哪些 skill、按什么顺序"。

**重要**：这里列出的 skill 顺序是**推荐序**，不是强制序。实际项目中律师可能因为客户节奏、信息到位程度而调整。roadmap 的目的是给项目组一个默认起点。

---

## IPO 项目 Roadmap

### 阶段 1：Setup（当前）
1. `ecm-setup:project-init` ✅
2. `ecm-setup:file-classify` — 对客户已提供的文件批量打标签
3. `ecm-setup:file-organize` — 按标签归位到对应 DD 章节目录，生成文件索引表

### 阶段 2：Design（方案设计）
4. `ecm-design:ipo-path` — 论证 A 股 / 港股 / 红筹路径选择，输出法律备忘录

### 阶段 3：Due Diligence（尽调）
5. `ecm-workflow:wf-ipo-dd-full` — 完整 IPO 尽调流程，自动顺序调用 17 个 DD skill
6. `ecm-dd:dd-data-verify` — 工商/财务数据自动交叉验证（Tushare/企查查）

### 阶段 4：Draft（文书起草）
7. `ecm-draft:report-assembly` — 拼接 DD 各章节 → 律师工作报告
8. `ecm-draft:opinion-letter` — 生成标准化法律意见书
9. `ecm-draft:disclosure-review` — 招股书法律部分**起草人自查**
10. `ecm-draft:format-adjust` — Word 排版、编号、目录、页眉页脚统一

### 阶段 5：QC（内核）
11. `ecm-qc:opinion-letter-review` — 法律意见书内核审查
12. `ecm-qc:work-report-review` — 律师工作报告内核审查
13. `ecm-qc:disclosure-review` — 招股书内核独立审查

---

## 并购重组项目 Roadmap

### 阶段 1：Setup
1. `ecm-setup:project-init` ✅
2. `ecm-setup:file-classify`
3. `ecm-setup:file-organize`

### 阶段 2：Design
4. `ecm-design:ma-structure` — 并购交易结构（发行股份/现金/混合/借壳）
5. `ecm-design:control-rights` — 控制权安排（收购比例/对赌/表决权/一致行动）
6. `ecm-design:cross-border` — 跨境合规与架构（如涉及跨境）

### 阶段 3：Due Diligence
7. `ecm-dd:dd-entity` — 标的主体资格
8. `ecm-dd:dd-history` — 历史沿革与股权演变
9. `ecm-dd:dd-shareholders` — 标的股东
10. `ecm-dd:dd-business` — 业务资质与重大合同
11. `ecm-dd:dd-assets` — 主要财产
12. `ecm-dd:dd-debt` — 重大债权债务
13. `ecm-dd:dd-related-party` — 关联交易
14. `ecm-dd:dd-litigation` — 诉讼仲裁处罚
15. `ecm-dd:dd-compliance` — 其他合规事项

### 阶段 4：Draft
16. `ecm-draft:report-assembly` — 法律尽调报告（并购版）
17. `ecm-draft:meeting-docs` — 交易方（收购方 + 标的方）会议文件
18. `ecm-draft:opinion-letter` — 法律意见书
19. `ecm-draft:disclosure-review` — 重组报告书 / 权益变动报告书自查

### 阶段 5：QC
20. `ecm-qc:opinion-letter-review`
21. `ecm-qc:disclosure-review`
22. `ecm-qc:meeting-docs-review`

---

## 再融资项目 Roadmap（定增 / 配股 / 可转债）

### 阶段 1：Setup
1. `ecm-setup:project-init` ✅
2. `ecm-setup:file-classify`
3. `ecm-setup:file-organize`

### 阶段 2：Design
4. `ecm-design:deal-structure` — 融资方案设计（工具选择 + 基本条款）

### 阶段 3：Due Diligence
5. `ecm-dd:dd-approval` — 本次发行批准授权（最核心）
6. `ecm-dd:dd-entity` — 发行人主体资格
7. `ecm-dd:dd-history` — 股本演变
8. `ecm-dd:dd-fundraising` — 募集资金运用
9. `ecm-dd:dd-compliance` — 合规事项
10. `ecm-dd:dd-litigation` — 诉讼/仲裁/处罚

### 阶段 4：Draft
11. `ecm-draft:opinion-letter` — 法律意见书
12. `ecm-draft:disclosure-review` — 募集说明书自查

### 阶段 5：QC
13. `ecm-qc:opinion-letter-review`
14. `ecm-qc:disclosure-review`

---

## 新三板挂牌项目 Roadmap

### 阶段 1：Setup
1. `ecm-setup:project-init` ✅
2. `ecm-setup:file-classify`
3. `ecm-setup:file-organize`

### 阶段 2：Design
4. `ecm-design:ipo-path` — 挂牌路径分析（基础层 / 创新层 / 北交所衔接）

### 阶段 3：Due Diligence
5. `ecm-workflow:wf-nto-listing` — 新三板挂牌专用尽调流程（比 IPO 宽松，但核心仍是 17 章体系的子集）

### 阶段 4：Draft
6. `ecm-draft:report-assembly`
7. `ecm-draft:opinion-letter`

### 阶段 5：QC
8. `ecm-qc:opinion-letter-review`

---

## 债券发行项目 Roadmap（框架，细节待开发）

### 阶段 1：Setup
1. `ecm-setup:project-init` ✅
2. `ecm-setup:file-classify`
3. `ecm-setup:file-organize`

### 阶段 2：Design
4. `ecm-design:deal-structure` — 发行方案（品种选择 / 期限 / 利率机制 / 增信）

### 阶段 3：Due Diligence
5. `ecm-dd:dd-approval`
6. `ecm-dd:dd-entity`
7. `ecm-dd:dd-history`
8. `ecm-dd:dd-debt` — 债务 / 偿债能力（债券项目尤其关键）
9. `ecm-dd:dd-compliance`
10. `ecm-dd:dd-litigation`

### 阶段 4：Draft
11. `ecm-draft:opinion-letter`
12. `ecm-draft:disclosure-review` — 募集说明书 / 发行条款

### 阶段 5：QC
13. `ecm-qc:opinion-letter-review`
14. `ecm-qc:disclosure-review`

---

## 其他 / 未知类型

如果项目类型无法明确归入上述 5 类，使用以下通用骨架，由律师按需调整：

1. `ecm-setup:project-init` ✅
2. `ecm-setup:file-classify`
3. `ecm-setup:file-organize`
4. `ecm-research:reg-search` — 先做法规检索，确认监管框架
5. `ecm-design:deal-structure` — 基础交易结构设计
6. 按需调用 `ecm-dd:dd-*`
7. 按需调用 `ecm-draft:*`
8. 按需调用 `ecm-qc:*`

---

## 维护

新增项目类型、调整 roadmap 步骤时：

1. 更新本文件
2. 同步更新 `SKILL.md` 里 "Phase 2 — 项目配置 → 项目类型变体子目录" 和 "简要版 Roadmap"
3. 如果新增了本仓库还没有的 skill，在 `docs/skill-roadmap.md` 里加占位
4. 在 `CHANGELOG.md` 记为 Changed
