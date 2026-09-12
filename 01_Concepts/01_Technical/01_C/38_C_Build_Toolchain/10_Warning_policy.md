# Warning policy

> Canonical C topic note — chapter 38.

## Definition
A warning policy defines which compiler diagnostics are enabled, which are errors, which are reviewed exceptions, and how policy is kept consistent across configurations and toolchains. Warnings are implementation diagnostics, not ISO C requirements.

## Mechanism and language rules
Use strong baseline warnings, language-specific warnings, conversion/sign/format diagnostics, and toolchain-specific checks where justified. Separate third-party code from product code rather than globally disabling useful diagnostics.

## Embedded implications
Warnings catch truncation, signedness errors, missing prototypes, format mismatches, unreachable paths, and suspicious constructs before they reach hardware. Treating warnings as errors can prevent regressions but requires a controlled migration and documented exceptions.

## Edge cases and failure modes
- Global suppression hiding unrelated defects.
- New compiler versions turning diagnostics into build failures unexpectedly.
- Generated/vendor code polluting product warning budgets.
- Treating every warning as equally severe.

## Verification / debugging
Keep warning flags version-controlled. CI should build representative configurations and fail on policy violations. Suppress locally and narrowly, with a reason and preferably a toolchain-version scope.

## Staff-level takeaway
A warning policy is an engineering control: it reduces defect injection while keeping signal high. The goal is not zero text in the compiler log; it is zero unexplained diagnostic risk.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
