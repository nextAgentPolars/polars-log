#### 18.28.1 R3 implementation authority retirement

R3 的法源判断仍保留为历史证据，但其 implementation authority 自本节起退役，不得据其继续
实现或验收。独立 implementation review 发现两项结构 blocker：通用 path open 可能跟随 final
symlink，dangling symlink 会被误归 unavailable，FIFO 等特殊叶还可能在 open 阶段阻塞；原 AST
witness 未冻结三个 handle-derived File.Stat、三处 context 顺序及 compare-before-close 的完整
数据流，存在实现错误而 resident proof 假绿的可能。

R4 只替换 candidate material 的平台 open 与对应 witness，不改变已批准 API、主干、错误 owner、
单一 bounded verifier、point-in-time claim 或 successor 边界。Unix 使用 no-follow/nonblocking
directory handle；Windows 使用 reparse-point directory handle。R3 阻断 scratch 只作隔离恢复
材料，不具 authority，R4 seal 后必须坍缩。

