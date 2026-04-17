# code-scan-patterns.md
# 来源：Apple App Store Review Guidelines 2026-02-06 + 实战经验汇总
# 用途：apple-review-preflight skill 代码级风险扫描模式，供提审前自查使用
# 维护：每次 Apple 更新 Guidelines 后同步更新

---

## 概述

提审前代码扫描是发现致命问题的最后防线。本文件按风险等级分类列出常见模式，
并分 Swift 和 React Native/Expo 两个技术栈给出代码示例和 shell 扫描命令。

**扫描顺序建议**：CRITICAL → HIGH → MEDIUM，发现 CRITICAL 立即停止提审修复。

---

## 🔴 CRITICAL — 立即阻断，必须修复后才能提交

### C1. 私有 API 调用

Apple 的静态扫描会检测私有 API，命中即被拒（Guideline 2.5.1）。

**Swift / Objective-C 示例**：
```swift
// ❌ 违规：下划线开头的私有方法
let window = UIApplication.shared._statusBar
view._setLayerBorderColor(UIColor.red.cgColor)

// ❌ 违规：NSSelectorFromString 调用私有方法
let sel = NSSelectorFromString("_removeAllAnimations")
layer.perform(sel)

// ❌ 违规：dlopen / dlsym 绕过限制
let handle = dlopen("/usr/lib/libMobileGestalt.dylib", RTLD_LAZY)
let sym = dlsym(handle, "MGCopyAnswer")

// ✅ 合规：使用公开 API
NotificationCenter.default.post(name: .UIApplicationDidBecomeActive, object: nil)
```

**React Native / Expo 示例**：
```javascript
// ❌ 违规：通过 NativeModules 调用私有方法
NativeModules.UIManager.sendAccessibilityEvent(tag, 8)  // 私有事件类型

// ❌ 违规：直接调用内部 bridge 方法
const bridge = global.__fbBatchedBridge
bridge._callFunction('AppState', '_handleAppStateChange', [])
```

**Shell 扫描命令**：
```bash
# 扫描私有 API 调用（Swift/ObjC）
grep -rn "_[a-z][A-Za-z]*:" --include="*.swift" --include="*.m" --include="*.mm" . \
  | grep -v "//.*_" \
  | grep -v "test\|Test\|spec\|Spec"

# 扫描 NSSelectorFromString（高风险，需人工确认是否调用私有方法）
grep -rn "NSSelectorFromString\|performSelector" --include="*.swift" --include="*.m" .

# 扫描 dlopen/dlsym
grep -rn "dlopen\|dlsym\|objc_msgSend" --include="*.swift" --include="*.m" --include="*.c" .

# 扫描已知危险私有类
grep -rn "UIStatusBar\|_UIAlertController\|BSActionSheet\|SBApplication" \
  --include="*.swift" --include="*.m" .
```

---

### C2. 动态执行代码（热更新/代码下发）

Guideline 2.5.2：严禁运行时下载并执行本机代码。JSPatch、hotfix 类方案全部违规。

**Swift / Objective-C 示例**：
```swift
// ❌ 违规：JSPatch 或类似框架
JPEngine.startEngine()
JPEngine.evaluateScript("...")

// ❌ 违规：动态加载 framework
let bundle = Bundle(url: URL(string: "https://example.com/patch.framework")!)

// ❌ 违规：eval 执行下载的脚本
// （Objective-C 通过 JavaScriptCore）
let context = JSContext()
context?.evaluateScript(downloadedScript)  // downloadedScript 来自网络
```

**React Native / Expo 示例**：
```javascript
// ❌ 违规：CodePush 热更新（需关闭或改为仅更新 JS bundle，但仍有风险）
import codePush from 'react-native-code-push'
codePush.sync({ updateDialog: true, installMode: codePush.InstallMode.IMMEDIATE })

// ❌ 违规：动态 eval
const code = await fetch('https://api.example.com/logic.js').then(r => r.text())
eval(code)  // 严禁

// ⚠️ 灰色地带：Expo Updates（需确认不替换 native 代码）
import * as Updates from 'expo-updates'
// 仅更新 JS/assets 理论上被允许，但审核时仍需在 Review Notes 说明
```

