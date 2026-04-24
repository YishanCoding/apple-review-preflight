# Source Map — 本 Skill 文件与 Apple 官方来源映射

> 列出本 skill 每个文件对应的 Apple 官方来源 URL，便于验证内容准确性和追踪更新。
> 格式：skill 文件 → 引用的 Apple 条款/文档 → 官方 URL

---

## SKILL.md（主入口）

| 引用内容 | Apple 来源 |
|---------|-----------|
| TOP 10 拒审原因 | [App Store Review Guidelines](https://developer.apple.com/cn/app-store/review/guidelines/) 综合 |
| 2026 年关键新规 | [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) |
| 预检流程 | 本 skill 整合设计 |

---

## guidelines/

| 文件 | 对应条款 | Apple 来源 URL |
|------|---------|---------------|
| `core-guidelines-map.md` | 全部条款概览 | [Guidelines 全文](https://developer.apple.com/cn/app-store/review/guidelines/) |
| `3-business.md` | 3.1–3.2 | [Guidelines §3](https://developer.apple.com/cn/app-store/review/guidelines/#business) |

---

## checks/

| 文件 | 对应条款 | Apple 来源 URL |
|------|---------|---------------|
| `review-failure-map.md` | 多条款（Top 拒审原因） | [Guidelines 全文](https://developer.apple.com/cn/app-store/review/guidelines/) |
| `background-modes-scan.md` | 2.5.4 | [Guidelines §2.5.4](https://developer.apple.com/cn/app-store/review/guidelines/#software-requirements) |
| `code-scan-patterns.md` | 2.5.1 / 2.5.2 / 3.1 / 4.8 / 5.1 | [Guidelines 多条款](https://developer.apple.com/cn/app-store/review/guidelines/) |
| `privacy-transparency-consistency.md` | 5.1.1 / 5.1.2 | [Guidelines §5.1](https://developer.apple.com/cn/app-store/review/guidelines/#data-collection-and-storage) |
| `report-template.md` | — | 本 skill 模板设计 |
| `required-reason-api-scan.md` | 5.1.1 | [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api) |

---

## references/

| 文件 | 对应条款 | Apple 来源 URL |
|------|---------|---------------|
| `privacy-manifest.md` | 5.1.1 | [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files) |
| `storekit-iap.md` | 3.1.1 | [StoreKit](https://developer.apple.com/documentation/storekit) / [In-App Purchase](https://developer.apple.com/in-app-purchase/) |
| `sign-in-with-apple.md` | 4.8 | [Sign in with Apple](https://developer.apple.com/sign-in-with-apple/) / [Guidelines §4.8](https://developer.apple.com/cn/app-store/review/guidelines/#sign-in-with-apple) |
| `store-metadata-compliance.md` | 2.3 / 2.3.7 | [Guidelines §2.3](https://developer.apple.com/cn/app-store/review/guidelines/#metadata) / [ASC Help](https://developer.apple.com/help/app-store-connect/manage-app-information/) |
| `new-os-api-compliance.md` | — | [Upcoming SDK requirements](https://developer.apple.com/news/?id=ueeok6yw) / [Xcode Release Notes](https://developer.apple.com/documentation/xcode-release-notes) |
| `medical-device-status.md` | 1.4 | [ASC: Declare medical device status](https://developer.apple.com/help/app-store-connect/manage-app-information/declare-regulated-medical-device-status) / [Apple News](https://developer.apple.com/news/?id=nyqbfz1y) |
| `contact-apple-channels.md` | — | [Developer Support](https://developer.apple.com/support/) / [Worldwide Telephone Hours](https://developer.apple.com/support/worldwide-telephone-hours/) / [Contact App Review](https://developer.apple.com/contact/app-store/) / [IP Dispute Forms](https://www.apple.com/legal/intellectual-property/dispute-forms/) / [DMA Support](https://developer.apple.com/support/dma-and-apps-in-the-eu/) |
| `app-clips.md` | 2.5.16(a) / 5.1.1 | [App Clips](https://developer.apple.com/app-clips/) / [WWDC23: What's new in App Clips](https://developer.apple.com/videos/play/wwdc2023/10178/) / [WWDC22: What's new in App Clips](https://developer.apple.com/videos/play/wwdc2022/10097/) |
| `push-notifications.md` | 4.5.4 / 5.1.1 | [User Notifications](https://developer.apple.com/documentation/usernotifications) / [APNs Overview](https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server) / [Critical Alerts Entitlement](https://developer.apple.com/contact/request/notifications-critical-alerts-entitlement/) |
| `widgets-live-activity.md` | 4.2 / 2.3.x / 5.1.1 | [WidgetKit](https://developer.apple.com/documentation/widgetkit) / [ActivityKit](https://developer.apple.com/documentation/activitykit) / [WWDC23: Update Live Activities](https://developer.apple.com/videos/play/wwdc2023/10185/) / [HIG: Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities) |

---

## operations/

| 文件 | 对应条款 | Apple 来源 URL |
|------|---------|---------------|
| `cicd-upload.md` | — | [Xcode Cloud](https://developer.apple.com/xcode-cloud/) / [altool/Transporter](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds) |
| `phased-release-strategy.md` | — | [ASC Help: Phased Release](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases) |
| `review-ops.md` | 全部 | [App Review](https://developer.apple.com/distribute/app-review/) / [Resolution Center](https://developer.apple.com/help/app-store-connect/manage-submissions/reply-to-app-review-messages) |
| `account-warnings.md` | 3.2(f) / ADP §3.2 | [Contact App Review](https://developer.apple.com/contact/app-store/) / [ADP License Agreement](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/) |
| `expedited-review.md` | — | [Expedited Review](https://developer.apple.com/contact/app-store/?topic=expedite) / [App Review](https://developer.apple.com/distribute/app-review/) |
| `ip-infringement.md` | 2.3.7 | [IP Dispute Forms](https://www.apple.com/legal/intellectual-property/dispute-forms/app-store/) / [Copyright Infringement](https://www.apple.com/legal/contact/copyright-infringement.html) / [App Name Dispute](https://www.apple.com/legal/internet-services/itunes/appnamenotices/) |
| `review-manipulation.md` | 5.6 / 3.2.2(vi) | [Apple Newsroom Fraud Prevention](https://www.apple.com/newsroom/2025/05/the-app-store-prevented-more-than-9-billion-usd-in-fraudulent-transactions/) / [ContentReports (DSA)](https://ContentReports.apple.com) |
| `app-penalty-recovery.md` | 4.3 / 5.6 | [Guidelines](https://developer.apple.com/cn/app-store/review/guidelines/) / [Contact App Review](https://developer.apple.com/contact/app-store/) |
| `editorial-featuring.md` | — | [Getting Featured](https://developer.apple.com/app-store/getting-featured/) / [ASC Featuring Nominations](https://developer.apple.com/help/app-store-connect/manage-featuring-nominations/nominate-your-app-for-featuring/) |
| `testflight-external-review.md` | 2.1 / 2.2 | [TestFlight](https://developer.apple.com/testflight/) / [ASC: Invite external testers](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers/) / [ASC: Submit a Beta App Review](https://developer.apple.com/help/app-store-connect/test-a-beta-version/submit-for-beta-app-review/) |
| `eu-dma-alternatives.md` | 3.1 / EU DMA / Alternative Terms Addendum / Notarization Review Guidelines | [Apple: DMA and apps in the EU](https://developer.apple.com/support/dma-and-apps-in-the-eu/) / [Apple EU updates](https://developer.apple.com/news/?id=awedznci) / [MarketplaceKit](https://developer.apple.com/documentation/marketplacekit) / [Notarization Review Guidelines for iOS and iPadOS apps](https://developer.apple.com/support/notarization-review-guidelines-for-ios-and-ipados-apps/) / [ExternalPurchaseLink](https://developer.apple.com/documentation/storekit/externalpurchaselink) |

---

## by-app-type/

| 文件 | 对应条款 | Apple 来源 URL |
|------|---------|---------------|
| `all-apps.md` | 通用 | [Guidelines 全文](https://developer.apple.com/cn/app-store/review/guidelines/) |
| `subscription.md` | 3.1.2 | [Auto-Renewable Subscriptions](https://developer.apple.com/app-store/subscriptions/) |
| `ai-apps.md` | 1.1 / 1.2 / 5.1（AI 输出安全、UGC、隐私） | [Guidelines §1.1](https://developer.apple.com/cn/app-store/review/guidelines/#objectionable-content) / [§1.2](https://developer.apple.com/cn/app-store/review/guidelines/#user-generated-content) / [§5.1](https://developer.apple.com/cn/app-store/review/guidelines/#data-collection-and-storage) |
| `ugc-social.md` | 1.2 | [Guidelines §1.2](https://developer.apple.com/cn/app-store/review/guidelines/#user-generated-content) |
| `games.md` | 4.2.7 / 3.1.1 | [Guidelines §4.2.7](https://developer.apple.com/cn/app-store/review/guidelines/#minimum-functionality) |
| `ecommerce.md` | 3.1.3(e) | [Guidelines §3.1.3(e)](https://developer.apple.com/cn/app-store/review/guidelines/#in-app-purchase) |
| `kids.md` | 1.3 | [Guidelines §1.3](https://developer.apple.com/cn/app-store/review/guidelines/#kids-category) |
| `health-fitness.md` | 1.4 / 5.1.3 | [Guidelines §1.4](https://developer.apple.com/cn/app-store/review/guidelines/#physical-harm) / [HealthKit](https://developer.apple.com/documentation/healthkit) |
| `mac-macos.md` | — | [Mac Catalyst](https://developer.apple.com/mac-catalyst/) / [Guidelines macOS 部分](https://developer.apple.com/cn/app-store/review/guidelines/) |
| `watchos.md` | — | [watchOS HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos) |
| `tvos.md` | — | [tvOS HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos) |
| `crypto-finance.md` | 3.1.5(i)-(v) | [Guidelines §3.1.5](https://developer.apple.com/cn/app-store/review/guidelines/#in-app-purchase) |
| `vpn.md` | 5.4 | [Guidelines §5.4](https://developer.apple.com/cn/app-store/review/guidelines/#vpn-apps) |
| `visionos.md` | — | [visionOS](https://developer.apple.com/visionos/) / [HIG Spatial](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos) |
| `dating.md` | 1.2 / 1.4 / 4.8 / Age Rating 元数据（1.1.4 仅限色情/hookup 内容） | [Guidelines §1.2](https://developer.apple.com/cn/app-store/review/guidelines/#user-generated-content) / [Guidelines §1.4](https://developer.apple.com/cn/app-store/review/guidelines/#physical-harm) / [DeclaredAgeRange API](https://developer.apple.com/documentation/declaredagerange) / [Apple: Age assurance](https://developer.apple.com/support/age-assurance/) |

---

## market-overrides/

| 文件 | 对应政策 | 来源 URL |
|------|---------|---------|
| `china.md` | ICP 备案 / PIPL / 版号 | [工信部 App 备案](https://www.miit.gov.cn/) / Apple Guidelines 中国区要求 |
| `eu-eea.md` | DMA / GDPR / ePrivacy | [Apple EU Updates](https://developer.apple.com/news/?id=awedznci) / [DMA](https://digital-markets-act.ec.europa.eu/) |
| `us.md` | COPPA / CCPA / 外部支付 | [StoreKit External Purchase](https://developer.apple.com/documentation/storekit/external-purchase-link) / [FTC COPPA](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa) |
| `uk.md` | Online Safety Act / UKGC / MHRA / UK GDPR / iOS 26.4 年龄验证 | [Apple DeclaredAgeRange](https://developer.apple.com/documentation/declaredagerange) / [Ofcom OSA](https://www.ofcom.org.uk/online-safety/) / [UKGC Licensing](https://www.gamblingcommission.gov.uk/) / [MHRA Medical Device Software](https://www.gov.uk/government/publications/medical-devices-software-applications-apps) / [ICO](https://ico.org.uk/) |

---

## policy/

| 文件 | 用途 | 来源 |
|------|------|------|
| `policy-updates-log.md` | Guidelines 变动时间线 | 综合 Apple News + Upcoming Requirements |
| `source-map.md`（本文件）| 文件↔来源映射 | — |
| `update-playbook.md` | 更新流程手册 | — |
| `policy/scripts/check-live-sources.sh` | live Apple 官方源校验（CN/EN Guidelines + Upcoming Requirements + Apple News） | [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) / [App Store Review Guidelines CN](https://developer.apple.com/cn/app-store/review/guidelines/) / [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) / [Apple Developer News](https://developer.apple.com/news/) |
| `scripts/check-guideline-updates.sh` | Wayback Machine 快照对比 | [Wayback CDX API](https://web.archive.org/) |

---

## scripts/

| 文件 | 用途 | 来源 |
|------|------|------|
| `scripts/preflight-scan.sh` | Bash 包装器：调度结构化项目扫描 | 本 skill 执行辅助脚本（基于仓库结构约定） |
| `scripts/preflight-scan.py` | 通用项目结构探测，输出 target / plist / manifest / 依赖信号 | 本 skill 执行辅助脚本（基于仓库结构约定） |

---

## 维护说明

- 新增文件时同步在此添加映射
- 定期检查 URL 是否仍然有效
- Apple 官网 URL 结构变动时及时更新
