---
name: apple-review-preflight
description: Use for App Store review compliance, submission preflight, rejection handling, and post-submission operations with Apple for iOS/iPadOS/macOS/tvOS/watchOS/visionOS apps. Covers App Review Guidelines, App Privacy, privacy manifests, required-reason APIs, IAP/subscriptions, Sign in with Apple, review notes, appeals, expedited review, account termination/warnings, IP infringement disputes, review manipulation/bad-review handling, editorial featuring nominations, app removal/chart-drop recovery, and contacting Apple channels. Triggers on: 审核被拒, 上架预检, 提交前合规检查, 加速审核, 被下架, 封号, 账号警告, 差评, 推广报备, 精品推荐, 侵权, 申诉, 联系苹果, App Review, review notes, appeal, expedited review, account termination, app removal, bad reviews, featuring nomination, IP infringement, DMCA, 2.1, 3.1, 3.2(f), 4.3, 4.8, 5.1, privacy manifest, PrivacyInfo.xcprivacy, Sign in with Apple, age rating 合规. Not for ASO keyword research, screenshot conversion optimization, or listing copywriting.
---

# Apple App Store Review Preflight

Apple 2024年审核了770万次提交，拒绝了190万次。**大多数拒审可以在提交前完全预防。**

**全文标记约定**：✅ = Apple 官方明文；⚠️ 经验规则 = 社区/实战共识，非 Apple 明文；⚠️ 待实测 = Apple 行为未公开验证；⚠️ 以 Apple 最新文档为准 = 政策浮动中；⚠️ 法律风险提示 = 涉及合同/诉讼，建议咨询律师。

---

## 快速入口

**路由多匹配时的优先级**：联系场景 > 任务 > App 类型 > 地区。前三者确定主流程（该读哪个文件做什么），地区叠加本土特殊要求。例：「订阅在中国区被拒」→ 先 `operations/review-ops.md`（主流程），再 `by-app-type/subscription.md`（订阅专项），最后 `market-overrides/china.md`（中国区覆盖）。

### 按任务路由

| 任务 | 读哪里 |
|------|--------|
| 提交前完整预检 | 本文件流程 → `scripts/preflight-scan.sh` → `checks/review-failure-map.md` |
| 被拒后处理/申诉 | `operations/review-ops.md` |
| IAP / 订阅合规 | `guidelines/3-business.md` + `references/storekit-iap.md` |
| 隐私/PrivacyInfo | `references/privacy-manifest.md` + `checks/privacy-transparency-consistency.md` |
| 元数据/截图/年龄分级 | `references/store-metadata-compliance.md` |
| 新 OS/SDK 要求 | `references/new-os-api-compliance.md` |
| 医疗器械状态声明 | `references/medical-device-status.md` |
| Sign in with Apple | `references/sign-in-with-apple.md` |
| 核心条款速查 | `guidelines/core-guidelines-map.md` |
| 政策来源映射 | `policy/source-map.md` |
| 政策更新日志 | `policy/policy-updates-log.md` |
| 审核时长 / 最佳提交时机 / 高峰期 | `operations/review-timing.md` |
| CI/CD上传失败 | `operations/cicd-upload.md` |
| 分阶段发布 | `operations/phased-release-strategy.md` |
| 政策更新检查 | `policy/update-playbook.md` + `policy/scripts/check-live-sources.sh`（主路径，live 源） + `policy/scripts/check-guideline-updates.sh`（辅助，Wayback 历史） |
| TestFlight 外部测试审核 | `operations/testflight-external-review.md` |
| EU DMA 替代分发（sideload / alt marketplace / web） | `operations/eu-dma-alternatives.md` |
| App Clips | `references/app-clips.md` |
| 推送通知合规（4.5.4） | `references/push-notifications.md` |
| Widget / Live Activity / Dynamic Island | `references/widgets-live-activity.md` |

### 按App类型路由

