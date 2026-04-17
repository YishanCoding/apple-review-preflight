# Apple Guidelines 变动日志

> 按时间倒序记录 App Store Review Guidelines 和相关政策的变动。
> 基线版本：2026-02-06（Apple 最新 Guidelines 版本）
> 更新方法见 `update-playbook.md`

---

## 变动记录

### 2026-04-01 — iOS 26.4 系统级年龄验证上线

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 年龄分级 | 英国区启用 18+ App 系统级年龄验证（Online Safety Act 合规） | `../market-overrides/uk.md` 第五章专项、`../references/store-metadata-compliance.md` 第四章通用 |
| 年龄分级 | 澳大利亚、巴西、新加坡于 2026-02-24 启用 18+ App 系统级年龄验证 | `../references/store-metadata-compliance.md` 第四章全局年龄验证推进时间表 |
| 年龄分级 | 犹他于 2026-05-06 启用 18+ App 系统级年龄验证 | `../market-overrides/us.md` 第六章已记录 |
| 年龄分级 | 路易斯安那于 2026-07-01 启用 18+ App 系统级年龄验证 | `../market-overrides/us.md` 第六章已记录 |

---

### 2026-03-31 — App Store 新增 11 种本地化语言

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 元数据 / 2.3 | 新增 Bangla / Gujarati / Kannada / Malayalam / Marathi / Odia / Punjabi / Slovenian / Tamil / Telugu / Urdu 共 11 种本地化；总数达 50 | `../references/store-metadata-compliance.md` §6.2 |

来源：[Apple Developer News 2026-03-31: App Store expands support to 11 new languages](https://developer.apple.com/news/?id=97t4mt64)

---

### 2026-03-30 — Apple Developer Program License Agreement 更新（新 framework 条款）

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| ADPLA §3.3.3(B), §3.3.7(K) | **Foveated Streaming** framework：新增使用要求 + 数据隐私说明（XR/空间内容的 eye-tracking 渲染） | ⚠️ 新增；涉及 visionOS / streaming App 需单独核对 ADPLA 条款 |
| ADPLA §3.3.3(Q) | **Family Controls** framework：新增使用要求（Screen Time / Parental Controls 类 App） | ⚠️ 新增；涉及家长控制类 App 需单独核对 ADPLA 条款 |
| ADPLA §3.3.7(J) | **Accessory Notifications** + **Accessory Live Activities** framework：新增使用要求（外设 / 配件类 App） | ⚠️ 新增；涉及配件控制 / live activity 的 App 需核对 ADPLA 条款 |

**签署要求**：开发者须登录 ASC → Agreements 接受更新后的 ADPLA 才能继续提交。翻译版本在公告后 1 个月内更新。

来源：[Apple Developer News 2026-03-30: Updated Apple Developer Program License Agreement now available](https://developer.apple.com/news/?id=fwswmjcn)

---

### 2026-03-26 — 医疗器械状态声明正式上线

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 1.4 / ASC | 新 App 立即需声明医疗器械状态（EEA/UK/US） | `../references/medical-device-status.md` 专门文件 |
| 1.4 / ASC | 存量 App 截止 early 2027 | `../by-app-type/health-fitness.md` 已引用 |

---

### 2026-03-15 — 中国区 App Store 佣金下调 ✅

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 佣金 / 3.1 | 中国大陆 storefront 标准 IAP 佣金 30% → **25%** | `../market-overrides/china.md` §7.3；`../references/storekit-iap.md` §八 |
| 佣金 / 3.1 | Small Business Program + Mini Apps Partner Program 15% → **12%** | 同上 |
| 佣金 / 3.1 | 订阅第二年 loyalty rate 15% → **12%**（中国区专属） | 同上 |
| 佣金 / 3.1 | 其他地区费率不变 | — |
| 佣金 / 3.1 | 无需签署更新条款即可享受新费率（Apple 明文） | — |

来源：✅ [Apple Developer News 2026-03-12: Adjustments to the China storefront of the App Store on iOS and iPadOS](https://developer.apple.com/news/?id=dadukodv)；媒体解读 [Bloomberg 2026-03-13](https://www.bloomberg.com/news/articles/2026-03-13/apple-lowers-app-store-cut-to-25-from-30-in-china-to-fend-off-local-regulators) / [TechCrunch 2026-03-13](https://techcrunch.com/2026/03/13/apple-drops-commission-rates-in-china-25-percent/)。

---

### 2026-02-06 — Guidelines 版本更新（当前基线）

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 整体 | Apple 发布 Guidelines 最新版本，本 skill 所有文件基于此版本 | 全部文件基线 |

---

### 2026-02-03 — SDK 最低要求公告

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 新增要求 | 2026-04-28 起必须使用 iOS 26 / iPadOS 26 / tvOS 26 / visionOS 26 / watchOS 26 SDK 编译 | `../references/new-os-api-compliance.md` 专门文件 |
| 新增要求 | 必须使用 Xcode 26 | `../operations/cicd-upload.md` CI/CD 环境需更新 |

---

### 2025-06-27 — EU DMA 全面改革公告

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 3.1 / EU | CTF → CTC（5% 佣金替代 €0.50/安装费） | `../market-overrides/eu-eea.md` 第一章 |
| 3.1 / EU | 新费用体系：Acquisition Fee (2%) + Store Services (5-13%) + CTC (5%) | `../market-overrides/eu-eea.md` 费用表 |
| 3.1 / EU | 2026-01-01 起统一新商业模式 | `../market-overrides/eu-eea.md` 第一章 |
| 3.1 / EU | 外部购买链接规范更新 | `../market-overrides/eu-eea.md` 第二章 |

---

### 2025-01-31 — 年龄分级问卷更新

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 年龄分级 | 引入 13+ / 16+ / 18+ 新分级梯度 | `../references/store-metadata-compliance.md` 第四章 |
| 年龄分级 | 问卷新增「医疗/治疗信息」频度选项 | 与医疗器械声明触发条件关联 |

---

### 2024-05-01 — Privacy Manifest 强制执行

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 5.1.1 | 新 App 和 App 更新必须包含 PrivacyInfo.xcprivacy | `../references/privacy-manifest.md` 专门文件 |
| 5.1.1 | 第三方 SDK 必须提供自己的 Privacy Manifest | `../checks/required-reason-api-scan.md` |

---

### 2024-03-06 — DMA 正式生效

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| EU | Apple 被认定为守门人，初版 DMA 合规方案上线 | `../market-overrides/eu-eea.md`（后续被 2025-06 改革覆盖） |

---

### 2022-06-30 — 账号删除功能强制要求

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| 5.1.1(v) | 所有支持账号注册的 App 必须提供账号删除功能 | `../by-app-type/all-apps.md` checklist |
| 5.1.1(v) | Sign in with Apple 用户删除时必须 revoke token | `../references/sign-in-with-apple.md` 第五章 |

---

## 维护说明

- 新增记录插入在最顶部（时间倒序）
- 每条记录必须包含：日期、影响条款、变动摘要、本 skill 相关文件
- 用 `scripts/check-guideline-updates.sh` 检测 Apple 官网变动
- 检测到变动后按 `update-playbook.md` 流程更新
