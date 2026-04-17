# CI/CD 上传与自动化配置手册
> 覆盖：fastlane / xcrun altool / Transporter / ITMS 错误修复 / CI 证书管理

---

## 一、fastlane 配置

### 1.1 基础安装

```bash
# 安装 fastlane
gem install fastlane
# 或使用 Bundler（推荐，锁定版本）
bundle add fastlane
bundle exec fastlane init
```

### 1.2 fastlane match（证书与 Profile 管理）

**match** 将证书和 Profile 存储在 Git 仓库（或 S3/Google Cloud Storage），团队共享。

```ruby
# Matchfile
git_url("https://github.com/yourorg/certificates")
git_branch("main")
storage_mode("git")          # 或 "s3" / "google_cloud"
type("appstore")             # development / adhoc / appstore / enterprise
app_identifier(["com.example.app", "com.example.app.widget"])
username("developer@example.com")
```

```bash
# 首次创建证书并存储
bundle exec fastlane match appstore

# CI 环境只读拉取（不创建新证书）
bundle exec fastlane match appstore --readonly
```

**加密密钥**：match 使用 `MATCH_PASSWORD` 环境变量加密仓库，CI 中通过 Secret 注入。

### 1.3 fastlane gym（构建）

```ruby
# Gymfile
scheme("MyApp")
export_method("app-store")
output_directory("./build")
output_name("MyApp.ipa")
clean(true)
include_symbols(true)         # 上传 dSYM 到 Crashlytics 等
include_bitcode(false)        # Bitcode 已于 Xcode 14 废弃
```

```bash
bundle exec fastlane gym
```

**常用参数**：
```ruby
gym(
  workspace: "MyApp.xcworkspace",
  scheme: "MyApp",
  configuration: "Release",
  export_options: {
    method: "app-store",
    provisioningProfiles: {
      "com.example.app" => "match AppStore com.example.app",
      "com.example.app.widget" => "match AppStore com.example.app.widget"
    }
  }
)
```

### 1.4 fastlane deliver（元数据 + 上传）

```ruby
# Deliverfile
username("developer@example.com")
app_identifier("com.example.app")
app_version("2.1.0")
ipa("./build/MyApp.ipa")
skip_metadata(true)           # 仅上传 Binary，不更新元数据
skip_screenshots(true)
submit_for_review(false)      # 上传但不提交审核（手动审核时用）
automatic_release(false)
```

```bash
bundle exec fastlane deliver
```

**自动提交审核**：
```ruby
deliver(
  submit_for_review: true,
  automatic_release: false,   # 通过后手动发布（配合 Phased Release）
  phased_release: true,
  submission_information: {
    add_id_info_uses_idfa: false,  # IDFA 声明
    export_compliance_uses_encryption: false
  }
)
```

### 1.5 完整 Fastfile 示例

```ruby
# fastlane/Fastfile
default_platform(:ios)

platform :ios do
  before_all do
    setup_ci if ENV['CI']     # CI 环境自动配置 Keychain
  end

  desc "同步证书"
  lane :certificates do
    match(type: "appstore", readonly: is_ci)
  end

  desc "构建并上传到 TestFlight"
  lane :beta do
    certificates
    increment_build_number(
      build_number: latest_testflight_build_number + 1
    )
    gym
    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      changelog: "Beta build #{lane_context[SharedValues::BUILD_NUMBER]}"
    )
  end

  desc "构建并提交审核"
  lane :release do
    certificates
    gym
    deliver(
      submit_for_review: true,
      phased_release: true,
      force: true             # 跳过 HTML 预览确认
    )
  end

  error do |lane, exception|
    # 发送 Slack 通知（可选）
    slack(
      message: "❌ Lane #{lane} failed: #{exception.message}",
      success: false
    ) if ENV['SLACK_URL']
  end
end
```

---

## 二、xcrun 命令行工具

### 2.1 xcrun altool（Xcode 13 及以下）

