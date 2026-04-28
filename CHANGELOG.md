# Changelog

## [1.2.0] - 2026-04-28

### Added
- `operations/review-timing.md` — new: review timing patterns and optimal submission windows. Covers Apple official 24h SLA, Runway 2026 weekly/monthly data, timezone-based submission timing (Beijing 00:00–04:00 = Cupertino 09:00 PDT), holiday peak delays (official Apple announcements for Dec 20–26 confirmed multi-year), app-type review time differences, status signal interpretation (Waiting for Review vs In Review), and Meet with App Review scheduling

### Changed
- `SKILL.md` routing tables: added "审核时长 / 提交时机 / 高峰期" → `operations/review-timing.md` in both task and contact-scenario sections
- `README.md` Coverage table: updated Operations row to include review timing

## [1.1.0] - 2026-04-24

### Added
- `scripts/preflight-scan.{py,sh}` — structure-aware preflight discovery for `Info.plist`, `PrivacyInfo.xcprivacy`, targets, manifests, entitlements, and dependency signals
- `policy/scripts/check-live-sources.sh` — live Apple source tracking for Guidelines EN/CN, Upcoming Requirements, and Apple News
- `docs/feature-map.svg` and `docs/feature-map-zh.svg` — updated README diagrams reflecting the new workflow

### Changed
- `SKILL.md` Step 1 now routes through `scripts/preflight-scan.sh` instead of assuming a fixed iOS path
- `SKILL.md` now defines a minimum output contract: `Scope / Findings / Missing Inputs / Evidence / Final Recommendation`
- `by-app-type/all-apps.md` now treats Privacy Manifest coverage as target-level, including App Clips / Widgets / Extensions
- `README.md` now positions policy tracking accurately as live-source review plus Wayback-assisted diff
- `README.md` installation notes for Codex/OpenClaw now clarify scanned skill roots instead of implying a universal default
- `policy/update-playbook.md` now uses repo-root execution and treats Wayback as a helper rather than the sole freshness source
- `guidelines/core-guidelines-map.md` and `checks/review-failure-map.md` now reference Apple's public rating prompt API wording more precisely

## [1.0.0] - 2026-04-17

### Added
- Initial public release
- `SKILL.md` — main entry point with 5-step preflight flow and TOP 10 rejection reasons
- `by-app-type/` — 14 app-type specific checklists (subscription, AI, games, health, kids, dating, ecommerce, crypto, VPN, UGC, macOS, tvOS, watchOS, visionOS)
- `checks/` — automated scan guides (privacy, Required Reason APIs, background modes, code patterns, metadata)
- `guidelines/` — core Apple guidelines reference (IAP/business, guidelines map)
- `market-overrides/` — regional compliance for China, EU/EEA, UK, US
- `operations/` — 11 operational guides (rejections, appeals, expedited review, account warnings, IP infringement, editorial featuring, phased release, CI/CD, TestFlight, EU DMA, review manipulation)
- `policy/` — policy tracking system with automated update detection script
- `references/` — 10 technical reference guides (privacy manifest, StoreKit/IAP, Sign in with Apple, metadata, new OS requirements, medical devices, contact channels, app clips, push notifications, widgets)

### Coverage
- Based on Apple's 2026 review data
- Aligned with App Store Review Guidelines last updated 2026-02-06
- Includes 2026 key requirement: iOS/iPadOS 26 SDK deadline (2026-04-28)
