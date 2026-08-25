# 2026-08-23 — 主脑播报全文

## 11:31

完成：项目已拉到 `/Volumes/移动硬盘/polars`。  
已隔离 HOSRookie SSH 身份，`origin` 为 SSH；验证通过。GitHub 主机指纹已按[官方文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)校验。

## 11:34

## 北极星首轮全景研究

**代码状态**：`main` / `1aadfec`，工作树干净；1,615 文件、1,176 Go、145 TS/TSX、274 个 Go 测试文件。

**架构主干**
- Gateway：HTTP/SSE、队列、收敛、监督、安全/记忆修复。
- Runner：gRPC 执行、隔离 workspace、补丁与结果回传。
- `application/tasks`：任务入口→计划→执行→验证→审查→修复→续接。
- SQLite：任务、计划、执行、授权、记忆、控制面 ledger 的持久化真相。
- Electron/React：只读 Gateway 投影，不是事实写入方。

**安全与发布**
- 默认监听 `127.0.0.1:8080`；网络决策缺失时 fail-closed。
- 凭证加密依赖 `POLARIS_ENCRYPTION_KEY`；未配置时不能宣称加密。
- 发布要求 Linux/Windows 包装 smoke、长 soak、可观测性证据、release-evidence bundle；macOS 包装证据当前明确不支持。
- 控制面 ledger 与 GlobalCommit 已落地；尚未宣称独立、长期存储的 Omega 服务。

**当前问题（已复现）**
1. `python3 -m unittest discover ...`：149 项中 3 项失败。  
2. 可观测性测试依赖 `go run` 校验器；本机没有 Go，因此被正确阻断。  
3. 两个 failure-sample 文档锚点已漂移：  
   - `runtime_gate_test.go:217` 为空行；  
   - 前端断连样例仍指向旧测试行号，未命中 fail-closed 断言。  

**验证边界**
- 此机无 Go、无桌面 `node_modules`，且项目规定的 WSL 工作区与环境文件不存在；因此 Go 全量门、桌面门、运行态/包装门均未执行，不能据此作“通过”结论。  
- 已完成只读架构、入口、契约、存储、CI、发布、安全和脚本测试审计；未修改任何源码。

## 11:36

明白：只以当前代码、测试、运行结果为证据；文档只作导航。Go、模块缓存、构建缓存和临时目录都放移动硬盘，不改全局配置；删除该工具链目录即可回退。

## 11:38

依赖下载仍在推进：模块缓存已增长到 94MB，当前未卡死；完成后立即跑代码测试门。

## 11:42

Go 基础门已真实运行：发现两处失败，不是文档结论。一个是本机代理 DNS 把 `.invalid` 映射成假 IP；另一个是 RFC3339Nano 文本排序导致租约时间偶发倒序。继续补齐外置 lint 工具。

## 11:44

lint 工具正在首次下载其分析器依赖；所有内容仍写入移动硬盘的模块缓存，尚未触碰仓库或用户目录。

## 11:50

已按**实际源码、配置和测试**研究，不采信文档自述，也未修改项目代码。

### Go 环境

全部位于移动硬盘：

`/Volumes/移动硬盘/polars-toolchain`

- Go 1.24.13 darwin/arm64
- golangci-lint v2.1.0
- SDK、GOPATH、模块/构建/lint 缓存、临时目录、HOME、Telemetry 均在外置盘
- Go Telemetry 已关闭
- 本轮误生成的内盘 Telemetry 已精确清除，复测未再生成
- 未修改全局 Shell 配置

使用：

`source /Volumes/移动硬盘/polars-toolchain/env.sh`

