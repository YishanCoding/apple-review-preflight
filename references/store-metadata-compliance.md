# App Store 元数据 / 截图 / 年龄分级合规

> 覆盖 App Store Connect 中所有元数据字段的字符限制、违规词规则、截图设备边框规范、年龄分级问卷（含 2026 新规）、In-App Events 及 App Previews 规格要求。
> 规则来源：App Store Review Guidelines 2.3 / 2.3.7 / 2.3.10 / ASC Help

---

## 一、文本元数据字段限制

| 字段 | 最大字符 | 规则 |
|------|---------|------|
| App Name | 30 | 不可含 price（"免费"/"free"）、促销词（"限时"/"特惠"）、与 Apple 产品名冲突的词、竞品名称 |
| Subtitle | 30 | 同上；不可重复 App Name 内容 |
| Keywords | 100 | 逗号分隔，不含空格；不可含竞品名、Apple 产品名、与 App 无关的词、单字符填充 |
| Description | 4000 | 不可含未上线功能、竞品名称、价格信息（会变动）、「#1」等排名声明（除非有可信来源） |
| Promotional Text | 170 | 可随时更新（无需新版本），适合促销信息 |
| What's New | 4000 | 每次提交版本时更新 |
| App Review Notes | 4000 | 演示账号、特殊硬件说明、隐藏功能入口 |
| URL（隐私政策等） | 255 | 必须 https，可公开访问，不要求登录 |

### 1.1 违规词列表（2.3.7 / 2.3.10）

以下关键词会触发自动/人工审核拒绝：

| 类型 | 示例 | 条款 |
|------|------|------|
| 竞品名称 | 「比微信更好」「类似 Telegram」 | 2.3.7 |
| Apple 产品名 | 「for iPhone 16 Pro」（除非确实仅支持特定设备） | 2.3.7 |
| 排名声明 | 「最好用的 XX App」「App Store 排名第1」 | 2.3.7（无可信来源） |
| 促销词 | 「限时免费」「5折优惠」「Sale」 | 2.3.7 |
| 价格 | 「仅 $0.99」「免费试用」（Subtitle/Name 中） | 2.3.7 |
| 「app」一词 | Name/Subtitle 中含 "app" | 2.3.7 |
| 平台名 | 「Android 也可用」 | 2.3.7 |
| 表情符号 | Name/Subtitle 中使用 emoji | 2.3.7 |
| 误导性分类 | App 实际功能与所选分类不符 | 2.3.10 |

### 1.2 App Name 变更注意事项

- 更改 App Name 需提交新版本
- 频繁更改 App Name 可能触发额外审核
- 开发者名称变更需联系 Apple Developer Support

---

## 二、截图规范

### 2.1 截图设备与尺寸要求

| 设备类型 | 尺寸（像素）| 必需 |
|---------|-----------|------|
| iPhone 6.9" | 1320 × 2868 | ✅ 必需（App Store 展示基准）|
| iPhone 6.7" | 1290 × 2796 | ✅ 必需 |
| iPhone 6.5" | 1284 × 2778 或 1242 × 2688 | 可选（向下兼容）|
| iPhone 5.5" | 1242 × 2208 | 仅支持 iPhone 8 Plus 及以下时需要 |
| iPad Pro 13" | 2064 × 2752 | ✅ iPad App 必需 |
| iPad Pro 12.9" | 2048 × 2732 | ✅ iPad App 必需 |
| Apple Watch | 视表盘尺寸 | watchOS App 必需 |
| Apple TV | 1920 × 1080 或 3840 × 2160 | tvOS App 必需 |
| Mac | 最小 1280 × 800 | macOS App 必需 |
| Vision Pro | 按 visionOS 要求 | visionOS App 必需 |

### 2.2 截图内容规则（2.3.1 / 2.3.3）

- **必须**：截图来自当前版本真实 UI（可加文案覆盖层）
- **必须**：展示 App 实际功能，不可展示未上线功能
- **禁止**：包含 iPhone/iPad 设备边框（除非使用 Apple 官方 Marketing Assets 提供的正确边框）
- **禁止**：包含其他 App 的 UI 元素
- **禁止**：包含 status bar 中的虚假信号/时间
- **建议**：第一张截图最具吸引力，App Store 搜索结果中首先展示

### 2.3 iPad 特别要求

- 如果 App 支持 iPad，**必须提供 iPad 截图**
- Universal App 不能只用 iPhone 截图代替 iPad 截图
- iPad 截图必须展示 iPad 上的实际布局（非放大的 iPhone 界面）

