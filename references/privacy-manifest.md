# Privacy Manifest 完整指南
> PrivacyInfo.xcprivacy 结构 + Required Reason API + 第三方 SDK 要求
> 强制执行时间：2024年5月起（新App）；现有App每次更新均需合规

---

## 一、PrivacyInfo.xcprivacy 文件概述

Privacy Manifest 是一个 XML Property List 文件，声明 App 或 SDK 使用的隐私敏感 API 及原因。Apple 从 Xcode 15 开始支持，从 2024年5月1日起强制要求。

**文件名**：`PrivacyInfo.xcprivacy`（固定名称，不可修改）

**位置**：
- App Target：添加到 App 主 Target（通常在 Sources 目录）
- SDK/Framework：放在 Framework Bundle 的根目录

### 1.1 在 Xcode 中添加

1. Xcode → File → New → File from Template → Resource → App Privacy
2. 选择对应 Target（App Target 或 Framework Target）
3. 文件会以 `.xcprivacy` 扩展名创建，Xcode 提供图形编辑界面
4. 也可直接编辑 XML 源码

---

## 二、PrivacyInfo.xcprivacy 完整结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- ① 声明 App 收集的数据类型（对应 Nutrition Labels）-->
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeEmailAddress</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <true/>          <!-- 是否与用户身份关联 -->
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>         <!-- 是否用于跨 App 追踪 -->
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>

    <!-- ② 声明是否使用数据追踪用户 -->
    <key>NSPrivacyTracking</key>
    <false/>

    <!-- ③ 声明追踪域名（若 NSPrivacyTracking = true）-->
    <key>NSPrivacyTrackingDomains</key>
    <array>
        <!-- <string>analytics.example.com</string> -->
    </array>

    <!-- ④ 声明使用的 Required Reason API（最重要！）-->
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategorySystemBootTime</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>35F9.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

---

## 三、Required Reason API 完整列表

以下5类 API 必须在 manifest 中声明使用原因，否则触发 ITMS-91053。

### 类别1：File Timestamp（文件时间戳）

**API 标识**：`NSPrivacyAccessedAPICategoryFileTimestamp`

**涉及 API**：
- `FileManager` 的 `creationDate`、`modificationDate` 属性
- `stat`、`statx`、`getattrlist`、`getattrlistbulk`、`fgetattrlist`
- `NSFileCreationDate`、`NSFileModificationDate`

**Reason Codes**：

| Code | 适用场景 |
|------|---------|
| `DDA9.1` | App 的核心功能需要展示文件时间戳给用户 |
| `C617.1` | 仅访问 App 自身目录内的文件时间戳（App 沙盒内）|
| `3B52.1` | 访问用户授权选择的文件的时间戳（如通过 Document Picker）|
| `0A2A.1` | 第三方 SDK：记录或发送诊断数据给开发者（非追踪）|

**最常用**：`C617.1`（访问自己的文件）

### 类别2：System Boot Time（系统启动时间）

**API 标识**：`NSPrivacyAccessedAPICategorySystemBootTime`

**涉及 API**：
- `systemUptime`（`ProcessInfo.processInfo.systemUptime`）
- `mach_absolute_time()`
- `sysctl()` 读取 `kern.boottime`
- `NSProcessInfo.systemUptime`

**Reason Codes**：

| Code | 适用场景 |
|------|---------|
| `35F9.1` | 计算 App 内事件的时间间隔（相对时间，不与绝对时间关联）|
| `8FFB.1` | 计算 App 自身的系统运行时间（测量 App 性能）|
| `3D61.1` | 第三方 SDK：提供防欺诈能力 |

**最常用**：`35F9.1`（动画、计时器等）

### 类别3：Disk Space（磁盘空间）

**API 标识**：`NSPrivacyAccessedAPICategoryDiskSpace`

**涉及 API**：
- `FileManager.default.attributesOfFileSystem(forPath:)`
- `volumeAvailableCapacity`、`volumeTotalCapacity`
- `NSFileSystemFreeSize`、`NSFileSystemSize`
- `statfs()`、`statvfs()`、`fstatfs()`、`fstatvfs()`

**Reason Codes**：

| Code | 适用场景 |
|------|---------|
| `85F4.1` | App 在写入数据前检查可用空间是否足够 |
| `E174.1` | 向用户显示磁盘空间信息（核心功能） |
| `7D9E.1` | 第三方 SDK：记录磁盘空间用于诊断/Bug 报告 |

**最常用**：`85F4.1`（下载前检查空间）

### 类别4：Active Keyboards（活跃键盘列表）

**API 标识**：`NSPrivacyAccessedAPICategoryActiveKeyboards`

**涉及 API**：
- `UITextInputMode.activeInputModes`

