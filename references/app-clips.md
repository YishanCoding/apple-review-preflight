# App Clips 审核合规指南
> App Clip 范围 / 尺寸 / 隐私 / IAP 限制 + Guideline 2.5.16 / 5.1.1 拒审处理
> 适用于所有带 App Clip Target 的 iOS App（iOS 14+；iOS 16+ 15 MB / iOS 17+ 50 MB）

---

## 一、App Clip 是什么

App Clip 是 App 的**轻量子集**（Swift/Objective-C 编译的独立 Bundle，与主 App 共享代码和资源），用户无需安装完整 App 即可通过 NFC、QR、Safari Smart Banner、iMessage、Maps 等方式**秒开**使用。

### 1.1 核心特性

| 特性 | 说明 |
|------|------|
| 启动速度 | Sub-second launch（冷启到可交互 < 1s）|
| 生命周期 | 使用后约 8 小时未再次调用，系统自动清除 |
| UI 容器 | App Clip Card（全屏卡片，含 Icon/Title/Subtitle/Open 按钮）|
| 升级路径 | 内置"Get the Full App"按钮（`SKOverlay.AppClipConfiguration`）|
| 与主 App 关系 | 同一 Bundle ID 下的 Target，共享代码但有独立 Entitlements |

### 1.2 Size Limit（2026 年现行）

⚠️ Apple 历史上多次调整上限，以 Xcode 打包时 App Store Connect 的校验为准：

| iOS 版本 | 上限 | 测量方式 |
|---------|------|---------|
| iOS 14–15 | **10 MB** | Uncompressed, thinned variant |
| iOS 16+ | **15 MB** | Uncompressed, thinned variant |
| iOS 17+ | **50 MB** | 仅限 digital invocation（QR/Safari/iMessage/Maps）；physical invocation（NFC/App Clip Code）仍按 15 MB |
| iOS 26 | ⚠️ 以 WWDC25/Xcode 26 Release Notes 为准（预期延续 50 MB / 15 MB 分层）|

**校验方法**：Archive 后，Xcode Organizer → Validate App → 错误信息会直接报 `exceeds the maximum allowable size of X MB after app thinning`。

### 1.3 调用方式（Invocation）

- **Physical**：NFC Tag、App Clip Code（Apple 专有视觉码）、第三方 QR
- **Digital**：Safari Smart App Banner、iMessage 链接、Maps 地点卡、Siri Suggestions、Apple Pay 相关触发

---

## 二、范围限制（Guideline 2.5.16(a)）

App Clip 必须解决**单一聚焦任务**，且与真实世界或网页上下文绑定。审核员会据此判断 Clip 是否合理。

### 2.1 允许 ✅

- 咖啡店扫码点单 → 立即下单
- 共享单车 NFC 解锁 → 开锁骑行
- 停车位 QR 扫码 → 缴费离场
- 餐厅扫码 → 查看菜单 + 点餐 + Apple Pay 结账
- 博物馆展品 NFC → 查看单件展品信息

### 2.2 禁止 ⚠️

- **推广 full App**：把 Clip 当"试玩广告"，首屏就是"下载完整 App 以解锁全部功能"
- **通用任务**：Clip 里有"登录""设置""个人资料""好友列表"等与当前场景无关的入口
- **Teaser 内容**：只展示 1 张图 + Download 按钮，没有实际功能闭环
- **无真实世界锚点**：纯粹靠 App Store 分享链接分发，没有 NFC/QR/Maps 上下文

### 2.3 单一任务原则

| 判定 | 例子 |
|------|------|
| ✅ 单一 | "扫这张桌子的 QR → 在本桌点餐" |
| ❌ 多任务 | "扫 QR → 进入商家主页（含点餐、会员、活动、外卖、客服）" |

---

## 三、元数据一致性（2.3.x 系列）

### 3.1 App Clip Card

