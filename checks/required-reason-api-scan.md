# required-reason-api-scan.md
# 来源：Apple App Store Review Guidelines 2026-02-06 + Apple Required Reason API 官方文档
# 参考：https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api
# 用途：apple-review-preflight skill Required Reason API 扫描指南
# 背景：2024年5月1日起强制要求，未声明原因的 API 使用将导致拒绝（ITMS-91053）
# 维护：每次 Apple 更新 Required Reason API 列表后同步更新

---

## 概述

Apple 将某些可能被滥用于设备指纹识别的 API 归类为 **Required Reason API**。
使用这些 API 时，必须在 `PrivacyInfo.xcprivacy` 中声明使用原因代码。

**关键原则**：
- App 本身的 PrivacyInfo.xcprivacy 必须覆盖 App 代码中的用法
- 每个独立 bundle target（如 App Clip / Widget / Activity / Share Extension）都应分别确认自己的 PrivacyInfo.xcprivacy 覆盖范围
- **第三方 SDK 也必须各自提供 PrivacyInfo.xcprivacy**（SDK 作者的责任）
- 如果 SDK 没有提供 PrivacyInfo.xcprivacy，你需要在你的 App 的 PrivacyInfo.xcprivacy 中代为声明

---

## API 类别一览

### 类别1：File Timestamp API（文件时间戳）

**涉及 API**：
- `NSFileManager`：`attributesOfItem(atPath:)`、`attributesOfFileSystem(forPath:)`
- `NSFileVersion`：creationDate、modificationDate
- `NSMetadataItem`：NSMetadataItemFSCreationDateKey、NSMetadataItemFSContentChangeDateKey
- POSIX：`stat()`、`fstat()`、`lstat()`、`getattrlist()`、`getattrlistbulk()`
- `CFURLCopyResourcePropertyForKey`（kCFURLContentModificationDateKey 等）

**合法原因代码**：
| 代码 | 适用场景 |
|------|---------|
| `DDA9.1` | App 的核心功能需要展示文件时间戳给用户 |
| `C617.1` | 仅访问 App 自身目录内的文件时间戳（App 沙盒内）|
| `3B52.1` | 访问用户授权选择的文件的时间戳（如通过 Document Picker）|
| `0A2A.1` | 第三方 SDK：记录或发送诊断数据给开发者（非追踪）|

**扫描命令**：
```bash
grep -rn "attributesOfItem\|NSFileCreationDate\|NSFileModificationDate\|getattrlist\|stat(" \
  --include="*.swift" --include="*.m" --include="*.c" . \
  | grep -v "//\|test\|Test\|Pods"
```

---

### 类别2：System Boot Time API（系统启动时间）

**涉及 API**：
- `systemUptime`（ProcessInfo.processInfo.systemUptime）
- `mach_absolute_time()`
- `sysctl()` 读取 `kern.boottime`
- `NSProcessInfo.systemUptime`
- `clock_gettime(CLOCK_MONOTONIC, ...)`

**合法原因代码**：
| 代码 | 适用场景 |
|------|---------|
| `35F9.1` | 计算 App 内的时间间隔（如动画时长、会话时长）|
| `8FFB.1` | 测量性能或响应时间（不上报到服务器）|
| `3D61.1` | 用于 Boottime 的回退计算逻辑 |

**扫描命令**：
```bash
grep -rn "systemUptime\|mach_absolute_time\|kern\.boottime\|CLOCK_MONOTONIC" \
  --include="*.swift" --include="*.m" --include="*.c" . \
  | grep -v "//\|test\|Test\|Pods"
```

---

### 类别3：Disk Space API（磁盘空间）

**涉及 API**：
- `NSFileManager.attributesOfFileSystem(forPath:)` 读取 `NSFileSystemFreeSize`、`NSFileSystemSize`
- `volumeAvailableCapacityForImportantUsage`
- `volumeAvailableCapacityForOpportunisticUsage`
- `URLResourceValues.volumeTotalCapacity`

**合法原因代码**：
| 代码 | 适用场景 |
|------|---------|
| `85F4.1` | 在下载大文件前检查是否有足够空间 |
| `E174.1` | 管理 App 缓存，当磁盘空间不足时清理 |

**扫描命令**：
```bash
grep -rn "NSFileSystemFreeSize\|NSFileSystemSize\|volumeAvailableCapacity\|volumeTotalCapacity\|attributesOfFileSystem" \
  --include="*.swift" --include="*.m" . \
  | grep -v "//\|test\|Test\|Pods"
```

