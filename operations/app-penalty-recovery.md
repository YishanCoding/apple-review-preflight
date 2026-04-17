# 被下架/清榜/清词应急恢复 (App Penalty Recovery)

> **读这个文件的场景**：App 突然从 App Store 下架、排名骤降（清榜）、核心关键词一夜归零（清词）。
> **前置区别**：如果是 App 审核被拒（Rejected），走 `../operations/review-ops.md`。如果是账号级别的 Pending Termination，走 `../operations/account-warnings.md`。
> **最后验证时间**：2026-04

---

## 一、三种惩罚类型速查

| 惩罚类型 | 表现 | 严重程度 | 是否有明确申诉通道 |
|---------|------|---------|-----------------|
| **下架 (Removal)** | App 从商店消失，无法被搜索或下载。 | 最严重 | 是（Resolution Center + App Review Board） |
| **清榜 (Chart Removal)** | App 仍可搜索下载，但从排行榜中消失。排名骤降至 50+ 或完全不显示。 | 中等 | 否（无官方通道） |
| **清词 (Keyword Clearing)** | App 仍在线，但原有稳定的关键词排名归零。 | 中等 | 否（无官方通道） |

---

## 二、下架 (App Removal) 处理

### 2.1 确认下架原因

Apple 通常通过两个渠道通知：
1. **App Store Connect → Resolution Center**：带有具体 Guideline 条款号。
2. **开发者注册邮箱**：收到包含违规说明的邮件。

> ⚠️ 经验规则：Apple 通常 "先斩后奏" —— 先下架，邮件可能延迟 1 天左右才到。

**2024-2026 常见下架原因**：
- Guideline 2.5.2 — App 不包含自身核心功能（vibe-coding/壳包问题）
- Guideline 3.2(f) — 欺诈/隐蔽功能
- 隐私清单 (Privacy Manifest) 不合规
- 长期未更新且功能失效
- 知识产权投诉

### 2.2 申诉流程

```
Step 1: 读 Resolution Center 中的具体拒审/下架原因
       ↓
Step 2: 如果是代码/功能问题 → 修复 → 提交新 Build → 在 Resolution Center 回复说明
       ↓
Step 3: 如果对裁定不服 → 通过 developer.apple.com/contact/app-store/ 
        → 选 "I would like to appeal an app rejection or app removal"
        → 提交至 App Review Board
       ↓
Step 4: 等待 App Review Board 回复（⚠️ 经验规则：24h - 30+ 天不等）
```

### 2.3 时效预期

| 情况 | 预期恢复时间 |
|------|-----------|
| 修改元数据后 Resubmit | 1-3 天 |
| 修复代码问题后 Resubmit | 取决于审核队列（常规 24-48h） |
| App Review Board 申诉 | ⚠️ 经验规则：数天到 30+ 天 |

### 2.4 下架期间不能做的事

1. **不能转移 App**：App 必须处于 "Ready for Sale" 状态才能转移。被下架的 App 无法转让到其他账号。
2. **不能用其他账号上传相同功能的 "备用 App"**：违反 Guideline 4.3 (Spam) 和 5.6 (Developer Code of Conduct)。Apple 会关联封禁所有相关账号。

---

## 三、清榜 (Chart Removal) 处理

### 3.1 如何判断是清榜而非自然下滑

| 清榜特征 | 自然下滑特征 |
|---------|-----------|
| 排名在一天内从 Top 10 → 50+ 或完全消失 | 排名逐步下降（几天到几周） |
| 下载量未明显变化但排名骤降 | 下载量和排名同步下降 |
| 仅排行榜消失，搜索排名不受影响 | 搜索和排行榜表现一致 |

> 检测工具建议：在设备设置中关闭"个性化推荐"来查看未个性化的真实排名。

### 3.2 应对策略

**Apple 没有官方的清榜申诉通道。** 可以尝试：

