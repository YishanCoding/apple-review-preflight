# App Store Review 操作手册
> 三合一：提交流程 + Review Notes + 申诉
> 基于 Apple 官方指南（2026-02-06）及实战经验

---

## 一、完整提交流程

### 1.1 Archive → Validate → Upload

```
Xcode → Product → Archive
         ↓
Organizer → Validate App（选 App Store Connect）
  · 检查签名、Entitlements、Privacy Manifest
  · 若通过：Distribute App → App Store Connect
  ↓
App Store Connect 后台接收 Build（通常5~15分钟，Processing 状态）
Processing 完成后 Build 可选
```

**Validate 失败常见原因**：
- 签名证书过期 → 重新 Archive 前在 Keychain 检查证书有效期
- Provisioning Profile 不匹配 → Xcode 中 Automatically manage signing 或手动更新 Profile
- Missing Privacy Manifest → 见 `../references/privacy-manifest.md`

### 1.2 TestFlight 内部测试（可选但推荐）

1. Build 处理完成后，在 ASC → TestFlight → Internal Testing 添加 Build
2. 内部测试员（最多100人）无需审核，立即可安装
3. 外部测试员（最多10,000人）需通过 Beta App Review（通常1个工作日）
4. TestFlight 版本有效期90天，过期自动失效

**TestFlight 注意**：
- 若 Build 在 TestFlight 阶段发现崩溃，修复后重新 Archive，旧 Build 可在 ASC 中 Expire
- Beta App Review 被拒不影响正式版审核记录

### 1.3 提交正式审核

1. ASC → App Store → 选择版本 → 选择 Build
2. 填写 What's New（每语言最多4000字符）
3. 填写 App Review Information：
   - Demo Account（必填，若有登录门槛）
   - Review Notes（见第二节）
   - Attachment（可上传截图/视频/PDF，最多1个文件）
4. 选择 Release 方式（见 `phased-release-strategy.md`）
5. 点击 Submit for Review

**提交前 Checklist**：
- [ ] Privacy Nutrition Labels 与代码实际数据收集一致
- [ ] 所有截图尺寸符合要求（见 `../references/store-metadata-compliance.md`）
- [ ] IAP 价格和描述已在 ASC 配置（若有）
- [ ] Review Notes 填写完整
- [ ] Demo Account 有效且数据充足
- [ ] Export Compliance 已正确声明（含加密）

---

## 二、ASC 系统错误 vs 人工拒审 判断矩阵

### 2.1 系统错误（ITMS 错误码）—— 上传/处理阶段自动检测

| 错误码 | 含义 | 处理方式 |
|--------|------|----------|
| ITMS-90035 | 签名无效或证书不可信 | 重新签名并确认 Certificate 在 ASC 中 Active |
| ITMS-90161 | Provisioning Profile 不匹配或过期 | 在 Apple Developer Portal 重新生成 Profile |
| ITMS-90338 | 非公开 API 使用（private framework） | 移除对私有 API 的调用 |
| ITMS-90542 | Watch App 版本号低于主 App | 同步 Watch Extension CFBundleVersion |
| ITMS-90596 | 缺少 WKExtensionDelegateClassName | 在 Info.plist 补充 key |
| ITMS-90683 | 缺少 NSCameraUsageDescription 等 Privacy String | 在 Info.plist 补充所有使用到的 NSXxxUsageDescription |
| ITMS-90694 | Swift 编译器版本不兼容 | 升级 Xcode 或锁定 Swift 版本 |
| ITMS-90703 | Invalid Bundle — 包含 Simulator 架构 | Archive 时确认 Build Active Architecture Only = NO |
| ITMS-90809 | 使用已废弃的 UIWebView API | 替换为 WKWebView |
| ITMS-91053 | Privacy Manifest 缺失必要 reason code | 见 `../references/privacy-manifest.md` 补充 |
| ITMS-91055 | 第三方 SDK 未提供 PrivacyInfo.xcprivacy | 升级 SDK 至提供 manifest 的版本 |
| processing failed（无 ITMS 码） | ASC 内部处理失败 | 等待30分钟重试上传；若持续失败联系 Apple Developer Support |

**判断规则**：ITMS-9xxxx 都是系统错误，在 Upload 阶段被拒，邮件主题含 "issues found"，**不计入人工审核拒审次数**。

### 2.2 人工审核拒审（Guideline 拒审）

