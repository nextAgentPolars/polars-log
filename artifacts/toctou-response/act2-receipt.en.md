# Act 2 — a real receipt

Input: one static, reachable SQL statement. Here's the receipt, verbatim from
`act2-receipt.json`:

```json
{
  "id": "demo.store::sample.go::::Upsert[0]@sample.go:9:2:exec",
  "method": "Exec",
  "file": "sample.go",
  "line": 9,
  "column": 2,
  "value": {"kind": "exact", "text": "CREATE TABLE IF NOT EXISTS demo_log(id INTEGER)"},
  "fact": {"operation": "ddl", "target": "t", "tables": ["t"], "complete": true},
  "complete": true
}
```

What the auditor asked for, point by point:

- **source rows at decision time** → `file`, `line`, `column`. Position 9:2.
  Not "somewhere in this file" — file, line, column.
- **not just the SQL the agent generated** → `fact` is the semantic claim
  (ddl, target table, completeness), not an echo of the SQL string. The string
  is right there in `value.text`, and the *claim about it* is right next to it.
- **replayable** → the analyzer is deterministic. Same input, byte-identical
  receipt. Run it twice if you don't believe me.
