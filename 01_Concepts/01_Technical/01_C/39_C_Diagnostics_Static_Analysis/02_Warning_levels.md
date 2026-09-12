# Warning levels

## Definition
**Warning levels** are compiler option sets that control how broadly and aggressively suspicious constructs are diagnosed. Names such as `-Wall` and `-Wextra` are compiler-defined collections, not universal meanings of “all warnings.”

## Scope and boundaries
Warning options are implementation-specific. The same source may produce different diagnostics under GCC, Clang, IAR, Arm Compiler, or another toolchain. Treat the selected compiler and version as part of the warning-policy contract.

## Mechanism and language rules
A mature policy normally combines a high-value baseline with targeted warnings. For example:

```text
baseline -> correctness warnings -> project-specific warnings -> extensions
```

Then classify diagnostics as errors, review-required warnings, or accepted exceptions. Avoid copying flags blindly from another project because generated code, SDKs, and compiler versions differ.

## Embedded implications
Warnings for conversions, pointer casts, packed structures, implicit declarations, switch coverage, format strings, and uninitialized values are especially valuable in firmware. Architecture-specific warnings can expose assumptions that are safe on a 32-bit MCU but unsafe on another target.

## Edge cases and failure modes
- Assuming `-Wall` literally enables every warning.
- Treating warning-level names as portable between compilers.
- Enabling aggressive warnings without fixing or classifying existing findings.
- Applying application warning policy unchanged to generated/vendor code.
- Silencing a category because it produces too many findings without measuring residual risk.

## Verification / debugging
Record the exact flags in the compilation database and CI configuration. Periodically review compiler documentation for newly added diagnostics. Compare warning sets across supported toolchains and ensure critical categories have equivalent coverage where possible.

## Performance, memory, timing and power
Warning levels primarily affect diagnostics, not runtime behavior. However, warning-driven corrections can eliminate unsafe conversions and dead code. Some compiler options that look diagnostic-related may also alter language semantics or optimization; keep those distinct.

## Staff-level takeaway
Think in **diagnostic coverage**, not flag names. Define which defect classes the project must detect, then select and validate the compiler options that provide that coverage.