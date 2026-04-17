# EU DMA 下的替代分发实操

> 覆盖 EU/EEA 区替代分发三大途径（App Store / Alternative Marketplace / Web Distribution）的实操流程：Notarization、MarketplaceKit 集成、External Purchase Link、2026 新商业模式（CTC）与税务合规。
> 本文件聚焦「怎么做」；`../market-overrides/eu-eea.md` §3 覆盖政策层面背景。
> Baseline：Apple App Review Guidelines 2026-02-06 版 + Apple EU DMA 系列支持页。
> ⚠️ DMA 相关规则受欧盟诉讼、Apple 上诉及多次政策调整影响，本文所列金额、阈值、API 名称均以 Apple 最新官方文档为准。

---

## 一、三种替代分发途径对比

| 维度 | App Store（默认） | Alternative Marketplace | Web Distribution |
|------|------------------|------------------------|------------------|
| 谁能用 | 所有开发者 | 开发者在第三方市场上架；或自建市场运营方 | 开发者账号 ≥ 2 年 + EU 监管合规 + EU 下载量达标（详见 §4） |
| 审核 | 完整 App Review | Notarization（市场运营方额外审核） | Notarization |
| 签名 | Apple 签名 | Apple 签名 + Marketplace 签名 | Apple 签名 + 开发者域名证书 |
| 佣金 / 费用 | Store Services 5-13% + Acquisition 2% + CTC 5% | CTC 5% | CTC 5% |
| Notarization 必需 | ❌（走 Review） | ✅ | ✅ |
| CTC 2026 适用 | ✅（数字商品） | ✅ | ✅ |
| 需要申请 Entitlement | ❌（默认） | ✅ `ManagingAlternativeDistributions` / MarketplaceKit | ✅ Web Distribution Entitlement |
| 可在同一 App 共存 | — | ✅（开发者可同时在 App Store + Alt Marketplace 发布） | ✅ |
| 商业推广（宣传外部价格）| 需 External Purchase Link 申请 | 原生支持 | 原生支持 |
| 仅限 EU 设备 | ❌ | ✅ 仅 EU/EEA 27+3 国 | ✅ 仅 EU/EEA |