---

## 三、App Previews（视频预览）

| 属性 | 要求 |
|------|------|
| 格式 | H.264 或 HEVC，30fps |
| 时长 | 15–30 秒 |
| 数量 | 每种设备最多 3 个 |
| 内容 | 必须为 App 内录屏（可加字幕和背景音乐）|
| 禁止 | 实拍非 App 内容、过度营销风格、不代表实际体验的特效 |
| 首帧 | 第一帧作为海报帧，App 未播放时展示 |

---

## 四、年龄分级问卷（2026 新规）

### 4.1 新年龄段体系

Apple 于 2025 年底 / 2026 年初更新了年龄分级系统，引入新的分级梯度：

| 分级 | 适用场景 |
|------|---------|
| 4+ | 无不良内容 |
| 9+ | 轻度卡通暴力、幻想暴力 |
| 12+ | 轻度现实暴力、偶尔粗话、模拟赌博 |
| **13+** | 频繁/剧烈卡通暴力或幻想暴力、不频繁现实暴力、偶尔色情内容 |
| **16+** | 频繁/剧烈现实暴力、频繁色情或暗示内容、频繁粗话 |
| 17+ | 不受限制的网页访问、赌博（真实货币）、频繁剧烈暴力和色情 |
| **18+** | 仅限成人内容（部分地区需要年龄验证） |

### 4.2 问卷关键项

ASC 中的年龄分级问卷包含以下维度：

| 维度 | 选项 | 影响 |
|------|------|------|
| 暴力 - 卡通/幻想 | None / Infrequent-Mild / Frequent-Intense | 直接影响分级 |
| 暴力 - 现实 | None / Infrequent-Mild / Frequent-Intense | 12+ 起步 |
| 色情/裸露 | None / Infrequent-Mild / Frequent-Intense | 12+ 起步 |
| 粗话 | None / Infrequent-Mild / Frequent-Intense | 9+ 起步 |
| 毒品/药物/酒精/烟草 | None / Infrequent-Mild / Frequent-Intense | 12+ 起步 |
| 赌博（模拟） | No / Yes | 12+ |
| 赌博（真实货币） | No / Yes | 17+ |
| 恐怖/惊悚 | None / Infrequent-Mild / Frequent-Intense | 9+ 起步 |
| 医疗/治疗信息 | None / Infrequent-Mild / Frequent-Intense | 影响 Medical Device 声明触发 |
| 不受限网页访问 | No / Yes | 17+ |
| 竞赛 | No / Yes | — |

### 4.3 年龄验证（2026 新要求）

从 iOS 26.4 开始，Apple 在部分地区启用**设备级年龄验证**：

| 地区 | 要求 | 生效日期 |
|------|------|---------|
| 澳大利亚、巴西、新加坡 | 18+ App 需年龄验证 | 2026-02-24 |
| 犹他 | 18+ App 需年龄验证 | 2026-05-06 |
| 路易斯安那 | 18+ App 需年龄验证 | 2026-07-01 |
| 英国 | 18+ App 需系统级年龄验证（Online Safety Act） | 2026-04-01（iOS 26.4） |

**对开发者的影响**：
- 年龄分级如实填写即可，**验证由系统完成**，无需 App 内额外实现
- 但分级不准确（如将 18+ 内容标为 12+）会导致拒审或下架
- ⚠️ 经验规则：UGC 类 App 应保守评估，宁可标高不可标低

### 4.4 MADE FOR KIDS

选择「Made for Kids」的 App 有额外限制（见 `../by-app-type/kids.md`）：
- 不可包含第三方广告
- 不可包含跨 App tracking
- 必须提供家长隐私政策

---

## 五、In-App Events

| 属性 | 限制 |
|------|------|
| Event Name | 30 字符 |
| Short Description | 50 字符 |
| Long Description | 120 字符 |
| 图片 | 1920 × 1080px（横向） |
| 视频 | 可选，30 秒内 |
| 最大活动事件 | 每 App 最多 5 个同时上线 |
| 审核 | 每个 Event 独立审核，内容规则与 App 元数据一致 |

---

## 六、本地化注意事项

### 6.1 基础规则

- 每种语言独立审核，一种语言被拒不影响其他语言
- 中国大陆 App Store 的描述语言应为简体中文
- 所有法律链接必须匹配 App 语言或提供对应语言版本
- 截图文案覆盖层需对应语言版本

### 6.2 支持的本地化语言（2026-03-31 扩展到 50 种）

自 **2026-03-31** 起 App Store 新增 **11 种** 本地化语言，合计支持 **50 种**：

