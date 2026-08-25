# Act 1 — the analyzer refuses to guess

Fed it dynamic SQL:

```go
db.Exec("INSERT INTO demo_users(name) VALUES('" + name + "')")
```

Complete output:

```
analyze: sqliteinventory: unknown_sql: dynamic string concatenation
exit status 1
```

That's it. No report. No partial results with a warning attached. The whole
analysis refuses to stand up, because one claim in it can't be proven.

This is by design — see `TestAnalyzeUnknownSQLFailsClosed` in the source tree.
The rule isn't "flag unknowns and move on." It's: **either a claim is proven,
or there is no claim.** A report with one unproven line in it is worse than no
report at all, because downstream consumers can't tell which line is the weak
one.

So when people ask "what do you do with SQL you can't prove?" — the answer is:
we don't ship anything. The run dies. The human finds out immediately, not two
weeks later when the audit trail turns out to have a hole in it.
