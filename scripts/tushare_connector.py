#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tushare_connector.py — Tushare Pro 通用接口薄封装

服务于 `ecm-dd:dd-data-verify` 这类需要"以第三方公开数据反查客户提供材料"的场景。
脚本只负责"取数"，不负责业务判断；所有比对、风险分级、建议由上层 Skill 处理。

依赖：
    - 环境变量 TUSHARE_TOKEN（必需；未设置时所有请求都会直接退化到 fallback）
    - pip install -r scripts/requirements.txt

基本用法（作为库）：

    from scripts.tushare_connector import TushareClient
    client = TushareClient()  # 从环境变量读 token
    df = client.stock_basic(name="贵州茅台")
    print(df)

命令行用法（作为脚本）：

    # smoke test：不发真实请求，仅打印客户端状态
    python scripts/tushare_connector.py --smoke

    # 按公司简称查基础资料
    python scripts/tushare_connector.py --name 贵州茅台

    # 按 ts_code 查
    python scripts/tushare_connector.py --ts-code 600519.SH --fields full

设计约束：
    1. API key 走环境变量，**绝不硬编码**。
    2. 无 token 时 `TushareClient()` 仍能被 import，但调用真实接口会抛
       `MissingCredentialError`，上层 Skill 据此落到 fallback（人工核对清单）。
    3. 网络错误、HTTP 非 2xx、Tushare 业务错误 (code != 0) 各自独立异常，方便上层区分。
    4. 所有查询函数返回 pandas.DataFrame，空结果返回空 DataFrame，不返回 None。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Optional

try:
    import pandas as pd
    import requests
except ImportError as _imp_err:  # pragma: no cover
    sys.stderr.write(
        f"[tushare_connector] 缺少依赖：{_imp_err}\n"
        "请先执行：pip install -r scripts/requirements.txt\n"
    )
    raise

TUSHARE_API_URL = "http://api.tushare.pro"
DEFAULT_TIMEOUT_SEC = 30


# ---------- 异常定义 --------------------------------------------------------


class TushareError(Exception):
    """Tushare 相关错误的基类。"""


class MissingCredentialError(TushareError):
    """未设置 TUSHARE_TOKEN。上层 Skill 捕获本异常后应进入 fallback。"""


class TushareAPIError(TushareError):
    """Tushare 业务层错误（code != 0）。携带原始 msg。"""


class TushareTransportError(TushareError):
    """HTTP / 网络层错误（超时、502、JSON 解析失败等）。"""


# ---------- 客户端 ----------------------------------------------------------


