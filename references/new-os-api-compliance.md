# 新 OS / SDK 合规指南

> 覆盖 Apple 平台 SDK 最低编译版本要求、Deprecated API 检查、Minimum Deployment Target 策略及 Apple Silicon macCatalyst 注意事项。
> 关键截止日期：**2026-04-28 起所有提交必须使用 iOS 26 SDK 编译**。

---

## 一、2026-04-28 SDK 最低要求（强制）

自 2026 年 4 月 28 日起，上传到 App Store Connect 的 App 必须满足以下最低 SDK 要求：

| 平台 | 最低 SDK | 最低 Xcode |
|------|---------|-----------|
| iOS / iPadOS | iOS 26 & iPadOS 26 SDK | Xcode 26 |
| tvOS | tvOS 26 SDK | Xcode 26 |
| visionOS | visionOS 26 SDK | Xcode 26 |
| watchOS | watchOS 26 SDK | Xcode 26 |
| macOS | 无新强制要求（但推荐 macOS 26 SDK） | Xcode 26 |

**来源**：[Upcoming SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw)（2026-02-03 发布）

### 1.1 不满足要求的后果

- App Store Connect 会**直接拒绝上传**（不是人工审核拒绝，是系统级拒绝）
- 已在 App Store 上架的旧版本不受影响，但无法提交更新
- TestFlight 内部测试不受限制

### 1.2 迁移 Checklist

- [ ] 安装 Xcode 26（需 macOS 15 Sequoia 或更高）
- [ ] 更新 CI/CD 构建环境中的 Xcode 版本
- [ ] 更新项目 `.xcodeproj` / `.xcworkspace` 中的 Build Settings
- [ ] 运行 `xcodebuild -showsdks` 确认 SDK 版本
- [ ] 修复 Xcode 26 新增的 warning 和 deprecation
- [ ] 在 iOS 26 模拟器和真机上验证功能正常

### 1.3 验证当前 SDK 版本

```bash
# 查看当前安装的 SDK 版本
xcodebuild -showsdks

# 查看 Xcode 版本
xcodebuild -version

# 查看编译后 binary 的 SDK 版本
otool -l YourApp.app/YourApp | grep -A2 LC_BUILD_VERSION

# 对于 .ipa 文件
unzip -o YourApp.ipa -d /tmp/app_check
otool -l /tmp/app_check/Payload/*.app/* | grep -A5 LC_BUILD_VERSION | head -20
```

---

## 二、Deprecated API 检查

### 2.1 Xcode 编译器 Warning

Xcode 26 会对以下 API 产生 deprecation warning：

```bash
# 编译时检查所有 deprecation warning
xcodebuild -project YourApp.xcodeproj \
  -scheme YourApp \
  -sdk iphoneos \
  clean build 2>&1 | grep -i "deprecated"
```

Swift 中使用 `#available` 做版本条件判断：

```swift
if #available(iOS 26, *) {
    // 使用 iOS 26 新 API
    let config = UIContentConfiguration.automatic()
    cell.contentConfiguration = config
} else {
    // 回退到旧 API
    cell.textLabel?.text = "Fallback"
}
```

Objective-C 中使用 `@available` 和 `__API_AVAILABLE` 宏：

```objc
if (@available(iOS 26, *)) {
    // 使用新 API
} else {
    // 回退
}

// 编译时启用 deprecation warning
// Build Settings → Other Warning Flags → -Wdeprecated-declarations
```

### 2.2 常见 Deprecated API 及替代

| Deprecated API | 替代 API | 从何版本开始 |
|---------------|---------|-------------|
| `UIWebView` | `WKWebView` | iOS 12（已完全移除） |
| `UIAlertView` | `UIAlertController` | iOS 9 |
| `UIActionSheet` | `UIAlertController` | iOS 9 |
| `UISearchDisplayController` | `UISearchController` | iOS 8 |
| `AddressBook.framework` | `Contacts.framework` | iOS 9 |
| `ALAssetsLibrary` | `PHPhotoLibrary` | iOS 9 |
| `UIApplication.openURL(_:)` | `UIApplication.open(_:options:completionHandler:)` | iOS 10 |
| `SKPaymentQueue.default()` | StoreKit 2 `Product.purchase()` | iOS 15 |
| `ASIdentifierManager` | `ATTrackingManager` | iOS 14 |

### 2.3 批量检查 Deprecated 调用

```bash
# 扫描项目中的已知 deprecated 调用（Swift）
grep -rn "UIWebView\|UIAlertView\|UIActionSheet\|ALAssetsLibrary\|addressBook" \
  --include="*.swift" YourProject/

# 扫描项目中的已知 deprecated 调用（Objective-C）
grep -rn "UIWebView\|UIAlertView\|UIActionSheet\|ALAssetsLibrary\|ABAddressBook" \
  --include="*.m" --include="*.h" YourProject/

# 检查第三方 Framework 中是否包含 deprecated API
for fw in Pods/**/*.framework; do
  echo "=== $fw ==="
  nm "$fw/$(basename "$fw" .framework)" 2>/dev/null | grep -i "UIWebView\|UIAlertView"
done
```

---

## 三、Minimum Deployment Target 策略

### 3.1 Apple 建议与市场实践

Apple 不强制 Minimum Deployment Target，但市场实践（覆盖率参考 Apple 官方或 Mixpanel 等第三方统计，⚠️ 经验规则）：

