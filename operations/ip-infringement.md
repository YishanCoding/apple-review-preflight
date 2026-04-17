# 知识产权侵权 — 维权与应诉 (IP Infringement)

> **读这个文件的场景**：你的品牌/代码/UI/关键词被抄袭（维权），或你收到了 Apple 转发的侵权投诉邮件（应诉）。
> **最后验证时间**：2026-04

---

## Part A：维权 — 你是原创方

### 一、投诉入口（2025/2026 当前）

| 投诉类型 | 当前入口 URL | 适用场景 |
|---------|-------------|---------|
| **版权 (DMCA)** | [apple.com/legal/contact/copyright-infringement.html](https://www.apple.com/legal/contact/copyright-infringement.html) | 代码抄袭、UI 素材盗用、内容版权侵权。 |
| **商标 / 内容争议** | [apple.com/legal/intellectual-property/dispute-forms/app-store/](https://www.apple.com/legal/intellectual-property/dispute-forms/app-store/) | 商标侵权、App 描述/截图侵权、关键词滥用品牌名。 |
| **App 名称争议** | [apple.com/legal/internet-services/itunes/appnamenotices/](https://www.apple.com/legal/internet-services/itunes/appnamenotices/) | 竞品使用你的品牌名作为 App 名称。 |

> ⚠️ 旧 URL `apple.com/legal/internet-services/itunes/appstorenotices/` 可能仍然可达，但建议使用上述分类表单以确保准确路由。

### 二、举证清单

| 证据类型 | 必需/推荐 | 说明 |
|---------|---------|------|
| **商标注册证** | 必需（商标案） | 中国商标注册证需英文翻译件。 |
| **软件著作权证书** | 推荐 | 中国软著证书 + 英文翻译。 |
| **侵权对比截图** | 必需 | 你的 App ↔ 侵权 App 的并排截图对比。 |
| **App Store 搜索截图** | 推荐（关键词案） | 搜索你的品牌词，侵权 App 出现在结果中的截图。 |
| **授权委托书** | 必需（代理人投诉） | 品牌/商标所有人签署的代理投诉授权书。 |
| **公司营业执照** | 推荐 | 证明合法经营身份。 |
| **代码相似性分析** | 推荐（代码案） | 使用代码查重工具的报告。 |
| **宣誓声明** | 必需（DMCA） | 表单要求签署 under penalty of perjury 的声明。 |

### 三、维权模板 — 商标/品牌词侵权（英文）

```
Dear Apple Legal Team,

We are writing to report a trademark infringement on the App Store.

**Our Trademark:**
- Trademark Name: [Your Brand]
- Registration Number: [Number]
- Jurisdiction: [Country]
- Owner: [Company Name]

**Infringing App:**
- App Name: [Infringing App Name]
- Apple ID: [ID]
- Developer: [Developer Name]
- Link: [App Store URL]

**Description of Infringement:**
The above-listed app uses our registered trademark "[Brand]" in its 
[app name / subtitle / keywords / metadata], causing consumer confusion 
and diverting traffic from our legitimate app [Your App Name] (Apple ID: [ID]).

Evidence of confusion includes [describe: search results showing competitor 
ranking for your brand term, user complaints about downloading the wrong app, etc.].

**Attached Documents:**
1. Trademark Registration Certificate (with English translation)
2. Side-by-side comparison screenshots
3. App Store search results showing the infringing app

We request that Apple review this matter and take appropriate action to protect 
our intellectual property rights.

Sincerely,
[Name / Title]
[Company]
[Contact Email]
```

### 四、维权模板 — 商标/品牌词侵权（中文，提交至 Apple 英文表单时需翻译）

```
致 Apple 法律团队：

我方是 [公司名称]，为 [品牌名] 的注册商标持有人（注册号：[编号]，
注册国：中国）。

**侵权应用：**
- 应用名称：[侵权 App 名称]
- Apple ID：[ID]
- 开发者：[开发者名称]
- 链接：[App Store URL]

**侵权描述：**
上述应用在其 [名称/副标题/关键词/描述] 中使用了我方注册商标 "[品牌名]"，
导致用户混淆，劫持我方合法应用 [你的 App 名称]（Apple ID: [ID]）的流量。

**附件：**
1. 商标注册证书（含英文翻译）
2. 侵权对比截图
3. App Store 搜索结果截图

恳请 Apple 审查此事并采取适当措施保护我方知识产权。

[姓名 / 职务]
[公司名称]
```

### 五、处理时间与预期

- 提交后会收到确认邮件和**投诉编号**（Complaint/Case Number）。
- Apple 没有公开 SLA。⚠️ 经验规则：简单的 App 名称争议可能数周内解决；复杂的商标/版权纠纷可能持续数月。
- 如果 Apple 驳回投诉：没有内部上诉机制。你可以补充证据重新提交，或通过联邦法院起诉（Apple 已退出 Copyright Claims Board，DMCA 争议只能走联邦法院）。

---

## Part B：应诉 — 你被投诉

### 一、收到投诉后的处理

当 Apple 收到针对你的 App 的投诉时，你会收到 Apple 转发的邮件，通常包含：
- 投诉方的姓名和邮箱
- 投诉内容摘要
- Apple 的要求：尽快解决，否则可能下架

**响应时间**：
- Apple 没有公布固定期限。⚠️ 经验规则：常见说法是 10 个工作日，但这不是 Apple 官方明文。
- 邮件中通常会说 "if the matter is not resolved shortly, Apple may be forced to pull the application"。

### 二、应对策略

**如果你确实侵权了**：
- 尽快修改 App 名称/元数据/侵权内容
- 回复 Apple 说明已整改

**如果你没有侵权**：

#### 反驳模板（英文）

```
Dear Apple Legal Team,

Re: Complaint [Case Number]

We have reviewed the complaint filed against our app [App Name] (Apple ID: [ID]).

We respectfully disagree with the allegation of [copyright/trademark] infringement 
for the following reasons:

1. [Reason 1: e.g., "Our app name '[Name]' is a generic/descriptive term that 
   cannot be exclusively claimed by any party."]
2. [Reason 2: e.g., "Our trademark registration [Number] predates the 
   complainant's registration."]
3. [Reason 3: e.g., "The app's functionality and design are entirely original 
   and independently developed."]

**Supporting Evidence:**
- [List of attached documents: trademark certificate, development history, 
  prior art, etc.]

We request that Apple dismiss this complaint and allow our app to remain 
available on the App Store.

Sincerely,
[Name / Company]
```

### 三、DMCA 反通知 (Counter-Notification)

如果你的 App 因 DMCA 投诉被下架，你可以提交 DMCA 反通知（Counter-Notification）给 Apple 的 Copyright Agent：

反通知需包含：
1. 被移除内容的标识
2. 宣誓声明（under penalty of perjury）：声明你有合法权利使用该内容
3. 同意管辖权（consent to jurisdiction）

提交后，根据 DMCA 法规，Apple **必须在 10-14 个工作日内恢复内容**，除非投诉方在此期间向法院提起诉讼。

> ⚠️ 法律风险提示：DMCA 反通知是法律文件，涉及 "under penalty of perjury" 宣誓。如有疑问，建议咨询律师。

---

## Part C：关键词/品牌名的特殊说明

| 争议类型 | 可投诉？ | 渠道 |
|---------|---------|------|
| **竞品用你的品牌名作 App 名称** | 是 | App Name Dispute 表单 |
| **竞品在元数据/关键词中塞你的品牌名** | 是 | Content Dispute 表单（引用 Guideline 2.3.7 禁止误导性元数据） |
| **竞品在 Search Ads 中竞价你的品牌词** | 否 | Apple 明确声明**不受理 Search Ads 竞价排名相关的商标投诉** |

---

## 来源

| 来源 | URL | 验证时间 |
|------|-----|---------|
| IP Dispute Forms | https://www.apple.com/legal/intellectual-property/dispute-forms/app-store/ | 2026-04 |
| Copyright Infringement | https://www.apple.com/legal/contact/copyright-infringement.html | 2026-04 |
| App Name Dispute | https://www.apple.com/legal/internet-services/itunes/appnamenotices/ | 2026-04 |
| Buzko Krasnov — App Store Disputes | https://www.buzko.legal/content-eng/guide-to-app-store-disputes-for-developers | 2026-04 |
| Guidelines §2.3.7 | https://developer.apple.com/cn/app-store/review/guidelines/#metadata | 2026-04 |
