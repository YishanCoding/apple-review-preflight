# 欧盟 / EEA App Store 特殊要求

> 覆盖 DMA 外部购买/侧载、GDPR + ePrivacy、Cookie Banner、替代 App 市场、外部支付 CTA 按钮规范及费用体系。
> 本文件仅列出 EU/EEA 地区与全球通用规则不同或额外的要求。
> 适用地区：27 个 EU 成员国 + 冰岛、列支敦士登、挪威（EEA）。

---

## 一、DMA（数字市场法）合规概述

自 2024 年 3 月起，Apple 被 EU 认定为「守门人」(gatekeeper)，必须遵守数字市场法 (Digital Markets Act)。Apple 于 2025 年 6 月宣布全面改革 EU 区 App Store 政策，2026 年 1 月 1 日起统一为新商业模式。

### 1.1 新商业模式（2026-01-01 起生效）

| 项目 | 说明 |
|------|------|
| 旧 CTF（Core Technology Fee）| ~~€0.50/安装/年~~（已取消） |
| 新 CTC（Core Technology Commission）| 5% 佣金（替代 CTF） |
| 初始获取费（Initial Acquisition Fee）| 2%（首次安装后 12 个月内通过 App Store 的交易） |
| Store Services Fee | 5%-13%（视使用的 App Store 服务层级） |
| 总佣金上限 | 最高约 20%（大型开发者）/ 10%-15%（小型开发者） |