**Shell 扫描命令**：
```bash
# 扫描 JSPatch 相关
grep -rn "JPEngine\|JSPatch\|hotfix\|HotFix" --include="*.swift" --include="*.m" --include="*.js" .

# 扫描动态加载
grep -rn "dlopen\|NSBundle.*URL\|loadNibNamed" --include="*.swift" --include="*.m" . \
  | grep -v "//\|test\|Test"

# 扫描 eval 在 JS 层
grep -rn "\beval(" --include="*.js" --include="*.ts" --include="*.tsx" . \
  | grep -v "//\|test\|Test\|__tests__"

# 检查 CodePush 依赖
grep -rn "react-native-code-push\|@codepush\|codePush" package.json yarn.lock .
```

---

### C3. 外部支付调用（数字商品/服务）

Guideline 3.1.1：数字商品和服务必须使用 StoreKit/IAP，不得引导到外部支付。

**Swift 示例**：
```swift
// ❌ 违规：在 App 内为数字商品发起外部支付
let paymentUrl = URL(string: "https://stripe.com/checkout?item=premium_plan")!
UIApplication.shared.open(paymentUrl)

// ❌ 违规：显示外部购买链接
let label = UILabel()
label.text = "在我们网站购买更便宜 → example.com/buy"  // 引导外部

// ✅ 合规：StoreKit
import StoreKit
let products = try await Product.products(for: ["com.app.premium"])
let result = try await products.first?.purchase()
```

**React Native 示例**：
```javascript
// ❌ 违规：调用 Stripe SDK 为数字商品收费
import { initStripe, createPaymentMethod } from '@stripe/stripe-react-native'
// 为"高级会员"等数字服务走 Stripe

// ❌ 违规：WebView 内嵌外部支付页
<WebView source={{ uri: 'https://paypal.me/myapp/9.99' }} />

// ✅ 合规：react-native-iap
import * as RNIap from 'react-native-iap'
const products = await RNIap.getProducts({ skus: ['premium_monthly'] })
await RNIap.requestPurchase({ sku: 'premium_monthly' })
```

**Shell 扫描命令**：
```bash
# 扫描外部支付 SDK
grep -rn "Stripe\|PayPal\|Braintree\|Square\|Alipay\|WechatPay\|stripe-react-native" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" \
  package.json Podfile . \
  | grep -v "//\|test\|Test"

# 扫描外部购买链接文字
grep -rn "cheaper\|website\|visit.*buy\|网站购买\|外部购买\|更便宜" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" \
  --include="*.strings" .

# 扫描 WebView 加载支付相关域名
grep -rn "paypal\|stripe\|checkout\|payment\|pay\." \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" . \
  | grep -i "webview\|url\|http"
```

---

### C4. 硬编码密钥 / 凭证

违反安全最佳实践，审核员可能发现后以 Guideline 5.X 拒绝，更严重的是泄露风险。

**Swift 示例**：
```swift
// ❌ 违规：硬编码 API 密钥
let apiKey = "sk-proj-aBcDeFgHiJkL1234567890"
let awsSecret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
let firebaseKey = "AIzaSyD-XXXXXXXXXXXXXXXXXXXXXXXXXXXX"

// ✅ 合规：从安全存储读取
let apiKey = Bundle.main.object(forInfoDictionaryKey: "API_KEY") as? String
// 或从 Keychain 读取
```

**React Native 示例**：
```javascript
// ❌ 违规：直接写在代码里
const API_KEY = 'AIzaSyD-XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
const SECRET = 'ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

// ❌ 违规：.env 文件提交到 repo（本身不违规，但风险极高）
// ✅ 合规：通过后端代理，App 不持有密钥
const response = await fetch('/api/proxy-endpoint')
```

