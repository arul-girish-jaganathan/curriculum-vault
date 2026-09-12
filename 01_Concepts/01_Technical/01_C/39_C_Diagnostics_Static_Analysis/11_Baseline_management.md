# Baseline management

## Definition
A **static-analysis baseline** records accepted existing findings so teams can enforce “no new defects” while paying down legacy debt incrementally. Baselines are useful for large C codebases where immediate cleanup of every historical warning is impractical.

## Scope and boundaries
A baseline is not an exemption from analysis. It should be tied to a specific source revision, analyzer version, configuration, and finding identity. New findings must remain visible even when old findings are tolerated.

## Mechanism and language rules
A practical model is:

```text
legacy findings -> baseline
new/changed findings -> quality gate
fixed legacy findings -> removed from baseline
```

Baseline entries should ideally be stable by rule, file, location, and diagnostic identity rather than fragile textual matching.

## Embedded implications
Long-lived firmware repositories accumulate vendor code, legacy drivers, generated files, and historical deviations. A baseline lets the team introduce stronger MISRA/CERT/static-analysis policy without blocking all development, while still preventing regression in actively changed modules.

## Edge cases and failure modes
- Baseline is silently refreshed on every build and therefore never shrinks.
- Analyzer upgrade causes all findings to appear “new.”
- Findings are moved rather than fixed to game the baseline.
- Baseline contains high-severity defects with no remediation plan.
- Generated/vendor code is mixed with application findings.

## Verification / debugging
Version the baseline and analyzer configuration. Require review for baseline changes. Track counts and severity over time. Prefer ownership and expiry for high-risk entries. Re-baseline only as a deliberate migration event with a documented comparison.

## Performance, memory, timing and power
Baselines primarily improve engineering throughput and CI adoption. They have no firmware runtime cost.

## Staff-level takeaway
Use baselines as a **migration mechanism, not a permanent landfill**. The quality trend should move toward fewer accepted findings, while the gate prevents new debt.