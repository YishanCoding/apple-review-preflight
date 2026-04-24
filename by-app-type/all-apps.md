# All Apps — 提交前必读通用清单

> 本文件是所有 App 提交前的**基础通关清单**。
> 加载专项类型文件之前，先完整过一遍本文件。
> 每一项均标注「为什么重要」，帮助判断紧急程度。

---

## 1. 隐私与账号

### 1.1 隐私政策 ✦ 高频第一拒审原因

- [ ] `App Store Connect → App Information → Privacy Policy URL` 已填写
- [ ] 链接在审核期间真实可访问（非 404、非登录墙、非 localhost）
- [ ] 内容与 App 实际收集的数据类型匹配（数据类型改变要同步更新政策）
- [ ] 支持中文展示（在中国大陆发布时）

**为什么重要**：Apple 会人工点击这个链接。链接 404 是 5.1.1(i) 直接拒审，不给申诉缓冲。

### 1.2 账号删除

- [ ] 设置页有「删除账号」入口，功能真实生效（非「停用」或「注销申请」）
- [ ] 删除后：用户生成内容、个人数据在合规周期后实际删除
- [ ] Apple 指引链接：[Offering Account Deletion](https://developer.apple.com/support/offering-account-deletion-in-your-app/)

**为什么重要**：5.1.1(v) 自 2022 年起强制执行，但至今仍是高频拒审。审核员直接在设置里找这个入口。

### 1.3 游客浏览（Guest Browse）

- [ ] 非账号相关内容（商品列表、文章、首页）无需登录即可访问
- [ ] 只在以下场景才触发登录：购买、发布内容、保存收藏等账号操作

**为什么重要**：5.1.1(v) 明确禁止"强制注册才能浏览公开内容"。审核员第一步就是不登录试用 App。

### 1.4 ATT（App Tracking Transparency）

- [ ] 只有在实际进行跨 App/跨网站 tracking 时才弹 ATT
- [ ] ATT 弹窗必须在任何 tracking SDK 初始化之前出现
- [ ] `NSUserTrackingUsageDescription` 描述清晰，说明用途

**为什么重要**：5.1.2(i)。错误时序（先 tracking 后弹窗）被 Apple 用自动化工具检测，拒审率极高。

### 1.5 PrivacyInfo.xcprivacy

- [ ] 主 App Target 包含 `PrivacyInfo.xcprivacy` 文件
- [ ] **每个 Extension Target 各自独立 manifest**（Widget / Live Activity / App Clip / Share Extension / Notification Service Extension）—— 主 App 有 manifest ≠ 全部 Target 都有，是 ITMS-91053/91056 的高频拒审点
- [ ] 所有 Required Reason API 均已声明（UserDefaults、文件时间戳、磁盘空间、Core Data 等）
- [ ] 第三方 SDK 的隐私清单也已合并（CocoaPods/SPM 依赖需各自有 PrivacyInfo）
- [ ] 详细扫描流程：`../checks/required-reason-api-scan.md`
- [ ] App Clip 专项：`../references/app-clips.md`
- [ ] Widget / Live Activity 专项：`../references/widgets-live-activity.md`

**为什么重要**：2024 年 5 月起强制要求，缺失直接在 ASC 上传阶段被自动拦截。

---

## 2. 功能完整性

### 2.1 演示账号

- [ ] Review Notes 中提供可用的演示账号（邮箱+密码）
- [ ] 账号已解锁所有需要审核的功能（订阅、高级功能等）
- [ ] 如果使用 2FA，在 Review Notes 中说明验证码获取方式

**为什么重要**：2.1(a)。演示账号无效是第二高频拒审原因。审核员没有账号就无法测试功能。

### 2.2 后端在线

- [ ] 审核期间所有 API 服务 24/7 可访问（不能因维护窗口下线）
- [ ] 审核 IP 来自美国旧金山区（不能对该区域做地理封锁）
- [ ] 如需特殊网络条件，在 Review Notes 说明

**为什么重要**：后端离线等同于 App 崩溃，2.1(a) 拒审。

### 2.3 IPv6 支持

- [ ] 所有网络请求在 IPv6-only 网络下正常运行
- [ ] 本地测试：Mac 上开启 `Settings → Sharing → Internet Sharing` 模拟 IPv6-only 热点

**为什么重要**：Apple 审核环境是 IPv6-only。含有硬编码 IPv4 地址或不支持 IPv6 的网络库会导致功能失效。

### 2.4 无崩溃

- [ ] 真机测试（不只模拟器），包括 iPhone 最小支持机型和 iPad
- [ ] 测试所有主要流程：注册、核心功能、购买、退出
- [ ] Xcode Organizer 无崩溃报告（TestFlight Beta 数据）

**为什么重要**：2.1(a)。在审核员测试时崩溃是立即拒审，且留下不良记录影响后续审核速度。

---

## 3. 元数据

### 3.1 截图

- [ ] 截图来自当前版本的真实 UI（非设计稿、非旧版本）
- [ ] 设备边框正确匹配截图尺寸（6.9" 截图不能套 6.5" 边框）
- [ ] 截图中展示的功能已上线（不能有"即将推出"的功能）
- [ ] 不含 Apple 设备图片、Apple Logo（5.2.4/5.2.5）

**为什么重要**：2.3.3/2.3.4。元数据与实际不符是第五高频拒审原因。

### 3.2 App Name

- [ ] 长度 ≤ 30 字符
- [ ] 不含促销词：「Free」「Best」「#1」「Limited」等
- [ ] 不含竞品名称、平台名称（「Android」「Samsung」）
- [ ] 不含「app」词（除非是品牌名的一部分）

**为什么重要**：2.3.7。App Name 违规属于 Metadata Rejected，可无需重新打包修复，但浪费审核周期。

### 3.3 Description

- [ ] 不含未上线功能的描述
- [ ] 不含竞品名称（「比 XX 更好用」类表述）
- [ ] 不含价格/促销信息（如「限时免费」「首月 0 元」）
- [ ] 不含占位符文字

---

## 4. IAP（In-App Purchase）

### 4.1 沙盒测试

- [ ] 所有 IAP 项目在 App Store Connect 中状态为 `Ready to Submit`
- [ ] 沙盒账号完成完整购买流程（从点击购买到解锁内容）
- [ ] 消耗品：测试多次购买
- [ ] 非消耗品：测试恢复购买

### 4.2 恢复购买

- [ ] 界面上有「恢复购买」按钮（Restore Purchases）
- [ ] 功能真实生效：在沙盒中删除 App 后重装可恢复

**为什么重要**：3.1.1。缺少恢复购买是 IAP 类 App 的固定拒审点。Apple 要求用户换设备后不需要重复付款。

### 4.3 数字内容必须走 IAP

- [ ] 数字功能/内容解锁不通过外部支付链接（非 US 区）
- [ ] 不在 App 内展示比 App Store 更低的价格

---

## 5. 设计合规

### 5.1 Sign in with Apple

- [ ] 如果有任何第三方登录（Google、微信、Facebook、Twitter 等），**必须同时提供** Sign in with Apple
- [ ] Apple 登录按钮样式符合 HIG 规范（不能缩小、变形、改色）

**为什么重要**：4.8。这是不可谈判的硬规则，缺少 Sign in with Apple 直接拒审。

### 5.2 字体可读性

- [ ] 正文字号在真实 iPhone 最小支持机型上清晰可读（建议 ≥ 14pt）
- [ ] 文字与背景对比度符合 WCAG AA 标准（4.5:1）

---

## 6. 2026 特殊要求

| 要求 | 截止日期 | 影响范围 |
|------|---------|---------|
| 必须使用 iOS/iPadOS 26 SDK 编译 | **2026-04-28** | 所有新提交和更新 |
| 年龄分级新增 13+/16+/18+ 档 | 2026-01-31（已过，存量App需更新） | 含成人内容、暴力、赌博相关功能的App |

**iOS 26 SDK 检查方式**：
```bash
# 确认 Xcode 版本支持 iOS 26 SDK
xcodebuild -showsdks | grep iphoneos
# 需要输出 iphoneos26.0 或更高
```

---

## Review Notes 模板

```
【演示账号】
邮箱：demo@example.com
密码：Demo1234!

【功能说明】
本次版本更新：[简述主要变更]
需重点审核：[列出新增功能]

【特殊说明】
[如：某功能需要特定地区；某功能需要硬件支持等]
```

---

## 相关详细文档

| 话题 | 文件 |
|------|------|
| PrivacyInfo 扫描 | `../checks/required-reason-api-scan.md` |
| 隐私五处一致性 | `../checks/privacy-transparency-consistency.md` |
| 高频拒审条款 | `../checks/review-failure-map.md` |
| IAP / 订阅合规 | `../guidelines/3-business.md` |
| 被拒后处理 | `../operations/review-ops.md` |
| 订阅专项 | `subscription.md` |
| AI功能专项 | `ai-apps.md` |
| UGC社区专项 | `ugc-social.md` |
| 游戏专项 | `games.md` |
| 电商专项 | `ecommerce.md` |