**Shell 扫描命令**：
```bash
# 扫描常见密钥模式
grep -rEn "(sk-proj-|AIzaSy|ghp_|AKIA[A-Z0-9]{16}|-----BEGIN (RSA|EC|PRIVATE))" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" \
  --include="*.json" --include="*.plist" . \
  | grep -v "test\|Test\|mock\|Mock\|example\|Example"

# 扫描 AWS 凭证模式
grep -rEn "aws_access_key|aws_secret|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY" \
  --include="*.swift" --include="*.js" --include="*.ts" --include="*.env" .

# 扫描通用密码字段
grep -rEn "(password|passwd|secret|token|api_key)\s*=\s*['\"][^'\"]{8,}" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" . \
  | grep -v "//\|test\|Test\|Placeholder\|YOUR_"
```

---

## 🟡 HIGH — 高风险，大概率被拒，提审前必须解决

### H1. 引入广告 SDK 但缺少 ATT 框架

Guideline 5.1.2 + Apple ATT 要求：使用任何广告/追踪 SDK 必须实现 ATT 权限请求。

**Swift 示例**：
```swift
// ❌ 违规：引入 Firebase Analytics 但没有 ATT
import FirebaseAnalytics
Analytics.logEvent("purchase", parameters: nil)
// 缺少：
// import AppTrackingTransparency
// ATTrackingManager.requestTrackingAuthorization(completionHandler:)

// ✅ 合规
import AppTrackingTransparency
import AdSupport

func requestTracking() {
    ATTrackingManager.requestTrackingAuthorization { status in
        switch status {
        case .authorized:
            // 可以使用 IDFA
            let idfa = ASIdentifierManager.shared().advertisingIdentifier
        case .denied, .restricted, .notDetermined:
            // 不使用 IDFA，降级处理
        @unknown default:
            break
        }
    }
}
```

**React Native 示例**：
```javascript
// ❌ 违规：使用 Facebook SDK 无 ATT
import { Settings } from 'react-native-fbsdk-next'
Settings.initializeSDK()  // 可能在 ATT 之前采集数据

// ✅ 合规
import { check, PERMISSIONS, request } from 'react-native-permissions'
// 或
import { requestTrackingPermissionsAsync } from 'expo-tracking-transparency'

const { status } = await requestTrackingPermissionsAsync()
if (status === 'granted') {
  // 初始化广告 SDK
}
```

**Shell 扫描命令**：
```bash
# 检测广告 SDK 是否存在
grep -rn "Firebase\|FacebookSDK\|GoogleMobileAds\|AppLovin\|ironSource\|Adjust\|AppsFlyer" \
  Podfile package.json yarn.lock .

# 检测是否有 ATT 实现
grep -rn "ATTrackingManager\|requestTrackingAuthorization\|AppTrackingTransparency" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" .

# 检测 Info.plist 是否有 ATT 描述字符串
grep -n "NSUserTrackingUsageDescription" ios/*/Info.plist Info.plist 2>/dev/null
```

---

### H2. 有账号注册无账号删除

Guideline 5.1.1(v)：2022年6月起强制要求，凡是支持账号注册的 App 必须提供 App 内删除账号功能。

**Swift 示例**：
```swift
// ❌ 违规：只有注册，没有删除账号入口
func createAccount(email: String, password: String) {
    // 注册逻辑...
}
// 缺少：deleteAccount() 功能

// ✅ 合规：提供完整的账号删除流程
func deleteAccount() async throws {
    // 1. 向用户确认
    // 2. 调用后端删除账号 API
    // 3. 本地清除所有数据
    // 4. 登出并返回首页
    try await APIClient.shared.deleteAccount(userId: currentUser.id)
    await clearLocalData()
    await AuthManager.shared.signOut()
}
```

