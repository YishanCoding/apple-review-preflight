# Phased Release 策略手册
> 何时用、如何控制、紧急 Hotfix 路径、发布模式选择矩阵

---

## 一、Phased Release 概述

Phased Release（分阶段发布）是 App Store 提供的一种风险控制机制，允许开发者在7天内逐步向用户推送新版本，而非一次性全量发布。

**关键特性**：
- 只影响**自动更新**的用户（设置中开启自动更新的用户）
- 手动在 App Store 搜索并下载的用户**始终获得最新版本**（不受 Phased Release 限制）
- 每个阶段持续约24小时（Apple 自动推进，无法精确控制时间点）
- 最多可暂停30天，超过30天 Apple 自动推进到100%

---

## 二、何时使用 Phased Release

### 推荐使用的场景

**大版本/重大架构变更**
- 重写了核心模块（网络层、数据库层、状态管理）
- 升级了主要框架版本（如 Swift 5.x → 6.x）
- 更换了第三方 SDK（如换了推送服务、崩溃监控）
- 风险：1%的用户遇到崩溃比100%好处理

**支付/订阅相关变更**
- 修改了 IAP 购买流程
- 更改了订阅逻辑或价格层级映射
- 引入了新的订阅类型（如从一次性购买迁移到订阅制）
- 风险：支付流程 Bug 直接影响收入，需快速止损

**AI 功能/大模型集成**
- 新增 AI 生成功能（内容质量不稳定）
- 接入新的推理模型（响应格式可能不一致）
- 服务器端成本不确定（需要监控实际调用量）
- 风险：服务器成本爆炸或内容质量问题需要回滚

**重要 UI/UX 改版**
- 核心导航结构变化
- 重新设计的主要用户流程
- 可能引发大量用户投诉的改动

**权限/隐私变更**
- 新增权限请求（Camera、Location 等）
- 更新了 ATT 弹窗文案
- 数据收集范围变化

### 不需要 Phased Release 的场景

- 纯 Bug Fix（Crash Rate > 1% 的紧急修复反而应该跳过 Phased，全量发布）
- 文案修改、UI 微调
- 性能优化（已在 TestFlight 充分验证）
- Hotfix 版本（应使用 Full Release + Expedited Review）

---

## 三、Phased Release 阶段详情

```
审核通过（Approved）
        ↓
    手动触发发布（或 Auto Release）
        ↓
Day 1-2:  1%  ←── 观察窗口：Crash Rate、负面评价、支付转化
Day 3:    2%  ←── 若 Day 1-2 稳定，自动推进
Day 4:    5%
Day 5:   10%
Day 6:   20%
Day 7:   50%
Day 8+: 100%  ←── 全量完成
```

### 各阶段观察指标

| 阶段 | 用户量参考（100万 MAU） | 重点观察 |
|------|-------------------------|----------|
| 1% | ~1万 | Crash Rate（基线对比）、ANR、关键 API 错误率 |
| 2-5% | 2~5万 | 用户评分变化、支付成功率（若有 IAP） |
| 10-20% | 10~20万 | 留存率、Session 时长、负面评价关键词 |
| 50%+ | 50万+ | 服务器负载、CDN 成本、AI 调用量 |

**通过标准（参考，需根据实际 App 调整）**：
- Crash Rate < 0.1%（或不高于前一版本基线的1.5倍）
- 无严重 ANR（Application Not Responding）
- 评分未出现显著下滑（连续24小时负面评价 < 10%）
- 关键业务指标无异常（如支付成功率 > 95%）

---

## 四、操作：暂停 / 恢复 / 跳过

### 4.1 在 ASC 中操作

**路径**：App Store Connect → My Apps → [App Name] → App Store → 版本详情 → Phased Release

**三个按钮**：
- **Pause Phased Release**：立即停止推进，已安装的用户不受影响，新用户继续收到此版本（但只有当前比例）
- **Resume Phased Release**：从暂停的百分比继续推进
- **Release to All Users**：立即跳到100%（不可逆）

### 4.2 通过 API 操作

使用 App Store Connect API（v1）：

```bash
# 获取当前 Phased Release 状态
curl -X GET \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersionPhasedReleases/{id}" \
  -H "Authorization: Bearer $JWT_TOKEN"

# 暂停（phasedReleaseState: PAUSED）
curl -X PATCH \
  "https://api.appstoreconnect.apple.com/v1/appStoreVersionPhasedReleases/{id}" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "appStoreVersionPhasedReleases",
      "id": "{id}",
      "attributes": {
        "phasedReleaseState": "PAUSED"
      }
    }
  }'

# 恢复（phasedReleaseState: ACTIVE）
# 全量（phasedReleaseState: COMPLETE）
```

**phasedReleaseState 值**：
- `INACTIVE`：创建但未开始
- `ACTIVE`：正在推进
- `PAUSED`：已暂停
- `COMPLETE`：已全量（终态）

---

## 五、紧急 Hotfix 路径

当发现严重问题（Crash Rate 飙升、支付中断、数据丢失等）时，按以下路径处理：

