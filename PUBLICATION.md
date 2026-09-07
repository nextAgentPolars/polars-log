# 增量发布标准 / Incremental publication standard

保留既有日志的时间锚、事件切片、代码差异、来源索引与脱敏原则；后续增量必须明确自己的边界，不继承未经重新验证的历史断言。

1. **冻结来源**：Git 证据使用完整 commit/tree/blob；会话证据若另行发布，必须声明固定截止、源文件身份、覆盖和缺失，不读取活文件后宣称完整。
2. **原文与导航分开**：逐字提取给出行范围与 SHA-256；新写摘要标明编写日期和事后性质。不得制造、补写或发布隐藏思维链。
3. **能力主张分级**：源码存在、历史验收记录、本次重演、生产运行是不同等级；历史 PASS 不能变成本次测试结果。未知干预、未知原因和未完成诊断保持 unknown。
4. **不自动发布原始日志**：排除内部系统指令、凭证、原始环境、数据库和无关私人数据。扫描只报告位置/类别，不输出命中的秘密。模式扫描之外仍须审阅来源和字段范围。
5. **不可变批次**：每批 `manifest.json` 列尽工件并绑定来源。既有批次发布后不原地修订；更正另加批次并声明 supersedes/修正范围。
6. **发布前门禁**：源工件重现、预检负例测试、提交字节/哈希检查通过后，固定待发布 HEAD/tree。只提交本批明确文件，排除他人草稿。push 前核对远端基线，使用普通 fast-forward push；远端变动则停下重审。
7. **发布后回执**：确认目标为 `nextAgentPolars/polars-log` 且远端 main 与已验收 HEAD 一致；不因本机 commit 成功就宣称已上传。

```sh
python3 -B -m unittest discover -s scripts -p 'test_publication_preflight.py'
python3 -B scripts/verify_batch_sources.py --source-repo /path/to/polars --batch batches/2026-09-07-continuation
python3 -B scripts/publication_preflight.py --expected-head "$(git rev-parse HEAD)"
```

预检只校验已提交的增量批次，不追认旧归档安全，不验证源项目运行行为。不得使用 Python 优化模式运行这些基于断言的检查。
