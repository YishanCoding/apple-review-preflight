# 交友类 App 专项风险（Dating / Friend-Making）

> 本文件仅记录交友 / 社交匹配类 App 超出通用审核规则的专项要求。适用于所有以"匹配陌生人""约会""交友""同城聊天""兴趣匹配"为主要功能的 App。
> 通用 UGC 规则见 `./ugc-social.md`，本文件只列增量。

---

## 1. 交友类 App 为什么高拒审

交友类是 App Store **历史上拒审率最高的类别之一**（⚠️ 经验值：实测 30–50%，高于均值 15–20%）。核心原因：

| 条款 | 拒审焦点 | 常见触发 |
|------|---------|---------|
| 1.4 | 涉及**物理伤害/线下见面风险** | 无"线下见面安全提示"、无身份核验、未成年保护缺失 |
| 1.2 | 用户生成内容 + 陌生人互动 | 无举报/屏蔽/审核闭环、匿名聊天无准入 |
| 1.2 + Age Rating | 儿童安全（child safety） | 未成年能进入成年聊天池、无年龄门 |
| 1.1.4 | 色情 / hookup / prostitution 内容 | 裸露内容、暗示性 hookup 表达、facilitate prostitution |
| 5.1.1 | 真实身份与隐私 | 要求真实姓名/身份证号无合理解释，或反之"完全匿名"导致骚扰 |
| 3.1.2 | 订阅类合规 | 「看谁喜欢了我」「无限右滑」订阅 UI 欺骗 |
| 4.8 | 第三方登录 | 只有 Facebook / 手机号，无 Sign in with Apple |

Apple 对 **"Chatroulette-style 随机聊天"** 和 **"仅基于地理位置的陌生人配对"** 保持高警惕，2024–2026 连续收紧（见第 5 节）。

---

## 2. 年龄门与验证（1.2 + Age Rating 元数据 + 1.4）

### 2.1 年龄分级

- [ ] 年龄分级**必须 17+**（涉及 unrestricted web access / 陌生人交流 / 可能的暗示性内容）
- [ ] ⚠️ 仅"同性朋友找朋友 / 同兴趣社群"且**明确禁止浪漫/约会表达**的 App 可考虑 12+，但易被 Apple 重新归类为交友 → 拒审。默认 17+ 更安全
- [ ] Primary Category 选 `Social Networking` 或 `Lifestyle`，不能选 `Entertainment`（会被重新分类后拒）

### 2.2 年龄验证流程

- [ ] **注册首屏必须有年龄门**，不是一个"我已年满 18"的复选框
- [ ] 输入生日（日 / 月 / 年），后端校验，**不能只选"我 > 18"**
- [ ] 18 岁以下用户：直接阻止注册，或明确切换为"仅朋友模式"（无浪漫匹配、无精确位置）
- [ ] Cookie / LocalStorage 记录已通过年龄门，防止用户绕开再注册
- [ ] ⚠️ 建议在 Review Notes 里写清"未成年注册流程演示路径"，避免审核员误判

### 2.3 iOS 26.4 系统级年龄信号（2026 新变量）

