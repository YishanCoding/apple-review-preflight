# background-modes-scan.md
# 来源：Apple App Store Review Guidelines 2026-02-06 §2.5.4 + Background Execution 官方文档
# 用途：apple-review-preflight skill 后台模式滥用检测
# 背景：2.5.4 是 Apple 拒绝率较高的条款，审核员会动态测试后台行为
# 维护：每次 Apple 更新后台模式政策后同步更新

---

## 概述

Guideline 2.5.4 要求 App 不得使用后台模式进行与声明功能无关的操作。
常见违规：用 `audio` 模式做后台保活（keep-alive）、用 `location` 模式持续采集位置用于非导航功能。

**审核员测试手段**：
1. 切换到后台，观察电量消耗和网络活动
2. 检查 Info.plist 中的 UIBackgroundModes 声明
3. 对比 App 功能，判断声明是否合理

---

## 所有后台模式详解

### audio — 后台音频播放

**Info.plist 值**：`audio`
**合法用途**：
- 音乐/播客播放器（如 Spotify、Apple Music 类）
- 录音 App（后台继续录制）
- 语音通话（VoIP 辅助音频）
- 冥想/白噪音 App（持续播放）

**常见滥用**：
```xml
<!-- ❌ 高危：用静音音频做 keep-alive，保持 App 后台运行 -->
<!-- 实质：播放一个0分贝的音频流，防止系统暂停 App -->
```
```swift
// ❌ 滥用示例：后台保活
let session = AVAudioSession.sharedInstance()
try? session.setCategory(.playback, options: .mixWithOthers)
try? session.setActive(true)
// 实际播放静音文件，目的是让 App 后台不被杀掉
```

**检查命令**：
```bash
# 检测是否有 audio 后台模式
grep -A5 "UIBackgroundModes" ios/*/Info.plist 2>/dev/null | grep "audio"

# 检测是否真的有音频功能
grep -rn "AVAudioPlayer\|AVPlayer\|AVAudioEngine\|MPNowPlayingInfoCenter" \
  --include="*.swift" --include="*.m" --include="*.js" . \
  --exclude-dir="Pods" --exclude-dir="node_modules" | grep -v "//\|test"

# 危险信号：有 audio 后台模式，但用的是静音或极低音量
grep -rn "volume.*0\|setVolume.*0\.0\|muted.*true\|AVAudioSession.*silent" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test"
```

**风险等级**：🔴 CRITICAL（如果是 keep-alive 用途）

---

### location — 后台位置

**Info.plist 值**：`location`
**合法用途**：
- 导航 App（持续追踪位置，如 Google Maps 类）
- 跑步/骑行追踪（记录运动轨迹）
- 货运/配送追踪（司机位置实时上报）
- 家庭安全（允许家人追踪位置的 App）
- 地理围栏（进入/离开特定区域触发事件）

**常见滥用**：
```swift
// ❌ 滥用：普通商业 App 后台持续采集位置
// 场景：天气App、电商App等，实际不需要后台位置
locationManager.startUpdatingLocation()  // 后台持续运行
locationManager.allowsBackgroundLocationUpdates = true  // 无合理理由
```

**检查命令**：
```bash
# 检测后台位置声明
grep -A10 "UIBackgroundModes" ios/*/Info.plist 2>/dev/null | grep "location"

# 检测是否设置了后台位置权限
grep -rn "allowsBackgroundLocationUpdates\|NSLocationAlwaysUsageDescription\|CLAuthorizationStatus.*always" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test"

# 检测是否有合理的导航/追踪功能
grep -rn "MKDirections\|CLLocationManager.*startUpdating\|GPX\|routeTracking\|navigationMode" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test"
```

**风险等级**：🔴 CRITICAL（如果没有实际导航/追踪功能）

---

### voip — VoIP 通话

**Info.plist 值**：`voip`
**合法用途**：
- 网络电话 App（WhatsApp 通话、FaceTime 类）
- 企业通讯工具（实时语音通话功能）

**重要**：使用此模式必须使用 CallKit 框架，否则会被拒绝（Guideline 4.2.1 扩展）。

**常见滥用**：
```swift
// ❌ 滥用：没有实际通话功能，却声明 voip 来保持后台连接
// 目的：维持 WebSocket 连接，实现"推送"效果
```

