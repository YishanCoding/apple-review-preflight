# 英国 App Store 特殊要求

> 覆盖 Brexit 后独立监管、Online Safety Act 2023、UKGC 博彩许可、MHRA 医疗器械转型期规则，以及 iOS 26.4 英国系统级 18+ 年龄验证。
> 本文件仅列出英国（UK）地区与全球通用规则不同或额外的要求。UK 不属于 EU/EEA，EU 特有规则（DMA、GDPR、ePrivacy）在 UK **均不适用**。

---

## 一、脱欧后的独立监管

### 1.1 常见误区澄清

| 误区 | 实际情况 |
|------|---------|
| 「UK 是 EU 的一部分」 | ❌ 2020-01-31 起 UK 退出 EU，2020-12-31 过渡期结束 |
| 「UK 适用 GDPR」 | ❌ UK 适用 **UK GDPR** + **Data Protection Act 2018** |
| 「UK 适用 DMA」 | ❌ DMA 不适用；UK 有 Digital Markets, Competition and Consumers Act 2024 (DMCC) |
| 「UK 适用 ePrivacy」 | ❌ UK 适用 **PECR**（Privacy and Electronic Communications Regulations） |
| 「App Store EU 条款覆盖 UK」 | ❌ Apple 的 EU/EEA 替代市场 / 外部购买链接**不在 UK 生效** |

### 1.2 UK 独立监管体系速览

| 领域 | EU 法规 | UK 对应法规 | 监管机构 |
|------|--------|------------|---------|
| 数据保护 | GDPR | UK GDPR + DPA 2018 | ICO |
| 电子通信 | ePrivacy Directive | PECR 2003 | ICO |
| 数字市场 | DMA | DMCC Act 2024 | CMA |
| 数字服务 / 内容 | DSA | Online Safety Act 2023 | Ofcom |
| 医疗器械 | EU MDR / IVDR | UK MDR 2002 + MHRA reforms | MHRA |
| 博彩 | 各成员国 | Gambling Act 2005 | UKGC |

### 1.3 Apple 在 UK 的特殊待遇

- **不提供**替代 App 市场 / Web Distribution（EU 专属）
- **不提供** EU 区的 StoreKit External Purchase Link Entitlement
- **提供**系统级年龄验证（iOS 26.4 起，见第五节）—— UK 是 Apple 首个推出此功能的欧洲市场

---

## 二、Online Safety Act 2023（OSA）

### 2.1 立法与实施阶段

OSA 于 2023-10-26 获皇家御准，Ofcom 分阶段实施：

| 阶段 | 时间 | 主要责任 |
|------|------|---------|
| Phase 1：Illegal Harms | 2025-03-17 起强制执行 | 非法内容风险评估 + 移除义务 |
| Phase 2：Child Safety | 2025 年中起 | 儿童保护评估 + 高度合规措施 (HEAA) |
| Phase 3：Transparency | 2025-2026 | 大型平台透明度报告等 |