**Shell 扫描命令**：
```bash
# 检测是否有注册功能
grep -rn "signUp\|register\|createAccount\|createUser" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" . \
  | grep -v "//\|test\|Test"

# 检测是否有删除账号功能
grep -rn "deleteAccount\|delete.*account\|removeAccount\|deactivate" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" . \
  | grep -v "//\|test\|Test"

# 检测 UI 层是否有删除入口
grep -rn "Delete Account\|删除账号\|注销账号\|deactivate" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" \
  --include="*.strings" --include="*.json" .
```

---

### H3. 第三方 OAuth 但缺少 Sign in with Apple

Guideline 4.8：App 如果提供第三方登录（Google、Facebook、微信等），必须同时提供 Sign in with Apple。

**Swift 示例**：
```swift
// ❌ 违规：有 Google 登录但没有 Apple 登录
func loginWithGoogle() {
    GIDSignIn.sharedInstance.signIn(withPresenting: self) { result, error in
        // Google 登录回调处理
    }
}
// 缺少 Sign in with Apple

// ✅ 合规
import AuthenticationServices

func loginWithApple() {
    let provider = ASAuthorizationAppleIDProvider()
    let request = provider.createRequest()
    request.requestedScopes = [.fullName, .email]
    let controller = ASAuthorizationController(authorizationRequests: [request])
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests()
}
```

**Shell 扫描命令**：
```bash
# 检测第三方登录 SDK
grep -rn "GIDSignIn\|FacebookLogin\|WechatLogin\|TwitterKit\|react-native-google-signin\|react-native-fbsdk" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" \
  Podfile package.json .

# 检测是否有 Apple 登录实现
grep -rn "ASAuthorizationAppleIDProvider\|SignInWithApple\|appleSignIn\|apple.*login\|login.*apple" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" . \
  -i
```

---

## 🟠 MEDIUM — 中等风险，可能引发追问或概率性拒绝

### M1. 生产代码中的 console.log / print

不直接导致拒绝，但可能暴露用户数据给日志系统，违反隐私承诺。审核员偶尔检查。

**Shell 扫描命令**：
```bash
# Swift：检测 print 和 debugPrint（应用 #if DEBUG 包裹）
grep -rn "^\s*print(\|^\s*debugPrint(\|^\s*NSLog(" \
  --include="*.swift" --include="*.m" . \
  | grep -v "#if DEBUG\|// DEBUG\|test\|Test"

# React Native：检测未被移除的 console.log
grep -rn "console\.log\|console\.debug\|console\.warn" \
  --include="*.js" --include="*.ts" --include="*.tsx" . \
  | grep -v "//\|test\|Test\|__tests__\|\.test\.\|\.spec\."
```

**修复建议**：
- Swift：用 `#if DEBUG ... #endif` 包裹，或使用 `OSLog`
- React Native：babel-plugin-transform-remove-console 在 production build 自动移除

---

### M2. 模糊的权限描述字符串

Guideline 5.1.1：NSUsageDescription 必须说明数据的具体用途，"App 需要访问相机"不够。

**常见问题示例**：
```
// ❌ 太模糊
NSCameraUsageDescription = "App needs camera access"
NSLocationWhenInUseUsageDescription = "For better experience"
NSMicrophoneUsageDescription = "To record audio"

// ✅ 合规（具体说明用途和受益）
NSCameraUsageDescription = "用于拍摄并识别植物，帮助您快速获取养护建议"
NSLocationWhenInUseUsageDescription = "用于查找您附近的花卉市场和园艺商店"
NSMicrophoneUsageDescription = "用于录制您的植物养护语音备忘"
```

**Shell 扫描命令**：
```bash
# 列出所有权限描述字符串
grep -A1 "UsageDescription" ios/*/Info.plist Info.plist 2>/dev/null

# 检测过于简短的描述（少于15个字符）
grep -A1 "UsageDescription" ios/*/Info.plist 2>/dev/null \
  | grep "<string>" \
  | awk '{if(length($0)<30) print NR": "$0" ← 可能太短"}'
```

---

### M3. IPv4 硬编码地址

