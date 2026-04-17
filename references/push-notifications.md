# Push Notification 合规指南
> App Review Guideline 4.5.4 + APNs / Critical Alerts / Time Sensitive 合规实务
> 基线：2026-02-06 Guidelines；交叉参考 `./privacy-manifest.md`、`../checks/review-failure-map.md`

---

## 一、4.5.4 核心规则

Apple Push Notification service (APNs) 是**特权通道**，使用前提：

| 约束 | 说明 |
|------|------|
| Opt-in required | 首次注册 remote notification 必须触发系统弹窗（`requestAuthorization`），用户拒绝即不可发送 |
| 可随时 opt-out | App 内必须提供"关闭推送"入口；用户在系统设置或 App 内关闭后，服务端必须立即停止发送 |
| 禁止用途 | 不得发送 abusive / defamatory / spam / 无针对性营销内容 |
| 不得胁迫授权 | 不得以"不开通知就禁用核心功能"的方式强制用户 opt-in（Guideline 4.5.4 明文禁止） |
| 营销类需单独同意 | Promotional / marketing 推送必须有**显式且可撤销**的同意 |

违反直接引用 Guideline 4.5.4 拒审，严重情况（反复推送营销）可能触发 Developer Program 警告。

---

## 二、营销类推送的 opt-in 要求

### 2.1 Transactional vs Marketing 分类

| 类型 | 示例 | 同意要求 |
|------|------|---------|
| Transactional | 订单状态、支付成功、好友消息、安全告警 | 系统权限足够 |
| Marketing | 促销、优惠券、"回来看看"、交叉推广 | **额外 in-app opt-in**，必须可撤销 |

### 2.2 Granular opt-in（分类订阅）

用户必须能独立选择类别。例如：

```
[ ] 订单与配送通知       ← transactional, 默认开
[ ] 账户安全             ← transactional, 默认开
[ ] 促销活动与优惠券     ← marketing, 默认关 ⚠️
[ ] 新品上架             ← marketing, 默认关 ⚠️
```

⚠️ **不要**把营销类别和 transactional 合并为单一开关——审核员会测试是否能"只要订单通知不要促销"。

### 2.3 初次弹窗不能用作营销 opt-in

系统 `requestAuthorization` 弹窗只覆盖"是否允许推送"，**不能**解读为营销同意。Apple HIG 建议：

- 营销同意应在"情境中"询问（如用户首次完成购买后）
- 同意需与 transactional 同意**分开**
- 默认值必须为"关闭"，用户主动勾选才算同意

---

## 三、内容规则

- **5.1.1 隐私**：通知正文默认在锁屏展示预览，禁止放置 full credit card、身份证号、完整医疗诊断、OTP 验证码全文等敏感信息。可用 `UNNotificationContent.interruptionLevel` + server-side mutable content，用户解锁后再拉取详情。
- **敏感内容遮罩**：健康、财务、密信类 App 建议默认 `hiddenPreviewsBodyPlaceholder`，并提供 in-app 开关。
- **本地化**：根据 `Accept-Language` 或用户 profile 语言发送，不得全量英文轰炸。
- **无欺骗性**：标题/正文不得伪装为系统通知、不得冒充其他 App。

✅ 推荐：payload 仅携带 ID，App Service Extension 在本地根据用户偏好渲染正文。

---

## 四、频率与时机

| 规则 | 说明 |
|------|------|
| 频率 | 单用户每日同类推送建议 ≤ 1~2 次；营销类每周 ≤ 2 次 |
| 文案 | 不得 "Buy now!!!" 这类压迫式营销；避免全大写、过度 emoji |
| 时区 | 按用户本地时区发送；**避免 22:00–08:00** 深夜推送（除非 transactional/critical） |
| Quiet hours | 尊重系统 Focus / Do Not Disturb；非 Time Sensitive 推送不应绕开 |
| A/B 测试 | 禁止以 "对照组收不到订单通知" 的方式测试 transactional；marketing A/B 不得使用 dark pattern 文案 |

---

## 五、推送类型与 entitlement

