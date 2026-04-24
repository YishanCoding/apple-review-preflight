# Apple Review Preflight

> A comprehensive AI skill for Apple App Store review compliance — covering pre-submission checklists, rejection prevention, appeals, and policy tracking.

**English** | [中文](#中文)

---

![Feature Map](docs/feature-map.png)

## What Is This?

A structured knowledge base and AI skill that helps app developers:

- **Prevent rejections** before submission (covers the top 10 rejection reasons)
- **Navigate rejections** with correct response strategies
- **Stay current** with Apple's evolving guidelines (Wayback snapshot diff + monthly review playbook — see [Policy Updates](#policy-updates))
- **Handle edge cases** — regional compliance, account warnings, expedited review, IP disputes, and more

Built on Apple's 2026 review data: 7.7M submissions reviewed, 1.9M rejected. **Most rejections are 100% preventable.**

---

## Coverage

| Area | Files |
|------|-------|
| App-type checklists | 14 types (subscription, AI, games, health, kids, dating, ecommerce, crypto, VPN, UGC, macOS, tvOS, watchOS, visionOS) |
| Pre-submission scans | Privacy manifest, Required Reason APIs, background modes, code patterns, metadata |
| Regional compliance | China (ICP/PIPL), EU/EEA (DMA/GDPR), UK (OSA/UKGC), US (COPPA/CCPA) |
| Operations | Rejections, appeals, expedited review, account warnings, IP infringement, editorial featuring, phased release, CI/CD |
| Automation scripts | `scripts/preflight-scan.{py,sh}` (project detection + PrivacyInfo per-target coverage matrix + Info.plist scan + risky deps); `policy/scripts/check-live-sources.sh` (4 live Apple sources w/ diff cache + Jina fallback); `policy/scripts/check-guideline-updates.sh` (Wayback auxiliary) |
| Policy tracking | Live source diff (primary) + Wayback snapshot diff (auxiliary), change log, source mapping, monthly review playbook |

---

## Installation

Skills are auto-discovered when placed in the agent's skill directory. The skill name comes from the SKILL.md frontmatter `name` field (here: `apple-review-preflight`); keep the directory named to match.

### Claude Code

```bash
git clone https://github.com/YishanCoding/apple-review-preflight ~/.claude/skills/apple-review-preflight
```

Restart Claude Code so the skill is indexed. Verify by typing `/` and confirming `apple-review-preflight` appears in the skill list, then invoke it.

### OpenClaw

```bash
git clone https://github.com/YishanCoding/apple-review-preflight ~/agent-skills/agents-skills/apple-review-preflight
```

### Codex

Codex shares OpenClaw's `agents-skills/` directory — install via OpenClaw above and Codex will pick it up automatically.

### Sharing across all three (Claude Code + OpenClaw + Codex)

Single source of truth, symlinked into Claude Code's skill dir:

```bash
git clone https://github.com/YishanCoding/apple-review-preflight ~/agent-skills/agents-skills/apple-review-preflight
ln -s ~/agent-skills/agents-skills/apple-review-preflight ~/.claude/skills/apple-review-preflight
```

### Plain Claude (no CLI)

Copy the contents of `SKILL.md` and paste into your conversation as a system prompt or initial message.

### Keep Updated

```bash
cd ~/.claude/skills/apple-review-preflight && git pull
# or, if shared via the symlink setup:
cd ~/agent-skills/agents-skills/apple-review-preflight && git pull
```

---

## Quick Start

### Pre-submission check (5 steps)

1. **Scan your project** — `bash scripts/preflight-scan.sh /path/to/your/project` (one-shot project detection + PrivacyInfo per-target coverage + Info.plist scan + risky deps), or run the manual commands in `SKILL.md` Step 1
2. **Load your app type** — find your category in `by-app-type/`
3. **Run compliance checks** — `checks/review-failure-map.md` + `checks/privacy-transparency-consistency.md`
4. **Check regional rules** — `market-overrides/` for China/EU/UK/US
5. **Generate report** — use `checks/report-template.md` (must follow the 5-section contract in `SKILL.md` Step 5)

### After a rejection

Go to `operations/review-ops.md` — it covers response strategy, appeal templates, and when to reply vs. resubmit.

### Route by scenario

| Scenario | File |
|----------|------|
| Expedited review | `operations/expedited-review.md` |
| Account warning / Pending Termination | `operations/account-warnings.md` |
| IP infringement dispute | `operations/ip-infringement.md` |
| App removed / keyword penalty | `operations/app-penalty-recovery.md` |
| Editorial featuring | `operations/editorial-featuring.md` |

---

## Policy Updates

Apple updates its guidelines regularly. To check for changes:

```bash
# Primary: 4 live sources (EN/CN Guidelines + Upcoming Requirements + Apple News)
bash policy/scripts/check-live-sources.sh

# Auxiliary: Wayback historical snapshots (long-term trend / time-travel)
bash policy/scripts/check-guideline-updates.sh
```

The live-source script catches changes earlier than Wayback (Apple often updates EN before CN, and posts News before changing Guidelines). See `policy/update-playbook.md` for the full update workflow.

---

## Contributing

PRs welcome for:
- New app-type guides
- Regional compliance updates
- Corrections to guideline references
- New rejection patterns

Please open an issue before large changes.

---

## License

MIT

---

---

# 中文

![功能概览](docs/feature-map-zh.png)

## 这是什么？

一个结构化的 Apple App Store 审核合规 AI Skill，帮助开发者：

- **提交前预防拒审**（覆盖 Top 10 拒审原因）
- **被拒后正确应对**（回复策略 + 申诉模板）
- **跟踪政策变化**（Wayback 快照对比 + 月度复查 playbook，详见下方 Quick Start 政策更新检查）
- **处理复杂场景**（区域合规、账号警告、加急审核、知识产权争议等）

---

## 安装

Skill 通过约定目录被 agent 自动发现。Skill 名取自 SKILL.md frontmatter 的 `name` 字段（本 skill：`apple-review-preflight`），目录名保持一致。

### Claude Code

```bash
git clone https://github.com/YishanCoding/apple-review-preflight ~/.claude/skills/apple-review-preflight
```

重启 Claude Code 让索引加载新 skill。在输入框打 `/` 确认 `apple-review-preflight` 出现在列表中，再调用。

### OpenClaw

```bash
git clone https://github.com/YishanCoding/apple-review-preflight ~/agent-skills/agents-skills/apple-review-preflight
```

### Codex

Codex 与 OpenClaw 共享 `agents-skills/` 目录，按上一步装好 OpenClaw，Codex 会自动识别。

### 三端共享（Claude Code + OpenClaw + Codex）

单一来源 + symlink 到 Claude Code 的 skill 目录：

```bash
git clone https://github.com/YishanCoding/apple-review-preflight ~/agent-skills/agents-skills/apple-review-preflight
ln -s ~/agent-skills/agents-skills/apple-review-preflight ~/.claude/skills/apple-review-preflight
```

### 纯 Claude（无 CLI）

将 `SKILL.md` 内容复制粘贴到对话开头作为上下文。

### 保持更新

```bash
cd ~/.claude/skills/apple-review-preflight && git pull
# 或者使用了 symlink 共享方案的话：
cd ~/agent-skills/agents-skills/apple-review-preflight && git pull
```

---

## 快速上手

**提交前预检**：
```bash
# 一键扫描（项目栈识别 + PrivacyInfo per-target 覆盖率 + Info.plist 扫描 + 依赖风险）
bash scripts/preflight-scan.sh /path/to/your/project
```
然后按 `SKILL.md` 的 5 步流程执行（Step 5 报告需符合强制 contract）。

**被拒后**：进入 `operations/review-ops.md`

**政策更新检查**：
```bash
# 主路径：4 个 live 源（CN/EN Guidelines + Upcoming Requirements + Apple News）
bash policy/scripts/check-live-sources.sh

# 辅助：Wayback 历史趋势 / 长周期回溯
bash policy/scripts/check-guideline-updates.sh
```

---

## 覆盖范围

| 模块 | 内容 |
|-----|------|
| App 类型专项 | 14 种（订阅、AI、游戏、健康、儿童、交友、电商、加密、VPN、UGC、macOS、tvOS、watchOS、visionOS） |
| 预检扫描 | 隐私清单、Required Reason API、后台模式、代码模式、元数据 |
| 区域合规 | 中国大陆（ICP/PIPL）、欧盟（DMA/GDPR）、英国（OSA）、美区（CCPA/外部支付） |
| 运营操作 | 被拒处理、申诉、加急审核、账号警告、知识产权、精品推荐、分阶段发布、CI/CD |
| 自动化脚本 | `scripts/preflight-scan.{py,sh}`（项目栈识别 + PrivacyInfo per-target 覆盖率矩阵 + Info.plist 扫描 + 依赖风险）；`policy/scripts/check-live-sources.sh`（4 个 Apple live 源 diff + Jina fallback）；`policy/scripts/check-guideline-updates.sh`（Wayback 辅助回溯） |
| 政策追踪 | Live 源 diff（主路径）+ Wayback 快照 diff（辅助）、更新日志、来源映射、月度复查 playbook |

---

## License

MIT
