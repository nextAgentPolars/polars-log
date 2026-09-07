# Polaris Bootstrap Log

[中文](README.md) · **English**

**How are AI agents building Polaris? This repository shares the decisions, code changes, verification records, and evidence from that work.**

Polaris is a Go task-governance platform. This log follows a Codex coordinating agent and worker agents as they develop the project under its governance rules. See [thePolarsMethodology](https://github.com/nextAgentPolars/thePolarsMethodology) for the ideas behind the approach, or [demo-repository](https://github.com/nextAgentPolars/demo-repository) to try the mechanisms yourself.

## Latest addition: August 25–September 2

The [batch published on September 7, 2026](batches/2026-09-07-continuation/README.md) includes:

- Metadata for 399 commits—not a claim that 399 tasks were completed.
- Three selected events: staged SQL proofs, Candidate Material R3→R4, and acceptance of first-boot Source promotion.
- Original code diffs and historical completion records, with source references, time anchors, and file hashes.

This is an incremental evidence batch, **not a complete session archive for that period**. Publishing it did not involve rerunning the project's tests or auditing the number of human technical interventions. Some materials within the batch are currently available only in Chinese.

## The original record: seven events

The original batch dates the start of the run to **August 23, 2026, at 23:30 Beijing time (UTC+8)** and reports no human technical intervention within its scope. That is the original batch's claim—not a finding that every later period has received the same audit. See [PROVENANCE.md](PROVENANCE.md) for sources, coverage corrections, and known gaps.

| Event | What happened |
|---|---|
| [01 · Kickoff](cot_archive/2026-08-23_2330_m0_kickoff/decision_summary.en.md) | The run began, with the initial human input and direction recorded. |
| [02 · Merge after two checks](cot_archive/2026-08-24_1059_dual_gate_merge/decision_summary.en.md) | Foundational changes were held until both required checks passed. |
| [03 · A second CFG rejected](cot_archive/2026-08-24_1320_second_cfg_veto/decision_summary.en.md) | A duplicate control-flow implementation was rejected and fresh code retired; a later review also blocked helper re-entry. |
| [04 · Auditing the preflight itself](cot_archive/2026-08-24_1741_preflight_self_audit/decision_summary.en.md) | The system found ways around its own checks and rebuilt them. |
| [05 · A naming-rule workaround blocked](cot_archive/2026-08-24_2131_naming_gate_circumvention/decision_summary.en.md) | A proposal to evade naming rules through test aliases was stopped. |
| [06 · Stronger structural checks](cot_archive/2026-08-25_0007_ast_gate_upgrade/decision_summary.en.md) | A string-based check could be fooled by comments. It was replaced with syntax-tree checks of where declarations belonged. |
| [07 · Event identity implemented](cot_archive/2026-08-25_0956_event_identity_landing/decision_summary.en.md) | A digest-based event identity contract was added, including conflict flags. |

Each event directory contains a `time-anchor.md` and decision summaries in both languages. Start with a summary, then use its time anchor to inspect the evidence; you do not need to read the entire archive first.

## Where to find the evidence

- `cot_archive/`: selected historical decision events—a reading guide, not complete coverage.
- `timeline/`: human messages, coordinating-agent updates, and daily records.
- `raw_cot/`: reasoning summaries published with the historical batch, not full hidden chain-of-thought.
- `artifacts/`: examples and supporting material. Constructed fixtures must be distinguished from runtime exports.
- `batches/`: later additions with explicit coverage and manifests.
- [PROVENANCE.md](PROVENANCE.md): sources, audit corrections, and missing evidence.
- [PUBLICATION.md](PUBLICATION.md): rules for incremental publication, redaction, and verification.

## How to read the claims

Timestamps, diffs, and hashes make evidence traceable. They do not, by themselves, establish correctness or completeness. A historical test result is not a fresh test run, and source code is not proof of deployment. Retrospective commentary must remain distinct from original artifacts.

You can check commits against [Polaris1933/beijixing](https://github.com/Polaris1933/beijixing) if you have access. Otherwise, you can inspect the artifacts included here, but hashes alone do not independently establish the authenticity of a private source repository.

Historical redaction rules exclude system instructions, internal protocols, and encrypted payloads. Later batches state their own selection rules and gaps. Pattern scans are not a guarantee that no sensitive material remains.

Know of an earlier comparable public record? Open an issue with evidence others can check.

## Terms of use

Records and code excerpts follow the source repository's licensing terms, with Apache-2.0 provenance. Historical reasoning summaries are published for verification and research; model training requires written permission.
