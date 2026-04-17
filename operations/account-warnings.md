# 账号警告与终止 (Account Warnings & Termination)

> **读这个文件的场景**：收到 Apple 账号级别的警告邮件，如 `Pending Termination Notice` 或 `Notice of Termination`（常见于 3.2(f) 欺诈/隐蔽功能），或账号突然无法转移 App。
> **前置区别**：如果是 App 级别的审核被拒（Guideline xx.x），请看 `../operations/review-ops.md`。
> **最后验证时间**：2026-04

---

## 一、警告级别与后果

| 状态 | 触发原因 | 后果 | 是否可申诉 | 申诉窗口 |
|------|---------|------|-----------|---------|
| **Pending Termination Notice** (终止前警告) | 违反开发者协议 3.2(f)（欺诈、马甲包、隐藏功能）；多次被拒未改；伪造资料；关联违规账号。 | App 立即下架；资金可能暂停结算；**禁止新建账号**；**禁止转移 App**。 | 是 | **14 个自然日** ⚠️ 经验规则（基于 2024-2025 开发者收到的实际邮件，Apple 未公开统一文档） |
| **Notice of Termination** (终止通知) | 申诉失败；超出申诉窗口未回复；严重违规。 | 账号注销；资金可能没收；开发者被列入黑名单。 | 是（请求恢复账号） | 无明确期限 |

> ⚠️ 经验规则：申诉窗口从**邮件发送之日**算起，且是**自然日（calendar days）**，绝不是工作日。不要等到最后一天。过去部分旧版邮件提及 30 天，但 2024-2026 年的信件确认通常为 14 天。

---

## 二、不要做的致命错误

> ⚠️ 法律风险提示：账号封禁通常涉及《Apple Developer Program License Agreement》（ADP）违约，处理不当将面临永久封禁。

1. **绝对不要用其他账号上马甲包**：在 Pending 期间创建新账号或用关联账号提包，违反 Guideline 4.3（Spam）和 5.6（Developer Code of Conduct）。Apple 会直接终止所有关联账号。
2. **不要狡辩或说谎**：Apple 手里通常有抓包记录或后台录屏。如果隐藏了热更新、私有 API 或第三方支付，直接承认并整改。
3. **不要只说 "I'm sorry"**：Apple 要求看到具体的**整改措施**，而非态度。

---

## 三、申诉流程

**入口**：[Contact App Review Team](https://developer.apple.com/contact/app-store/)

**选项**：
1. 若为 Pending Notice：下拉菜单选 **"I would like to appeal an app rejection or app removal"**。
2. 若为 Terminated：下拉菜单选 **"Re-instate a Terminated Developer Program Membership"**。

---

## 四、三段式申诉声明模板

社区共识（⚠️ 经验规则），高质量的申诉信必须包含三个部分：

### 1. 详细解释问题 (Detailed Explanation)
客观描述发生的事情，不要带情绪。如果是误解，用事实反驳。如果是自己的过错，承认错误原因（如外包代码、第三方 SDK 引入、审核不严）。

### 2. 具体整改措施 (Specific Remediation)
不仅是 "我们已经改了"，而是具体的行动清单：移除了哪个类库、更改了哪个设置、制定了怎样的新审核流程。

### 3. 澄清信息 (Clarifying Information)
提供证据证明你是一个合法的正规开发者。

### 模板示例（因 3.2(f) 隐藏功能被 Pending）

```markdown
Dear App Review Board,

I am writing to appeal the Pending Termination Notice regarding our developer account [Account ID] and app [App Name, App ID].

**1. Explanation of the Issue:**
We received a notice regarding a violation of Section 3.2(f) of the Developer Program License Agreement. After a thorough investigation, we discovered that a third-party SDK [SDK Name] used for [purpose] included remote-configuration code that altered the app's behavior without our explicit knowledge. We take full responsibility for this oversight.

**2. Remediation Measures:**
We have immediately taken the following actions:
- Removed the [SDK Name] completely from our codebase (see attached GitHub commit snippet).
- Implemented a strict internal code-review policy prohibiting the integration of unverified third-party libraries.
- Audited our entire app for any remaining remote-configuration capabilities and found none.
- Re-submitted build [Build Number] which is fully compliant with the App Store Review Guidelines.

**3. Clarifying Information:**
We are a legitimate business established in [Year], serving [Number] users. We have always strived to provide a safe and transparent experience on the App Store. Attached are our company registration documents and links to our official website to verify our business standing.

We sincerely apologize for this incident and kindly request that you review our updated build and restore our account standing.

Thank you for your time,
[Your Name / Title]
[Company Name]
```

### 模板示例（因被误判为欺诈应用，要求澄清）

```markdown
Dear App Review Board,

I am writing to appeal the Pending Termination Notice for [Account ID]. 

We believe there has been a misunderstanding regarding our app [App Name, App ID]. The notice cited Section 3.2(f) (Fraud/Deceptive behavior).

**Clarification:**
Our app provides [service description]. Recently, we experienced an automated surge in fake account registrations from a botnet attack, which may have looked like manipulative behavior. 

**Remediation:**
We have:
1. Implemented [Bot Protection Service] on our backend to block fraudulent traffic.
2. Deleted all fake accounts from our database.
3. Updated the app to require SMS verification for new signups.

We are a legitimate service provider. Attached are our server logs demonstrating the bot attack and our subsequent mitigation, as well as our business registration. We have not engaged in any deceptive practices towards Apple or our users.

We respectfully request a review of this evidence and the reinstatement of our account in good standing.

Thank you.
```

---

## 五、举证清单

| 证据类型 | 适用场景 | 说明 |
|------|------|------|
| **代码/变更记录** | 隐藏功能、违规 SDK | Git diff、移除记录，证明违规代码已彻底清除。 |
| **合法经营证明** | 被判欺诈、马甲包、关联账号 | 营业执照、软著、公司网站、实体办公地照片。 |
| **服务器/安全日志** | 被判刷量、恶意行为 | 证明是遭到攻击而非自己作恶。 |
| **沟通记录** | 外包欺诈 | 证明违规是外包/合作方所为（Apple 不一定买账，但有助于说明意图）。 |

---

## 六、时效与预期

- **提交后**：App Review Board 的审核时效非常不稳定。2025/2026 社区反馈显示，短则 24 小时，长则 **30 天以上** 无回复（⚠️ 经验规则）。
- **如果没回复**：在 14 天窗口期内，每隔 5-7 天礼貌地追加一次信息（"Following up on our appeal..."），但不要一天发一封。
- **如果被拒**：收到 Notice of Termination。后续只能通过 "Re-instate a Terminated Developer Program Membership" 碰运气，或在部分极端情况下（如明显误判）诉诸法律途径。

---
> 🔗 相关引用：[Apple 账号终止政策讨论区 (Apple Developer Forums)](https://developer.apple.com/forums/) | [Apple 开发者协议 (ADP)](https://developer.apple.com/support/terms/apple-developer-program-license-agreement/)