| 拒审来源 | 特征 | 常见 Guideline |
|----------|------|----------------|
| Binary 拒审 | Resolution Center 有拒审信息，状态变为 Rejected | 2.x（App 完整性）、4.x（设计）、5.x（法律） |
| Metadata 拒审 | 截图/文字被拒，Binary 可能通过 | 2.3.x（Metadata）|
| 隐私拒审 | 数据收集 Label 不实 | 5.1.1、5.1.2 |
| IAP 拒审 | 绕过 IAP、虚拟货币 | 3.1.1、3.1.2 |
| Sign in with Apple 缺失 | 有第三方登录但无 SIWA | 4.8 |

---

## 三、App Review Notes 撰写模板

App Review Notes 是审核员唯一的上下文来源，务必清晰。上限4000字符（英文优先）。

### 3.1 标准模板结构

```
DEMO ACCOUNT
Username: demo@example.com
Password: Demo1234!
[如有2FA，说明如何获取验证码，或提供绕过方式]

KEY FEATURES TO REVIEW
1. [功能名称]：[一句话说明在哪里找到，如何触发]
2. [功能名称]：[说明]

SPECIAL SETUP / BACKEND NOTES
- [后端特殊状态，如"demo账号已预置付费内容，无需购买"]
- [地理限制说明，如"此功能仅限美区账号"]
- [网络要求，如"需要访问 api.example.com，无防火墙限制"]

IN-APP PURCHASES
- 沙盒环境可使用 Apple Sandbox tester 账号完成购买
- Sandbox Apple ID: sandbox_test@example.com / Password: Sandbox123!

PERMISSIONS REQUESTED
- Camera：用于 [具体用途]
- Location (When In Use)：用于 [具体用途]
- Notifications：用于 [具体用途]

[如有 AR/特殊硬件要求]
DEVICE REQUIREMENTS
- 需要支持 LiDAR 的设备测试 AR 功能（iPhone 12 Pro 及以上）
```

### 3.2 演示账号特殊场景

**场景：App 需要真实用户数据才能展示内容**
```
DEMO ACCOUNT NOTE
The demo account (demo@example.com) has been pre-loaded with:
- 30 days of activity history
- 5 sample projects with full data
- Premium subscription activated (no purchase needed)
Please do not change the account password as it is shared for review purposes.
```

**场景：App 有审核员所在地区不可用的功能**
```
REGIONAL NOTE
The "Live Scores" feature is only available in the US and CN regions.
The review account is set to US region. If you are reviewing from a different
region, please use the demo account provided which is pre-configured for US.
```

**场景：需要物理设备配对（如蓝牙硬件）**
```
HARDWARE NOTE
The primary feature requires pairing with our IoT device.
Since you may not have the hardware, we have included a "Demo Mode"
accessible via: Settings → Developer → Enable Demo Mode.
In Demo Mode, all hardware interactions are simulated.
```

---

## 四、被拒后处理流程

### 4.1 Resolution Center 回复策略

**原则**：
- 72小时内回复（拖延会影响排队优先级）
- 语气礼貌专业，不抗辩，聚焦于"我们如何修复"
- 若需要修复后重新提交，先修复再回复

**回复类型 A：已修复并重新提交**
```
Thank you for your review.

We have addressed the issue regarding [Guideline X.X - 拒审原因摘要].

Changes made in this update:
1. [具体修改1]
2. [具体修改2]

We have submitted a new build (version X.X.X, build NNNN) that includes
these fixes. Please review the updated version at your convenience.

If you have any additional questions or need further clarification,
please let us know.
```

**回复类型 B：提供澄清（不需要修改代码）**
```
Thank you for your review.

We would like to provide additional context regarding [Guideline X.X].

[清晰解释该功能的合规性，引用 Guideline 原文]

Specifically:
- [证据1：如截图、文档链接]
- [证据2]

We believe our app is in compliance with [Guideline X.X] because [理由].
We have also updated the Review Notes to clarify this for future reviews.

Please let us know if you need any additional information.
```

**回复类型 C：接受拒审但请求指导**
```
Thank you for the feedback.

We understand the concern regarding [issue]. We would like to better
understand the specific requirement so we can make the appropriate changes.

Could you please clarify:
1. [具体问题1]
2. [具体问题2]

This will help us address the issue correctly and avoid similar problems
in future submissions.
```

### 4.2 "Eligible to be Resolved on Your Next Update" 专用模板

当审核员说某个问题 "eligible to be resolved on your next update"（可在下一次更新中修复），说明该问题不会阻止本次发布，但需要在下一版本修复。

