# Guidelines 更新 Playbook

> 如何定期检查 Apple Guidelines 变动并更新本 skill。
> 建议频率：每月一次，或在 WWDC / Apple 重大公告后立即执行。

---

## 一、更新流程概览

```
① 检查 Apple News / Upcoming Requirements
        ↓
② 运行 scripts/check-guideline-updates.sh 对比快照
        ↓
③ 识别变动条款
        ↓
④ 更新 policy-updates-log.md
        ↓
⑤ 更新对应 guidelines/*.md 和其他受影响文件
        ↓
⑥ 更新 source-map.md（如有新来源）
        ↓
⑦ 验证交叉引用完整性
        ↓
⑧ 提交 commit
```

---

## 二、Step 1：检查 Apple 官方信息源

### 2.1 必查来源

| 来源 | URL | 检查内容 |
|------|-----|---------|
| Apple Developer News | https://developer.apple.com/cn/news/ | 新公告、政策变动 |
| Upcoming Requirements | https://developer.apple.com/news/upcoming-requirements/ | 即将生效的强制要求和截止日期 |
| App Store Review Guidelines | https://developer.apple.com/cn/app-store/review/guidelines/ | Guidelines 正文变动 |
| ASC Help | https://developer.apple.com/help/app-store-connect/ | ASC 功能更新 |
| WWDC Sessions | https://developer.apple.com/wwdc/ | 每年 6 月，新 OS/SDK/政策 |

### 2.2 补充来源

| 来源 | 用途 |
|------|------|
| [9to5Mac](https://9to5mac.com) | 开发者相关新闻汇总 |
| [MacRumors Developer](https://www.macrumors.com/guide/developer/) | 开发者政策动态 |
| [Apple Developer Forums](https://developer.apple.com/forums/) | 官方回复和社区反馈 |

---

## 三、Step 2：运行快照对比脚本

```bash
# 在 skill 根目录运行
bash policy/scripts/check-guideline-updates.sh
```

### 3.1 脚本工作原理

1. 调用 Wayback Machine CDX API 获取 Apple Guidelines 页面最近 10 次快照索引
2. 取最新两次快照的文本内容
3. 生成 unified diff 输出变动

### 3.2 解读输出

- `No changes between two latest snapshots.` — 无变动，记录检查日期即可
- 有 diff 输出 — 分析变动：
  - `+` 行：新增内容
  - `-` 行：删除内容
  - 重点关注条款号变动、新增条款、措辞变化

### 3.3 脚本限制

- Wayback Machine 的抓取频率不固定，可能有数周延迟
- 中文版页面的抓取可能不如英文版频繁
- 如果脚本输出「快照不足 2 个」，改用英文版 URL 或人工对比

---

## 四、Step 3：识别变动条款

对比结果中，重点关注：

| 变动类型 | 影响级别 | 处理方式 |
|---------|---------|---------|
| 条款号新增 | 高 | 判断是否需要新文件或在现有文件中添加章节 |
| 条款号删除 | 高 | 检查本 skill 中是否有引用，移除或标注过时 |
| 措辞变化（实质性） | 中 | 更新对应文件中的描述 |
| 措辞变化（非实质性） | 低 | 仅记录在 policy-updates-log.md |
| 截止日期变更 | 高 | 更新 SKILL.md 2026 年关键新规表和对应文件 |
| 新增平台/设备要求 | 中 | 更新 new-os-api-compliance.md 或对应 by-app-type 文件 |

---

## 五、Step 4：更新 policy-updates-log.md

在 `policy-updates-log.md` 最顶部插入新记录，格式：

```markdown
### YYYY-MM-DD — 变动简述

| 影响条款 | 变动 | 本 skill 影响 |
|---------|------|-------------|
| X.X.X | 变动描述 | `../path/to/affected-file.md` 已更新 / 需更新 |
```

---

## 六、Step 5：更新受影响文件

### 6.1 更新原则

- 直接修改对应文件内容，不创建「补丁」或「附录」
- 保持文件结构不变，仅更新变动的具体内容
- 如变动重大需要新文件，在 SKILL.md 路由表中添加入口
- 更新后检查文件行数是否超过 500 行（拆分阈值）

### 6.2 需同步更新的位置

每次变动可能影响多个文件，按以下顺序检查：

1. **SKILL.md** — `2026 年关键新规` 表（如有新截止日期）
2. **guidelines/*.md** — 条款正文变动
3. **checks/*.md** — checklist 中的条款引用
4. **by-app-type/*.md** — 特定 App 类型受影响的条款
5. **references/*.md** — 技术参考变动
6. **market-overrides/*.md** — 地区特殊政策变动

---

## 七、Step 6-7：更新 source-map.md + 验证交叉引用

### 7.1 更新 source-map.md

如果新增了 Apple 来源 URL 或现有 URL 失效，更新 `source-map.md`。

### 7.2 验证交叉引用

```bash
# 在 skill 根目录运行，检查所有内部链接是否指向存在的文件
cd /Users/sam/agent-skills/agents-skills/apple-review-preflight

find . -name "*.md" -print0 | while IFS= read -r -d '' file; do
  dir=$(dirname "$file")
  grep -oE '`(\.\./)?(by-app-type|checks|guidelines|market-overrides|operations|policy|references)/[A-Za-z0-9_-]+\.md`|`[A-Za-z0-9_-]+\.md`' "$file" \
    | tr -d '`' \
    | while IFS= read -r ref; do
      case "$ref" in *xxx.md) continue ;; esac
      case "$ref" in
        ../*) target="$dir/$ref" ;;
        by-app-type/*|checks/*|guidelines/*|market-overrides/*|operations/*|policy/*|references/*) target="./$ref" ;;
        *) target="$dir/$ref" ;;
      esac
      if [ -f "$target" ]; then
        continue
      fi
      # Bare filenames in catalogs (such as source-map.md) are valid if they
      # uniquely resolve somewhere under the skill root.
      matches=$(find . -name "$ref" -type f 2>/dev/null | wc -l | tr -d ' ')
      if [ "$matches" -eq 0 ]; then
        echo "BROKEN: $file -> $ref"
      fi
    done
done
```

---

## 八、特殊时间节点

### 8.1 WWDC（每年 6 月）

WWDC 通常发布：
- 新 OS 版本（影响 `new-os-api-compliance.md`）
- Guidelines 重大更新
- 新 framework/API（可能影响 required reason API 列表）
- 新设备类型（可能需要新的 by-app-type 文件）

**建议**：WWDC 后 1 周内完成全面更新。

### 8.2 新 SDK 编译截止日期（通常每年 4 月）

- 更新 `new-os-api-compliance.md` 中的版本号和日期
- 更新 `SKILL.md` 中的关键新规表
- 更新 `operations/cicd-upload.md` 中的 Xcode 版本要求

### 8.3 Apple 突发公告

- 实时关注 Apple Developer News
- 医疗器械、DMA、隐私等重大政策变动可能随时发布
- 发现后立即执行更新流程

---

## 九、更新 Checklist

每次更新完成后，验证：

- [ ] `policy-updates-log.md` 已添加新记录
- [ ] 受影响文件已更新内容
- [ ] `source-map.md` 已更新（如有新来源）
- [ ] 交叉引用验证通过（无 BROKEN 链接）
- [ ] SKILL.md 路由表与实际文件一致
- [ ] 每个文件 < 500 行
- [ ] commit message 包含变动条款号

---

## 十、参考

- 快照对比脚本：`scripts/check-guideline-updates.sh`
- 变动日志：`policy-updates-log.md`
- 来源映射：`source-map.md`