| 字段 | 要求 |
|------|------|
| Title | 与 Clip 实际功能一致；不得出现 full App 的品牌 tagline |
| Subtitle | 描述本次可完成的动作（如"Pay for parking at Lot A"）|
| Icon | 可与 full App 图标不同；需与 subtitle 语境吻合 |
| Header Image | 1800×1200，不得含"Download the App""Free Trial"等 CTA |
| Action Verb | Open / View / Play / Order / Pay 等系统预设动词 |

### 3.2 App Clip Experience URL

在 ASC → App Clip → Advanced App Clip Experiences 中配置：

- 每个 Experience 对应一个 URL（如 `https://coffee.example.com/store/123`）
- URL 必须由 Associated Domains（`appclips:` prefix）声明
- URL 真实可访问（审核员会点击）；返回 404 直接拒

```xml
<!-- App Clip target 的 Entitlements -->
<key>com.apple.developer.associated-domains</key>
<array>
    <string>appclips:coffee.example.com</string>
</array>
```

### 3.3 Smart App Banner 与 App Clip 共存

在网页 `<head>` 中：

```html
<!-- 触发 App Clip（iOS 14+），未安装 full App 时优先 Clip -->
<meta name="apple-itunes-app"
      content="app-id=123456789, app-clip-bundle-id=com.example.coffee.Clip">
```

⚠️ `app-id` 与 `app-clip-bundle-id` 必须属于同一 App Record；不一致会被 2.3.1 拒。

---

## 四、隐私（2.5.16 + 5.1.1）

App Clip 的隐私要求**比 full App 更严**：Apple 期望 Clip 只收集完成当前任务所必需的最小数据。

### 4.1 不可做的事

| 行为 | 原因 |
|------|------|
| 调用 ATT（`ATTrackingManager.requestTrackingAuthorization`）| 系统直接阻断；Clip 不允许 tracking |
| 弹窗登录后才能用 | 违反 "focused task" 原则；除 Sign in with Apple 外不得强制注册 |
| 集成三方广告 SDK | 几乎一定触发 tracking 代码路径，拒审 |
| 大规模 Analytics | 可做匿名 crash/性能（无用户 ID），但禁止跨会话行为画像 |

### 4.2 可做的事 ✅

- **Sign in with Apple**：Clip 中允许的唯一完整登录方式（且必须是可选）
- **Apple Pay**：直接可用，无需登录
- **一次性信息采集**：完成当前订单所必需的配送地址等（不得持久化到 Clip 外）
- **匿名 Crash 报告**：不含 user ID 的诊断数据

### 4.3 Privacy Manifest 覆盖 Clip Target

⚠️ App Clip 是独立 Bundle，**必须有独立 `PrivacyInfo.xcprivacy`**：

- 放在 App Clip Target 的资源中（Target Membership 勾选 Clip Target）
- Required Reason API 规则同 full App（见 [`./privacy-manifest.md`](./privacy-manifest.md)）
- `NSPrivacyCollectedDataTypes` 应只列 Clip 实际收集的字段（通常远少于 full App）
- `NSPrivacyTracking` 必须为 `false`

常见遗漏：`UserDefaults`（CA92.1）、`SystemBootTime`（35F9.1）——Clip 也会用，必须声明。

---

## 五、IAP（Guideline 3.1）

App Clip 中的 IAP **受限**：

| 类型 | Clip 中是否允许 |
|------|----------------|
| Consumable（消耗型） | ✅ 允许（如一次性订单增值服务）|
| Non-Consumable（永久） | ⚠️ 技术上允许但 Apple 不鼓励，因 Clip 生命周期短 |
| Auto-Renewable Subscription | ❌ 禁止在 Clip 中销售 / 推广订阅 |
| Non-Renewing Subscription | ❌ 禁止 |

### 5.1 Apple Pay（推荐）

App Clip 中销售**实体商品/服务**（咖啡、停车、共享单车）必须用 **Apple Pay**，不得用 IAP（这是 Guideline 3.1.3(e) "Goods and Services Outside of the App" 的反向应用）。