1. **通过 Developer Contact 表单询问**：[developer.apple.com/contact/](https://developer.apple.com/contact/) — 礼貌地描述异常现象，询问是否有任何合规问题需要解决。
2. **自查合规**：检查近期是否有可疑的推广渠道引入了非真实用户。
3. **等待**：⚠️ 经验规则 — 72% 的排名波动会在 24-48 小时内自行恢复。真正的清榜惩罚通常在 3-7 天后解除。2025 年 2 月的一次大规模排名冻结持续了 2 周以上。

### 3.3 清榜询问模板（英文）

```
Subject: Inquiry About Ranking Anomaly for [App Name]

Dear Apple Developer Support,

We have noticed an abnormal ranking drop for our app [App Name] 
(Apple ID: [ID]) starting on [Date]. Our app dropped from position [X] to 
[Y] on the [Category] chart within [Time Period], while our download volume 
remained consistent.

We have reviewed our app for compliance with all App Store Review Guidelines 
and have not conducted any promotional activities that violate Guideline 5.6.

Could you please advise whether there is any compliance issue with our app 
that we should address?

We are committed to fully complying with Apple's policies and appreciate any 
guidance you can provide.

Thank you,
[Name / Company]
```

---

## 四、清词 (Keyword Clearing) 处理

### 4.1 如何判断是清词而非算法调整

| 清词特征 | 算法调整特征 |
|---------|-----------|
| 原本稳定的核心关键词排名突然归零 | 多个关键词排名出现梯度变化 |
| 仅影响你一个 App | 整个品类的 App 都有排名变动 |
| 其他关键词不受影响 | 广泛影响多个关键词 |

> ⚠️ 2025 年特殊情况：Apple 在 2025 年中期对搜索算法进行了重大更新，引入语义索引和 AI 驱动的意图匹配。这导致大量 App 出现关键词变动，但这不是惩罚性清词，而是算法变更。

### 4.2 应对策略

**Apple 没有官方的清词申诉通道。** 建议：

1. **元数据优化**：重新审视 App Name / Subtitle / Keywords，确保与 App 实际功能高度相关（Guideline 2.3.7）。
2. **避免关键词堆砌**：删除与 App 功能无关的热门词。
3. **维持核心词的自然下载信号**：保持对核心关键词 20-40% 的优化投入（⚠️ 经验规则）。
4. **恢复周期**：⚠️ 经验规则 — 大多数清词在 3-7 天后恢复；部分可能持续数周。

---

## 五、关于 "备用 App" 策略的严正警告

2019 年前，部分运营指南建议 "准备一个马甲包作为备用"。**2025/2026 年这是非常危险的做法**：

- Guideline **4.3 (Spam)**：禁止提交重复或功能相同的 App。
- Guideline **5.6 (Developer Code of Conduct)**：禁止操纵评分、排名、搜索结果或伪装应用身份。
- Apple 2024 年封禁了 **14.6 万个开发者账号**，其中大量因为多账号马甲包关联被一并封禁。

> ⚠️ 法律风险提示：在账号被处罚期间使用其他账号上架替代品，几乎必然导致所有关联账号被同步封禁。

---

## 来源

| 来源 | URL | 验证时间 |
|------|-----|---------|
| App Store Review Guidelines (4.3, 5.6) | https://developer.apple.com/cn/app-store/review/guidelines/ | 2026-04 |
| Apple Newsroom — Fraud Prevention | https://www.apple.com/newsroom/2025/05/the-app-store-prevented-more-than-9-billion-usd-in-fraudulent-transactions/ | 2026-04 |
| Developer Contact | https://developer.apple.com/contact/ | 2026-04 |
| Contact App Review | https://developer.apple.com/contact/app-store/ | 2026-04 |
| ASOWorld — Keyword Ranking Freeze | https://asoworld.com/en/blog/is-apple-store-locking-your-keywords-decoding-the-ranking-freeze-survival-tactics/ | 2026-04 |
| KeyApp — ASO Storm 2025 | https://keyapp.top/blog/blog-news/aso-storm-2025-how-to-survive-and-win/ | 2026-04 |