**场景**：审核员标注某 minor issue 可以在下次更新处理，但当前版本可以通过。

**回复模板**：
```
Thank you for the review and for noting that [issue description] is eligible
to be resolved in our next update.

We acknowledge this feedback and confirm that we will address [specific issue]
in our next app update (planned for [大概时间，如 Q2 2026]).

Our planned fix:
[简述修复方案]

We appreciate Apple's flexibility in allowing us to proceed with the current
version while we prepare the comprehensive fix. We are committed to maintaining
full compliance with the App Store Review Guidelines.

Please proceed with the review of the current version.
```

**注意**：此类问题通常为 Metadata 小问题或 UX 改进建议，不适用于隐私、IAP、SIWA 等核心合规问题。

### 4.3 被拒后 Resubmit 完整操作流程

被拒审后修复并重新提交是最常见的操作，但 ASC 的版本/构建模型容易让新手困惑。以下是完整决策树和操作步骤。

#### 4.3.1 Version vs Build 的概念区分

| 概念 | Info.plist 字段 | 示例 | 对外可见 |
|------|-----------------|------|----------|
| **Version**（App Store 版本号）| CFBundleShortVersionString | `0.1.3` | ✅ 用户在 App Store 看到 |
| **Build**（构建号）| CFBundleVersion | `4` | ❌ 仅审核员和开发者可见 |

**核心规则**：一个 Version 下可以关联多个 Build。ASC 允许在**同一个 Version 0.1.3 的页面里更换 Build** —— 这是被拒后最常用的重提交方式。

#### 4.3.2 要不要新建 Version 的决策表

| 情况 | 新建 Version? | 操作 |
|------|--------------|------|
| 只修 bug，代码改动小，重新 resubmit | ❌ 不要 | 同一 Version 0.1.3 下递增 Build 号 |
| Apple 说 "eligible to be resolved on your next update" 且你选豁免 | ❌ 不要 | 仅在 Resolution Center 回复（§4.2 模板）；Build/Version 都不动 |
| 你点过 "Remove This Version" 撤回 | ✅ 必须新建 | ASC 强制新建下一 Version |
| 顺手带一批新功能或明显变更 | ✅ 建议新建 | 0.1.3 → 0.1.4，What's New 相应更新 |
| 拒审后隔了 ≥ 30 天未处理，Version 自动过期 | ✅ 必须新建 | ASC 该 Version 可能已关闭 |

#### 4.3.3 Resubmit 6 步流程（最常用：同 Version 换 Build）

**Step 1 · Xcode 修代码并递增 Build number**

```
Target → General
  Version:  0.1.3       ← 保持不变
  Build:    4           ← 从 3 递增到 4（不能复用或倒退）
```

或在 `Info.plist` 直接编辑：
```xml
<key>CFBundleShortVersionString</key>
<string>0.1.3</string>
<key>CFBundleVersion</key>
<string>4</string>
```

**Step 2 · Archive & Upload**

```
Xcode → Product → Archive
Organizer → Distribute App → App Store Connect → Upload
```

等待 ASC 处理 Build（5~15 分钟 Processing 状态），完成后 TestFlight 列表可见。

**Step 3 · 在 ASC 版本页替换 Build**

1. ASC → 我的 App → [你的 App] → 左侧选中被拒的 **iOS App 0.1.3**（状态 "Rejected"）
2. 滚动到 **Build** 区域
3. 点现有 build 右边的 **"-"** 移除旧 Build
4. 点 **"+"** 选择新上传的 build 4
5. Save

**Step 4 · 更新 App Review Information（重要）**

在 Review Notes 末尾**追加**修复说明（见 §4.3.4 模板），降低审核员的不信任感。

**Step 5 · Resubmit for Review**

版本页顶部的按钮从 "Submit for Review" 变为 "Resubmit"（仅在 Rejected 状态下显示）。点它。

**Step 6 · 回复 Resolution Center**

**在 Step 5 之后**，去 ASC → Resolution Center 贴回复（§4.1 类型 A 模板），内容应包含新 build 号（如 `build 0.1.3 (4)`）。

#### 4.3.4 Review Notes 追加修复说明模板

在原有 Review Notes 末尾**追加**（不要替换），让审核员能对比前后差异：

