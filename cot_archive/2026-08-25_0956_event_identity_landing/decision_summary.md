# 裁决摘要

commit 2ea90a0:pkg/contracts/controlplane/v1/event_identity.go(236 行)+
event_identity_test.go(491 行)。

合同要点:ControlPlaneEventV1 携带 IntentEpochRef / AttemptRef / AuthorizationRef
三引用 + PayloadDigest + CanonicalDigest + IdempotencyKey;payload 字节故意不
携带,只带严格摘要;ValidateControlPlaneEvent 重算不匹配即拒;同幂等键不同
canonical digest = 冲突标记,非静默去重。

同时晨间 Root 三次执法:拦单正例变绿、冻结 3 文件边界、压住不放行(文件逼近
400 行 + 收据语义疑点,等 Sol 反例审计)。
