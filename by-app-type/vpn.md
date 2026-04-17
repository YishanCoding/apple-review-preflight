# VPN App 专项风险

> 本文件仅记录超出通用审核规则的专项要求。适用于提供 VPN、网络代理、隐私保护隧道等功能的 App。

---

## 1. 必须使用 NEVPNManager API

**规则来源：App Store Review Guidelines 5.4 / 技术要求**

- **强制要求**：所有 VPN 功能必须通过 Apple 官方的 **Network Extension 框架**（`NEVPNManager` / `NETunnelProviderManager`）实现。
- **禁止方式**：
  - 使用 tun/tap 虚拟网卡的底层实现（iOS/iPadOS 不支持）
  - 通过 WebSocket 或 SSH 隧道实现的"伪 VPN"，且未使用 Network Extension
  - 需要越狱才能工作的实现方式
- **技术路径**：
  - **IKEv2 VPN**：使用 `NEVPNManager`，适合标准 VPN 协议
  - **自定义协议（WireGuard、Shadowsocks 等）**：使用 `NETunnelProviderManager` + Packet Tunnel Provider Extension
  - **内容过滤**：使用 `NEFilterDataProvider`（仅限 MDM/企业场景）
- **Entitlement 要求**：`com.apple.developer.networking.networkextension`，且必须在 Apple Developer 后台申请开通（不是默认可用）。
- **申请流程**：在 developer.apple.com 申请 Network Extension 能力，Apple 会审核申请理由，通常需要 1-3 个工作日。

---

## 2. 仅企业账号开发者可发布

**规则来源：App Store Review Guidelines 5.4**

- VPN App **只能由企业账号（Organization account）开发者发布**，个人账号（Individual）不允许。
- 与加密货币钱包要求相同，Apple 认为 VPN 属于需要法律主体承担责任的高风险类别。
- **审核初期检查**：账号类型不符会在资格验证阶段被拒，无需等待内容审核。

**实操检查**：
```
App Store Connect → 开发者账号信息 → 确认显示为"公司"（Company）而非"个人"（Individual）
```

---

## 3. 禁止出售或披露用户数据给第三方

**规则来源：App Store Review Guidelines 5.4 / 5.1.1**

VPN App 对数据处理有极为严格的要求，因为 VPN 流量包含用户的所有网络活动：

- **完全禁止**：
  - 将用户网络流量数据出售给第三方（广告商、数据经纪商等）
  - 利用用户流量数据建立用户画像用于广告目的
  - 将用户的 DNS 查询记录或访问历史共享给任何第三方（执法机构除外，且需符合法律要求）
  - 在用户不知情的情况下在流量中注入广告或追踪代码
- **必须承诺**：
  - 不记录用户活动（No-log 政策），或至少在隐私政策中明确说明记录范围和保留期限
  - 数据请求响应政策（如何处理政府数据请求）
- **审核验证**：Apple 审核员会仔细检查隐私政策，隐私政策与实际行为不一致是拒审重点。

---

## 4. 需要许可证的地区在 Review Notes 中提供

**规则来源：App Store Review Guidelines 5.4 / 各国法规**

以下地区对 VPN 服务有特殊许可证要求，提交时必须在 Review Notes 中说明：

| 地区 | 要求 | 备注 |
|------|------|------|
| 中国大陆 | 工信部 VPN 服务许可证 | 中国区上架几乎不可能，2017年起大规模下架 |
| 俄罗斯 | Roskomnadzor 注册 | 需接受流量监控，与 VPN 本质冲突 |
| 伊朗 | 国家批准的 VPN | 实际上无法合规运营 |
| 阿联酋 | TRA 批准 | 需为持牌运营商的增值服务 |
| 土库曼斯坦 | 事实上禁止 | |

**Review Notes 格式**：
```
This VPN app is geo-restricted from countries where VPN services require 
government licensing (China, Russia, Iran, UAE, etc.) using App Store's 
territory availability settings.
Applicable license information: [如有许可证，提供许可证号和颁发机构]
```

**实操**：在 App Store Connect 的"价格与销售范围"中，手动取消勾选无法合规运营的地区。

---

## 5. VPN App 隐私政策特殊要求

VPN App 的隐私政策需包含超出普通 App 的额外条款：

**必须明确说明的内容**：

1. **流量日志策略**：
   - 是否记录用户访问的网站/IP
   - 是否记录连接时间、时长
   - 是否记录用户真实 IP（会话日志）
   - 记录保留期限

2. **数据使用目的**：
   - 记录的数据（如有）具体用于什么目的（运营、故障排查等）
   - 明确声明不用于广告

3. **数据共享**：
   - 是否与第三方服务商共享（如云服务商）
   - 如何响应执法机构数据请求（Warrant Canary 是加分项）

4. **服务器位置**：
   - VPN 服务器所在国家/地区
   - 数据实际存储和处理地点

5. **注销和数据删除**：
   - 用户注销后数据如何处理
   - 用户如何申请删除全部数据

**隐私政策语言要求**：必须提供与 App 上架地区对应语言的版本（至少需要英文版）。

---

## 常见拒审场景

1. **个人账号提交 VPN App**：直接被资格拒审。
2. **未申请 Network Extension Entitlement**：技术上无法实现，打包时会失败。
3. **隐私政策未说明流量日志政策**：审核员明确要求补充。
4. **App 在中国/俄罗斯等地区上架但无许可证**：Apple 会要求下架或提供许可证。
5. **VPN App 内置广告**：即使广告与 VPN 流量无关，也会引发审核员对数据使用的怀疑。
6. **免费 VPN App 商业模式不清晰**：审核员可能要求说明盈利模式（暗示可能变现用户数据）。
7. **App 声称"军事级加密"等无法验证的安全声明**：按 4.0 误导性内容处理。
