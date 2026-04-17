# 加速审核 (Expedited App Review)

> **读这个文件的场景**：线上 App 有严重 bug 需要紧急修复上架、版本绑定了时间性事件（节日/发布会）、或安全漏洞急需修补。
> **前置区别**：加速审核 = 加快进入审核队列。不代表会通过审核。如果版本本身有 Guideline 问题，加速审核后照样被拒。
> **最后验证时间**：2026-04

---

## 一、当前入口（2025/2026）

| 项目 | 详情 |
|------|------|
| **URL** | [developer.apple.com/contact/app-store/?topic=expedite](https://developer.apple.com/contact/app-store/?topic=expedite) ✅ Apple 官方 |
| **访问方式** | 需登录开发者账号 → 自动跳转至 Apple ID 认证 → 加载表单 |
| **替代入口** | developer.apple.com → Contact Us → App Review → Expedited App Review Request |
| **旧邮箱** | AppReview@apple.com（不推荐用于加速审核请求，仅用于一般审核沟通）|

---

## 二、Apple 认可的加速理由

✅ Apple 官方描述为 "extenuating circumstances"：

| 理由 | 说明 | 通过率（⚠️ 经验规则）|
|------|------|----------|
| **严重 Bug 修复** | 线上版本出现崩溃、数据丢失、功能完全不可用。 | 高 |
| **安全漏洞** | 发现可被利用的安全漏洞（数据泄露、注入、认证绕过）。 | 高 |
| **时间绑定事件** | App 发布绑定真实世界事件（节日促销、发布会、合作推广）。 | 中 |
| **不被接受的理由** | "我们想快点上线" / "我们承诺了客户" / 无具体技术原因。 | 低/拒绝 |

---

## 三、审核时效

| 状态 | 预期时间 | 来源 |
|------|---------|------|
| 加速请求被批准 | 4-12 小时内完成审核 | ⚠️ 经验规则（社区共识） |
| 常规审核队列 | 50% 在 24h 内，90% 在 48h 内 | ✅ Apple 官方（developer.apple.com/distribute/app-review/） |
| 加速请求被拒绝 | 回到常规队列，无惩罚 | ⚠️ 经验规则 |

> ⚠️ 2026 年特殊情况：由于 AI/Vibe-coding 浪潮导致 App Store 提交量激增（据报道增长约 84%），2026 年初审核排队明显拥堵，部分开发者反馈提交加速请求后 9-45 天仍无响应。建议在此期间**降低预期**，并做好常规排队的准备。

---

## 四、频率限制

Apple **没有公布硬性次数上限**（如"每年不超过 X 次"），但明确警告：

> "Excessive requests may result in Apple deprioritizing your future expedite submissions."

⚠️ 经验规则：社区共识是每 App 每年不超过 2-3 次。滥用加速审核会导致：
- 未来的加速请求被自动降权
- 极端情况下可能影响账号信誉

---

## 五、邮件/表单模板

### 场景 1：严重 Bug 修复

```
Subject: Expedited Review Request — Critical Crash Fix for [App Name]

Dear App Review Team,

We have discovered a critical bug in our live app [App Name] (Apple ID: [ID]) 
that causes the app to crash on launch for users running iOS [version] when 
[specific condition].

Impact: Approximately [X]% of our active users ([Number] users) are affected. 
Our crash reporting tool [Crashlytics/Sentry] shows [Number] crash events in 
the past [X] hours.

We have identified and fixed the root cause ([brief technical description]) and 
submitted build [Build Number] for review.

We respectfully request an expedited review to minimize the negative impact on 
our users.

Thank you for your consideration.
[Name / Company]
```

### 场景 2：安全漏洞修补

```
Subject: Expedited Review Request — Security Vulnerability Patch for [App Name]

Dear App Review Team,

We have identified a security vulnerability in our live app [App Name] 
(Apple ID: [ID]) that could allow [brief description of the risk, e.g., 
"unauthorized access to user authentication tokens via an insecure API endpoint"].

We have patched this vulnerability in build [Build Number] by [brief description 
of the fix, e.g., "migrating all API communication to certificate-pinned HTTPS 
and invalidating all existing tokens"].

Given the potential impact on user data security, we respectfully request an 
expedited review for this critical update.

Thank you.
[Name / Company]
```

### 场景 3：时间绑定事件

```
Subject: Expedited Review Request — Time-Sensitive Update for [App Name]

Dear App Review Team,

Our app [App Name] (Apple ID: [ID]) has a time-sensitive update tied to 
[specific event, e.g., "our partnership launch with [Partner] on [Date]" or 
"the [Holiday] promotion starting [Date]"].

This update includes [brief description of the changes]. We have thoroughly 
tested the build and it complies with all App Store Review Guidelines.

We submitted build [Build Number] on [Date] and respectfully request an 
expedited review to ensure the update is available before [Deadline Date].

Thank you for your time.
[Name / Company]
```

### 中文版（通用结构，Bug 修复场景）

```
标题：加速审核请求 — [App 名称] 紧急崩溃修复

尊敬的 App Review 团队：

我们在线上版本 [App 名称]（Apple ID: [ID]）中发现了一个严重 bug，
导致用户在 [具体条件] 下启动即崩溃。

影响范围：约 [X]% 的活跃用户（[数量] 名用户）受影响。过去 [X] 小时内
崩溃监控系统记录了 [数量] 次崩溃事件。

我们已定位并修复了根本原因（[简要技术说明]），并提交了版本 [Build 号]。

恳请加速审核，以尽快减少对用户的影响。

谢谢！
[姓名 / 公司]
```

---

## 六、常见坑

1. **加速 ≠ 通过**：加速审核只是让你更快排到队列前面。如果版本有 Guideline 问题，一样会被拒。被拒后再次加速审核的通过率会更低。
2. **不要同时在多个通道提加速**：在表单提交一次即可。同时发邮件 + 表单 + 电话不会更快，反而可能被标记为过度请求。
3. **表单中要有技术细节**：Apple 需要判断紧急性。"App has a bug" 不够，需要说明 bug 的严重性和影响范围。
4. **审核期间保持后端在线**：加速审核可能在半夜进行，确保后端服务 24/7 可用，演示账号有效。
5. **2026 拥堵期**：如果加速请求被拒或无响应，不要恐慌。准备好 Plan B（如暂时回滚服务端逻辑、开启 Feature Flag 关闭问题功能）。

---

## 来源

| 来源 | URL | 验证时间 |
|------|-----|---------|
| App Review | https://developer.apple.com/distribute/app-review/ | 2026-04 |
| Expedited Review 表单 | https://developer.apple.com/contact/app-store/?topic=expedite | 2026-04 |
| Apple Developer Forums — 审核拥堵 | https://developer.apple.com/forums/thread/821221 | 2026-04 |
| Polpiella — Expedited Reviews | https://www.polpiella.dev/expedited-app-reviews | 2026-04 |
