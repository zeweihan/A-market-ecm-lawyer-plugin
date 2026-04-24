#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_folder.py — 批量审阅前的目录扫描工具

功能：
    列出目标目录下所有"可读文件"（支持的扩展名），按格式分布、大小、命名排序打印，
    作为 `ecm-dd:dd-file-review` 第 2 步"扫描目录清单"的快速工具。

用法：
    python skills/ecm-dd-file-review/scripts/scan_folder.py <folder>
    python skills/ecm-dd-file-review/scripts/scan_folder.py <folder> --recursive
    python skills/ecm-dd-file-review/scripts/scan_folder.py <folder> --json

输出：
    - 默认：可读的文本摘要（文件数、按扩展名分布、文件清单）
    - --json：供上层 Skill 解析的 JSON
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path

# 本 Skill 能调用外部 skill 读取的扩展名
READABLE_EXTS = {
    # pdf skill
    ".pdf",
    # docx skill
    ".docx",
    ".doc",
    # xlsx skill
    ".xlsx",
    ".xls",
    # 原生 Read
    ".txt",
    ".md",
    ".csv",
    ".rtf",
    # 图像（原生 Read + 视觉）
    ".png",
    ".jpg",
    ".jpeg",
    ".heic",
    ".gif",
    ".webp",
}

LARGE_FILE_MB = 10  # 超过这个大小建议拆分


@dataclass
class FileEntry:
    path: str
    size_bytes: int
    extension: str
    is_large: bool


def scan(folder: Path, recursive: bool) -> list[FileEntry]:
    entries: list[FileEntry] = []
    it = folder.rglob("*") if recursive else folder.iterdir()
    for p in it:
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext not in READABLE_EXTS:
            continue
        size = p.stat().st_size
        entries.append(
            FileEntry(
                path=str(p.relative_to(folder)),
                size_bytes=size,
                extension=ext,
                is_large=size > LARGE_FILE_MB * 1024 * 1024,
            )
        )
    return sorted(entries, key=lambda e: (e.extension, e.path))


def _print_human(entries: list[FileEntry], folder: Path) -> None:
    print(f"目录：{folder}")
    print(f"可读文件总数：{len(entries)}")
    if not entries:
        print("（空）")
        return

    counter = Counter(e.extension for e in entries)
    print("按扩展名分布：")
    for ext, count in counter.most_common():
        print(f"  {ext:<6} {count}")

    large = [e for e in entries if e.is_large]
    if large:
        print(f"\n大文件（>{LARGE_FILE_MB} MB，建议拆分处理）：")
        for e in sorted(large, key=lambda x: -x.size_bytes):
            print(f"  {e.size_bytes / 1024 / 1024:6.1f} MB  {e.path}")

    print("\n文件清单（按扩展名 → 路径）：")
    for e in entries:
        mark = " ⚠" if e.is_large else ""
        print(f"  {e.extension:<6} {e.path}{mark}")


def _print_json(entries: list[FileEntry], folder: Path) -> None:
    payload = {
        "folder": str(folder),
        "total": len(entries),
        "by_extension": dict(Counter(e.extension for e in entries)),
        "large_threshold_mb": LARGE_FILE_MB,
        "files": [asdict(e) for e in entries],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="扫描目录下的可读文件，为 ecm-dd-file-review 的批量审阅打底。",
    )
    p.add_argument("folder", help="目标目录路径")
    p.add_argument(
        "--recursive", "-r", action="store_true", help="递归扫描子目录"
    )
    p.add_argument(
        "--json", dest="as_json", action="store_true", help="输出 JSON 而非人读文本"
    )
    args = p.parse_args(argv)

    folder = Path(args.folder).expanduser().resolve()
    if not folder.exists():
        sys.stderr.write(f"错误：目录不存在 {folder}\n")
        return 2
    if not folder.is_dir():
        sys.stderr.write(f"错误：不是目录 {folder}\n")
        return 2

    entries = scan(folder, args.recursive)

    if args.as_json:
        _print_json(entries, folder)
    else:
        _print_human(entries, folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