**Reason Codes**：

| Code | 适用场景 |
|------|---------|
| `3EC4.1` | App 是自定义键盘 Extension |
| `54BD.1` | App 需要根据当前键盘语言自动调整 UI（如文字方向、字体）|

### 类别5：User Defaults（UserDefaults）

**API 标识**：`NSPrivacyAccessedAPICategoryUserDefaults`

**涉及 API**：
- `UserDefaults`（包括 `standardUserDefaults`）
- `NSUserDefaults`

**Reason Codes**：

| Code | 适用场景 |
|------|---------|
| `CA92.1` | 读取/写入 App 自身的 UserDefaults（首选项、设置）|
| `1C8F.1` | 读取 App Group 共享的 UserDefaults（主 App 与 Extension 共享）|
| `C56D.1` | 第三方 SDK：只读访问 UserDefaults |
| `AC6B.1` | 第三方 SDK：读写 App 通过 API 授权访问的 UserDefaults |

**最常用**：`CA92.1`（所有 App 几乎都用 UserDefaults 存设置）

---

## 四、第三方 SDK 的 Manifest 要求

### 4.1 规则

- **SDK 必须提供自己的 `PrivacyInfo.xcprivacy`**，内嵌在 SDK Framework/XCFramework 中
- App 的 manifest 不需要重复声明 SDK 使用的 API（SDK 自己声明）
- Xcode 在打包时会自动合并 App 和所有 SDK 的 manifest
- 若 SDK **未提供** manifest，App 需要在自己的 manifest 中代为声明该 SDK 使用的 API

### 4.2 Apple 要求提供 manifest 的 SDK 列表

