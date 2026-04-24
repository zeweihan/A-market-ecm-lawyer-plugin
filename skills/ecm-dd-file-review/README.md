# ecm-dd-file-review

ECM 尽职调查工具类 skill：对已归位到项目目录的客户文件做批量阅读、字段抽取、跨文件
一致性核查，输出"文件审阅摘要"供业务 DD skill 作为输入使用。

本 skill **不输出** DD Memo（五段式）。合规结论由业务 DD skill 完成。

## 快速开始

```bash
# 扫描目录
python skills/ecm-dd-file-review/scripts/scan_folder.py 02-尽职调查/02-03-设立/

# 外部 skill 不可用时的兜底文本抽取
python skills/ecm-dd-file-review/scripts/fallback_read.py 某文件.pdf
```

详见 [SKILL.md](./SKILL.md)。

## 依赖

本 skill 优先调用 Anthropic 官方 `pdf` / `docx` / `xlsx` 外部 skill；缺失时走
[scripts/fallback_read.py](./scripts/fallback_read.py) 做最低限度的文本抽取。
