#!/usr/bin/env python3
"""
fetch_cninfo_announcements.py
================================

拉取股东大会通知 + 发出该通知的董事会决议公告，用于内核审查的交叉比对。

数据源：巨潮资讯网（证监会指定的 A 股法定信息披露平台）
调用接口：http://www.cninfo.com.cn/new/hisAnnouncement/query（POST）

依赖：
  - requests
  - pypdf  （纯 Python，跨平台；pip install pypdf）

用法：
  python fetch_cninfo_announcements.py \\
      --stock-code 002807 \\
      --meeting-date 20250325 \\
      --output-dir /tmp/refs

输出：
  打印一个 JSON 到 stdout，包含：
    - 两份文件的元数据 + 已下载 PDF 路径 + 抽取的文本路径
    - 所有候选公告列表（便于人工确认自动挑选是否正确）
    - errors 数组（遇到的任何问题）

退出码：
  0 — 两份文件都拿到
  1 — 只拿到其中一份
  2 — 一份都没拿到（调用方应降级到手动上传）

设计原则：本脚本不 fail-hard；任何异常都收集到 errors 里并继续执行，
调用方根据 JSON 和退出码决定是否降级。
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

# ---------- 常量 ----------

CNINFO_STOCK_LIST_URLS = {
    "沪深京": "http://www.cninfo.com.cn/new/data/szse_stock.json",
    "三板": "http://www.cninfo.com.cn/new/data/gfzr_stock.json",
}

CNINFO_QUERY_API = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_STATIC_BASE = "http://static.cninfo.com.cn/"

# 巨潮按"股东大会"和"董事会"两个类目检索。这两个类目名是见证业务最核心的两份底稿。
CATEGORY_CODES = {
    "股东大会": "category_gddh_szsh",
    "董事会": "category_dshgg_szsh",
}

# 巨潮 POST 要用浏览器型 UA 否则可能被拒
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

CST = timezone(timedelta(hours=8))

# ---------- 工具函数 ----------


def ms_to_cst(ms) -> str:
    """巨潮返回的 announcementTime 是 Unix 毫秒；转北京时间字符串。"""
    if not ms:
        return ""
    try:
        dt = datetime.fromtimestamp(int(ms) / 1000, tz=CST)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ms)


def get_org_id(stock_code: str, market: str = "沪深京") -> str:
    """从巨潮拉全量股票列表，拿到该股票的 orgId。orgId 是巨潮内部主键。"""
    url = CNINFO_STOCK_LIST_URLS.get(market, CNINFO_STOCK_LIST_URLS["沪深京"])
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    for item in data.get("stockList", []):
        if item.get("code") == stock_code:
            return item["orgId"]
    raise ValueError(
        f"股票代码 {stock_code} 不在巨潮 {market} 列表中。"
        f"可能是代码错误、或股票已退市、或板块不对（沪深京/三板）。"
    )


def search(stock_code: str, org_id: str, category: str,
           start_date: str, end_date: str) -> list:
    """调 cninfo POST API，返回原始 announcements 列表（含 adjunctUrl）。

    日期格式：YYYYMMDD 字符串（脚本内部用）；传给 cninfo 时改成 YYYY-MM-DD~YYYY-MM-DD。
    """
    se_date = (
        f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:]}"
        f"~{end_date[:4]}-{end_date[4:6]}-{end_date[6:]}"
    )
    payload = {
        "pageNum": "1",
        "pageSize": "30",
        "column": "szse",
        "tabName": "fulltext",
        "plate": "",
        "stock": f"{stock_code},{org_id}",
        "searchkey": "",
        "secid": "",
        "category": CATEGORY_CODES[category],
        "trade": "",
        "seDate": se_date,
        "sortName": "time",
        "sortType": "desc",
        "isHLtitle": "true",
    }
    r = requests.post(CNINFO_QUERY_API, data=payload, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data.get("announcements") or []


def pick_shareholders_notice(anns: list, meeting_dt: datetime) -> dict | None:
    """从'股东大会'类目里挑出'召开...股东大会的通知'。

    规则：标题同时含'股东'、'通知'，排除'补充通知''会议资料''决议公告'这些其他类型；
    候选多个时选公告时间距会议最近的。
    """
    candidates = []
    for a in anns:
        title = a.get("announcementTitle", "") or ""
        if "通知" not in title:
            continue
        if not ("股东大会" in title or "股东会" in title):
            continue
        # 排除以下类型（它们也可能带"通知"但不是我们要的主通知）
        if any(kw in title for kw in ["决议公告", "会议资料", "取消", "延期", "更正"]):
            continue
        candidates.append(a)

    if not candidates:
        return None

    # 按与会议日期的距离排序（越近越优先）
    def dist(a):
        ts = a.get("announcementTime", 0)
        if not ts:
            return float("inf")
        pub_dt = datetime.fromtimestamp(int(ts) / 1000, tz=CST)
        return abs((meeting_dt.replace(tzinfo=CST) - pub_dt).total_seconds())

    candidates.sort(key=dist)
    return candidates[0]


def pick_board_resolution(anns: list, meeting_dt: datetime) -> dict | None:
    """从'董事会'类目里挑出发出股东大会通知的董事会决议公告。

    规则：标题含'董事会'+'决议公告'。多候选时选时间晚于但最接近会议日之前的
    （因为决定召开股东大会的董事会决议通常在股东大会通知同一天或前几天披露）。
    """
    candidates = []
    for a in anns:
        title = a.get("announcementTitle", "") or ""
        if "董事会" not in title:
            continue
        if "决议公告" not in title:
            continue
        # 排除独立董事会议、专门委员会等
        if any(kw in title for kw in ["独立", "专门委员会", "审计委员会", "提名委员会",
                                      "薪酬委员会", "战略委员会"]):
            continue
        candidates.append(a)

    if not candidates:
        return None

    meeting_cst = meeting_dt.replace(tzinfo=CST)

    # 偏好：公告日期 <= 会议日期（即：先披露董事会决议，再开股东会），按距离排序，近的优先
    def score(a):
        ts = a.get("announcementTime", 0)
        if not ts:
            return (2, float("inf"))
        pub_dt = datetime.fromtimestamp(int(ts) / 1000, tz=CST)
        diff = (meeting_cst - pub_dt).total_seconds()
        if diff >= 0:
            return (0, diff)   # 在会议之前披露，优先
        else:
            return (1, -diff)  # 在会议之后披露，次优先

    candidates.sort(key=score)
    return candidates[0]


def build_pdf_url(adjunct_url: str) -> str:
    """将 adjunctUrl（相对路径，如 finalpage/2025-03-28/1224556789.PDF）拼成完整 URL。"""
    return CNINFO_STATIC_BASE + (adjunct_url or "").lstrip("/")


def download_pdf(url: str, out_path: Path) -> None:
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    out_path.write_bytes(r.content)


def extract_pdf_text(pdf_path: Path) -> str:
    """抽取 PDF 文本。优先 pypdf（纯 Python），fallback 到命令行 pdftotext。"""
    # 方案 A：pypdf
    try:
        import pypdf  # type: ignore
        reader = pypdf.PdfReader(str(pdf_path))
        chunks = []
        for page in reader.pages:
            try:
                chunks.append(page.extract_text() or "")
            except Exception:
                chunks.append("")
        text = "\n".join(chunks).strip()
        if text:
            return text
    except Exception:
        pass

    # 方案 B：pdftotext（如果系统装了 poppler）
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=90,
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass

    return ""  # 都失败就返回空串，调用方据此判断是否降级


def ann_to_metadata(a: dict) -> dict:
    """把巨潮原始 announcement dict 缩减为我们关心的元数据字典。"""
    return {
        "title": a.get("announcementTitle"),
        "time_cst": ms_to_cst(a.get("announcementTime")),
        "announcement_id": a.get("announcementId"),
        "org_id": a.get("orgId"),
        "adjunct_url": a.get("adjunctUrl"),
        "pdf_url": build_pdf_url(a.get("adjunctUrl", "")),
        "detail_url": (
            f"http://www.cninfo.com.cn/new/disclosure/detail?"
            f"stockCode={a.get('secCode')}"
            f"&announcementId={a.get('announcementId')}"
            f"&orgId={a.get('orgId')}"
        ),
    }


# ---------- 主流程 ----------


def fetch_one(
    anns: list, picker, meeting_dt: datetime,
    stock_code: str, meeting_date: str,
    label: str, output_dir: Path, errors: list,
) -> tuple[dict | None, list]:
    """对某个类目的 anns 列表，picker 挑出最佳匹配，下载 PDF 并抽文本。

    返回 (主结果 dict 或 None, 候选清单)。
    """
    candidates = [ann_to_metadata(a) for a in anns]

    best = picker(anns, meeting_dt)
    if best is None:
        errors.append(f"未找到{label}（类目内 {len(anns)} 条公告中没有命中规则的候选）")
        return None, candidates

    meta = ann_to_metadata(best)
    pdf_url = meta["pdf_url"]
    if not pdf_url or pdf_url.endswith("/"):
        errors.append(f"{label}候选命中但 adjunctUrl 为空，无法下载 PDF")
        return meta, candidates

    pdf_path = output_dir / f"{label}_{stock_code}_{meeting_date}.pdf"
    txt_path = pdf_path.with_suffix(".txt")
    try:
        download_pdf(pdf_url, pdf_path)
    except Exception as e:
        errors.append(f"{label} PDF 下载失败: {e}")
        return meta, candidates

    try:
        text = extract_pdf_text(pdf_path)
        if text:
            txt_path.write_text(text, encoding="utf-8")
        else:
            errors.append(f"{label} PDF 下载成功但文本抽取为空（可能是扫描版 PDF）")
    except Exception as e:
        errors.append(f"{label} 文本抽取失败: {e}")

    meta["pdf_path"] = str(pdf_path)
    meta["text_path"] = str(txt_path) if txt_path.exists() else None
    meta["text_preview"] = (text[:500] + "...") if text and len(text) > 500 else text
    return meta, candidates


def main() -> int:
    parser = argparse.ArgumentParser(
        description="拉取股东大会通知和董事会决议公告（用于见证意见内核审查交叉比对）"
    )
    parser.add_argument("--stock-code", required=True,
                        help="股票代码，如 002807。沪市 6xxxxx，深市 0xxxxx/3xxxxx，北交所 4xxxxx/8xxxxx")
    parser.add_argument("--meeting-date", required=True,
                        help="股东大会召开日期 YYYYMMDD，如 20250325")
    parser.add_argument("--output-dir", default=".",
                        help="PDF 与文本输出目录（默认当前目录）")
    parser.add_argument("--days-before", type=int, default=45,
                        help="向前搜索天数（默认 45 天，覆盖年度股东大会 20 日通知期 + 余量）")
    parser.add_argument("--market", default="沪深京",
                        choices=["沪深京", "三板"],
                        help="板块：沪深京=A股主板/创业板/科创板/北交所；三板=新三板")
    args = parser.parse_args()

    try:
        meeting_dt = datetime.strptime(args.meeting_date, "%Y%m%d")
    except ValueError:
        print(json.dumps({
            "error": f"meeting-date 格式错误，期望 YYYYMMDD，收到 {args.meeting_date}"
        }, ensure_ascii=False), file=sys.stderr)
        return 2

    start_date = (meeting_dt - timedelta(days=args.days_before)).strftime("%Y%m%d")
    end_date = (meeting_dt + timedelta(days=3)).strftime("%Y%m%d")  # 略微往后留 3 天缓冲

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "query": {
            "stock_code": args.stock_code,
            "meeting_date": args.meeting_date,
            "market": args.market,
            "search_range": [start_date, end_date],
        },
        "shareholders_notice": None,
        "board_resolution": None,
        "shareholders_notice_candidates": [],
        "board_resolution_candidates": [],
        "errors": [],
    }

    # 先拿 orgId
    try:
        org_id = get_org_id(args.stock_code, args.market)
    except Exception as e:
        result["errors"].append(f"获取 orgId 失败: {e}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    # 搜股东大会类目
    try:
        gddh_anns = search(args.stock_code, org_id, "股东大会", start_date, end_date)
    except Exception as e:
        result["errors"].append(f"搜索'股东大会'类目失败: {e}")
        gddh_anns = []

    time.sleep(1)  # 对巨潮服务器友好一点，间隔 1 秒

    # 搜董事会类目
    try:
        dsh_anns = search(args.stock_code, org_id, "董事会", start_date, end_date)
    except Exception as e:
        result["errors"].append(f"搜索'董事会'类目失败: {e}")
        dsh_anns = []

    # 挑选 + 下载 + 抽文本
    notice_meta, notice_cands = fetch_one(
        gddh_anns, pick_shareholders_notice, meeting_dt,
        args.stock_code, args.meeting_date,
        "股东大会通知", output_dir, result["errors"],
    )
    result["shareholders_notice"] = notice_meta
    result["shareholders_notice_candidates"] = notice_cands

    resolution_meta, resolution_cands = fetch_one(
        dsh_anns, pick_board_resolution, meeting_dt,
        args.stock_code, args.meeting_date,
        "董事会决议公告", output_dir, result["errors"],
    )
    result["board_resolution"] = resolution_meta
    result["board_resolution_candidates"] = resolution_cands

    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 退出码
    notice_ok = notice_meta is not None and notice_meta.get("text_path")
    resolution_ok = resolution_meta is not None and resolution_meta.get("text_path")
    if notice_ok and resolution_ok:
        return 0
    elif notice_ok or resolution_ok:
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
