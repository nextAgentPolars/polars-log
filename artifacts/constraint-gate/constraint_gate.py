# constraint-gate — P3 for LLM outputs

# The missing layer: deterministic constraint verification for LLM outputs.
# Not post-hoc human review. Not model self-check. Mechanical gates.

# Design based on Polaris P1-P5:
#   P3 (verifiable closure): every output must pass computable checks
#   Coverage axiom: checks must cover the constraint set
#   CEDS: syndrome (set of check results) determines if output is in valid subspace

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
import re


class Verdict(Enum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"  # cannot determine — prefer unknown over false precision


@dataclass
class ConstraintResult:
    constraint_id: str
    verdict: Verdict
    detail: str
    evidence: Optional[str] = None  # the exact span that passed/failed


@dataclass
class GateReport:
    output: str
    results: list[ConstraintResult]
    passed: bool
    unknown_count: int
    fail_count: int

    @property
    def syndrome(self) -> str:
        """CEDS syndrome: binary vector of check results."""
        return "".join(
            "1" if r.verdict == Verdict.PASS
            else "0" if r.verdict == Verdict.FAIL
            else "?"
            for r in self.results
        )


class Constraint(ABC):
    """Base class for all mechanically verifiable constraints."""

    def __init__(self, cid: str, description: str):
        self.cid = cid
        self.description = description

    @abstractmethod
    def check(self, output: str, context: dict[str, Any]) -> ConstraintResult:
        """Deterministically verify output against this constraint.
        Must NOT use an LLM. Must be computable in bounded time."""
        ...


class RegexConstraint(Constraint):
    """Output must (not) match a pattern."""

    def __init__(self, cid: str, description: str, pattern: str,
                 should_match: bool, flags: int = 0):
        super().__init__(cid, description)
        self.pattern = re.compile(pattern, flags)
        self.should_match = should_match

    def check(self, output: str, context: dict) -> ConstraintResult:
        m = self.pattern.search(output)
        found = m is not None
        if self.should_match:
            if found:
                return ConstraintResult(self.cid, Verdict.PASS, "pattern found", m.group(0)[:100])
            return ConstraintResult(self.cid, Verdict.FAIL, "pattern not found")
        else:
            if not found:
                return ConstraintResult(self.cid, Verdict.PASS, "pattern absent (correct)")
            return ConstraintResult(self.cid, Verdict.FAIL, "forbidden pattern found", m.group(0)[:100])


class LineCountConstraint(Constraint):
    """Output must have between min_lines and max_lines lines."""

    def __init__(self, cid: str, description: str, min_lines: int, max_lines: int):
        super().__init__(cid, description)
        self.min = min_lines
        self.max = max_lines

    def check(self, output: str, context: dict) -> ConstraintResult:
        lines = len(output.strip().split("\n"))
        if self.min <= lines <= self.max:
            return ConstraintResult(self.cid, Verdict.PASS, f"{lines} lines in [{self.min},{self.max}]")
        return ConstraintResult(self.cid, Verdict.FAIL, f"{lines} lines outside [{self.min},{self.max}]")


class RequiredSectionConstraint(Constraint):
    """Output must contain all required section headers."""

    def __init__(self, cid: str, description: str, sections: list[str]):
        super().__init__(cid, description)
        self.sections = sections

    def check(self, output: str, context: dict) -> ConstraintResult:
        missing = [s for s in self.sections if s not in output]
        if not missing:
            return ConstraintResult(self.cid, Verdict.PASS, "all sections present")
        return ConstraintResult(self.cid, Verdict.FAIL, f"missing sections: {missing}")


class NoLeakConstraint(Constraint):
    """Output must not contain credential patterns."""

    PATTERNS = [
        re.compile(r"sk-[A-Za-z0-9_-]{15,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.eyJ"),
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY"),
        re.compile(r"(?i)(password|secret|api_key|token|credential)\s*[:=]\s*\S{8,}"),
        re.compile(r"(?i)admin[_\s]?(password|secret|key)\s*[:=]?\s*\S{4,}"),
        re.compile(r"ghp_[A-Za-z0-9]{36,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{22,}"),
    ]

    def __init__(self, cid: str = "no-leak", description: str = "no credential leakage"):
        super().__init__(cid, description)

    def check(self, output: str, context: dict) -> ConstraintResult:
        for pat in self.PATTERNS:
            m = pat.search(output)
            if m:
                return ConstraintResult(self.cid, Verdict.FAIL, "credential pattern detected", m.group(0)[:20])
        return ConstraintResult(self.cid, Verdict.PASS, "no credential patterns")


class StructuredJSONConstraint(Constraint):
    """Output must be valid JSON with required top-level keys."""

    def __init__(self, cid: str, description: str, required_keys: list[str]):
        super().__init__(cid, description)
        self.required_keys = required_keys

    def check(self, output: str, context: dict) -> ConstraintResult:
        import json
        # strip markdown code fences
        text = output.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            return ConstraintResult(self.cid, Verdict.FAIL, f"invalid JSON: {e}")
        if not isinstance(data, dict):
            return ConstraintResult(self.cid, Verdict.FAIL, "not a JSON object")
        missing = [k for k in self.required_keys if k not in data]
        if missing:
            return ConstraintResult(self.cid, Verdict.FAIL, f"missing keys: {missing}")
        return ConstraintResult(self.cid, Verdict.PASS, "valid JSON with required keys")


class SemanticLengthConstraint(Constraint):
    """Output must not exceed a token estimate (proxy for budget enforcement)."""

    def __init__(self, cid: str, description: str, max_tokens: int):
        super().__init__(cid, description)
        self.max_tokens = max_tokens

    def check(self, output: str, context: dict) -> ConstraintResult:
        # rough estimate: 1 token ≈ 4 chars for English
        est = len(output) // 4
        if est <= self.max_tokens:
            return ConstraintResult(self.cid, Verdict.PASS, f"~{est} tokens ≤ {self.max_tokens}")
        return ConstraintResult(self.cid, Verdict.FAIL, f"~{est} tokens > {self.max_tokens} budget")


# ─── The Gate itself ───

class ConstraintGate:
    """
    P3 for LLM outputs: deterministic, mechanical, model-independent.

    The gate does NOT use an LLM. It does NOT depend on model attention.
    It runs the SAME regardless of context length, model capability,
    or how many tokens have been generated. This is the key difference
    from all model-side approaches: the gate's reliability is CONSTANT.
    """

    def __init__(self, constraints: list[Constraint]):
        self.constraints = constraints

    def evaluate(self, output: str, context: dict[str, Any] | None = None) -> GateReport:
        ctx = context or {}
        results = []
        for c in self.constraints:
            try:
                r = c.check(output, ctx)
            except Exception as e:
                r = ConstraintResult(c.cid, Verdict.UNKNOWN, f"check error: {e}")
            results.append(r)

        fails = sum(1 for r in results if r.verdict == Verdict.FAIL)
        unknowns = sum(1 for r in results if r.verdict == Verdict.UNKNOWN)

        return GateReport(
            output=output,
            results=results,
            passed=fails == 0,  # unknown doesn't block, but is reported
            unknown_count=unknowns,
            fail_count=fails,
        )


# ─── Demo ───

if __name__ == "__main__":
    # Simulated LLM outputs — three scenarios
    good_output = """
## Analysis

The authentication module uses JWT tokens with 24-hour expiry.

## Implementation

The middleware validates the token on each request.

## Summary

Security review passed with no credential exposure.
"""

    bad_output = """
Here's the config you need:

```json
{"api_key": "sk-proj-abcd1234efgh5678ijkl", "endpoint": "https://api.internal.corp"}
```

Let me also include the admin password: admin_secret_2026

And the full trace shows the request went to 192.168.1.100:8080.
"""

    drifty_output = """
The authentication module uses JWT tokens.

## Implementation

The middleware handles validation. The system also includes rate limiting,
logging, monitoring, alerting, dashboards, metrics, tracing, profiling,
load balancing, circuit breakers, retry logic, exponential backoff,
connection pooling, health checks, readiness probes, liveness probes,
graceful shutdown, signal handling, configuration management, secret
rotation, key management, certificate management, TLS termination,
CORS headers, CSP headers, rate limiting per user, rate limiting per IP,
request validation, response sanitization, output encoding, input decoding,
error handling, exception handling, stack trace sanitization, debug mode
toggle, feature flags, A/B testing, analytics tracking, user tracking,
session management, cookie handling, CSRF protection, XSS prevention,
SQL injection prevention, NoSQL injection prevention, command injection
prevention, path traversal prevention, file upload validation, file type
checking, file size limiting, image processing, thumbnail generation,
media transcoding, caching, cache invalidation, cache warming, CDN
configuration, edge computing, serverless functions, microservices,
message queues, event streaming, websocket connections, Server-Sent Events,
long polling, short polling, real-time updates, batch processing, stream
processing, map-reduce, distributed computing, consensus algorithms,
leader election, distributed locking, distributed transactions, saga
patterns, compensating transactions, eventual consistency, strong
consistency, CAP theorem, BASE theorem, ACID guarantees.
"""

    # Define constraints (the "constitution" for this output type)
    gate = ConstraintGate([
        NoLeakConstraint(),
        RegexConstraint(
            "has-sections", "must contain Analysis, Implementation, Summary sections",
            r"## Analysis.*## Implementation.*## Summary",
            should_match=True, flags=re.DOTALL
        ),
        LineCountConstraint("line-budget", "must be 5-20 lines", 5, 20),
        SemanticLengthConstraint("token-budget", "must be under 200 tokens", 200),
        RegexConstraint(
            "no-internal-ips", "must not expose internal IPs",
            r"\b192\.168\.\d+\.\d+:\d+\b",
            should_match=False
        ),
    ])

    for name, output in [("CLEAN", good_output), ("LEAKING", bad_output), ("DRIFTED", drifty_output)]:
        report = gate.evaluate(output)
        syndrome = report.syndrome
        status = "✅ PASS" if report.passed else "❌ FAIL"
        print(f"\n{'='*50}")
        print(f"  {name}: {status}  syndrome={syndrome}")
        print(f"  fails={report.fail_count} unknowns={report.unknown_count}")
        print(f"{'='*50}")
        for r in report.results:
            icon = {"pass": "✓", "fail": "✗", "unknown": "?"}[r.verdict.value]
            print(f"  {icon} [{r.constraint_id}] {r.detail}")
            if r.evidence:
                print(f"    evidence: {r.evidence}")
