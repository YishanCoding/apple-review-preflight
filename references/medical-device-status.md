# 医疗器械状态声明指南

> 覆盖 App Store Connect 医疗器械状态声明要求、适用范围、FDA/EU MDR 分类界定、ASC 填写指引及与条款 1.4 的关系。
> 关键截止日期：新 App 立即生效（2026-03-26 起）；**存量 App 必须在 early 2027 前声明**。

---

## 一、背景与时间线

2026 年 3 月 26 日，Apple 宣布在 EEA（欧洲经济区）、英国和美国区域要求特定类别的 App 在 App Store Connect 中声明其是否为受监管的医疗器械。

| 时间点 | 要求 |
|-------|------|
| 2026-03-26 | 新 App（满足触发条件）上传时必须声明医疗器械状态 |
| early 2027 | 存量 App（满足触发条件）必须完成声明，否则可能影响更新和分发 |

**来源**：[Apple Developer News](https://developer.apple.com/news/?id=nyqbfz1y) / [ASC Help: Declare regulated medical device status](https://developer.apple.com/help/app-store-connect/manage-app-information/declare-regulated-medical-device-status)

---

## 二、哪些 App 需要声明

满足**以下任一条件**的 App 必须声明医疗器械状态：

| 触发条件 | 说明 |
|---------|------|
| App 分类为 Health & Fitness 或 Medical | ASC 中 Primary 或 Secondary Category 为这两个分类 |
| 年龄分级问卷中「Medical / Treatment Information」选择了 Frequent/Intense | 即使 App 不在 Health & Fitness / Medical 分类下 |

**适用地区**：EEA（27 个 EU 成员国 + 冰岛、列支敦士登、挪威）、英国、美国

### 2.1 不适用的情况

- App 不分发到 EEA / UK / US
- App 分类不是 Health & Fitness 或 Medical，且年龄分级中未勾选频繁医疗/治疗信息
- 纯健身记录 App（不涉及医疗声明）通常仍需声明，但选择「不是医疗器械」即可

---

## 三、医疗器械 vs 健康 App 的分类界定

### 3.1 什么是受监管的医疗器械

| 地区 | 监管框架 | 典型分类 |
|------|---------|---------|
| 美国 | FDA 21 CFR Part 820 | Class I（低风险）/ Class II（中风险）/ Class III（高风险） |
| EU/EEA | EU MDR (2017/745) | Class I / IIa / IIb / III |
| 英国 | UK MDR 2002（MHRA）| Class I / IIa / IIb / III |

### 3.2 判定流程

```
App 是否具有以下任一功能？
├── 诊断疾病或健康状况 → 可能是医疗器械
├── 监测生命体征用于临床决策 → 可能是医疗器械
├── 提供治疗建议（非通用健康建议） → 可能是医疗器械
├── 控制/连接医疗硬件设备 → 可能是医疗器械
└── 仅记录/展示运动/饮食/睡眠数据 → 通常不是医疗器械
```

### 3.3 常见场景分类

| App 功能 | 是否医疗器械 | 说明 |
|---------|------------|------|
| 步数/卡路里追踪 | ❌ 不是 | 通用健康记录 |
| 心率监测（仅展示数据） | ❌ 不是 | 不做临床判断 |
| 心率异常检测并建议就医 | ✅ 可能是 | 涉及诊断辅助 |
| BMI 计算器 | ❌ 不是 | 通用计算 |
| 血糖管理 + 胰岛素剂量建议 | ✅ 是 | 治疗辅助 |
| 冥想/正念 | ❌ 不是 | 通用健康 |
| CBT 心理治疗程序 | ✅ 可能是 | 视具体声明 |
| 视力检测 | ✅ 可能是 | 诊断辅助 |
| 连接蓝牙血压计并展示数据 | ✅ 可能是 | 视是否做临床判断 |
| 女性经期追踪 | ❌ 不是 | 通用健康记录 |
| 排卵预测用于避孕 | ✅ 可能是 | 涉及医疗声明 |

**关键原则**：如果 App 的功能描述中包含「诊断」「检测」「治疗」「预防」等医疗词汇，大概率需要声明为医疗器械或至少认真评估。

---

## 四、ASC 填写指引

### 4.1 在 App Store Connect 中操作

1. 登录 [App Store Connect](https://appstoreconnect.apple.com)
2. 选择 App → App Information
3. 找到「Regulated Medical Device Status」（部分地区显示为「受监管医疗器械状态」）
4. 选择适用声明

### 4.2 声明选项

| 选项 | 适用场景 | 需要额外信息 |
|------|---------|------------|
| **不是医疗器械** | App 不具备医疗器械功能 | 无 |
| **是医疗器械** | App 具有受监管的医疗器械功能 | 需要提供以下信息 |

### 4.3 声明为「是医疗器械」时需要的信息

| 地区 | 必填信息 |
|------|---------|
| 美国 | FDA Registration Number、510(k) Number 或 De Novo Number（如适用）、设备分类 |
| EU/EEA | EU MDR 注册信息、CE 标志声明、Notified Body 编号（Class IIa 及以上）|
| 英国 | MHRA 注册信息、UKCA 标志声明 |
| 所有地区 | Instructions for Use（使用说明）的 URL |

### 4.4 App Store 展示效果

声明为医疗器械的 App，其 App Store 产品页会显示：
- 「Regulated Medical Device」标签
- 监管信息（注册号等）
- 使用说明链接

---

## 五、与条款 1.4 的关系

### 5.1 条款 1.4 原文要点

> 要点摘述：涉及医疗诊断或治疗的 App 必须符合适用的监管要求，不得鼓励用户以损害健康的方式使用设备。

条款 1.4 要求任何涉及医疗诊断或治疗建议的 App 必须符合适用的监管要求。这与医疗器械状态声明是**互补关系**：

| 维度 | 条款 1.4 | 医疗器械状态声明 |
|------|---------|----------------|
| 性质 | 审核规则（人工判断） | ASC 系统字段（声明制） |
| 检查时点 | 审核阶段 | 上传/提交阶段 |
| 后果 | 拒审 | 无法提交（early 2027 后）|
| 适用范围 | 全球 | EEA / UK / US |

### 5.2 合规矩阵

| 场景 | 条款 1.4 | 医疗器械声明 | 风险 |
|------|---------|------------|------|
| 健身记录 App，不做医疗声明 | ✅ 通过 | 选「不是医疗器械」| 低 |
| 健身 App 但元数据含「检测」字样 | ⚠️ 可能被质疑 | 需认真评估 | 中 |
| 医疗 App 但未获 FDA/CE | ❌ 拒审 | 无法选「是医疗器械」| 高 |
| 医疗 App 且已获 FDA/CE | ✅ 通过 | 选「是医疗器械」+ 填监管号 | 低 |
| 选「不是医疗器械」但实际做诊断 | ❌ 1.4 拒审 | 虚假声明风险 | 极高 |

---

## 六、审核 Checklist

### 提交前必检

- [ ] **1.4**：App 元数据和 UI 中不包含「诊断」「治疗」「预防」等医疗声明（除非有监管批准）
- [ ] **ASC 要求**：已填写「Regulated Medical Device Status」（如分发到 EEA/UK/US）
- [ ] **ASC 要求**：如选「是医疗器械」：FDA / EU MDR / MHRA 注册信息已准备
- [ ] **ASC 要求**：如选「是医疗器械」：Instructions for Use URL 已配置且可公开访问
- [ ] **ASC 要求**：年龄分级问卷中「Medical / Treatment Information」如实填写
- [ ] **2.3.1**：App 描述中的健康相关声明用词准确（「帮助了解趋势」而非「诊断」）
- [ ] **HealthKit** 数据使用（如有）符合 5.1.3 要求（不用于广告、不出售）

### 常见问题

| 场景 | 风险 | 建议 |
|------|------|------|
| 存量健康 App 尚未声明 | 2027 前必须完成 | 尽早评估并声明 |
| 不确定是否为医疗器械 | 中 | 咨询法律/监管顾问；保守起见可先选「不是」但确保元数据无医疗声明 |
| App 连接蓝牙健康设备 | 高 | 需明确设备本身是否为 FDA/CE 注册的医疗器械 |
| 使用 Apple Watch 传感器数据 | 中 | 展示数据不触发，分析数据并给建议可能触发 |

---

## 七、参考链接

- [Apple Developer News: Regulated medical device apps](https://developer.apple.com/news/?id=nyqbfz1y)
- [ASC Help: Declare regulated medical device status](https://developer.apple.com/help/app-store-connect/manage-app-information/declare-regulated-medical-device-status)
- [App Store Review Guidelines 1.4](https://developer.apple.com/cn/app-store/review/guidelines/#physical-harm)
- [FDA: Mobile Medical Applications](https://www.fda.gov/medical-devices/digital-health-center-excellence/device-software-functions-including-mobile-medical-applications)
- [EU MDR 2017/745](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
- 相关文件：`../by-app-type/health-fitness.md`（健康类 App 专项）、`../checks/review-failure-map.md`