```bash
# 验证 IPA
xcrun altool --validate-app \
  --file MyApp.ipa \
  --type ios \
  --username "developer@apple.com" \
  --password "@keychain:Application Loader: developer@apple.com"

# 上传 IPA（使用 App-Specific Password）
xcrun altool --upload-app \
  --file MyApp.ipa \
  --type ios \
  --username "developer@apple.com" \
  --password "xxxx-xxxx-xxxx-xxxx"    # App-Specific Password

# 使用 API Key（推荐，不需要 Apple ID）
xcrun altool --upload-app \
  --file MyApp.ipa \
  --type ios \
  --apiKey "XXXXXXXXXX" \
  --apiIssuer "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

> **注意**：Xcode 15+ 中 altool 已被废弃，推荐使用 `xcrun notarytool`（macOS）或 `xcodebuild -exportArchive` + Transporter。

### 2.2 xcrun notarytool（macOS App 公证，非 iOS）

```bash
# 公证 macOS App/PKG/DMG
xcrun notarytool submit MyApp.pkg \
  --apple-id "developer@apple.com" \
  --password "xxxx-xxxx-xxxx-xxxx" \
  --team-id "XXXXXXXXXX" \
  --wait

# 查看公证历史
xcrun notarytool history \
  --apple-id "developer@apple.com" \
  --password "xxxx-xxxx-xxxx-xxxx" \
  --team-id "XXXXXXXXXX"

# 查看具体公证日志（失败时用）
xcrun notarytool log <submission-id> \
  --apple-id "developer@apple.com" \
  --password "xxxx-xxxx-xxxx-xxxx" \
  --team-id "XXXXXXXXXX"
```

### 2.3 xcodebuild 上传（Xcode 14+）

```bash
# Archive
xcodebuild archive \
  -scheme MyApp \
  -archivePath ./build/MyApp.xcarchive \
  CODE_SIGN_IDENTITY="Apple Distribution: Company Name" \
  PROVISIONING_PROFILE_SPECIFIER="match AppStore com.example.app"

# Export IPA
xcodebuild -exportArchive \
  -archivePath ./build/MyApp.xcarchive \
  -exportPath ./build/ \
  -exportOptionsPlist ExportOptions.plist
```

**ExportOptions.plist 示例**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>XXXXXXXXXX</string>
    <key>uploadBitcode</key>
    <false/>
    <key>uploadSymbols</key>
    <true/>
    <key>signingStyle</key>
    <string>manual</string>
    <key>provisioningProfiles</key>
    <dict>
        <key>com.example.app</key>
        <string>match AppStore com.example.app</string>
    </dict>
</dict>
</plist>
```

---

## 三、Transporter 使用

Transporter 是 Apple 官方的图形化/命令行上传工具（Mac App Store 可免费下载）。

### 3.1 命令行模式

```bash
# Transporter 路径（安装后）
/Applications/Transporter.app/Contents/itms/bin/iTMSTransporter

# 上传 IPA（使用 API Key）
/Applications/Transporter.app/Contents/itms/bin/iTMSTransporter \
  -m upload \
  -f /path/to/MyApp.ipa \
  -apiKey XXXXXXXXXX \
  -apiIssuer xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx \
  -v eXtreme

# 上传 IPA（使用 Apple ID）
/Applications/Transporter.app/Contents/itms/bin/iTMSTransporter \
  -m upload \
  -f /path/to/MyApp.ipa \
  -u developer@apple.com \
  -p "xxxx-xxxx-xxxx-xxxx" \
  -v eXtreme
```

### 3.2 App Store Connect API Key 生成

1. ASC → Users and Access → Keys → Generate API Key
2. 选择 Role：App Manager 或 Developer（上传用 Developer 即可）
3. 下载 .p8 文件（只能下载一次）
4. 记录 Key ID 和 Issuer ID

```bash
# 环境变量方式（fastlane/CI 推荐）
export APP_STORE_CONNECT_API_KEY_KEY_ID="XXXXXXXXXX"
export APP_STORE_CONNECT_API_KEY_ISSUER_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export APP_STORE_CONNECT_API_KEY_KEY_FILEPATH="/path/to/AuthKey_XXXXXXXXXX.p8"
```

---

## 四、常见 ITMS 错误代码和修复