| App类型 | 文件 |
|---------|------|
| 订阅 | `by-app-type/subscription.md` |
| AI/LLM功能 | `by-app-type/ai-apps.md` |
| UGC/社区 | `by-app-type/ugc-social.md` |
| 交友/Dating | `by-app-type/dating.md` |
| 游戏/loot box | `by-app-type/games.md` |
| 电商/实物 | `by-app-type/ecommerce.md` |
| 儿童分类 | `by-app-type/kids.md` |
| 健康/医疗 | `by-app-type/health-fitness.md` |
| macOS/Catalyst | `by-app-type/mac-macos.md` |
| watchOS | `by-app-type/watchos.md` |
| tvOS | `by-app-type/tvos.md` |
| 加密/金融 | `by-app-type/crypto-finance.md` |
| VPN | `by-app-type/vpn.md` |
| visionOS | `by-app-type/visionos.md` |

### 按地区路由

| 地区 | 文件 |
|------|------|
| 中国大陆 | `market-overrides/china.md` |
| 欧盟/EEA | `market-overrides/eu-eea.md` |
| 英国（post-Brexit 独立监管） | `market-overrides/uk.md` |
| 美区外部支付 | `market-overrides/us.md` |

### 按联系场景路由

| 场景 | 触发关键词 | 文件 |
|------|----------|------|
| 联系 Apple 全通道 | 联系苹果、contact apple、邮箱、电话、通道 | `references/contact-apple-channels.md` |
| 账号警告/终止 | 账号警告、Pending Termination、3.2(f)、封号、账号被封 | `operations/account-warnings.md` |
| 审核时长 / 提交时机 | 审核多久、什么时候提交、高峰期、节假日延迟、review timing、waiting for review 多久、in review 多久 | `operations/review-timing.md` |
| 加速审核 | 加速审核、expedited review、紧急上架、加急 | `operations/expedited-review.md` |
| 知识产权侵权 | 侵权投诉、被侵权、品牌词被占、DMCA、商标、抄袭 | `operations/ip-infringement.md` |
| 差评处理/推广报备 | 恶意差评、差评举报、推广报备、刷榜、review attack | `operations/review-manipulation.md` |
| 被下架/清榜/清词 | 被下架、清榜、清词、排名消失、关键词归零、app removal | `operations/app-penalty-recovery.md` |
| 精品推荐自荐 | 精品推荐、featured、编辑推荐、自荐、App of the Day | `operations/editorial-featuring.md` |

---

## TOP 10 拒审原因（9/10 完全可预防）

> 详细条款映射（含 CRITICAL/HIGH/MEDIUM 三级 + 完整触发信号）见 `checks/review-failure-map.md`。

| 排名 | 原因 | 条款 | 如何预防 |
|------|------|------|---------|
| 1 | 隐私政策缺失/链接失效/内容不完整 | 5.1.1 | 提交前人工点击验证，无需登录即可访问 |
| 2 | 演示账号不可用或后端审核期间下线 | 2.1(a) | Review Notes 提供账号，后端 24/7 在线 |
| 3 | 强制注册才能浏览非账号内容 | 5.1.1(v) | 商品/内容浏览不拦截，只在账号操作时触发登录 |
| 4 | 有账号注册但无账号删除功能 | 5.1.1(v) | 设置页提供真实删除入口 |
| 5 | 元数据与实际功能不符 | 2.3.1 | 截图来自当前版本真实 UI，描述不含未上线功能 |
| 6 | IAP 配置不完整或购买流程中断 | 3.1.1 | 沙盒测试完整购买流程，提供恢复购买 |
| 7 | PrivacyInfo.xcprivacy 缺失或不完整 | 5.1.1 | 所有 Required Reason API 必须声明 |
| 8 | 第三方登录缺少 Sign in with Apple | 4.8 | 任何第三方 OAuth 必须同时提供 Apple 登录 |
| 9 | App 崩溃或明显 bug | 2.1(a) | 真机测试，特别是 iPad 和不同 iOS 版本 |
| 10 | 元数据含竞品名称/促销词 | 2.3.7 | 检查 App Name/Subtitle/Keywords/Description |

---

## 2026 年关键新规

