# 精品推荐自荐 (Editorial Featuring & Self-Nomination)

> **读这个文件的场景**：App 即将首发、重大更新、或配合节日/新 OS 发布，希望获得 App Store 编辑推荐（Today Tab / 精品推荐 / App of the Day）。
> **核心变化**：2024 年起，Apple 废弃了 `AppStorePromotion@apple.com` 邮箱，改为 App Store Connect 内置的 **Featuring Nominations** 表单。
> **最后验证时间**：2026-04

---

## 一、当前官方入口（2025/2026）

| 项目 | 详情 |
|------|------|
| **推荐入口** | App Store Connect → Apps → [你的 App] → Featuring → Nominations ✅ Apple 官方 |
| **官方指南** | [Getting Featured on the App Store](https://developer.apple.com/app-store/getting-featured/) |
| **ASC 帮助文档** | [Nominate your app for featuring](https://developer.apple.com/help/app-store-connect/manage-featuring-nominations/nominate-your-app-for-featuring/) |
| **WWDC 介绍** | [What's new in App Store Connect (WWDC 2024)](https://developer.apple.com/videos/play/wwdc2024/10063/) |
| **旧邮箱** | `AppStorePromotion@apple.com` — 不再是推荐渠道 |
| **旧网页** | developer.apple.com/app-store/discoverability/ — 仍存在但内容已转向搜索/发现机制，不再是自荐入口 |

---

## 二、ASC Featuring Nominations 提交流程

### Step 1：选择提名类型

| 类型 | 适用场景 |
|------|---------|
| **New Content** | 新增应用内内容、活动、限时优惠。 |
| **App Enhancements** | 新功能、重大更新、性能优化。 |
| **App Launch** | 新 App 首发或预购。 |

### Step 2：填写必填字段

| 字段 | 说明 |
|------|------|
| Nomination Name | 内部标识名（Apple 编辑可见）。 |
| Description | 描述你的 App 为什么值得推荐（What / Why / Priority）。 |
| Publish Date | 预计上线/更新日期。 |

### Step 3：填写推荐字段（强烈建议）

| 字段 | 说明 |
|------|------|
| Related Apps | 最多 10 个关联 App（如果你有系列产品或想建议专题）。 |
| Platforms | iOS / iPadOS / macOS / tvOS / watchOS / visionOS。 |
| Countries/Regions | 目标市场。 |
| Localizations | 多语言描述。 |
| In-App Events | 关联 ASC 中已创建的 In-App Event。 |
| Supplemental URLs | 最多 5 个（TestFlight 链接、设计文档、视频 Demo、媒体报道）。 |
| Helpful Details | 无障碍特性、团队故事、社会影响等加分信息。 |

> 支持 CSV 批量导入，适合多 App 同时提名。

---

## 三、提交时间策略

| 时机 | 建议提前量 | 说明 |
|------|----------|------|
| **新 App 首发** | 1-3 个月 | 越早越好，给编辑充分评估时间。 |
| **重大更新** | 3 周以上 | Apple 官方建议至少 3 周。 |
| **新 OS 发布** | Beta 期间（6-8月） | 在 WWDC 后立即提交，展示对新 OS 特性的支持。 |
| **节日/活动** | 3-4 周 | 圣诞/春节/万圣节等，Apple 会提前策划专题。 |
| **被推荐过的 App** | 每次重大更新时 | 有推荐历史的 App 再次被推荐的概率更高（⚠️ 经验规则）。 |

---

## 四、加分项 — 什么样的 App 更容易被推荐

✅ Apple 官方评估维度（来自 [Getting Featured](https://developer.apple.com/app-store/getting-featured/)）：

| 维度 | 具体要求 |
|------|---------|
| **用户体验** | 流畅、直觉、无 bug。 |
| **UI 设计** | 遵循 Human Interface Guidelines，视觉精良。 |
| **创新性** | 独特的功能或解决问题的方式。 |
| **无障碍** | 支持 VoiceOver、Dynamic Type、色彩对比度。 |
| **本地化** | 多语言支持，尤其是目标市场的本地化质量。 |
| **新平台特性** | 支持最新 iOS/macOS 特性（如 iOS 26 Liquid Glass、AI Tags）。 |
| **App Store 产品页** | 高质量截图、App Preview 视频、完整描述。 |

**游戏额外维度**：玩法设计、美术/动画、操控手感、剧情、重玩性、音效、技术性能。

---

## 五、自荐内容模板

### ASC Nomination Description（英文）

```
[App Name] is a [category] app that [one-sentence value proposition].

**What's New:**
We are launching [feature/update/content] on [Date], which [describe the 
user benefit].

**Why Feature-Worthy:**
1. [Highlight 1: e.g., "First app to integrate iOS 26 Liquid Glass design 
   language throughout the entire UI."]
2. [Highlight 2: e.g., "Full VoiceOver and Dynamic Type support, making 
   [service] accessible to visually impaired users."]
3. [Highlight 3: e.g., "Localized in 12 languages with culturally adapted 
   content for each market."]

**Traction:**
- [Number] active users across [Number] countries
- [Rating] average rating with [Number] reviews
- [Any press coverage or awards]

**Supplemental Materials:**
- TestFlight: [Link]
- Video Demo: [Link]
- Press Kit: [Link]
```

### ASC Nomination Description（中文，用于中国区本地化字段）

```
[App 名称] 是一款 [类别] 应用，[一句话价值主张]。

**本次更新亮点：**
我们将于 [日期] 发布 [功能/内容]，为用户带来 [具体价值]。

**推荐理由：**
1. [亮点 1：如 "全面适配 iOS 26 Liquid Glass 设计语言"]
2. [亮点 2：如 "完整支持 VoiceOver 和动态字体"]
3. [亮点 3：如 "已本地化 12 种语言"]

**产品数据：**
- [数量] 活跃用户，覆盖 [数量] 个国家/地区
- 平均评分 [分数]，[数量] 条评价
- [媒体报道/获奖情况]
```

---

## 六、App Store Awards 与 Today Tab

| 项目 | 是否可自荐 | 说明 |
|------|----------|------|
| **Today Tab 故事** | 间接 | 无单独提交表单。通过 Featuring Nomination 提供引人注目的故事角度和素材，可能吸引编辑关注。 |
| **App of the Year / Game of the Year** | 否 | Apple 编辑团队内部评选，无公开提名入口。2025 年评选了 45 个入围者，覆盖 12 个类别。 |
| **WWDC Design Awards** | 否 | Apple 内部评选。 |

---

## 七、关于联系 Apple 编辑

> ⚠️ 经验规则：通过 LinkedIn 搜索 Apple 编辑并私信联系，在 2019 年前是常见做法。2025 年这种方式**不被 Apple 官方推荐**，且效果不确定。

**官方接触编辑的机会**：
- **WWDC 现场活动**：WWDC 2026（6 月 8-12 日）包含线下环节，部分开发者可参加 1-on-1 Labs，间接接触 Apple 团队。
- **Apple Entrepreneur Camp**：面向特定群体的开发者加速计划，包含与 Apple 团队的直接互动。

---

## 来源

| 来源 | URL | 验证时间 |
|------|-----|---------|
| Getting Featured | https://developer.apple.com/app-store/getting-featured/ | 2026-04 |
| ASC Featuring Nominations | https://developer.apple.com/help/app-store-connect/manage-featuring-nominations/nominate-your-app-for-featuring/ | 2026-04 |
| WWDC 2024 ASC Updates | https://developer.apple.com/videos/play/wwdc2024/10063/ | 2026-04 |
| WWDC 2025 ASC Updates | https://developer.apple.com/videos/play/wwdc2025/328/ | 2026-04 |
| Discovery on the App Store | https://developer.apple.com/app-store/discoverability/ | 2026-04 |
| 2025 App Store Awards | https://www.apple.com/newsroom/2025/11/apple-announces-finalists-for-the-2025-app-store-awards/ | 2026-04 |
