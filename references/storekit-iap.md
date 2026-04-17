# StoreKit & IAP 完整指南
> StoreKit 2 vs 1 对比 + 完整购买流程 + 沙盒测试 + 收据验证 + 订阅管理
> 基于 iOS 16+ / StoreKit 2 （Swift async/await）

---

## 一、StoreKit 2 vs StoreKit 1 主要差异

| 特性 | StoreKit 1（旧版） | StoreKit 2（iOS 15+）|
|------|-------------------|---------------------|
| API 风格 | 委托模式（Delegate/Notification）| async/await |
| 收据 | App Receipt（本地文件） | JWS 签名的 Transaction |
| 验证 | 需服务端验证 receipt-data | 客户端可直接验证 JWS（App Attest 配合）|
| 订阅状态 | 需轮询服务端 | `Transaction.currentEntitlements` 实时获取 |
| 退款检测 | 困难（需 S2S Notification）| `Transaction.updates` 包含退款事件 |
| 家庭共享 | 需额外处理 | `Transaction.isUpgraded`、`ownershipType` |
| 最低系统要求 | iOS 3+ | iOS 15+ |
| 推荐使用 | 需支持 iOS 14 及以下时 | iOS 15+ 项目首选 |

**结论**：新项目直接用 StoreKit 2；需要支持 iOS 14 的项目用 StoreKit 1 或做双版本兼容。

---

## 二、StoreKit 2 完整购买流程实现

### 2.1 Product 加载

```swift
import StoreKit

// 在 App 初始化时加载商品列表
class StoreManager: ObservableObject {
    @Published var products: [Product] = []
    @Published var purchasedProductIDs: Set<String> = []
    
    // 在 ASC 中配置的产品 ID
    private let productIdentifiers: Set<String> = [
        "com.example.app.premium.monthly",
        "com.example.app.premium.yearly",
        "com.example.app.coins.100",
    ]
    
    init() {
        Task {
            await loadProducts()
            await updatePurchasedProducts()
        }
    }
    
    @MainActor
    func loadProducts() async {
        do {
            products = try await Product.products(for: productIdentifiers)
            // 按价格排序
            products.sort { $0.price < $1.price }
        } catch {
            print("Failed to load products: \(error)")
        }
    }
}
```

### 2.2 发起购买

```swift
extension StoreManager {
    @MainActor
    func purchase(_ product: Product) async throws -> Transaction? {
        let result = try await product.purchase()
        
        switch result {
        case .success(let verification):
            // 验证 Transaction
            let transaction = try checkVerified(verification)
            
            // 更新 entitlement
            await updatePurchasedProducts()
            
            // 必须调用 finish()，否则 Transaction 会重复出现
            await transaction.finish()
            
            return transaction
            
        case .userCancelled:
            return nil
            
        case .pending:
            // 等待家长批准（Parental Controls）或 Ask to Buy
            return nil
            
        @unknown default:
            return nil
        }
    }
    
    func checkVerified<T>(_ result: VerificationResult<T>) throws -> T {
        switch result {
        case .unverified:
            // StoreKit 验证失败（极少见，可能是设备时间异常）
            throw StoreError.failedVerification
        case .verified(let safe):
            return safe
        }
    }
    
    enum StoreError: Error {
        case failedVerification
    }
}
```

### 2.3 Entitlement 检查（订阅状态）

```swift
extension StoreManager {
    @MainActor
    func updatePurchasedProducts() async {
        var purchased: Set<String> = []
        
        // 遍历所有当前有效的 Transaction
        for await result in Transaction.currentEntitlements {
            guard case .verified(let transaction) = result else { continue }
            
            // 检查是否已退款或撤销
            if transaction.revocationDate != nil { continue }
            
            // 检查订阅是否在有效期内
            if let expirationDate = transaction.expirationDate,
               expirationDate < Date() { continue }
            
            purchased.insert(transaction.productID)
        }
        
        purchasedProductIDs = purchased
    }
    
    // 检查具体功能是否解锁
    var isPremium: Bool {
        purchasedProductIDs.contains("com.example.app.premium.monthly") ||
        purchasedProductIDs.contains("com.example.app.premium.yearly")
    }
}
```

### 2.4 监听 Transaction 更新（后台续订、退款等）

