# CI build matrices

> Canonical C topic note — chapter 38.

## Definition
A CI build matrix systematically builds a project across meaningful dimensions such as compiler, language mode, target, optimization, library configuration, feature set, and warning/static-analysis policy.

## Mechanism and language rules
The matrix should target risk, not combinatorial explosion. Keep one authoritative production configuration and add dimensions that can expose portability or ABI defects. Typical axes include debug/release, multiple compiler versions, target variants, 32/64-bit hosts, and feature configurations.

## Embedded implications
For firmware, matrix builds can catch CPU/FPU mismatches, conditional-compilation drift, linker-script errors, configuration combinations that exceed memory budgets, and compiler-specific assumptions. Hardware-in-loop can cover a smaller set of high-value target configurations.

## Edge cases and failure modes
- Testing many combinations while missing the actual release configuration.
- Allowing matrix jobs to use different dependency versions.
- Ignoring size/timing regressions because compilation succeeds.
- Configuration-specific warnings being hidden.

## Verification / debugging
Define required gates per matrix dimension: compile, link, static analysis, unit tests, image-size limits, and target smoke tests. Archive logs and artifacts for failures.

## Staff-level takeaway
A CI matrix is a risk model. Select dimensions from known portability, safety, ABI, and product-configuration risks and ensure the exact release build is always exercised.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
