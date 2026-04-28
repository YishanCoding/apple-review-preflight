# 审核时长规律与最佳提交时机

> **读这个文件的场景**：想知道审核通常多久有结果、什么时候提交更快、节假日是否会延迟、以及如何读懂不同审核状态的时间信号。
> **最后验证时间**：2026-04

---

## 一、Apple 官方口径

| 项目 | 内容 | 来源 |
|------|------|------|
| 官方承诺 | "On average, 90% of submissions are reviewed in less than 24 hours." | ✅ [App Review](https://developer.apple.com/distribute/app-review/) |
| 多次提交时 | 如果需要多次提交才能解决问题，整体会拉长到几天 | ✅ [Tech Talk: Tips for preventing common review issues](https://developer.apple.com/kr/videos/play/tech-talks/10885/) |
| 排队顺序 | 提交不保证按顺序审核 | ✅ [Overview of submitting for review](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review) |

> ⚠️ "90% under 24 hours" 是整体平均，不是 SLA。统计看的是全体分布，不区分 App 类别或提交类型。开发者体感与官方数字差距大，主要因为：多轮重提的总耗时被算进去、单次长尾异常的感受被放大。

---

## 二、2026 年实测数据（Runway）

第三方 Runway 基于真实客户发布数据的统计：

### 当前水位（2026-04）

| 状态 | 平均时长 |
|------|---------|
| Waiting for Review | 9小时48分 |
| In Review | 1小时26分 |

### 月度趋势

| 月份 | Waiting for Review 平均 | 备注 |
|-----|----------------------|------|
| 2026-01 | 17小时35分 | 全年最长；论坛大量报告异常延迟 |
| 2026-02 | 12小时35分 | |
| 2026-03 | 9小时59分 | |
| 2026-04 | 9小时48分 | 当前最低 |

> ⚠️ 2026 年新趋势：AI/Vibe Coding 工具导致提交量激增（据报道同比 +24%），2026年初出现明显排队波动，Apple Developer Forums 有开发者报告 Waiting for Review 持续 8–20 天，Apple Staff 回复"we're investigating"。Apple 官方坚称整体指标未变，但长尾异常比"教科书式 24 小时"更普遍。

---

## 三、最佳提交时机

### 3.1 按星期

📊 Runway 完整星期分布（近两周滚动平均）：

| 星期 | 平均等待时长 | 建议 |
|------|------------|------|
| 周二 | **9小时28分** | ✅ 最佳 |
| 周三 | **9小时31分** | ✅ 最佳 |
| 周四 | 11小时48分 | ✅ 可以 |
| 周一 | 13小时12分 | 🟡 尚可 |
| 周日 | 15小时26分 | ⚠️ 避免 |
| 周五 | 18小时47分 | ❌ 避免 |
| 周六 | 19小时00分 | ❌ 最差 |

**常见误解**："周一有周末积压"——Runway 数据显示周一（13h12m）表现优于周日、周五、周六，并非最差提交日。

**周五/六风险**：Apple 审核员周末人员缩减。若周五入队后当天未被取走，将等到周一才被处理。

### 3.2 按时间段（北京时间）

**时区换算**（夏令时 PDT，美国 3月–11月；差值 15 小时）：

| 北京时间 | 库比蒂诺 PDT |
|---------|------------|
| 00:00 | 09:00（工作日开始）|
| 04:00 | 13:00（午后）|
| 08:00 | 17:00（接近下班）|
| 16:00 | 01:00（深夜）|

> 冬令时 PST（美国 11月–3月）：差值变为 16 小时，北京 00:00 = 库比蒂诺 08:00。

**北京时间 00:00–04:00 提交的逻辑**：

✅ 时区数学已确认：北京午夜对应库比蒂诺早上9点（当地工作日开始时刻，即库比蒂诺日历前一天 09:00 PDT）。

⚠️ 经验规则：此时提交理论上进入当天第一批处理池。但 Apple 已在多时区部署审核员，"早晨入队即被取走"的效果尚未有小时粒度第三方数据验证，属于合理推测。

**实操建议**：若有条件，叠加北京时间 00:00–06:00 + 周二/周三，预期效果最佳。

---

## 四、审核状态信号解读

### 4.1 两种状态的含义

| 状态 | Apple 官方定义 |
|------|--------------|
| `Waiting for Review` | Apple 已收到提交，**还未开始审** |
| `In Review` | App Review **正在审核中** |

`Waiting for Review` 时间长，**不代表**审核员已看过你的 App 并有负面判断——App 还未被取走。

### 4.2 `Waiting for Review` 时长信号

| 时长 | 更可能的解释 |
|------|-----------|
| < 12小时 | 正常入队 |
| 12–24小时 | 轻微拥堵，或周末/节前积压 |
| > 48小时 | 队列异常，或账号配置/协议问题 |
| > 7天 | 联系 Apple Developer Support |

### 4.3 `In Review` 时长信号

| 时长 | 更可能的解释 |
|------|-----------|
| < 15分钟 | 快速确定性问题：首屏 bug、链接失效、上轮遗留问题快速复核 |
| 15–60分钟 | 标准人工审核，覆盖基础合规和功能验证 |
| 1–3小时 | 较深入审核，涉及隐私声明、IAP 路径验证 |
| 3小时以上 | 高级审核员介入，业务模式审查、商业边界判断 |

> `In Review` 仅几分钟即被拒 → 优先排查首屏硬问题，而非撰写商业逻辑解释。`In Review` 数小时后被拒 → 优先检查业务边界、支付路径、审核材料完整性。

---

## 五、高峰期延迟规律

### 5.1 年末假期（最有文献记录）

✅ Apple 多年连续发布官方延迟警告：

| 年份 | 官方警告期 | 政策 |
|------|----------|------|
| 2024 | 12月20–26日 | 继续接受提交，但速度变慢 |
| 2023 | 12月22–27日 | 继续接受提交，但速度变慢 |
| 2021 | 11月24–28日（感恩节）+ 12月23–27日 | 继续接受提交，但速度变慢 |
| 2020年及更早 | 12月23–27日 | **封窗**，完全不接受新提交（来源：[Apple 2020公告](https://developer.apple.com/news/?id=83m4plrb)）|

2024年官方原文：
> "Please plan to submit time-sensitive submissions early, as we anticipate high volume and reviews may take longer to complete from December 20–26."

📊 Runway 月度数据佐证：1月（节后积压）平均17h35m，全年最长；12月约10h59m，比正常月高约20–30%（Runway 2025-12 历史数据）。

**实操建议**：12月15日前完成所有时效性版本提交；12月20日后提交的版本做好等待1周以上的准备。

### 5.2 感恩节（11月下旬）

✅ 官方确认（限2021年）：2021年公告明确列出11月24–28日为减速期。后续年份未见类似公告，但11月下旬提交量高峰是惯例。

### 5.3 WWDC（六月）/ iOS 新版发布（九月）

⚠️ 经验规则：开发者社区报告这两个时期提交量激增、审核延迟。Apple 未就此发布官方延迟警告（与圣诞期官方公告性质不同）。若版本有时间弹性，建议避开 WWDC 周（通常6月初）和 iPhone 发布周（通常9月中旬）。

---

## 六、不同 App 类型的时长差异

> ⚠️ 重要说明：**Apple 官方不发布分类别审核时长数据**。以下均为社区经验和第三方研究推断。

### 6.1 提交类型差异

⚠️ 经验规则（多方来源一致）：

| 提交类型 | 典型时长 |
|---------|---------|
| 小版本更新（Bug 修复）| 12–24小时 |
| 功能更新 | 24–48小时 |
| 新 App（首次提交）| 24–72小时 |
| 全新开发者账号的首个 App | 可达7天 |
| 被拒后重提交 | 12–24小时 |

更新版本审核员有历史记录可参考；新 App 需要全面评估商业模式、内容合规、数据收集策略。

> **申诉路径（App Review Board）**：这是审核被拒后的正式异议流程，不是常规提交。提交申诉后等待时间通常5–14天，成功率较低，适用于确信 Apple 判断有误的情况。入口：App Store Connect → 被拒版本 → Request Appeal。

### 6.2 受监管类别（额外审查时间）

⚠️ 经验规则：

| 类别 | 估计额外时间 | 核心原因 |
|------|------------|---------|
| 金融/银行/加密货币 | +2–5天 | 需验证牌照资质、合规证明 |
| 医疗/健康（含设备声明）| +1–3天 | 医疗声明和免责声明审查 |
| 儿童（Kids 4+）| +1–3天 | COPPA 合规、数据收集和广告审查 |
| 游戏（含战利品箱/随机付费）| +3–7天 | 年龄分级审查、3.1.1 概率披露 |

### 6.3 平台差异

⚠️ 经验规则：

| 平台 | 典型时长 |
|------|---------|
| tvOS | ~1天（提交量少，最快）|
| iOS/iPadOS | ~1–3天 |
| macOS | ~2–7天（2026年有延长趋势报告）|

---

## 七、主动干预手段

### 7.1 Meet with App Review（视频会议咨询）

✅ Apple 官方提供的30分钟 Webex 一对一咨询：

| 项目 | 详情 |
|------|------|
| 内容 | 讨论审核预期、规范对齐、反复被拒的具体问题 |
| 开放时间 | **每周二和周四**（当地营业时间，subject to availability）|
| 预约入口 | [developer.apple.com/distribute/app-review/](https://developer.apple.com/distribute/app-review/) → "View schedule" → 搜索 "App Review" |
| 适用场景 | 同一结构性条款被连续3轮命中；文字 Review Messages 来回无法解决 |

> ⚠️ 预约链接中的 Event ID 会随每期活动更换，旧链接可能失效。请从官方入口查询当前可预约期次，不要直接使用他人分享的固定 URL。

**不适用场景**：仅有一次被拒且问题清晰时，直接修复后重提更高效。

### 7.2 加急审核（Expedited Review）

见 `operations/expedited-review.md`。

### 7.3 提供完整 Demo 账号和审核说明

✅ Apple 官方文档直接说明：
> "If you don't include this information, the app review process may be delayed and your app may not pass review."

这是唯一有 Apple 官方直接背书的"防延迟手段"。必须提供：含完整权限的 Demo 账号、特殊功能操作步骤、需要特殊硬件/环境时的演示视频。

---

## 八、时间信号判断框架

```
提交后 → Waiting for Review
   ├── < 12h → 正常
   ├── > 48h → 检查账号配置、协议状态
   └── > 7天 → 联系 Apple Developer Support

进入 In Review 后
   ├── < 15分钟出结果 → 首屏硬问题 / 上轮遗留
   ├── 15–60分钟 → 标准人工审核
   ├── 1–3小时 → 隐私/IAP 验证
   └── 3小时以上 → 业务模式深度审查

同一条款反复命中
   ├── 1–2次 → 回复 Review Messages，附截图证据
   └── 3次以上 → 预约 Meet with App Review
```

---

## 来源

| 来源 | URL | 验证时间 |
|------|-----|---------|
| App Review | https://developer.apple.com/distribute/app-review/ | 2026-04 |
| Overview of submitting for review | https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review | 2026-04 |
| App and submission statuses | https://developer.apple.com/help/app-store-connect/reference/app-information/app-and-submission-statuses | 2026-04 |
| Tech Talk: Tips for preventing common review issues | https://developer.apple.com/kr/videos/play/tech-talks/10885/ | 2026-04 |
| 2024年假期公告 | https://developer.apple.com/news/?id=iwvebnw2 | 2026-04 |
| 2023年假期公告 | https://developer.apple.com/news/?id=uijoypq9 | 2026-04 |
| 2021年假期公告（感恩节+圣诞）| https://developer.apple.com/news/?id=y4fgrhhe | 2026-04 |
| Runway App Store Review Times（实时数据）| https://www.runway.team/appreviewtimes | 2026-04 |
| Apple Developer Forums — Review taking much longer than usual | https://developer.apple.com/forums/thread/814122 | 2026-04 |
| 9to5Mac — Vibe coding App Store review delays | https://9to5mac.com/2026/03/29/vibe-coding-developers-report-long-app-store-review-queues/ | 2026-04 |
