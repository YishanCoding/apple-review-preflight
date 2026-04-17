# Review Failure Map — 高频拒审原因 × 条款映射

> 整合 Guideline 2.x 性能条款 + 实战拒审数据

---

## CRITICAL — 立即拒审，无商量余地

| 原因 | 条款 | 判断信号 |
|------|------|---------|
| 使用私有/未公开 API | 2.5.1 | 代码调用 `_` 开头方法，或 Apple 未公开的框架 |
| 动态下载和执行代码 | 2.5.2 | `eval()`、JSPatch、动态 patch；OTA 更新不能新增功能 |
| 恶意软件 / 病毒传播 | 2.5.3 | 影响 OS 或硬件正常运行的代码 |
| App 崩溃或严重 bug | 2.1(a) | 审核员实际测试时崩溃 |
| 在 App 内为数字内容提供外部支付（非授权地区） | 3.1.1 | Stripe checkout、外部订阅链接用于解锁数字功能 |
| 隐私政策完全缺失 | 5.1.1(i) | ASC 元数据未填隐私政策 URL |
| 有账号创建但无账号删除 | 5.1.1(v) | 注册功能存在，但设置里无删除入口 |
| PrivacyInfo.xcprivacy 缺失（使用了 Required Reason API） | 5.1.1 | 使用 UserDefaults/文件时间/磁盘空间 API 但无清单 |

---

## HIGH — 大概率拒审

| 原因 | 条款 | 判断信号 |
|------|------|---------|
| 演示账号不可用/后端下线 | 2.1(a) | 审核员无法登录或访问功能 |
| 强制注册才能浏览公开内容 | 5.1.1(v) | 首屏拦截所有用户，无 Guest/Skip |
| 第三方 OAuth 登录未配 Sign in with Apple | 4.8 | Google/微信/Facebook 登录但无 Apple 登录选项 |
| ATT 弹窗时机错误（先 tracking 后弹窗） | 5.1.2(i) | Firebase/Adjust 初始化在 ATT 授权之前 |
| IAP 配置不完整或沙盒测试失败 | 2.1(b)/3.1.1 | 部分 IAP 在 ASC 中未激活；购买流程中断 |
| 元数据与实际功能不符 | 2.3.1 | 截图含未上线功能；描述含占位符文字 |
| 隐私政策链接 404 或需登录访问 | 5.1.1(i) | 审核期间链接失效 |
| UGC App 缺少举报/屏蔽机制 | 1.2 | 有用户生成内容但无举报/屏蔽功能 |
| 后台模式声明与实际用途不符 | 2.5.4 | audio 仅用于 keep-alive；location 无实际定位功能 |
| 使用废弃 API | 2.5.1 | Xcode 有 deprecated API 警告 |
| Kids Category App 含第三方追踪 | 1.3 | 儿童 App 集成 Firebase Analytics、Facebook SDK |

---

## MEDIUM — 较常见，但有时可通过申诉

| 原因 | 条款 | 判断信号 |
|------|------|---------|
| App Name 含促销词/竞品名 | 2.3.7 | 包含「Free」「Best」「#1」「Android」 |
| 截图含未上线功能或错误设备边框 | 2.3.3/2.3.4 | 截图来自设计稿；6.1" 截图套 6.7" 边框 |
| 描述含竞品名称（如「比 XX 好用」） | 2.3.7 | Description 提及竞品 |
| 正文字体在真机上不可读 | 4（Design） | 字号过小或对比度不足，模拟器正常但真机难读 |
| 纯 WebView 壳，无原生价值 | 4.2 | App 全部功能是 WKWebView 渲染网页 |
| 评分提示使用自定义 UI | 5.6.1 | 非 `SKStoreReviewRequest` 的自定义评分弹窗 |
| 权限描述过于模糊 | 5.1.1 | `NSCameraUsageDescription` = "This app needs camera" |
| 元数据含 Apple 商标/Logo | 5.2.4/5.2.5 | 截图/图标含 Apple Logo 或 iPhone 图片 |
| 推送通知用于营销（未经明确选择） | 4.5.4 | 用户未 opt-in 就收到促销推送 |

---

## 2.x 性能条款速查

### 2.1 App 完整性
- 必须提供最终版本（无占位符、无空白页面、无 lorem ipsum）
- IAP 必须在审核期间可访问（沙盒测试）
- Review Notes 必须填写演示账号和功能说明

### 2.2 Beta 版测试
- 禁止将 Beta/Demo/试用版提交到 App Store（用 TestFlight）
- 大幅更新先提交 TestFlight Beta App Review

### 2.3 元数据准确性
| 字段 | 限制 | 常见违规 |
|------|------|---------|
| App Name | 30 字符 | 促销词、含「app」、竞品名 |
| Subtitle | 30 字符 | 同 Name 规则 |
| Description | 4000 字符 | 未上线功能、虚假价格 |
| Keywords | 100 字符 | 竞品品牌词、无关词 |
| 截图 | — | 设计稿/边框错误/未上线功能 |
| 年龄分级 | — | 未诚实填写 |

### 2.4 硬件兼容性
- iPhone App 尽量在 iPad 上运行
- 禁止不必要的资源占用（过度耗电、大量 SSD 写入）
- 禁止无关后台挖矿

### 2.5 软件要求
| 条款 | 关键要求 |
|------|---------|
| 2.5.1 | 仅公共 API；在当前 OS 运行 |
| 2.5.2 | 禁止下载执行修改功能的代码 |
| 2.5.4 | 后台服务仅用于原定用途 |
| 2.5.5 | 必须在纯 IPv6 网络下运行 |
| 2.5.6 | 必须使用 WebKit（可申请替代浏览器引擎） |
| 2.5.13 | 面容 ID 用 LocalAuthentication，不用 ARKit |
| 2.5.18 | 广告仅在主二进制，不在扩展/Widget/通知 |
