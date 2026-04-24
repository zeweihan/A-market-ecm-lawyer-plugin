# 数据连接器使用说明 / Data Connectors

`scripts/` 目录下的数据连接器脚本，为 `ecm-dd:dd-data-verify` 等需要调用外部数据源
的 skill 提供"取数"底层能力。脚本本身不做业务判断，**所有比对逻辑、风险分级、建议措施由
上层 Skill 负责**。

## 脚本清单

| 脚本 | 功能 | 依赖的环境变量 |
|------|------|---------------|
| `scripts/tushare_connector.py` | Tushare Pro（上市公司行情 / 工商 / 财务数据） | `TUSHARE_TOKEN` |
| `scripts/qcc_connector.py` | 企查查开放平台（工商 / 股东 / 主要人员 / 知识产权 / 行政处罚） | `QCC_APPKEY`、`QCC_SECRET` |

## 安装

```bash
pip install -r scripts/requirements.txt
```

## 环境变量

**所有 API 凭证均通过环境变量注入**，脚本内部不硬编码任何 token/key。推荐在 shell 启动脚本
（`~/.zshrc` / `~/.bashrc`）或项目本地的 `.env`（**不要提交到 git**）里配置：

```bash
export TUSHARE_TOKEN="xxxxxxxxxxxxxxxxxxxxxx"
export QCC_APPKEY="yyyyyyyyy"
export QCC_SECRET="zzzzzzzzzzzz"
```

## 预检（smoke test）

每个脚本都带 `--smoke` 参数，不发真实请求，仅打印客户端状态。推荐在 CI 或新机器上先跑一遍：

```bash
python scripts/tushare_connector.py --smoke
python scripts/qcc_connector.py --smoke
```

没有环境变量时 `--smoke` 依然会返回 exit 0（并友好提示凭证未设置）——这是预期行为，
确保 skill 即便在没有 API 的机器上也能"可加载、可预检、仅业务调用 fallback"。

## CLI 示例

```bash
# Tushare：查"贵州茅台"基础 + 公司详情
python scripts/tushare_connector.py --name 贵州茅台 --fields full

# Tushare：查 600519.SH 2024 年年报财务指标
python scripts/tushare_connector.py --ts-code 600519.SH --period 20241231 --financials

# 企查查：按关键字查基础工商信息
python scripts/qcc_connector.py --basic 腾讯科技

# 企查查：按 KeyNo 组合拉多维数据（常用于 DD 批量核查）
python scripts/qcc_connector.py --detail <KeyNo> --shareholders <KeyNo> --penalty <KeyNo>
```

## 作为 Python 库使用

```python
from scripts.tushare_connector import TushareClient, MissingCredentialError
from scripts.qcc_connector import QccClient

ts = TushareClient()       # 自动从 TUSHARE_TOKEN 读取
qcc = QccClient()          # 自动从 QCC_APPKEY / QCC_SECRET 读取

try:
    df = ts.stock_basic(name="贵州茅台")
    basic = qcc.company_basic("腾讯科技（深圳）有限公司")
except MissingCredentialError:
    # 凭证缺失：上层 Skill 进入 fallback —— 输出"人工核对清单"
    pass
```

## 异常分层

| 异常 | 含义 | 上层 Skill 推荐处理 |
|------|------|---------------------|
| `MissingCredentialError` | 环境变量未设置 | 进入 fallback：输出"人工核对清单"，不再尝试本次 API 调用 |
| `*APIError`（业务错误）| 凭证有效但业务返回错误 (code != 0 / Status != 200) | 记入"比对报告 / 本项 API 失败"，改为人工核对；不影响其他项 |
| `*TransportError`（网络 / HTTP）| 超时、502、JSON 解析失败 | 可以重试一次；若仍失败则同"业务错误"处理 |

## 安全约束

1. **凭证绝不硬编码**。任何 PR 如果在脚本里写了明文 token / key，审核阶段必须驳回。
2. **凭证绝不落盘到工作目录**。`.env` 必须在根 `.gitignore` 中排除。
3. **日志不打印凭证**。脚本打印 headers 时只打印 `Token` 的 MD5，不打印 AppKey / Secret 原文。
4. **限流与配额**：Tushare 免费 token 有每分钟 / 每天调用上限；企查查按次扣费。DD 批量调用
   前建议先看 `--smoke` 输出确认 key 正确，以免把额度用在错 key 上。

## 故障排查

| 现象 | 可能原因 | 处置 |
|------|---------|------|
| `MissingCredentialError` | 环境变量未 export 到当前 shell | `echo $TUSHARE_TOKEN` 验证；注意 GUI 启动的 IDE 可能读不到 `~/.zshrc` |
| Tushare `code=2002` | 接口调用权限不足（积分 / 套餐问题） | 登录 tushare.pro 检查账号权限；部分接口需要付费订阅 |
| Tushare `code=-2001` | 调用超限 | 减少并发 / 等待一分钟再重试；或升级套餐 |
| 企查查 `Status=401` | AppKey/Secret 签名错误 | 检查是否与开放平台控制台一致；注意两端 `Secret` 易混淆 |
| 企查查 `Status=404` | 接口路径变化 | 以企查查最新开放平台文档为准；用 `QccClient.call()` 调未封装的路径 |

## 维护

新增数据源时：

1. 在 `scripts/` 下新增 `<source>_connector.py`，沿用相同设计约束（dataclass client / 异常三层 / `--smoke` CLI）。
2. 在本文件表格里加一行。
3. 在 `scripts/requirements.txt` 里追加 pin 到次版本的依赖。
4. 在 `ecm-dd:dd-data-verify` 的 SKILL.md "可选数据源"段落里登记。