```
===== UPDATES IN BUILD [新 build 号] (addressing [拒审日期] feedback) =====

1. Guideline [X.X.X] — [简短摘要]
   [具体修复内容，1-3 句]
   
   Verification: [审核员如何快速验证修复]
   Example: "Launch the app → you should land on main Tab without login prompt."

2. Guideline [X.X] — [简短摘要]
   [具体修复内容]
   
   Verification: [如何验证]

No changes to demo account credentials or backend setup.
```

**写作要点**：
- 每个修复条目一定加 **Verification** 行告诉审核员"怎么一秒验证"。这是通过率最大的加速器。
- 不要用 marketing 语言（"we improved UX"），直接描述**技术改动**。
- 如果测试路径变了，明确写新的复现步骤。

#### 4.3.5 常见坑

| 坑 | 症状 | 正确做法 |
|---|------|---------|
| **Build number 倒退或复用** | Upload 报错 "build already exists" | 新 Build 号必须严格大于历史最大值 |
| **只回复 Resolution Center 不点 Resubmit** | Apple 不会拿新 Build 去审 | Resubmit 按钮 + Resolution Center 回复**两步都要做** |
| **Resolution Center 先回复后 Resubmit** | Apple 回复的时间戳早于 build，审核员可能困惑 | 先 Resubmit 让 Build 进入队列，再回复引用新 build 号 |
| **替换 Build 后忘改 What's New** | 商店看到的 What's New 是旧版 | 若代码修改影响了用户可见功能，同步更新 What's New |
| **Review Notes 只写修了什么** | 审核员不知道从哪验证 | 必须加 Verification 行（怎么复现修复效果）|
| **新建 Version 导致 IAP/订阅测试中断** | 沙盒测试账号关联失效 | 能用同 Version 换 Build 就别新建 Version |
| **拒审后 30 天没动静** | Version 被 ASC 自动撤销 | 尽快 resubmit，或主动 Withdraw 后新建 Version |

---

## 五、申诉流程

### 5.1 何时申诉

**适合申诉的情形**：
- 审核员误解了功能用途（已在 Resolution Center 澄清无效）
- Guideline 解读存在歧义，且有充分理由认为自己合规
- 同类竞品已通过审核，存在一致性问题
- 拒审理由明显错误（如 "app crashes on launch" 但实际可正常运行）

**不适合申诉的情形**：
- 确实违反 Guideline（应修复后重新提交）
- 纯粹的商业诉求（如"我们的产品很重要请通过"）
- 已经在 Resolution Center 多次协商无果的功能性拒审

### 5.2 申诉渠道

**App Review Board（正式申诉）**：
- 入口：ASC → App → 被拒版本 → App Review → Appeal
- 或通过：https://developer.apple.com/contact/app-store/?topic=appeal
- 适用：正式版审核被拒
- 响应时间：通常5~10个工作日

**Beta App Review 申诉**：
- 入口：ASC → TestFlight → 被拒 Build → Contact Us
- 响应更快（2~3个工作日）

### 5.3 申诉信起草指南

**结构**：
1. 背景（App 名称、版本、Bundle ID、拒审 Guideline）
2. 我们的理解（引用 Guideline 原文）
3. 我们的实现（具体说明功能如何合规）
4. 证据（截图、视频、参考竞品）
5. 请求（请重新审核此 App）

**申诉信模板**：
```
Subject: App Review Board Appeal - [App Name] (Bundle ID: com.xxx.xxx)
Version: X.X.X | Build: NNNN
Rejected Guideline: X.X - [Guideline Title]

Dear App Review Board,

We are writing to respectfully appeal the rejection of [App Name] version X.X.X
under Guideline X.X ([Guideline 标题]).

GUIDELINE INTERPRETATION
[引用 Guideline 原文，然后说明你的理解]

OUR IMPLEMENTATION
[详细说明你的功能是如何实现的，为何符合 Guideline]
Specifically:
1. [要点1]
2. [要点2]

SUPPORTING EVIDENCE
- [附件1描述]
- [附件2描述]
- Similar apps currently available on the App Store: [App名称] (ID: XXXXXXXXXX)

We respectfully request that the App Review Board reconsider our submission.
We are fully committed to compliance and are happy to provide any additional
information you may need.

Thank you for your time and consideration.

[Developer Name]
[Contact Email]
[Apple Developer Account ID]
```

### 5.4 申诉注意事项

- 每个 Build 只能申诉一次，谨慎使用
- 申诉期间不能修改 App，若确实需要修改则撤回申诉，修复后重新提交
- 申诉不影响后续版本的审核
- App Review Board 的决定具有最终性，无法再次申诉同一版本

