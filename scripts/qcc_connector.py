#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qcc_connector.py — 企查查（QCC）开放平台接口薄封装

服务于 `ecm-dd:dd-data-verify`：用企查查工商数据反查客户提供的营业执照、股东册、
主要人员、知识产权、行政处罚等材料。

依赖：
    - 环境变量 QCC_APPKEY（必需）
    - 环境变量 QCC_SECRET（必需）
    - pip install -r scripts/requirements.txt

鉴权机制（企查查开放平台默认约定）：
    Token = MD5(AppKey + Timespan + SecretKey).upper()
    HTTP header 带 `Token` 和 `Timespan`；URL 附带 `key=AppKey`。
    具体接口路径与字段以企查查最新官方文档为准；本脚本只封装几个 DD 高频接口，
    其他接口可用 `.call(path, params)` 直接调用。

基本用法（作为库）：

    from scripts.qcc_connector import QccClient
    c = QccClient()
    basic = c.company_basic("腾讯科技（深圳）有限公司")

命令行用法（smoke test）：

    python scripts/qcc_connector.py --smoke
    python scripts/qcc_connector.py --basic 腾讯科技

设计约束同 tushare_connector.py：凭证走环境变量、异常分层、无凭证进 fallback。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Optional

try:
    import requests
except ImportError as _imp_err:  # pragma: no cover
    sys.stderr.write(
        f"[qcc_connector] 缺少依赖：{_imp_err}\n"
        "请先执行：pip install -r scripts/requirements.txt\n"
    )
    raise

QCC_BASE_URL = "https://api.qichacha.com"
DEFAULT_TIMEOUT_SEC = 30


# ---------- 异常 ------------------------------------------------------------


class QccError(Exception):
    """企查查相关错误基类。"""


class MissingCredentialError(QccError):
    """未同时设置 QCC_APPKEY 和 QCC_SECRET。上层 Skill 据此 fallback。"""


class QccAPIError(QccError):
    """业务层错误（Status != '200'）。"""


class QccTransportError(QccError):
    """HTTP / 网络 / JSON 解析错误。"""


# ---------- 客户端 ----------------------------------------------------------


