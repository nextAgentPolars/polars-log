# 续接批次：2026-08-25 → 2026-09-02

这是对既有 polars-log 的**增量证据批次**，不是全量会话续传，也不替换历史记录。

## 覆盖

- 起点：旧归档冻结截止 `2026-08-25T02:26:00+00:00`，提交按 committer 时间严格大于该截止选取。
- 终点：源仓封存提交 `427c7580b19563f9d2a6bf5bec5f776256d71075`，2026-09-02 21:31:44 +08:00。
- `commits.jsonl`：从终点可达、落在上述过滤范围的 **399 条提交元数据**；不是完成任务数，也不是速度/质量评分。
- 三个事件：E08 staged SQL proof、E09 R3/R4 candidate material、E10 first-boot Source seal。
- **未覆盖**：该期间会话原文、全部 worker、用户消息、9 月 3 日之后活动；人工技术干预数量未审计。

## 阅读顺序

1. [E08 分阶段 SQL 证明](events/2026-08-25_1511_staged_sequence_proofs/decision_summary.md)
2. [E09 R3→R4 实现与验证器修正](events/2026-09-01_1039_candidate_material_r4/decision_summary.md)
3. [E10 首启收口与成本反身记录](events/2026-09-02_2131_first_boot_source_seal/decision_summary.md)

每个事件都有时间锚、明确标注的事后导览和原始代码/文档工件。历史治理文档本身是当时的工程记录，**不是原始测试进程输出**。不把摘要、推断和运行事实混为一层。

## 校验与发布边界

`manifest.json` 绑定每个工件的 SHA-256、字节数与来源命令/commit/blob/行区间。
在日志仓库根目录运行：

```sh
python3 -B -m unittest discover -s scripts -p 'test_publication_preflight.py'
python3 -B scripts/publication_preflight.py --expected-head "$(git rev-parse HEAD)"
python3 -B scripts/verify_batch_sources.py --source-repo /path/to/polars --batch batches/2026-09-07-continuation
```

发布前对新增工件做模式扫描与人工源文件审阅。模式扫描不保证发现所有秘密；本批不导出 raw rollout、隐藏推理、内部系统指令、环境转储、用户消息、二进制或数据库。代码 diff 中的治理领域类型/测试不是隐藏推理。

本批未重跑源项目测试、未启动产品、未改动活动源仓；没有宣称竞品差距、同一 OS 进程十天存活或网络中断根因。
