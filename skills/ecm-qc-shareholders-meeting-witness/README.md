# Shareholders-Meeting Witness Review Skill

A [Claude Agent Skill](https://docs.claude.com/en/docs/skills) that performs
internal quality control (内核) review of Chinese A-share shareholders'
meeting witness legal opinions (股东大会法律见证意见书) — producing a
tracked-changes Word document with inline comments based on public Chinese
securities regulations and industry practice.

> [English short intro above; full documentation in Chinese below.]

---

## 这是什么

面向中国 A 股上市公司（及新三板挂牌公司）**股东（大）会法律见证业务**
的内核审查 Claude Skill。当律师项目组起草完一份股东大会见证意见（法律
意见书）后，把文件交给本 skill，它会扮演"内核小组"角色，对照公开法规
和行业实务经验，输出一份带修订痕迹（Track Changes）和批注（Comments）
的 Word 文档。

**与通用的"让 Claude 帮我看一下文档"相比，本 skill 特有的价值**：

1. **三级降级的参考文件获取** — 自动从巨潮资讯网拉取该公司对应届次的
   "股东大会通知"和"董事会决议公告"两份关键参考文件；拉不到则提示
   用户上传；两者都没有则跳过交叉比对并显式说明。
2. **12 项核心字段交叉核对** — 在拿到参考文件的情况下，对见证意见与
   通知/决议做逐字段事实性核对（日期/时间/届次/地点/股权登记日/议案
   清单/特别决议标注/关联回避/中小投资者单独计票/董事会届次等）。
3. **9 类真实高频错误扫描** — 基础信息类、议案结构类、特别决议类、累积
   投票类、关联回避类、模板残留类、章程适用类、底稿类、质控程序类。
4. **形式要件 14 项清单勾对** — 标题、声明段、结论措辞、签字律师、
   律所盖章等。
5. **严格的输出格式约束** — 修订者固定为可配置的名称（默认"内核"）；
   最小显示改动原则（只标记变动的字符，不整段替换）；解释文字只进
   批注，不进正文。

## 快速开始

### 安装（Claude Desktop）

1. 下载最新的 `ecm-qc-shareholders-meeting-witness.skill` 文件
   （或从源码打包：`python -m scripts.package_skill <path-to-this-repo>`）
2. 打开 Claude Desktop → Settings → Skills → Upload
3. 选择 `.skill` 文件上传即可

### 使用

1. 在 Claude Desktop 新开一个对话
2. 上传你要审查的股东大会见证意见（`.docx` 文件）
3. 告诉 Claude："帮我内核审查一下这份见证意见"（或 "review this"、
   "出内核意见"、"挑错" 等均可触发）
4. Claude 会自动：
   - 读取文档，识别公司股票代码和股东大会召开日期
   - 尝试从巨潮资讯网拉取参考文件
   - 若失败，提示你手动上传或跳过
   - 执行四维度审查（交叉比对 + 形式 + 实质 + 常见错误扫描）
   - 生成带修订痕迹和批注的 Word 文档

### 首次使用的依赖安装

Claude 第一次调用本 skill 时会自动执行：

```bash
pip install requests pypdf --break-system-packages
```

这两个依赖用于从巨潮资讯网下载公告 PDF 并抽取文本。

## 三级降级逻辑（Reference File Retrieval）

这是本 skill 最重要的流程特性。日常真实场景中，"自动拉取"未必总能成功
（网络问题、股票代码识别不出、退市公司、未披露、等等）；本 skill 设计了
明确的降级路径：

```
Level 1 · 自动拉取
  └─ 成功 → 进入交叉比对审查
  └─ 失败 ↓

Level 2 · 提示用户上传
  └─ 用户上传文件 → 读取后进入交叉比对审查
  └─ 用户无文件 ↓

Level 3 · 跳过交叉比对 + 在输出文档顶部插入整体性批注
         明确告知"本次内核未进行与股东大会通知/董事会决议
         公告的交叉核对"，只做形式 + 实质 + 常见错误扫描
```

## 数据来源选型

本 skill **仅依赖公开数据源**，不需要任何付费 API key：

| 数据源 | 是否采用 | 说明 |
|---|---|---|
| [AKShare](https://github.com/akfamily/akshare) / 巨潮资讯网公开 API | ✅ 采用 | 证监会指定法定披露平台；免费；有 `category=股东大会/董事会` 精确分类筛选 |
| [Tushare Pro](https://tushare.pro) `anns_d` 接口 | ❌ 未采用 | 数据质量同等，但需要单独付费权限 |
| [企查查 MCP](https://agent.qcc.com/) | ❌ 不适用 | 企查查主打工商/司法/知识产权数据，不含上市公司法定披露公告 |

替换数据源很容易：只需修改 `scripts/fetch_cninfo_announcements.py` 里的
`search()` 函数即可保持上层工作流不变。

## 项目结构

```
ecm-qc-shareholders-meeting-witness/
├── SKILL.md                         # 主入口：工作流 + 配置 + 免责声明
├── LICENSE                          # MIT
├── README.md                        # 本文件
├── scripts/
│   └── fetch_cninfo_announcements.py   # 巨潮公告拉取脚本
└── references/
    ├── cross-check-matrix.md        # 12 项字段交叉比对矩阵
    ├── form-requirements.md         # 形式要件 14 项清单
    ├── substantive-checklist.md     # 实质审查 8 类要点
    ├── common-errors.md             # 9 类常见错误模式库
    └── comment-templates.md         # 批注标准话术模板
```

## 配置

**修订者名称**（用于 tracked change 和 comment 的作者字段）

默认为 `内核`。如需自定义（如 `质控`、`合规`、`DC`、某律所特定审查团队
名），只需在对话开始时告诉 Claude 即可，例如：

> "请把本次审查的修订者名称改为'质控'。"

Claude 会在整个 workflow 中保持一致。

## 法规依据

本 skill 的全部审查标准均基于公开发布的法规：

- 《公司法》（2024 年修订）
- 《上市公司股东会规则》（2025 年修订）
- 《律师事务所从事证券法律业务管理办法》（中国证监会 2019 年第 223 号令）
- 《律师事务所从事证券法律业务执业规则》（中华全国律师协会）
- 《公开发行证券公司信息披露的编报规则第 12 号》

未引用任何律所、组织或个人的非公开内部资料。

## 局限性

- **仅适用于中国 A 股 / 新三板市场**的股东（大）会见证业务。不适用于
  港股、美股或其他境外市场。
- **不做法律判断** — 所有"含糊/需要专业核查"的事项都以【核实】批注的
  形式转交签字律师决定，不替代律师做实体判断。
- **不访问公司内部系统** — 涉及内部工作底稿、律师执业关系、转委托等
  事项仅以【底稿】【核实】批注提示，不自动核查。
- **依赖巨潮公开披露的时效性** — 极个别公司可能披露延迟或未在常规
  时间窗口内披露，此时自动拉取会失败，需用户手动上传。

## 贡献

欢迎 PR。适合贡献的方向包括：

- **新增常见错误类型**（如某类议案的新监管点）→ 更新
  `references/common-errors.md` + `references/comment-templates.md`
- **改进自动挑选启发式**（应对 "同一天多份董事会决议公告" 等边缘情形）
  → 修改 `scripts/fetch_cninfo_announcements.py` 中的 `pick_*` 函数
- **扩展到其他市场**（港股披露易 HKEXnews / 美股 SEC EDGAR）→ 新增
  `scripts/fetch_<market>.py` 并在 SKILL.md 里加分支逻辑

请在 PR 中保持：
- 所有示例用虚构公司名（"某公司"、"示例上市公司"），不使用真实公司名
- 引用的规则/条例均为公开发布版本
- 中文标点符号规范（全角引号、破折号等）

## License

MIT — 详见 [LICENSE](./LICENSE) 文件。

Skill 输出不构成法律意见，使用者应自行核实并由签字律师承担最终责任。
