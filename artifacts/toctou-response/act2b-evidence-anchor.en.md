# Act 2b — the anchor record

Constructed fixture — same schema as production (see `evidence_anchor.go:17-57`
in the source repo). No live database on this machine, so this is built field
by field against the real schema. Saying so up front.

```json
{
  "anchor_id": "anchor_01a02c81_x1b_receipt_a3f2",
  "attempt_id": "attempt_0007",
  "source_kind": "analyzer_receipt",
  "source_ref": "demo.store::sample.go::::Upsert[0]@sample.go:9:2:exec",
  "evidence_kind": "sql_write_receipt",
  "digest": "sha256:01a9dd87f7504bbe04a4de3f96e39e96",
  "status": "active",
  "validity": "valid",
  "recheck_path": "rescan:sample.go@attempt_0008"
}
```

Three things worth staring at:

- `digest` binds this anchor to the world **as it was** — sha256:01a9dd87…,
  the exact source state at decision time. Not "current state." The world it
  was born in.
- `attempt_id` — this anchor belongs to attempt_0007. Attempt 0008 re-anchors
  from scratch. Old anchors don't get inherited; they get superseded.
- `recheck_path` — what happens when this goes stale is a field value, not a
  promise someone made in a meeting.

And the consumption ledger (who used this evidence, when, in which phase):

```json
{
  "consumer_phase": "verifying",
  "consumer_id": "psi_source_boundary",
  "result": "consumed"
}
```

"Which gates actually consumed this receipt?" is a SELECT, not a memory test.
