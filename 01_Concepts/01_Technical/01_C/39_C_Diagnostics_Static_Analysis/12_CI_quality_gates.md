# CI quality gates

## Definition
**CI quality gates** turn engineering requirements into automated build or analysis conditions that must pass before code can merge or release. For C firmware, gates commonly cover compilation warnings, static analysis, tests, sanitizers, coverage, size budgets, and artifact integrity.

## Scope and boundaries
A gate should measure a defined risk, have deterministic inputs, and produce an actionable failure. Gates that are routinely bypassed lose their value. Not every diagnostic belongs in a hard gate; severity and ownership should be explicit.

## Mechanism and language rules
A layered pipeline can be:

```text
compile -> warnings -> static analysis -> unit tests -> sanitizers
       -> target build -> size/map checks -> integration/release tests
```

Use changed-code gates for fast feedback and full-suite gates for release confidence.

## Embedded implications
Useful firmware gates include zero new high-severity static-analysis findings, clean release warnings, flash/RAM budgets, successful linker assertions, ABI compatibility checks, boot-image validation, and host sanitizer tests. Hardware-in-loop jobs can cover target-only properties such as MMIO, interrupts, DMA, and timing.

## Edge cases and failure modes
- CI tests only the host build.
- Gates use different compiler flags than release.
- A flaky hardware test is ignored until it becomes meaningless.
- Size limits are checked only after release packaging.
- Static-analysis baselines allow regressions.

## Verification / debugging
Every gate should publish its inputs and outputs: tool versions, flags, source revision, logs, reports, firmware hash, and map/size data. Make failures reproducible locally where practical. Track gate health and time-to-fix rather than simply counting pipeline failures.

## Performance, memory, timing and power
CI gates add build time, but early failure reduces integration cost. Size and timing regression tests directly protect firmware resource budgets. Cache immutable dependencies without allowing stale build inputs to bypass the dependency graph.

## Staff-level takeaway
Quality gates are **automated policy enforcement**. Start with high-value risks, keep results trustworthy, and make the release pipeline stricter than—not different from—the developer build.