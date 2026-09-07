# E09 — 不仅修实现，还修验证器：Candidate Material R3 → R4

> 2026-09-07 编写的证据导览，不是历史会话原文。

**为什么进化**：历史 R3 retirement 原文指出，通用 path open 可跟随末端 symlink 或在 FIFO 阻塞，旧 AST witness 又未冻结 File.Stat/context/compare-before-close 的完整数据流，可能出现错误实现和验证假绿。
**进化了什么**：R3 实现权限退役；R4 使用平台 no-follow directory handles，并加强物理身份、生命周期、平台 flags 与反例 witness；既有 API 与授权边界不扩张。
**进化后能做什么**：把唯一 bounded verifier 的前后观察绑定到 handle-derived 的 root/candidates/candidate 身份，覆盖 FIFO/symlink 等失败路径。
**历史审查记录**：code-seal.original.md 记录四轮实施反例审查，前三轮阻断错误覆盖、AST false-green、平台证明问题；这是源仓历史声明，不是本次独立重演。
**证据**：r3-retirement.original.md → diff/02a7c79.patch → code-seal.original.md；manifest 给出精确提交、blob、行区间和摘要。
**边界**：只证明两个调用边界的 point-in-time identity；不证明连续或返回后的稳定性，不授予 Restart/写入权限。Windows 编译记录不等于 Windows 行为实测。本批不重跑测试。
