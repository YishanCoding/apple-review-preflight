#!/bin/bash
# 用 Wayback Machine 对比 Apple Guidelines 最近两次快照
# 用法：bash check-guideline-updates.sh

set -euo pipefail

TARGET="https://developer.apple.com/cn/app-store/review/guidelines/"
export CDX_API="https://web.archive.org/cdx/search/cdx?url=${TARGET}&output=json&limit=-10&collapse=digest"

python3 << 'PY'
import json, re, html, urllib.request, sys, difflib, os

api = os.environ.get("CDX_API") or "https://web.archive.org/cdx/search/cdx?url=https://developer.apple.com/cn/app-store/review/guidelines/&output=json&limit=-10&collapse=digest"
target = "https://developer.apple.com/cn/app-store/review/guidelines/"

print(f"[1/3] Fetching CDX index: {api}")
rows = json.load(urllib.request.urlopen(api))
caps = rows[1:] if rows and rows[0][0] == "timestamp" else rows
if len(caps) < 2:
    sys.exit("需实测：Wayback 有效快照不足 2 个")

def fetch(ts):
    url = f"https://web.archive.org/web/{ts}id_/{target}"
    raw = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
    m = re.search(r"<main[\s\S]*?</main>", raw, re.I)
    body = m.group(0) if m else raw
    body = re.sub(r"<(script|style)[\s\S]*?</\1>", "", body, flags=re.I)
    text = re.sub(r"<[^>]+>", "\n", body)
    return re.sub(r"\n{2,}", "\n", html.unescape(text))

print("[2/3] Fetching last two snapshots...")
newer_ts, older_ts = caps[-1][0], caps[-2][0]
newer, older = fetch(newer_ts), fetch(older_ts)

print(f"[3/3] Diff {older_ts} -> {newer_ts}")
diff = list(difflib.unified_diff(older.splitlines(), newer.splitlines(),
                                   fromfile=older_ts, tofile=newer_ts, n=2))
if not diff:
    print("No changes between two latest snapshots.")
else:
    for line in diff[:200]:
        print(line)
PY
