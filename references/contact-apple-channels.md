# 联系 Apple 全通道地图

> **读这个文件的场景**：需要就任何非标准流程问题联系 Apple（非常规 App Review 拒审处理，那个走 `../operations/review-ops.md`）。
> **最后验证时间**：2026-04

---

## 一、核心变化（2019 → 2025/2026）

2019 年时，开发者常用 `AppReview@apple.com`、`ChinaDev@asia.apple.com` 等邮箱直接联系 Apple。**2025 年这些邮箱均不再被 Apple 官方文档公开推荐**，Apple 已将开发者联系统一收敛至：

1. **developer.apple.com/contact/** — 通用开发者联系表单（需登录）
2. **App Store Connect → Resolution Center** — 审核相关沟通
3. **developer.apple.com/contact/app-store/** — App Review Board 申诉/加速审核专用
4. **apple.com/legal/intellectual-property/** — 知识产权争议专用

> ⚠️ 经验规则：部分旧邮箱可能仍然能收到自动回复或转发，但 Apple 不保证处理，且响应时间远慢于官方表单通道。

---

## 二、通道总表

| 类别 | 2025 推荐入口 | 旧入口（已不推荐） | 响应时效 | 中国大陆可访问 |
|------|-------------|------------------|---------|-------------|
| **App 审核申诉** | ASC Resolution Center + [Contact App Review](https://developer.apple.com/contact/app-store/) | AppReview@apple.com | 50% 在 24h 内，90% 在 48h 内 ✅ Apple 官方 | 是 |
| **加速审核** | [Expedited Review 表单](https://developer.apple.com/contact/app-store/?topic=expedite) | AppReview@apple.com | 批准后 4-12h ⚠️ 经验规则（2026 年因提交量激增波动大） | 是 |
| **App Review Board 上诉** | [Contact App Review](https://developer.apple.com/contact/app-store/) → 选 "appeal" | — | 24-72h 工作日 ⚠️ 经验规则 | 是 |
| **账号终止申诉** | [Contact App Review](https://developer.apple.com/contact/app-store/) → 选 "appeal an app rejection or app removal" | — | 数日至 30+ 日 ⚠️ 经验规则 | 是 |
| **账号恢复** | [Contact App Review](https://developer.apple.com/contact/app-store/) → 选 "Re-instate a Terminated Developer Program Membership" | — | 数周至数月 ⚠️ 经验规则 | 是 |
| **开发者计划 / 账号** | [Developer Contact](https://developer.apple.com/contact/) 表单 + [电话回拨](https://developer.apple.com/support/worldwide-telephone-hours/) | DevPrograms@apple.com | 表单 1-3 工作日 ⚠️ 经验规则；电话当天回拨 ✅ Apple 官方 | 是（中文普通话支持，工作日 09:00-17:00 CST） |
| **中国区开发者** | [Developer Contact](https://developer.apple.com/contact/)（支持中文） + 电话回拨 | ChinaDev@asia.apple.com / 4006 701 855 | 同上 | 是 |
| **知识产权 — 版权 (DMCA)** | [Copyright Infringement](https://www.apple.com/legal/contact/copyright-infringement.html) | — | 数周 ⚠️ 经验规则 | 是 |
| **知识产权 — 商标/内容** | [App Store Content Dispute](https://www.apple.com/legal/intellectual-property/dispute-forms/app-store/) | apple.com/legal/internet-services/itunes/appstorenotices/ | 数周 ⚠️ 经验规则 | 是 |
| **知识产权 — App 名称** | [App Name Dispute](https://www.apple.com/legal/internet-services/itunes/appnamenotices/) | — | 数周 ⚠️ 经验规则 | 是 |
| **支付 / 收款** | ASC → Agreements, Tax, and Banking + [Developer Contact](https://developer.apple.com/contact/) | iTSPayments@apple.com | 1-5 工作日 ⚠️ 经验规则 | 是 |
| **税收** | ASC → Agreements, Tax, and Banking + [Developer Contact](https://developer.apple.com/contact/) | iTSTax@apple.com | 1-5 工作日 ⚠️ 经验规则 | 是 |
| **报表 / 财务** | ASC → Sales and Trends / Payments and Financial Reports | iTunesAppReporting@apple.com | ASC 自助 | 是 |
| **技术支持 (TSI)** | [Technical Support](https://developer.apple.com/support/technical/)（每年 2 次代码级支持） | developer.apple.com/membercenter | 3 个工作日 ✅ Apple 官方 | 是 |
| **合同** | [Developer Contact](https://developer.apple.com/contact/) | DevContracts@apple.com | 1-5 工作日 ⚠️ 经验规则 | 是 |
| **EU DMA — 互操作** | [Interoperability Request](https://developer.apple.com/contact/request/interoperability/) | N/A | 未公开 | 不适用（仅 EU） |
| **EU DMA — 替代条款** | [Alternative EU Terms](https://developer.apple.com/contact/request/alternative-eu-terms-addendum/) | N/A | 未公开 | 不适用（仅 EU） |
| **EU DSA — 内容举报** | [ContentReports.apple.com](https://ContentReports.apple.com) | N/A | 未公开 | 不适用（仅 EU） |
| **举报问题 App** | [reportaproblem.apple.com](https://reportaproblem.apple.com) | — | 无 SLA | 是 |
| **精品推荐自荐** | ASC → [Featuring Nominations](https://developer.apple.com/help/app-store-connect/manage-featuring-nominations/nominate-your-app-for-featuring/) | AppStorePromotion@apple.com | 无回复承诺 | 是 |

---

## 三、Apple 电话回拨机制

Apple 不再公布直拨电话号码。当前模式：

1. 访问 [developer.apple.com/contact/](https://developer.apple.com/contact/)
2. 选择问题类型 → 填写表单
3. 选择「电话」联系方式 → Apple 在工作时间内回拨

**中国大陆电话支持时间**：周一至周五 09:00-17:00 CST，普通话服务。

> ⚠️ 经验规则：旧的 4006 701 855 号码在部分社区帖子中仍有提及，但 Apple 官方文档中未找到 2025 年的公开确认。建议通过网页表单预约回拨。

---

## 四、各场景的详细处理流程

| 场景 | 详细流程文件 |
|------|-----------|
| App 审核被拒/申诉 | `../operations/review-ops.md` |
| 账号警告/终止 | `../operations/account-warnings.md` |
| 加速审核 | `../operations/expedited-review.md` |
| 知识产权侵权 | `../operations/ip-infringement.md` |
| 差评处理/推广报备 | `../operations/review-manipulation.md` |
| 被下架/清榜/清词 | `../operations/app-penalty-recovery.md` |
| 精品推荐自荐 | `../operations/editorial-featuring.md` |

---

## 五、常见坑

1. **不要往旧邮箱发敏感信息**：即使邮箱仍能收件，Apple 不保证保密性和处理时效。
2. **电话回拨不适合审核申诉**：电话支持仅处理账号/技术问题，审核申诉必须走 Resolution Center 或 App Review Board 表单。
3. **EU 专用通道不适用于非 EU 开发者**：ContentReports、Interoperability Request 仅面向 EU/EEA 市场。
4. **TSI 不是万能通道**：每年 2 次的代码级技术支持不能用于审核申诉或业务咨询。

---

## 来源

| 来源 | URL | 验证时间 |
|------|-----|---------|
| Apple Developer Support | https://developer.apple.com/support/ | 2026-04 |
| Worldwide Telephone Hours | https://developer.apple.com/support/worldwide-telephone-hours/ | 2026-04 |
| Contact App Review | https://developer.apple.com/contact/app-store/ | 2026-04 |
| IP Dispute Forms | https://www.apple.com/legal/intellectual-property/dispute-forms/ | 2026-04 |
| Copyright Infringement | https://www.apple.com/legal/contact/copyright-infringement.html | 2026-04 |
| App Name Dispute | https://www.apple.com/legal/internet-services/itunes/appnamenotices/ | 2026-04 |
| DMA Support | https://developer.apple.com/support/dma-and-apps-in-the-eu/ | 2026-04 |
| TSI | https://developer.apple.com/support/technical/ | 2026-04 |
| ASC Featuring Nominations | https://developer.apple.com/help/app-store-connect/manage-featuring-nominations/ | 2026-04 |
| ContentReports (DSA) | https://ContentReports.apple.com | 2026-04 |
| Report a Problem | https://reportaproblem.apple.com | 2026-04 |
