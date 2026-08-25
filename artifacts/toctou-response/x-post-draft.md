# X post draft (one post, two links)

---

Answering the question about state capture between analysis and execution —
with artifacts, not adjectives.

Short answer: **you don't capture mutable state. You make staleness
computable.**

Four things you can check right now:

1. Feed the analyzer dynamic SQL and it refuses to produce a report at all.
   Error: "unknown_sql: dynamic string concatenation". No partials, no
   warnings. The run dies. [gist §1]

2. A real receipt from a clean run: file, line, column, exact SQL text, and
   the semantic fact next to it (ddl / complete). Deterministic — same input,
   byte-identical receipt. [gist §2]

3. Change one line of the source. Every receipt flips to STALE by a sha256
   comparison. Not an investigation — a comparison. The old claim isn't
   patched, it's invalidated. [gist §3]

4. The event identity contract that ties receipts to epochs, attempts, and
   authorization refs — digest-addressed, payload-optional, conflicts flagged
   instead of silently deduplicated. Landed yesterday 09:56, hour 34 of the
   run. [gist §4]

The full 36h chain (105 sessions, 32,821 reasoning entries) exists,
hash-committed. Want a specific slice? DM — hash-verified disclosure.

And if you want to run the mechanism yourself instead of reading about it:
a 250-line toy, clone and go. [repo link]

---
