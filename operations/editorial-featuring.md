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

> ⚠️ 以下节日时间基于 2023-2026 美区 Today 页实测数据（51,256 条）反推，比 Apple 官方"至少3周"更精确。

| 时机 | Nomination 提交截止 | In-App Event 提交截止 | 实测曝光窗口 |
|------|-------------------|--------------------|------------|
| **情人节（2/14）** | **1/1 前** | 1/1 前 | 最早提前 9 天（2024）；2025 年仅提前 1-2 天 |
| **母亲节（5/12）** | **4/1 前** | 4/1 前 | 礼品类仅当天进入集合，无提前几周曝光 |
| **感恩节（11/28）** | **10/15 前** | 10/15 前 | OUR FAVORITES 从提前 4 天开始，持续至当天 |
| **黑色星期五（11/29）** | **10/15 前** | 10/15 前 | 当天上线，编辑准备早 |
| **圣诞节（12/25）** | **11/1 前** | 11/1 前 | 最早提前 20 天；礼品类集中在最后 1 周 |
| **新 App 首发** | 1-3 个月前 | — | 越早越好，给编辑充分评估时间 |
| **重大版本更新** | 5-6 周前 | 4-6 周前 | Apple 官方说"至少3周"，实测建议留更多余量 |
| **新 OS 发布** | Beta 期间（6-8月） | — | WWDC 后立即提交，展示对新 OS 特性的支持 |

**关键认知**：不要因为"节日还有一个月"就觉得来得及——页面曝光往往只在节日前最后 1-4 天密集出现，但苹果审核 + 排期需要 4-8 周。**母亲节尤其危险**：礼品类 App 只在当天被推，4 月底才提交的申请几乎无效。

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

---

## 八、推荐生态趋势：从量大到精选叙事

> 数据来源：点点数据（diandian.com），美区，2023-01-01 ~ 2026-04-20，共 51,256 条记录。

### 8.1 Today 页记录数的断崖式下滑

| 年份 | Today 页记录数 | 主导推荐位 | 核心特征 |
|------|--------------|-----------|---------|
| 2023 | 14,279 | ESSENTIALS / COLLECTION | 大批量榜单式分发，位多量大 |
| 2024 | 9,987 | ESSENTIALS + NOW TRENDING | 开始向主题化收缩 |
| 2025 | 3,862 | OUR FAVORITES / APP OF THE DAY | 精简，叙事驱动 |
| 2026 YTD | 585 | APP OF THE DAY / NOW TRENDING | 少位、强主题、每位都有观点 |

**年度降幅 95.9%，但这不是苹果推荐意愿下降，而是范式改变**：`ESSENTIALS` 可以容纳 10-20 个 App 的列表位，从 2023 年的 310 天出现频率到 2025 年后基本退出，取而代之的是需要独立成篇的主题编辑位。

竞争从"挤进大名单"，变成了"说服一个编辑为什么今天必须推你"。

### 8.2 各推荐位年度频次

| 推荐位 | 2023 | 2024 | 2025 | 2026 YTD | 趋势 |
|--------|------|------|------|----------|------|
| ESSENTIALS | 310 天 | 315 天 | 70 天 | 0 | ⬇ 基本退出 |
| OUR FAVORITES | 106 天 | 58 天 | 129 天 | 25 天 | ↗ 主力主题位 |
| NOW TRENDING | 75 天 | 127 天 | 58 天 | 21 天 | ↔ 节日/热点型 |
| FROM THE EDITORS | 11 天 | 25 天 | 17 天 | 1 天 | → 稀缺高规格 |
| APP OF THE DAY | 334 天 | 309 天 | 327 天 | 102 天 | ✓ 最稳定骨架 |
| GAME OF THE DAY | 349 天 | 313 天 | 346 天 | 104 天 | ✓ 最稳定骨架 |
| TRY SOMETHING NEW | 51 天 | 31 天 | 81 天 | 6 天 | ↗ 新体验导向 |
| WORLD PREMIERE | 27 天 | 92 天 | 40 天 | 18 天 | → 首发/独家 |

### 8.3 推荐位三层结构