```swift
// 在 @main App 中启动 Transaction 监听
@main
struct MyApp: App {
    @StateObject private var store = StoreManager()
    /// 保留 Task 引用以管理生命周期
    private var transactionListenerTask: Task<Void, Error>?
    
    init() {
        // 在 init 中保存 listener task 引用
        let store = StoreManager()
        _store = StateObject(wrappedValue: store)
        transactionListenerTask = Task.detached {
            for await result in Transaction.updates {
                do {
                    let transaction = try store.checkVerified(result)
                    if transaction.revocationDate != nil {
                        await store.updatePurchasedProducts()
                        await transaction.finish()
                        continue
                    }
                    await store.updatePurchasedProducts()
                    await transaction.finish()
                } catch {
                    print("Transaction verification failed: \(error)")
                }
            }
        }
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
        }
    }
}
```

---

## 三、沙盒测试环境配置

### 3.1 创建 Sandbox Apple ID

1. ASC → Users and Access → Sandbox → Testers → "+"
2. 填写邮箱（建议用临时邮箱，如 `sandbox_test_001@example.com`）
3. 填写国家/地区（影响货币和定价）
4. 密码复杂度要求：8位以上，含大小写和数字

**注意**：Sandbox Apple ID 不能用于正式 App Store 购买，仅用于测试。

### 3.2 在真机上使用 Sandbox 账号

1. 设备 → 设置 → App Store → 滚动到底部 → Sandbox Account
2. 登录 Sandbox Apple ID（**不是**主 Apple ID）
3. 设备的主 Apple ID 不受影响

### 3.3 沙盒环境特性

| 特性 | 说明 |
|------|------|
| 订阅续订速度 | 大幅加速（1个月 = 5分钟，1年 = 1小时）|
| 订阅自动续订上限 | 每个 Sandbox 账号最多续订12次 |
| 退款 | 在 ASC 中手动触发（Sandbox → Transactions → Refund）|
| 付款 | 不产生真实费用 |
| App Receipt | 签名不同，无法用生产环境验证端点验证 |

### 3.4 Sandbox 加速的订阅周期对应表

| 真实周期 | Sandbox 周期 |
|---------|-------------|
| 1周 | 3分钟 |
| 1个月 | 5分钟 |
| 2个月 | 10分钟 |
| 3个月 | 15分钟 |
| 6个月 | 30分钟 |
| 1年 | 1小时 |

### 3.5 在 Simulator 测试

StoreKit 2 支持在 Simulator 中测试（不需要真机）：
1. Xcode → File → New → File → StoreKit Configuration File
2. 添加商品（Consumable/Non-Consumable/Auto-Renewable Subscription）
3. Xcode → Edit Scheme → Run → Options → StoreKit Configuration → 选择刚创建的文件
4. 运行 App，购买流程使用本地模拟，无需网络和 Sandbox 账号

```swift
// 检测是否在 Simulator 测试环境
#if DEBUG
// 可以添加测试专用逻辑
#endif
```

---

## 四、服务端收据验证 vs 客户端验证

### 4.1 StoreKit 2 的 JWS Transaction

StoreKit 2 中每个 Transaction 是 JSON Web Signature（JWS）格式，可在客户端验证（Apple 公钥已内置在系统）。

```swift
// 客户端验证（StoreKit 2 自动处理）
switch result {
case .verified(let transaction):
    // Apple 已验证签名，可信任
    // transaction.productID、transaction.purchaseDate 等字段可直接使用
    break
case .unverified(_, let error):
    // 验证失败，不要授予权限
    break
}
```

### 4.2 服务端验证（推荐用于高价值订阅）

**为什么还需要服务端验证**：
- 防止 Runtime Hook（越狱设备修改 StoreKit 返回值）
- 跨设备订阅状态同步（用户换设备）
- 服务端业务逻辑（发放权益、记录购买历史）
- 处理 S2S Notification（退款、续订失败等）

**App Store Server API（推荐，替代旧的收据验证端点）**：

```swift
// 客户端：获取 Transaction JWS 并发送到服务端
func sendTransactionToServer(_ transaction: Transaction) async {
    // transaction.jwsRepresentation 是 JWS 字符串
    let jws = transaction.jwsRepresentation
    
    var request = URLRequest(url: URL(string: "https://api.yourserver.com/verify")!)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try? JSONEncoder().encode(["transactionJWS": jws])
    
    let (_, _) = try? await URLSession.shared.data(for: request)
}
```