| 策略 | Minimum Target | 建议 |
|------|---------------|------|
| 激进 | 最新主版本（如 iOS 26）| 仅新项目、面向最新设备 |
| 主流 | 当前主版本 - 1（如 iOS 18）| ✅ 推荐大多数项目 |
| 保守 | 当前主版本 - 2（如 iOS 17）| 金融/医疗等高覆盖需求 |
| 遗留 | 当前主版本 - 3 或更旧（如 iOS 16）| 仅维护旧项目 |

**注意**：iOS 从 18 直接跳到 26（Apple 2025 年统一版本号为 OS 代号 + 年份）。请以 [Apple App Store 官方统计](https://developer.apple.com/support/app-store/) 的当前分布为准。

### 3.2 更改 Deployment Target 的 Checklist

- [ ] 在 Xcode → Project → Info → Deployment Target 中修改
- [ ] 更新所有 Target（App、Extension、Widget 等）保持一致
- [ ] 更新 CocoaPods / SPM 的 platform 版本声明
- [ ] 检查所有 `#available` / `@available` 条件是否仍然有效
- [ ] 更新 CI/CD 中的模拟器版本列表

---

## 四、Apple Silicon 与 macCatalyst 注意事项

### 4.1 Apple Silicon Mac 上的 iOS App

- Apple Silicon Mac 可以直接运行 iOS App（通过 Mac App Store → iPhone & iPad Apps）
- 开发者可在 ASC 中**选择退出**（Pricing and Availability → Mac App Store 取消勾选）
- 如果不退出，需确保 App 在 Mac 上可用（无 Camera-only 功能、键盘支持等）

### 4.2 macCatalyst 特别要求

```bash
# 检查 Catalyst 构建是否正常
xcodebuild -project YourApp.xcodeproj \
  -scheme YourApp \
  -destination 'platform=macOS,variant=Mac Catalyst' \
  build 2>&1 | tail -20
```

| 注意项 | 说明 |
|-------|------|
| 屏幕尺寸 | macCatalyst 窗口可调整大小，需支持多种尺寸 |
| 菜单栏 | macOS 用户期望有菜单栏操作（`UIMenuBuilder`） |
| 触控板 | 替代 touch 手势的 trackpad/mouse 支持 |
| 沙盒 | macCatalyst App 默认 sandboxed，文件访问受限 |
| Entitlements | 部分 iOS entitlements 在 macCatalyst 中不可用或行为不同 |
| 审核 | macCatalyst App 同时需要满足 macOS 审核要求 |

### 4.3 macCatalyst 常见问题

| 问题 | 解决 |
|------|------|
| App 在 Mac 上窗口太小 | 设置 `UIApplicationSceneManifest` 的 minimum size |
| Camera API crash | 使用 `#if targetEnvironment(macCatalyst)` 条件编译 |
| Push Notification 不弹出 | macCatalyst 使用 UNUserNotificationCenter（同 iOS）但需额外 entitlement |
| 网络请求被沙盒阻止 | 检查 App Sandbox entitlements 中的 Network 权限 |

---

## 五、App Extensions 与新 SDK

### 5.1 Widget / Live Activity

如果使用 WidgetKit，注意：

- iOS 26 SDK 可能引入新的 Widget 尺寸或 API
- `ActivityKit` Live Activity 在 iOS 23.1+ 可用
- Widget Extension 的 Deployment Target 必须与主 App 一致

### 5.2 App Intents（Siri / Shortcuts）

- iOS 26 强化了 App Intents 框架
- 如果 App 声明了 Siri 支持，需确保 Intent 在新 SDK 下正常工作

---

## 六、审核 Checklist

### 提交前必检

- [ ] 使用 Xcode 26 编译（`xcodebuild -version` 确认）
- [ ] 目标 SDK 为 iOS 26 / iPadOS 26（`xcodebuild -showsdks` 确认）
- [ ] 无 `UIWebView` 引用（包括第三方 SDK）
- [ ] 所有 deprecation warning 已处理或确认不影响功能
- [ ] Minimum Deployment Target 设置合理（建议 iOS 18+，见第三章策略表）
- [ ] macCatalyst（如启用）：Mac 上功能正常、窗口可调整
- [ ] Apple Silicon Mac（如未退出）：iOS App 在 Mac 上可用
- [ ] 所有 App Extensions 的 SDK 和 Deployment Target 一致
- [ ] CI/CD 构建环境已更新到 Xcode 26

### 系统级拒绝（非人工审核）

| 错误 | 原因 | 修复 |
|------|------|------|
| ITMS-90725 | SDK 版本过低 | 升级 Xcode 到 26 |
| ITMS-90809 | 包含 UIWebView | 替换为 WKWebView，检查第三方 SDK |
| ITMS-90338 | 不支持的架构（如 armv7） | 移除 32-bit 架构支持 |
| ITMS-90XXX | Missing required SDK | 重新编译并确认 SDK 版本 |

---

## 七、参考链接

- [Upcoming SDK minimum requirements](https://developer.apple.com/news/?id=ueeok6yw)
- [Xcode Release Notes](https://developer.apple.com/documentation/xcode-release-notes)
- [Mac Catalyst](https://developer.apple.com/mac-catalyst/)
- 相关文件：`../operations/cicd-upload.md`（CI/CD 上传）、`../by-app-type/mac-macos.md`（macOS 专项）