自 2026-02-24（澳洲 / 巴西 / 新加坡）与 2026-04-01（英国）起，iOS 26.4 在这些地区推送**系统级年龄声明**，App 可通过 `DeclaredAgeRange` API 读取用户声明的**粗粒度年龄段**（以年龄区间上下限表达，例如 "上限 < 18" 或 "下限 ≥ 18"）。⚠️ 待实测：API 具体类型与字段以 [Apple 开发者文档](https://developer.apple.com/documentation/declaredagerange) 为准。

- [ ] 在上述地区上架的交友 App **应调用 `DeclaredAgeRange`**，拒绝上限 < 18 的用户注册
- [ ] 未调用系统年龄信号 + 仅自报年龄，在英国/澳洲上架会因 **1.2 / 1.4 + Age Rating 元数据** 被重点关照
- [ ] Utah / Louisiana 年龄验证法要求 App Store 层做过滤，开发者侧仍需自己实现应用内阻止
- [ ] ⚠️ iOS 26.4 年龄信号是**粗粒度、可用户声明的**，不等于真实年龄验证。对中高风险交友 App 仍需要独立 KYC / 证件验证流程

---

## 3. 举报 / 屏蔽 / 封禁机制（1.2 核心，拒审 #1 原因）

这是交友类 **最高频拒审点**，审核员会直接在 App 内寻找这些入口，找不到即拒。

### 3.1 必备四件套（相较 UGC 更严）

- [ ] **屏蔽用户**（block）：入口在对方个人页 + 聊天界面「···」里，立即生效，对方聊天 / 匹配 / 出现在列表全部消失
- [ ] **举报用户**（report user）：独立于"举报内容"，举报后该用户**立即从当前用户视野消失**
- [ ] **举报内容 / 消息**：每条消息、每张照片、每段语音旁都能长按举报
- [ ] **不礼貌行为 / 骚扰投诉**：专门分类，而非"其他"一项兜底

### 3.2 违规内容处理 SLA（EU DSA + 运营目标）

- [ ] EU 用户遇到明显违规内容（NCII / CSAM / 骚扰）必须走 DSA 第 16 条 notice-and-action 流程
- [ ] ⚠️ 经验规则：社区通行的内部运营目标为 **24h 内处理明显违规**。DSA 第 16 条本身并未规定硬性 24h SLA，"obviously illegal" 内容的"及时处理"是法律解读，非 Apple 明文要求
- [ ] CSAM 必须**自动拦截**（0 容忍，不依赖人工 SLA）
- [ ] Review Notes 中写明 Moderation 团队规模 + 响应时间
- [ ] ⚠️ 小团队建议在 Review Notes 说明"自动过滤 + 48h 人工"而非空白，直接写 "we use AI" 审核员常常不信

### 3.3 申诉机制（Appeals）

- [ ] 被封禁 / 被警告用户有**申诉入口**（email 或应用内工单）
- [ ] 申诉处理有 SLA 承诺（通常 72h）
- [ ] ⚠️ EU DSA 要求透明的申诉渠道，缺失易被 1.2 + 5.6 联合拒审

详见 `./ugc-social.md` §1 四件套与 `../checks/review-failure-map.md` → "1.2 UGC"。

---

## 4. 内容审核（1.2）

### 4.1 过滤层（人工 + 自动必须双重）

| 层 | 最低要求 | 推荐实现 |
|----|---------|---------|
| 文本 | 关键词 + 上下文 | OpenAI Moderation / Perspective API |
| 图片 | CSAM 哈希 + NSFW 分类 | PhotoDNA（CSAM）+ AWS Rekognition / Google Vision SafeSearch |
| 语音 | 至少转文字后过滤 | ASR + 文本管线 |
| 视频 | 抽帧 NSFW + 语音管线 | 抽帧 + Rekognition Video |

### 4.2 NSFW 处理

- [ ] **默认禁止**裸露 / 色情内容 → 1.1.4 / 1.1.3
- [ ] 若允许 "suggestive"（泳装、暗示）→ **必须 17+ + 有开关**，默认关闭
- [ ] ⚠️ 2022-10 起，Apple 明确禁止 "hookup apps that may include pornography or facilitate prostitution"
- [ ] **Tea / TeaOnHer 事件教训（2025-10 下架）**：让用户上传他人信息"做背景调查"违反 5.1.2，即使出发点是"女性安全"

### 4.3 NCII（Non-Consensual Intimate Imagery，"复仇色情"）

- [ ] **零容忍政策**写入社区准则与 Review Notes
- [ ] 举报 NCII 有独立入口，走紧急处理管线（目标 ≤ 1 小时）
- [ ] 接入 StopNCII.org 哈希库（可选，但对审核员有说服力）

### 4.4 ML-based 图片检测（Apple 推荐）

- [ ] 头像 / 聊天图片上传前本地或服务端跑 NSFW 分类
- [ ] 疑似违规自动进入人工队列，**不直接发布**
- [ ] 在 Review Notes 中写明所用 ML 模型 / API（增加可信度）

---

## 5. 随机聊天 / 匿名聊天（1.2 特别限制，2024+ 收紧）

⚠️ **自 2024 年 Apple App Review Guidelines 更新**：「Apps used primarily for pornographic content, Chatroulette-style interactions, random or anonymous chat, objectification of real people, physical threats, or bullying **do not belong on the App Store and may be removed without notice**」。

### 5.1 什么样的「随机 / 匿名」会被拒

- [ ] 「随机匹配陌生人 1v1 聊天」且**无注册门槛** → 直接拒审（等同 Omegle）
- [ ] 「隐藏身份与对方聊天」作为主打 → 直接拒审
- [ ] App 描述 / 截图 / 关键词出现 `stranger chat` / `random chat` / `anonymous chat` → 命中审核员关键词扫描

### 5.2 合规改造方向（若确需随机匹配）

- [ ] 强制注册（手机 / SIWA）+ 实名或**照片真人验证**
- [ ] 匹配前展示基本资料（非完全匿名），或至少展示是已验证用户
- [ ] 聊天全程可举报 / 屏蔽 / 退出
- [ ] 未成年用户**不进入随机匹配池**
- [ ] App 描述避免使用 "random" / "stranger" / "anonymous"，改为 "matched based on interests" / "community"

---

## 6. 隐私与位置（5.1.1 + 1.4）

### 6.1 位置精度

- [ ] **默认只显示距离**（"2 km 内"），不显示精确坐标
- [ ] 距离粒度**不得低于 1 km 级别**（⚠️ 经验规则：曾有高精度泄露导致拒审 + 用户起诉的传闻，未见 Apple 官方明文精度门槛）
- [ ] 服务端 API **不得返回真实 lat/lng**，只返回 bucketed distance
- [ ] 关闭位置权限后仍可使用核心功能（或清晰替代：按城市搜索）
- [ ] `NSLocationWhenInUseUsageDescription` 明确说明「用于附近匹配，不会精确共享」

### 6.2 虚假位置 / 反作弊

- [ ] 检测 mock location（iOS 通过 `CLLocationManager.locationServicesEnabled` 与 signal 一致性）
- [ ] ⚠️ 虚拟定位工具容易被滥用做 catfish，审核员不会直接查但用户投诉会进入 5.6

### 6.3 真人验证（Photo Verification / Liveness）

- [ ] 推荐提供可选 "verified badge"：摆特定姿势自拍 + liveness 检测
- [ ] liveness 数据 **不上传云端训练**（隐私政策明示）
- [ ] 验证照片**不公开展示**，仅用于比对
- [ ] ⚠️ 不强制要求，但在 Review Notes 中体现有此能力可显著降低 1.1.4 关注度

### 6.4 头像审核

- [ ] 头像上传前跑 NSFW + 人脸检测（无人脸的头像可选降权，不能禁止）
- [ ] 不允许儿童照片做头像（人脸年龄估计 < 18 → 人工复审）

---

## 7. IAP 与订阅（3.1.2）

交友 App 常见付费模式的合规点：

| 付费模式 | 类型 | 合规要点 |
|---------|------|---------|
| Premium 会员（无限右滑 / 看谁喜欢我） | Auto-renewable subscription | 续订价格、周期、可取消入口必须清晰；试用期规则见 `../references/storekit-iap.md` |
| Boost / Super Like | Consumable | 明示次数 / 时效，不得"模糊赠送"诱导复购 |
| Unlock next match（解锁下一位） | Consumable | ⚠️ 易被判 deceptive pricing（3.1.1），需明示单价与总价 |
| Coin 充值包 | Consumable | 需走 IAP，不能跳外部支付（3.1.1） |
| Gift / Tipping 给主播 | Consumable | 若有直播打赏，按 `./ugc-social.md` + 3.2.1 约束 |

- [ ] 订阅价格与周期在购买按钮**同屏可见**（3.1.2(a)）
- [ ] 续订条款链接（标准 EULA 或自定义）指向 App 内或有效 URL
- [ ] 「看谁喜欢了你」此类 paywall 不得在 UI 上伪装成「系统消息」
- [ ] ⚠️ 「滑到第 X 个弹订阅墙」常见但合规，关键是**付费前明示内容**

---

## 8. 第三方登录（4.8）

- [ ] **任何使用 Google / Facebook / 微信登录的交友 App 必须同步提供 Sign in with Apple**
- [ ] SIWA 按钮**视觉权重不低于**其他登录方式（大小 / 位置 / 顺序对等）
- [ ] Facebook Login 在交友 App 中历史上被广泛使用，但现已不能单独作为登录方式
- [ ] 手机号登录**不算** OAuth，不触发 4.8，但仍需有隐私与注销流程（5.1.1(v)）

详见 `../references/sign-in-with-apple.md`。

---

## 9. 儿童分类冲突（Kids Category 禁用）

- [ ] 交友类 **永远不能**进入 Kids Category，即使声称"仅朋友交往""同龄兴趣社群"
- [ ] Primary Category 不可选 Kids，Secondary Category 不可选 Kids
- [ ] 即便 App 面向青少年（13–17），也归到 **Social Networking 17+** 或**直接限制 18+**
- [ ] 如果混合了"儿童学习 + 陌生人聊天"功能，Apple 会按**最高风险功能**归类 → 拒审

详见 `./kids.md`。

---

## 10. 提交前 Dating-Specific Checklist

### 10.1 功能与合规
- [ ] 年龄门在注册首屏 + 校验生日（2.1 / 2.2）
- [ ] 屏蔽 / 举报用户 / 举报内容 / 申诉入口齐备（1.2）
- [ ] Moderation 四件套（自动过滤 + 人工审核 + SLA + 记录）
- [ ] NCII / CSAM 零容忍策略写入社区准则 + Review Notes（1.2）
- [ ] 无 "random chat" / "stranger chat" / "anonymous chat" 描述（1.2 2024 更新）
- [ ] 位置返回距离而非精确坐标（5.1.1 / 1.4）
- [ ] 头像 / 上传图片走 NSFW + 人脸检测（1.2）
- [ ] 已实现真人验证或有明确 roadmap（5.1.1 + 1.4 物理伤害缓解）

### 10.2 商业化
- [ ] 订阅 UI 符合 3.1.2(a)，续订条款齐全
- [ ] Consumable boost / super-like 不构成 deceptive pricing（3.1.1）
- [ ] 所有数字商品走 IAP（3.1.1 / 3.1.3）

### 10.3 账号与登录
- [ ] Sign in with Apple 与其他 OAuth 同等展示（4.8）
- [ ] 账号删除入口在 App 内（5.1.1(v)）
- [ ] 删除账号后 Moderation 历史记录保留（平衡 GDPR 与反滥用）

### 10.4 元数据 / 截图
- [ ] App 描述不使用 `stranger` / `random` / `anonymous` / `hookup` / `NSFW`
- [ ] 截图不展示裸露 / 暗示性姿态 / 露骨文字（2.3.1）
- [ ] Review Notes 附：测试账号 + moderation 流程图 + SLA 承诺

详见 `../references/store-metadata-compliance.md` 与 `../checks/review-failure-map.md`。

---

## 11. 常见拒审案例（模式总结）

1. **"Stranger Chat" 关键词触发 1.2 拒审**
   App 描述里写 "chat with strangers nearby"，审核员按新随机聊天规则直接拒。
   修复：描述改为 "meet people nearby who share your interests"，补充注册 + 审核说明。

2. **Moderation Backlog 导致 SLA 拒审**
   Review Notes 写了"24h 人工审核"，但测试账号举报 3 小时后审核员发现内容仍在。
   修复：实现"举报立即隐藏 + 异步人工复核"，Review Notes 明确"举报 → 立即隐藏 → 24h 内裁决"。

3. **位置坐标在 API Response 中暴露**
   审核员抓包发现 `/api/nearby` 返回 `lat: 37.7749, lng: -122.4194`，直接 5.1.1 + 1.4 拒审。
   修复：服务端只返回 `distance_km`，坐标计算在服务端完成。

4. **未成年用户可进入成年聊天池**
   审核员注册 16 岁账号，仍可匹配到 30+ 用户。
   修复：年龄门硬阻断 + 后端强校验 + iOS 26.4 `DeclaredAgeRange` 读取（英澳地区）。

5. **订阅试用页欺骗性 UI（3.1.2 / 3.1.1）**
   "免费 3 天"字体巨大，"之后每周 ¥128"藏在角落。
   修复：将完整价格与周期放在 CTA 按钮同屏等视觉权重处。

---

## 参考

- 通用 UGC 四件套：`./ugc-social.md`
- 年龄分级与元数据：`../references/store-metadata-compliance.md`
- 拒审条款 → 修复映射：`../checks/review-failure-map.md`
- 订阅与 IAP 细则：`../references/storekit-iap.md`
- SIWA 实现细则：`../references/sign-in-with-apple.md`
