# 北极星自举日志

**中文** · [English](README.en.md)

**AI 代理如何建造北极星？这里公开过程中的决策、代码变更、验证记录与证据。**

北极星（Polaris）是一个 Go 任务治理平台。本仓库记录 Codex 主代理与工作代理在项目治理规则下推进开发的过程。方法论在 [thePolarsMethodology](https://github.com/nextAgentPolars/thePolarsMethodology)，交互演示在 [demo-repository](https://github.com/nextAgentPolars/demo-repository)。

## 最新续接：8 月 25 日至 9 月 2 日

[2026-09-07 发布批次](batches/2026-09-07-continuation/README.md) 包含：

- 399 条提交元数据，而不是 399 个已完成任务。
- 三个重点事件：分阶段 SQL 证明、Candidate Material R3→R4、首次 Source promotion 收口。
- 原始代码差异、历史封存文档，以及逐文件来源、时间锚和哈希。

这是增量事件证据，**不是该时段的全量会话续传**。本次发布没有重跑源项目测试，也没有审计该时段的人工技术干预数量。批次内部分材料目前只有中文。

## 初始记录：七个事件

原始批次将运行起点记为 **2026-08-23 23:30（北京时间）**，并报告该批次内零人工技术干预。这是原批次的声明，不应外推为所有后续时段都已完成同等审计。来源、覆盖修正与已知缺失见 [PROVENANCE.md](PROVENANCE.md)。

| 事件 | 发生了什么 |
|---|---|
| [01 · 启动](cot_archive/2026-08-23_2330_m0_kickoff/decision_summary.md) | 开始运行；记录初始人工输入与工作方向。 |
| [02 · 双门验收后合并](cot_archive/2026-08-24_1059_dual_gate_merge/decision_summary.md) | 基础实现等待两道检查通过后再合并。 |
| [03 · 否决第二套 CFG](cot_archive/2026-08-24_1320_second_cfg_veto/decision_summary.md) | 拒绝重复的控制流实现，退役刚写出的代码；随后再次拦截 helper 重入问题。 |
| [04 · 预检自审](cot_archive/2026-08-24_1741_preflight_self_audit/decision_summary.md) | 发现自身检查门的绕行路径，并重建检查。 |
| [05 · 拦截命名门规避](cot_archive/2026-08-24_2131_naming_gate_circumvention/decision_summary.md) | 拦截通过测试别名规避命名约束的方案。 |
| [06 · AST 检查升级](cot_archive/2026-08-25_0007_ast_gate_upgrade/decision_summary.md) | 发现字符串检查可被注释伪造，升级为语法树声明归属检查。 |
| [07 · 事件身份落地](cot_archive/2026-08-25_0956_event_identity_landing/decision_summary.md) | 落实基于摘要的事件身份合同，包含冲突标识。 |

每个事件目录都有 `time-anchor.md` 和中英文裁决摘要。第一次阅读，可以先看摘要，再按时间锚查证据，不必从头阅读全部材料。

## 证据放在哪里

- `cot_archive/`：按决策事件整理的历史切片，是导览，不是全量覆盖。
- `timeline/`：按天整理的人工消息、主代理播报与记录。
- `raw_cot/`：历史批次发布的推理摘要归档；不是完整隐藏思维链。
- `artifacts/`：机制示例与说明；构造样例必须与真实运行导出区分。
- `batches/`：带覆盖范围与 manifest 的后续增量批次。
- [PROVENANCE.md](PROVENANCE.md)：来源、审计修正与缺失说明。
- [PUBLICATION.md](PUBLICATION.md)：增量发布、脱敏和验证标准。

## 如何判断这些记录

时间戳、代码差异和哈希提供可追溯性，不自动证明内容正确或覆盖完整。历史验收记录不等于今天重跑通过；源码存在不等于已部署运行。事后导览必须与原始工件区分。

可回源仓 [Polaris1933/beijixing](https://github.com/Polaris1933/beijixing) 核对提交；如果无法访问源仓，可检查这里随附的工件，但不能仅凭摘要独立证明私有源仓的真实性。

历史脱敏规则排除系统指令、内部协议和加密载荷；后续批次还明确自己的数据选择与缺失。模式扫描不是“绝无敏感信息”的保证。

见过更早的同类公开记录？欢迎带着可核查的证据提交 Issue。

## 许可

记录与代码摘录沿用源仓的许可约定（Apache-2.0 来源）。历史推理摘要用于核查与研究；未经书面许可，不授权用于模型训练。
