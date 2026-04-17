# watchOS App 专项风险

> 本文件仅记录超出通用审核规则的专项要求。适用于包含 watchOS target 的 App，以及独立 watchOS App。

---

## 1. watchOS App 独立运行要求（Guidelines 2.4.1）

**规则来源：App Store Review Guidelines 2.4.1**

自 watchOS 7 起，Apple 要求 watchOS App **必须能够独立运行**，不得完全依赖配对 iPhone 才能使用核心功能。

**具体要求**：
- Watch App 必须在没有 iPhone 的情况下可以启动并展示有意义的内容。
- 如果 Watch App 的核心功能需要网络数据，必须在 Watch 上直接实现网络请求（URLSession），不能通过 WatchConnectivity 从 iPhone 代理所有网络请求。
- **常见违规**：Watch App 打开后只显示"请在 iPhone 上操作"或无限 loading 状态。
- **例外**：部分高度依赖 iPhone 传感器（如 GPS 精度要求极高）的功能可以在 iPhone 不可用时显示降级提示，但不能是 App 的唯一状态。

**判断标准**：
- 审核员会在没有配对 iPhone 的情况下测试 Watch App。
- Watch App 必须通过独立网络请求、本地数据或 CloudKit 等方式提供可用内容。

---

## 2. 账号和权限链路：与 iOS 账号状态同步

**规则来源：App Store Review Guidelines 2.1 / 实践规则**

- 如果 iOS App 有登录账号，watchOS App 的登录状态必须与 iOS 同步，不得要求用户在手表上单独登录。
- **推荐方式**：WatchConnectivity（`WCSession`）传递 token，或使用 CloudKit / iCloud Keychain 共享凭证。
- **Sign in with Apple**：watchOS 本身不能发起 Sign in with Apple 流程，必须依赖 iOS 侧完成后同步状态。
- 用户注销时，iOS 与 Watch 的登录状态必须保持一致，不能出现 iOS 已注销但 Watch 仍显示登录态的情况。
- **权限同步**：如果 App 使用 HealthKit 权限，watchOS 和 iOS 需要分别申请（权限不共享），需在两端分别引导用户授权。

---

## 3. Complications 内容限制

**规则来源：App Store Review Guidelines / Human Interface Guidelines**

- Complications 展示的内容必须有实际信息价值，不能是纯广告、品牌宣传或无意义的装饰内容。
- **禁止**：Complication 仅展示 App Logo 和"打开 App"，没有任何有用信息。
- **禁止**：Complication 展示与 App 声明功能无关的内容。
- **内容时效性**：Complications 应展示相对实时的数据，如果数据明显过期（超过合理刷新周期），需要显示时间戳或过期标识。
- **隐私**：不得在 Complication 中展示敏感信息（如健康数据、财务余额），因为 Complications 在锁屏状态下可见。
- **WidgetKit Complication**：watchOS 9+ 的 Complications 使用 WidgetKit，同样适用通用 Widget 规则（不得展示第三方广告）。

---

## 4. 后台刷新的合理使用

**规则来源：App Store Review Guidelines 2.4 / watchOS 技术文档**

- watchOS 的后台任务资源极为有限，Apple 会检查 App 是否滥用后台刷新配额。
- **Background App Refresh**（`WKApplicationRefreshBackgroundTask`）：
  - 每次后台任务必须在 **30 秒内完成**，否则 watchOS 会终止进程。
  - 请求频率不能超过系统分配配额（通常每小时最多几次，具体由系统动态决定）。
  - 必须在任务结束时调用 `task.setTaskCompleted(success:)`。
- **后台网络请求**（`WKURLSessionRefreshBackgroundTask`）：
  - 必须使用后台 URLSession（`URLSessionConfiguration.background`）。
  - 不得发起大量并发后台请求。
- **审核标准**：如果 App 的后台刷新逻辑导致电池消耗异常，审核员可能拒审并要求优化。
- **不允许**：在 Complications 的 `getTimeline` 中发起同步网络请求（会导致 Complication 更新延迟或崩溃）。

---

## 5. 常见 watchOS 拒审场景

| 场景 | 原因 | 解决方案 |
|------|------|---------|
| Watch App 启动后显示"请配合 iPhone 使用" | 违反 2.4.1 独立运行要求 | 实现独立网络请求或本地数据展示 |
| Complication 只显示 Logo，无信息 | 无实际内容价值 | 展示有意义的数据（时间、步数、天气等） |
| Watch App 截图使用 iPhone 截图替代 | 截图不符合要求 | 必须提供 Apple Watch 截图（2 张以上） |
| 登录状态不同步，Watch 上需要重新登录 | 用户体验不佳 | 通过 WatchConnectivity 或 iCloud Keychain 同步 |
| 后台任务超过 30 秒未完成 | 系统限制 | 拆分任务或优化网络请求 |
| Watch App 功能与 iOS App 完全重复且无任何手表优化 | 内容价值不足（2.1） | 至少针对手表场景优化 UI 和交互 |
| 在 Complication 展示密码、余额等敏感信息 | 锁屏可见性隐私风险 | 仅展示非敏感摘要信息 |

---

## 截图要求

- 必须提供 **Apple Watch 截图**（不能用 iPhone/iPad 截图替代）。
- 支持的尺寸：40mm、41mm、44mm、45mm、49mm（Ultra），建议至少提供 41mm 和 45mm。
- 截图数量：每种尺寸至少 1 张，最多 10 张。
- 截图必须展示 Watch App 的实际功能界面，不能只展示 Complications。
