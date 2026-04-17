# Widgets / Live Activity / Dynamic Island 合规指南
> WidgetKit、ActivityKit、Dynamic Island 的审核要点与 4.2 / 2.3 / 5.1.1 交集
> Guidelines baseline: 2026-02-06；ActivityKit API status: 2026-04

---

## 一、三者区别与范围

| 能力 | 框架 | 起始版本 | 显示位置 | 数据模型 |
|------|------|---------|---------|---------|
| Widget | WidgetKit | iOS 14.0+ | Home Screen / Lock Screen / StandBy | Timeline (静态快照集合) |
| Live Activity | ActivityKit | iOS 16.1+ | Lock Screen + Dynamic Island | 实时状态 (ContentState) |
| Dynamic Island | ActivityKit (UI 层) | iOS 16.1+（Pro/Pro Max & 全系 15+ ⚠️以 Apple 官方清单为准）| 药丸区域 | Live Activity 的 presentation 变体 |

**关键约束**：
- Widget **不是独立 App**，必须由主 App 提供完整功能（4.2 最小功能要求）
- Live Activity **最长 8 小时前台驻留**，push 可延续至额外 4 小时后必须 end（ActivityKit 硬限制）
- Dynamic Island 提供 4 种 presentation：`compactLeading` / `compactTrailing` / `minimal` / `expanded` — 必须同时实现 Lock Screen + Dynamic Island，不能只做其一（iOS 17+ 要求）

**三者关系**：
```
Live Activity (ActivityAttributes)
├── Lock Screen UI  ──── 必需
└── Dynamic Island  ──── 必需
    ├── compact (leading + trailing)
    ├── minimal  (单一药丸)
    └── expanded (leading / trailing / center / bottom)
```

---

## 二、4.2 最小功能要求

### 2.1 Widget 不能等于 App（4.2 最小功能）

- Widget 是 App 功能的**摘要/入口**，不能是 App 内功能的完整复制
- Widget-only App（仅提供 Widget、主 App 空壳）——拒审（4.2）
- 主 App 必须是"worth having"，单独可用

### 2.2 Live Activity 必须有真实"进行中"事件（Section 4 Design + 4.2）

✅ 合规场景：
- 订单/外卖追踪、打车 ETA
- 体育比赛实时比分
- 计时器 / 番茄钟 / 训练
- 导航剩余距离
- 直播倒计时 / 音乐播放

⚠️ 常见滥用（拒审）：
- 营销推广、优惠券常驻
- Always-on "品牌驻留"
- 天气、股票等**非事件性**的持续信息（应使用 Widget 而非 Live Activity）
- 假装"进行中"的静态提醒

### 2.3 结束义务

- 事件结束后 App **必须调用** `Activity.end(...)`，不能让系统自然超时
- `dismissalPolicy: .immediate` 或 `.after(date)` 需对用户合理

---

## 三、元数据与截图（2.3.x）

### 3.1 Widget 截图

- **ASC 上传**：可在 App Preview & Screenshots 中单独展示 Widget，需使用真实 iOS 版本 device frame
- 禁止展示 Widget 家族中**实际未提供**的尺寸（systemSmall / systemMedium / systemLarge / systemExtraLarge / accessoryInline / accessoryCircular / accessoryRectangular）
- StandBy 展示必须在横屏设备框架中

### 3.2 Live Activity 截图

- 上传 Lock Screen 截图必须为真实锁屏态（含顶部状态栏、壁纸）
- Dynamic Island 截图建议使用 Pro 机型 device frame，展示 expanded 状态
- App Preview 视频中如展示 Live Activity 更新，需为真实交互（不得后期合成）

### 3.3 避免 2.3.3 拒审

⚠️ **截图含未上线功能**是常见拒审点：如截图中 Live Activity 显示"AI 实时翻译"，但 App 尚无此能力——直接拒

---

## 四、隐私（5.1.1 + Privacy Manifest）

### 4.1 Lock Screen 信息敏感度

- Widget / Live Activity 在锁屏可被任何持有设备者看到（即使锁定）
- 必须使用 **Privacy Redaction API**：

```swift
Text(orderCode)
    .privacySensitive()   // 锁屏时自动打码为占位

// 或自定义 redacted 外观
.redacted(reason: .privacy)
```

