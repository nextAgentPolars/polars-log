# receipt-demo

A ~250-line Go demo of the **receipt + AST anchor + digest chain + staleness
flip** pattern — the smallest load-bearing wall of the Polaris governance
platform.

This is **NOT the product**. The product is a 230k-line governance platform.
This toy exists so you can run the mechanism yourself in 60 seconds.

# receipt-demo

一个 ~250 行的 Go 演示:**收据 + AST 锚点 + 摘要链 + 失效翻转**模式——
北极星治理平台最小的一面承重墙。

这**不是产品**。产品是一个 23 万行的治理平台。这个玩具的存在,
是为了让你在 60 秒内亲手跑通这个机制。

---

## Run / 运行

```bash
go run . scan testdata     # anchor: scan, emit receipts, append to ledger
# edit testdata/sample.go — change anything
go run . verify testdata   # read-only comparison: anchored vs current
go run . scan testdata     # re-anchor: the new world gets new receipts
```

## What you will see / 你会看到

**Scan** emits one receipt per database call:

```
receipt sample.go:9:2:Exec  op=UNKNOWN  [UNKNOWN: dynamic argument — precision refused]
receipt sample.go:12:2:Exec op=DDL     sql="CREATE TABLE IF NOT EXISTS demo_log(id INTEGER)"
receipt sample.go:16:3:Exec op=DELETE  [DEAD: provably unreachable: inside constant-false branch]
ledger: 3 entries, head=7d364d0d9d87...
```

Three shapes, three treatments:

- **Dynamic argument** → `UNKNOWN`. Precision refused. We do not guess.
- **Constant SQL** → exact receipt with position (`file:line:col`) and full text.
- **`if false` branch** → `DEAD`. Provably unreachable — excluded from claims.

**Verify** after editing the file:

```
STALE  sample.go:12:2:Exec — current source digest 393796... has no matching anchored claim
3 claim(s) invalidated. The old world is gone; re-scan to re-anchor.
```

The old receipts are **not updated** — they were anchored to a source digest
that no longer exists. Staleness is a digest comparison, not an investigation.

**Re-scan** appends new receipts. The ledger chain grows:
`7d364d… → 20b4fb… → …` — append-only, tamper-evident.

## What this demonstrates / 这演示了什么

1. **Decision-time anchoring** — every claim carries the digest of the world it
   was made against (`SourceSHA256`), not a reference to live state.
2. **Fail-closed** — unknown SQL produces `UNKNOWN`, never a guess. Dead code
   produces `DEAD`, never a false claim.
3. **TOCTOU by comparison** — "did the world change?" is a sha256 comparison,
   not an investigation. Changed ⇒ invalidated ⇒ re-anchor.
4. **Append-only ledger** — receipts are never edited or deleted; the chain
   proves order and integrity.

## What this does NOT include / 不包含

The product's analyzer handles closures, aliasing, fixpoint widening,
interprocedural effects, prepared statements, and ~30 more SQL shapes —
with 223 tests and mechanical gates. This toy handles one file and three
shapes. **The pattern is the smallest load-bearing wall; the wall itself
ships separately.**

## License

Apache-2.0 for the demo code. Not licensed for model training without
written permission.
