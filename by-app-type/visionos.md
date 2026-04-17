# visionOS App 专项风险

> 本文件仅记录超出通用审核规则的专项要求。适用于 Apple Vision Pro（visionOS）平台的 App。

---

## 1. 沉浸式体验的空间数据隐私要求

**规则来源：App Store Review Guidelines 5.1.1 / visionOS 隐私框架**

visionOS 引入了前所未有的空间传感数据类型，Apple 对其有严格限制：

**受保护的空间数据类型**：
- **手部追踪数据**（Hand Tracking）：手势、手指关节位置
- **头部位置和方向数据**（Head Pose）
- **眼动追踪数据**（Eye Tracking）——见下一节
- **世界感知数据**（World Sensing）：AR 环境扫描、平面检测
- **ARKit 空间锚点数据**

**使用原则**：
- 空间数据只能用于 App 功能所必需的目的，**不得用于广告、用户画像或分析**。
- 不能将空间数据发送至后台服务器（除非是功能必需，如云端 3D 渲染，且需明确告知用户）。
- **Info.plist 权限描述**：所有空间数据权限（`NSWorldSensingUsageDescription`、`NSHandsTrackingUsageDescription` 等）的描述必须准确、具体，不能用模糊表述。
- 禁止在用户未处于沉浸式体验时静默采集环境数据。

---

## 2. 眼动追踪数据的特殊限制

**规则来源：App Store Review Guidelines 5.1.1 / ARKit 隐私指南**

眼动追踪（Eye Tracking）是 visionOS 中受保护程度最高的数据：

- **系统级隔离**：Apple 采用了隐私保护设计——App **无法直接获取用户注视点的精确坐标**。系统只告诉 App"用户选择了哪个元素"（通过 RealityKit 的 focus 检测），而不是眼球的实际位置数据。
- **不允许**：尝试通过 ARKit 或其他 API 获取原始眼球追踪数据（不是 SwiftUI/RealityKit 框架的焦点检测）。
- **允许**：
  - 使用 SwiftUI `onHover` / RealityKit 的凝视检测来响应用户注意力（高层 API）
  - 在 App 内实现基于注视的 UI 交互（如"注视即选中"）
- **隐私政策要求**：如果 App 使用了任何凝视相关功能，必须在隐私政策中说明其用途，即使实际上没有收集原始数据。
- **未来风险**：即使 App 只使用高层 API，审核员可能会询问眼动交互的实现方式，建议在 Review Notes 中主动说明。

---

## 3. 与 iOS/iPadOS App 的主要差异点

visionOS 版 App 不能简单等同于 iOS App，以下是关键差异：

| 维度 | iOS/iPadOS | visionOS |
|------|-----------|---------|
| 输入方式 | 触摸屏 | 凝视 + 手势 + Bluetooth 键鼠/手柄 |
| 空间模式 | 仅平面 UI | 窗口（Window）/ 体积（Volume）/ 沉浸式（Immersive Space） |
| 深度感知 | 无 | App 可感知环境（需授权） |
| 隐私数据类型 | 位置、相机、麦克风等 | 额外增加手部、眼动、世界感知 |
| 权限申请 | 运行时请求 | 同 iOS 运行时请求，但类型更多 |
| 截图 | 设备截图 | 需要 visionOS 模拟器或设备截图 |

**审核注意**：
- 如果你的 App 是从 iOS 迁移到 visionOS（Mac Catalyst 类似），审核员会检查 UI 是否针对空间计算做了适当优化，纯缩放的 iPad UI 可能被认为不符合 visionOS 体验标准。
- 涉及相机权限（`NSCameraUsageDescription`）的功能在 Vision Pro 上会通过外部摄像头实现，但隐私要求与 iOS 一致。

---

## 4. visionOS 版截图和预览要求

**规则来源：App Store Connect Help**

- **截图尺寸**：visionOS 专用截图尺寸为 **2732×2048 px**（横向）。
- **截图数量**：最少 1 张，最多 10 张。
- **格式**：PNG 或 JPEG。
- **内容要求**：
  - 必须反映 visionOS 上的实际 App 界面，不能用 iPhone/iPad 截图替代。
  - 建议展示 App 的空间 UI 特性（窗口悬浮在环境中的效果）。
  - 可以使用 visionOS 模拟器截图（Xcode → Simulator → File → Take Screenshot）。
- **App 预览视频**：
  - 分辨率：2732×2048 px
  - 时长：15–30 秒
  - 可展示沉浸式体验，但不能使用真实用户面部（隐私要求）
- **注意**：如果 App 是 iPad App 的 visionOS 兼容版本（Designed for iPad），仍可使用 iPad 截图，但建议提供 visionOS 专用截图以展示最佳体验。

---

## 5. 沉浸式体验设计合规注意事项

- **安全警告**：如果 App 包含高度沉浸式体验（Full Space），建议在进入前展示安全提示（与周围环境的安全距离，不要在移动中使用）。
- **退出机制**：沉浸式 App 必须提供清晰的退出方式（数字冠一键退出是系统级保障，但 App 内也应有退出按钮）。
- **晕动症（Motion Sickness）**：高速移动或不稳定的视觉体验需要提供设置开关（如降低运动效果）以适应不同用户。
- **内容评级**：沉浸式暴力或成人内容的评级标准比平面内容更严格，因为沉浸感会放大内容的影响。

---

## 常见 visionOS 拒审场景

1. **使用了 ARKit 低层 API 获取眼动数据**：即使未存储，也可能触发隐私审查。
2. **截图使用 iPhone 界面**：visionOS 版本必须提供专用截图。
3. **沉浸式体验没有退出按钮**：依赖数字冠是不够的。
4. **权限描述（Usage Description）过于模糊**：如 `NSWorldSensingUsageDescription` 写"用于改善体验"会被要求修改。
5. **App 将手部追踪数据发送到服务器**但未在隐私政策中说明。
6. **UI 仅是 iPad App 放大版，未利用空间计算特性**：审核员认为用户体验不符合平台标准（Guidelines 2.1）。