```
发现严重问题
      ↓
Step 1: 立即 Pause Phased Release（防止更多用户受影响）
      ↓
Step 2: 评估是否需要回退当前版本
  ├── 可以：联系 Apple Developer Support 请求下架当前版本
  │         （极少数情况，Apple 通常不接受）
  └── 不可以：进入 Hotfix 流程
      ↓
Step 3: 开发 Hotfix
  · 最小化改动，只修复关键问题
  · 不引入新功能
  · 版本号规则：1.2.0 → 1.2.1
      ↓
Step 4: 提交 Hotfix + 申请 Expedited Review
  · ASC → App → 联系我们 → 申请加急审核
  · 或：https://developer.apple.com/contact/app-store/?topic=expedite
  · 说明：严重 Crash 影响用户，提供 Crash Rate 数据
  · Expedited Review 通常24小时内完成（工作日）
      ↓
Step 5: Hotfix 审核通过后，选择 Full Release（跳过 Phased）
      ↓
Step 6: 监控 Hotfix 版本稳定性后，Resume 原计划（或直接跳过）
```

### Expedited Review 申请模板

```
Subject: Expedited Review Request - [App Name] Version X.X.X

We are requesting an expedited review for [App Name] (Bundle ID: com.xxx.xxx).

REASON FOR EXPEDITED REVIEW:
Our version X.X.X (currently in Phased Release) has a critical issue:
- Crash Rate: X% (baseline was X%, current is X%)
- Affected users: approximately X users
- Issue: [简述 Crash 原因，如 "nil force unwrap in payment completion handler"]

IMPACT:
- [具体影响，如 "Users are unable to complete purchases"]
- We have paused Phased Release to prevent further spread

FIX IN VERSION X.X.X:
- [修复内容描述]
- We have thoroughly tested this fix in TestFlight

We appreciate your consideration and are available to provide any
additional information needed.
```

### Hotfix 发布模式选择

| 场景 | 推荐发布模式 |
|------|-------------|
| Crash Rate > 2%，大量用户受影响 | Full Release（立即全量）|
| 功能异常但不影响核心流程 | Phased Release（继续观察）|
| 支付/数据丢失等严重问题 | Full Release + Expedited Review |
| 服务端问题（不需要新 Binary） | 服务端修复即可，不需要提交新版本 |

---

## 六、Manual Release vs Auto Release vs Phased Release 选择矩阵

### 三种发布模式说明

| 模式 | 触发时机 | 用户覆盖速度 | 适用场景 |
|------|----------|-------------|----------|
| **Manual Release** | 开发者手动点击"发布" | 点击后立即100%覆盖自动更新用户 | 需要配合营销活动（如发布日同步上线），或等待服务端准备就绪 |
| **Auto Release** | 审核通过后立即发布 | 立即100%覆盖自动更新用户 | 纯 Bug Fix、小改动、不需要控制时间点 |
| **Phased Release** | 审核通过后（或手动触发后）按7天逐步推进 | 7天内从1%→100% | 大版本、风险较高的变更 |

### 选择决策树

```
Q1: 是否需要在特定时间点发布？
  ├── 是 → Manual Release（配合营销节奏）
  └── 否 → Q2

Q2: 是否属于高风险变更？（大版本/IAP/AI功能/架构变更）
  ├── 是 → Phased Release
  └── 否 → Q3

Q3: 是否是紧急 Bug Fix？（Crash Rate > 1%）
  ├── 是 → Auto Release 或 Manual Release（尽快全量）
  └── 否 → Auto Release（默认）
```

### 组合用法

**最常见的最佳实践**：
```
大版本发布 = Manual Release + Phased Release
  → 审核通过后不立即发布
  → 等到工作日上午（方便监控）
  → 手动触发发布 → 自动走 Phased 1%→100%
```

**配合营销活动**：
```
产品发布日 = Manual Release（关闭 Phased）
  → 提前1-2天提交审核（预留审核时间）
  → 审核通过后不立即发布
  → 活动开始时手动点击发布
  → 立即全量覆盖
```

**小更新**：
```
Minor Update = Auto Release（关闭 Phased）
  → 审核通过立即全量
  → 适合文案修改、小 Bug Fix
```

### ASC 配置方式

提交版本时，在 "Version Release" 部分选择：
- `Automatically release this version`：审核通过后立即发布（Auto Release）
- `Manually release this version`：审核通过后等待手动发布（Manual Release）
- 勾选 `Release Over 7-Day Period Using Phased Release`：叠加 Phased Release

**注意**：Manual Release + Phased Release 可以同时启用。Manual Release 控制何时开始，Phased Release 控制开始后的推进节奏。

---

## 七、Phased Release 常见误区

**误区1：Phased Release 可以控制哪些用户收到更新**
- 错误。Apple 随机选择用户，开发者无法指定地区、设备型号等条件。

**误区2：暂停 Phased Release 会让已更新的用户回退旧版本**
- 错误。暂停只阻止新用户接收更新，已安装新版本的用户不受影响，也不会回退。

**误区3：Phased Release 期间可以修改元数据（截图/文案）**
- 可以，但需要重新提交审核。修改元数据不影响已发布的 Binary。

**误区4：100% 后无法回滚到旧版本**
- 正确。App Store 没有"回滚"功能。唯一选项是提交新版本（Hotfix）并申请加急审核。这正是为什么 Phased Release 很重要——它给了你发现问题并用 Hotfix 覆盖的时间窗口。
