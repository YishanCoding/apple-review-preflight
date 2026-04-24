#!/usr/bin/env bash
# check-live-sources.sh — Apple 官方 live 源校验（主路径）
#
# 用法：
#   bash policy/scripts/check-live-sources.sh
#
# 工作机制：
#   - 抓 4 个 live 源（CN/EN Guidelines + Upcoming Requirements + Apple News）
#   - 直连失败时 fallback 到 https://r.jina.ai/<url>（markdown proxy）
#   - 抽 main 区域文本，存到 policy/cache/<slug>.txt
#   - 与上次 cache 做 unified diff，输出变动
#   - 第一次跑只建立 baseline，无 diff 输出
#
# 与 check-guideline-updates.sh 的关系：
#   - 本脚本 = 主路径（live 源，新鲜度高，覆盖 EN/CN/News）
#   - check-guideline-updates.sh = 辅助/历史回溯（Wayback 快照，长周期趋势）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CACHE_DIR="$SKILL_ROOT/policy/cache"
mkdir -p "$CACHE_DIR"

# slug|url （slug 用于文件名）
SOURCES=(
  "guidelines-en|https://developer.apple.com/app-store/review/guidelines/"
  "guidelines-cn|https://developer.apple.com/cn/app-store/review/guidelines/"
  "upcoming-requirements|https://developer.apple.com/news/upcoming-requirements/"
  "apple-news|https://developer.apple.com/news/"
)

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

fetch_url() {
  # 写到 $2 指定的文件，避免大字符串经 subshell 捕获引发 SIGPIPE
  local url="$1"
  local out="$2"
  local rc
  # 优先直连
  curl -sSL -A "$UA" --max-time 30 -o "$out" "$url" 2>/dev/null
  rc=$?
  if [[ $rc -eq 0 && -s "$out" ]]; then
    return 0
  fi
  [[ -n "${DEBUG_FETCH:-}" ]] && echo "   [debug] direct curl rc=$rc size=$(stat -f%z "$out" 2>/dev/null || echo 0)" >&2
  # Jina markdown proxy fallback
  curl -sSL --max-time 60 -o "$out" "https://r.jina.ai/$url" 2>/dev/null
  rc=$?
  if [[ $rc -eq 0 && -s "$out" ]]; then
    return 0
  fi
  [[ -n "${DEBUG_FETCH:-}" ]] && echo "   [debug] jina curl rc=$rc size=$(stat -f%z "$out" 2>/dev/null || echo 0)" >&2
  return 1
}

extract_text() {
  # 注意：用 -c 而非 heredoc，否则 heredoc 占用 stdin，外部传入的 HTML 进不来
  python3 -c '
import sys, re, html
raw = sys.stdin.read()
m = re.search(r"<main[\s\S]*?</main>", raw, re.I)
body = m.group(0) if m else raw
body = re.sub(r"<(script|style|nav|footer|header)[\s\S]*?</\1>", "", body, flags=re.I)
text = re.sub(r"<[^>]+>", "\n", body)
text = html.unescape(text)
text = re.sub(r"\n[ \t]*\n+", "\n", text)
lines = [l.strip() for l in text.splitlines() if l.strip()]
print("\n".join(lines))
'
}

echo "=== Apple Live Source Check $(date '+%Y-%m-%d %H:%M:%S') ==="
echo ""

NEW_BASELINES=0
CHANGED=0
UNCHANGED=0
FETCH_FAILED=0

i=0
total=${#SOURCES[@]}
for entry in "${SOURCES[@]}"; do
  i=$((i + 1))
  slug="${entry%%|*}"
  url="${entry##*|}"
  cache="$CACHE_DIR/$slug.txt"
  prev="$CACHE_DIR/$slug.prev.txt"

  printf "[%d/%d] %-25s ... " "$i" "$total" "$slug"

  tmp_raw=$(mktemp)
  if ! fetch_url "$url" "$tmp_raw"; then
    rm -f "$tmp_raw"
    echo "❌ fetch failed (direct + r.jina.ai both failed)"
    FETCH_FAILED=$((FETCH_FAILED + 1))
    continue
  fi

  text=$(extract_text < "$tmp_raw")
  rm -f "$tmp_raw"

  if [[ -z "$text" ]]; then
    echo "⚠️ empty extracted text — page structure may have changed"
    FETCH_FAILED=$((FETCH_FAILED + 1))
    continue
  fi

  if [[ ! -f "$cache" ]]; then
    printf "%s" "$text" > "$cache"
    line_count=$(wc -l < "$cache" | tr -d ' ')
    echo "📌 baseline saved (${line_count} lines)"
    NEW_BASELINES=$((NEW_BASELINES + 1))
    continue
  fi

  mv "$cache" "$prev"
  printf "%s" "$text" > "$cache"

  if diff -q "$prev" "$cache" >/dev/null 2>&1; then
    echo "✅ no change"
    UNCHANGED=$((UNCHANGED + 1))
    rm -f "$prev"
    continue
  fi

  diff_count=$(diff "$prev" "$cache" 2>/dev/null | grep -c '^[<>]' || true)
  echo "🔔 changed (${diff_count} lines diff)"
  CHANGED=$((CHANGED + 1))

  echo ""
  echo "  --- diff preview (first 40 lines) ---"
  diff -u "$prev" "$cache" 2>/dev/null | head -40 | sed 's/^/  /' || true
  echo "  --- end diff ---"
  echo "  URL: $url"
  echo "  完整 diff: diff -u $prev $cache"
  echo ""
done

echo ""
echo "=== Summary ==="
echo "  Changed:   $CHANGED"
echo "  Unchanged: $UNCHANGED"
echo "  Baselined: $NEW_BASELINES (首次运行，下次起会报告变动)"
echo "  Failed:    $FETCH_FAILED"
echo ""
if [[ $CHANGED -gt 0 ]]; then
  echo "⚠️  发现变动 — 按 policy/update-playbook.md 流程更新对应 skill 文件。"
fi
echo "ℹ️  Wayback 历史趋势/长周期回溯：bash policy/scripts/check-guideline-updates.sh"
