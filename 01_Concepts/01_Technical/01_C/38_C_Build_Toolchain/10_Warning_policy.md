# Warning policy

## Definition
A **warning policy** defines which compiler diagnostics are enabled, which are errors, which are reviewed exceptions, and how the policy evolves. Warnings are not merely stylistic feedback; many identify constructs that can lead to undefined behavior, portability problems, truncation, suspicious control flow, or API misuse.

## Scope and boundaries
Warnings are compiler diagnostics, not proof of correctness. A clean warning build can still contain runtime defects, and a warning can be a false positive or a deliberate extension. Policy should therefore combine compiler diagnostics with static analysis, testing, and code review.

## Mechanism and language rules
A strong baseline commonly includes high-value general warnings plus language-specific warnings, with compiler-version differences explicitly handled. Warning options should be scoped narrowly when suppression is necessary:

```c
/* Prefer fixing the root cause; localize unavoidable suppression. */
```

Treat warnings as a categorized risk signal: correctness, portability, maintainability, generated-code noise, or intentional extension.

## Embedded implications
Embedded builds should pay particular attention to integer conversions, sign changes, format strings, pointer casts, alignment, unreachable code, missing prototypes, enum handling, initialization, and implicit declarations. A new compiler version may emit new diagnostics; the policy must distinguish genuine regressions from toolchain noise.

Third-party/vendor code can be built under a different warning policy, but the boundary and justification should be explicit.

## Edge cases and failure modes
- `-w` or equivalent globally disables useful diagnostics.
- `-Werror` is applied blindly to generated/vendor code and blocks builds.
- Local suppressions outlive the defect that motivated them.
- Warning output changes because the build used a different compiler mode.
- A warning is silenced without recording why it is safe.

## Verification / debugging
Version-control the warning flags. Run clean builds in CI and record compiler version. Track warning counts and categories. Review every suppression with owner, reason, scope, and expiry/revalidation criteria.

## Performance, memory, timing and power
Warnings generally do not affect generated code, but some diagnostic-related options or optimization/debug combinations can. More importantly, warning-driven fixes often remove accidental conversions or unreachable paths that otherwise affect correctness and performance.

## Staff-level takeaway
A warning policy is a **risk-management system**. Keep the signal high, make exceptions explicit, and ensure the build fails on defects that the organization has decided are unacceptable.