#!/usr/bin/env python3
"""
render_paragraphs.py — 把 docx 文档中每一段的"渲染后编号 + 正文"输出出来。

为什么需要这个脚本？
==============================================================
项目组经常用 Word 自动编号（<w:numPr> + numbering.xml）和手动文本编号
（直接在 <w:t> 里写"一、""1.""（二）"）混搭。

如果只看 <w:t> 文本，会出现下面这种典型误判：

  P42（自动编号 numId=22 ilvl=0）：本次股东会的表决程序
  P47（无 numPr，文本写"（二）"）：（二）本次股东会的表决结果

  → 直觉判断："P47 是（二），但 P42 没有（一），编号不一致"
  → 实际渲染：P42 在 Word 里显示为"（一）本次股东会的表决程序"
            ——因为它的 numId=22 是公司的"（一、二、三）"格式
  → 结论：渲染后两段连贯，没有问题；批注就是误报

本脚本通过解析 word/numbering.xml + word/document.xml，**重建每段的
渲染后编号**，避免上述误判。

用法
==============================================================
    python3 render_paragraphs.py /path/to/file.docx
        → 打印每段的渲染编号 + 正文摘要

    python3 render_paragraphs.py /path/to/file.docx --para 47
        → 只看 P47 的详细信息（自动 vs 手动）

    python3 render_paragraphs.py /path/to/file.docx --numbering-summary
        → 打印 numbering.xml 中每个 numId 的格式

依赖：仅 Python 标准库，无需 pip install
"""

from __future__ import annotations
import sys
import re
import zipfile
import xml.etree.ElementTree as ET
import argparse
from collections import defaultdict

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = "{%s}" % NS["w"]


