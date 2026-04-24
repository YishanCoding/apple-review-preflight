#!/usr/bin/env python3
"""
preflight-scan.py — Apple Review Preflight 项目扫描

用法：
    python3 preflight-scan.py [project_root] [--format markdown|json]

输出：项目栈识别 / Target 清单 / PrivacyInfo 覆盖率矩阵 / Info.plist 扫描 / 依赖风险

依赖：仅 Python 3.8+ stdlib + macOS 自带的 plutil
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


EXCLUDE_DIRS = {"node_modules", "Pods", "build", "DerivedData", ".git", "vendor", ".dart_tool"}

PRODUCT_TYPE_LABELS = {
    "com.apple.product-type.application": "App",
    "com.apple.product-type.app-extension": "Extension",
    "com.apple.product-type.application.watchapp": "WatchApp",
    "com.apple.product-type.application.watchapp2": "WatchApp",
    "com.apple.product-type.watchkit-extension": "WatchExtension",
    "com.apple.product-type.watchkit2-extension": "WatchExtension",
    "com.apple.product-type.app-extension.intents-service": "IntentsExtension",
    "com.apple.product-type.application.on-demand-install-capable": "AppClip",
    "com.apple.product-type.bundle.unit-test": "Test",
    "com.apple.product-type.bundle.ui-testing": "UITest",
    "com.apple.product-type.framework": "Framework",
    "com.apple.product-type.tv-app-extension": "TVExtension",
}

USAGE_DESCRIPTION_RE = re.compile(r"NS\w+UsageDescription$")

RISKY_DEP_KEYWORDS_NPM = [
    "purchase", "subscription", "auth", "analytics", "tracking",
    "firebase", "sentry", "revenuecat", "codepush", "stripe",
    "adjust", "appsflyer", "branch", "facebook", "google-signin",
]

RISKY_DEP_REGEX_PODFILE = re.compile(
    r"\b(Firebase|Facebook|Sentry|RevenueCat|Stripe|Adjust|AppsFlyer|CodePush|Branch|GoogleSignIn|FBSDK)\b",
    re.IGNORECASE,
)

RISKY_DEP_REGEX_PUBSPEC = re.compile(
    r"\b(in_app_purchase|firebase|sign_in_with_apple|adjust|appsflyer|sentry|stripe|revenue_cat)\b",
    re.IGNORECASE,
)


# ---------- 通用工具 ----------

def _excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def find_files(root: Path, names):
    out = []
    for p in root.rglob("*"):
        if _excluded(p):
            continue
        if p.is_file() and p.name in names:
            out.append(p)
    return out


def find_dirs(root: Path, suffixes):
    out = []
    for p in root.rglob("*"):
        if _excluded(p):
            continue
        if p.is_dir() and any(p.name.endswith(s) for s in suffixes):
            out.append(p)
    return out


def plutil_to_json(path: Path):
    """用 plutil 把 plist/pbxproj 转 JSON。失败返回 None。"""
    try:
        result = subprocess.run(
            ["plutil", "-convert", "json", "-o", "-", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass
    return None


def _read_package_deps(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
        return {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    except (json.JSONDecodeError, OSError):
        return {}


# ---------- 1. 栈识别 ----------

def detect_stack(root: Path) -> dict:
    pubspec = root / "pubspec.yaml"
    capacitor = list(root.glob("capacitor.config.*"))
    package_json = root / "package.json"
    xcodeprojs = [p for p in root.rglob("*.xcodeproj") if not _excluded(p)]
    package_swift = root / "Package.swift"

    if pubspec.exists():
        return {"stack": "flutter", "evidence": ["pubspec.yaml"]}
    if capacitor:
        return {"stack": "capacitor", "evidence": [c.name for c in capacitor]}
    if package_json.exists():
        deps = _read_package_deps(package_json)
        if any(k.startswith("expo") for k in deps):
            return {"stack": "expo", "evidence": ["package.json (expo)"]}
        if "react-native" in deps:
            return {"stack": "react-native", "evidence": ["package.json (react-native)"]}
    if xcodeprojs:
        return {
            "stack": "native-ios",
            "evidence": [str(p.relative_to(root)) for p in xcodeprojs[:3]],
        }
    if package_swift.exists():
        return {"stack": "swift-package", "evidence": ["Package.swift"]}
    return {"stack": "unknown", "evidence": []}


# ---------- 2. Target 探测 ----------

def find_targets(xcodeproj: Path, root: Path) -> list:
    pbx = xcodeproj / "project.pbxproj"
    if not pbx.exists():
        return []
    data = plutil_to_json(pbx)
    if not data:
        return []
    objects = data.get("objects", {})
    rel_xcodeproj = str(xcodeproj.relative_to(root))
    # 推断 platform（macos / ios / tvos / watchos / unknown）
    parts = [p.lower() for p in xcodeproj.relative_to(root).parts]
    platform = "unknown"
    for hint in ("ios", "macos", "tvos", "watchos", "visionos"):
        if hint in parts:
            platform = hint
            break
    targets = []
    for _id, obj in objects.items():
        isa = obj.get("isa")
        if isa not in ("PBXNativeTarget", "PBXAggregateTarget"):
            continue
        product_type = obj.get("productType", "")
        targets.append({
            "name": obj.get("name", ""),
            "type": PRODUCT_TYPE_LABELS.get(product_type, "Aggregate" if isa == "PBXAggregateTarget" else "Other"),
            "product_type": product_type,
            "is_test": "test" in product_type.lower(),
            "is_aggregate": isa == "PBXAggregateTarget",
            "xcodeproj": rel_xcodeproj,
            "platform": platform,
        })
    return targets


# ---------- 3. PrivacyInfo 覆盖率 ----------

def manifest_coverage(targets, manifests, root: Path) -> list:
    coverage = []
    for tgt in targets:
        if tgt["is_test"] or tgt["is_aggregate"]:
            continue
        if tgt["type"] in ("Framework",):
            continue
        name = tgt["name"]
        match, confidence = None, "low"
        for m in manifests:
            rel = str(m.relative_to(root))
            # 优先按平台目录匹配（避免 iOS Runner manifest 被算到 macOS Runner）
            if name and tgt["platform"] != "unknown" and tgt["platform"] in rel.lower() and name in rel:
                match, confidence = rel, "platform+name-match"
                break
            if name and name in rel:
                match, confidence = rel, "name-match"
        coverage.append({
            "target": name,
            "type": tgt["type"],
            "platform": tgt["platform"],
            "xcodeproj": tgt["xcodeproj"],
            "manifest": match,
            "confidence": confidence,
        })
    return coverage


# ---------- 4. Info.plist 扫描 ----------

def scan_info_plist(path: Path) -> dict:
    data = plutil_to_json(path)
    if not isinstance(data, dict):
        return {"path": str(path), "error": "parse failed"}
    out = {"path": str(path)}
    if "UIBackgroundModes" in data:
        out["UIBackgroundModes"] = data["UIBackgroundModes"]
    usage = {k: v for k, v in data.items() if USAGE_DESCRIPTION_RE.match(k)}
    if usage:
        out["UsageDescriptions"] = usage
    if "NSUserTrackingUsageDescription" in data:
        out["ATT_string"] = data["NSUserTrackingUsageDescription"]
    return out


# ---------- 5. 依赖风险扫描 ----------

def scan_npm_deps(path: Path) -> list:
    deps = _read_package_deps(path)
    return [
        f"{k}={v}" for k, v in deps.items()
        if any(kw in k.lower() for kw in RISKY_DEP_KEYWORDS_NPM)
    ]


def scan_podfile(path: Path) -> list:
    try:
        text = path.read_text()
    except OSError:
        return []
    return sorted(set(RISKY_DEP_REGEX_PODFILE.findall(text)))


def scan_pubspec(path: Path) -> list:
    try:
        text = path.read_text()
    except OSError:
        return []
    return sorted(set(RISKY_DEP_REGEX_PUBSPEC.findall(text)))


# ---------- 6. 输出 ----------

def render_markdown(r: dict) -> str:
    out = []
    out.append("# Apple Review Preflight Scan Report\n")
    out.append(f"**Project root**: `{r['root']}`")
    stack = r["stack"]
    out.append(f"**Stack**: `{stack['stack']}` ({', '.join(stack['evidence']) or 'no evidence'})\n")

    out.append("## Targets\n")
    if r["targets"]:
        out.append("| Target | Platform | Type | productType | xcodeproj |")
        out.append("|--------|----------|------|-------------|-----------|")
        for t in r["targets"]:
            out.append(
                f"| `{t['name']}` | {t['platform']} | {t['type']} | "
                f"`{t['product_type'] or '(aggregate)'}` | `{t['xcodeproj']}` |"
            )
    else:
        out.append("_(no .xcodeproj found or pbxproj not parseable)_")
    out.append("")

    out.append("## PrivacyInfo coverage\n")
    if r["coverage"]:
        out.append("| Target | Platform | Type | Manifest | Confidence |")
        out.append("|--------|----------|------|----------|------------|")
        for c in r["coverage"]:
            mark = c["manifest"] or "❌ **missing**"
            out.append(f"| `{c['target']}` | {c['platform']} | {c['type']} | {mark} | {c['confidence']} |")
        missing = [c for c in r["coverage"] if not c["manifest"]]
        if missing:
            out.append("")
            out.append(f"⚠️ **{len(missing)} Target 可能缺 PrivacyInfo.xcprivacy（ITMS-91053/91056 风险）**")
            out.append("提示：启发式按 Target 名匹配 manifest 路径，可能漏报。请人工核对每个 Extension Target 的 Build Phase 是否包含 PrivacyInfo.xcprivacy。")
    else:
        out.append("_(no Targets to check)_")
    out.append("")

    out.append("## All PrivacyInfo.xcprivacy files\n")
    if r["manifests"]:
        for m in r["manifests"]:
            out.append(f"- `{m}`")
    else:
        out.append("_(none found)_")
    out.append("")

    out.append("## Info.plist scan\n")
    if not r["info_plists"]:
        out.append("_(no Info.plist found)_")
    for p in r["info_plists"]:
        out.append(f"### `{p['path']}`")
        if p.get("error"):
            out.append(f"- _parse error: {p['error']}_")
        if p.get("UIBackgroundModes"):
            out.append(f"- **UIBackgroundModes**: {p['UIBackgroundModes']}")
        if p.get("UsageDescriptions"):
            for k, v in p["UsageDescriptions"].items():
                summary = (v or "").strip().replace("\n", " ")[:80]
                out.append(f"- **{k}**: \"{summary}\"")
        if p.get("ATT_string"):
            out.append(f"- **ATT**: \"{p['ATT_string'][:80]}\"")
        out.append("")

    out.append("## Risky dependencies\n")
    deps = r["dependencies"]
    if deps["npm"]:
        out.append("**npm/yarn:**")
        for d in deps["npm"]:
            out.append(f"- {d}")
        out.append("")
    if deps["podfile"]:
        out.append("**Podfile:**")
        for d in deps["podfile"]:
            out.append(f"- {d}")
        out.append("")
    if deps["pubspec"]:
        out.append("**pubspec.yaml:**")
        for d in deps["pubspec"]:
            out.append(f"- {d}")
        out.append("")
    if not any(deps.values()):
        out.append("_(no risky dependencies detected)_")
    out.append("")

    out.append("## Warnings\n")
    if r["warnings"]:
        for w in r["warnings"]:
            out.append(f"- ⚠️ {w}")
    else:
        out.append("_(none)_")

    return "\n".join(out)


# ---------- main ----------

def scan(root: Path) -> dict:
    stack = detect_stack(root)
    xcodeprojs = find_dirs(root, [".xcodeproj"])

    targets = []
    for xp in xcodeprojs:
        targets.extend(find_targets(xp, root))

    info_plists = find_files(root, ["Info.plist"])
    info_plist_data = [scan_info_plist(p) for p in info_plists]

    manifests = find_files(root, ["PrivacyInfo.xcprivacy"])
    manifest_paths = sorted(str(m.relative_to(root)) for m in manifests)

    coverage = manifest_coverage(targets, manifests, root)

    deps = {"npm": [], "podfile": [], "pubspec": []}
    for pj in find_files(root, ["package.json"])[:5]:
        deps["npm"].extend(scan_npm_deps(pj))
    for pf in find_files(root, ["Podfile"]):
        deps["podfile"].extend(scan_podfile(pf))
    for ps in find_files(root, ["pubspec.yaml"]):
        deps["pubspec"].extend(scan_pubspec(ps))
    for k in deps:
        deps[k] = sorted(set(deps[k]))

    warnings = []
    for c in coverage:
        if not c["manifest"]:
            warnings.append(
                f"`{c['target']}` ({c['type']}) 可能缺 PrivacyInfo.xcprivacy "
                f"(启发匹配未命中) — 请人工核实（ITMS-91053/91056）"
            )
    for ip in info_plist_data:
        bgm = ip.get("UIBackgroundModes") or []
        if "audio" in bgm:
            warnings.append(f"`{ip['path']}` 声明 audio 后台模式 — 需在 review notes 说明实际用途")
        if "fetch" in bgm and "voip" in bgm:
            warnings.append(f"`{ip['path']}` 同时声明 fetch + voip — 高风险组合")
    if not manifests and stack["stack"] != "unknown":
        warnings.append(
            "全项目未找到任何 PrivacyInfo.xcprivacy — 自 2024-05 起强制要求，"
            "ASC 上传阶段会被自动拦截"
        )

    return {
        "root": str(root),
        "stack": stack,
        "targets": targets,
        "info_plists": info_plist_data,
        "manifests": manifest_paths,
        "coverage": coverage,
        "dependencies": deps,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description="Apple Review Preflight 项目扫描")
    parser.add_argument("root", nargs="?", default=".", help="项目根目录（默认当前目录）")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        sys.exit(f"路径不存在：{root}")

    report = scan(root)

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))


if __name__ == "__main__":
    main()
