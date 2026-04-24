#!/usr/bin/env bash
#
# package-skill.sh — 把一个 skill 目录打包成 .skill 文件（zip 格式）
#
# 用法：
#   ./scripts/package-skill.sh skills/<skill-name>
#   ./scripts/package-skill.sh skills/<skill-name> --output custom/path
#
# 产出：
#   dist/<skill-name>.skill（默认）
#
# 说明：
#   .skill 文件就是 zip。顶层必须是一个与 skill 同名的目录（而不是 SKILL.md 直接在 zip 根部），
#   以便解压后是 <skill-name>/ 目录，和源码目录结构一致。

set -euo pipefail

usage() {
    cat <<EOF
用法: $0 <skill-dir> [--output <output-dir>]

参数:
  <skill-dir>          要打包的 skill 目录，例如 skills/ecm-qc-shareholders-meeting-witness
  --output <dir>       自定义输出目录（默认 dist/）

示例:
  $0 skills/ecm-qc-shareholders-meeting-witness
  $0 skills/listing-pathway-selection --output /tmp/release
EOF
}

if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

SKILL_DIR="$1"
shift

OUTPUT_DIR="dist"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "错误：未知参数 $1" >&2
            usage
            exit 1
            ;;
    esac
done

# ---------- 校验 ----------

if [[ ! -d "$SKILL_DIR" ]]; then
    echo "错误：$SKILL_DIR 不是目录" >&2
    exit 1
fi

SKILL_NAME="$(basename "$SKILL_DIR")"

if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
    echo "错误：$SKILL_DIR 下没有 SKILL.md" >&2
    exit 1
fi

# ---------- 打包 ----------

mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/${SKILL_NAME}.skill"

# 删掉旧的
rm -f "$OUTPUT_FILE"

# 切到 skill 的父目录，从父目录打包，这样 zip 内路径是 <skill-name>/...
PARENT_DIR="$(dirname "$SKILL_DIR")"
ABS_OUTPUT="$(cd "$(dirname "$OUTPUT_FILE")" && pwd)/$(basename "$OUTPUT_FILE")"

(
    cd "$PARENT_DIR"
    # 排除 macOS、编辑器、缓存文件
    zip -r "$ABS_OUTPUT" "$SKILL_NAME" \
        -x "*.DS_Store" \
        -x "*/__pycache__/*" \
        -x "*.pyc" \
        -x "*/.pytest_cache/*" \
        -x "*/node_modules/*" \
        -x "*.swp" \
        > /dev/null
)

# ---------- 输出摘要 ----------

SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
FILECOUNT=$(unzip -l "$OUTPUT_FILE" | tail -1 | awk '{print $2}')

echo "✓ 已打包：$OUTPUT_FILE"
echo "  大小：$SIZE"
echo "  文件数：$FILECOUNT"
echo ""
echo "测试解压："
echo "  unzip -l \"$OUTPUT_FILE\""