---

### 类别4：Active Keyboard APIs（活动键盘）

**涉及 API**：
- `UITextInputMode.activeInputModes`

**合法原因代码**：
| 代码 | 适用场景 |
|------|---------|
| `54BD.1` | 根据当前键盘语言定制 App 语言输入体验 |

**说明**：此 API 容易被用于推断用户地区/语言偏好做设备指纹，因此受限制。

**扫描命令**：
```bash
grep -rn "activeInputModes\|UITextInputMode" \
  --include="*.swift" --include="*.m" . \
  | grep -v "//\|test\|Test\|Pods"
```

---

### 类别5：User Defaults APIs（用户默认值）

**涉及 API**：
- `UserDefaults`（任何 read/write 操作）
- `NSUserDefaults`
- React Native：`AsyncStorage`（底层使用 NSUserDefaults）
- Flutter：`shared_preferences`（底层使用 NSUserDefaults）

**合法原因代码**：
| 代码 | 适用场景 |
|------|---------|
| `CA92.1` | 存储 App 本身的用户偏好设置（如主题、语言）|
| `1C8F.1` | 读取 App Group 共享的 UserDefaults |
| `C56D.1` | 读取由 MDM 或系统设置的 managed defaults |
| `AC6B.1` | 在 App 和 Extension 之间共享数据 |

**重要提示**：这是最常见的遗漏项，因为几乎所有 App 都使用 UserDefaults，但很多开发者忘记声明。

**扫描命令**：
```bash
# Swift
grep -rn "UserDefaults\|NSUserDefaults" \
  --include="*.swift" --include="*.m" . \
  | grep -v "//\|test\|Test\|Pods" | head -30

# React Native
grep -rn "AsyncStorage" \
  --include="*.js" --include="*.ts" --include="*.tsx" . \
  | grep -v "//\|test\|Test\|node_modules" | head -20
```

---

## 第三方 SDK 的责任

Apple 要求每个 SDK 提供自己的 PrivacyInfo.xcprivacy。以下是常见 SDK 的现状：

| SDK | PrivacyInfo.xcprivacy | 备注 |
|----|----------------------|------|
| Firebase iOS SDK 10.18+ | ✅ 已提供 | 需更新到最新版本 |
| Facebook SDK 16.1+ | ✅ 已提供 | 需更新 |
| Adjust SDK 4.38.1+ | ✅ 已提供 | 需更新 |
| AppsFlyer 6.12.2+ | ✅ 已提供 | 需更新 |
| Amplitude 8.16+ | ✅ 已提供 | 需更新 |
| Crashlytics（Firebase子集）| ✅ 包含在 Firebase 内 | — |
| 旧版本或冷门 SDK | ❌ 可能缺失 | 需手动在 App PrivacyInfo.xcprivacy 补充 |

**检查 SDK 是否提供 PrivacyInfo.xcprivacy**：
```bash
# CocoaPods 项目：检查 Pods 目录
find Pods/ -name "PrivacyInfo.xcprivacy" 2>/dev/null | sort

# 对比 Podfile.lock 中的 SDK 列表
cat Podfile.lock | grep -E "^\s+-" | sed 's/.*- //' | sed 's/ .*//'

# SPM 项目：检查 checkouts 目录
find .build/checkouts -name "PrivacyInfo.xcprivacy" 2>/dev/null | sort

# npm/yarn 项目（React Native）
find node_modules -name "PrivacyInfo.xcprivacy" 2>/dev/null | sort
```

---

## 在 PrivacyInfo.xcprivacy 中正确填写

**完整填写示例**（覆盖多个 API 类别）：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>

        <!-- 文件时间戳 API -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>  <!-- 仅访问 App 自身目录内的文件时间戳 -->
            </array>
        </dict>

        <!-- 系统启动时间 API -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategorySystemBootTime</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>35F9.1</string>  <!-- 计算 App 内时间间隔 -->
            </array>
        </dict>

        <!-- 磁盘空间 API -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryDiskSpace</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>85F4.1</string>  <!-- 下载前检查空间 -->
            </array>
        </dict>

        <!-- 活动键盘 API -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryActiveKeyboards</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>54BD.1</string>  <!-- 定制输入体验 -->
            </array>
        </dict>

        <!-- User Defaults API -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>  <!-- 存储用户偏好设置 -->
            </array>
        </dict>

    </array>
</dict>
</plist>
```

---

## 全量快速扫描脚本

```bash
#!/bin/bash
# Required Reason API 快速扫描脚本
# 使用方法：bash required-reason-scan.sh