**来源**：[Apple Developer News](https://developer.apple.com/news/?id=awedznci)

### 1.2 三种分发方式

| 方式 | 说明 | 费用 |
|------|------|------|
| App Store（使用 IAP） | 默认方式 | Store Services + CTC + Acquisition |
| App Store（外部支付链接） | 在 App 内引导用户到外部网站付款 | CTC + Acquisition（无 Store Services） |
| 替代 App 市场（Alternative Marketplace）| 通过第三方市场分发 | CTC |
| Web Distribution | 直接通过开发者网站安装 | CTC |

---

## 二、外部购买链接（StoreKit External Purchase Link）

### 2.1 概述

EU 区开发者可在 App 内放置链接，引导用户到外部网站完成数字内容购买，无需通过 IAP。

### 2.2 申请与配置

1. 在 Apple Developer Portal 申请 `StoreKit External Purchase Link Entitlement (EU)`
2. EU 区无需特殊审批，申请即获得
3. 实现 StoreKit `ExternalPurchaseLink` API

### 2.3 外部支付 CTA 按钮规范

Apple 对外部购买链接有严格的 UI 规范：

| 规范 | 要求 |
|------|------|
| 披露页 | 点击外部链接前必须展示系统披露页（system disclosure sheet） |
| 内容 | 披露页告知用户将离开 App，Apple 不负责外部交易 |
| 位置 | 外部购买链接可放在 App 内任意位置 |
| 限制 | ⚠️ 待实测：Apple 2026 新商业模式下 IAP 和外部链接可在同一 App 中共存，但系统披露页始终生效。以 Apple 最新文档为准 |
| 样式 | 无特殊按钮样式要求，但必须触发系统披露页 |

### 2.4 代码示例

```swift
import StoreKit

// EU 区外部购买链接
if ExternalPurchaseLink.canOpen {
    // 系统会自动插入披露页
    try await ExternalPurchaseLink.open()
}
```

---

## 三、替代 App 市场（Alternative Marketplaces）

### 3.1 开发者可以做的事

| 能力 | 说明 |
|------|------|
| 申请成为替代 App 市场 | 需满足 €1M 担保函 + 合规要求 |
| 在替代 App 市场分发 App | 开发者可选择在第三方市场上架 |
| Web Distribution | 通过自己的网站直接分发 iOS App |

### 3.2 对普通开发者的影响

- 大多数开发者不需要关注替代 App 市场
- 如果希望同时在 App Store 和替代 App 市场上架，App 可包含不同的支付方式
- Web Distribution 需要申请 entitlement 并满足条件（开发者账号需有 2 年历史 + EU 用户安装量达标）

### 3.3 Notarization（公证）要求

所有通过替代 App 市场或 Web Distribution 分发的 App 仍需通过 Apple 的 **Notarization** 流程：

| 项目 | 说明 |
|------|------|
| 性质 | 恶意软件扫描 + 基本合规检查（非完整 App Review） |
| 检查内容 | 恶意代码、隐私清单、签名有效性 |
| 不检查内容 | UI 设计、功能完整性、业务规则（3.1 等） |
| 拒绝后果 | 无法在 EU 区安装（系统级阻止） |
| 时效 | 通常数小时内完成 |

**注意**：Notarization 不等于 App Review，但仍可能因隐私清单缺失、签名问题等被拒。

---

## 四、GDPR 合规

### 4.1 与 App Store 审核的关系

| GDPR 要求 | App Store 审核关联 | 条款 |
|----------|-----------------|------|
| 合法基础 | 隐私政策须声明处理数据的合法基础 | 5.1.1 |
| 数据主体权利 | App 须提供访问/删除/导出个人数据的功能 | 5.1.1(v) |
| 数据保护官（DPO） | 隐私政策须提供 DPO 联系方式（如适用）| 5.1.1 |
| 数据泄露通知 | 72 小时内通知监管机构 | — |
| 跨境传输 | 传输到 EU 以外需充分性决定 / SCC / BCR | 5.1.1 |

### 4.2 ePrivacy 指令（Cookie 相关）

| 要求 | 说明 |
|------|------|
| Cookie 同意 | 非必要 Cookie 需用户主动同意（opt-in） |
| 同意管理 | 需提供「接受」和「拒绝」同等突出的选项 |
| 撤回同意 | 用户必须能随时撤回 Cookie 同意 |
| App 内适用 | App 使用类 Cookie 技术（如 tracking SDK）同样适用 |

### 4.3 Cookie Banner / 同意弹窗最佳实践

```
首层弹窗：
┌──────────────────────────────────────┐
│ 我们使用 Cookie 和类似技术来改善体验  │
│                                      │
│  [管理偏好]  [全部拒绝]  [全部接受]   │
└──────────────────────────────────────┘

注意：
- 「全部拒绝」和「全部接受」按钮必须同等大小和颜色
- 不可使用 dark pattern（如把拒绝按钮做成灰色小字）
- 预勾选非必要 Cookie 违反 ePrivacy
```

---

## 五、ATT（App Tracking Transparency）在 EU 的特殊性

| 注意点 | 说明 |
|-------|------|
| ATT + GDPR 双重合规 | EU 用户同时受 ATT 和 GDPR 保护 |
| ATT ≠ GDPR 同意 | 获得 ATT 授权不等于 GDPR 合法基础，仍需独立的 GDPR 同意 |
| 拒绝 ATT 后 | 不可通过 fingerprinting 或其他方式追踪（Apple + GDPR 双重禁止） |
| ⚠️ 经验规则 | 建议先展示 GDPR 同意弹窗，再触发 ATT 弹窗 |

---

## 六、EU 区年龄验证

### 6.1 系统级年龄验证（iOS 26.4+）

从 2026 年起，Apple 在部分地区启用设备级年龄验证。EU/EEA 地区的具体时间表以 Apple 官方公告为准：

- 18+ 应用需系统级年龄验证
- 开发者无需额外实现，由系统处理
- 但年龄分级必须准确（见 `../references/store-metadata-compliance.md`）

> **注意**：英国（UK）不属于 EU/EEA，其年龄验证要求请关注 Apple 单独公告。

### 6.2 DSA（数字服务法）

| 要求 | 说明 |
|------|------|
| 未成年人保护 | 不可对已知未成年人投放定向广告 |
| 透明度报告 | 大型平台需发布内容审核透明度报告 |
| 违法内容举报 | 需提供举报违法内容的机制 |

---

## 七、审核 Checklist（EU/EEA 专项）

### 提交前必检

- [ ] **GDPR**：隐私政策包含合法基础、DPO 联系方式、数据主体权利说明
- [ ] **GDPR**：App 提供数据访问/删除/导出功能（5.1.1(v)）
- [ ] **ePrivacy**：非必要 tracking 在用户同意前不启动
- [ ] **ePrivacy**：Cookie/tracking 同意弹窗提供等同突出的「接受」和「拒绝」
- [ ] **ATT**：ATT 弹窗与 GDPR 同意分开处理
- [ ] **DMA（如使用外部购买链接）**：已申请 StoreKit External Purchase Link Entitlement (EU)
- [ ] **DMA**：外部购买链接正确触发系统披露页
- [ ] 年龄分级准确（EU 区年龄验证由系统处理）
- [ ] 如数据传输到 EU 以外：已有 SCC / 充分性决定 / BCR

### EU 区特有拒审场景

| 场景 | 原因 | 修复 |
|------|------|------|
| 外部购买链接未触发系统披露页 | DMA 合规要求 | 使用 StoreKit ExternalPurchaseLink API |
| 同一页面同时展示 IAP 和外部链接 | ⚠️ 待实测 | 2026 新规下可共存但需披露页；以 Apple 最新文档为准 |
| 隐私政策无 GDPR 条款 | 5.1.1 + GDPR | 补充合法基础、数据主体权利等 |
| 非必要 SDK 在同意前已加载 | ePrivacy 违规 | 延迟加载直到用户同意 |

---

## 八、费用对比速查表

| 开发者类型 | App Store + IAP | App Store + 外部链接 | 替代市场 / Web |
|-----------|----------------|-------------------|--------------|
| 大型（>$1M/年）| ~20% | ~7% | 5% |
| 小型（<$1M/年）| ~13% | ~7% | 5% |
| 免费 App | 0% | 0% | 0% |

*具体费率取决于使用的服务层级，以上为概算。详见 [Apple EU Business Terms](https://developer.apple.com/news/?id=awedznci)。*

---

## 九、参考链接

- [Apple: Updates for apps in the European Union](https://developer.apple.com/news/?id=awedznci)
- [StoreKit External Purchase Link](https://developer.apple.com/documentation/storekit/external-purchase-link)
- [DMA — Digital Markets Act](https://digital-markets-act.ec.europa.eu/)
- [GDPR Official Text](https://gdpr.eu/)
- 相关文件：`../references/storekit-iap.md`、`../guidelines/3-business.md`、`../checks/privacy-transparency-consistency.md`
