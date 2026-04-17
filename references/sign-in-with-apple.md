# Sign in with Apple 完整参考

> 条款 4.8 要求：任何使用第三方或社交账号登录的 App 必须同时提供 Sign in with Apple。
> 本文件覆盖触发条件、豁免情形、按钮设计规范、email relay、token revocation 及代码实现。

---

## 一、何时必须提供 Sign in with Apple

**触发条件（4.8 明文）**：App 使用了任何第三方或社交账号登录（包括但不限于）：

- Google Sign-In
- Facebook Login
- Twitter/X OAuth
- WeChat Login（微信登录）
- 任何 OAuth 2.0 / OpenID Connect 第三方身份提供商

只要存在上述任意一种，就必须**同时提供 Sign in with Apple 作为等同选项**。

### 1.1 「等同选项」的含义

- Sign in with Apple 按钮必须与其他登录选项**视觉上同等突出**
- 不能把 Sign in with Apple 藏在二级页面而其他 OAuth 放首页
- 推荐做法：所有第三方登录按钮与 Sign in with Apple 按钮在同一屏幕、同等大小

---

## 二、豁免情形（不需要提供 Sign in with Apple）

| 豁免类型 | 说明 | 条款依据 |
|---------|------|---------|
| 仅使用自有账号系统 | App 只有邮箱+密码注册，无任何第三方 OAuth | 4.8 不适用 |
| 企业内部 App（B2B） | 通过 Apple Business Manager 分发的内部 App | 4.8 豁免 |
| 教育机构 App | 使用学校 SSO（如 SAML/Shibboleth）的教育类 App | 4.8 豁免 |
| 政府机构 App | 使用政府身份认证系统（如电子身份证）的 App | 4.8 豁免 |
| 公司内部 SSO | 仅供员工使用，通过公司 IdP（如 Okta、Azure AD）登录 | 4.8 豁免 |
| 金融/合规要求 | 法律要求使用特定身份验证方式（如银行 eKYC） | 4.8 豁免 |
| 第三方账号仅用于连接服务 | 第三方登录不用于设置或认证用户的主账号（如连接游戏平台账号用于跨平台游戏） | 4.8 不适用 |

**注意**：
- 使用 WeChat Login 但声称「只面向中国用户」**不构成豁免** — 只要 App 在 App Store 上架且包含第三方登录，就必须提供 SIWA
- ⚠️ 经验规则：如果 App 同时有邮箱注册和第三方 OAuth，仅因「邮箱注册是主要方式」不能豁免

---

## 三、Sign in with Apple 按钮设计规范

### 3.1 官方按钮样式

Apple 提供了严格的 [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple) 按钮规范：

| 属性 | 要求 |
|------|------|
| 按钮类型 | `ASAuthorizationAppleIDButton`（iOS）或官方 JS/REST 按钮 |
| 最小尺寸 | 140pt × 44pt（高度需满足 44pt 可触摸目标，宽度最小 140pt） |
| 圆角 | 支持 small/medium/large，需与其他登录按钮风格一致 |
| 颜色 | 三种官方样式：Black、White、White with Outline |
| 文案 | 「Sign in with Apple」「Continue with Apple」「Sign up with Apple」 |
| 本地化 | 使用系统按钮时自动本地化，自定义按钮需手动匹配 |
| Apple logo | 必须使用官方 SF Symbol 或资源包中的 Apple logo，**不可使用自制 logo** |

### 3.2 禁止行为

- ❌ 自定义绘制 Apple logo
- ❌ 更改按钮文案（如「用苹果登录」非官方本地化版本）
- ❌ 按钮尺寸小于其他第三方登录按钮
- ❌ 使用过时的按钮资源

### 3.3 iOS 原生实现

```swift
import AuthenticationServices

let appleButton = ASAuthorizationAppleIDButton(
    authorizationButtonType: .signIn,
    authorizationButtonStyle: .black
)
appleButton.addTarget(self, action: #selector(handleAppleSignIn), for: .touchUpInside)

@objc func handleAppleSignIn() {
    let provider = ASAuthorizationAppleIDProvider()
    let request = provider.createRequest()
    request.requestedScopes = [.fullName, .email]
    
    let controller = ASAuthorizationController(authorizationRequests: [request])
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests()
}
```

### 3.4 Web 端 / React Native / Flutter

- **Web**：使用 Apple JS SDK 或 REST API（`appleid.apple.com/auth/authorize`）
- **React Native**：`@invertase/react-native-apple-authentication` 或 `expo-apple-authentication`
- **Flutter**：`sign_in_with_apple` package
- **Capacitor**：`@nicklassandell/cap-apple-sign-in` 或 `@nicolo-ribaudo/capacitor-apple-sign-in`

---

## 四、Email Relay（隐藏邮箱）

用户可以选择「隐藏我的邮箱」，此时 Apple 返回一个代理邮箱地址：

```
格式：<random>@privaterelay.appleid.com
```

### 4.1 App 必须正确处理代理邮箱

- **必须**：在 Apple Developer Portal → Certificates, Identifiers & Profiles → Services → Sign in with Apple → Edit → 配置 Email Sources（域名和邮箱）
- **必须**：向代理邮箱发送的邮件必须通过已注册的域名/邮箱发出，否则邮件会被 Apple Relay 丢弃
- **禁止**：要求用户提供「真实邮箱」来替代 Apple 代理邮箱

### 4.2 配置 Email Sources