**检查命令**：
```bash
# 检测 voip 声明
grep -A10 "UIBackgroundModes" ios/*/Info.plist 2>/dev/null | grep "voip"

# 检测是否有 CallKit 实现（voip 必须配套）
grep -rn "CXProvider\|CXCallController\|CallKit\|CXCall" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test\|Pods"

# 危险信号：有 voip 但没有 CallKit
VOIP=$(grep -c "voip" ios/*/Info.plist 2>/dev/null)
CALLKIT=$(grep -rlc "CXProvider\|CallKit" --include="*.swift" . 2>/dev/null | wc -l)
echo "voip声明: $VOIP | CallKit实现: $CALLKIT"
```

**风险等级**：🔴 CRITICAL（如果没有实际通话功能）

---

### fetch — 后台 App 刷新

**Info.plist 值**：`fetch`
**合法用途**：
- 新闻 App 在后台预拉取最新内容
- 邮件 App 在后台检查新邮件
- 社交 App 在后台刷新 Feed

**注意事项**：
- 系统按需调用，不保证执行频率
- 每次调用有约30秒时限
- iOS 13+ 建议迁移到 BGAppRefreshTask（BackgroundTasks 框架）

```swift
// ✅ 合规：BGAppRefreshTask（推荐）
import BackgroundTasks
BGTaskScheduler.shared.register(
    forTaskWithIdentifier: "com.app.refresh",
    using: nil
) { task in
    self.handleAppRefresh(task: task as! BGAppRefreshTask)
}
```

**检查命令**：
```bash
grep -A10 "UIBackgroundModes" ios/*/Info.plist 2>/dev/null | grep "fetch"
grep -rn "BGAppRefreshTask\|performFetchWithCompletionHandler\|setMinimumBackgroundFetchInterval" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test"
```

**风险等级**：🟡 LOW（本身合规，但需确认实际有内容刷新需求）

---

### processing — 后台处理任务

**Info.plist 值**：`processing`
**合法用途**：
- 数据库同步、大文件处理
- ML 模型训练/推理
- 照片处理、视频转码

```swift
// ✅ 合规：BGProcessingTask
let request = BGProcessingTaskRequest(identifier: "com.app.processing")
request.requiresNetworkConnectivity = true
request.requiresExternalPower = false
try? BGTaskScheduler.shared.submit(request)
```

**检查命令**：
```bash
grep -A10 "UIBackgroundModes" ios/*/Info.plist 2>/dev/null | grep "processing"
grep -rn "BGProcessingTask\|BGTaskScheduler" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test"
```

**风险等级**：🟡 LOW（较少滥用，但需确认实际有处理任务）

---

### remote-notification — 远程通知后台处理

**Info.plist 值**：`remote-notification`
**合法用途**：
- 接收推送通知后在后台下载内容（静默推送）
- 更新徽章数量

**滥用风险**：过于频繁的静默推送会被系统限流，且消耗用户电量。

**检查命令**：
```bash
grep -A10 "UIBackgroundModes" ios/*/Info.plist 2>/dev/null | grep "remote-notification"
grep -rn "performFetchWithCompletionHandler\|didReceiveRemoteNotification.*fetchCompletionHandler" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test"
```

**风险等级**：🟠 MEDIUM（需确认有合理的静默通知使用场景）

---

### bluetooth-central / bluetooth-peripheral — 蓝牙

**Info.plist 值**：`bluetooth-central` / `bluetooth-peripheral`
**合法用途**：
- 连接蓝牙健康设备（心率带、血糖仪）
- 智能家居控制（后台维持连接）
- 蓝牙打印机、POS 机

**检查命令**：
```bash
grep -A10 "UIBackgroundModes" ios/*/Info.plist 2>/dev/null | grep "bluetooth"
grep -rn "CBCentralManager\|CBPeripheralManager\|CoreBluetooth" \
  --include="*.swift" --include="*.m" . | grep -v "//\|test\|Pods"
```

**风险等级**：🟠 MEDIUM（需有实际蓝牙设备连接场景）

---

### external-accessory — 外部配件

**Info.plist 值**：`external-accessory`
**合法用途**：连接 MFi 认证的硬件配件

**风险等级**：🟡 LOW（较少 App 使用）

---

## 高危组合预警

以下组合出现时，拒审概率极高：