### ITMS-90035：签名无效

**错误信息**：`ERROR ITMS-90035: "Invalid Signature. A sealed resource is missing or invalid."`

**原因**：
- 代码签名证书不匹配
- Embedded Provisioning Profile 中的 Certificate 与签名不一致
- 手动修改了 IPA 内容（如替换资源文件）

**修复**：
```bash
# 检查签名
codesign -dvvv MyApp.app

# 检查 Provisioning Profile
security cms -D -i MyApp.app/embedded.mobileprovision

# 重新 Archive（确保 Keychain 中有对应私钥）
# Xcode → Product → Clean Build Folder → Archive
```

### ITMS-90161：Profile 不匹配

**错误信息**：`ERROR ITMS-90161: "Invalid Provisioning Profile. The provisioning profile included in the bundle com.example.app [MyApp.app] is invalid."`

**原因**：
- Profile 已过期（Developer Portal 中查看）
- Profile 中 Bundle ID 不匹配
- Profile 不是 App Store Distribution 类型

**修复**：
```bash
# fastlane match 重新下载
bundle exec fastlane match appstore --force_for_new_devices

# 或手动：Developer Portal → Profiles → 撤销旧 Profile → 生成新 Profile
```

### ITMS-90338：私有 API

**错误信息**：`ERROR ITMS-90338: "Non-public API usage. The app references non-public selectors in Xxx.framework: privateMethod"`

**修复**：
```bash
# 用 nm 命令检查哪个框架引用了私有 API
nm -u MyApp | grep privateMethod

# 或用 otool
otool -l MyApp | grep -A2 LC_LOAD_DYLIB

# 检查第三方 SDK 版本，升级至修复版本
```

### ITMS-90683：缺少权限描述字符串

**错误信息**：`ERROR ITMS-90683: "Missing Purpose String in Info.plist File. Your app's code references one or more APIs that access sensitive user data. The app's Info.plist file should contain a NSCameraUsageDescription key..."`

**修复**：在 Info.plist 中添加对应 key：

```xml
<!-- 相机 -->
<key>NSCameraUsageDescription</key>
<string>需要访问相机以扫描二维码</string>

<!-- 相册 -->
<key>NSPhotoLibraryUsageDescription</key>
<string>需要访问相册以选择图片</string>

<!-- 麦克风 -->
<key>NSMicrophoneUsageDescription</key>
<string>需要访问麦克风以录制音频</string>

<!-- 位置（使用期间） -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>需要位置信息以显示附近内容</string>

<!-- 位置（始终） -->
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>需要后台位置以提供实时通知</string>

<!-- 联系人 -->
<key>NSContactsUsageDescription</key>
<string>需要访问联系人以邀请朋友</string>

<!-- 通知（iOS 10+，UNUserNotificationCenter） -->
<!-- 通知不需要 Info.plist key，但需要在代码中请求权限 -->

<!-- 面容 ID / Touch ID -->
<key>NSFaceIDUsageDescription</key>
<string>需要面容 ID 以快速解锁</string>

<!-- 健康 -->
<key>NSHealthShareUsageDescription</key>
<string>需要读取健康数据以分析运动趋势</string>
<key>NSHealthUpdateUsageDescription</key>
<string>需要写入健康数据以记录锻炼</string>

<!-- 蓝牙 -->
<key>NSBluetoothAlwaysUsageDescription</key>
<string>需要蓝牙连接您的设备</string>

<!-- 追踪（ATT，iOS 14+） -->
<key>NSUserTrackingUsageDescription</key>
<string>通过您的数据提供个性化广告体验</string>
```

### ITMS-91053：Privacy Manifest 缺少 Reason Code

见 `../references/privacy-manifest.md` 完整处理。

### ITMS-90809：使用废弃 UIWebView

**修复**：
```swift
// 删除所有 UIWebView 使用，替换为 WKWebView
import WebKit

let webView = WKWebView(frame: .zero, configuration: WKWebViewConfiguration())
let request = URLRequest(url: URL(string: "https://example.com")!)
webView.load(request)
```

同时检查第三方 SDK 中是否仍使用 UIWebView（升级 SDK 版本）。

