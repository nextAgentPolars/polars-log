# PROVENANCE / 物证索引

Every artifact in this repo traces to one of three sources. Re-run the commands to verify.

本仓库每件物证都可追溯到以下三个来源之一。命令可自行重跑。

## Source 1: Main session / 主会话

`~/.codex/sessions/2026/08/23/rollout-2026-08-23T10-44-22-01a02c81-3eef-7bf1-90e5-6d3301a2bd90.jsonl`

- Prime broadcasts, human messages, dispatch records
- 79 human messages / 641 prime messages extracted to `timeline/*/human-commands.md` and `prime-broadcasts.md`

## Source 2: Writer-reviewer session / 评审协调会话

`~/.codex/sessions/2026/08/24/rollout-2026-08-24T11-13-14-01a031c2-082f-7302-9411-bc75ba220312.jsonl`

- 1,661 reasoning items, 03:13–09:38 UTC Aug 24
- Walkthrough: `timeline/2026-08-24/E01-second-cfg-veto/cot/cot-walkthrough.md`

## Source 3: Main repo commits / 主仓提交

`github.com/Polaris1933/beijixing`

```
git log --format="%h %ad %s" --date=format:"%H:%M" 675b381^..HEAD
```

Full sequence also in `timeline/commits-all.md`.

## Redaction scan / 脱敏扫描(可自行重跑)

```bash
# credentials / 密钥类(应为空)
grep -rnE "sk-[A-Za-z0-9]{15,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,}\.eyJ|-----BEGIN|gAAAAAB" cot_archive/ --include="*.md"

# system prompts / 内部指令(应为空)
grep -rln "Engram Persistent Memory\|base_instructions" cot_archive/ --include="*.md"

# encrypted payloads / 密文块(应为空)
grep -rln "gAAAAAB" cot_archive/ --include="*.md"
```

Last scan: 2026-08-25, all three clean.

## Known redactions / 已执行脱敏

- `spawn_agent` payloads: encrypted blobs truncated, model identifier retained (public)
- Session `base_instructions` (internal protocol): stripped from all reasoning chains
- No credentials were found in reasoning summaries (scanned, zero hits)

## What is NOT here / 未收录内容

- Summaries written after the fact (including AI-generated analyses) — only verbatim traces
- The writer agents' own sessions (separate rollouts; will be added per-event)
- Full hidden chain-of-thought — OpenAI persists reasoning summaries only; this is noted in every walkthrough

---

## Audit log / 审计日志

### 2026-08-25 — 外部核查发现脱敏残留,当日修复

- 残留:内部协议块 10 处、环境上下文块 4 处(初版扫描模式过窄)
- 修复:硬截止 2026-08-25T02:26:00Z;扫描模式扩至 7 类;重提取净 2,115 条;复检归零
- 计数修正:641→667 差异系源文件为活文件、未声明截止所致,已声明硬截止

---

## 2026-08-25 — 全链条清点(诚实度修正,重要)

外部审计(Kimi)触发全链条排查,发现此前归档**仅覆盖链条的 18%**。
已按冻结截止 `2026-08-25T02:26:00Z` 全量提取并修正:

| 项 | 此前档案声明 | 全链条实测 |
|---|---|---|
| 会话 | 3 个(主脑/评审/写手) | **105 个** |
| 推理条目 | ~5,900(三会话) | **32,821**(全量,脱敏后) |
| 消息 | 79(主会话人类)+ 667(主会话播报) | 1,911(全会话) |
| 工具调用 | 未统计 | 20,708 |

- 全量原始层:`raw_cot/`(104 个会话文件 + `_REGISTRY.md`,逐会话推理全文)
- 此前 `cot_archive/` 七切片定位修正:**不是全记录,是导览路径**——
  覆盖约 18% 的推理链,选择标准是"决策事件",不含其余 82% 的过程推理
- 此前"79 条人类消息"声明修正:那是**主会话**的人类消息;全链条 105 会话
  中的人类消息总量为 1,911 条中的 message 类(含跨会话协调消息)
- 脱敏:全量重扫,零残留(模式同 Kimi 审计后版本)

**本节即为"震惊级诚实"的执行:档案此前自称记录了过程,
实测它只记录了过程的 18%——这个差距本身,现在也是档案的一部分。**

---

## 2026-09-07 — 源仓 Git 证据续接（不是全量会话续传）

新批次位于 [`batches/2026-09-07-continuation`](batches/2026-09-07-continuation/README.md)。

- 冻结源端：`427c7580b19563f9d2a6bf5bec5f776256d71075`，2026-09-02 21:31:44 +08:00；提取只读已提交 Git 对象，不依赖活动工作区或当前 HEAD。
- 提交索引：终点可达且 committer 时间严格晚于旧冻结截止 `2026-08-25T02:26:00Z` 的 399 条提交。提交时间不是会话时间，数量不是完成任务或质量评分。
- 三个导览事件：staged SQL proofs、Candidate Material R3→R4、FirstBoot Source promotion seal。
- `*.patch` 是精确 Git diff；`*.original.md` 是指定 commit/blob/行区间的逐字提取；`time-anchor.md`、`decision_summary.md`、批次 README 是 **2026-09-07 事后编写的导航**。旧文“没有事后摘要”不适用于这些明确标注的导航文件。
- 历史 seal 记录的 PASS/耗时属于历史文档声明；本轮仅重算来源和工件身份，未重跑源项目测试。原文已声明处置的临时测试日志/数据库不在本批。
- 会话原文、用户消息、隐藏推理、内部协议、二进制和数据库均不导出。人工技术干预为 unknown；不能把旧批次的零干预声明外推到本批。
- 新批次各文件的摘要、字节数与提取来源见 `manifest.json`；通过 `scripts/verify_batch_sources.py` 可从持有的源仓对象重现。若源仓访问受限，公开读者仍可检查随附工件与 manifest，但不能仅靠摘要独立证明私有源仓的真实性。
- 脱敏按新增工件全量扫描，并审阅来源与字段范围；历史归档此次未重扫、未改写。哈希只用于身份/一致性，不证明内容无误或记录完备。