@dataclass
class QccClient:
    """企查查开放平台通用调用器。

    每个 get 方法返回的是企查查的原始 JSON（`dict`），保留 `Paging`/`Result`/`Status`
    等字段，由上层 Skill 再做字段抽取 —— 因为 DD 比对常需要保留完整返回便于追溯。
    """

    appkey: Optional[str] = None
    secret: Optional[str] = None
    base_url: str = QCC_BASE_URL
    timeout: int = DEFAULT_TIMEOUT_SEC

    def __post_init__(self) -> None:
        if self.appkey is None:
            self.appkey = os.environ.get("QCC_APPKEY", "")
        if self.secret is None:
            self.secret = os.environ.get("QCC_SECRET", "")

    @property
    def has_credential(self) -> bool:
        return bool(self.appkey and self.secret)

    def _sign_headers(self) -> dict[str, str]:
        """生成企查查要求的 Token / Timespan 签名头。"""
        if not self.has_credential:
            raise MissingCredentialError(
                "未设置 QCC_APPKEY / QCC_SECRET 环境变量。"
                "请 export QCC_APPKEY=... QCC_SECRET=... 或显式传入构造参数。"
            )
        timespan = str(int(time.time()))
        raw = f"{self.appkey}{timespan}{self.secret}"
        token = hashlib.md5(raw.encode("utf-8")).hexdigest().upper()
        return {"Token": token, "Timespan": timespan}

    def call(self, path: str, params: Optional[dict[str, Any]] = None) -> dict:
        """通用 GET 调用。`path` 是 `/ECIV4/GetBasicDetailsByName` 这样的相对路径。"""
        url = f"{self.base_url}{path}"
        full_params = dict(params or {})
        full_params.setdefault("key", self.appkey)
        try:
            resp = requests.get(
                url,
                headers=self._sign_headers(),
                params=full_params,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            body = resp.json()
        except requests.RequestException as exc:
            raise QccTransportError(f"HTTP / 网络错误：{exc}") from exc
        except ValueError as exc:
            raise QccTransportError(f"响应非合法 JSON：{exc}") from exc

        status = str(body.get("Status", ""))
        if status and status != "200":
            raise QccAPIError(
                f"企查查业务错误 Status={status} Message={body.get('Message')}"
            )
        return body

    # -- dd-data-verify 高频接口 --------------------------------------------

    def company_basic(self, keyword: str) -> dict:
        """按公司名称 / 统一社会信用代码关键字查基础工商信息。"""
        return self.call(
            "/ECIV4/GetBasicDetailsByName", params={"keyword": keyword}
        )

    def company_detail(self, keyno: str) -> dict:
        """按 KeyNo 查企业完整工商详情。"""
        return self.call(
            "/ECIV4/GetCompanyDetailsByName", params={"keyWord": keyno}
        )

    def shareholders(self, keyno: str) -> dict:
        """股东及出资信息。"""
        return self.call(
            "/ECIV4/GetStockCertificateInfo", params={"keyNo": keyno}
        )

    def employees(self, keyno: str) -> dict:
        """主要人员（法定代表人 / 董监高）。"""
        return self.call("/ECIV4/GetEmployees", params={"keyNo": keyno})

    def intellectual_property(self, keyno: str) -> dict:
        """知识产权（专利 / 商标 / 软著）。"""
        return self.call(
            "/ECIV4/GetIntellectualProperty", params={"keyNo": keyno}
        )

    def penalty(self, keyno: str) -> dict:
        """行政处罚信息。"""
        return self.call("/ECIV4/GetPenaltyInfo", params={"keyNo": keyno})

    def change_records(self, keyno: str) -> dict:
        """工商变更记录（名称 / 注册资本 / 法定代表人 / 股东等变更）。"""
        return self.call("/ECIV4/GetChangeRecords", params={"keyNo": keyno})


# ---------- CLI -------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="企查查开放平台薄封装 —— ECM DD 自动比对场景使用。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "常用：\n"
            "  export QCC_APPKEY=xxx QCC_SECRET=yyy\n"
            "  python scripts/qcc_connector.py --basic 腾讯科技\n"
            "  python scripts/qcc_connector.py --detail <KeyNo>\n"
            "  python scripts/qcc_connector.py --smoke\n"
        ),
    )
    parser.add_argument("--basic", help="按公司名关键字查基础工商信息")
    parser.add_argument("--detail", help="按 KeyNo 查完整工商详情")
    parser.add_argument("--shareholders", help="按 KeyNo 查股东及出资")
    parser.add_argument("--employees", help="按 KeyNo 查主要人员")
    parser.add_argument("--ip", help="按 KeyNo 查知识产权")
    parser.add_argument("--penalty", help="按 KeyNo 查行政处罚")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="不发真实请求，仅打印 client 状态",
    )
    return parser


def _smoke_test(client: QccClient) -> int:
    print("[qcc_connector] smoke test")
    print(f"  has_credential = {client.has_credential}")
    print(f"  base_url       = {client.base_url}")
    print(f"  timeout        = {client.timeout}s")
    if not client.has_credential:
        print(
            "  NOTE: QCC_APPKEY / QCC_SECRET 未设置。脚本可 import，但调用真实接口"
            "会抛 MissingCredentialError（这是预期行为）。"
        )
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    args = _build_argparser().parse_args(argv)
    client = QccClient()

    if args.smoke:
        return _smoke_test(client)

    # 先收集"要调用什么"（lambda 延迟执行，这样异常会在 try 里被捕获）
    actions: list[tuple[str, Any]] = []
    if args.basic:
        actions.append(("company_basic", lambda: client.company_basic(args.basic)))
    if args.detail:
        actions.append(("company_detail", lambda: client.company_detail(args.detail)))
    if args.shareholders:
        actions.append(
            ("shareholders", lambda: client.shareholders(args.shareholders))
        )
    if args.employees:
        actions.append(("employees", lambda: client.employees(args.employees)))
    if args.ip:
        actions.append(
            ("intellectual_property", lambda: client.intellectual_property(args.ip))
        )
    if args.penalty:
        actions.append(("penalty", lambda: client.penalty(args.penalty)))

    if not actions:
        sys.stderr.write(
            "错误：需至少一个查询参数（--basic / --detail / ...），"
            "或使用 --smoke 做预检。\n"
        )
        return 2

    try:
        for name, thunk in actions:
            body = thunk()
            print(f"=== {name} ===")
            print(json.dumps(body, ensure_ascii=False, indent=2))
    except MissingCredentialError as exc:
        sys.stderr.write(f"[MissingCredentialError] {exc}\n")
        return 3
    except QccAPIError as exc:
        sys.stderr.write(f"[QccAPIError] {exc}\n")
        return 4
    except QccTransportError as exc:
        sys.stderr.write(f"[QccTransportError] {exc}\n")
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