| 新增语言 | 代码 | 区域 |
|---------|------|------|
| Bangla（孟加拉语）| `bn` | India / Bangladesh |
| Gujarati（古吉拉特语）| `gu` | India |
| Kannada（卡纳达语）| `kn` | India |
| Malayalam（马拉雅拉姆语）| `ml` | India |
| Marathi（马拉地语）| `mr` | India |
| Odia（奥里亚语）| `or` | India |
| Punjabi（旁遮普语）| `pa` | India / Pakistan |
| Slovenian（斯洛文尼亚语）| `sl` | Slovenia |
| Tamil（泰米尔语）| `ta` | India / Sri Lanka |
| Telugu（泰卢固语）| `te` | India |
| Urdu（乌尔都语）| `ur` | Pakistan / India |

**使用场景**：
- [ ] ASC → App Information → Localizations 下可选新语言作为 primary 或 additional
- [ ] 翻译覆盖的字段：App Name / Subtitle / Description / Keywords / Promo Text / What's New / In-App Event / Custom Product Page 均可配置对应语言的 localized 版本
- [ ] iOS Info.plist `CFBundleLocalizations` 加入对应 code 即可启用系统层 localization

⚠️ **提交路径说明**：新增一种 localization 通常需要随下一个 app version 一并审核；**Promotional Text** 和部分 Localized Metadata 子字段可通过 `../operations/review-ops.md` §七 的独立提交通道送审（无需新 build）。但 App Name / Subtitle / Description / Keywords 等核心字段的首次本地化必须跟 version 一起提交。

**影响最大的地区**：印度（8 种新增）、巴基斯坦（Punjabi / Urdu）、孟加拉国（Bangla）、斯洛文尼亚。历史上这些市场仅能用 English 或 Hindi，上架后曝光提升明显。

⚠️ 经验规则：新增语言 localization 首次提交需跟 version 一起审核；后续对已启用语言的 metadata 调整，**Promo Text** 类字段可走独立通道（见 `../operations/review-ops.md` §七）而无需新 build。

**来源**：
- ✅ [Apple Developer News 2026-03-31: App Store expands support to 11 new languages](https://developer.apple.com/news/?id=97t4mt64)
- ✅ [ASC: Add a localization](https://developer.apple.com/help/app-store-connect/manage-app-information/add-localizations)

---

## 七、审核 Checklist

### 提交前必检

- [ ] **2.3.7**：App Name（≤30字）不含促销词、竞品名、"app"、emoji
- [ ] **2.3.7**：Subtitle（≤30字）不重复 App Name、不含禁止词
- [ ] **2.3.7**：Keywords（≤100字）不含竞品名、Apple 产品名
- [ ] **2.3.1**：Description 不含未上线功能描述
- [ ] **2.3.7**：Description 不含排名声明（无可信来源）、竞品名
- [ ] **2.3.1**：截图来自当前版本真实 UI
- [ ] 截图尺寸符合每种设备要求（6.9" + 6.7" 必需）
- [ ] iPad App 已提供 iPad 独立截图
- [ ] 隐私政策 URL 有效、可公开访问、内容完整
- [ ] EULA/Terms URL 有效（⚠️ JuJuBit 经验：Notion 公开链接在审核员网络下可能无法访问，建议使用自有域名）
- [ ] 年龄分级问卷如实填写（UGC App 保守评估）
- [ ] App Review Notes 已填写演示账号和特殊说明

### 常见元数据拒审

| 场景 | 条款 | 修复 |
|------|------|------|
| App Name 含「免费」 | 2.3.7 | 移除价格相关词 |
| Subtitle 含 emoji | 2.3.7 | 移除 emoji |
| Keywords 含竞品「WhatsApp」 | 2.3.7 | 移除竞品名 |
| 截图展示 beta 功能 | 2.3.1 | 更新为当前版本截图 |
| 隐私政策链接 404 | 5.1.1 | 修复链接或更换 host |
| 年龄分级低于实际内容 | 年龄分级 | 重新填写问卷 |

---

## 八、参考链接

- [App Store Review Guidelines 2.3](https://developer.apple.com/cn/app-store/review/guidelines/#metadata)
- [App Store Connect Help: App Information](https://developer.apple.com/help/app-store-connect/manage-app-information/)
- [Screenshot Specifications](https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications/)
- [App Preview Specifications](https://developer.apple.com/help/app-store-connect/reference/app-preview-specifications/)
- 相关文件：`../checks/review-failure-map.md`、`../by-app-type/all-apps.md`