- 敏感字段（订单号、金额、姓名、地址、验证码、健康数据）**必须** `privacySensitive()`

### 4.2 Push Token 管理

- `Activity.pushTokenUpdates` / `Activity.pushToStartTokenUpdates`（iOS 17.2+）产生的 token **视为用户标识符**
- 上送服务器需在 Privacy Manifest `NSPrivacyCollectedDataTypes` 中声明 `NSPrivacyCollectedDataTypeDeviceID`（若用于追踪则 `Tracking: true`）
- 参考：[privacy-manifest.md](./privacy-manifest.md)

### 4.3 Widget Intents 数据收集

- `AppIntentTimelineProvider` / `IntentConfiguration` 若读取用户内容（位置、日历、联系人），必须：
  - Info.plist 对应 usage string
  - Privacy Manifest 声明收集类型
  - ASC Nutrition Label 一致

### 4.4 Privacy Manifest 覆盖 Widget Extension

⚠️ **极常见漏洞**：主 App 有 `PrivacyInfo.xcprivacy`，Widget/ActivityExtension 没有
- 每个 Extension Target **都是独立 Bundle**，需独立 manifest
- 否则触发 ITMS-91053 / ITMS-91056
- Xcode：File → New → App Privacy File → Target Membership 勾选 WidgetExtension

---

## 五、Live Activity 特殊规则

### 5.1 更新频率预算（2026-04 状态）⚠️

- APNs 对每台设备每 App 的 Live Activity push 有**动态预算**，Apple 官方未公开精确数字
- 业界观测：高优先级（`apns-priority: 10`）约 **~4 次/小时** 不会被节流 ⚠️
- 低优先级（`apns-priority: 5`）预算更宽松，适合后台/非紧急更新
- 超出预算 → 后续 push **静默丢弃**（不返回错误）
- 开发测试：Settings → Developer → **Increase Frequency of Live Activity Updates** 临时放宽
- 推送混合策略：关键事件用 priority 10，周期性更新用 priority 5

### 5.2 内容规则

| 允许 | 禁止 |
|------|------|
| 真实进行中事件状态 | Marketing 文案 / 优惠券推销 |
| ETA / 进度 / 得分 | 伪装成 push 通知的行为 |
| 用户可验证的数据 | 与事件无关的 Badge / Banner |

### 5.3 End-of-activity 自动消失

- 事件结束后必须 `end(using:dismissalPolicy:)` 主动结束
- `dismissalPolicy: .default` 在 Lock Screen 保留 4 小时后消失
- 长时间未 end 的 Activity 会被审核员观察到（⚠️ 经验规则：reviewer 常用 4 小时以上窗口测试，Apple 未公开具体审核时长）

---

## 六、Dynamic Island 设计合规（HIG）

间接影响审核（Section 4 Design + 2.3）：

- **不得** tap Dynamic Island 跳转广告或促销页（必须回主 App 对应事件详情）
- **不得** 在 compact/minimal 显示与事件无关信息（例：点赞数、广告计数）
- 三种 presentation 必须**合理**使用：
  - `compact`：关键状态摘要（图标 + 短数字）
  - `minimal`：只在同屏多个 Activity 时出现，显示最少信息
  - `expanded`：长按显示，完整信息 + 至多 1 个主操作
- 严禁让 Dynamic Island 持续动画争夺注意力（4.2 Minimum Functionality）

---

## 七、代码扫描模式

### 7.1 grep 关键 API

```bash
# Live Activity 使用点
rg "ActivityKit\.Activity|Activity<.*>\.request|Activity\.authorizationInfo" --type swift

# Widget 配置类型
rg "WidgetConfiguration|StaticConfiguration|AppIntentConfiguration|ActivityConfiguration" --type swift

# Timeline Provider
rg "TimelineProvider|AppIntentTimelineProvider|IntentTimelineProvider" --type swift

# 隐私打码 API
rg "privacySensitive|redacted\(reason: \.privacy\)" --type swift
```

### 7.2 正确的 Live Activity 生命周期

