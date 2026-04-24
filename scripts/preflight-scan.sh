#!/usr/bin/env bash
# preflight-scan.sh — Apple Review Preflight 项目扫描的 bash 包装
#
# 用法：
#   bash scripts/preflight-scan.sh [project_root] [--format markdown|json]
#   bash scripts/preflight-scan.sh                          # 扫当前目录，markdown
#   bash scripts/preflight-scan.sh ~/projects/MyApp         # 扫指定项目
#   bash scripts/preflight-scan.sh . --format json          # JSON 输出（agent 友好）
#
# 依赖：python3（macOS 自带）+ plutil（macOS 自带）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$SCRIPT_DIR/preflight-scan.py"

if [[ ! -f "$PY" ]]; then
  echo "找不到 preflight-scan.py（应在 $PY）" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "需要 python3（macOS 系统自带）" >&2
  exit 1
fi

if ! command -v plutil >/dev/null 2>&1; then
  echo "需要 plutil（macOS 系统自带，本脚本只支持 macOS）" >&2
  exit 1
fi

exec python3 "$PY" "$@"