1. 登录 [Apple Developer](https://developer.apple.com) → Account → Certificates, Identifiers & Profiles
2. 点击 Services → Sign in with Apple for Email Communication
3. 添加发件域名（如 `notifications.yourapp.com`）
4. 配置 SPF/DKIM DNS 记录
5. 验证域名

### 4.3 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 用户收不到邮件 | 未注册 Email Sources 域名 | 在 Developer Portal 配置发件域名 |
| 邮件被退回 | SPF/DKIM 未配置 | 添加 DNS 记录 |
| 用户切换设备后无法登录 | 未存储 user identifier | 始终以 `user` 字段作为唯一标识 |

---

## 五、Token Revocation Endpoint（账号删除必需）

自 2022 年起，Apple 要求 App 在用户删除账号时必须调用 Apple 的 revocation endpoint 撤销 token。

### 5.1 为什么必须实现

- **条款 5.1.1(v)**：App 必须提供账号删除功能
- 如果用户通过 Sign in with Apple 注册，删除账号时必须同时 revoke Apple token
- **不做 revocation 会导致拒审**

### 5.2 Revocation 流程

```
POST https://appleid.apple.com/auth/revoke
Content-Type: application/x-www-form-urlencoded

client_id=<your_service_id>&
client_secret=<your_jwt>&
token=<refresh_token>&
token_type_hint=refresh_token
```

### 5.3 生成 client_secret（JWT）

```python
import jwt
import time

# Apple Developer Portal 获取的信息
team_id = "YOUR_TEAM_ID"
client_id = "com.example.app"          # Service ID 或 Bundle ID
key_id = "YOUR_KEY_ID"                 # Sign in with Apple 私钥 ID
private_key = open("AuthKey.p8").read() # 下载的 .p8 私钥

now = int(time.time())
payload = {
    "iss": team_id,
    "iat": now,
    "exp": now + 86400 * 180,  # 最长 6 个月
    "aud": "https://appleid.apple.com",
    "sub": client_id
}

client_secret = jwt.encode(payload, private_key, algorithm="ES256", headers={"kid": key_id})
```

### 5.4 完整 Revocation 实现（Node.js）

```javascript
const axios = require('axios');
const jwt = require('jsonwebtoken');
const fs = require('fs');

function generateClientSecret() {
  const privateKey = fs.readFileSync('AuthKey.p8');
  const now = Math.floor(Date.now() / 1000);
  
  return jwt.sign({
    iss: process.env.APPLE_TEAM_ID,
    iat: now,
    exp: now + 86400 * 180,
    aud: 'https://appleid.apple.com',
    sub: process.env.APPLE_CLIENT_ID
  }, privateKey, {
    algorithm: 'ES256',
    header: { kid: process.env.APPLE_KEY_ID }
  });
}

async function revokeAppleToken(refreshToken) {
  const clientSecret = generateClientSecret();
  
  const response = await axios.post(
    'https://appleid.apple.com/auth/revoke',
    new URLSearchParams({
      client_id: process.env.APPLE_CLIENT_ID,
      client_secret: clientSecret,
      token: refreshToken,
      token_type_hint: 'refresh_token'
    }).toString(),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
  
  // 成功返回 HTTP 200，无 body
  return response.status === 200;
}
```

---

## 六、Credential State 检查

App 启动时应检查 Apple ID credential 状态，处理用户撤销授权的场景：

```swift
func checkCredentialState() {
    let provider = ASAuthorizationAppleIDProvider()
    provider.getCredentialState(forUserID: savedUserIdentifier) { state, error in
        switch state {
        case .authorized:
            break // 正常
        case .revoked:
            // 用户已撤销授权，需登出并清理本地数据
            self.signOut()
        case .notFound:
            // credential 未找到，引导重新登录
            self.showSignIn()
        case .transferred:
            // App 转让场景，需要迁移用户
            self.migrateUser()
        @unknown default:
            break
        }
    }
}
```

---

## 七、审核 Checklist

### 提交前必检

- [ ] **4.8**：有第三方 OAuth → 已提供 Sign in with Apple 作为等同选项
- [ ] **4.8**：Sign in with Apple 按钮使用官方 `ASAuthorizationAppleIDButton` 或官方资源
- [ ] **4.8**：按钮尺寸 ≥ 其他登录按钮，且在同一屏幕
- [ ] **5.1.1(v)**：账号删除流程中已调用 Apple revocation endpoint
- [ ] Email Relay：已在 Developer Portal 配置 Email Sources 域名
- [ ] Email Relay：SPF/DKIM DNS 记录已配置
- [ ] Credential State：App 启动时检查 `.revoked` 状态
- [ ] 正确存储 `user` identifier 作为唯一标识（不依赖 email）
- [ ] Web 端 / 多端：redirect URI 已在 Services 中正确配置

### 常见拒审场景

| 场景 | 条款 | 修复 |
|------|------|------|
| 有 Google/Facebook 登录但无 SIWA | 4.8 | 添加 Sign in with Apple |
| SIWA 按钮放在二级页面 | 4.8 | 移到与其他 OAuth 同一屏幕 |
| 账号删除不 revoke Apple token | 5.1.1(v) | 实现 revocation endpoint 调用 |
| 自定义 Apple logo 不规范 | 4.8 | 使用 `ASAuthorizationAppleIDButton` |
| 代理邮箱用户无法收到验证邮件 | 功能缺陷 | 配置 Email Sources + SPF/DKIM |

---

## 八、参考链接

- [App Store Review Guidelines 4.8](https://developer.apple.com/cn/app-store/review/guidelines/#sign-in-with-apple)
- [Sign in with Apple 概述](https://developer.apple.com/sign-in-with-apple/)
- [HIG: Sign in with Apple 按钮](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)
- [Revoke Tokens](https://developer.apple.com/documentation/sign_in_with_apple/revoke_tokens)
- [Offering Account Deletion](https://developer.apple.com/support/offering-account-deletion-in-your-app/)
- 相关文件：`../checks/code-scan-patterns.md`（代码扫描 SIWA 检查）、`../by-app-type/all-apps.md`（通用 checklist）