def chinese_num(n: int) -> str:
    """1 → 一, 2 → 二, ..., 10 → 十, 11 → 十一, ..."""
    if n <= 0:
        return str(n)
    digits = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    if n <= 10:
        return digits[n]
    if n < 20:
        return "十" + digits[n - 10]
    if n < 100:
        return digits[n // 10] + "十" + (digits[n % 10] if n % 10 else "")
    return str(n)


def format_num(n: int, fmt: str) -> str:
    """Render a number according to a Word numFmt.

    Word/OOXML has both ISO standard names and "legacy" Office names —
    Chinese-style 一二三 counters appear under multiple aliases:
      - chineseCounting / chineseCountingThousand / chineseLegalSimplified
      - japaneseCounting / japaneseLegal (legacy CJK shared)
      - taiwaneseCounting / taiwaneseCountingThousand
    All render as 一、二、三... in Word for zh-CN/zh-TW/ja-JP locales.
    """
    chinese_aliases = {
        "chineseCounting", "chineseCountingThousand", "chineseLegalSimplified",
        "japaneseCounting", "japaneseLegal",
        "taiwaneseCounting", "taiwaneseCountingThousand",
        "ideographDigital", "ideographTraditional", "ideographZodiac",
    }
    if fmt in chinese_aliases:
        return chinese_num(n)
    if fmt == "decimalEnclosedCircleChinese":
        return f"（{chinese_num(n)}）"
    if fmt == "lowerLetter":
        return chr(ord("a") + n - 1) if 1 <= n <= 26 else str(n)
    if fmt == "upperLetter":
        return chr(ord("A") + n - 1) if 1 <= n <= 26 else str(n)
    if fmt == "lowerRoman":
        return _roman(n).lower()
    if fmt == "upperRoman":
        return _roman(n)
    # 默认 decimal
    return str(n)


def _roman(n: int) -> str:
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    s = ""
    for v, sym in vals:
        while n >= v:
            s += sym
            n -= v
    return s


def parse_numbering(numbering_xml: bytes) -> dict:
    """Parse numbering.xml → return: numId → list of (ilvl, numFmt, lvlText, start)."""
    root = ET.fromstring(numbering_xml)
    # First parse abstractNum
    abs_map = {}  # abstractNumId → [(ilvl, fmt, lvlText, start), ...]
    for an in root.findall(f"{W}abstractNum"):
        aid = an.get(f"{W}abstractNumId")
        levels = []
        for lvl in an.findall(f"{W}lvl"):
            ilvl = int(lvl.get(f"{W}ilvl") or "0")
            fmt_el = lvl.find(f"{W}numFmt")
            fmt = fmt_el.get(f"{W}val") if fmt_el is not None else "decimal"
            txt_el = lvl.find(f"{W}lvlText")
            ltxt = txt_el.get(f"{W}val") if txt_el is not None else "%1."
            start_el = lvl.find(f"{W}start")
            start = int(start_el.get(f"{W}val")) if start_el is not None else 1
            levels.append((ilvl, fmt, ltxt, start))
        abs_map[aid] = levels
    # Then map numId → abstractNumId
    numid_map = {}  # numId → list-of-levels
    for n in root.findall(f"{W}num"):
        nid = n.get(f"{W}numId")
        abs_id_el = n.find(f"{W}abstractNumId")
        if abs_id_el is None:
            continue
        aid = abs_id_el.get(f"{W}val")
        if aid in abs_map:
            numid_map[nid] = abs_map[aid]
    return numid_map


def render_lvl_text(lvl_text: str, counters: dict[int, int], fmts: dict[int, str]) -> str:
    """Replace %1, %2, ... in lvlText with the current counter values, formatted."""
    def _sub(m):
        idx = int(m.group(1)) - 1  # %1 → ilvl 0
        val = counters.get(idx, 1)
        fmt = fmts.get(idx, "decimal")
        return format_num(val, fmt)
    return re.sub(r"%(\d)", _sub, lvl_text)


def get_para_text(p: ET.Element) -> str:
    """Extract all visible text from a paragraph element."""
    parts = []
    for t in p.iter(f"{W}t"):
        if t.text:
            parts.append(t.text)
    for dt in p.iter(f"{W}delText"):
        # tracked-change deletions are not displayed
        pass
    return "".join(parts)


def render_document(docx_path: str) -> list[dict]:
    """Return list of {idx, num_xml, num_rendered, text, raw_text, has_autonum}."""
    with zipfile.ZipFile(docx_path) as zf:
        try:
            numbering_xml = zf.read("word/numbering.xml")
        except KeyError:
            numbering_xml = b'<?xml version="1.0"?><w:numbering xmlns:w="' + NS["w"].encode() + b'"/>'
        document_xml = zf.read("word/document.xml")
    numid_map = parse_numbering(numbering_xml)

    root = ET.fromstring(document_xml)
    body = root.find(f"{W}body")
    if body is None:
        return []

    # Track counters per (numId, ilvl)
    counters_by_numid = defaultdict(dict)  # numId → {ilvl: int}
    results = []

    paragraphs = list(body.iter(f"{W}p"))
    for i, p in enumerate(paragraphs):
        text = get_para_text(p)
        ppr = p.find(f"{W}pPr")
        rendered_num = ""
        has_autonum = False
        autonum_meta = {}

        if ppr is not None:
            numpr = ppr.find(f"{W}numPr")
            if numpr is not None:
                numid_el = numpr.find(f"{W}numId")
                ilvl_el = numpr.find(f"{W}ilvl")
                if numid_el is not None:
                    numid = numid_el.get(f"{W}val")
                    ilvl = int(ilvl_el.get(f"{W}val")) if ilvl_el is not None else 0
                    if numid in numid_map:
                        has_autonum = True
                        autonum_meta = {"numId": numid, "ilvl": ilvl}
                        levels = numid_map[numid]
                        # increment counter at this level, reset deeper levels
                        ctr = counters_by_numid[numid]
                        ctr[ilvl] = ctr.get(ilvl, levels[ilvl][3] - 1) + 1
                        # reset deeper levels
                        for deeper in range(ilvl + 1, len(levels)):
                            if deeper in ctr:
                                del ctr[deeper]
                        # render lvlText at this ilvl
                        _, fmt, lvl_text, _ = levels[ilvl]
                        fmts = {lvl_info[0]: lvl_info[1] for lvl_info in levels}
                        rendered_num = render_lvl_text(lvl_text, ctr, fmts)

        results.append({
            "idx": i,
            "rendered_num": rendered_num,
            "text": text[:80],
            "raw_text": text,
            "has_autonum": has_autonum,
            "autonum_meta": autonum_meta,
        })

    return results


def print_summary(docx_path: str):
    rows = render_document(docx_path)
    print(f"{'Idx':>4} {'AutoNum':<25} {'Text':<80}")
    print("=" * 110)
    for r in rows:
        if not r["raw_text"].strip():
            continue
        anum = ""
        if r["has_autonum"]:
            meta = r["autonum_meta"]
            anum = f"[{r['rendered_num']}] (numId={meta['numId']} L{meta['ilvl']})"
        print(f"P{r['idx']:>3} {anum:<25} {r['text']}")


def print_para_detail(docx_path: str, idx: int):
    rows = render_document(docx_path)
    if idx < 0 or idx >= len(rows):
        print(f"P{idx} out of range (0..{len(rows)-1})")
        return
    r = rows[idx]
    print(f"=== Paragraph P{idx} ===")
    print(f"  Auto-numbered: {r['has_autonum']}")
    if r["has_autonum"]:
        print(f"  numId / ilvl: {r['autonum_meta']['numId']} / {r['autonum_meta']['ilvl']}")
        print(f"  Rendered number: {r['rendered_num']!r}")
    print(f"  Raw text in <w:t>: {r['raw_text']}")
    if r["has_autonum"]:
        print(f"  ==> Word renders this as: {r['rendered_num']}{r['raw_text']}")
    else:
        print(f"  ==> Word renders this as (text only): {r['raw_text']}")


def print_numbering_summary(docx_path: str):
    with zipfile.ZipFile(docx_path) as zf:
        try:
            nb = zf.read("word/numbering.xml")
        except KeyError:
            print("No numbering.xml in this docx.")
            return
    m = parse_numbering(nb)
    print(f"Found {len(m)} numbering definitions:")
    for nid, levels in sorted(m.items(), key=lambda x: int(x[0])):
        print(f"  numId={nid}:")
        for ilvl, fmt, ltxt, start in levels:
            print(f"    ilvl={ilvl}: numFmt={fmt}, lvlText={ltxt!r}, start={start}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("docx", help="path to .docx file")
    ap.add_argument("--para", type=int, help="show detail for a specific paragraph index")
    ap.add_argument("--numbering-summary", action="store_true", help="show numbering.xml definitions")
    args = ap.parse_args()

    if args.numbering_summary:
        print_numbering_summary(args.docx)
    elif args.para is not None:
        print_para_detail(args.docx, args.para)
    else:
        print_summary(args.docx)


if __name__ == "__main__":
    main()
