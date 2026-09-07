#### 18.49.10 FirstBoot Source Promotion final implementation seal

当前 seal base、代码验收、全部 gate/blob identity、focus/cold/cross/serial/preflight receipts 与 Sol reviews
均已收齐。本节封存 claim boundary 与 disposal；不改旧文。以下从 seal_id= 到 decision= 的原样文本（末尾含一个
LF）SHA-256 为 d8542fcb7f8fd4df6b356a308c4a53cf39d6eba76c92d72e31e817ddb0c2f0d1：

```text
seal_id=L3.GATEWAY.FIRST_BOOT_SOURCE_PROMOTION.IMPLEMENTATION_SEAL.2026-09-02.R1
seal_base=head=09beb49f5907b72adc7552918c8402c411154b8f;tree=cdf2c3aa78d5205fce65f7ecb3c7bdf7598a9f49;clean=true
code_test_acceptance=head=78315152baa64b83236feb64b7b013d5c52ca459;tree=347e7e9ec1173ebd50b4bbf9e87db13f55de449b
law=commit=1dfac1dea15e7e6fdb40145345102e65b4e99162;tree=a1f7c595e69f213c4bf9d735ba74f1d996e1eb0c
r1_branch_amendment=commit=2375298bea18ed164fed1b86b94d908587516690;tree=2b48547f7f53c9763b278ac46b99aa7baa1088a3;digest=b5c631df1e9a945e93d6fb0623c1b1b7a8e9ffba4ce5f878f603642203337910
r1_implementation=commit=327071960df5366739d3e5ec7c73da41ecb4a77c;tree=b73ba878e0120af836f551d933999493144fc9ce
capture_caller_amendment=commit=f26a1619da1cc0bd76bf64f0b8ea775798141b21;tree=7156a742a06ecdea4f13bb0dc9a32a014542dd7f;digest=07c3fb164e7bc6a2918522365ad3eeabfcf67a4a224e5afd4563c420f721e685
caller_gate_implementation=commit=78315152baa64b83236feb64b7b013d5c52ca459;tree=347e7e9ec1173ebd50b4bbf9e87db13f55de449b
proof_budget_amendment=commit=7525d24d443310027810a7b390f7672b56343c07;tree=ca57bae7394b3381470a5c20bd3e5810d9a21f91;digest=c6faa0a818b86f4e764cc0192a1f01d83a006cea4e23611541defe74c8b29d20
measured_budget_amendment=commit=09beb49f5907b72adc7552918c8402c411154b8f;tree=cdf2c3aa78d5205fce65f7ecb3c7bdf7598a9f49;digest=0c44587dd8b4d42e7437b2576241588b4c5f2f5edd3893e71cca5f26b6bc702c
r1_card_sha256=0a000fc5af5007edaf460cd5270cde224c9495f9fa6d1b0651dacbc7fb65b039
agents_sha256=06775eb5e74c6a030a9a9eb8db8d6aa5274b4ee87f9a076b67322a1bc474e81f
witness.bootstrap_source.go=c31bd7e693014c83df261c3cb1c6bec486a360f1
witness.bootstrap_source_test.go=10207d5c59cba63fe4479cc633a43b68d7fbb9a8
witness.runtime_mount.go=bd917b129259f688db4eaeb903dcedd9669788c9
witness.runtime_mount_test.go=bc4616b6bf9449bc92e95a7db4003e3f569685e8
witness.session_supervisor.go=a9f24c4a6bdb2adf3b1abe2a166e1c2f5f7c1e85
witness.session_supervisor_test.go=4853251f64ff7edc63c51aa511e23ff5ef468509
witness.initial_source_branch_test.go=96fcbd17d620b5157f592ff0450db37fd085f730
witness.bootstrap_capture_test.go=5e924d91824cd4708188c96e0dc71bbe7b50f613
witness.writer_inventory_test.go=1024ef5f1f8f48f1b72240d31b63ef519dae1124
gate.branch=internal/store/sqlite/initial_source_branch_test.go@96fcbd17d620b5157f592ff0450db37fd085f730;amendment=2375298bea18ed164fed1b86b94d908587516690/digest=b5c631df1e9a945e93d6fb0623c1b1b7a8e9ffba4ce5f878f603642203337910
gate.capture=cmd/gateway/bootstrap_capture_test.go@5e924d91824cd4708188c96e0dc71bbe7b50f613+pkg/contracts/intent/v1/writer_inventory_test.go@1024ef5f1f8f48f1b72240d31b63ef519dae1124;amendment=f26a1619da1cc0bd76bf64f0b8ea775798141b21/digest=07c3fb164e7bc6a2918522365ad3eeabfcf67a4a224e5afd4563c420f721e685
identity.input_tree=347e7e9ec1173ebd50b4bbf9e87db13f55de449b;serial_command_sha256=2fc5dc15747531f3329cebef0df49d29e82fa11f4df56f3630f93f28a986ce7f;preflight_command_sha256=de1a93c76ef92af7d1c012e0acb395c9837bb88d1908121ce82f27eef4ba25b0;env_config_sha256=07c260a33d1641587057c173f072e88bb802da41df84018ed2cdafd8e6e2ea35
verification.focused=Gateway PASS wall=1.72s RSS=472055808;SQLite caller PASS wall=.87s RSS=228016128;source packages PASS wall=.39s RSS=127959040;SQLite source authority PASS wall=3.65s RSS=229900288;vet PASS wall=.47s RSS=149340160;latest caller-gate vet PASS wall=.40s RSS=79413248
verification.source_boundary=PASS wall=1.29s RSS=476659712;latest PASS wall=3.51s RSS=481411072
verification.caller=Gateway caller PASS wall=.742s;Intent writer caller PASS wall=1.230s
verification.cold=PASS wall=66.58s RSS=607797248;first history lease/process/heartbeat/runtime=3/1/3/3;second delta=4/1/3/4;final=7/2/6/7;M1 rows=0
verification.instrumented_caller=Gateway PASS wall=5.81s RSS=470777856 children=3;Intent PASS wall=1.02s RSS=214401024 children=3;each children=two unsafe capability go-list plus one full packages.Load go-list;aggregate wall=6.83s maxRSS=470777856 children=6;launcher/wrapper/log/temp deleted
verification.cross=Windows amd64 exact Gateway PASS wall=4.54s RSS=548405248;artifact_sha256=5f9b35623ec512f307f082cb38c950dab33462b0cd672bd9312a22d3e3f9bf71;bytes=42692096;artifact deleted
verification.serial=clean committed go test -p 1 ./... -count=1 -timeout 900s PASS wall=699.06s RSS=1898233856
verification.preflight=head=09beb49f5907b72adc7552918c8402c411154b8f PASS wall=.33s RSS=40452096;status_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
sol_reviews=R1 card independent Sol xhigh PASS;branch/caller/proof-budget/measured-budget L1 reviews PASS;implementation blockers=0
budget.light=wall<=20s,RSS<=512MiB,read/write<=256MiB,network=0,subprocess=0,concurrency=1
budget.caller=each exact gate wall<=10s,RSS<=512MiB,read<=128MiB,write<=256MiB,network=0,subprocess<=3 canonical go list/packages.Load,concurrency=1;aggregate wall<=20s,maxRSS<=512MiB,total_read<=256MiB,total_write<=512MiB,subprocess<=6 serial
budget.heavy=opt-in only;wall<=180s,RSS<=1GiB,IO<=2GiB,network=0,subprocess<=6 only canonical packages.Load,concurrency=1
budget.cross=wall<=120s,RSS<=1GiB,temp<=1GiB,subprocess<=4 serial
budget.serial=wall<=15m,RSS<=2GiB,temp<=4GiB,go-p=1
proof=increment=1;new_dimension=FirstBoot Source durable promotion ordered between initializer current and sole supervisor,with Restart Source writes=0;each L1 gate/budget amendment proof_increment=0
claim=only FirstBoot Source promotion and Restart byte-exact are sealed;Source revision=1;M1Unlocked=false;M1 three tables=0;M1 is the next capability leaf;CLI/Grok later
retain=production,resident Psi_light witnesses,opt-in Psi_heavy witness,existing branch/capture gate deltas,all amendment/card digests and this seal
dispose=cold DB/source/candidate/cross binary/probe/launcher/wrapper/log/output discarded;runtime-mount empty;no overlay/clone/mutation
owner=Gateway mount owns sequencing;SourceMutationOwner owns candidate/q;admitted Store owns Source and Atomic durability;clean serial/preflight mother owns final acceptance
governance_receipt=[治理反身探测] trigger=proof_family_dominance fingerprint=polars/18.49/serial_go/proof_family_dominance evidence=failed_receipt_3270719_wall_702.90s+accepted_receipt_7831515_wall_699.06s;both_over_50_percent cause=unknown candidate=diagnose(serial_go_cost_drivers) plan_change=none disposition=diagnostic_leaf
governance_boundary=the non-blocking diagnostic leaf is registered;the final serial gate remains mandatory and is neither weakened nor deleted
scope_within_epoch=true;safety_not_weakened=true;verification_not_narrowed=true;recovery_defined=true
M1Unlocked=false
decision=sealed
```

治理回执仅登记一条非阻断 diagnostic leaf；最终串行门不弱化。M1 仅称下一 capability leaf，未解锁。
