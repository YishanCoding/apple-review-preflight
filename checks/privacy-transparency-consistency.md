# privacy-transparency-consistency.md
# 来源：Apple App Store Review Guidelines 2026-02-06 + Apple Privacy Nutrition Labels 要求
# 用途：apple-review-preflight skill 隐私五处一致性检查（P0新增项）
# 重要：这是 2023 年后新增的高频拒绝原因，审核员会交叉比对五处声明
# 维护：每次 Apple 更新隐私要求后同步更新

---

## 概述

Apple 要求 App 的隐私声明在以下**五处**完全一致，任何一处遗漏或矛盾都可能导致拒绝。
这是 Guideline 5.1.1（数据收集与存储）和 5.1.2（数据使用与共享）的核心执行机制。

**五处必须对齐**：
1. PrivacyInfo.xcprivacy（代码层声明）
2. App Store Connect Privacy Nutrition Labels（商店展示）
3. Info.plist purpose strings（系统权限弹窗）
4. App Review Notes（向审核员的说明）
5. 实际代码的数据收集行为（运行时行为）

---

## 第一处：PrivacyInfo.xcprivacy

**作用**：Xcode 15+ 引入，声明 App 及其所有依赖 SDK 使用的 Required Reason API 和隐私数据类型。
**位置**：主 App target 和每个独立 bundle target（如 App Clip / Widget / Activity / Share Extension）都可能需要各自的 `PrivacyInfo.xcprivacy`；每个 SDK 也需要自己的 PrivacyInfo.xcprivacy。

**文件结构**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- 声明使用的隐私数据类型 -->
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeEmailAddress</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <true/>  <!-- 是否与用户身份关联 -->
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>  <!-- 是否用于追踪 -->
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>

    <!-- 声明使用的 Required Reason API（详见 required-reason-api-scan.md）-->
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>  <!-- 理由代码，详见 required-reason-api-scan.md -->
            </array>
        </dict>
    </array>

    <!-- 是否追踪用户 -->
    <key>NSPrivacyTracking</key>
    <false/>

    <!-- 追踪域名（如有追踪则必填）-->
    <key>NSPrivacyTrackingDomains</key>
    <array/>
</dict>
</plist>
```

**检查方法**：
```bash
# 确认文件存在
find . -name "PrivacyInfo.xcprivacy" -not -path "*/Pods/*" -not -path "*/node_modules/*"

# 查看内容
cat PrivacyInfo.xcprivacy 2>/dev/null || find . -name "PrivacyInfo.xcprivacy" -exec cat {} \;

# 检查是否被正确包含在 Xcode target 中（需在 Xcode 确认）
grep -rn "PrivacyInfo" *.xcodeproj/project.pbxproj 2>/dev/null | head -5
```

**常见不一致示例**：
- PrivacyInfo.xcprivacy 未声明 Email，但代码实际收集邮箱用于账号创建
- PrivacyInfo.xcprivacy 声明 `NSPrivacyTracking = false`，但实际接入了 Adjust 且未做 ATT 判断
- 主 App 有 manifest，但 Widget / App Clip target 没有

---

## 第二处：App Store Connect Privacy Nutrition Labels

**作用**：在 App Store 产品页向用户展示数据收集信息，审核员也会对照此处。
**位置**：App Store Connect → 你的 App → App 隐私

**数据类型分类**（需逐一勾选）：
```
联系信息          → 姓名、邮件、电话、实际地址
健康与健身         → 健康数据、健身数据
财务信息          → 支付信息、信用评分、其他财务信息
位置             → 精确位置、粗略位置
敏感信息          → 种族、宗教、性取向
联系人           → 通讯录
用户内容          → 邮件或短信、照片或视频、语音/声音、其他用户内容
浏览历史          → 浏览记录
搜索历史          → 搜索记录
标识符           → 用户 ID、设备 ID
购买             → 购买记录
使用数据          → 产品互动、广告数据、崩溃数据
诊断             → 崩溃数据、性能数据、其他诊断数据
其他数据          → 其他
```

**每类数据需填写**：
- 是否与用户身份关联（Linked to You）
- 是否用于追踪（Used to Track You）
- 使用目的（App 功能、分析、广告等）

**检查方法**：
- 登录 App Store Connect，截图当前 Privacy Nutrition Labels 设置
- 对照 PrivacyInfo.xcprivacy 逐项比对
- 对照代码中实际的数据收集点逐项比对

**常见不一致示例**：
```
❌ Nutrition Labels 未勾选"崩溃数据"，但 Podfile 包含 Firebase Crashlytics
❌ Nutrition Labels 声明不收集位置，但 Info.plist 有 NSLocationWhenInUseUsageDescription
❌ Nutrition Labels 勾选了"广告"目的，但 PrivacyInfo.xcprivacy 的 NSPrivacyTracking = false
```

---

## 第三处：Info.plist Purpose Strings

**作用**：系统权限弹窗向用户展示的说明文字，必须与实际用途一致。
**位置**：`ios/YourApp/Info.plist` 或 React Native 项目的 `ios/` 目录下

**所有权限描述字符串**：
```xml
<!-- 相机 -->
<key>NSCameraUsageDescription</key>
<string>用于拍摄植物照片以获取 AI 识别结果</string>

