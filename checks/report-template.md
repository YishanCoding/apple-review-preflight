# report-template.md
# 来源：apple-review-preflight skill 内部规范
# 用途：提审前审计报告输出格式模板，供 skill 主入口生成标准化报告使用
# 说明：使用此模板时将 [占位符] 替换为实际内容，删除不适用的部分
# 维护：根据审核反馈持续优化报告格式

---

## 模板正文

---

## Apple Review Preflight Report — [App名] v[版本号]

**App 类型**：[工具 / 社交 / 电商 / 健康 / 内容订阅 / 游戏 / 企业内部 / 儿童]
**Bundle ID**：[com.company.appname]
**分发地区**：[全球 / 中国大陆 / 美国 / 指定地区列表]
**技术栈**：[Swift + UIKit / Swift + SwiftUI / React Native + Expo / React Native CLI / Flutter / Capacitor]
**检查日期**：[YYYY-MM-DD]
**检查人**：[检查者姓名或 "apple-review-preflight skill"]
**对应 Guidelines 版本**：Apple App Store Review Guidelines 2026-02-06

---

### 🔴 立即阻断（CRITICAL）

> 以下问题必须在提交前全部修复，否则必然被拒。

- **[GUIDELINE 2.5.1] 私有 API 调用**
  - 证据：`src/utils/DeviceInfo.swift:42` 调用了 `UIApplication.shared._statusBar`
  - 修复：替换为公开 API `UIApplication.shared.statusBarFrame`（iOS 13+）或使用 `UIWindowScene` 获取状态栏高度

- **[GUIDELINE 2.5.2] 动态代码执行**
  - 证据：`package.json` 包含 `react-native-code-push ^7.0.5`，且 `App.js:15` 配置了 `updateDialog: true`
  - 修复：移除 CodePush 或改为 `InstallMode.ON_NEXT_RESTART` 并在 Review Notes 中向审核员说明

- **[GUIDELINE 3.1.1] 数字商品外部支付**
  - 证据：`src/screens/Upgrade.tsx:88` 调用 Stripe SDK 购买"高级会员"（数字服务）
  - 修复：使用 `react-native-iap` + StoreKit，移除 Stripe 相关调用

- **[GUIDELINE 5.1.1(v)] 有账号注册无账号删除**
  - 证据：`src/auth/Register.tsx` 存在注册功能，全项目无 `deleteAccount`、`注销账号` 相关实现
  - 修复：在账号设置页新增"删除账号"入口，后端实现数据清除逻辑，并在 Review Notes 中说明位置

---

### 🟡 高风险（HIGH）

> 以下问题大概率导致被拒，强烈建议提审前修复。

- **[GUIDELINE 5.1.2 / ATT] 引入广告 SDK 但缺少 ATT 权限请求**
  - 证据：`Podfile` 包含 `Firebase/Analytics` 和 `Facebook-iOS-SDK`，但全项目无 `ATTrackingManager` 调用
  - 修复：在用户完成引导页后调用 `ATTrackingManager.requestTrackingAuthorization`；Info.plist 添加 `NSUserTrackingUsageDescription`

- **[GUIDELINE 4.8] 第三方 OAuth 但缺少 Sign in with Apple**
  - 证据：`LoginScreen.swift` 实现了 Google 登录，但无 Apple 登录按钮
  - 修复：添加 `ASAuthorizationAppleIDProvider` 实现；Apple 登录按钮必须与其他登录方式同等显眼

- **[GUIDELINE 2.5.4] 后台模式声明与功能不符**
  - 证据：`Info.plist` 声明了 `UIBackgroundModes: [audio]`，但代码中的音频为静音（volume = 0.0），疑为 keep-alive 滥用
  - 修复：移除 audio 后台模式声明，改用 `BGAppRefreshTask` 满足后台刷新需求

---

### 🟠 中等风险（MEDIUM）

> 以下问题可能触发审核员追问或概率性拒绝，建议修复。

- **[GUIDELINE 5.1.1] 权限描述字符串过于模糊**
  - 证据：`NSCameraUsageDescription = "App needs camera"` — 未说明具体用途
  - 修复：改为 `"用于拍摄植物照片，通过 AI 识别获取养护建议"`

- **[GUIDELINE 5.1.1 / PrivacyInfo] 未声明 Required Reason API**
  - 证据：代码中使用了 `UserDefaults`（CA92.1 理由）和 `ProcessInfo.systemUptime`（35F9.1 理由），但 `PrivacyInfo.xcprivacy` 中无对应声明
  - 修复：在 `PrivacyInfo.xcprivacy` 的 `NSPrivacyAccessedAPITypes` 中添加 `NSPrivacyAccessedAPICategoryUserDefaults`（CA92.1）和 `NSPrivacyAccessedAPICategorySystemBootTime`（35F9.1）

- **[GUIDELINE 5.1.1] 隐私五处不一致**
  - 证据：App Store Connect Nutrition Labels 未勾选"崩溃数据"，但 `Podfile` 包含 Firebase Crashlytics
  - 修复：登录 App Store Connect，在 App Privacy 中补充勾选"崩溃数据"（诊断类）

