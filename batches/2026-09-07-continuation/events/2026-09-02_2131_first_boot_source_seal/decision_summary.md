# E10 — 首次 Source promotion 收口与验证成本反身记录

> 2026-09-07 编写的证据导览，不是历史会话原文。

**工程难点**：首次 Source durable promotion 必须在 initializer current0 之后、唯一 supervisor 启动之前；其后 renew/validate current1，失败按已接受状态收尾，不能用删除已持久化 Source 冒充回滚。
**交付变化**：3270719 落实首次 promotion；7831515 增补 capture caller gate；427c758 封存实现、gate/blob 身份及能力边界。
**历史验收**：final-seal.original.md 记录 cold 66.58s、serial Go 699.06s、首启/续启 history 与 M1 rows=0。本批核对原文与 Git 身份，不重跑、不把历史 PASS 改称今日实测 PASS。原文声明临时日志、数据库、跨编译产物已处置，故本批不声称含这些原始运行输出。
**治理反身性**：同一 seal 记录两次 serial Go 耗时占比过半，登记诊断叶；cause=unknown、plan_change=none，最终 serial gate 仍强制执行。这是“发现成本问题并登记诊断”，不是“已经优化提速”。
**能力边界**：seal 明确 M1Unlocked=false。不能将首次 Source 持久化/重启边界的收口改写为北极星本体已全面自主驾驶。
**证据**：两份代码 patch 与 final-seal.original.md；精确来源与校验和见 manifest。