```python
# 服务端（Python 示例）：验证 JWS
# 使用 Apple 官方 App Store Server Library
# pip install app-store-server-library

from appstoreserverlibrary.api_client import AppStoreServerAPIClient, Environment
from appstoreserverlibrary.signed_data_verifier import SignedDataVerifier

# 方式 1：使用 SignedDataVerifier 验证 JWS Transaction
verifier = SignedDataVerifier(
    root_certificates=root_certificates,   # Apple Root CA 证书列表
    enable_online_checks=True,
    environment=Environment.PRODUCTION,     # 或 Environment.SANDBOX
    bundle_id=BUNDLE_ID,
    app_apple_id=APP_APPLE_ID,             # App Store Connect 中的 Apple ID（数字）
)

transaction = verifier.verify_and_decode_signed_transaction(jws_string)
print(transaction.product_id)
print(transaction.expires_date)

# 方式 2：使用 API Client 查询交易历史
api_client = AppStoreServerAPIClient(
    signing_key=PRIVATE_KEY_PEM,   # .p8 文件内容
    key_id=KEY_ID,
    issuer_id=ISSUER_ID,
    bundle_id=BUNDLE_ID,
    environment=Environment.PRODUCTION,
)

response = api_client.get_transaction_history(original_transaction_id)
```

**旧版收据验证（App Receipt，仅 StoreKit 1）**：

```
# 不推荐（已被 App Store Server API 替代，Apple 宣布计划废弃）
POST https://buy.itunes.apple.com/verifyReceipt
POST https://sandbox.itunes.apple.com/verifyReceipt（沙盒）

Body: { "receipt-data": "base64编码的收据", "password": "共享密钥" }
```

### 4.3 App Store Server Notifications V2

在 ASC → App Information → App Store Server Notifications 配置 URL，Apple 会在以下事件时推送通知：
- `SUBSCRIBED`：新订阅
- `DID_RENEW`：订阅续订成功
- `EXPIRED`：订阅到期
- `DID_FAIL_TO_RENEW`：续订失败（宽限期）
- `GRACE_PERIOD_EXPIRED`：宽限期结束
- `REFUND`：退款成功
- `REVOKE`：家庭共享撤销

---

## 五、Restore Purchases 实现

```swift
// 恢复购买（必须提供此功能，否则违反 Guideline 3.1.1）
extension StoreManager {
    func restorePurchases() async throws {
        // StoreKit 2 中，直接调用 sync() 从 Apple 服务器同步最新状态
        try await AppStore.sync()
        
        // sync() 完成后，Transaction.currentEntitlements 已更新
        await updatePurchasedProducts()
    }
}

// UI 中调用
Button("恢复购买") {
    Task {
        do {
            try await store.restorePurchases()
            // 成功提示
        } catch {
            // 错误提示（如网络错误）
        }
    }
}
```

**重要**：Restore 按钮必须在 UI 中显示，通常放在订阅页面底部。审核员会测试此功能。

---

## 六、订阅状态管理

### 6.1 获取订阅详细状态

```swift
// 获取订阅组的最新状态
func getSubscriptionStatus() async -> Product.SubscriptionInfo.Status? {
    guard let product = products.first(where: { $0.type == .autoRenewable }) else {
        return nil
    }
    
    guard let statuses = try? await product.subscription?.status else {
        return nil
    }
    
    // 找到最相关的状态（通常取第一个）
    return statuses.first { status in
        switch status.state {
        case .subscribed, .inGracePeriod, .inBillingRetryPeriod:
            return true
        default:
            return false
        }
    }
}
```

### 6.2 订阅状态枚举

```swift
// Product.SubscriptionInfo.RenewalState
switch status.state {
case .subscribed:
    // 订阅有效
    print("活跃订阅")
    
case .expired:
    // 订阅已过期
    let expirationReason = status.renewalInfo.value?.expirationReason
    print("过期原因: \(expirationReason)")
    
case .inGracePeriod:
    // 续订失败，在宽限期内（用户仍有访问权）
    // 引导用户更新支付方式
    print("宽限期（约16天）")
    
case .inBillingRetryPeriod:
    // Apple 正在重试续订（宽限期后）
    // 用户已无访问权
    print("账单重试期")
    
case .revoked:
    // 家庭共享被撤销
    print("家庭共享已撤销")
    
@unknown default:
    break
}
```