硬编码 IP 意味着无法通过 DNS 灵活切换，且暗示可能绕过 ATS（App Transport Security）。

**Shell 扫描命令**：
```bash
# 扫描硬编码 IP（排除 localhost/回环地址）
grep -rEn "([0-9]{1,3}\.){3}[0-9]{1,3}" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" \
  --include="*.plist" --include="*.json" . \
  | grep -v "127\.0\.0\|0\.0\.0\.0\|255\.255\|192\.168\|10\.\|172\.\|//\|test\|Test"
```

---

### M4. 元数据含竞品品牌词

Guideline 2.3.7：不得在元数据中使用竞品名称做关键词堆砌或误导。常见误区：代码注释或字符串中包含 "Android"、"Google Play" 字样被截图提交。

**Shell 扫描命令**：
```bash
# 扫描不应出现在用户可见文字中的竞品词
grep -rn "Android\|Google Play\|Play Store\|Samsung\|Galaxy" \
  --include="*.strings" --include="*.json" --include="*.swift" --include="*.tsx" \
  --include="*.ts" . \
  | grep -v "//\|test\|Test\|README\|\.md"
```

---

## 快速全量扫描脚本

将以下命令保存为 `preflight-code-scan.sh`，在项目根目录执行：

```bash
#!/bin/bash
# Apple Review Preflight — 代码快速扫描脚本
# 使用方法：bash preflight-code-scan.sh | tee scan-report.txt

echo "=== CRITICAL: 私有 API ==="
grep -rn "NSSelectorFromString\|dlopen\|dlsym" --include="*.swift" --include="*.m" . | grep -v "//\|test"

echo ""
echo "=== CRITICAL: 动态执行 ==="
grep -rn "JPEngine\|JSPatch\|eval(" --include="*.swift" --include="*.m" --include="*.js" . | grep -v "//\|test"

echo ""
echo "=== CRITICAL: 外部支付 SDK ==="
grep -rn "Stripe\|PayPal\|Braintree" Podfile package.json 2>/dev/null

echo ""
echo "=== CRITICAL: 硬编码密钥 ==="
grep -rEn "(sk-proj-|AIzaSy|ghp_|AKIA)" --include="*.swift" --include="*.js" --include="*.ts" . | grep -v "test\|mock\|example"

echo ""
echo "=== HIGH: 广告SDK + ATT检测 ==="
HAS_AD_SDK=$(grep -rln "Firebase\|FacebookSDK\|GoogleMobileAds\|Adjust" Podfile package.json 2>/dev/null | wc -l)
HAS_ATT=$(grep -rln "ATTrackingManager\|requestTrackingAuthorization" --include="*.swift" . | wc -l)
echo "广告SDK引用: $HAS_AD_SDK 处 | ATT实现: $HAS_ATT 处"

echo ""
echo "=== HIGH: 账号注册 vs 删除 ==="
REG=$(grep -rln "signUp\|createAccount" --include="*.swift" --include="*.js" . | wc -l)
DEL=$(grep -rln "deleteAccount\|delete.*account" --include="*.swift" --include="*.js" . | wc -l)
echo "注册相关: $REG 文件 | 删除相关: $DEL 文件"

echo ""
echo "=== HIGH: 第三方OAuth + Apple登录 ==="
OAUTH=$(grep -rln "GIDSignIn\|FacebookLogin\|react-native-google-signin" --include="*.swift" --include="*.js" Podfile package.json 2>/dev/null | wc -l)
APPLE=$(grep -rln "ASAuthorizationAppleIDProvider\|SignInWithApple" --include="*.swift" --include="*.js" . | wc -l)
echo "第三方OAuth: $OAUTH 处 | Apple登录: $APPLE 处"

echo ""
echo "=== MEDIUM: console.log / print ==="
grep -rn "^\s*print(\|console\.log(" --include="*.swift" --include="*.js" --include="*.ts" . | grep -v "//\|test\|__tests__" | head -20

echo ""
echo "=== 扫描完成 ==="
```