| 类型 | 触发方式 | Entitlement / 审批 | 典型用途 |
|------|----------|------------------|---------|
| Local Notification | `UNUserNotificationCenter.add()` | 无 | 闹钟、本地提醒 |
| Remote (APNs) | 服务端 push | APNs key/cert | 消息、订单 |
| Provisional | `.provisional` authorization | 无 | 无声投递至 Notification Center |
| Time Sensitive (iOS 15+) | `interruptionLevel = .timeSensitive` | Time Sensitive Notifications capability（entitlement `com.apple.developer.usernotifications.time-sensitive`） | 安防、健康提醒、配送预警 |
| Critical Alert | `.critical` + 声音 | **需 Apple 审批** [Critical Alerts entitlement](https://developer.apple.com/contact/request/notifications-critical-alerts-entitlement/) | 医疗、生命安全、家庭安防、CO 探测 |
| PushKit (VoIP) | `PKPushRegistry` | `com.apple.developer.pushkit.unrestricted-voip`（iOS 13+ 必须配合 CallKit） | VoIP 来电、PTT |

⚠️ Critical Alerts 只授予具备公共安全 / 医疗 / 家庭安防正当理由的 App；滥用将整批 App 被吊销。
⚠️ Time Sensitive **不能**用于营销——Apple 明确列为滥用情形。
⚠️ PushKit VoIP 不再允许用于非 VoIP 场景（iOS 13 起必须在收到时调用 CallKit `reportNewIncomingCall`，否则进程被终止 + 审核拒绝）。

---

## 六、Review Notes 考虑

审核员会在真机上测试：

1. 首次启动，拒绝权限 → App 仍可使用核心功能？
2. 接受权限 → 进入设置关闭"促销" → 服务端是否仍发营销？
3. 是否能独立关闭营销而保留 transactional？
4. 通知正文是否在锁屏暴露敏感数据？
5. 是否声明了 Critical Alerts 但用于非紧急场景？

在 Review Notes 中主动说明：
- 营销 opt-in 的位置（截图路径 + 步骤）
- 哪些推送属于 transactional（合规依据）
- 如使用 Critical Alerts，附 entitlement 审批邮件截图

---

## 七、代码扫描模式

### 7.1 需搜索的符号

```bash
# 权限请求与注册
requestAuthorization
registerForRemoteNotifications
UNUserNotificationCenter
UNNotificationRequest
PKPushRegistry

# interruption level / critical
interruptionLevel
\.timeSensitive
\.critical
criticalAlert

# 本地 schedule（需确认是否遵守 opt-out）
UNTimeIntervalNotificationTrigger
UNCalendarNotificationTrigger
UNUserNotificationCenter.*add\(   # 真正的 API 是 UNUserNotificationCenter.current().add(_:)
```

### 7.2 正确的 opt-out 遵守模式

```swift
func scheduleLocalReminder(_ content: UNNotificationContent) async {
    // ① 检查系统权限
    let settings = await UNUserNotificationCenter.current().notificationSettings()
    guard settings.authorizationStatus == .authorized ||
          settings.authorizationStatus == .provisional else { return }

    // ② 检查 App 内 granular opt-out（用户可能关了促销）
    guard NotificationPreferences.shared.isEnabled(for: content.categoryIdentifier) else {
        return
    }

    // ③ 尊重 quiet hours
    if QuietHours.isWithinQuietPeriod(Date()) &&
       content.interruptionLevel != .timeSensitive {
        return
    }

    let req = UNNotificationRequest(identifier: UUID().uuidString,
                                    content: content,
                                    trigger: nil)
    try? await UNUserNotificationCenter.current().add(req)
}
```

❌ 反模式：在 opt-out 后仍调用 `add()`、服务端在 unsubscribe 后仍下发、用 `.timeSensitive` 包装营销。

---

## 八、常见拒审

| 场景 | 触发条款 |
|------|---------|
| 拒绝通知后核心功能被 gray out | 4.5.4（胁迫 opt-in） |
| 默认勾选营销订阅，用户未主动同意 | 4.5.4 + 5.1.1 |
| 单一开关混合 transactional 与 marketing | 4.5.4（缺 granular） |
| 推送正文包含完整信用卡号 / OTP / 诊断 | 5.1.1 Privacy |
| 推送 "Rate us now!" / 求评分营销 | 4.5.4 + 5.6 |
| 声明 Critical Alerts 但用于推广 / 普通消息 | 4.5.4 + entitlement 滥用 |
| Dark pattern opt-in（按钮文案诱导、拒绝入口隐藏） | 4.5.4 + 5.1.1(v) |

---

## 九、提交前 checklist

- [ ] **4.5.4**：首次推送权限通过 `requestAuthorization` 触发，拒绝后 App 核心功能仍可用
- [ ] **4.5.4**：App 内提供 granular 开关，transactional 与 marketing 独立
- [ ] **4.5.4**：默认不订阅营销；系统弹窗未被作为营销同意
- [ ] **4.5.4**：服务端接入 opt-out 状态，unsubscribe 后 100% 停发
- [ ] **5.1.1**：通知 payload 不含敏感明文（卡号/OTP/诊断），锁屏预览已测试
- [ ] **时区/频率**：服务端按用户时区调度，避开 22:00–08:00；频率限流已配置
- [ ] **Critical Alerts**：如使用，entitlement 审批邮件留档，Review Notes 说明用途
- [ ] **Time Sensitive**：仅用于真正紧急场景（非营销、非一般消息）
- [ ] **PushKit VoIP**：收到 push 后必定调用 CallKit `reportNewIncomingCall`
- [ ] **Review Notes**：截图说明 opt-in 路径 + 分类开关位置
- [ ] **代码扫描**：`grep` 所有 `add(UNNotificationRequest)` 点都前置权限与偏好检查

---

参考：
- [Apple 修订推送营销规则（4.5.4 放宽但须显式同意）](https://www.jdsupra.com/legalnews/apple-eases-push-notification-and-other-13374/)
- [Critical Alerts 申请入口](https://developer.apple.com/contact/request/notifications-critical-alerts-entitlement/)
- [Using Critical Alerts（实现细节）](https://blog.kulman.sk/using-critical-alerts-on-ios/)
- 交叉参考：`./privacy-manifest.md`（通知数据收集申报）、`../checks/review-failure-map.md`（4.5.4 典型拒审映射）
