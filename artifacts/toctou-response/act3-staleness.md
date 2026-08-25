# Act 3 — 状态变化 → 收据失效(回应 TOCTOU)

样例改动一行:`demo_log(id INTEGER)` → `demo_log(id INTEGER, actor TEXT)`

```
run2 源文件 sha256: 01a9dd87f7504bbe04a4de3f96e39e96
run3 源文件 sha256: 749a1f9e4ca85d649be29afa6fa6c017   ← 变了
```

run2 时的收据声明(绑定在 sha 01a9… 的世界上):
`text: "CREATE TABLE IF NOT EXISTS demo_log(id INTEGER)"`

run3 重跑后的收据(同 id 同位置,内容已随源变化):
`text: "CREATE TABLE IF NOT EXISTS demo_log(id INTEGER, actor TEXT)"`

**机制:旧收据不被"更新"——它绑定在 sha 01a9… 的世界上,那个世界已不存在。
新世界产生新收据。任何持有旧收据的消费者,做一次 sha 比对即知失效。
"状态变了吗"不是调查,是一次比对。**