### 6.3 升级/降级订阅

```swift
// 从月订阅升级到年订阅
// 直接 purchase 新产品，StoreKit 自动处理降级/升级逻辑
let yearlyProduct = products.first { $0.id == "com.example.app.premium.yearly" }!

let result = try await yearlyProduct.purchase(options: [
    // 可指定促销优惠
    .promotionalOffer(offerID: "welcome_back", keyID: keyID, nonce: nonce, 
                      signature: signature, timestamp: timestamp)
])
```

---

## 七、常见 IAP 拒审原因和修复

### 7.1 Guideline 3.1.1 — 绕过 IAP

**拒审场景**：
- App 内有链接跳转到网页购买（如"在官网购买以节省20%"）
- 按钮文字暗示可以用其他方式购买
- 邮件中发送购买链接

**修复**：
- 删除所有引导用户绕过 IAP 的 UI 元素
- 网页端购买页面可以存在，但不能从 App 内直接链接
- 例外：Reader App（Netflix、Spotify 类）可不提供 IAP，也不能有购买链接（灰色地带，需谨慎）

### 7.2 Guideline 3.1.2 — 订阅信息不完整

**拒审场景**：
- 未清晰展示价格、续订周期
- 没有"取消订阅"的说明（需链接到 App Store 订阅管理）
- 试用期结束后直接扣费未提前提醒

**修复**：
```swift
// 显示完整订阅信息
if let subscription = product.subscription {
    let period = subscription.subscriptionPeriod
    let trialPeriod = subscription.introductoryOffer
    
    Text("价格：\(product.displayPrice) / \(period.localizedDescription)")
    
    if let trial = trialPeriod {
        Text("免费试用：\(trial.period.localizedDescription)")
    }
    
    // 必须包含取消说明
    Link("管理订阅", destination: URL(string: "itms-apps://apps.apple.com/account/subscriptions")!)
}
```

### 7.3 虚拟货币规则（3.1.1）

**常见问题**：
- 虚拟货币可以在用户之间转让（不允许）
- 购买虚拟货币后可以提现（不允许）
- 虚拟货币用于支付现实服务（需使用 IAP）

**允许的场景**：
- 在 App 内使用虚拟货币购买虚拟商品（游戏道具、滤镜等）
- 虚拟货币只能单向流动（购买→使用，不可退还为现金）

### 7.4 Guideline 2.1 — IAP 缺失 Demo 账号

**问题**：App 有 IAP 但 Review Notes 未提供沙盒测试账号，或提供的账号无法购买。

**修复**：
在 Review Notes 中提供：
```
SANDBOX TESTING
To test in-app purchases:
1. Use Sandbox Apple ID: sandbox_iap@example.com / TestPass123!
2. Or use your own Sandbox Apple ID (Settings → App Store → Sandbox Account)
3. Purchases in Sandbox do not charge real money

SUBSCRIPTION TEST
- The demo account has NOT pre-activated any subscription
- Please test purchase using the Sandbox account above
- The monthly subscription will auto-renew every 5 minutes in Sandbox
```

### 7.5 消耗型商品的持久化

```swift
// 消耗型商品（Consumable）购买后必须 finish()，且服务端需记录
// 否则用户重新安装 App 后，Restore 不会恢复消耗型商品
func handleConsumablePurchase(_ transaction: Transaction) async {
    // 1. 发送到服务端记录
    await sendTransactionToServer(transaction)
    
    // 2. 本地更新（如增加虚拟货币余额）
    await addCoins(100)
    
    // 3. 必须 finish
    await transaction.finish()
}
```

---

## 八、佣金费率与区域差异

Apple App Store 不同地区 / 条款下的佣金率并非单一 30%。LTV / 单价 / ROI 计算前先核对本表。

### 8.1 当前费率总览（2026-04 更新）