```swift
// ① 启动
let attributes = OrderAttributes(orderID: "A123")
let state = OrderAttributes.ContentState(stage: .packing, eta: Date()+600)
let content = ActivityContent(state: state, staleDate: Date()+900)

let activity = try Activity<OrderAttributes>.request(
    attributes: attributes,
    content: content,
    pushType: .token   // 用于远程推送更新
)

// ② 更新（本地或 APNs push）
await activity.update(
    ActivityContent(state: newState, staleDate: Date()+900)
)

// ③ 结束（事件完成后必须调用）
await activity.end(
    ActivityContent(state: finalState, staleDate: nil),
    dismissalPolicy: .default   // 锁屏保留短时间后消失
)
```

---

## 八、常见拒审清单

| # | 场景 | 条款 |
|---|------|------|
| 1 | Widget-only App（主 App 空壳） | 4.2 |
| 2 | Live Activity 用作营销/常驻推广 | Section 4 / 4.2 |
| 3 | Widget 截图含未上线功能 | 2.3.3 |
| 4 | Privacy Manifest 未含 Widget/Activity Extension Target | 5.1.1 / ITMS-91053 |
| 5 | Live Activity 从不 `.end()`、依赖系统超时 | 2.5.16 / Section 4 |
| 6 | Dynamic Island 点击跳转广告页 | Section 4 / 3.2.2 |
| 7 | Push 频率超出预算、滥用 priority 10 | Section 4 / ⚠️ ActivityKit throttling behavior |
| 8 | 锁屏显示未打码敏感信息（订单号、地址） | 5.1.1 |

---

## 九、Review Notes 考虑

提交时在 App Review Information → Notes 中说明：

- **如何触发 Live Activity**：
  > "To test Live Activity: 1) Login with demo account `test@demo.com` / `Pass1234`; 2) Tap 'Place Test Order' on the home tab; 3) Live Activity appears on Lock Screen and Dynamic Island within 5s; 4) It auto-ends after 10 minutes."
- **Widget 配置路径**：
  > "To add Widget: long-press Home Screen → + → search 'AppName' → choose systemMedium → select category via widget configuration intent."
- **Dynamic Island 测试机型**：
  > "Dynamic Island requires iPhone 14 Pro or later. Expanded view is accessible via long-press on the pill."
- **推送验证**：若 Live Activity 走 APNs push 更新，附 sample curl 或说明 push payload 结构

---

## 十、提交前 Checklist

### Widget
- [ ] 主 App 是独立可用的（非仅 Widget 壳）— 4.2
- [ ] Widget 截图仅展示已实现的 family sizes — 2.3.3
- [ ] Widget Extension 有独立 `PrivacyInfo.xcprivacy` — 5.1.1
- [ ] Intent Configuration 声明 usage string（如用位置/联系人）— 5.1.1
- [ ] Lock Screen / StandBy 敏感字段使用 `privacySensitive()` — 5.1.1

### Live Activity
- [ ] 代表**真实进行中**的事件（非营销/常驻）— 4.2
- [ ] 所有路径均调用 `activity.end(...)`，无孤立 Activity — Section 4
- [ ] Push 频率：priority 10 ≤ ~4/h，其余走 priority 5 ⚠️
- [ ] Lock Screen UI **和** Dynamic Island 三种 presentation 均实现 — HIG
- [ ] `ActivityExtension` target 有独立 Privacy Manifest — 5.1.1
- [ ] Push token 上送若用于标识，已在 Nutrition Label 声明 — 5.1.1
- [ ] Dynamic Island 点击目标为 deep link 至事件详情，非广告 — Section 4

### Dynamic Island
- [ ] compact / minimal / expanded 三态都提供且信息合理 — HIG
- [ ] 不争夺注意力（无持续动画/闪烁）— Section 4
- [ ] 长按展开内容与事件强相关 — 4.2

### Review Notes
- [ ] Live Activity 触发步骤清晰（demo 账号 + 路径）
- [ ] 若仅 Pro 机型可见 Dynamic Island，已说明
- [ ] 已说明如何验证结束/自动 dismiss

---

## 交叉引用

- Privacy Manifest 完整填写规范：[./privacy-manifest.md](./privacy-manifest.md)
- 拒审场景与条款对照：[../checks/review-failure-map.md](../checks/review-failure-map.md)