| 层级 | 代表推荐位 | 申请逻辑 | 适用阶段 |
|------|-----------|---------|---------|
| **日更核心位** | APP OF THE DAY / GAME OF THE DAY | 单 App 强叙事，门槛最高 | 长期目标，先建立编辑认知 |
| **主题编辑位** | OUR FAVORITES / NOW TRENDING / FROM THE EDITORS | 节日/热点/文化场景，有明确时间窗口 | **Today 页最现实突破口** |
| **持久发现位** | Editors' Choice Apps / Apps You Might've Missed / Best New Apps | 长周期陈列，适合持续经营 | **第一阶段重点** |

---

## 九、礼品/情感类 App 的推荐规律（数据实证）

### 9.1 已验证样本

| App | Today 页 | App 页 | 主要出现形式 | 核心叙事 |
|-----|---------|--------|------------|---------|
| **Givingli** | 28 条 | 18 条 | APP OF THE DAY + NOW TRENDING + Editors' Choice | 礼品卡数字化，情感表达工具 |
| **Chatbooks** | 5 条 | 12 条 | APP OF THE DAY + NOW TRENDING + Editors' Choice | 家庭照片 → 照片书，回忆整理 |
| **Shutterfly** | 3 条 | 0 | APP OF THE DAY + NOW TRENDING | 照片打印与礼品化结合 |
| **1800Flowers** | 6 条 | 0 | APP OF THE DAY + NOW TRENDING | 节日鲜花，强节日爆发型 |
| **Etsy** | 6 条 | 12 条 | NOW TRENDING + ESSENTIALS + Great Apps Updated for iOS 26 | 手工礼品 + 平台更新能力 |
| **Mixtiles** | 1 条 | 0 | NOW TRENDING | 照片墙贴，纪念物场景 |

### 9.2 三条稳定规律

**规律一：双通路，不是单点爆发。**
Givingli、Chatbooks 既有 Today 页的节日爆发，也有 Editors' Choice Apps 的长期陈列。只靠节日冲一次的策略缺少长期编辑认知积累。

**规律二：苹果不推"购物工具"，推"情感变实体"的产品。**
这些 App 的共性：情感表达 + 个性化纪念 + 照片/回忆为核心。产品叙事关键词：personalized / keepsake / memory / meaningful gifting，而非 SKU 丰富或折扣力度。

**规律三：礼品类可以拿到 APP OF THE DAY。**（⚠️ 常见误判）
Givingli、Chatbooks、Shutterfly 都有 AOTD 记录。"礼品类不能做 AOTD"是错误的——关键是产品叙事和体验完成度。

### 9.3 Givingli 的完整成长路径（可复现案例）

| 时间 | 推荐位 | 意义 |
|------|--------|------|
| 2023-01 ~ 06 | Editors' Choice Apps（6次，约每2周一次）| **第一阶段**：ECA 积累编辑信任 |
| **2023-06-18** | **APP OF THE DAY（首次）** | 距首次 ECA 仅 153 天；**触发时机：父亲节前 2 天** |
| **2023-11-24** | **APP OF THE DAY（第 2 次）** | **触发时机：感恩节前 1 天** |
| 2024-05-12 | NOW TRENDING "Find Gifts for Mom"（#6 位）| 母亲节当天进入集合 |
| 2025-02-10~14 | OUR FAVORITES + NOW TRENDING（3天连续）| 情人节集合排名 **#1** |
| 2025-03-21 | APP OF THE DAY（第 3 次）| 非节日期间，品牌认知驱动 |
| 2025-09 起 | Editors' Choice Apps（每 14 天，持续至今）| **第二阶段**：进入固定轮换 |
| **2025-12-22** | **APP OF THE DAY（第 5 次）** | **触发时机：圣诞节前 3 天** |

**结论**：ECA 是 AOTD 的前置跑道。数据中 89 个有 ECA 积累的 App 后来都拿到了 AOTD，中位数积累周期 **342 天**，Givingli 的 153 天已属快速通道。礼品类 AOTD 几乎全部绑定节日窗口（父亲节/感恩节/圣诞节前）。

### 9.4 母亲节集合的竞争格局（2024 年实测，20 个 App）

2024-05-12 "Find Gifts for Mom" 共 20 个 App，礼品/照片纪念类占 10 个（50%）：

