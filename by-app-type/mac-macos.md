# macOS / Mac App Store 专项风险

> 本文件仅记录超出通用审核规则的专项要求。适用于通过 Mac App Store 分发的 macOS App（含 Mac Catalyst App）。直接分发（Developer ID 签名）不受本文件约束。

---

## 1. 沙盒化（App Sandbox）要求

**规则来源：Mac App Store Review Guidelines / App Sandbox 技术文档**

- Mac App Store 中的所有 App **必须启用 App Sandbox**（Hardened Runtime + Entitlements）。
- **禁止使用**的 Entitlement：
  - `com.apple.security.temporary-exception.*`（临时例外）：仅在极少数经 Apple 审批的情况下允许，必须在 Review Notes 中详细说明必要性。
  - `com.apple.security.cs.disable-library-validation`：禁止，除非有充分理由并获得批准。
- **文件系统访问**：必须通过 NSOpenPanel / NSSavePanel 获取用户授权，不能假定拥有任意路径访问权。
- **网络访问**：需在 Entitlements 中明确声明 `com.apple.security.network.client` 或 `com.apple.security.network.server`。
- **进程间通信**：XPC Services 是推荐方式，裸 socket IPC 需额外审查。

**常见沙盒违规**：
- 尝试读写 `~/Library/Application Support/其他App/` 目录（需通过用户授权）
- 使用 `posix_spawn` 或 `NSTask` 启动任意进程（需声明 `allow-unsigned-executable-memory` 等）

---

## 2. 禁止自动启动（登录时自动运行）

**规则来源：Mac App Store Review Guidelines 2.4**

- **禁止**：App 在未经用户明确同意的情况下将自身注册为登录项（Login Item）。
- **允许的方式**：使用 `SMLoginItemSetEnabled` API，且必须：
  1. 在 App 内提供明显的 UI 开关（如"开机启动"复选框）
  2. 默认状态为**关闭**（Off）
  3. 用户可随时通过 App 内开关或系统偏好设置取消
- **禁止方式**：在 LaunchAgents / LaunchDaemons 目录写入 plist 文件实现自启动。
- **背景进程**：如 App 有后台 Helper 进程（SMLoginItem），Helper 必须与主 App 同在一个沙盒边界内。

---

## 3. 禁止自定义更新机制

**规则来源：Mac App Store Review Guidelines 3.2 / 2.4.5**

- **严格禁止**：在 Mac App Store 版本中集成 Sparkle、自定义 SUUpdater 或任何绕过 Mac App Store 的更新机制。
- **严格禁止**：提示用户访问外部网站下载更新版本。
- **严格禁止**：在 App 内展示"新版本可用，请前往官网下载"类型的提示。
- **唯一例外**：Developer ID 分发版本（非 MAS 版本）可使用 Sparkle 等更新框架。
- **实操建议**：如果你同时维护 MAS 版和 Developer ID 版，确保两个 target 的更新逻辑通过编译条件完全分离。

---

## 4. 禁止要求 root 权限或 setuid

**规则来源：Mac App Store Review Guidelines / 沙盒机制**

- **完全禁止**：App 或其任何组件（Helper、脚本）在运行时请求提权（`sudo`、`AuthorizationExecuteWithPrivileges`、setuid 二进制文件）。
- **禁止**：在 App 内安装需要 root 权限的系统扩展（Kernel Extension / kext），MAS 中不允许 kext。
- **System Extensions（DriverKit）**：部分类型的 System Extension 可在 MAS 中使用，但需要 Apple 单独批准对应 Entitlement。
- **Privileged Helper**：如确实需要特权操作，必须使用 `SMJobBless` 机制，且该 Helper 不能通过 MAS 分发（需配合 Developer ID 方案）。

---

## 5. 单一安装包要求

**规则来源：Mac App Store Review Guidelines 2.1**

- App 必须通过单一的 `.app` 包分发，不得要求用户运行额外的安装脚本或安装程序。
- **禁止**：在首次启动时弹出安装向导要求用户额外操作（如"请将 App 拖入 Applications 文件夹"——MAS 已自动处理）。
- **禁止**：安装阶段写入 `/usr/local/bin` 或其他系统目录的命令行工具（沙盒限制）。
- **允许**：在 App 首次启动时引导用户进行可选配置（如授予辅助功能权限），但必须是请求权限，不能是修改系统文件。

---

## 6. 禁止许可证屏幕和许可证密钥

**规则来源：Mac App Store Review Guidelines 3.2**

- **禁止**：启动时弹出许可证协议（EULA）要求用户接受才能继续（Apple 已通过 App Store 条款覆盖基础许可）。
- **禁止**：要求用户输入序列号、激活码或许可证密钥才能使用 App 功能。
- **禁止**：包含 LicenseSpring、Cryptlex 等许可证管理 SDK。
- **允许**：展示简短的使用说明或欢迎界面，只要不阻止用户正常使用。
- **订阅/IAP**：功能解锁必须通过 StoreKit，不得绕过 App Store 付款体系。

---

## 7. Mac Catalyst 额外注意事项

**规则来源：Human Interface Guidelines / Mac App Store 审核实践**

Mac Catalyst 将 iPad App 编译为 macOS App，但以下差异需特别处理：

- **UI 适配**：
  - 菜单栏（Menu Bar）：Catalyst App 必须实现合理的菜单栏结构，不能为空菜单。
  - 键盘快捷键：至少支持基础快捷键（⌘Q 退出、⌘, 偏好设置、⌘W 关闭窗口）。
  - 窗口大小调整：必须支持窗口缩放，不得锁定固定尺寸（Apple 审核员会手动测试）。
- **截图要求**：Mac 版必须提供 macOS 截图（1280×800 或 1440×900），不能用 iPad 截图替代。
- **功能降级**：如某些 iOS/iPadOS 功能在 macOS 上不可用（如摄像头 AR），必须优雅降级，不得崩溃。
- **Catalyst 优化**：建议启用 "Mac Idiom"（`UIUserInterfaceIdiomMac`）而非 "iPad Scaled"，以获得更好的 macOS 原生体验，也更符合 Apple 审核期望。

---

## 常见拒审场景

1. **包含 Sparkle 更新框架**：即使在 `#if !MAS` 编译条件下，如果 Sparkle 代码仍可访问，审核员可能拒审。
2. **启动时请求辅助功能权限**但未解释用途，且功能不合理（如截图工具要求辅助功能权限）。
3. **Hardened Runtime 关闭**（Xcode 打包时未启用）：Mac App Store 必须启用。
4. **App 尝试访问 `~/Desktop` 等用户目录**而未通过 NSOpenPanel 获得用户授权。
5. **Mac Catalyst App 没有菜单栏条目**：审核员认为 App 未完成 macOS 适配。
6. **App 在 macOS Sequoia 上使用了废弃的 API**（如旧版 NSOpenPanel 代理方法），导致功能失常。