| 规则 | 截止日 | 来源 |
|------|--------|------|
| 必须使用 iOS/iPadOS 26 SDK 编译 | **2026-04-28** | ✅ Apple Upcoming Requirements |
| 年龄分级问卷更新（新增 13+/16+/18+） | 2026-01-31（已过） | ✅ Apple News |
| 医疗器械状态声明（存量 App） | early 2027 | ✅ ASC Help |
| 中国区元数据 AI 品牌词限制 | 持续 | ⚠️ 经验规则（2.3.7推断） |

---

## 预检流程（5步）

### Step 1：项目结构探测 + 自动扫描

**推荐：一键扫描脚本**（输出含 PrivacyInfo per-target 覆盖率矩阵 + Info.plist 全量扫描 + 依赖风险清单）

```bash
# 在 skill 仓库根目录执行，扫描指定项目
bash <skill-root>/scripts/preflight-scan.sh /path/to/your/project

# 或者 JSON 格式（agent 友好）
bash <skill-root>/scripts/preflight-scan.sh /path/to/your/project --format json
```

> ⚠️ 不要假设固定路径（如 `ios/App/App/Info.plist`）。脚本会先做栈探测，再按发现的文件做扫描——原生 iOS / RN / Expo / Flutter / Capacitor / monorepo 的目录结构各不相同，硬编码路径会漏检。

**手工命令集**（脚本不可用时的 fallback，或想自己控制扫描范围）：

```bash
# 0. 项目栈探测 — 先识别项目结构
ls -d ios *.xcodeproj *.xcworkspace 2>/dev/null
ls package.json pubspec.yaml capacitor.config.* Podfile Package.swift 2>/dev/null

# 1. 列出所有 Info.plist（覆盖主 App + 所有 Extension/Widget/App Clip Target）
find . -name "Info.plist" -not -path "*/Pods/*" -not -path "*/node_modules/*" -not -path "*/build/*" 2>/dev/null

# 2. 对每个 Info.plist 检查后台模式和权限描述
find . -name "Info.plist" -not -path "*/Pods/*" -not -path "*/node_modules/*" -not -path "*/build/*" -print0 2>/dev/null | \
  while IFS= read -r -d '' f; do
    echo "=== $f ==="
    plutil -p "$f" 2>/dev/null | grep -E "UIBackgroundModes|UsageDescription|NSUserTracking" || echo "(no matches)"
  done

# 3. 列出所有 PrivacyInfo.xcprivacy
find . -name "PrivacyInfo.xcprivacy" 2>/dev/null
```

脚本会自动枚举：
- `Info.plist`
- `PrivacyInfo.xcprivacy`
- `.xcodeproj` / `.xcworkspace`
- `*.entitlements`
- `Podfile` / `Package.swift`
- `package.json` / `pubspec.yaml` / `capacitor.config.*`
- 可能存在的 App Clip / Widget / Extension 目录

**如果脚本输出多个 target 或多个 `Info.plist` / `PrivacyInfo.xcprivacy`**：
- 继续审计时必须按 target 逐个检查，不能只抽样看一个文件
- App Clip / Widget / Activity Extension 视为独立 bundle，manifest 覆盖要单独确认

### Step 2：按 App 类型加载专项 checklist

先读 `by-app-type/all-apps.md`，再加载匹配的类型文件。

### Step 3：运行 checks/ 扫描

必跑：
- `checks/review-failure-map.md` — 按条款的高频拒审原因
- `checks/privacy-transparency-consistency.md` — 隐私五处一致性
- `checks/required-reason-api-scan.md` — Required Reason API
- `checks/background-modes-scan.md` — 后台模式滥用
- `checks/code-scan-patterns.md` — 代码风险模式

### Step 4：区域检查

如分发到中国大陆，读 `market-overrides/china.md`。
如分发到 EU，读 `market-overrides/eu-eea.md`。

### Step 5：输出报告（强制 contract）

使用 `checks/report-template.md` 输出报告，**必须包含以下五段**（缺一则报告无效）：

| # | 段落 | 必填字段 |
|---|------|---------|
| 1 | **scope** | App 类型 / Bundle ID / 分发地区 / 技术栈 / 检查日期 / Guidelines 版本 / 实际扫描的 Target 列表（主 App + 所有 Extension） |
| 2 | **findings** | 按严重性分级（CRITICAL / HIGH / MEDIUM），每条带条款编号 + 证据（文件:行号 / 配置项名 / 截图描述）+ 修复建议；同级内按条款编号排序 |
| 3 | **passed** | 已通过的检查项（避免遗漏感、便于复检） |
| 4 | **missing inputs** | 因缺信息无法验证的项目 + 需要的具体输入 |
| 5 | **final recommendation** | 明确 go / no-go + 理由 |

