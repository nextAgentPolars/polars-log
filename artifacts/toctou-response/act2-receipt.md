# Act 2 — 真实收据:决策时刻的源码行(回应 source rows at decision time)

输入:静态可达 SQL 一条(`CREATE TABLE IF NOT EXISTS demo_log(id INTEGER)`)

分析器产出的收据(逐字,来自 act2-receipt.json):

```json
{
  "id": "demo.store::sample.go::::Upsert[0]@sample.go:9:2:exec",
  "method": "Exec",
  "file": "sample.go",
  "line": 9,
  "column": 2,
  "value": {"kind": "exact", "text": "CREATE TABLE IF NOT EXISTS demo_log(id INTEGER)"},
  "fact": {
    "operation": "ddl",
    "target": "t",
    "tables": ["t"],
    "complete": true
  },
  "complete": true
}
```

审计者要的三样:
- **source rows at decision time** → `file/line/column` = sample.go:9:2(精确到列)
- **not just the SQL generated** → `fact` 是语义事实(operation/tables/complete),
  不是 SQL 文本的复述
- **可重放** → 同一输入重跑,同一收据逐字节重现(分析器确定性)