---

## 六、Phased Release 状态机

（详细策略见 `phased-release-strategy.md`，本节仅为快速参考）

```
提交通过
    ↓
Manual Release（开发者手动触发）
    or
Auto Release（通过后自动开始 Phased）
    ↓
Day 1-2:   1%  用户（约7天一个阶段）
Day 3:     2%
Day 4:     5%
Day 5:     10%
Day 6:     20%
Day 7:     50%
Day 8+:    100%（完成）

可操作：
  Pause（暂停，最长30天）→ Resume（恢复）
  Skip to Full Release（立即推送100%）
```

**状态转移规则**：
- 每个阶段持续约24小时（Apple 会在后台自动推进）
- Pause 后30天内不恢复 → Apple 自动推进到100%
- 一旦 100% 无法回退到更低比例
- Hotfix 场景见 `phased-release-strategy.md`

---

## 七、提交独立性（Multiple Submissions in Progress）

### 7.1 背景

历史上 ASC 只允许**同一 App 同一时间一个 submission**——某个 version 正在 "Waiting for Review" / "In Review" 期间，任何其他 submission 都会被阻塞。

自 **2025-10-29** Apple 放宽该规则：可以在既有 submission under review 时，独立提交**不依赖 app version 的 items** 进审核。该次放宽同时覆盖 In-App Events、Custom Product Pages（上限提升到 70 + 新增关键词字段）、Product Page Optimization、Game Center achievements/leaderboards。

### 7.2 当前支持独立提交的项

| 项目 | 是否独立送审 | 用途 |
|------|------------|------|
| **In-App Events** | ✅ 独立 | 赛季上线、活动页等 |
| **Custom Product Pages**（2025-10-29 扩展到 70 页 + 关键词字段） | ✅ 独立 | 投放变体落地页 |
| **Product Page Optimization**（A/B 测试变体） | ✅ 独立 | 图标 / 截图 / promo text A/B |
| **Promotional Text / Localized Metadata**（部分字段） | ✅ 独立 | 无需新 build |
| **Game Center achievements / leaderboards**（2025-10-29 同批上线） | ✅ 独立 | 游戏 |
| **新 app version（含 build）** | 仍受约束 | 同一 App 仍只能一个 version submission 在审 |
| **同一 version 下递增 build** | 仍受约束 | 需等 version submission 完成或取消 |

### 7.3 实操流程

ASC → App → 对应入口（In-App Events / Custom Product Pages / etc.）→ 独立提交按钮，无需取消当前 version submission。

```
Version 1.5 submission           In-App Event submission
─────────────────────            ────────────────────
  Waiting for Review  ────┐
  In Review               │    Submit event
  ...                     │    ↓
                          └──► In Review（独立审核轨道）
                               Approved
                               Scheduled
```

两条轨道**并行独立**，不阻塞对方。

### 7.4 使用建议

- **优先级切换**：核心 bug fix build 在审时，可独立推上活动页 / event 保障业务节奏
- **审核 SLA 差异**：In-App Events 和 Custom Product Pages 通常 < 24h；version review 仍按标准 SLA
- ⚠️ **不要滥用**：独立通道仍会被拒（版权 / metadata / 政策），且 rejection 同样计入 App 审核历史
- ⚠️ 旧版本 IAP promo codes 已于 **2026-03-26** 弃用，改用 Offer Codes（详见 `../references/storekit-iap.md` §九）

### 7.5 代价 / 坑位

- [ ] Custom Product Page 上限自 **35 → 70**（2025-10-29 生效），新增关键词字段用于搜索定向；超过 70 需申请
- [ ] In-App Event 独立提交不代表无限制，每个 App 同一 event 仍需 ≤ 10 个 locale
- [ ] 历史上 "submit additional items" 按钮在 ASC 某些页面隐藏，2025-10-29 已统一入口
- [ ] ⚠️ 经验规则：不同团队看到 feature 上线时间略有差异，部分账号延后至 **2025-11** 才可见

**来源**：
- ✅ [Apple Developer News 2025-10-29: Enhancements to help you submit and market your apps and games](https://developer.apple.com/news/?id=gf6mgrs6)
- ✅ [ASC: Overview of submitting for review](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review/)
- ✅ [MacRumors 2025-10-29 报道](https://www.macrumors.com/2025/10/29/apple-developer-app-store-updates)