**Fail-fast 规则**：
- 任一 CRITICAL 未修复 → final recommendation 必须为 **no-go**
- missing inputs 包含演示账号 / 后端在线状态 / IAP 沙盒结果 / PrivacyInfo Target 覆盖率之一 → 不得标 go，先补齐输入再判断
- 报告中所有 finding 必须有可定位的证据（文件路径+行号 / 截图引用 / 配置项名）；纯主观或"建议检查"不算 finding，应放入 missing inputs
- 报告未引用本次实际运行的 Step 1 探测结果（项目栈 + Target 列表） → 报告无效，重跑 Step 1

**最小输出契约**：
- `Scope`：本次检查覆盖的目录、target、平台、分发地区
- `Findings`：按 CRITICAL / HIGH / MEDIUM 分类，必须附证据
- `Missing Inputs`：无法验证的 ASC / 账号 / 沙盒 / 后端输入
- `Evidence`：命令输出、文件路径、条款号、截图来源
- `Final Recommendation`：`Ready to submit` / `Submit with known risks` / `Do not submit`

---

## 提交前快速检查清单

> 关键子集，完整清单（每项带「为什么重要」注释）见 `by-app-type/all-apps.md`。提交前请以 all-apps.md 为准。

**隐私与账号**
- [ ] 隐私政策 URL：有效、无需登录可访问、内容完整
- [ ] 所有法律链接（EULA/Terms）：人工点击验证，非 404
- [ ] 有账号注册 → 有账号**删除**功能（非停用）
- [ ] 游客可浏览非账号功能，不强制注册
- [ ] 有第三方 OAuth → 同时提供 Sign in with Apple
- [ ] ATT 弹窗：仅在有跨 App tracking 时出现，且在任何 tracking 之前
- [ ] 每个 App bundle / App Clip / Widget / Activity Extension 都有自己的 `PrivacyInfo.xcprivacy`（如适用）
- [ ] 所有 Required Reason API 均已在对应 target 的 manifest 中声明

**功能与稳定性**
- [ ] 演示账号已准备（填入 App Review Notes）
- [ ] 后端服务审核期间 24/7 在线
- [ ] 无崩溃（真机测试，包括 iPad）
- [ ] IPv6 网络下正常工作
- [ ] 所有 IAP 沙盒测试通过，恢复购买可用
- [ ] 2026-04-28 后：使用 iOS 26 SDK 编译

**元数据**
- [ ] 截图：来自当前版本真实 UI，设备边框正确
- [ ] App Name（≤30字）：无促销词、无竞品名、无「app」
- [ ] Description：无未上线功能、无竞品名称
- [ ] App Review Notes 填写完整

**设计**
- [ ] 正文字号在真实 iPhone/iPad 上可读
- [ ] 提供超越纯 WebView 的原生价值

---

## ASC 系统错误 vs 人工拒审判断矩阵

| 状态/错误 | 是否进入人工审核 | 正确处理 |
|-----------|----------------|---------|
| Build 卡在 Processing | 否 | 查 ASC/Apple System Status，检查 Privacy Manifest 和 SDK 签名 |
| ITMS-90xxx / asset validation failed | 否 | 看上传链路，不要改业务代码 |
| Metadata Rejected | 是（轻量） | 修截图/文案/年龄分级，无需重新打包 |
| Rejected（含 Guideline 编号） | 是 | 进 `operations/review-ops.md` 流程 |

---

## 参考来源

- [App Store Review Guidelines](https://developer.apple.com/cn/app-store/review/guidelines/) — 最后更新 2026-02-06
- [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/)
- [App Review](https://developer.apple.com/distribute/app-review/)
- [Offering Account Deletion](https://developer.apple.com/support/offering-account-deletion-in-your-app/)
- 更新日志见 `policy/policy-updates-log.md`