@dataclass
class TushareClient:
    """Tushare Pro 通用接口薄封装。

    参数：
        token: 显式传入 token；默认读环境变量 TUSHARE_TOKEN。
        api_url: 接口地址；一般无需修改。
        timeout: 单次请求超时（秒）。
    """

    token: Optional[str] = None
    api_url: str = TUSHARE_API_URL
    timeout: int = DEFAULT_TIMEOUT_SEC

    def __post_init__(self) -> None:
        if self.token is None:
            self.token = os.environ.get("TUSHARE_TOKEN", "")

    # -- 低层调用 -----------------------------------------------------------

    @property
    def has_credential(self) -> bool:
        return bool(self.token)

    def call(
        self,
        api_name: str,
        params: Optional[dict[str, Any]] = None,
        fields: Optional[str] = None,
    ) -> pd.DataFrame:
        """调用任意 Tushare Pro 接口，返回 DataFrame。"""
        if not self.has_credential:
            raise MissingCredentialError(
                "未设置 TUSHARE_TOKEN 环境变量；请在 shell 中 export TUSHARE_TOKEN=xxx "
                "或在调用 TushareClient(token=...) 时显式传入。"
            )

        payload = {
            "api_name": api_name,
            "token": self.token,
            "params": params or {},
            "fields": fields or "",
        }
        try:
            resp = requests.post(self.api_url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            raise TushareTransportError(f"HTTP / 网络错误：{exc}") from exc
        except ValueError as exc:  # JSONDecodeError
            raise TushareTransportError(f"响应非合法 JSON：{exc}") from exc

        if data.get("code", 0) != 0:
            raise TushareAPIError(
                f"Tushare 业务错误 code={data.get('code')} msg={data.get('msg')}"
            )

        body = data.get("data") or {}
        items = body.get("items") or []
        columns = body.get("fields") or []
        return pd.DataFrame(items, columns=columns)

    # -- dd-data-verify 使用的预置接口 --------------------------------------

    def stock_basic(
        self, ts_code: Optional[str] = None, name: Optional[str] = None
    ) -> pd.DataFrame:
        """股票基础信息（沪深 A 股 + 创业 + 科创 + 北交所）。"""
        params: dict[str, Any] = {}
        if ts_code:
            params["ts_code"] = ts_code
        if name:
            params["name"] = name
        return self.call("stock_basic", params=params)

    def stock_company(self, ts_code: str) -> pd.DataFrame:
        """上市公司基本信息（工商口径，含注册资本、实控人、主营业务等）。"""
        return self.call("stock_company", params={"ts_code": ts_code})

    def top10_holders(self, ts_code: str, period: str) -> pd.DataFrame:
        """前十大股东。period 格式 YYYYMMDD，一般传季度末（如 20241231）。"""
        return self.call(
            "top10_holders", params={"ts_code": ts_code, "period": period}
        )

    def top10_floatholders(self, ts_code: str, period: str) -> pd.DataFrame:
        """前十大流通股东。"""
        return self.call(
            "top10_floatholders", params={"ts_code": ts_code, "period": period}
        )

    def fina_indicator(self, ts_code: str, period: str) -> pd.DataFrame:
        """财务指标（每股收益、ROE、资产负债率等）。"""
        return self.call(
            "fina_indicator", params={"ts_code": ts_code, "period": period}
        )

    def income(self, ts_code: str, period: str) -> pd.DataFrame:
        """利润表。"""
        return self.call("income", params={"ts_code": ts_code, "period": period})

    def balancesheet(self, ts_code: str, period: str) -> pd.DataFrame:
        """资产负债表。"""
        return self.call(
            "balancesheet", params={"ts_code": ts_code, "period": period}
        )


# ---------- CLI 入口 --------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tushare Pro 通用接口薄封装 —— ECM DD 自动比对场景使用。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "常用：\n"
            "  export TUSHARE_TOKEN=xxxxxx\n"
            "  python scripts/tushare_connector.py --name 贵州茅台\n"
            "  python scripts/tushare_connector.py --ts-code 600519.SH\n"
            "  python scripts/tushare_connector.py --smoke     # 不发请求，仅打印状态\n"
        ),
    )
    parser.add_argument("--name", help="公司简称（证券简称）")
    parser.add_argument("--ts-code", dest="ts_code", help="ts_code，例如 600519.SH")
    parser.add_argument(
        "--fields",
        choices=["basic", "full"],
        default="basic",
        help="basic（只取 stock_basic）或 full（同时取 stock_company）",
    )
    parser.add_argument(
        "--period",
        help="报告期 YYYYMMDD（如 20241231），给 --financials 用",
    )
    parser.add_argument(
        "--financials",
        action="store_true",
        help="附加查询 fina_indicator 最新财务指标（需 --ts-code + --period）",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="不发真实请求，仅打印 client 状态（供 CI / 预检使用）",
    )
    return parser


def _smoke_test(client: TushareClient) -> int:
    print("[tushare_connector] smoke test")
    print(f"  has_credential = {client.has_credential}")
    print(f"  api_url        = {client.api_url}")
    print(f"  timeout        = {client.timeout}s")
    if not client.has_credential:
        print(
            "  NOTE: TUSHARE_TOKEN 未设置。脚本可 import，但调用真实接口会抛"
            " MissingCredentialError（这是预期行为）。"
        )
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    args = _build_argparser().parse_args(argv)
    client = TushareClient()

    if args.smoke:
        return _smoke_test(client)

    if not args.name and not args.ts_code:
        sys.stderr.write(
            "错误：需要至少一个 --name 或 --ts-code（或使用 --smoke 走预检）。\n"
        )
        return 2

    try:
        basic = client.stock_basic(ts_code=args.ts_code, name=args.name)
        print("=== stock_basic ===")
        print(basic.to_string(index=False) if not basic.empty else "(空结果)")

        if args.fields == "full" and not basic.empty and args.ts_code is None:
            # 用 basic 里第一个 ts_code 去取 company 详情
            args.ts_code = basic.iloc[0]["ts_code"]

        if args.fields == "full" and args.ts_code:
            company = client.stock_company(args.ts_code)
            print("\n=== stock_company ===")
            print(company.to_string(index=False) if not company.empty else "(空结果)")

        if args.financials:
            if not (args.ts_code and args.period):
                sys.stderr.write(
                    "错误：--financials 需要同时提供 --ts-code 和 --period。\n"
                )
                return 2
            fina = client.fina_indicator(args.ts_code, args.period)
            print("\n=== fina_indicator ===")
            print(fina.to_string(index=False) if not fina.empty else "(空结果)")
    except MissingCredentialError as exc:
        sys.stderr.write(f"[MissingCredentialError] {exc}\n")
        return 3
    except TushareAPIError as exc:
        sys.stderr.write(f"[TushareAPIError] {exc}\n")
        return 4
    except TushareTransportError as exc:
        sys.stderr.write(f"[TushareTransportError] {exc}\n")
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
