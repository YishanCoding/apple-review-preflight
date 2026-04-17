# TestFlight 外部测试员审核操作手册
> External Tester Review 与 Production App Review 是两条独立审核轨道
> 基于 Apple 官方指南（2026-02-06）+ App Store Connect Help

---

## 一、内部 vs 外部 Tester 根本区别

许多团队误以为 TestFlight 发布就是"无审核通道"，但仅对**内部**成员成立。外部测试员需要一次独立的 Beta App Review（[Apple Developer](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers/)）。

| 维度 | Internal Testers | External Testers |
|------|------------------|------------------|
| 数量上限 | ≤ 100（仅 ASC 团队成员）✅ | ≤ 10,000（任意邮箱 / 公链）✅ |
| 需要 Apple 审核 | ❌ 否，上传即可分发 | ✅ 是，**Beta App Review 必过** |
| 审核 SLA | N/A | ⚠️ 首次 ~24h；后续增量常数小时 |
| 分发方式 | ASC 邀请邮件，无需公链 | Email 邀请 + Public Link（匿名）|
| Production IAP Sandbox | ✅ Sandbox 账号可完整测试 | ✅ Sandbox 账号可完整测试 |
| 适合角色 | QA/PM/内部早期 dogfood | Closed Beta/Open Beta/公测 |
| Build 有效期 | 90 天 ✅ | 90 天 ✅ |
| 每 tester 可安装设备数 | 30 台 ✅ | 30 台 ✅ |

> ⚠️ 关键误区：外部 tester 是否"邀请一次就终身免审"？**不是**。每个新 Version 的首个 Build 都要过 Beta Review；同一 Version 后续 Build 通常可自动放行（见 §三）。

---

## 二、外部 Beta App Review 流程

```
Xcode Archive → Upload
        ↓
ASC 处理（5~15 min Processing）
        ↓
ASC → TestFlight → 选中 Build → Add to External Group
        ↓
填写 "What to Test" + Beta App Description + Review Info
        ↓
点击 Submit for Review
        ↓
Apple Beta Review（⚠️ 通常 ~24h，偶有 48~72h 延迟）
        ↓
Approved → 自动向 External Group 推送邀请 + 公链生效
        or
Rejected → Resolution Center 反馈，修复重提
```

**提交限制**（[Apple Developer](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers/)）：
- 每 24h 最多提交 **6 个 Beta Review 请求**
- 同一 Version **同时只能有 1 个 Build 在 Beta Review 队列**
- 必须先建**至少 1 个 Internal Group** 才能创建 External Group ✅

---

## 三、触发 Beta App Review 的场景

| 场景 | 是否触发新一轮 Beta Review |
|------|----------------------------|
| 首次向 External Group 提交 Build | ✅ 触发完整审核 |
| 同一 Version 下递增 Build（仅 bug fix）| ⚠️ 通常自动放行，不再人工复审 |
| Version 号升级（1.2 → 1.3）| ✅ 首个 Build 必审 |
| 变更 "What to Test" 文案 | ⚠️ 可能触发 metadata 复审 |
| 大版本号跳跃（1.2 → 2.0）| ✅ 视同新 App，必审 |
| 新增权限 / Privacy usage description | ✅ 触发（2.1 + 5.1.1）|
| 新增 IAP / 订阅 SKU | ✅ 触发（3.1.x）|
| Legal / Privacy Policy URL 变更 | ⚠️ 可能触发 metadata 审核 |
| Encryption Export Compliance 声明改动 | ✅ 触发 |

> ⚠️ "自动放行"规则未被 Apple 书面承诺，实战中偶见 Apple 对无关改动仍启动人工复审，不要依赖。

---

## 四、常见拒审原因（与 Production 不同的特殊规则）