| 场景 | 佣金率 | 适用 |
|------|--------|------|
| 标准 IAP（大多数地区） | **30%** | 未参加 SBP 的开发者，全球默认 |
| **中国区** 标准（2026-03-15+） | **25%** | 中国大陆 storefront；✅ Apple Developer News 2026-03-12 公告 |
| Small Business Program（全球） | **15%** | 年 proceeds < $1M USD |
| **中国区** SBP / Mini Apps（2026-03-15+） | **12%** | 中国大陆 storefront + SBP / Mini Apps Partner Program |
| Auto-Renewable Subscription 第 2 年（loyalty rate，全球） | **15%** | 订阅连续 12 个月以上的 proceed |
| **中国区** 订阅 loyalty rate（2026-03-15+） | **12%** | ✅ Apple Developer News 2026-03-12 明确 auto-renewals after first year 为 12% |
| **EU DMA** — StoreKit External Purchase Link | 27%（首年）/ 12%（loyalty） | 2026-01-01 起被 CTC 5% + Store Services 5-13% 等替代；详见 `../market-overrides/eu-eea.md` §3 和 `../operations/eu-dma-alternatives.md` |
| **EU DMA** — Alternative Marketplace / Web Distribution | 0%（Apple 不抽成） + CTC 5% | 用 Alternative Terms Addendum 的开发者 |
| 付费 App（paid apps）| 同上 IAP 费率结构 | 首次付费下载按同区域 IAP 费率抽成 |
| 美区外部购买链接 | ⚠️ 以 Apple 最新公告为准（2024 Epic v. Apple 裁决后多次调整；历史上为 27%/12%） | 详见 `../market-overrides/us.md` §1 |

### 8.2 Small Business Program（SBP）

- **资格**：日历年度内总 proceeds < $1M USD（所有 App 合并）
- **入口**：ASC → Apple Developer Program → Small Business Program → 申请
- **时效**：申请月起生效（非追溯）；如年度 proceeds 超过 $1M，**次年** 1 月自动回到 30%/25%
- **地区**：全球适用；中国区 SBP 从 2026-03-15 起由 15% → 12%

### 8.3 中国区 2026-03-15 下调详情

