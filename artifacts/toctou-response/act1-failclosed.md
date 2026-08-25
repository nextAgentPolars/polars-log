# Act 1 — Fail-closed on dynamic SQL(拒绝猜测)

输入:样例含动态拼接 `db.Exec("INSERT INTO demo_users(name) VALUES('" + name + "')")`

命令与完整输出:

```
$ go run ./cmd/receiptharness /private/tmp/receipt-demo/sample
analyze: sqliteinventory: unknown_sql: dynamic string concatenation
exit status 1
```

**没有报告被产出。**分析器拒绝为含未证明 SQL 的代码出具任何收据——
不是"标记 Unknown 继续",而是整场分析拒绝成立。
对应测试:`TestAnalyzeUnknownSQLFailsClosed`(设计行为,非事故)。

这就是"宁要 Unknown 不要假精确"的完全体:Unknown 也不给你,
**要么证明,要么没有**。
