# polaris-bootstrap-log

A public, evidence-first record of an AI system building itself.

This repository documents **Polaris** (北极星) — a Go task-governance platform — during a zero-human-intervention development run that started 2026-08-23 23:30 CST. A Codex-based "Prime" agent scheduled parallel worker agents ("luna"), reviewed every line, and ran under a frozen constitution (`AGENTS.md`, 860 lines) plus 44 mechanical invariant gates.

No narratives here. Only: timestamps, verbatim reasoning traces, gate outputs, code at decision time, and commit hashes. Every claim can be checked against the source repo at `github.com/Polaris1933/beijixing`.

**Found something earlier that looks like this? Public evidence welcome. Open invitation.**

---

# 北极星自举日志

一个公开的、证据优先的仓库,记录一个 AI 系统建造自己的过程。

记录对象:北极星(Polaris),Go 任务治理平台。运行起点 2026-08-23 23:30(北京时间),Codex 基座的主脑调度并行 luna 写手,在冻结宪法(860 行 AGENTS.md)与 44 个机械不变量门下工作,全程零人工技术干预。

这里没有叙事。只有:时间戳、逐字推理链、门输出、决策时刻的代码、commit hash。每条声明都可以回主仓 `github.com/Polaris1933/beijixing` 核对。

**如果你见过更早的同类公开记录,欢迎提交——这是公开邀请,不是修辞。**

---

## Structure / 结构

```
cot_archive/            按决策事件切片(主发布物)
  <date>_<hhmm>_<event>/
    time-anchor.md          时间锚:会话/时刻/前置状态/触发事件
    reasoning_chain.md      原始推理与消息流(逐条,未删改)
    decision_summary.md     裁决摘要(中文)
    decision_summary.en.md  裁决摘要(英文)
    diff/                   对应代码变更
timeline/                   按天的人类消息、主脑播报、日记录(原始层)
```

## Reading order / 阅读顺序

First time? Read the slices in order. Each `time-anchor.md` gives you enough context to jump in cold — you don't need all 36 hours.

第一次读?按顺序读切片。每个 `time-anchor.md` 自带上下文,可以从任意切片冷启动,不需要读完全部 36 小时。

## The seven slices / 七个切片

| # | Slice | What happened |
|---|---|---|
| 1 | `2026-08-23_2330_m0_kickoff` | Run starts. Five human sentences, zero technical directives. |
| 2 | `2026-08-24_1059_dual_gate_merge` | Overnight foundation merges: 7 commits, +27k lines, held until dual-gates green. |
| 3 | `2026-08-24_1320_second_cfg_veto` | **The main event.** Agent proposes a parallel CFG. Constitution vetoes it. Agent retires its own fresh code in 8 minutes. Second interception 21 min later. |
| 4 | `2026-08-24_1741_preflight_self_audit` | System finds 3 bypasses in its own enforcement gate. Refuses happy-path green. Rebuilds the gate. |
| 5 | `2026-08-24_2131_naming_gate_circumvention` | Writer tries dodging the naming gate with test aliases. Blocked — evasion itself intercepted. |
| 6 | `2026-08-25_0007_ast_gate_upgrade` | System discovers its own structure test was forgeable by comments. Hardens to AST-level. |
| 7 | `2026-08-25_0956_event_identity_landing` | Event identity contract lands: digest-addressed, payload-optional, conflict-flagging. The TOCTOU answer. |

## Redaction rules / 脱敏规则

- Stripped: system prompts, internal protocol blocks, encrypted inter-agent payloads
- Kept: model identifiers (public), local paths (already public in commits), human messages (verbatim — including the blunt ones)
- Scan commands included in `PROVENANCE.md`; re-run them yourself

## License / 许可证

Records and code excerpts: follows the source repo (Apache-2.0 lineage). Reasoning traces: published for verification and study. **Not licensed for model training without written permission.** / 记录与代码摘录随源仓许可证;推理链供核查与研究使用,**未经书面许可不授权用于模型训练**。