- **[GUIDELINE 2.3.7] 生产代码含竞品词**
  - 证据：`src/onboarding/Welcome.tsx:23` 文字中包含 "比 Android 版更流畅"
  - 修复：修改文案，不在用户可见文字中出现竞品名称

- **生产代码残留 console.log**
  - 证据：`src/api/client.ts` 含 15 处 `console.log`，部分打印了用户 token
  - 修复：安装 `babel-plugin-transform-remove-console` 或包裹 `if (__DEV__)` 判断

---

### ✅ 已合规（PASSED）

> 以下检查项已通过，无需修改。

- **[GUIDELINE 3.1.1] 实物商品支付**：App 内使用 Stripe 仅用于实物商品（鲜花配送），数字服务已使用 IAP ✅
- **[GUIDELINE 4.8] Sign in with Apple**：已实现，与 Google 登录并列显示 ✅
- **[GUIDELINE 5.1.1] 账号删除功能**：`设置 → 账号 → 删除账号` 路径存在，后端实现已确认 ✅
- **[GUIDELINE 2.5.1] 私有 API**：全项目扫描未发现私有 API 调用 ✅
- **[GUIDELINE 2.5.2] 动态代码执行**：无 JSPatch、eval 等动态执行机制 ✅
- **PrivacyInfo.xcprivacy 存在**：文件已创建并包含在 Xcode target 中 ✅
- **ATT 框架实现**：`AppDelegate.swift` 中在主界面加载后调用 ATT，时机合理 ✅
- **硬编码密钥**：扫描未发现明文密钥，API Key 通过 Info.plist + 后端代理管理 ✅

---

### ⚠️ 未能验证（MISSING INPUTS）

> 以下项目因缺少必要信息无法完成检查，需人工补充确认。

- **App Store Connect Nutrition Labels**：未提供 App Store Connect 截图，无法验证与代码实际行为的一致性
  - 需要：登录 App Store Connect → App Privacy 截图

- **第三方 SDK PrivacyInfo.xcprivacy 覆盖率**：未运行 `pod install`，无法扫描 Pods 目录中的 SDK 隐私声明
  - 需要：在已 `pod install` 的环境下运行 `find Pods/ -name "PrivacyInfo.xcprivacy"`

- **测试账号可用性**：未验证 Review Notes 中提供的测试账号是否能正常登录并触发权限弹窗
  - 需要：用审核员视角走一遍完整流程

- **In-App Purchase 沙盒测试**：未确认 IAP 沙盒环境是否正常，审核员会测试购买流程
  - 需要：使用 Sandbox 账号完整测试一次购买+恢复购买流程

---

### 📋 建议的 App Review Notes

> 以下文本可直接复制到 App Store Connect → 版本信息 → App 审核信息 → 备注

```
【测试账号】
邮箱：reviewer_test@yourapp.com
密码：ReviewTest2026!
说明：该账号已开通全部付费功能，无需购买即可体验完整内容。
首次登录如需邮箱验证，验证码将发送至上述邮箱（或请联系 support@yourapp.com 获取）。

【核心功能路径】
1. 打开 App → 完成引导（3步）→ 进入主界面
2. 相机识别：首页右下角"拍照识别"按钮 → 请求相机权限 → 拍植物照片 → 获取结果
3. 删除账号：设置（右上角齿轮）→ 账号管理 → 删除账号

【权限说明】
- 相机：用于 AI 植物识别功能，不在后台使用，不上传原始图片
- 位置（仅前台）：用于查找附近园艺商店，用户点击"附近"时触发，拒绝后功能降级为手动搜索
- 追踪（ATT）：完成注册后弹出，用于向您展示更相关的园艺内容推荐，拒绝后全功能正常使用

【支付说明】
- App 内数字服务（高级会员）使用 Apple In-App Purchase
- 如 App 内有实物商品购买（如种子、工具），该部分使用第三方支付（Stripe），不涉及数字商品

【特殊说明】
- App 支持 iOS 16.0+
- 首次启动需要网络连接（加载内容），离线状态下可查看已缓存内容
```

---

## 风险摘要

| 优先级 | 数量 | 项目 |
|--------|------|------|
| 🔴 CRITICAL | [N] | [列出标题] |
| 🟡 HIGH | [N] | [列出标题] |
| 🟠 MEDIUM | [N] | [列出标题] |
| ✅ PASSED | [N] | — |
| ⚠️ 未验证 | [N] | — |

**提审建议**：
- [ ] 所有 CRITICAL 已修复 → 方可提交
- [ ] HIGH 建议修复（可以先提交，但大概率被拒）
- [ ] MEDIUM 可接受风险后提交，建议在 Review Notes 中主动说明

---

## 填写说明（使用模板时参考）

**App 类型**填写参考：
- 工具：非游戏、非订阅内容、功能型 App
- 内容订阅：提供视频/音频/文章等内容，有订阅制付费
- 儿童：目标用户含13岁以下，受 COPPA/儿童分类限制，需特别注意

**技术栈**识别：
- 看项目根目录：有 `Podfile` → 原生/RN；有 `pubspec.yaml` → Flutter；有 `capacitor.config.ts` → Capacitor
- 看 `package.json`：有 `react-native` → React Native；有 `expo` → Expo