尽管是 Beta，**App Review Guidelines 2.1 App Completeness 仍完整适用**（[Apple Developer](https://developer.apple.com/app-store/review/guidelines/#app-completeness)）。

| Guideline | Beta 典型拒审点 | 应对 |
|-----------|----------------|------|
| 2.1 | 占位符 / Lorem ipsum / 空白页 / "TODO" 标签 | Beta 也要功能完整，未完成页禁入口 |
| 2.1 | Crash on launch（最常见）| 上传前至少一轮内部冒烟 |
| 2.3.1 | What to Test 描述空或仅写 "bug fixes" | 列出具体测试点 |
| 3.1.1 | IAP 配置未同步 ASC（价格缺失）| Sandbox 账号实测走通购买 |
| 5.1.1 | 新权限未在 Info.plist 加 Usage Description | 见 `./cicd-upload.md` §四 ITMS-90683 |
| 5.1.2 | Privacy Nutrition 与实际数据收集不符 | 与 Production 同等标准 |
| 4.8 | 第三方登录但无 Sign in with Apple | 同 Production 规则 |
| 2.3.3 | Beta App Description 含对比/贬损用语 | 中性描述 |

> ⚠️ Demo Account 要求与 Production **完全相同**：有登录门槛的 Beta Build 必须提供测试账号，否则必拒。参考 `./review-ops.md` §三模板。

---

## 五、被拒后处理

1. **ASC → TestFlight → 被拒 Build → Resolution Center** 查看理由
2. 修复代码或 metadata（`What to Test` / Beta Description 等）
3. **是否需要新 Build**：
   - 仅 metadata 问题 → 直接编辑 metadata，重新提交 Review，无需新 Build ✅
   - 代码问题 → Xcode 递增 Build number，Archive + Upload，选新 Build 重提
4. **旧 Build 是否失效**：Rejected Build **不会**自动失效，但也无法分发给外部；可在 ASC 手动 Expire
5. **快速通道**：Beta Review 拒审可通过 ASC → TestFlight → Contact Us 申诉（`./review-ops.md` §5.2），通常 2~3 工作日响应
6. 被拒**不计入** Production App Review 历史，不影响正式版审核记录 ✅

---

## 六、Production Review 与 Beta Review 的关系

| 问题 | 答案 |
|------|------|
| 可以并行提交吗？ | ✅ 可以，Beta 审核与 Production 审核是独立队列 |
| Beta Approved 是否加速 Production Review？ | ❌ **不会**。两条轨道完全独立，审核员也不共享 |
| Beta Review Notes 会被 Production 审核员看到吗？ | ❌ 不会。必须在 Production 的 App Review Information 里重填 |
| Beta 被拒后能否继续提交 Production？| ✅ 可以，互不阻断 |
| 同一 Build 能否既用于 Beta 也用于 Production？| ✅ 可以，ASC 允许一个 Build 同时关联 External Group 和 App Store 版本 |
| Production 拒审期间能继续发 Beta 吗？| ✅ 可以，Beta 轨道不受影响 |

> ⚠️ 实战建议：用 Beta 先跑一轮外部测试并稳定后，再提交 Production，可降低 Production 首轮拒审率，但 Beta Approved **不等于** Production 会过。

---

## 七、提交前 Checklist

- [ ] Build 已完成 ASC Processing，未标记为 "Missing Compliance" 或 "Invalid Binary"
- [ ] 至少 1 个 Internal Group 已建立（External Group 的前置条件）✅
- [ ] Beta App Description 填写完整（[Apple Developer](https://developer.apple.com/testflight/)）
- [ ] "What to Test" 包含具体测试路径，非 "bug fixes"
- [ ] Beta App Review Information：Demo Account + 联系邮箱 + 电话
- [ ] Privacy Nutrition Label 与实际数据收集一致（5.1.1 / 5.1.2）
- [ ] 所有新增权限有 Info.plist Usage Description（2.5.1）
- [ ] 首次使用加密：Export Compliance 已声明
- [ ] IAP SKU 在 ASC 状态为 "Ready to Submit" 或 "Approved"（3.1.1）
- [ ] 无 Lorem ipsum / TODO / 占位符页面（2.1）
- [ ] 已内部冒烟测试，无启动崩溃（2.1）
- [ ] Privacy Manifest 已包含（`../references/privacy-manifest.md`）

---

## 八、常见坑

| 坑 | 症状 | 正确做法 |
|---|------|---------|
| **External Group 10,000 上限是"每 App"** | 多公链叠加触顶 | 所有 External Group 共享 10k 配额，规划分组 |
| **Build 90 天自动过期** | Tester 报 "Beta expired" | 发布前 7 天上传新 Build，保持滚动 |
| **Family Sharing 不适用 TestFlight** | Tester 家人无法共享 Beta | ⚠️ TestFlight Beta 不支持 Family Sharing，每人需单独邀请（[Apple Legal](https://www.apple.com/legal/internet-services/testflight/)）|
| **公链分享导致 PII 泄露** | 匿名 tester 数据进入你的后台 | 公链打开 "Filter by Criteria" 或改用 Email 邀请 |
| **What to Test 是 public** | 泄露未发布功能 | 不写机密 roadmap，尤其公链 Beta |
| **Beta Review 期间无法修改 metadata** | "Submit" 按钮灰掉 | 先 Cancel Review，改完再提 |
| **Sandbox IAP 账号误登真实 Apple ID** | 购买走真实扣款 | Settings → App Store → Sandbox Account 单独登录 |
| **Tester 升级 iOS 后 Build 不兼容** | Crash on launch | 维护 min deployment target，及时出 compat Build |
| **公链无法在欧盟 DMA 区域启用** | ⚠️ 部分地区政策限制 | 关注 ASC 区域设置和 Alternative Distribution 条款 |
| **Internal Build 误发给外部** | 外部收不到 | External Group 要求 Build **非** Internal Only，且已过 Beta Review |

---

## 相关文档
- `./review-ops.md` — Production App Review 操作、Review Notes 模板、申诉流程
- `../by-app-type/all-apps.md` — 跨类型通用审核要点
- `../checks/review-failure-map.md` — 拒审条款 → 修复路径映射
- `../references/privacy-manifest.md` — Privacy Manifest 与 Required Reason API
