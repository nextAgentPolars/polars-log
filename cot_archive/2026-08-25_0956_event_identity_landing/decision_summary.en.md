# Decision Summary

Commit 2ea90a0: pkg/contracts/controlplane/v1/event_identity.go (236 lines)
+ event_identity_test.go (491 lines).

Contract: ControlPlaneEventV1 carries IntentEpochRef / AttemptRef /
AuthorizationRef plus PayloadDigest, CanonicalDigest, IdempotencyKey. Payload
bytes deliberately not carried — only their strict digest.
ValidateControlPlaneEvent recomputes and rejects any mismatch. Same
idempotency key with different canonical digest = flagged as conflict, never
silently deduplicated.

Same morning, Root enforced three times: blocked a single-positive-green,
froze a 3-file scope, held a release over a 400-line approach and receipt
semantics — waiting on Sol's adversarial audit.