| 组合 | 风险原因 |
|------|---------|
| `audio` + 无音频 UI + 无媒体控制 | 几乎确定是 keep-alive 滥用 |
| `location` + 无地图/导航功能 | 位置数据采集滥用嫌疑 |
| `voip` + 无 CallKit + 无通话界面 | VoIP 模式滥用保持连接 |
| `location` + `audio` + 无明确功能 | 综合后台保活，拒绝率接近100% |

---

## 全量后台模式扫描脚本

```bash
#!/bin/bash
# 后台模式扫描脚本 — Apple Review Preflight
# 使用方法：bash background-modes-scan.sh

echo "=== 后台模式声明 (UIBackgroundModes) ==="

find . -name "Info.plist" -not -path "*/Pods/*" -not -path "*/node_modules/*" -print0 2>/dev/null | \
while IFS= read -r -d '' plist; do
  echo ""
  echo "文件: $plist"
  # 提取 UIBackgroundModes 内容（路径作为参数传给 python，避免转义/空格问题）
  python3 - "$plist" 2>/dev/null <<'PY'
import plistlib, sys
path = sys.argv[1]
try:
    with open(path, 'rb') as f:
        plist = plistlib.load(f)
    modes = plist.get('UIBackgroundModes', [])
    if modes:
        print('  声明的后台模式:')
        for m in modes:
            print(f'    - {m}')
    else:
        print('  无后台模式声明')
except Exception as e:
    print(f'  解析失败: {e}')
PY
done

echo ""
echo "=== 功能实现验证 ==="

echo ""
echo "【audio 模式验证】"
AUDIO_DECL=$(grep -rl "audio" ios/*/Info.plist 2>/dev/null | wc -l)
AUDIO_IMPL=$(grep -rln "AVAudioPlayer\|AVPlayer\|AVAudioEngine\|MPNowPlayingInfoCenter" \
  --include="*.swift" --include="*.m" . --exclude-dir="Pods" 2>/dev/null | wc -l)
AUDIO_KEEPALIVE=$(grep -rln "volume.*0\b\|setVolume.*0\.0\b" --include="*.swift" . 2>/dev/null | wc -l)
echo "  audio后台声明: $AUDIO_DECL | 音频功能实现: $AUDIO_IMPL | 静音音频(keep-alive风险): $AUDIO_KEEPALIVE"
[ "$AUDIO_DECL" -gt 0 ] && [ "$AUDIO_IMPL" -eq 0 ] && echo "  ⚠️  警告：声明了audio后台模式但没有找到音频功能实现"

echo ""
echo "【location 模式验证】"
LOC_BG=$(grep -rln "allowsBackgroundLocationUpdates\s*=\s*true" --include="*.swift" . 2>/dev/null | wc -l)
LOC_NAV=$(grep -rln "MKDirections\|startUpdatingLocation\|CLLocationManager" --include="*.swift" . \
  --exclude-dir="Pods" 2>/dev/null | wc -l)
echo "  后台位置更新: $LOC_BG | 位置功能实现: $LOC_NAV"

echo ""
echo "【voip 模式验证】"
VOIP_DECL=$(grep -rl "voip" ios/*/Info.plist 2>/dev/null | wc -l)
CALLKIT_IMPL=$(grep -rln "CXProvider\|CXCallController" --include="*.swift" . --exclude-dir="Pods" 2>/dev/null | wc -l)
echo "  voip声明: $VOIP_DECL | CallKit实现: $CALLKIT_IMPL"
[ "$VOIP_DECL" -gt 0 ] && [ "$CALLKIT_IMPL" -eq 0 ] && echo "  ⚠️  警告：voip后台模式需要配合CallKit使用"

echo ""
echo "=== 扫描完成 — 请人工复核高风险组合 ==="
```

---

## 合规改造建议

### 替代 keep-alive 的合规方案

| 需求 | 滥用方案（禁止）| 合规方案 |
|------|--------------|---------|
| 后台维持长连接 | audio 静音 keep-alive | Silent Push + 重连机制 |
| 后台定期刷新数据 | voip 保活 + 定时器 | BGAppRefreshTask |
| 后台大量处理数据 | 多个模式叠加 | BGProcessingTask |
| 后台上传文件 | fetch 循环 | Background URL Session |