**来源**：[Ofcom: Guide for services](https://www.ofcom.org.uk/online-safety/information-for-industry/guide-for-services)、[gov.uk: OSA explainer](https://www.gov.uk/government/publications/online-safety-act-explainer/online-safety-act-explainer)

### 2.2 哪些 App 受 OSA 约束

| 服务类型 | 典型 App | OSA 是否适用 |
|---------|---------|-------------|
| User-to-User (U2U) | 社交、论坛、聊天、UGC 视频 | ✅ 适用 |
| Search Services | 搜索引擎、聚合搜索 | ✅ 适用 |
| Pornography | 成人内容 | ✅ 严格适用（HEAA 强制） |
| 纯 1 对 1 通讯 | 仅端到端私信 | ⚠️ 部分豁免，以 Ofcom 最终指引为准 |
| 纯工具 App | 计算器、记事本 | ❌ 通常不适用 |
| 游戏内聊天 | 多人在线游戏 | ✅ 适用（U2U 功能） |

### 2.3 与 Apple 审核的关联

OSA 不是 App Store 审核条款，但：

- 若 Ofcom 命令下架，Apple 将按 Section 5 Legal（本地法律合规）在 UK 区移除
- 年龄分级须与 OSA 儿童保护措施一致（见 `../references/store-metadata-compliance.md`）
- UGC App 建议在 App Review Notes 中标明 OSA 合规状态
- 罚款：全球营业额 10% 或 £1800 万（取高者）；高管可承担刑责
- ⚠️ 经验规则：知悉违法内容须「迅速」移除，无统一小时 SLA，以 Ofcom 指引为准

---

## 三、UKGC（UK Gambling Commission）

### 3.1 博彩 App 许可证要求

向 UK 用户提供真钱博彩必须持 UKGC 许可证：

| 许可证 | 适用对象 |
|--------|---------|
| Remote Operating Licence | 博彩运营方 |
| Remote Gambling Software Licence | 游戏 / 引擎供应商 |
| Personal Management Licence | 关键岗位人员 |

### 3.2 与 Apple Guideline 5.3.3 / 5.3.4 的关联

- [ ] App 由运营方（licensee）实名提交（5.3.4）
- [ ] App Review Notes 注明 **UKGC Account Number**（5.3.4）
- [ ] 地理围栏：非 UK 用户不可访问（5.3.4）
- [ ] 最低年龄 18+（OSA 要求 HEAA 年龄验证）
- [ ] App 内嵌入 **GamStop** 自我排除接入点
- [ ] 不得用 IAP 购买筹码 / 虚拟货币用于真钱博彩（5.3.3）

### 3.3 Apple 技术要求

| 要求 | 说明 |
|------|------|
| 原生 iOS | ⚠️ 经验规则：历史上 Apple 要求博彩为原生 iOS（非 HTML5 壳），以 Apple 最新公告为准 |
| 免费下载 | App 免费（5.3.4 要求；不可收取付费下载或订阅） |
| 不得使用 IAP 作为筹码 | 真钱筹码走外部支付（信用卡 / 银行），不得通过 IAP 购买筹码（5.3.3） |
| 区域限制 | ASC 仅开启 UK / 其他持牌地区 |

**来源**：[Apple Guideline 5.3](https://developer.apple.com/app-store/review/guidelines/#5.3)、[UKGC: Licensing](https://www.gamblingcommission.gov.uk/licensees-and-businesses)

---

## 四、MHRA（医疗器械软件）

### 4.1 Post-Brexit 监管现状

UK 不再适用 EU MDR / IVDR。MHRA 当前为**过渡承认 + 即将改革**：

| 路径 | 适用范围 | 有效期 |
|------|---------|-------|
| CE 标识（EU MDR） | GB（英格兰、威尔士、苏格兰） | ⚠️ 延长至 **2028-06-30 或 2030-06-30**（按风险等级）；MHRA 2025 年咨询「无限期承认」中 |
| UKCA 标识 | GB | 持续有效 |
| CE 标识（EU MDR） | 北爱尔兰（NI） | 持续（Windsor Framework） |

**来源**：[MHRA medical devices](https://www.gov.uk/topic/medicines-medical-devices-blood/medical-devices-regulation-safety)、[MHRA indefinite recognition consultation](https://www.lw.com/en/insights/uk-mhra-launches-consultation-on-indefinite-recognition-of-ce-marked-medical-devices)

### 4.2 软件即医疗器械（SaMD）

- MHRA 在 GB 仍依 UK MDR 2002 将软件分类为医疗器械（⚠️ 待实测：新 UK 专属规则生效后可能微调）
- 境外厂商须指定 **UK Responsible Person**
- 与 Apple Guideline 1.4.1 / 5.1.1 叠加执行，详见 `../references/medical-device-status.md`

### 4.3 提交资料

| 场景 | App Review Notes 附件 |
|------|---------------------|
| 健康 App（非医疗器械） | 隐私政策 + 免责声明 |
| GB 区 SaMD | MHRA 注册号 + UKCA / 过渡期 CE 证书 |
| 仅 NI | EU MDR CE 证书 |

---

## 五、iOS 26.4 英国系统级年龄验证

### 5.1 概述（2026-04-01 上线）

Apple 在 iOS 26.4 为 UK 启用**设备级 18+ 年龄验证**——Apple 自发推出，响应 UK 儿童保护政策（非 OSA 直接强制）：

| 项目 | 说明 |
|------|------|
| 触发时机 | iOS 26.4 升级后首次使用 |
| 验证方式 | 自动（Apple 账号历史 + 支付）或手动（信用卡 / 驾照 / PASS ID） |
| 未验证后果 | 无法下载 / 访问 18+ 分级 App |
| 分级联动 | ASC 年龄分级 18+ 的 App 自动触发 |

**来源**：[Apple: Age assurance developer Q&A](https://developer.apple.com/support/age-assurance/) ✅、[Apple Support: UK Apple Account age requirements](https://support.apple.com/en-us/126788) ✅

### 5.2 开发者职责

| 职责 | 说明 |
|------|------|
| UI 实现 | ✅ Apple 处理系统弹窗，开发者无需实现年龄询问 |
| 分级准确性 | ⚠️ 必须：虚报分级（成人内容标 12+）将导致下架 |
| API 调用 | 18+ App 须在 App 内调用 **DeclaredAgeRange API** 检查，不能仅靠 ASC 分级 |
| Xcode | 须 Xcode 26.2+，链接 `DeclaredAgeRange` 框架 |

### 5.3 DeclaredAgeRange API

**⚠️ 以下为流程结构示意，非逐字可编译代码**；具体类型名、属性/方法签名、枚举 case、请求参数以 [Apple 开发者文档](https://developer.apple.com/documentation/declaredagerange) 和 Xcode 26+ 最新 SDK 为准（iOS 26.4 新增框架，API 仍可能调整）。

```swift
import DeclaredAgeRange

// 概念流程：
// 1. 查询本 App 所在地区 / 分级需要哪些 regulatory features
//    （由 AgeRangeService 的单例属性返回，用 try await 取值）
// 2. 若需要年龄门，判断当前账号是否具备调用资格
//    （家长同意、Apple ID 设置、区域是否启用等前置条件）
// 3. 发起一次 age-range 请求，系统弹窗展示已声明年龄段
// 4. 根据返回的 age-range 上下限判断 18+：
//      upperBound < 18 → 未成年
//      lowerBound >= 18 → 成年
//    用户拒绝共享时按"未成年"保守处理或走家长审批

// 伪代码：
// let features = try await AgeRangeService.shared.requiredRegulatoryFeatures
// let eligible = try await AgeRangeService.shared.isEligibleForAgeFeatures
// let response = try await AgeRangeService.shared.requestAgeRange(ageGates: [18], in: scene)
// switch response { ... }
```

核心原则（[Apple](https://developer.apple.com/support/age-assurance/) ✅）：
- Apple 仅**确认并分享**年龄；**执行责任在开发者**
- 家长可通过 Screen Time 覆盖分级（需在 App 内妥善处理）

### 5.4 与 OSA 的关系

- iOS 26.4 年龄验证**不等同于** OSA 的 HEAA（highly effective age assurance）
- 色情 App 等严管类**仍须自行**接入第三方年龄验证服务
- Apple 系统级验证可作**辅助证据**，不免除 OSA 义务

---

## 六、数据驻留 / 跨境传输

### 6.1 UK → 其他地区

| 目的地 | 机制 |
|-------|------|
| EEA（EU + 冰岛、挪威、列支敦士登）| UK 单方 adequacy 决定 ✅ 自由传输 |
| 美国 | **UK Extension to EU-US DPF**（2023-10-12 起）；接收者未 DPF 认证则用 IDTA / UK Addendum to SCC |
| 其他 adequate 国家 | 以 ICO 清单为准（Japan、韩国、Israel 等） |
| 其他国家 | **IDTA** 或 **UK Addendum to EU SCC** + TRA（Transfer Risk Assessment） |

**来源**：[ICO: International transfers](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/)

### 6.2 EU → UK

2021-06 EU adequacy decision 生效；2025-07-22 EU 公布新草案延续至 **2031 年**（⚠️ 待最终通过）。UK 若通过 DUA Act 大幅改革 UK GDPR，可能触发 EU 审查。

### 6.3 UK GDPR 与 EU GDPR 差异点

| 项目 | EU GDPR | UK GDPR |
|------|---------|---------|
| 儿童数字同意年龄 | 16（成员国可下调至 13） | **13** |
| 监管机构 | 各成员国 DPA | **ICO** 统一 |
| 罚款上限 | €2000 万 / 全球营业额 4% | £1750 万 / 全球营业额 4% |

### 6.4 Children's Code（AADC）

ICO 的 Age Appropriate Design Code（2021 生效）对面向 / 可能触达儿童的 App 强制 15 项标准：默认最高隐私、数据最小化、Profiling 默认关闭、禁止 nudge 儿童降低隐私。与 Apple 1.3 / Kids Category 叠加（见 `../by-app-type/kids.md`）。

---

## 七、提交前 UK 专项 checklist

- [ ] **UK GDPR**：隐私政策列 ICO + UK Representative（开发者位于 UK 外时）
- [ ] **UK GDPR**：儿童同意年龄设为 **13 岁**（非 EU 的 16 岁）
- [ ] **PECR**：Cookie / tracking 符合 Regulation 6（opt-in）
- [ ] **OSA**（U2U / 搜索类）：已完成 illegal content risk assessment 并留档
- [ ] **OSA**（涉儿童）：已完成 children's access assessment 与 HEAA
- [ ] **OSA**：App 内提供违法内容举报机制（5.1.1 / 1.2）
- [ ] **UKGC**（博彩）：Review Notes 注明 UKGC Account Number（5.3.4）；GamStop 接入
- [ ] **MHRA**（SaMD）：附 UKCA 或过渡期 CE 证书 + MHRA 注册号
- [ ] **iOS 26.4 年龄验证**：ASC 分级准确；混合内容接入 DeclaredAgeRange API
- [ ] **数据传输**：UK → US 用 DPF UK Extension 或 IDTA，文档齐备
- [ ] **Children's Code**：面向儿童 App 默认隐私最高

### UK 区特有拒审场景

| 场景 | 原因 | 修复 |
|------|------|------|
| 套用 EU 外部购买链接逻辑 | UK 不适用 DMA | 移除外部支付，改用 IAP |
| 隐私政策仅写 EU GDPR 未提 UK GDPR / ICO | 5.1.1 | 补 UK GDPR + DPA 2018 + ICO 联系方式 |
| UGC App 无举报 / 过滤机制 | 1.2 + OSA | 增加举报、屏蔽、审核 |
| 博彩 App 未写 UKGC 许可证号 | 5.3.4 | Review Notes 补充 |
| 18+ App 仅靠 ASC 分级 | Apple 审核 + OSA | 集成 DeclaredAgeRange 并在 App 内门控 |
| SaMD 使用过期 CE 证书 | Section 5 Legal + MHRA | 申请 UKCA 或确认在过渡承认期 |

---

## 八、关键来源

- [Apple: Age assurance developer Q&A](https://developer.apple.com/support/age-assurance/) ✅
- [Apple: DeclaredAgeRange framework](https://developer.apple.com/documentation/declaredagerange/) ✅
- [Apple Support: UK Apple Account age requirements](https://support.apple.com/en-us/126788) ✅
- [Apple: App Review Guidelines 5.3 Gaming, Gambling, and Lotteries](https://developer.apple.com/app-store/review/guidelines/#5.3) ✅
- [gov.uk: Online Safety Act explainer](https://www.gov.uk/government/publications/online-safety-act-explainer/online-safety-act-explainer)
- [Ofcom: Guide for services — complying with OSA](https://www.ofcom.org.uk/online-safety/information-for-industry/guide-for-services)
- [UKGC: Licensing for remote operators](https://www.gamblingcommission.gov.uk/licensees-and-businesses)
- [MHRA: Medical devices regulation](https://www.gov.uk/topic/medicines-medical-devices-blood/medical-devices-regulation-safety)
- [ICO: UK GDPR guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/)
- [ICO: International data transfers](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/)
- [ICO: Age Appropriate Design Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/)
- 相关文件：`../references/store-metadata-compliance.md`、`../references/medical-device-status.md`、`../by-app-type/kids.md`、`../policy/policy-updates-log.md`、`./eu-eea.md`
