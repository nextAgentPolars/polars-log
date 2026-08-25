# Decision Summary

Root's broadcast, verbatim: "Preflight isn't a false red — three bypasses found
across Make / DAG / ref. Submission blocked. Luna is on root-cause fix. We do
not pass happy-path green off as a Gate."

Disposition: surface-green refused as a pass. Submission blocked. Gate rebuilt.
18:48 — rebuild landed: d39e014 "ci: add bounded repository preflight"
(new files scripts/preflight_root.py + scripts/root_preflight/, Makefile made
dynamic). The system found holes in its own enforcement tool and rebuilt the
tool instead of accepting the green.