| 排名 | App | 品类 |
|------|-----|------|
| #1 | 1800Flowers | 鲜花/传统礼品 |
| #2~4 | Resy / OpenTable / Fandango | 餐厅/电影体验型礼物 |
| #5 | Chatbooks | 家庭照片书 |
| #6 | Givingli | 礼品卡+情感表达 |
| #7 | Once Upon | 照片书创作 |
| #9 | Keepsake Frames | 数字相框 |
| #15 | Handwrytten | AI 手写风格卡片 |
| #16 | Shutterfly | 照片打印+礼品 |
| #17 | Ink Cards | 定制卡片邮寄 |
| #20 | Mixtiles | 照片墙贴 |

情人节集合（2025）更精英：只有 6 个 App，Givingli 排第 1，其余 5 个是大零售商（Target/Nordstrom/Macy's/Anthropologie/Etsy）。小型创意工具要进入情人节精英圈，"个性化/创意/情感表达"是区分大零售商的核心维度。

---

## 十、Editors' Choice Apps（ECA）机制

### 10.1 轮换规律

- **轮换周期**：约 14 天一轮，每次展示约 8-12 个 App，分批替换而非全部刷新
- **进入 ECA 不是永久的**：Givingli 曾有 840 天空窗（2023-06 到 2025-09），很可能对应产品迭代期或编辑关系断档——进入 ECA 后需要每隔 6-8 周有产品层面的更新来维持编辑兴趣

### 10.2 进入 ECA 的三条路径（数据推断）

| 路径 | 特征 | 适用场景 |
|------|------|---------|
| **新 App 突破型** | 新上架 + 强设计 + 苹果平台优先功能 | 首发时冲击 |
| **节日季乘势型** | 在 NOW TRENDING 节日集合首次曝光，之后进入轮换 | 节日申请为跳板 |
| **版本大更新型** | 大版本 + iOS 新能力，以 Best New Apps 为跳板进入 ECA | 最普适的路径 |

"版本大更新型"最现实：将一次重要版本更新包装为 nomination，争取进入 "Best New Apps and Updates"，再以此为跳板申请 ECA。

---

## 十一、APP OF THE DAY 的语言模式

数据中 47 条 AOTD editorial_desc 揭示的编辑语言习惯：

**格式公式**：`[情感动词] + [核心体验] + [与用户的连接]`

| 类型 | 样本 | 占比 |
|------|------|------|
| 情感动词开头 | "Feel Transported With Soundscapes" / "Find Your Groove With djay" / "Bring the Night Sky to Life" | 72%（34/47）|
| 名词/描述开头 | "Customized Soundscapes for You" | 28% |

**常用动词**：Feel / Find / Bring / Make / Get / Try / Watch / Play / Learn

**语言特征**：
- 5-7 个词，极短
- 不描述功能，直接描述用户情感体验
- 动词有画面感（"Bring to Life" 而非 "See"）
- 结尾常以 "With + App名" 或 "for You" 收束

**申请时建议在 tagline 字段同时准备 2-3 个版本，给编辑选择空间。**

---

## 十二、申请前置条件检查

在提交 Nomination 之前，以下条件必须就绪——否则申报了大概率无效：

| 前置条件 | 说明 | 优先级 |
|---------|------|--------|
| **生成/核心体验质量稳定** | 核心功能 90%+ 达可交付标准，无明显瑕疵 | ⭐ 必须 |
| **交付链路完整** | 全流程顺滑，承诺可落地 | ⭐ 必须 |
| **评分健康** | App Store 评分 ≥ 4.5，评价数量符合品类基线 | ⭐ 必须 |
| **视觉资产就绪** | 截图/Preview 视频已更新，清晰展示核心体验 | 建议 |
| **版本有亮点** | 近 30 天有新功能或体验大改，而非仅修 bug | 建议 |
| **In-App Event 方案** | 活动有明确 CTA、功能变化、时间窗口 | 建议 |
| **申请材料就绪** | 主叙事、产品亮点、节日版文案、演示视频 | 建议 |

> 原则：前三项（体验质量 + 交付 + 评分）都就绪，再进入申请流程才有意义。

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