Apple 维护了一个[强制要求提供 manifest 的 SDK 清单](https://developer.apple.com/support/third-party-SDK-requirements/)（持续更新）。

**截至2026年2月，主要包括**（不完整，以 Apple 官方页面为准）：

| SDK | 最低合规版本 | Privacy API 使用 |
|-----|------------|-----------------|
| Firebase （Google Analytics for Firebase） | 10.18.0+ | UserDefaults, FileTimestamp |
| Firebase Crashlytics | 10.18.0+ | FileTimestamp, SystemBootTime |
| Firebase Performance | 10.18.0+ | SystemBootTime, DiskSpace |
| Amplitude Analytics | 8.17.1+ | UserDefaults, FileTimestamp |
| Branch.io | 3.4.3+ | UserDefaults, FileTimestamp |
| AppsFlyerLib | 6.12.2+ | UserDefaults, SystemBootTime |
| Mixpanel | 4.1.6+ | UserDefaults |
| Adjust SDK | 4.38.0+ | UserDefaults, FileTimestamp |
| Sentry | 8.17.0+ | FileTimestamp, SystemBootTime |
| Bugsnag | 6.28.0+ | FileTimestamp, UserDefaults |
| Lottie | 4.3.0+ | 无（或版本更新后无需声明）|

**检查方法**：
```bash
# 查看 Framework 内是否有 PrivacyInfo.xcprivacy
find /path/to/SDK.framework -name "PrivacyInfo.xcprivacy"

# 或在 Pods 目录检查
find Pods -name "PrivacyInfo.xcprivacy" -exec echo {} \;
```

### 4.3 SDK 未提供 Manifest 时的处理

若 SDK 还未提供 manifest（旧版本）：
1. **首选**：升级 SDK 到提供 manifest 的版本
2. **次选**：在 App 的 PrivacyInfo.xcprivacy 中代为声明该 SDK 的 API 使用

```xml
<!-- 代为声明 SDK 使用的 API，在 reason 后注明 -->
<dict>
    <key>NSPrivacyAccessedAPIType</key>
    <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array>
        <string>CA92.1</string>
        <!-- 注：此条目覆盖 LegacySDK 的使用，SDK v1.x 尚未提供 manifest -->
    </array>
</dict>
```

---

## 五、与 App Store Privacy Nutrition Labels 的一致性要求

Privacy Manifest 中的 `NSPrivacyCollectedDataTypes` 必须与 ASC 中填写的 Privacy Nutrition Labels **完全一致**。不一致会导致：
- ITMS-91053 类似错误
- 审核员手动拒审（Guideline 5.1.1）

### 5.1 NSPrivacyCollectedDataType 完整值列表

**联系信息类**：
- `NSPrivacyCollectedDataTypeEmailAddress`
- `NSPrivacyCollectedDataTypePhoneNumber`
- `NSPrivacyCollectedDataTypePhysicalAddress`
- `NSPrivacyCollectedDataTypeName`

**健康与健身类**：
- `NSPrivacyCollectedDataTypeHealth`
- `NSPrivacyCollectedDataTypeFitness`

**财务信息类**：
- `NSPrivacyCollectedDataTypePaymentInfo`
- `NSPrivacyCollectedDataTypeCreditInfo`
- `NSPrivacyCollectedDataTypeOtherFinancialInfo`

**位置类**：
- `NSPrivacyCollectedDataTypePreciseLocation`
- `NSPrivacyCollectedDataTypeCoarseLocation`

**敏感信息类**：
- `NSPrivacyCollectedDataTypeSensitiveInfo`

**联系人类**：
- `NSPrivacyCollectedDataTypeContacts`
- `NSPrivacyCollectedDataTypeEmailsOrTextMessages`
- `NSPrivacyCollectedDataTypePhotosorVideos`
- `NSPrivacyCollectedDataTypeAudioData`
- `NSPrivacyCollectedDataTypeGameplayContent`
- `NSPrivacyCollectedDataTypeCustomerSupport`
- `NSPrivacyCollectedDataTypeOtherUserContent`

**浏览历史类**：
- `NSPrivacyCollectedDataTypeBrowsingHistory`

**搜索历史类**：
- `NSPrivacyCollectedDataTypeSearchHistory`

**标识符类**：
- `NSPrivacyCollectedDataTypeDeviceID`
- `NSPrivacyCollectedDataTypeUserID`

**购买记录类**：
- `NSPrivacyCollectedDataTypePurchaseHistory`

**使用数据类**：
- `NSPrivacyCollectedDataTypeProductInteraction`
- `NSPrivacyCollectedDataTypeAdvertisingData`
- `NSPrivacyCollectedDataTypeOtherUsageData`

**诊断类**：
- `NSPrivacyCollectedDataTypeCrashData`
- `NSPrivacyCollectedDataTypePerformanceData`
- `NSPrivacyCollectedDataTypeOtherDiagnosticData`

### 5.2 NSPrivacyCollectedDataTypePurposes 值列表

- `NSPrivacyCollectedDataTypePurposeAppFunctionality`（App 核心功能）
- `NSPrivacyCollectedDataTypePurposeAnalytics`（分析）
- `NSPrivacyCollectedDataTypePurposeDeveloperAdvertising`（开发者投放广告）
- `NSPrivacyCollectedDataTypePurposeThirdPartyAdvertising`（第三方广告）
- `NSPrivacyCollectedDataTypePurposeProductPersonalization`（个性化）
- `NSPrivacyCollectedDataTypePurposeOther`（其他）

---

## 六、Xcode 添加和验证步骤

### 6.1 添加新 PrivacyInfo.xcprivacy

1. Xcode → File → New → File
2. 搜索 "Privacy"，选择 "App Privacy"
3. 命名为 `PrivacyInfo`（扩展名自动为 `.xcprivacy`）
4. 确认 Target Membership 勾选了正确的 Target

### 6.2 图形界面编辑

Xcode 提供分类编辑界面：
- **Privacy Nutrition Label Types**：对应 `NSPrivacyCollectedDataTypes`
- **Privacy Accessed API Types**：对应 `NSPrivacyAccessedAPITypes`
- **Privacy Tracking Enabled**：对应 `NSPrivacyTracking`
- **Privacy Tracking Domains**：对应 `NSPrivacyTrackingDomains`

### 6.3 验证 manifest 完整性

```bash
# Archive 后检查合并结果
# 路径：.xcarchive/Products/Applications/MyApp.app/PrivacyInfo.xcprivacy
cat MyApp.xcarchive/Products/Applications/MyApp.app/PrivacyInfo.xcprivacy

# 检查所有 Frameworks 中的 manifest
find MyApp.xcarchive -name "PrivacyInfo.xcprivacy" -exec echo "Found: {}" \; -exec cat {} \;
```

### 6.4 使用 Xcode 的 Privacy Report

Xcode 15.2+ 支持生成 Privacy Report：
1. Xcode → Product → Archive
2. Organizer → 选择 Archive → Generate Privacy Report
3. 报告列出所有使用的隐私 API 及其声明状态

### 6.5 常见错误排查

**ITMS-91053**：缺少必要的 reason code
- 打开 Report（Organizer 中）查看具体缺少哪个 API 的 reason
- 在 PrivacyInfo.xcprivacy 中补充对应条目

**ITMS-91055**：第三方 SDK 未提供 manifest
- 升级 SDK 版本
- 或在 App manifest 中代为声明

**Build 通过但 ASC 处理时报错**：
- 检查是否所有 Framework 都正确嵌入（非 Link Only）
- 检查 Widget Extension、NotificationContent Extension 等是否也有 manifest（各 Extension 作为独立 Bundle，需要各自的 manifest）
