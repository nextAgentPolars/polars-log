# Act 3 — the world changed

One line edited: `demo_log(id INTEGER)` became `demo_log(id INTEGER, actor TEXT)`.

```
run2 source sha256: 01a9dd87f7504bbe04a4de3f96e39e96
run3 source sha256: 749a1f9e4ca85d649be29afa6fa6c017
```

The run2 receipt claimed: `text: "CREATE TABLE IF NOT EXISTS demo_log(id
INTEGER)"` — anchored to the world where sha was 01a9dd87.

That world is gone. The receipt is **not updated** — it's invalidated. Any
consumer still holding the old receipt does one sha256 comparison and knows.

"Did the state change between analysis and execution?" is not an investigation.
It's a comparison. If the digests differ, the claim doesn't get patched — it
dies, and the system says so instead of moving on with a stale fact.
