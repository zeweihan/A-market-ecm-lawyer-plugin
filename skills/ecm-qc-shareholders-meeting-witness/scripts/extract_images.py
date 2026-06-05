#!/usr/bin/env python3
"""
extract_images.py — 从 docx 抽取所有内嵌图片到临时目录。

用途：见证意见的 Logo / 页眉 / 签字页常含律所图片，需要让 AI 用视觉能力
逐张读图（特别是判断 Logo 是否含 "Mallesons" 字样）。

用法：
    python3 extract_images.py /path/to/file.docx
    python3 extract_images.py /path/to/file.docx --out /tmp/myimgs

输出：把 word/media/*.png / *.jpg / *.jpeg 等所有内嵌图片解压到目标目录，
并打印每张图片的路径 + 文件大小。后续可对每张图片调用 Read 视觉工具核查。
"""

from __future__ import annotations
import sys, os, zipfile, argparse, tempfile


def extract(docx_path: str, out_dir: str | None = None) -> list[str]:
    if out_dir is None:
        base = os.path.basename(docx_path).replace(".docx", "")
        out_dir = os.path.join(tempfile.gettempdir(), f"witness_imgs_{base}")
    os.makedirs(out_dir, exist_ok=True)

    paths = []
    with zipfile.ZipFile(docx_path) as zf:
        for name in zf.namelist():
            if not name.startswith("word/media/"):
                continue
            data = zf.read(name)
            fname = os.path.basename(name)
            out = os.path.join(out_dir, fname)
            with open(out, "wb") as f:
                f.write(data)
            paths.append(out)
    return paths


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("docx", help="path to .docx file")
    ap.add_argument("--out", help="output directory (default: temp)")
    args = ap.parse_args()

    paths = extract(args.docx, args.out)
    if not paths:
        print("(no embedded images found)")
        return
    print(f"Extracted {len(paths)} images to: {os.path.dirname(paths[0])}\n")
    for p in paths:
        size = os.path.getsize(p)
        print(f"  {p}  ({size:,} bytes)")
    print(f"\nNext: for each image above, call Read with the absolute path to view it visually.")
    print(f"Focus on header/footer images (often image1.png or image2.png).")
    print(f"Check whether any image contains 'Mallesons' text — if yes, write【必改】comment.")


if __name__ == "__main__":
    main()
