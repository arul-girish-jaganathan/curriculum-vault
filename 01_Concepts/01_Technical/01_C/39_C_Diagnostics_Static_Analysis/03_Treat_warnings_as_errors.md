# Treat warnings as errors

## Definition
Treating warnings as errors makes selected compiler diagnostics build-blocking. The policy turns known defect classes into explicit quality gates rather than allowing them to accumulate as background noise.

## Scope and boundaries
`-Werror`-style mechanisms are compiler-specific. They should be applied deliberately because compiler upgrades can introduce new diagnostics and third-party code can have different ownership. The goal is not “never see a warning”; it is “do not ship unresolved diagnostics that the project has classified as unacceptable.”

## Mechanism and language rules
A useful policy separates:

```text
fatal diagnostics -> review-required warnings -> documented exceptions
```

Use specific promotion/demotion controls where supported. Keep suppressions narrow and close to the code or build boundary that requires them.

## Embedded implications
For safety- or reliability-sensitive firmware, warnings about implicit declarations, incompatible pointers, truncation, sign changes, format mismatches, unreachable code, and missing initialization should generally be high priority. A build that silently tolerates these can ship target-specific corruption.

Generated code and vendor SDKs may require separate compilation policies. Do not weaken the application's entire warning set merely to accommodate them.

## Edge cases and failure modes
- A new compiler release breaks CI because every newly introduced warning is promoted.
- Developers disable `-Werror` locally and never notice regressions.
- A broad suppression hides unrelated warnings.
- Legacy debt is so large that teams stop treating warnings as meaningful.
- A warning is “fixed” with an unsafe cast.

## Verification / debugging
Establish a baseline, then reduce warnings until the project reaches a clean state. For upgrades, review new diagnostics separately. Make CI reproduce the same flags used for release and publish the warning log for traceability.

## Performance, memory, timing and power
The policy itself has little runtime cost. Its value is preventing defects that can become timing, memory, or correctness failures. Keeping builds clean also makes compiler diagnostics during optimization and target migration more actionable.

## Staff-level takeaway
`-Werror` is effective only when paired with **ownership and exception discipline**. Promote high-confidence defect classes, isolate external code, and make the release build the authoritative gate.