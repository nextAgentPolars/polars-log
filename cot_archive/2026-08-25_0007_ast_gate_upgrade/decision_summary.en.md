# Decision Summary

Root's broadcasts, verbatim (two stages):
"Round 5: features, budget, production, preflight all green — but the structure
gate blocked the commit. Pure binary-expression control got stuffed into
call_schedule.go. Doing a clean owner split, no semantic changes."
"The owner split itself was correct — but Round 6 found its structure test only
matches strings and can be forged by comments. Upgrading to a Go AST
declaration-ownership gate. Production code unchanged."

Two levels in one slice: first the gate caught an owner-boundary violation,
then it caught its own test being forgeable, and hardened itself to AST level.
