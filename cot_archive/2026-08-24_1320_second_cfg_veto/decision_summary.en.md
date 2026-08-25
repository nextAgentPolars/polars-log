# Decision Summary

Root's veto, verbatim: "Architecture gate intercepted a wrong direction: to fix
unreachable writes, no second CFG. Branch paused. Reachable-write receipts now
propagate along the existing TypedExit path — one control-flow owner only. The
main line continues untouched."

Reviewer's analysis, verbatim (excerpt): "The error source is a second AST
walker — flow_loop_write.go:9-33 loopMutations re-traverses the loop AST;
flow_loop_alias.go:193-378 markStmt/markNode... root already vetoed."

Next 8 minutes: the writer retired its own fresh code. Refactored onto the
single typedExit trunk. Three new constitution articles drafted on the spot —
no raw-AST helper summaries, no sync-treating async calls, three-way loop exit
split. At 13:41 a second interception: loop convergence tried re-entering
helper scans. Same constitution, blocked again. Summary + fixpoint convergence.

17:30 — the whole battle landed: commit 3059a60, 43 files, +8,100 lines.