见 `../market-overrides/china.md` §7.3。关键点：
- 仅中国大陆 App Store storefront
- 标准 30%→25%；SBP / Mini Apps Partner Program 15%→12%；订阅第二年 loyalty rate 15%→12%
- 自动生效，**无需重新签署协议**
- 其他地区费率不变
- ✅ Apple Developer News 2026-03-12 正式公告（[developer.apple.com/news/?id=dadukodv](https://developer.apple.com/news/?id=dadukodv)）；Bloomberg / TechCrunch 2026-03-13 跟进报道

### 8.4 EU DMA 新商业模式下的费用结构（2026-01-01+）

EU 开发者可选**保留旧条款**（30%/15% + 0 CTF）或**切换新条款**（降佣金 + CTC 5% + Acquisition/Store Services）。详细对比见 `../market-overrides/eu-eea.md` §3 和 `../operations/eu-dma-alternatives.md` §6。

### 8.5 对定价 / 财务建模的影响

| 建模项 | 是否需要重算 |
|--------|-------------|
| 中国区 LTV / ROI（2026-03-15 之后）| ✅ 必须重算（net revenue +5pp 或 +3pp）|
| 中国区订阅定价 | ⚠️ 无需调价，但净收入提升；可选择降价让利或维持 |
| 全球（非中国非 EU）LTV | ❌ 不需变，30%/15% 维持 |
| EU LTV（2026-01-01+） | ✅ 按是否切换新条款分别建模 |
| 美区外部购买链接 LTV | ⚠️ 待 Apple 最新公告；诉讼持续影响 |

**来源**：
- ✅ 中国区费率下调（含 loyalty rate 15→12%）：[Apple Developer News 2026-03-12](https://developer.apple.com/news/?id=dadukodv)；媒体解读 [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-13/apple-lowers-app-store-cut-to-25-from-30-in-china-to-fend-off-local-regulators) / [TechCrunch](https://techcrunch.com/2026/03/13/apple-drops-commission-rates-in-china-25-percent/)
- ✅ Small Business Program: [Apple Developer](https://developer.apple.com/app-store/small-business-program/)
- ✅ 订阅 loyalty rate: [Auto-Renewable Subscriptions](https://developer.apple.com/app-store/subscriptions/)

---

## 九、Offer Codes / Promo Codes（优惠码体系）

### 9.1 两套体系的区别与现状（2026-04 更新）

| 体系 | 用途 | 支持的 IAP 类型 | 状态 |
|------|------|--------------|------|
| **IAP Promo Codes** | 媒体发放、免费赠送 | 历史上支持 consumable / non-consumable / non-renewing subscription；Auto-Renewable Subscription **不支持** | ⚠️ **已弃用**：2026-03-26 新生成 cutoff，不再新增支持 |
| **Offer Codes** | 订阅引流、Winback、Retention | **2025-10-29 起**扩展到 consumable / non-consumable / non-renewing subscription（此前仅 Auto-Renewable Subscription） | ✅ 推荐使用 |
| **App Store Promo Codes（免费下载码）** | 付费 App 免费下载 | 付费 App 本体 | ✅ 持续可用 |

### 9.2 Offer Codes 扩展细节（2025-10-29+）

自 **2025-10-29** Apple Developer News 起，Offer Codes 支持全部 IAP 类型：

| IAP 类型 | 支持 Offer Codes? | 典型用例 |
|---------|------------------|---------|
| Auto-Renewable Subscription | ✅（原生） | 免费试用延长、首月折扣 |
| Non-Renewing Subscription | ✅（**2025-10-29 新增**） | 赛季通行证首购优惠 |
| Consumable | ✅（**2025-10-29 新增**） | 金币包满减、限时促销 |
| Non-Consumable | ✅（**2025-10-29 新增**） | 解锁功能的首发优惠 |

**生效路径**：ASC → Monetization → Subscriptions / In-App Purchases → Offer Codes → 创建 Campaign → 生成 alphanumeric codes 或 custom codes。

### 9.3 Offer Codes 调用代码（StoreKit 2）

```swift
import StoreKit

// iOS 16+ 唤起系统 Offer Code Redemption Sheet
try await AppStore.presentOfferCodeRedeemSheet(in: scene)

// 或使用 SwiftUI modifier（iOS 16+；completion 是同步回调）
SomeView()
    .offerCodeRedemption(isPresented: $showRedeem) { result in
        switch result {
        case .success:
            // 兑换成功；完成处理需要放在 Task 中异步执行
            Task { await refreshPurchases() }
        case .failure(let error):
            print("Redeem failed:", error)
        }
    }
```

⚠️ `offerCodeRedemption` 的 completion 是 `@MainActor (Result<Void, Error>) -> Void`（非 async）；在其中调用 async 逻辑必须 `Task { ... }` 包裹。兑换后真实 entitlement 建议通过 `Transaction.updates` 统一处理（见 §六.订阅状态管理）。具体 scene 参数类型与可用修饰符以当前 SDK 为准。

### 9.4 Promo Codes 弃用迁移

**2026-03-26 cutoff** 之前已生成的 IAP Promo Codes：
- 仍然可以兑换，直到过期（最长 28 天）
- 不能再生成新 codes

**迁移建议**：
- [ ] 媒体 / 评测发放：改用付费 App Promo Codes 或 Offer Codes
- [ ] 赠送场景：改用 Offer Codes（可自定义金额与次数）
- [ ] Refund 场景：不应使用任何 promo 体系，走 [Refund API](https://developer.apple.com/documentation/appstoreserverapi/request_a_refund) 或 ASC 审批
- [ ] Winback campaigns 改用 [Win-Back Offers](https://developer.apple.com/documentation/storekit/win-back_offers)（iOS 18+）

### 9.5 常见坑

- [ ] ⚠️ **混淆 Offer Codes / Promo Codes / App Store Promo Codes** 三者：体系不同、适用 IAP 类型不同
- [ ] Offer Codes Campaign 同时支持最多 **999,000 codes**，超过需拆分 campaign
- [ ] Custom offer codes 可让用户输入易记字符（如 `WELCOME2026`），但需在同一 campaign 内唯一
- [ ] 一个 Apple ID **一生只能用一次** 相同 Offer Code；重复兑换会返回 `.offerAlreadyUsed`

**来源**：
- ✅ [Apple: Offer Codes Overview](https://developer.apple.com/app-store/subscriptions/#offer-codes)
- ✅ [Apple Developer: Set up offer codes](https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-offer-codes)
- ✅ [StoreKit: presentOfferCodeRedeemSheet](https://developer.apple.com/documentation/storekit/appstore/presentoffercoderedeemsheet(in:)/)
- ✅ 2025-10-29 扩展到全部 IAP 类型：[Apple Developer News 2025-10-29: Enhancements to help you submit and market your apps and games](https://developer.apple.com/news/?id=gf6mgrs6)
