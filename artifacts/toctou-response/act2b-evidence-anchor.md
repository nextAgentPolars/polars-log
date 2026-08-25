# 工件 2 — 证据锚定实例(回应 permissions/authorization at decision time)

> 形态:**constructed fixture** — 按生产 schema(`evidence_anchor.go:17-57`)逐字段构造,
> 非运行时库导出(本机无运行时库)。schema 本身可在主仓 `internal/store/sqlite/evidence_anchor.go`
> 核对;字段语义即生产行为。

## 锚定记录(evidence_anchors 一行)

```json
{
  "anchor_id": "anchor_01a02c81_x1b_receipt_a3f2",
  "task_id": "[REDACTED:business]",
  "attempt_id": "attempt_0007",
  "source_kind": "analyzer_receipt",
  "source_ref": "demo.store::sample.go::::Upsert[0]@sample.go:9:2:exec",
  "scope_type": "repo",
  "scope_key": "/workspace/demo",
  "projection_key": "sql.write:demo.store:Upsert",
  "evidence_kind": "sql_write_receipt",
  "digest": "sha256:01a9dd87f7504bbe04a4de3f96e39e96",
  "goal_version": "goal-v3",
  "verification_contract_version": "v1",
  "status": "active",
  "validity": "valid",
  "freshness": "fresh",
  "recheck_path": "rescan:sample.go@attempt_0008",
  "created_at": "2026-08-25T02:20:11Z",
  "updated_at": "2026-08-25T02:20:11Z"
}
```

要点(对照审计者 R2):
- **digest = 决策时源状态**(`sha256:01a9dd87…`,即 Act 3 里 run2 的源文件哈希)——
  权限/证据绑定在"当时的世界上",不绑定在"现在的世界"上;
- **attempt_id 绑定**:此锚只对 attempt_0007 有效;attempt_0008 必须重锚;
- **recheck_path**:失效后的复查路径是字段值,不是口头约定。

## 消费台账(evidence_anchor_consumptions 一行)

```json
{
  "consumption_id": "cons_01a02c81_verify_0042",
  "anchor_id": "anchor_01a02c81_x1b_receipt_a3f2",
  "consumer_phase": "verifying",
  "consumer_id": "psi_source_boundary",
  "result": "consumed",
  "reason": "receipt digest matched workspace snapshot at verify time",
  "consumed_at": "2026-08-25T02:24:40Z"
}
```

要点:**谁在何时消费了哪条证据,有台账**。审计者可以反向追问:
"这个收据被哪些门用过?"——查 consumption 表,不查记忆。

## 失效后的世界(Act 3 联动)

源文件改为 sha256:749a1f9e… 后,同一 anchor 的状态迁移:

```
validity: valid → stale
freshness: fresh → aged
status: active → superseded (by re-anchor at attempt_0008)
```

迁移是 digest 比对的机械结果,不是人工判断。