### Processing Failed（无错误码）

**原因**：ASC 服务器内部错误，偶发。

**处理步骤**：
1. 等待30分钟，检查 App Store Connect System Status（https://developer.apple.com/system-status/）
2. 重新上传同一 Build（不需要重新 Archive，但需确保未修改 .ipa）
3. 若连续失败超过3次，联系 Apple Developer Support

---

## 五、CI/CD 证书管理要点

### 5.1 GitHub Actions

```yaml
# .github/workflows/release.yml
name: App Store Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: macos-15     # 使用最新 macOS runner
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Select Xcode version
        run: |
          sudo xcode-select -s /Applications/Xcode_16.4.app
          xcodebuild -version  # 验证 Xcode 版本
          # ⚠️ 注意：2026-04-28 起 App Store 提交必须使用 Xcode 26+ 和对应 SDK
          # 届时需更新为 Xcode_26.app 和 macos-26 runner
        
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          
      - name: Setup SSH for match
        uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ secrets.MATCH_DEPLOY_KEY }}
          
      - name: Run fastlane release
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_KEY_FILEPATH: /tmp/asc_key.p8
        run: |
          echo "${{ secrets.ASC_PRIVATE_KEY }}" > /tmp/asc_key.p8
          bundle exec fastlane release
```

**必须存入 GitHub Secrets 的值**：
| Secret Name | 说明 |
|-------------|------|
| MATCH_DEPLOY_KEY | 访问证书 Git 仓库的 SSH 私钥 |
| MATCH_PASSWORD | match 仓库加密密码 |
| ASC_KEY_ID | App Store Connect API Key ID |
| ASC_ISSUER_ID | App Store Connect Issuer ID |
| ASC_PRIVATE_KEY | .p8 文件内容（完整文本，含 -----BEGIN----- 行） |

### 5.2 Bitrise

```yaml
# bitrise.yml 关键 steps
- activate-ssh-key@4:
    inputs:
    - ssh_rsa_private_key: "$BITRISEIO_SSH_PRIVATE_KEY"
    
- fastlane@3:
    inputs:
    - lane: release
    - work_dir: "$BITRISE_SOURCE_DIR"
```

**Bitrise Keychain 管理**：fastlane 的 `setup_ci` 会自动处理 CI 环境的 Keychain，无需手动干预。

### 5.3 Xcode Cloud

Xcode Cloud 原生支持 App Store 证书，**无需 fastlane match**：
1. 在 Xcode → Product → Xcode Cloud → Create Workflow 中配置
2. Xcode Cloud 自动管理签名（使用 Automatic Signing）
3. 可直接配置 Post-Action 提交到 TestFlight 或 App Store

**Xcode Cloud 限制**：
- 不支持 Shell Script 调用 fastlane（只能用 CI scripts）
- 每月免费25小时，超出按量付费
- 仅 Apple Silicon Mac 可运行（M1 runner）

### 5.4 证书轮换最佳实践

- 证书有效期：Development 1年，Distribution 1年
- **提前30天**在 Developer Portal 生成新证书
- 使用 fastlane match 时：`bundle exec fastlane match appstore --force` 强制更新
- 将证书过期日期加入团队日历提醒
- 绝不在代码仓库中明文存储证书 .p12 文件

### 5.5 多 Target / App Extension 签名

每个 Extension（Widget、NotificationContent、ShareExtension 等）需要独立的 Provisioning Profile：

```ruby
# Matchfile 中指定所有 Bundle ID
app_identifier([
  "com.example.app",
  "com.example.app.widget",
  "com.example.app.notification-content",
  "com.example.app.share-extension"
])
```

```ruby
# Gymfile 中明确每个 target 的 Profile
gym(
  export_options: {
    provisioningProfiles: {
      "com.example.app"                         => "match AppStore com.example.app",
      "com.example.app.widget"                  => "match AppStore com.example.app.widget",
      "com.example.app.notification-content"    => "match AppStore com.example.app.notification-content",
      "com.example.app.share-extension"         => "match AppStore com.example.app.share-extension"
    }
  }
)
```