<!-- 麦克风 -->
<key>NSMicrophoneUsageDescription</key>
<string>用于录制语音备忘，方便您随时记录养护心得</string>

<!-- 精确位置 -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>用于查找您附近的园艺商店和植物活动</string>

<!-- 后台位置（需额外申请）-->
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>用于在您靠近植物市场时发送提醒通知</string>

<!-- 照片库读取 -->
<key>NSPhotoLibraryUsageDescription</key>
<string>用于从相册选取植物照片进行识别</string>

<!-- 照片库写入 -->
<key>NSPhotoLibraryAddUsageDescription</key>
<string>用于将识别结果和养护记录保存至相册</string>

<!-- 通讯录 -->
<key>NSContactsUsageDescription</key>
<string>用于邀请好友加入您的植物社区</string>

<!-- 追踪（ATT）-->
<key>NSUserTrackingUsageDescription</key>
<string>允许追踪有助于我们向您展示更相关的内容和广告</string>

<!-- 面容ID / 触控ID -->
<key>NSFaceIDUsageDescription</key>
<string>使用面容 ID 快速安全地登录账号</string>

<!-- 蓝牙 -->
<key>NSBluetoothAlwaysUsageDescription</key>
<string>用于连接您的智能植物检测设备</string>

<!-- 健康 -->
<key>NSHealthShareUsageDescription</key>
<string>用于读取健康数据，提供个性化养护建议</string>

<!-- 日历 -->
<key>NSCalendarsUsageDescription</key>
<string>用于将浇水和施肥提醒添加至日历</string>
```

**检查方法**：
```bash
# 列出所有权限描述
grep -B1 -A1 "UsageDescription" ios/*/Info.plist 2>/dev/null

# React Native：
grep -B1 -A1 "UsageDescription" ios/YourApp/Info.plist

# 检查是否有空描述
grep -A1 "UsageDescription" ios/*/Info.plist 2>/dev/null | grep "<string></string>"

# 检查描述字符串长度（太短通常不够具体）
python3 -c "
import plistlib, sys
with open('ios/YourApp/Info.plist', 'rb') as f:
    plist = plistlib.load(f)
for k, v in plist.items():
    if 'UsageDescription' in k:
        print(f'{k}: {len(str(v))} chars -> {v}')
" 2>/dev/null
```

**常见不一致示例**：
```
❌ Info.plist 有 NSLocationAlwaysUsageDescription，但 Nutrition Labels 只勾选了"粗略位置"
❌ Info.plist 有 NSCameraUsageDescription，但 PrivacyInfo.xcprivacy 未声明相机数据类型
❌ 权限描述说"用于增强体验"，与实际功能完全无关
```

---

## 第四处：App Review Notes（审核说明）

**作用**：向 Apple 审核员直接说明特殊功能、权限用途、测试账号等信息。
**位置**：App Store Connect → 版本信息 → App 审核信息 → 备注

**必须在 Review Notes 中说明的情况**：
```
1. 使用了相机/麦克风/位置等敏感权限 → 说明具体功能场景
2. App 有账号系统 → 提供测试账号（邮箱+密码）
3. App 涉及特定行业（医疗、金融、儿童等）→ 说明合规依据
4. App 有 Demo 模式或特殊进入方式 → 说明操作步骤
5. 使用了后台模式 → 说明具体用途（见 background-modes-scan.md）
6. App 内有 WebView 加载外部内容 → 说明内容来源和安全措施
7. 使用了追踪 SDK → 说明 ATT 弹出时机
```

**Review Notes 模板**：
```
测试账号：
- 邮箱：reviewer@example.com
- 密码：TestAccount2026!
- 注意：首次登录会收到验证码邮件，测试账号已预设为跳过验证码

权限说明：
- 相机：用于 [具体功能]，审核时可在 [页面名称] 找到入口
- 位置：仅在用户主动点击"查找附近"时请求，不在后台持续使用
- 追踪（ATT）：在用户完成注册后弹出，拒绝后功能不受影响