安装包 SHA256 已与 [Go 官方下载页](https://go.dev/dl/)一致。

### 实际项目结构

源码盘点：

- 1,615 个跟踪文件
- 1,176 个 Go 文件
- 274 个 Go 测试文件
- 92 个 Go 包
- 145 个 TS/TSX 文件

实际运行结构是：

- Gateway：HTTP、SSE、任务调度、授权、模型、记忆、安全及连接器
- Runner：通过 gRPC 接收任务，管理工作区、补丁、浏览器和执行状态
- SQLite：核心持久化与队列
- React/Electron：桌面控制台，只通过 Gateway 合同读取状态
- 飞书、GitHub、Telegram及通用 Webhook 接入

### 当前真实质量状态

- Source-boundary 门禁：**通过**
- 完整 Go 测试：**两项失败**
  1. 本机 fake-IP DNS 将 `.invalid` 域名解析成 `198.18.0.128`，属于测试不隔离系统解析器。
  2. SQLite 使用变长 RFC3339Nano 文本比较时间，字典序可能颠倒真实先后；这是实际实现缺陷。
- golangci-lint：**一项失败**，为重复无效赋值。
- Python：149 项中 **2 项失败**，都是源码证据行号已经过期。
- 前端依赖尚未安装，因此前端测试尚未验证。
- 仓库仍为 clean，HEAD：`1aadfec03595e41cce12d0cfa25bbc0cb31bce69`
- 项目专属 Git 身份已配置。

我没有把“完整测试跑过”冒充“逐行审计完毕”，也不会未经授权直接修这些问题。

## 11:51

从实际代码看，**北极星是一个 AI 研发任务编排与执行平台**，不是普通聊天机器人。

它的工作链路是：

1. 用户从桌面端、飞书、Telegram等入口提出需求  
2. 系统整理需求，建立项目、任务、计划和待办  
3. 调用不同 AI Provider 进行规划、执行、审查  
4. Runner 在隔离工作区修改文件、执行测试或浏览器任务  
5. 高风险操作进入人工授权  
6. 最终保存执行证据、故障诊断、上下文和记忆

核心组成：

- **Gateway**：中央控制面和 HTTP API
- **Runner**：实际执行任务的节点
- **SQLite**：任务、授权、记忆和运行状态的事实库
- **React/Electron**：桌面工作台
- **连接器**：飞书、GitHub、Telegram、Webhook
- **治理系统**：安全、可观测性、失败恢复、人工介入

简单说，它想做的是：

> 把“向 AI 提需求”升级为一套可计划、可执行、可审查、可恢复、可追踪的自动化研发系统。

目前代码规模和功能面已经很大，但仍处于持续建设状态：后端测试还有两个失败点，前端尚未完成本机验证，因此现在不能认定为稳定可发布产品。

## 11:52

**差异很大，但“产品差异大”不等于“竞争壁垒已经大”。**

北极星最大的区别不是更会写代码，而是它想成为一套 **Agent 控制平面/研发操作系统**。

| 产品 | 主要定位 |
|---|---|
| Claude Code | 在终端里与单个代码 Agent 协作、执行命令和修改代码。[Anthropic](https://docs.anthropic.com/en/docs/claude-code/cli-usage) |
| Cursor | IDE 辅助开发，并提供运行在远程隔离机器上的后台 Agent。[Cursor](https://docs.cursor.com/background-agent) |
| GitHub Copilot | IDE/GitHub 内问答、规划、修改代码并创建 PR。[GitHub](https://docs.github.com/en/copilot/get-started/what-is-github-copilot) |
| Devin | 云端“AI 软件工程师”，具备 IDE、终端、浏览器，主要承接范围明确的工程任务。[Devin](https://docs.devin.ai/get-started/devin-intro) |
| Codex | 本地与云端协作，支持多 Agent、独立 worktree及长任务管理。[OpenAI](https://openai.com/index/introducing-the-codex-app/) |
| **北极星** | 管理需求、项目、Agent、模型、任务执行、人工授权、证据、记忆、恢复和持续运行。 |

### 北极星真正特殊的地方

1. **不是绑定一个模型**  
   它把模型看成可配置资源，可以给规划、执行、审查等角色分别绑定 Provider。

2. **任务不是一次性聊天**  
   需求会沉淀为项目、任务、Mission、Todo、执行记录和状态，而不是对话结束就消失。

3. **控制面与执行面分离**  
   Gateway 管理事实和调度，Runner 负责实际执行，可以扩展为多个执行节点。

4. **治理比写代码更重**  
   内建人工授权、安全许可、失败恢复、运行证据、诊断、记忆治理和状态收敛。

5. **入口不限于 IDE**  
   桌面端、飞书、Telegram、GitHub、Webhook都可以成为任务入口。

### 但它还没有形成明显壁垒

当前 Codex已经支持多 Agent 和 worktree；Devin有长期会话、API和团队集成；Cursor也有远程后台 Agent。因此“多 Agent、能执行代码”已经不是稀缺能力。

北极星要形成壁垒，必须证明三件事：

- 跨天、跨项目任务状态确实不会乱；
- 多 Agent协作比直接使用 Codex/Claude Code更可靠；
- 授权、恢复、证据链能真实降低生产事故。

**结论：**

- 与 Claude Code、Cursor相比：定位差异很大。
- 与 Codex、Devin相比：方向差异中等，能力重叠明显。
- 当前阶段：架构野心很大，但成熟度和真实闭环证据还不足。

一句话概括：

> 别人在造更强的“AI 程序员”，北极星想造“管理一群 AI 程序员的研发操作系统”。

## 12:05

对，我前面说“研发操作系统”还停留在外形。看完实际代码后，更准确的定义是：

> **北极星是一个 Agent 交付控制平面与状态收敛内核。**  
> 它不是主要让模型更聪明，而是把模型不稳定的一次性输出，变成**可治理、可验证、可恢复、可追责、可积累**的工程状态。

## 一、它的记忆不是“长上下文”，而是经验治理系统

当前实现不是典型向量库/RAG。核心价值不是“记得多”，而是：

> **决定哪条经验有资格影响下一次执行。**

完整链路是：

```text
任务/评审/对话产生经验
        ↓
MemoryCandidate 候选隔离
        ↓
范围规则 + 治理策略 + 证据 + 审批人数
        ↓
accepted / rejected / superseded
        ↓
版本化 MemoryEntry
        ↓
按仓库、角色、阶段、任务类型、具体对象匹配
        ↓
valid / suspect / stale 判定
        ↓
只能作为 advisory 建议进入执行
        ↓
记录命中；写入失败进入 repair 队列
```

### 1. 记忆先进入隔离区

任务结束不会直接污染长期经验，而是先生成候选：

- 来源、任务、attempt
- selector
- proposal
- report、review、verification 等证据
- draft/pending/approved 状态

见 `internal/application/memory/handlers.go:36-84`。

### 2. 记忆需要治理，不是模型自己说了算

它支持：

- accept、reject、discard、escalate
- supersede 旧版本
- scope allow/block/observe
- 分类策略
- 审批 quorum
- 指定 reviewer role
- 必需证据类型
- 不同审批人计数

因此“Agent 总结了一条经验”与“系统允许以后使用这条经验”是两件事。

### 3. 召回不是关键词碰撞，而是运行上下文匹配

匹配维度包括：

- repo、task type
- provider、role、phase
- file/module/component/route 等目标对象
- metadata、evidence digest

对象级经验优先于全局经验，并进行确定性排序与合并。

随后还要检查：

- 30 天内：valid
- 30–90 天：suspect
- 超过 90 天：stale
- 依赖是否断裂
- 当前 workspace/repo digest 是否仍与当时证据一致

见 `memory/validity.go:19-138`。

### 4. 最重要的安全设计：记忆永远没有最终裁决权

正式 MemoryIndex 合同强制要求：

- 必须是 `accepted`
- 必须是 `valid`
- `usage_mode=advisory`
- `advisory_only=true`

见 `pkg/contracts/memoryindex/v1/types.go:68-147`。

也就是说：

> 记忆可以提醒 Agent，但不能覆盖当前代码、验证结果和运行时事实。

这正是它比简单“把历史对话塞回提示词”稳定的地方。

### 5. 记忆系统自身也支持降级和

## 12:15

对，这才是北极星真正的理论核心：

> **概率性生成，确定性验收，形式化迁移。**

可以表达为：

\[
O_t \sim P(\cdot \mid Input)
\]

LLM 只产生不可信候选 \(O_t\)。控制平面计算：

\[
A_t = Gate(S_t, O_t, E_t, Policy)
\]

只有当 \(A_t=accept\) 时：

\[
S_{t+1}=\delta(S_t,O_t)
\]

否则只能进入：

```text
reject / hold / retry / rollback / escalate
```

其中 `Gate` 和状态转移函数 `δ` 必须是确定性的、可重放的。

### 因而系统能证明什么

它不能证明“LLM 的答案绝对正确”，但可以证明：

- 输出属于当前 task/attempt；
- 前置状态允许这次迁移；
- 指定验证已经执行；
- 证据没有过期；
- workspace 没在验证后变化；
- review、策略和权限条件满足；
- 状态迁移符合预定义图；
- 相同输入和证据可以重放出相同结论。

所以准确说是：

> **证明这次状态迁移相对于既定合同是合法的，而不是证明世界层面的绝对正确。**

记忆系统也是同一原则：

```text
LLM 总结的经验
→ 不可信 Candidate
→ 证据与治理审批
→ Accepted Entry
→ 仍然只能 Advisory
→ 不能直接推进任务状态
```

因此北极星最核心的架构分离是：

> **把“生成内容的能力”交给概率模型，把“是否接受内容、是否推进状态”的权力留给确定性系统。**

这比“多 Agent”“长期记忆”“自动写代码”都更接近它的本质。

## 12:16

LLM outputs are inherently probabilistic and therefore cannot be trusted by default. But the decision to accept an output and advance the task to the next state can be deterministic—and formally verifiable.

## 12:29

我把实际代码还原后，结论很明确：

> **它做的不是普通“意图分类”，而是意图编译与准入。**  
> 设计思想非常好，但当前语义模型还没有达到这套思想应有的严谨程度。

## 一、当前已经实现的意图模型

实际上存在三套相互连接、但尚未统一的模型。

### 1. ChatEntry：从话语识别到任务提交

```text
MessageEnvelope
    ↓ 持久化 InputLedger
LowCostRoute
    ↓
IntentJoinery
    ├─ LanguageFunction
    ├─ Surface
    ├─ PenetrationDepth
    └─ Action
    ↓
IntentCandidateLifecycle
    ↓
MinimumWorkflowLeaf
    ↓
S12 只生成叶子结果
    ↓
S13 独占任务提交权
```

#### 第一层：低成本路由

分类为：

```text
empty
ordinary
status
cancel
repeat
memory_store
memory_recall
unsupported
frustration
material
```

对应 `route_low_cost.go`。

它回答的是：

> 这句话是否值得进入任务意图处理？

#### 第二层：IntentJoinery 四元组

每条受控消息被建模成：

\[
J=(LanguageFunction,\ Surface,\ Depth,\ Action)
\]

其中：

**LanguageFunction**

```text
identity_only
pure_affective
knowledge_question
exploratory_ambition
weak_action_signal
strong_action_request
```

**Surface**

```text
chat_only
answer_only
advisory_only
intent_candidate_private
contract_draft
promotion_request
```

**Depth**

```text
chat
answer
advisory
candidate
task_trunk
```

**Action**

```text
reply
answer
advise
clarify
reject
promote
```

见 `internal/application/chatentry/intent_joinery.go:63-158`。

它想表达的不是“用户在说什么主题”，而是：

> **这句话最多允许穿透到系统的哪一层。**

这是很好的设计意图。

#### 第三层：意图候选生命周期

弱意图不会直接创建任务，而是进入：

```text
candidate_pending
    ↓ 补充信息
candidate_clarifying
    ↓ 契约完整
candidate_confirmed
    ↓ 用户显式 confirm
promoted_to_task_trunk
```

旁路状态还有：

```text
expired
rebased
quarantined
rejected
```

候选绑定：

- session、sender
- input ledger
- intent de

## 12:39

**符合，而且比“做一个更准的意图分类器”更符合这个项目。**

但要重新定义目标：

> 北极星不应该证明“系统绝对理解了用户意图”，而应该证明：  
> **本次状态迁移没有超出当前已被接受的用户意图。**

这才与项目“概率性生成、确定性验收”的理念完全一致。

---

# 一、意图系统在北极星里的正确位置

它不应该只是 ChatEntry 前面的一个分类器，而应该成为任务系统的**规格根节点**：

```text
用户原始表达
    ↓
IntentDeltaProposal（LLM，可不可信）
    ↓
证据锚点、冲突检查、权限检查
    ↓
AcceptedIntentDelta（确定性接收）
    ↓
Versioned IntentState
    ↓
TaskContract Candidate
    ↓
任务准入
    ↓
Plan / Execution / Verification
    ↓
IntentFulfillment Witness
```

形式上：

\[
I_{t+1}=Reduce(I_t,\ Accept(\Delta I_t,E,Policy))
\]

其中：

- LLM 只能提出 `ΔI`；
- `Accept` 决定这个增量是否有资格进入正式意图；
- `Reduce` 是确定性的；
- Task 只是某个 IntentState 的执行投影。

---

# 二、最关键的边界：不要让“意图”吞掉其他真相域

当前设计有把意图、能力、权限、风险、任务类型揉在一起的倾向。

更符合北极星哲学的做法，是明确真相所有者：

| 真相域 | 所有者 |
|---|---|
| 用户目标、偏好、禁止事项 | 用户 |
| 语义解释候选 | LLM |
| 正式 IntentState | Intent Control Plane |
| 能力是否存在 | Runtime/Capability Plane |
| 操作是否允许 | Policy/Governance Plane |
| 工作区当前状态 | Runtime Truth |
| 是否完成 | Verification Authority |
| 历史经验 | Memory Advisory |

因此：

> “用户想让我打开网页”不等于“浏览器能力存在”，也不等于“允许执行”。

Admission 应该是多个真相域的交集，而不是意图分类器一个字段决定。

---

# 三、最值得打开思维的点：不要选唯一意图，保留候选集合

LLM 无法可靠地给出唯一正确语义，可以输出：

```text
PossibleIntents:
1. 知识问答：解释“修复”的含义
2. 代码任务：修复某个问题
```

然后把每个解释投影为操作效果：

```text
Effect(I1) = answer_only
Effect(I2) = repo_write
```

如果候选效果不同，就不能自动进入写操作。

可以定义：

\[
SafeEffect=\bigcap Effect(I_k)
\]

### 例子

用户说：

> 帮我分析一下登录模块

可能解释为：

- 给出概念分析；
- 读取代码后分析；
- 修改登录代码。

共同安全效果只有：

```text
read_only_analysis
```

因此系统可以先走只读分析，而不是必须“猜中唯一意图”。

这与北极星的 Minimum Leaf 原则天然一致：

>

## 12:47

**会不会麻烦，取决于是否把“控制平面”暴露给用户。**

## 结论

- **现在的 Polaris：还不能媲美 Claude Code / Codex。**
- **按前面的方向重构后：有机会在长期意图稳定性上超过它们。**
- 但如果每次识别到歧义都让用户确认，最终会变成一个**安全但烦人的审批系统**。

前一轮代码探针已经暴露出当前问题：  
“只分析、不要改代码”仍可能进入修改路径；旧合同还可能吞掉用户的新修正。这说明目前连基础自然度都未稳定。

## 用户不应看到复杂模型

内部可以有：

- 候选意图
- IntentState 版本
- 禁止项
- Effect Set
- Coverage Witness
- Fulfillment Witness

但用户只应该感知三种状态：

1. **我理解了，正在做**
2. **我完成了，这是证据**
3. **这里存在一个会改变结果的关键分歧，请你决定**

绝不能让用户回答：

> 请选择 intent class、runtime form、confirmation state……

那会直接输给 Claude Code 和 Codex。

## 什么时候才应该问用户

| 情况 | 用户体验 |
|---|---|
| 多种理解最终都会导向同一个安全动作 | 不问，直接做 |
| 阅读、分析、解释、搜索代码 | 不问 |
| 明确要求修改仓库内代码并测试 | 通常不问 |
| 两种理解会导致不同文件或不同交付物 | 只问一个关键问题 |
| 删除、发布、付款、外部写入、权限扩大 | 必须确认 |
| 用户中途说“不要改了，只分析” | 立即停止受影响动作并重基，不要求重述全部需求 |

核心原则是：

> **不要因为语义不确定而提问；只有这种不确定性会造成不同的实质效果时才提问。**

这与 OpenAI 当前公开建议一致：安全、范围内的本地操作应连续完成，只在外部写入、破坏性、付费或实质扩大范围时确认。[OpenAI Model Guidance](https://developers.openai.com/api/docs/guides/latest-model)  
Claude Code 同样把交互摩擦放在权限模式上，而不是要求用户逐层确认语义。[Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)

## 能否媲美 Claude Code / Codex

必须分成两种能力：

### 1. 第一反应的自然理解

Claude Code、Codex 依靠强模型和丰富上下文，这方面优势很大。  
如果 Polaris 继续依赖关键词和硬分类，**很难媲美**。

正确路线必须是：

> LLM 生成多个语义候选；确定性内核只裁决哪些效果可以被接受。

不是让规则系统代替模型理解语言。

### 2. 长任务中的意图守恒

这里反而是 Polaris 最有机会超越它们的地方：

- 用户纠正后，旧计划自动失效
- “不要改数据库”不会在十轮以后丢失
- 执行计划必须证明覆盖目标且没有越权
- 完成必须证明满足的是用户接受过的意图版本
- 恢复任务时不会靠模型“回忆大概意思”

Claude Code/Codex 可能更像一个理解力很强的人；Polaris 可以变成：

> **理解力来自模型，但承诺、边界和交付不会依赖模型记性。**

## 真正的验收标

## 12:51

# Polaris：设计语言与当前成果总览

> 当前证据：`main@1aadfec`，与 `origin/main` 一致，工作树干净。以下区分**已经实现**与**尚待落地的统一设计**。

## 一、项目的一句话定义

> **Polaris 是面向长期复杂任务的“意图守恒、证据驱动、可恢复收敛控制平面”。**

它不追求让 LLM 永远理解正确，而是保证：

> **概率模型可以提出建议，但只有经过确定性裁决的结果，才能改变系统真相。**

英文产品语言可表达为：

> **An intent-preserving, evidence-driven convergence control plane for long-horizon agentic work.**

---

# 二、统一设计语言

## 1. Governing Thesis：治理命题

用户此前提出的那句话，就是整个系统最核心的设计命题：

> **LLM outputs are probabilistic and untrusted, but whether a task should accept an output and transition state can be deterministic and formally verifiable.**

对应系统原则：

```text
Model proposes.
Policy admits.
State machine transitions.
Evidence verifies.
Memory advises.
The user remains the semantic authority.
```

---

## 2. 八个核心术语

| 设计语言 | 含义 |
|---|---|
| **Root-Owned Truth** | 每类真相只有一个根所有者，LLM 无权直接修改 |
| **Intent Conservation** | 用户目标、禁令和验收条件在长任务中不能漂移 |
| **Intent Delta** | 每句话是对既有意图状态的增删改，而不是重新分类 |
| **Semantic Convergence** | 多种理解逐渐收敛到效果等价的安全行动 |
| **Minimum Authorized Effect** | 只执行所有合法理解共同允许的最小效果 |
| **Deterministic Admission** | 是否接收模型输出由确定性合同、策略和证据决定 |
| **Witness-Carried Delivery** | 计划、执行、验收都携带可检查的见证 |
| **Recoverable Continuity** | 失败和重启后恢复真实状态，而不是依赖模型回忆 |

---

# 三、统一主干

```text
用户表达 Utterance
        │
        ▼
IntentDeltaProposal
LLM 提出多个语义候选，不拥有真相
        │
        ▼
CandidateIntentSet
目标 / 禁令 / 偏好 / 风险 / 效果候选
        │
        ▼
Semantic Convergence Kernel
证据 + 权限 + 冲突 + 当前性 + 风险裁决
        │
        ▼
AcceptedIntentDelta
唯一允许写入意图真相的变更
        │
 

## 13:11

文档已创建：

`/Volumes/移动硬盘/polars/docs/意图识别8.23 思想风暴.md`

- 630 行，约 22 KB
- 基于当前 `main@1aadfec`
- 技术路径、符号和格式已校验
- 尚未提交 Git

## 四项问题的裁决

### 1. Kernel 成为新的“神”

这个风险成立，所以我已经收窄并改名：

> `Semantic Convergence Kernel` → `Semantic Admission Kernel`

**Semantic Convergence 是全系统过程，不属于单个组件。**

Kernel 只做：

- 当前性
- 权限
- 证据
- 冲突
- 效果
- 风险
- 合法迁移

它不理解自然语言、不生成语义、不查询全部真相、不裁决完成，内部也**不允许使用 LLM**。

原则是：

> 一个裁决可以有唯一所有者，但不能同时拥有裁决依赖的全部真相。

### 2. IntentState 膨胀

不采用“每轮复制一个巨型对象”，改为：

```text
小型 IntentStateHead
+ 稀疏 IntentDeltaLog
+ 可寻址 Facets
+ 周期性 Snapshot
```

只有目标、禁令、义务、授权效果、验收条件等发生实质变化时才创建版本。

Digest 只覆盖 canonical core 和 facet refs；原始聊天文本留在 ledger，通过证据引用连接。

### 3. 自然语言 → Delta 鸿沟

这是当前 **P0 最高优先级**。

不能继续通过增加关键词、分类和状态枚举解决。正确顺序是：

1. 建立跨轮、否定、疑问、修正、禁令等效果级评测集。
2. LLM 输出多个 `IntentDeltaProposal` 候选。
3. 每项变化必须携带 evidence span。
4. 显式投影候选会产生的效果。
5. Kernel 只决定候选能否被接收，不假装证明语义理解正确。

现有测试通过、外部探针失败，说明：

> 当前系统证明了内部自洽，却没有证明语义入口正确。

### 4. 用户体验与严格性的张力

默认策略不是“最小到什么也不做”，而是：

> **最小、已授权、有推进价值、优先可逆的行动。**

只有同时满足以下条件才询问：

1. 存在多个合理理解；
2. 会产生实质不同的效果；
3. 没有安全且有价值的共同动作；
4. 选错会造成外部、破坏性、付费、扩权或大范围返工。

交互约束：

- 一次最多一个阻断问题；
- 其余问题保留，不连续轰炸用户；
- 可安全调查时继续推进；
- 重要动作使用非阻断回显；
- 高风险效果才显式确认；
- 用户新增禁令后，冲突中的旧 Attempt 立即 stale/hold/rebase。

## 最终优先顺序

```text
效果级语义评测
→ 最小 IntentDeltaProposal
→ 小型 Semantic Admission Kernel
→ 统一 IntentState
→ Coverage/Fulfillment Witness
→ 用户体验调优
```

**现在最不应该做的是先实现一个庞大的 Kernel。最应该先解决的是自然语言如何可靠产生稀疏、多候选、带证据的 Delta。**

## 14:15

已更新进文档，新增 **第14章「8.23 最新收敛更新」**：

- Kernel 去神化并更名
- 权威准入闭环禁止 LLM
- IntentState 轻量化结构
- 语义入口优先的实施顺序
- 沉默推进与澄清策略
- 最新总裁决

文件现为 745 行，格式检查通过，尚未提交 Git。

## 14:33

检查完了。结论不是“意图识别没做”，而是：

> **项目已经把“状态迁移与稳定交付治理”做得很深，但“用户究竟想要什么”仍由两套互不统一的启发式入口判断。**

当前代码能证明“系统按现有规则迁移了”，还不能证明“现有规则正确理解了用户”。

## 一、当前真实架构

```text
飞书 / Telegram / Webhook
        ↓
ChatEntry 规则识别
RouteLowCost → IntentJoinery → CandidateLifecycle
        ↓
S11 最小叶片 → S12 回复/延迟 → S13 TaskInput 提交
        │
        └──── UserIntentCarrier ────┐
                                    ↓
桌面输入框                      Task Service
        ↓                           ↓
Work Center                    任务分类/规划/验证/恢复
RequirementModel                  ↓
→ ApertureDecision          Product Mainline
→ LLM RequirementContract
→ SemanticState
→ 用户显式确认
        ↓
UserIntentCarrier
+ RequirementJoinery ──────────────┘
```

关键事实：

1. **ChatEntry 和 Work Center 是两套意图入口。**
2. 二者只在 `TaskInput/UserIntentCarrier` 层汇合。
3. 当前没有统一的 `IntentState`、字段级 `IntentDelta`、currentness reducer 或 `Semantic Convergence Kernel`。
4. 全仓精确搜索所谓 `IntentDelta`，只找到回复治理里的 `ReplyProjectionDeltaV1`；它负责阻止模型回复直接修改全局状态，不是自然语言意图状态增量：  
   `internal/application/chatentry/model_reply_governance.go:106-123,155-193`
5. `CurrentIntentState` 实际记录的是 `active_task_submitted/queue_pending` 这类任务运行状态，不是用户语义状态：  
   `internal/application/chatentry/session_compression_projection.go:137-158,200-211`

---

# 二、ChatEntry 代码落点

## 1. 总编排

入口位于：

- `internal/application/chatentry/accept.go:53-381`

完整顺序是：

1. 规范化、验证消息 Envelope
2. `RouteLowCost`
3. 先写 InputLedger
4. 写 ConversationTurn
5. 产品策略/S3 情绪分支
6. S2 上下文压缩
7. 构造 IntentJoinery 与 ActionCandidate
8. 执行候选生命周期

## 17:39

可以，但先钉死一个边界：

> **我们无法形式化证明“自然语言就是用户真实意图”。能形式化证明的是：系统只接收有当前证据支撑、满足确定性约束的状态增量。**

所以我不会造一个包办语义理解的“神级 Kernel”，而会建立一条唯一主干：

```text
用户输入
  ↓
不可变事实记录 Observation
  ↓
候选语义增量 Candidate IntentDelta
  ↓
确定性 Semantic Reducer
  ↓
唯一 Canonical IntentState
  ↓
确定性 Admission Decision
  ↓
RequirementJoinery
  ↓
TaskInput
  ↓
现有 S11 → S12 → S13
```

# 一、只保留一个语义真相所有者

新建：

```text
pkg/contracts/intent/v1/
internal/application/intentkernel/
```

只有 `intentkernel` 能更新 `Canonical IntentState`。

以下模块全部降级为 Adapter：

- ChatEntry：不再直接判断后写 TaskInput
- Work Center：不再直接把 LLM JSON 当需求真相
- Memory：只能提供 advisory evidence
- Attachment：只能提供 observation
- LLM：只能提出 Candidate Delta
- 前端：只能确认某个精确 state digest

任何入口都不能绕过 Kernel。

---

# 二、IntentState 必须克制

不把所有可能字段都塞进去。第一版只保留决定任务走向的六个核心维度：

```go
type IntentStateV1 struct {
    IntentID    string
    Revision    uint64
    Digest      string

    Objective   FieldValue[string]
    Effect      FieldValue[EffectMode]
    Target      FieldValue[TargetSpec]
    Constraints FieldValue[[]string]
    NonGoals    FieldValue[[]string]
    Done        FieldValue[[]string]

    SpeechAct   SpeechAct
    Status      IntentStatus

    OpenConflicts []IntentConflict
    OpenQuestions []IntentQuestion
}
```

其中：

```text
EffectMode:
- answer_only
- analyze_read_only
- propose_changes
- modify
- create
- delete
- controlled_external_action
```

`task_class` 不属于用户原始意图，只能从 IntentState 派生，不能反过来统治语义。

每个 `FieldValue` 都必须携带：

```text
value
source_observation_id
source_span
accepted_

## 17:41

我先做完整清点，再逐份通读；不会只搜关键词或抽样。

## 17:46

我已逐篇通读完 **21 份手稿，约 472KB**，不是关键词抽样；未修改任何文件。

## 我对整套思想的总理解

北极星真正研究的不是“怎样让 Agent 更聪明”，而是：

> **如何把概率性智能限制在一个确定、可验证、可恢复的状态迁移系统里。**

线段论规定主干；P1-P5规定可靠性；空间榫卯规定组合合法性；关系材料规定输入主权；动态真相闭包规定状态如何演化；Ψ负责事后检查。

## 对意图识别最重要的启发

### 意图识别不是“判断用户在说什么”

而是：

> **裁决这句话被允许改变系统里的什么。**

因此正确主干应是：

```text
用户话语
→ 不可变 Observation Ledger
→ Candidate IntentDelta
→ Intent Assembly Kernel
→ IntentContract@epoch
→ Admission Witness
→ TaskInput
```

### 1. IntentState 不该是越来越胖的结构体

它应当只是事件轨迹的**物化视图**。

用户每次补充、否定、纠正，都追加事件；旧意图不被覆盖，而是：

```text
supersede / rebase / reject / quarantine
```

这样字段膨胀、digest、历史追踪、重启恢复可以同时解决。

### 2. 用户纠正属于“目标演化”

例如：

```text
先修改代码
→ 改成只分析，不要修改
```

不是在旧合同上改两个字段，而是产生：

```text
IntentEpoch 7 → IntentEpoch 8
```

旧确认、旧任务和迟到结果必须因 epoch 过期而失效。

### 3. Semantic Kernel 不能成为新的“神”

它不负责理解自然语言，也不负责判断“真正含义”。

它只负责确定性裁决：

- Delta 是否作用于当前 epoch
- 是否越过允许的语义表面
- 穿透深度是否合法
- 是否与硬约束冲突
- 是否具备提交 witness

**LLM 可以提议，不能提交，更不能自证。**

因此它更适合叫：

> **Intent Assembly Kernel**  
> 意图装配内核

### 4. 引入“类型化语义表面”

不同话语只能写入不同表面：

| 用户表达 | 允许表面 |
|---|---|
| “是什么意思？” | 回答表面，禁止任务晋升 |
| “只分析，不修改” | 只读分析表面 |
| “修复这个问题” | Patch 候选表面 |
| “部署” | 运行态表面，但仍需独立授权 |
| “不要……” | 控制约束表面，优先级高于动作关键词 |

这能从结构上解决“看到修复两个字就晋升 repo_patch”的问题。

### 5. 内部严格不等于用户麻烦

只在未决信息可能改变以下内容时澄清：

- 是否产生副作用
- 操作范围
- 不可逆边界
- 最终交付物

其他情况采用**最小安全行动**，并只给主脑投影：

```text
当前 IntentContract
+ 未决义务
+ 最近有效修订
+ 必要上下文
```

用户不需要看到内部 epoch、digest、reducer 和 witness。

## 最值得落地的第一批 Ψ

```text
ψ_question_cannot_mutate
ψ_negation_precedence
ψ_effect_within_authority
ψ_

## 18:01

已完成：

- 旧方案已明确退役，不再并列生效。
- 文档升级为 v3“意图真相轨迹方案”。
- 新主干已写入：Ledger → Delta → Assembly → Trajectory → Epoch → Witness。
- 现有代码未删除，仅标记为待迁移。
- 文档校验通过；文件尚未 Git 提交。

## 18:05

我会把它拆成两层研究：**可直接复用的骨架**与**只能借鉴的机制**，目标不是硬 fork，而是最大限度少造轮子。

## 18:25

## 结论

这个思路是对的，但要修正一句：

> **不要 fork 整个 Grok CLI；应把它当作“机制矿、交互样板和测试语料库”。**

整仓二开看似省事，实际上会接管 Grok 的整套 Agent 内核。北极星最省轮子的路线是：

> **扩展现有 Go `cmd/cli`，保留 Gateway 为唯一真相源，只移植 Grok 已验证的交互与可靠性机制。**

这样可以完全绕过桌面端，同时不破坏北极星真正的差异化能力。

---

## 一、为什么不建议整仓 fork

研究快照：

- Grok Build `xai-grok-pager-bin 1.0.6`
- HEAD：`19d42e35c07a9c9244f03f6df0c4c353f970d4f9`
- 94 个内部 Rust package
- 官方仓库是周期性从内部 monorepo 同步，且不接受外部贡献，长期维护 fork 会很重。[官方源码](https://github.com/xai-org/grok-build/tree/19d42e35c07a9c9244f03f6df0c4c353f970d4f9) [仓库结构说明](https://github.com/xai-org/grok-build/blob/19d42e35c07a9c9244f03f6df0c4c353f970d4f9/README.md)

静态生产依赖闭包：

| 入口 | 内部 crate | Rust 文件 | 约 LOC |
|---|---:|---:|---:|
| `xai-acp-lib` | 1 | 8 | 2,277 |
| `xai-workflow` | 1 | 7 | 3,306 |
| `xai-grok-workspace` | 49 | 880 | 490,002 |
| `xai-grok-shell` | 70 | 1,554 | 932,842 |
| `xai-grok-pager-render` | 57 | 1,010 | 575,695 |
| `xai-grok-pager` | 86 | 2,309 | 1,535,270 |
| 最终二进制 | 88 | 2,323 | 1,545,610 |

关键事实是：**连渲染层都不是一个可以薄取的叶子模块。**

整仓 fork 会同时带进：

- 第二套 Agent loop
- 第二套 provider、工具、权限、memory、workspace
- Rust 工具链和庞大依赖
- xAI 登录、远端配置、更新、遥测、分享等产品逻辑
- 与北极星 IntentTrajectory 竞争的第二个语义所有者

这不是少造轮子，而是接手一辆别人的整车。

---

## 二、Grok 真正值得借的能力

### 1. 单写者会话 Actor

它把会话变更串行化，并区分：

- 未提交
- 已提交
- 已提交但确认丢失

这很适合北极星的 `IntentTrajectoryOwner`、任务状态和命令幂等处理。

### 2. 崩溃后的确定性恢复

Grok 重连时不是简单“连上就继续”，而是：

1. 重放 `initialize`
2. 逐个恢复 `session/load`
3. 转发恢复过程中的通知
4. 必须等到对应响应真正到达，才允许下一条请求

这避免了“连接已恢复，但会话尚未恢复”的竞态。[重连源码](https://github.com/xai-org/grok-build/b

## 18:35

已保存：

`/Volumes/移动硬盘/polars/docs/polars cli.md`

共 708 行，`git diff --check` 通过。未修改其他文档。

## 18:51

捋完了。**北极星不是“意图识别 + CLI”**，真正完整的形态应是：

```text
Observation
→ IntentTrajectory / IntentContractEpoch
→ TaskContract / CapabilityContract
→ Plan / Mission / Todo
→ EffectAuthorization
→ Runner / Agent / Browser 产生候选结果
→ ControlPlane 确定性接收
→ Verification / Review
→ Delivery / Syncback
→ IntentFulfillmentWitness / ProjectClosure
→ WorkEntry + 可恢复事件流
→ Desktop / Connector / CLI
```

## 一、统一设计语言

北极星每一段都应该遵循同一种结构：

```text
概率性输出 Candidate
→ 小型确定性 Gate
→ 状态迁移
→ Witness
```

不仅意图如此：

- LLM 输出 `CandidateIntentDelta`
- Planner 输出 `PlanCandidate`
- Runner 输出 `Patch/ActionCandidate`
- Reviewer 输出 `ReviewAdvice`
- Connector 输出 `DeliveryCandidate`

它们都不能直接改权威状态。

**不要再造一个“全能 Kernel”**。每段由自己的小 Owner 裁决，Gateway 负责串联和唯一写入。

---

## 二、CLI 前必须闭合的三条主干

### 1. 业务状态主干

```text
意图 → 任务 → 计划 → 执行 → 验证 → 评审 → 交付 → 履约
```

当前代码已经具备较强的“任务内部闭环”：

- 持久队列
- 准入与能力矩阵
- Plan、Mission、Todo
- Runner 分派
- 安全前检
- Patch/Agent/Browser
- Verification、Review
- Convergence、Memory ingestion

组合根见 `cmd/gateway/main.go:56-102`，任务主线见  
`internal/application/tasks/service_task_intake.go:83-139`。

但它目前只闭合到“任务执行成功”，还没有闭合到“用户意图已经履约”。

### 2. 真相与权威主干

必须把这些身份绑定起来：

```text
IntentEpoch
→ TaskContract
→ PlanRevision
→ AttemptID
→ EffectAuthorization
→ Evidence
→ GlobalCommit
→ FulfillmentWitness
```

用户修改意图后产生新 epoch，旧 epoch 的：

- 计划
- attempt
- 授权
- Runner 回传
- delivery

都必须失效或隔离，不能继续提交。

### 3. 续接与恢复主干

```text
Lease / Session / Checkpoint
→ 故障分类
→ Reattach / Resume / Retry / Reroute
→ Replan / Rollback / Human Help
→ 重启继续
```


## 18:55

下面是**评审版综合排期**，暂不落盘。基于当前 HEAD `1aadfec`。

## 总盘面

- **基准周期：22 周**
- **时间：2026-08-24 ～ 2027-01-24**
- **组织：3 条实现线 + 1 条独立验收线**
- **产品 CLI：第 18 周才正式开工**
- 估算浮动：约 ±20%，M0 后重新校准。

```text
M0 合同定盘
 ├─ M1 意图真相
 ├─ M2 能力与授权
 ↓
M3 控制面与全局提交
 ├─ M4 恢复续接
 ├─ M5 交付履约
 ↓
M6 项目与全能力接入
 ↓
M7 投影、连接器、事件流
 ↓
M8 后端完整性总验收
 ↓
M9 CLI
 ↓
M10 稳定化与候选发布
```

---

# 一、综合大排期

| 里程碑 | 时间 | 核心交付 | 完成门 |
|---|---|---|---|
| **M0 主干合同定盘** | 08-24～09-06 | Owner、状态、合同、效果分类、验收基线 | 所有后续状态迁移有唯一 Owner |
| **M1 意图真相主干** | 09-07～09-27 | Observation、IntentTrajectory、Epoch、统一入口 | 任意入口生成相同 epoch；旧 epoch 不能提交 |
| **M2 能力与效果授权** | 09-07～10-04 | CapabilityLifecycleContract、效果矩阵、授权绑定 | 无精确授权不能产生外部效果 |
| **M3 生产控制面** | 09-28～10-25 | Ledger writer、Attempt、候选提交、确定性接收 | 重放结果一致；无分叉、无重复提交 |
| **M4 重启续接与恢复** | 10-12～11-15 | checkpoint、reattach、resume、失败路由 | 杀 Gateway/Runner 后可续接且不重复副作用 |
| **M5 验证、交付与履约** | 10-12～11-22 | Verification、Review、Delivery、Fulfillment Witness | 成功、已交付、已履约三者不再混用 |
| **M6 项目与全能力接入** | 11-09～12-06 | 项目动态更新、聚合闭环、五类能力接入 | 多能力项目能成功、阻断、恢复并明确终止 |
| **M7 投影、连接器、事件协议** | 11-23～12-13 | durable SSE、cursor、replay、最终回传 | 断线重连不丢事件；原会话收到终态 |
| **M8 后端完整性总验收** | 12-14～12-20 | 全链杀进程、重放、安全、履约矩阵 | Backend Complete Gate 全绿 |
| **M9 北极星 CLI** | 12-21～01-10 | 提交、观察、授权、恢复、项目、诊断 | CLI 不持有私有真相，与其他入口语义一致 |
| **M10 稳定化与候选发布** | 01-11～01-24 | 迁移、性能、安全、fresh install、候选构建 | 项目 release preflight + 不可变候选全绿 |

---

# 二、各阶段详细工作包

## M0：主干合同定盘

### 工作

1. 核验仓库当前 release preflight；缺失或失效则先补。
2. 输出完整状态所有权表：
   - IntentTrajectoryOwner
   - Ta

## 18:58

已保存至：

`/Volumes/移动硬盘/polars/docs/排期.md`

共 545 行，`git diff --check` 通过；未修改其他文档，未提交。

## 19:14

没停，当前 **4 线并行**：

- 已完成：Owner、Capability、Preflight 三项全仓审计。
- 已确认：ControlPlane 无生产写链、Delivery 真相缺失、能力合同分散。
- 正在收敛：根级 Preflight、M0 首个实现叶、CapabilityLifecycleContract 骨架。
- 当前硬门：统一 Preflight 缺失；AGENTS 指定的 WSL 两份模板本机不可读。

我会持续推进只读设计与落点；模板恢复后立即进入源码实现。

## 20:01

没有中断，当前 **主脑 + 2 条 Luna Max** 持续运行。

### 已完成
- Root development preflight 已实跑通过。
- 已接入 Make、Backend CI、Desktop CI。
- 已修复：
  - Make 参数注入绕过
  - CI marker 假绿
  - 伪造 release bundle 假绿
- Release 当前保持 fail-closed，未冒充可发布。

### 正在并行
1. 将 1158 行 preflight“神脚本”拆成独立 Owner 模块。
2. 修正 CapabilityLifecycleContract：
   - refs-only
   - 父子深拷贝
   - 列表三态
   - Store/执行快照回归测试

随后立即独立复审、运行父级 Go/Ψ Gate，再进入 Attempt 原子迁移叶。

## 20:02

收到。此后每三分钟播报一次；仅汇报，不中断执行。

## 20:08

**3 分钟进度播报：**

- CapabilityLifecycleContract 已完成第二轮修正：
  - refs-only
  - 父子深拷贝
  - 列表三态
  - SQLite 与执行快照回归均通过
- 独立 Capability 复审正在运行。
- Preflight“神脚本”模块拆分仍在运行，暂无阻断。
- 当前 development Gate 绿色；release 继续红灯封闭。
- 未执行构建、启动或发布。

## 20:14

**3 分钟播报**
- Root preflight 独立 Gate：PASS（35 项）
- Capability 合同独立 Gate：PASS
- Release 仍按设计红灯，未构建/发布
- 正进行父级全套验收，随后进入 Attempt 原子迁移。

## 20:18

**3 分钟播报**
- 两个首叶父级验收均通过
- 全仓 Go 仅 1 项红：真实 DNS 把 `.invalid` 映射为假 IP
- 已并行审计测试根因、Attempt 接口影响
- 另发现 preflight 可能生成 `pyc` 自污染，正在补审；未构建/发布。

## 20:23

**3 分钟播报**
- DNS 红灯已根修复：测试改为注入失败 resolver，独立复审中
- preflight 自写 `pyc` 根修复实施中
- Attempt 原子写 Store 合同并行实施中
- Release 仍红灯；无构建、启动、部署。

## 20:26

**3 分钟播报**
- DNS 与 preflight 自污染修复均已独立 PASS
- Attempt 原子迁移实现完成：正式 Store 合同、去非原子 fallback
- 正在独立复审 Attempt
- Intent Owner、ControlPlane writer 两条下一叶已并行审计。

## 20:31

**3 分钟播报**
- Attempt 原子叶父级+独立 Gate：PASS
- 全仓复验又暴露既有不确定性：RFC3339Nano 文本排序把 later 事件排到前面
- 已停止盲目重跑，转入根因审计
- Intent/ControlPlane 下一叶建模仍在并行。

## 20:37

**3 分钟播报**
- Authorization 错序已量化：2000 次中 14 次，根因确认
- 修复线正改为按 append 因果序读取，非掩盖测试
- 同时复审 Intent/ControlPlane 是否越过 M0；防止提前造平行真相
- 其余 Gate 维持绿色。

## 20:41

**3 分钟播报**
- Authorization 因果排序修复已落地
- 父级压力门：Store 200 次、Service 500 次全绿
- 独立终审仍在跑
- Intent/ControlPlane M0 边界复审中，重点防止越级到 M1/M3。

## 20:45

**3 分钟播报**
- 全仓 `go test ./...` 已全绿，M0 基础 Gate 冻结
- 拒绝两种越级：空载 Intent owner、提前接 ControlPlane writer
- 现并行实现两条纯 M0 机械叶：
  1. Intent legacy writer fence
  2. ControlPlane refs-only 事件身份合同。

## 20:46

对，已设为硬门：每叶先核对 **Owner、阶段、依赖、真相源、禁止项**；架构不闭合就不实施。刚刚已拦下“空载 Intent Owner”和“提前接 ControlPlane Writer”两次越级。工作继续。

## 20:48

**3 分钟播报**
- 架构硬门已写入主脑约束并同步两条执行线
- 两条线都只做 M0：
  - Intent：登记旧写者，不启用新 Owner
  - ControlPlane：只冻结身份合同，不接 Writer
- 无越级改动；仍未构建/启动/部署。

## 20:51

**3 分钟播报**
- ControlPlane 合同初版完成，正在架构终审
- 终审重点不是“测试绿”，而是：
  - 跨语言 canonical 是否唯一
  - 是否有 golden digest
  - 非法事件能否伪装等价
  - API 是否过度膨胀
- Intent Writer Fence 仍在实施。

## 20:56

**3 分钟播报**
- ControlPlane 初版被终审打回，已按架构修正：
  - 8/9 元素固定 canonical tuple
  - 跨语言 golden digest
  - 非法事件不得伪装等价/冲突
  - 删除冗余 API
- 正在二次终审；Intent Fence 同步终审中。

## 21:01

**3 分钟播报**
- ControlPlane M0 身份合同：父级+独立 Gate PASS
- Golden digest 已用独立 Python 重算一致
- 仍未接任何 Store/Writer/DB，严格停在 M0
- Intent Fence 终审正在收口。

## 21:04

**3 分钟播报**
- Intent Fence 初版测试虽绿，但架构终审 FAIL，已打回
- 正在修 6 类问题：
  - AST 漏检
  - 扫描错误被吞
  - 登记非双向
  - SQLite 真写者漏盘点
  - digest 无独立 golden
  - API 膨胀
- 不接受“测试绿但门可绕过”。

## 21:09

**3 分钟播报**
- ControlPlane 合同已正式 Gate PASS
- Intent Fence 修复仍在执行，未超范围
- 当前重点补齐 **应用调用者 + SQLite 真写者** 双层盘点，并让扫描器遇错必红
- 继续等待完整红绿收据，不提前宣布完成。

## 21:12

**3 分钟播报**
- Intent Fence 二版机械漏洞已补，但我发现新的架构风险：
  - 把 Todo/Assignment 等非 Intent DB 写者也算进来了
  - 把 SQLite 误当成真相 Owner
  - 用“每函数一个状态”掩盖同一 TaskInput 投影
- 已要求终审按“真相语义”而非数量审查。

## 21:16

明白。架构未闭合，任何叶子都不准落地；当前 Intent Fence 已因此退回重建。

## 21:19

进度：Intent Fence 二版正式判退。现按真实表/字段重建，SQLite 只作适配器；并行启动 M0 全局架构预审。

## 21:20

架构核对中：已补齐遗漏的 TaskService、动态派发、Canvas、协商写入面；仍未允许进入 M1。

## 21:23

三分钟播报：第三版已开始重写，旧测试自证结构已拆除；当前只改 Fence 四文件，生产链零改动。

## 21:24

架构预审结果：局部叶均合规，但完整 M0 仍缺 Owner 总表、3 个核心合同、状态语义及 repo_patch 黄金轨迹；不会提前报完成。

## 21:28

三分钟播报：已发现并堵住两类 Gate 漏洞——跨状态写者静默漏检、SQLite 变体写法绕过；正在补红测。

## 21:30

三分钟播报：Fence 已改为真实状态共享 Owner，扫描全 SQLite；当前正验证 wrapper、动态 SQL、多状态写者均不能绕 Gate。

## 21:33

三分钟播报：Fence 红测继续扩到“命名藏写入”旁路；同时 Owner 总表正从当前 Store/Service 真相逐项取证。

## 21:35

三分钟播报：并行启动 M0 Owner 事实栅栏；它只冻结冲突，不粉饰为完成。Intent Fence 目标测已绿。

## 21:37

三分钟播报：Intent Fence 已送独立终审；父级复算确认 25 写者、25 路径、7 状态，摘要一致。

## 21:40

三分钟播报：终审与高次数 Gate 并行运行中；当前无生产代码、Store、Schema 或运行态改动。

## 21:42

收到。后续先过 Owner、阶段、依赖、真相源、事务边界、禁止项六道架构门；不闭合就不实施。

## 21:44

进度：Owner 清单已按架构拆为 291/245 行，源码边界与高频 Gate 均绿；现交由非实现者独立审查，M0 仍锁定。

## 21:46

架构审查刚拦下一处真实绕过：间接 SQL 可漏过 Intent 清单。已禁止验收并派发根因修复；M0、M1继续锁定。

## 21:51

又拦下一处：Owner 清单自洽但漏了真实写者。已拒绝验收，补“源码↔清单双向覆盖门”；两处都按根因修，不做表面补项。

## 21:53

剩余 M0 主干已出初稿，但我未直接放行：正复核“合同编译者是否真是 Owner、履约 witness 是否多 Owner、M0 解锁语义”三处风险。

## 21:57

两条修复线都在推进。Intent 门已从“搜字符串”升级为“定位 SQL 执行点再分类”；我同时压制过度复杂化，防止 Gate 自己变成新风险源。

## 22:02

双向 Owner 门已进入真实仓库扫描，并主动报红两类旧盲区：动态 SQL、Todo/Mission 状态写入。当前是预期红灯，未被“补名单”掩盖。

## 22:04

架构复审已否决初稿三处：多 Owner witness、双重解锁语义、投影 Owner 碎片化。主干已改正，未让错误方案进入实现。

## 22:09

架构门仍是硬前置：我先收口两道事实门，不会因测试绿就越过 Owner/真相源审查；当前没有进入 M1，也没有任何构建、启动或发布动作。

## 22:11

进度：Intent 写者门已完成实现，正在做独立只读终审；Owner Inventory 正按“源码↔回执双向覆盖”修正。新扫描已证明旧 PASS 计数不可信，因此我已禁止保数，要求按真实多写者降级裁决。当前活动线段仅是 M0 事实冻结，右端仍为 **ContractDesignFrozen=false / M1 blocked**。

## 22:15

进度：根侧已独立复跑 Intent 合同与 Fence 各 50 次，均通过；但终审仍未放行，因为还在检查静默旁路。Owner Inventory 扫描又抓到两类架构漏洞：动态表 SQL 被误放行、分支赋值会覆盖未知路径；已要求补成 fail-closed 反例。当前 Gate 仍红，未向后推进。

## 22:19

独立终审已明确判 **FAIL**：集合与 digest 都绿，但仍存在 function value、外部 caller、同名传播、动态 DDL/尾部注入旁路。按你的要求，我不会拿绿测冒充架构成立；Intent 门继续锁住，正在把“两套 SQL 解析器”收敛为一个真相分析器，而不是继续堆补丁。

## 22:21

进度：Intent 终审的 FAIL 已固化，计划主干已调整为“单一 SQLite mutation 分析真相源 → 两道事实门”。Owner Inventory 当前已修掉旧计数伪 PASS，现为 **PASS 2 / CONFLICT 8 / MISSING 2 / BLOCKED 2**；扫描继续在动态只读查询证明处 fail-closed，未被白名单绕过。M1 仍锁定。

## 22:26

进度：Owner Inventory 叶已安全收口，结构事实已纠正为 **2/8/2/2**，所有非测试 Go 文件均 <400 行；私有扫描器保持红，不再继续扩建。现在已按冻结架构进入 S0→S1：只建立共享 `sqliteinventory` 分析器，暂不碰 Intent/Owner 两个投影，也不改生产 writer、Store、schema 或事务。

## 22:27

进度：共享分析器目前仍在 **S0 接口冻结/源码形态盘点**，尚未写代码，这是刻意的架构门，不是停工。另一只只读叶正全量枚举现有 SQLite 的 literal、分支、Join、Sprintf、参数 helper、DDL/RETURNING 等真实形态；S1 只能覆盖这份最小闭包，禁止凭想象造通用框架。

## 22:32

进度：S0 已生成首版机器合同；根侧预审已拦下三处潜在架构回退并要求当场修正：SymbolID 不能是字符串黑盒、caller scope 不能只扫 SQLite 目录、DDL 不能用全局布尔白名单。当前正在按完整 `PackagePath/RelPath/Receiver/Name/TypeArity` 与显式 DDL witness 重做，尚未进入消费者迁移。

## 22:35

进度：S0 合同现已可编译，并已按职责拆分，`api.go 286 / discovery.go 131 / source.go 272`，没有用压行绕过 400 行门。下一步才是 S1 的 value lattice、call graph 与 SQL fact；当前仍无消费者接线、无 Owner 激活、无生产状态改动。

## 22:39

进度：真实语法闭包已盘清：78 个 SQLite 文件、347 个直接 SQL 调用；并确认两个容易漏掉的主干事实——`QueryRowContext` 实际执行 `UPDATE ... RETURNING`，且 `cmd/migrate/sqlite.go` 还有 adapter 目录外的 PRAGMA/VACUUM 直连。S1 已把扫描默认范围扩到整个生产 module；任何按 Go 方法名判读写、或只扫 `internal/store/sqlite` 的实现都会直接判废。

## 22:41

进度：S1 核心现已恢复可编译，并拆成 9 个职责文件，全部低于 400 行。根侧又拦下两类“表面可编译、语义不可信”的风险：不能把所有同名 `.Exec/.Query` 都当数据库调用；不能把精确多语句 DDL 全判未知。当前正补 DB/Tx/Stmt 来源证明、UPDATE 列识别、Join/闭包/range 数据流与多语句逐句解析。

## 22:43

收到。已把“架构成立”设为硬前置：当前只走 **S0→S1 单一分析器主干**；独立 Gate 未通过前，不迁移 Intent/Owner、不解锁 M1，测试绿也不算放行。

## 22:46

进度播报：生产探针发现 **147 个假红**，根因是“全仓扫描”误等于“全仓所有未知调用都致命”，并把非数据库同名 `Query` 当 SQL。已否决该实现路线，强制改为 **type-backed receiver provenance + SQL 相关性切片**；M1 继续封锁。

## 22:50

进度播报：`go/packages ./...` 虽能补类型证明，但实测 **45.267 秒仍未完成**，而仓库 Ψ 单门限是 5 秒，已再次否决。现在收敛为：**全仓廉价发现 → SQL 相关包/调用闭包切片 → 仅切片做类型证明**，既不能漏写者，也不能拖垮门禁。

## 22:56

进度播报：进一步实测确认，问题不在类型证明本身——全仓 94 包、912 文件 typed load 仅 **1.622 秒**；真正超时的是对 5289 个函数反复跑值流。架构已收敛为 **全仓类型真相 + 仅 SQL 相关函数子图做 fixpoint**，避免 import/name 启发式漏掉 `s.db` 写者。

## 23:01

进度播报：类型阶段和性能主干已稳定，现有 smoke 0.292 秒；同时抓出并修正了两处架构级确定性问题：普通 `s.db.ExecContext` 曾被误判成 method expression，以及 execution ID 含绝对 checkout 路径。当前所有 analyzer 生产文件已重新拆到 **<400 行**；正在补齐反例矩阵，尚未放行。

## 23:10

进度播报：S1 反例集已从 5 条扩到 9 组，新增接口 receiver、闭包、分支、未知函数值、有限 SQL alternatives、模板静态后缀、投影错误强制返回；当前全部通过。仍未放行：还缺外部 caller、placeholder/quote sanitizer、长链收敛及 **349 个生产 execution 对账**。

## 23:14

进度播报：生产面已首次完成机械对账——**349/349 SQL execution，missing=0**（SQLite 347 + migrate 2），总探针约 **2.10 秒**。INSERT lexer修正后红项从 70 降到 52；仍有 2 个接口 provenance 红和 fixpoint 红，所以继续封锁 S1。

## 23:18

收到。当前严格按 **S1 唯一事实分析器 → 独立架构验收 → S2/S3 投影 → S4 退役旧解析器** 推进；架构不闭合，即使测试全绿也不放行。

## 23:20

**23:20 进度**：单调格根因已验证，传播由超限变为第 3 轮收敛；仍保持 **349/349、2.10 秒**。当前还有 `44` 个 SQL 不确定、`2` 个接口接收者不确定，S1 继续保持红灯；正在按通用序列格、闭包与接口证明收敛，未走白名单。

## 23:23

**23:23 进度**：独立架构微审已完成，确认不能靠提高上限或枚举组合硬消红。S1 唯一实现方向已锁定为：**符号序列格 + 行相关记录 + 闭包效果摘要 + 接收者能力格**；当前实现正在按这四个根结构替换，后继 Intent/Owner 仍未解锁。

## 23:27

**23:27 进度**：刚拦下一条不合架构的实现——用 `[][]SQLValue` 枚举可选条件，本质仍会产生 `2^n` 爆炸。我已要求撤回该方向，改成真正的符号序列 atom（必选/可选/重复）；这正是“测试可能绿，但架构不能过”的实例。当前仍停留在 S1，不越级。

## 23:29

**23:30 进度**：枚举式 `listPaths` 已开始退役，代码已转为带 `required / optional / repeat` 的符号序列。现在正在补最关键的空/非空双路径：确保可选过滤条件为空时不会留下孤立 `WHERE`，非空时又能证明不会改变主语句与目标表。S1 仍未验收。

## 23:33

**23:34 进度**：符号序列现已具备基数信息，且新增了两类反例锁：结构体 range 必须保留字段关联；`return` 后不得继续污染闭包/列表。下一道门是让安全序列由 SQL 解析器证明，而不是直接标记 `SafeTemplate`；证明未完成前仍保持 fail-closed。

## 23:37

**23:37 进度**：当前探针进一步改善到 **349/349、1.87 秒、接口歧义 0、SQL 红 42**。接口能力格和行相关 record 已生效；但 `flow.go/lattice.go` 因新增语义超过行数门，我已要求按职责拆文件，不能用压缩格式躲过架构边界。

## 23:40

**23:40 进度**：又抓到两处“绿测会掩盖错误”的风险：闭包早退路径的 capture effect 会被后续语句覆盖；后轮出现 `Unknown` 时旧的 `Exact return` 可能继续存活。两处都已要求按单调格修复并补反例，不能靠当前 package PASS 放行。

## 23:42

**23:43 进度**：我又否决了一个“自签证书”风险：不能用列表变量名自动生成 `GuardID` 再自证安全。Guard 必须来自真实 `len(list)` 条件及其 CFG 分支，并随 `Empty/NonEmpty` 路径传播；否则看似形式化，实则只是换名字的白名单。正在按真实路径证据重做。

## 23:44

收到。继续按“架构证明 → 实现 → 独立审查 → 验收”主干推进；测试绿不替代架构成立，S1 未过门不启动 S2。

## 23:47

23:47 进度：真实源码位置生成的 `len` 分支 Guard 已落入值环境；正在按职责拆分超 400 行文件。刚才编译红是拆文件过程中的重复符号瞬态，不算回归结论。前置审查已确认：范围仅 S1、全仓引用已搜、左端 S0/右端“349 条全证明事实”、失败由 S1 门吸收；仍禁止进入 S2。

## 23:49

23:49 进度：超长生产文件已全部拆到 400 行内；Guard 正从“变量名标签”升级为“真实 sequence identity + CFG 支配证据”。独立复核确认三类真实路径仍缺 cardinality、Repeat、`fmt.Sprintf` sequence hole 和结构边界，因此 S1 继续保持红灯，未越级。

## 23:52

23:52 进度：两路独立架构复核已闭合到同一结论——动态片段必须同时具备“来源证明 + SQL 语法槽证明”，不能信自报 Role。当前正在补 `make` 空序列、guard cardinality、range Repeat 与反例 fixtures；编辑中出现的语法红仅是未写完瞬态，尚未进入验收。

## 23:54

23:55 进度：条件 SQL 已改成结构化 `CommonPrefix + SequenceBoundary + CommonSuffix`，旧的 conditional bool 正在退出；4 个聚焦反例/正例已绿，包括无真实长度 Guard 必须 fail-closed。下一步不是看测试数，而是证明普通 filter 分支的 optional atom 与外层 clause Guard 分离、再闭合真实三路径。

## 23:57

23:58 进度：我已拦住两处“测试绿但架构错”的方向：① required 首元素存在时，普通 `if` 的 0/1 append 不该因缺少 len Guard 被误判；② `list:+变量名` 不能当 sequence identity。现在正拆分“atom 分支来源”与“clause 非空 Guard”，并改为定义位置身份；未完成前不跑 349 放行。