✅ Apple 官方：[Update on apps distributed in the European Union](https://developer.apple.com/support/dma-and-apps-in-the-eu/)

---

## 二、Notarization（公证）流程

### 2.1 与 App Review 的区别

| 维度 | App Review | Notarization |
|------|------------|--------------|
| 检查恶意软件 | ✅ | ✅ |
| 检查签名 / entitlements | ✅ | ✅ |
| 检查 Privacy Manifest | ✅ | ✅ |
| 检查基本 metadata 披露（developer name, screenshots, age rating）| ✅ | ✅（仅基本） |
| 审查 UI / 设计质量 | ✅ | ❌ |
| 审查功能完整性（2.1 Performance） | ✅ | ❌ |
| 审查业务规则（3.x IAP、4.x Design） | ✅ | ❌ |
| 审查内容政策（1.x Objectionable） | ✅ | ❌（仅非法/恶意内容） |
| 耗时 | 1-3 天 | 数小时（多数 < 1 小时） |
| 拒绝后果 | 不能上架 App Store | 无法在 EU 设备安装（系统阻止） |

⚠️ Notarization **不是** App Review 的替代品：Notarization 通过，不代表 App 通过了任何设计/内容审查。开发者仍对 App 的内容合规性负责。

### 2.2 流程

1. **申请 entitlement**（Alternative Marketplace 或 Web Distribution 场景）
   - Apple Developer Portal → Identifiers → 配置对应 entitlement
   - Web Distribution 需签署 Alternative Terms Addendum（如还未切到 2026 统一条款）
2. **确认 Apple Developer Program 会员状态**
   - 会员到期会导致 Notarization ticket 自动撤销
3. **本地构建 .ipa / Alternative Distribution Package**
   ```bash
   # Alternative Distribution Package（用于 Alt Marketplace / Web Distribution）
   xcodebuild -exportArchive \
     -archivePath ./build/MyApp.xcarchive \
     -exportPath ./build/ \
     -exportOptionsPlist ExportOptions-AlternativeDistribution.plist
   ```
   `ExportOptions-AlternativeDistribution.plist` 的 `method` 键需设为 `alternative-distribution`（⚠️ 以 Xcode 当前版本支持的字符串为准）。
4. **提交 Notarization**
   ```bash
   # Xcode GUI: Organizer → Distribute App → Alternative Distribution
   # 或命令行（⚠️ altool 已废弃，Apple 尚未在 iOS 侧公布稳定命令行；以 Xcode 集成流为准）
   ```
5. **等待 Notarization 审查**
   - 自动恶意扫描 + 基本合规检查
   - 失败时返回日志，修复后重新提交
6. **拿到 Notarization ticket**
   - Ticket 绑定到 build，发布时随 package 一起分发
   - Ticket 过期/撤销会导致用户无法安装新副本（已安装的继续可用）
7. **发布**
   - Marketplace：交给 Marketplace 运营方上架
   - Web Distribution：上传到自家域名 + 更新 manifest.json

### 2.3 Notarization 可能被拒的典型原因

- Privacy Manifest 缺失或 Reason Code 不合规（见 `../references/privacy-manifest.md`）
- 签名无效 / entitlement 未授予
- Bundle 包含已知恶意代码或已被吊销的证书
- Metadata 声明与实际 binary 不一致（如声明不收集位置但引用 CoreLocation）

---

## 三、Alternative Marketplaces（替代应用市场）

### 3.1 成为市场运营方的门槛

| 要求 | 细节 |
|------|------|
| Apple Developer Program 会员 | ✅ 必需 |
| 签署 Alternative Marketplace Addendum | ✅ |
| 财务担保二选一 | (a) 向 Apple 提供 **€1,000,000 standby letter of credit**（由 A 级银行开立）；或 (b) 成员两年且上一年 EU App Store app 安装量 ≥ 100 万 |
| MarketplaceKit 集成 | ✅ 必需 |
| 合规 / KYC 能力 | 运营方对入驻 App 做基本审核、身份核验 |
| 举报/下架机制 | 提供用户 flagging、违规 App 下架流程 |

⚠️ 金额与阈值依 Apple Alternative Terms Addendum，有 hn 讨论指出 €1M 本质是「劝退锁」([HN thread](https://news.ycombinator.com/item?id=39653965))。以 Developer Portal 最新条款为准。

### 3.2 MarketplaceKit 关键流程

运营方（Alt Marketplace）通过 `MarketplaceKit` 拉起 Notarized App 的**系统级**安装 UI。关键输入三元组：

1. **Alternative Distribution Package URL**（HTTPS）— 指向 Notarized `.ipa` / 分发包
2. **Install Verification Token**（JWS）— 运营方服务端签发，Apple 校验其合法性
3. **Account** — 当前已登录的市场账号标识

调用路径（⚠️ 以下为**结构示意**，非逐字可编译；具体类型名、初始化器、参数顺序以 [MarketplaceKit 官方文档](https://developer.apple.com/documentation/marketplacekit) 为准）：

```swift
import MarketplaceKit

// 概念示意：构造安装描述并提交给系统
// MarketplaceKit 提供 ActionButton（SwiftUI/UIKit，视版本） +
// 底层 AppLibrary.InstallationRequest 两种入口，两者接收的都是
// (alternativeDistributionPackage URL, installVerificationToken, account) 三元组。
// 用户点击后弹出 Apple 系统级安装确认（非开发者自定义 UI）。

let packageURL: URL = /* 从服务端获取 */
let token: String   = /* JWS install verification token */
let account: String = /* 当前账号 */

// 提交给 AppLibrary 触发系统安装流程（伪代码，签名以 Apple 文档为准）
// let request = AppLibrary.InstallationRequest(
//     alternativeDistributionPackageURL: packageURL,
//     installVerificationToken: token,
//     account: account
// )
// try await AppLibrary.current.requestAppInstallation(request)
```

⚠️ **重要约束**（Apple 确认）：
- 不存在 "按 bundle ID 直接安装" 的便捷 API — 必须用签名 package URL + verification token
- UI 必须使用 Apple 提供的 `ActionButton` 或系统 install sheet，不得自绘安装按钮并伪造系统弹窗
- Entitlement 名称以 Apple Developer Portal 最新 key 为准（历史上出现过 `com.apple.developer.marketplace-kit` 等不同写法），**不要依赖本文件引用的具体 key 名称，请以 Xcode 模板和 Apple 文档为准**

### 3.3 运营方责任清单

- [ ] 对入驻开发者做身份核验（legal entity, trader status under DSA）
- [ ] 审核 App Metadata（age rating, 数据收集披露）
- [ ] 提供违规 App 举报入口（DSA §16 要求）
- [ ] 响应 takedown 请求 (policy、IP、illegal content)
- [ ] 维护 MarketplaceKit 集成，保证 Notarized package 正确安装
- [ ] 向 EU 终端用户清晰披露运营方身份（营业地址、联系方式）

### 3.4 对「普通开发者」的影响

大多数开发者不需要自建市场。常见路径：

1. 选择在 Epic Games Store / AltStore PAL / Setapp Mobile / Aptoide 等已运营市场上架；
2. 继续留在 App Store，不参与 Alt Marketplace。

---

## 四、Web Distribution（网页直接分发）

### 4.1 资格要求

| 条件 | 细节 |
|------|------|
| 开发者账号年龄 | ≥ 2 年（以 enrollment 起算） |
| 账号类型 | Organization / Company（个人账号不可） |
| 法律实体 | 位于 EU 成员国，或在 EU 注册且受 DMA 管辖 |
| 历史下载量 | 至少 1 个 App 在过去 12 个月内于 EU 达到 **1,000,000 首次安装** |
| 税务 / 消费者权益 | 合规（⚠️ Apple 保留以合规记录否决资格的权利） |
| Entitlement | 需申请 Web Distribution Entitlement 并签署对应 addendum |

⚠️ 待实测：Apple 在 2025-06 更新中放宽了部分 Web Distribution 限制，但门槛（2 年 + 100 万安装）尚未公开取消。([ppc.land 2025-06-26](https://ppc.land/apple-expands-eu-app-store-alternatives-with-new-installation-features/))

### 4.2 技术实施

1. **App Store Connect → App → Distribution → Web Distribution** 启用
2. 将 `.ipa`（或 Alternative Distribution Package）通过 Notarization
3. 托管 package 到自有域名（**HTTPS 强制**）
4. 生成并托管 `manifest.json`：
   ```json
   {
     "bundleId": "com.example.myapp",
     "version": "1.2.0",
     "minOSVersion": "17.4",
     "packageURL": "https://example.com/downloads/MyApp-1.2.0.ipa",
     "notarizationTicketURL": "https://example.com/downloads/MyApp-1.2.0.ticket",
     "signature": "<JWS>"
   }
   ```
   ⚠️ 实际字段以 Apple MarketplaceKit / Web Distribution 文档为准（manifest schema 与 JWS 签名细节变动频繁）。
5. 页面用 Apple 提供的 `marketplace-kit://` URI scheme 拉起系统安装（iOS 17.5+ Safari / 部分受支持浏览器）：
   ```html
   <!-- Apple 文档方式：点击链接触发 iOS 系统级安装确认页 -->
   <a id="install" href="#">Install</a>
   <script>
     document.getElementById('install').addEventListener('click', (e) => {
       e.preventDefault();
       const params = new URLSearchParams({
         alternativeDistributionPackage: 'https://example.com/downloads/MyApp-1.2.0.ipa',
         installVerificationToken: '<SERVER-SIGNED-JWS>',
         account: '<current-user-account>'
       });
       window.location.href = 'marketplace-kit://install?' + params.toString();
     });
   </script>
   ```
   ⚠️ 待实测：`marketplace-kit://` scheme 参数名称和顺序以 [Apple Web Distribution 文档](https://developer.apple.com/support/dma-and-apps-in-the-eu/) 最新版为准。历史上有过 `manifestURL` 等命名，但当前 Apple 官方路径是"签名 package URL + 验证 token + 账号"三元组。
6. 用户点击后，iOS 弹出系统级安装确认（Apple 官方 UI，开发者不可自定义）。

### 4.3 Commercial 限制

- 仅限 EU/EEA 设备（根据 Apple ID region + 设备地理）
- 不能分发到非 EU 国家（即使用户在 EU）
- 广告、营销、分析 SDK 同样受 GDPR/ePrivacy 约束
- 涉及 IAP 或订阅：不能调用 StoreKit IAP（Web Distribution App 必须使用自己的支付系统，CTC 5% 仍适用）

---

## 五、External Purchase Links（站内购买外链）

### 5.1 Entitlement 申请

1. Developer Portal → Identifiers → Edit → 勾选 `com.apple.developer.storekit.external-purchase-link`
2. 签署 StoreKit External Purchase Link Entitlement (EU) Addendum
3. EU 区申请即获批（⚠️ 与美国、日本、韩国等其他地区的 EPL 条款不同）

### 5.2 正确 API

```swift
import StoreKit

// 正确：使用静态方法 open()
if ExternalPurchaseLink.canOpen {
    do {
        try await ExternalPurchaseLink.open()
        // 系统自动插入披露页（disclosure sheet）
    } catch {
        // 用户取消或无法打开
    }
}

// ❌ 错误：把 ExternalPurchaseLink 当构造函数
// let link = ExternalPurchaseLink(url: ...) // 编译不通过
```

### 5.3 Disclosure Screen（必需）

- 由**系统**自动呈现，开发者无法跳过或自定义
- 告知用户：即将离开 App、交易由第三方处理、Apple 不负责
- 用户点击「Continue」后才会跳转外链

### 5.4 Commerce Rules

| 场景 | 允许 | 备注 |
|------|------|------|
| 同一 App 同时存在 IAP 和 External Purchase Link | ✅（2025-06 后） | 以 Apple 最新条款为准 |
| External link 指向 web checkout | ✅ | 需合规 PSP |
| External link 指向其他 App（URL scheme） | ⚠️ 待实测 | Apple 2025-06 放宽为「destination of developer's choice」 |
| 在 link 旁展示 web 价格 | ✅ | 2024-08 起明确允许 |
| 跨 App 跳转 | ✅ | [Communication and promotion of offers](https://developer.apple.com/support/apps-using-alternative-payment-providers-in-the-eu/) |

### 5.5 与 DMA 其他条款关系

- 使用 External Purchase Link 不影响 Alt Marketplace / Web Distribution 资格
- 走 EPL 的 App 仍在 App Store 内，受 App Review 完整审核
- EPL 引流的交易产生 **Acquisition 2% + CTC 5%**（无 Store Services 费用）

---

## 六、2026 商业模式（CTF → CTC）

### 6.1 新旧对比

| 项 | 旧（Alternative Terms Addendum，2024-2025） | 新（2026-01-01 起统一条款） |
|----|---------------------------------------------|------------------------------|
| Core Technology Fee | €0.50 / 首次安装 / 年（超过 100 万安装后）| ❌ 取消 |
| Core Technology Commission（CTC） | — | ✅ 5%（数字商品/服务收入） |
| Initial Acquisition Fee | — | ✅ 2%（首次获客后 12 个月内，仅 App Store 渠道） |
| Store Services Fee | 10%/17% 两档 | 5% / 13% 两档（Tier 1 / Tier 2） |
| 总佣金概算（大开发者） | 17% + €0.50/install | ~20%（App Store + IAP） / ~7%（App Store + EPL） / 5%（Alt 渠道） |

✅ 来源：[Apple: Updates for apps in the European Union](https://developer.apple.com/news/?id=awedznci)、[RevenueCat: one entitlement, three fees, and CTF's 2026 sunset](https://www-docs.revenuecat.com/blog/growth/apple-eu-dma-update-june-2025/)

### 6.2 Accounting 含义

- **CTC 按收入计**：没有销售 = 没有 CTC（不再像 CTF 按安装数前置扣款）
- **Store Services Tier 2** 包含自动更新、自动推荐、搜索建议等「增值」服务；Tier 1 仅基础分发
- 2% Acquisition 仅适用「通过 App Store 获客的 12 个月内」首次安装用户
- **外部链接渠道**：CTC 5% + Acquisition 2%，无 Store Services

### 6.3 切换策略（误解最多）

⚠️ 业内常见误解：「只能选一次条款，不能回滚」。实际情况：

- 2026-01-01 前仍在旧 EU Alternative Terms Addendum 的开发者会被统一迁移到新条款；
- Apple 允许开发者在特定时间窗口内做 **一次** 主动切换（如：已 opt-in Alternative Terms 的开发者可以选择回到 Standard Terms，反之亦然）；
- ⚠️ 待实测：2026 年中后段是否允许再次切换，以 ASC 条款管理页为准；
- 建议：**不要为「观望费用」频繁切换**，签约条款变更通常不可撤销。

### 6.4 何时选新 vs 保留旧

| 场景 | 推荐 |
|------|------|
| 纯免费 App，安装量小 | 统一新条款（免费 App 零费用差别不大） |
| Free + IAP，EU 是主要市场 | 新条款 + External Purchase Link（~7% 总费用） |
| 超大体量免费 App（游戏、社交） | 比较 CTF €0.50 × 安装 vs CTC 5% × 收入 |
| 计划自建 Marketplace 或 Web Distribution | 必须走新条款（CTC） |

---

## 七、税务、银行、合规

### 7.1 VAT 代扣代缴变化

| 渠道 | Apple 是否代扣代缴 EU VAT | 开发者义务 |
|------|--------------------------|-----------|
| App Store（IAP） | ✅ | 无（Apple 作 MoR） |
| App Store + External Purchase Link | ❌（外部交易部分） | 开发者自行处理 VAT，注册 OSS 或各国税号 |
| Alternative Marketplace | ❌ | 开发者（或 Marketplace 运营方）自行处理 |
| Web Distribution | ❌ | 开发者自行处理 |

开发者需要：
- 注册 **EU OSS（One-Stop Shop）** 以一口径申报 27 国 B2C VAT；
- 或在每个销售国单独注册 VAT（不推荐）；
- 保存 10 年交易记录（EU VAT 法规）。

### 7.2 PSP（Payment Service Provider）选型要点

- 支持 **3DS2** 强认证（PSD2 SCA 要求）
- 支持 **EU local methods**：SEPA DD、iDEAL、Bancontact、Giropay、P24、Swish 等
- 能输出符合 Apple External Purchase Report 的对账数据（开发者需每月向 Apple 上报 EPL 交易）
- 常见选型：Stripe、Adyen、Paddle（MoR 模式，可替开发者处理 VAT）、Mollie、Lemon Squeezy

### 7.3 UK 不适用

- UK 不是 EU/EEA，**DMA 完全不适用**；
- UK App Store 仍使用标准 30%/15% 佣金、不支持 Alt Marketplace / Web Distribution / External Purchase Link (EU) Entitlement；
- UK 的竞争监管由 CMA（Competition and Markets Authority）负责，走独立流程（参考 Apple UK Market Investigation 公告）。

---

## 八、替代分发 Decision Matrix

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 大型游戏工作室，EU 收入占比高 | App Store + External Purchase Link | 保留 App Store 获客 + EPL 降低佣金至 ~7% |
| 专业工具 / 开发者工具（小众垂类） | App Store + 考虑 Setapp Mobile 等 | 垂类市场订阅制更友好 |
| 教育 App（学校批量分发） | Apple School Manager Custom App + App Store | DMA 渠道对 B2B 教育无额外价值 |
| 游戏模拟器 / Emulator | Alt Marketplace（AltStore PAL 等） | App Store 对模拟器政策仍严苛，Alt 市场更宽松 |
| 成人内容 / 18+ | Alt Marketplace 或 Web Distribution | App Store 禁止；Alt 渠道 + EU 年龄验证可合规 |
| 加密钱包 / 币圈工具 | 视合规审查 + Alt Marketplace 可选 | App Store 合规门槛高；Alt 渠道对地区金融牌照要求仍适用 |
| 自有流量大厂（>100 万 EU 下载）| Web Distribution 直连自家域名 | 跳过 App Store Services 费用，总成本最低（仅 CTC 5%） |
| 中小独立开发者 | App Store 默认 | Alt 分发的合规 / VAT / PSP 成本不划算 |

---

## 九、踩坑清单

1. **忘记 Notarization 在 version 更新后重新提交** — 每个 build 都要 Notarize，否则用户拿不到新版。
2. **Notarization ticket 过期 / 证书撤销** — 开发者离开 Apple Developer Program 或证书被吊销，已分发的 App 会在后续启动时被系统拦截。
3. **误用 ExternalPurchaseLink API** — 错把 `ExternalPurchaseLink` 当构造函数；正确是静态方法 `ExternalPurchaseLink.open()`，必须 `async`。
4. **未声明 MarketplaceKit entitlement** — Alternative Marketplace App 忘记在 provisioning profile 中声明 MarketplaceKit 相关 entitlement（具体 key 以 Xcode 模板和 Apple 文档为准），Notarization 会拒。
5. **VAT 代收义务遗漏** — 走 EPL / Alt Marketplace / Web Distribution 后，Apple 不再代扣 EU VAT，开发者忘记注册 OSS 被 EU 各国追税。
6. **同一 App 在 App Store 和 Alt Marketplace 使用不同 Bundle ID** — 安装会互相冲突 / 用户数据无法迁移。规划期就应决定是否同 Bundle ID 双渠道。
7. **Web Distribution 页面未使用 HTTPS 或 manifest.json 签名无效** — 系统级 install 拒绝。
8. **未处理 Notarization 拒绝日志** — Notarization 失败 ≠ 彻底无解，大部分因 Privacy Manifest / Reason Code 缺失，修复后即可通过（见 `../references/privacy-manifest.md`）。
9. **External Purchase Link 旁未遵守 commerce rules** — 如展示误导性「比 App Store 便宜 30%」文案；Apple 允许展示价格但禁止贬损性对比。
10. **把 Notarization 当 App Review** — 以为通过 Notarization 就无审核风险；实际 Alt 市场运营方 + EU 监管（DSA、GDPR、消费者权益指令）仍对内容负责。
11. **低估切换条款的不可逆性** — 签署 Alternative Terms Addendum 后在 2026 过渡期结束前未主动切换，会默认落到新条款；复杂场景先咨询税务/法务。

---

## 十、关键来源

- ✅ [Apple: Update on apps distributed in the European Union](https://developer.apple.com/support/dma-and-apps-in-the-eu/)
- ✅ [Apple: Updates for apps in the European Union（2025-06-26）](https://developer.apple.com/news/?id=awedznci)
- ✅ [Apple: Alternative payment options on the App Store in the European Union](https://developer.apple.com/support/alternative-payment-options-on-the-app-store-in-the-eu/)
- ✅ [Apple: Communication and promotion of offers on the App Store in the EU](https://developer.apple.com/support/apps-using-alternative-payment-providers-in-the-eu/)
- ✅ [Apple: Commissions, fees, and taxes for EU distribution](https://developer.apple.com/help/app-store-connect/distributing-apps-in-the-european-union/commissions-fees-and-taxes/)
- ✅ [Apple: Core Technology Fee（过渡期说明）](https://developer.apple.com/support/core-technology-fee/)
- ✅ [Apple: Updates to the StoreKit External Purchase Link Entitlement](https://developer.apple.com/news/?id=szrqxadx)
- ✅ [StoreKit ExternalPurchaseLink 类型文档](https://developer.apple.com/documentation/storekit/externalpurchaselink)
- ✅ [MarketplaceKit 文档入口](https://developer.apple.com/documentation/marketplacekit)
- ⚠️ [RevenueCat: EU DMA June 2025 解读](https://www-docs.revenuecat.com/blog/growth/apple-eu-dma-update-june-2025/)（第三方汇总）
- ⚠️ [DaringFireball: Apple DMA 政策分析](https://daringfireball.net/2025/06/apple_app_store_policy_updates_dma)（社区观点）
- 相关文件：`../market-overrides/eu-eea.md`、`./review-ops.md`、`../references/storekit-iap.md`、`../references/privacy-manifest.md`