特殊说明：
- [其他需要说明的内容]
```

**检查方法**（对照其他四处验证 Review Notes 是否一致）：
```
✅ 每个 Info.plist 权限描述 → 对应在 Review Notes 中有场景说明
✅ Review Notes 提到的功能 → 对应在 PrivacyInfo.xcprivacy 和 Nutrition Labels 中有声明
✅ Review Notes 提到"不追踪" → 对应 NSPrivacyTracking = false 且无追踪 SDK
```

**常见不一致示例**：
```
❌ Review Notes 说"App 不收集位置"，但 Info.plist 有 NSLocationWhenInUseUsageDescription
❌ Review Notes 说"仅用于账号功能"，但 Nutrition Labels 勾选了"广告"目的
❌ Review Notes 提供了测试账号，但该账号没有触发权限请求的功能入口
```

---

## 第五处：实际代码的数据收集行为

**作用**：这是审核员动态运行 App 时观察到的真实行为，也是其他四处声明的"原始真相"。

**关键数据收集点扫描**：
```bash
# 检测位置数据收集
grep -rn "CLLocationManager\|requestLocation\|startUpdatingLocation\|useractivity.*location" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" .

# 检测相机使用
grep -rn "AVCaptureSession\|AVCaptureDevice\|CameraRoll\|ImagePicker" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" .

# 检测联系人访问
grep -rn "CNContactStore\|ABAddressBook\|Contacts.framework" \
  --include="*.swift" --include="*.m" .

# 检测设备标识符
grep -rn "identifierForVendor\|advertisingIdentifier\|deviceToken\|pushToken" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" .

# 检测第三方分析 SDK 的数据上报
grep -rn "Analytics.logEvent\|Mixpanel.sharedInstance\|Amplitude\|Segment" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" .

# 检测健康数据访问
grep -rn "HKHealthStore\|HKQuery\|requestAuthorization.*health" \
  --include="*.swift" --include="*.m" .
```

---

## 五处一致性快速自查矩阵

| 数据类型 | PrivacyInfo.xcprivacy | Nutrition Labels | Info.plist | Review Notes | 代码行为 |
|---------|----------------------|-----------------|-----------|-------------|---------|
| 邮箱地址 | □ 已声明 | □ 已勾选 | □ N/A | □ 已说明 | □ 实际使用 |
| 精确位置 | □ 已声明 | □ 已勾选 | □ NSLocationWhenInUse | □ 已说明 | □ 实际使用 |
| 相机 | □ 已声明 | □ 已勾选 | □ NSCameraUsage | □ 已说明 | □ 实际使用 |
| 设备ID | □ 已声明 | □ 已勾选 | □ N/A | □ 已说明 | □ 实际使用 |
| 崩溃数据 | □ 已声明 | □ 已勾选 | □ N/A | □ 已说明 | □ SDK引入 |
| 追踪 | □ NSPrivacyTracking | □ 已勾选 | □ NSUserTracking | □ 已说明 | □ ATT实现 |

**使用方法**：每行所有格子都打勾 = 该数据类型一致性通过。有任何空格 = 存在不一致，提审前必须修复。

---

## 快速一致性检查命令

```bash
#!/bin/bash
# 五处一致性快速检查脚本
echo "=== 检查 PrivacyInfo.xcprivacy ==="
PRIVACY_INFO=$(find . -name "PrivacyInfo.xcprivacy" -not -path "*/Pods/*" -not -path "*/node_modules/*" 2>/dev/null)
if [ -z "$PRIVACY_INFO" ]; then
  echo "❌ 未找到 PrivacyInfo.xcprivacy"
else
  echo "$PRIVACY_INFO" | while IFS= read -r privacy_file; do
    echo "✅ 找到: $privacy_file"
    count=$(grep -c "NSPrivacyCollectedDataType" "$privacy_file" 2>/dev/null || true)
    echo "  数据类型声明: $count"
  done
fi

echo ""
echo "=== 检查 Info.plist 权限字符串 ==="
find . -name "Info.plist" -not -path "*/Pods/*" -exec grep -l "UsageDescription" {} \; 2>/dev/null | while read f; do
  echo "文件: $f"
  grep "UsageDescription" "$f" | sed 's/<[^>]*>//g' | sed 's/^\s*/  - /'
done

echo ""
echo "=== 检查代码中实际的数据采集 ==="
echo "位置: $(grep -rln "CLLocationManager\|startUpdatingLocation" --include="*.swift" --include="*.js" . 2>/dev/null | wc -l) 个文件"
echo "相机: $(grep -rln "AVCaptureSession\|ImagePicker" --include="*.swift" --include="*.js" . 2>/dev/null | wc -l) 个文件"
echo "联系人: $(grep -rln "CNContactStore" --include="*.swift" . 2>/dev/null | wc -l) 个文件"
echo "设备ID: $(grep -rln "identifierForVendor\|advertisingIdentifier" --include="*.swift" . 2>/dev/null | wc -l) 个文件"
echo "分析SDK: $(grep -rln "Analytics\|Mixpanel\|Amplitude\|Segment" --include="*.swift" --include="*.js" . 2>/dev/null | wc -l) 个文件"

echo ""
echo "=== Nutrition Labels 和 Review Notes 需手动对照 App Store Connect ==="
echo "请登录 App Store Connect 确认 Privacy Nutrition Labels 与以上扫描结果一致"
```