```swift
// Clip 中触发 Apple Pay
let request = PKPaymentRequest()
request.merchantIdentifier = "merchant.com.example.coffee"
request.supportedNetworks = [.visa, .masterCard, .amex]
request.merchantCapabilities = .threeDSecure
// ...
```

### 5.2 订阅升级路径

想推广订阅 → 使用 `SKOverlay.AppClipConfiguration` 引导用户下载 full App 后在 full App 内购买。Clip 内**不得**展示订阅价格/条款。

详见 [`./storekit-iap.md`](./storekit-iap.md) 第七节。

---

## 六、代码结构与运行限制

App Clip runtime 被系统严格沙盒：

| 能力 | Clip 可用性 |
|------|------------|
| Background Modes（audio/location/BLE 常驻）| ❌ 不允许 |
| Remote Push Notification | ❌ 完全禁止 |
| Local Push | ⚠️ 仅 "ephemeral" 通知（Clip 活跃期内 8 小时窗口，系统限制）|
| UIBackgroundTasks | ❌ |
| HealthKit | ❌ |
| CallKit | ❌ |
| File System（沙盒外） | ❌ 仅 `NSTemporaryDirectory()` 可写，Clip 终止后即清 |
| UserDefaults 与 full App 共享 | ⚠️ 需 App Group Entitlement + 同一 Team ID；不自动共享 |
| Keychain 与 full App 共享 | ⚠️ 需 Keychain Sharing Entitlement |
| ARKit / Camera / Location | ✅ 允许（需 Info.plist usage description） |
| CoreNFC（NDEF 读取）| ✅ 允许（NFC 调用 Clip 本身即需要）|

### 6.1 App Group 共享示例

```swift
// Clip 和 full App 共享 UserDefaults（需配置 App Group entitlement）
let shared = UserDefaults(suiteName: "group.com.example.coffee")
shared?.set(orderID, forKey: "lastClipOrderID")
// full App 启动后读取并衔接体验
```

Privacy Manifest 需声明 `1C8F.1`（App Group UserDefaults）而非 `CA92.1`。

---

## 七、Review Notes 模板

App Clip 审核最常见问题是审核员**找不到调用入口**。必须在 Review Notes 明确说明：

```
APP CLIP REVIEW NOTES

Invocation URL (for testing in Safari):
  https://coffee.example.com/store/DEMO123

How to test the App Clip:
1. Open Safari on iPhone (iOS 16+).
2. Paste the URL above. Safari will show an App Clip banner at top.
3. Tap "Open" — the App Clip Card will appear.
4. Tap "Open" on the card to launch the clip.

Alternative invocation methods we support:
- NFC tag: we cannot ship a physical tag, but the URL above
  is identical to the NDEF payload on our production tags.
- App Clip Code: attached as "appclip_code_demo.png" in the
  review attachments.

Expected flow:
1. Clip loads store #DEMO123 menu
2. User taps "Order Latte ($5)"
3. Apple Pay sheet appears; use Sandbox card
4. Order confirmation screen within the clip

No login required. No IAP inside the clip.
Full App upsell is shown via SKOverlay after order success (optional).
```

---

## 八、常见拒审

