### 18.29 Candidate Material R4 code seal

#### 18.29.1 Sealed identity

`L3.INITIAL_SOURCE.CANDIDATE_MATERIAL.2026-09-01.R4` 已完成 code seal：

- replacement law：`18cdc1d6739d875c6d38e74a7c7e611b3648047a`
  / tree `0eea86a8ccd5cd25550aaf7fcf1d3893f92cd0e2`；
- code：`02a7c799a54ecf046f5dd5a8bf94bc25623d9eb8`
  / tree `7f9bb6b52b84cfa5e29a898cfca9b3c03bb87a3e`；
- `owner_material.go` SHA-256
  `a11508d312044ef6d09489de900c378ec34347b589fec78c957e17a98dac1c1c`；
- Unix adapter SHA-256
  `040cdd6cc80ad2ebc7352ce3a483bd309d396f0db4cb9ad38d97329c680409ac`；
- Windows adapter SHA-256
  `aa3592b36185b21c7d9b951f28bb91d363147ca28087bef6f13b8cbb4ac8be49`；
- common test SHA-256
  `3f01f65ee7856d59d4d4eae9b10c5a8b97353ee492e79bd538417aabf4ab37e2`；
- Unix test SHA-256
  `9f928e3028073b5f80349f41dd879c0d64405b11ec928c3e4c7445194da067fa`；
- Windows test SHA-256
  `837d615f8888d13f04156219042c5edd4f7b8ebdd21ec0e16b60c41cf1f92cb9`。

实现保持 exact two-field/no-tag `CandidateMaterialV1` 与 read-only Owner method。每个 snapshot
重新执行 `candidateTarget`，以平台 no-follow directory handles 对 root、candidates、candidate
立即 `File.Stat`，围绕唯一一次 `Owner.verifyCandidate` 比较三个物理身份。Unix
`ELOOP/ENOTDIR` 与 handle-derived symlink/type 归 corrupt；普通 IO 归 unavailable；所有
failure 经 `materialFailure` 保证 zero result 与 non-nil error；close failure 以 unavailable
支配且保留 cause。该 proof 只成立于 pre/post 两个 call boundary，不宣称 continuous 或
post-return stability。

独立 Sol xhigh 对 final implementation bytes 完成四轮反例审查；前三轮分别阻断 raced
symlink/type 错误覆盖、AST false-green、平台 flags/raw-handle/FIFO 预算假证明；最终结果为
`VERDICT=PASS`、`BLOCKERS=无`、`REQUIRED_FIX=无`。seal-time isolated caller witness
只发现 method 定义与 tests，production caller exact count 为 `0`。

#### 18.29.2 Verification receipt 与 proof collapse

fresh LocalAccept：

- `go test ./internal/runtime/source -run CandidateMaterial -count=1 -timeout 30s`：PASS；
- existing Candidate/Tree residency：PASS；
- `go vet ./internal/runtime/source`：PASS；
- `TestSourceBoundaryPsiPassesRepository`：PASS；
- serial `internal/runtime/source`：PASS；
- Windows amd64 test binary compile：PASS；artifact 已丢弃；
- `gofmt`、changed-set、diff-check：PASS。

第一次 full serial 不是验收证据：repo-local `tmp/candidate-material-r3-blocked/*.go` 被
`sqliteinventory` 当成 production package typecheck，产生确定性 red。根因是将退役 Go
scratch 误当隔离证明材料；该 scratch 随即按本 card disposition 丢弃。删除后 fresh serial
mother `go test -p 1 ./... -count=1 -timeout 900s` PASS，`576.49s`、最大 RSS
`1678753792B`；随后 clean `make preflight` PASS，`0.43s`、最大 RSS `40370176B`。

```text
proof_increment=1
new_dimension=one durable Restart candidate is bound at call boundaries to one contained no-follow immutable bounded tree without granting Restart
resident=call-time carrier,three platform production files,and API/error/identity/platform/budget tests
stay_reason=removing the no-follow/platform or dataflow witnesses reopens a dimension not detected by the parent verifier
class=Ψ_light
budget=focused<1.1s/source-boundary<3.1s/serial-source<0.3s/Windows-compile<0.7s;serial-mother=576.49s/1678753792B within <=15m/2GiB;network=0;concurrency=1
identity=R4-card-sha+18cdc1d/0eea86a8+02a7c79/7f9bb6b+six-blobs+Sol-PASS+caller-0+clean-serial-mother+preflight
owner=SourceMutationOwner;parent source/full-Go/preflight gates absorb failure
collapse=discarded R2/R3/R4 temp card files,blocked R3 Go scratch,temp candidates,focused output,cross-compile binary,caller probe and process logs;retained only production mechanism,resident Ψ_light and this compact seal
```

本叶没有创建 Gateway caller、Permission、capture、M0/M1、Restart sequence、CLI、schema、
release 或 deploy；`M1Unlocked=false`。后继必须另立 fresh composition exact card，并在同一
lineage 重新确认 durable currentness 与 material，不能把本 call-time carrier 当作权限或
return-time lease。