echo "=== Required Reason API 使用检测 ==="
echo ""

echo "【文件时间戳 API】"
RESULT=$(grep -rn "attributesOfItem\|NSFileCreationDate\|NSFileModificationDate\|getattrlist\|fstat\b" \
  --include="*.swift" --include="*.m" --include="*.c" . \
  --exclude-dir="Pods" --exclude-dir="node_modules" --exclude-dir=".build" \
  --exclude-dir="Tests" --exclude-dir="test" 2>/dev/null | grep -v "//")
[ -n "$RESULT" ] && echo "$RESULT" || echo "  未检测到使用"

echo ""
echo "【系统启动时间 API】"
RESULT=$(grep -rn "systemUptime\|mach_absolute_time\|kern\.boottime\|CLOCK_MONOTONIC" \
  --include="*.swift" --include="*.m" --include="*.c" . \
  --exclude-dir="Pods" --exclude-dir="node_modules" --exclude-dir=".build" \
  --exclude-dir="Tests" --exclude-dir="test" 2>/dev/null | grep -v "//")
[ -n "$RESULT" ] && echo "$RESULT" || echo "  未检测到使用"

echo ""
echo "【磁盘空间 API】"
RESULT=$(grep -rn "NSFileSystemFreeSize\|volumeAvailableCapacity\|volumeTotalCapacity\|attributesOfFileSystem" \
  --include="*.swift" --include="*.m" . \
  --exclude-dir="Pods" --exclude-dir="node_modules" --exclude-dir=".build" \
  --exclude-dir="Tests" --exclude-dir="test" 2>/dev/null | grep -v "//")
[ -n "$RESULT" ] && echo "$RESULT" || echo "  未检测到使用"

echo ""
echo "【活动键盘 API】"
RESULT=$(grep -rn "activeInputModes\|UITextInputMode" \
  --include="*.swift" --include="*.m" . \
  --exclude-dir="Pods" --exclude-dir="node_modules" --exclude-dir=".build" \
  --exclude-dir="Tests" --exclude-dir="test" 2>/dev/null | grep -v "//")
[ -n "$RESULT" ] && echo "$RESULT" || echo "  未检测到使用"

echo ""
echo "【User Defaults API】"
RESULT=$(grep -rn "\bUserDefaults\b\|NSUserDefaults\|AsyncStorage" \
  --include="*.swift" --include="*.m" --include="*.js" --include="*.ts" . \
  --exclude-dir="Pods" --exclude-dir="node_modules" --exclude-dir=".build" \
  --exclude-dir="Tests" --exclude-dir="test" 2>/dev/null | grep -v "//" | head -5)
[ -n "$RESULT" ] && echo "$RESULT" && echo "  ...（仅显示前5条）" || echo "  未检测到使用"

echo ""
echo "=== PrivacyInfo.xcprivacy 检查 ==="
PRIVACY_FILES=$(find . -name "PrivacyInfo.xcprivacy" -not -path "*/Pods/*" -not -path "*/node_modules/*" 2>/dev/null)
if [ -z "$PRIVACY_FILES" ]; then
  echo "❌ 未找到 PrivacyInfo.xcprivacy — 必须创建！"
else
  echo "✅ 找到以下 manifest:"
  printf "%s\n" "$PRIVACY_FILES"
  FIRST_PRIVACY_FILE=$(printf "%s\n" "$PRIVACY_FILES" | head -1)
  DECLARED=$(grep -c "NSPrivacyAccessedAPIType>" "$FIRST_PRIVACY_FILE" 2>/dev/null)
  echo "   首个 manifest 已声明 API 类别数：$DECLARED"
  echo "   提醒：如存在 App Clip / Widget / Activity / Extension，请逐个 target 检查"
fi

echo ""
echo "=== SDK PrivacyInfo.xcprivacy 覆盖情况 ==="
SDK_COUNT=0
for dir in Pods/ node_modules/ .build/checkouts/; do
  if [ -d "$dir" ]; then
    count=$(find "$dir" -name "PrivacyInfo.xcprivacy" 2>/dev/null | wc -l)
    SDK_COUNT=$((SDK_COUNT + count))
  fi
done
echo "第三方 SDK 中的 PrivacyInfo.xcprivacy 数量：$SDK_COUNT"
for dir in Pods/ node_modules/ .build/checkouts/; do
  [ -d "$dir" ] && find "$dir" -name "PrivacyInfo.xcprivacy" 2>/dev/null | head -10
done
```