| # | 场景 | Guideline | 修复 |
|---|------|-----------|------|
| 1 | Clip 内包含完整 App 的 Tab Bar / 多模块导航 | 2.5.16(a) | 精简为单一任务闭环 |
| 2 | Clip 没有 NFC/QR/Maps 等真实世界锚点，仅靠 App Store 分享链接 | 2.5.16(a) | 配置 Advanced App Clip Experience + Associated Domains |
| 3 | `PrivacyInfo.xcprivacy` 只在 full App Target，Clip Target 缺失 | 5.1.1 / ITMS-91053 | 为 Clip Target 单独添加 manifest |
| 4 | 进入 Clip 立即要求注册账号 / 手机号登录 | 2.5.16(a) + 5.1.1(v) | 改为匿名可用；如必要使用 Sign in with Apple |
| 5 | Smart App Banner 中 `app-clip-bundle-id` 与 App Record 不匹配 | 2.3.1 | 修正 meta tag 或 ASC 配置 |
| 6 | Clip 打包 > 15 MB（physical invocation 场景） | 2.5.16(a)（size policy）| Strip 资源、拆 On-Demand Resources、用 full App 承载大功能 |
| 7 | Clip 内销售 Auto-Renewable Subscription | 3.1.2 | 移除订阅 UI，改为引导下载 full App |
| 8 | Clip 调用 `ATTrackingManager` 或集成广告 SDK | 2.5.16 + 5.1.1 | 移除 tracking 代码与 SDK；确认 `NSPrivacyTracking=false` |

---

## 九、提交前 Checklist

- [ ] **2.5.16(a)** Clip 只解决单一任务，无多模块导航
- [ ] **2.5.16(a)** 至少一个真实世界 / 网页调用锚点（NFC / QR / Smart Banner / Maps）
- [ ] **2.5.16(a)** Clip 大小在目标 iOS 版本上限内（15 MB / 50 MB）
- [ ] **2.3.1** App Clip Card 的 Title/Subtitle/Icon/Header Image 与实际功能一致
- [ ] **2.3.1** `apple-itunes-app` meta 中 `app-id` 与 `app-clip-bundle-id` 匹配
- [ ] **2.5.16** 未调用 ATT；未集成广告 SDK；`NSPrivacyTracking=false`
- [ ] **2.5.16** 未强制注册；Sign in with Apple 为可选
- [ ] **5.1.1** Clip Target 有独立 `PrivacyInfo.xcprivacy`，Required Reason API 已声明
- [ ] **3.1.3(e)** 实体商品/服务用 Apple Pay，不用 IAP
- [ ] **3.1.2** Clip 内不销售订阅
- [ ] **Entitlements** Associated Domains（`appclips:`）已配置且域名可访问
- [ ] **Review Notes** 提供测试 URL + NFC/QR payload 说明
- [ ] **Testing** Archive → Validate 通过，无 size 超限警告
- [ ] **App Group / Keychain** 跨 Clip ↔ full App 数据共享场景已用对应 Entitlement

相关文档：
- [`./privacy-manifest.md`](./privacy-manifest.md) — Clip Target 的 Required Reason API 声明
- [`./storekit-iap.md`](./storekit-iap.md) — IAP 规则与 Apple Pay 边界
- [`../by-app-type/all-apps.md`](../by-app-type/all-apps.md) — 通用审核红线

---

## 十、关键来源

- Apple Developer — [App Clips Overview](https://developer.apple.com/app-clips/)
- Apple Developer — [Creating an App Clip with Xcode](https://developer.apple.com/documentation/appclip/creating-an-app-clip-with-xcode)
- Apple Developer — [Choosing the Right Functionality for Your App Clip](https://developer.apple.com/documentation/appclip/choosing-the-right-functionality-for-your-app-clip)
- Apple Developer — [Responding to Invocations](https://developer.apple.com/documentation/appclip/responding-to-invocations)
- Apple Developer — [App Clip Experiences in App Store Connect](https://developer.apple.com/help/app-store-connect/configure-app-clip-experiences/)
- App Review Guidelines — [2.5.16 App Clips](https://developer.apple.com/app-store/review/guidelines/#app-clips) / [5.1.1 Data Collection and Storage](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage)
- WWDC22 — [What's new in App Clips](https://developer.apple.com/videos/play/wwdc2022/10097/)（15 MB 上限引入）
- WWDC23 — [What's new in App Clips](https://developer.apple.com/videos/play/wwdc2023/10178/)（iOS 17 数字调用 50 MB）
- ⚠️ iOS 26 的 size 上限以 Xcode 26 Release Notes / App Store Connect 实际校验错误为准
