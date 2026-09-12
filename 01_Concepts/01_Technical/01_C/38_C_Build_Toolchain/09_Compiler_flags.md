# Compiler flags

> Canonical C topic note — chapter 38.

## Definition
Compiler flags select language mode, diagnostics, optimization, target ISA, ABI, preprocessing, debug information, sanitization, and code-generation behavior. They are part of the build contract.

## Mechanism and language rules
Flags such as language standard selection, warnings, optimization level, target CPU/FPU, debug info, LTO, section generation, and floating-point model can change both accepted source and generated code. Some flags alter assumptions the compiler may make about the environment.

## Embedded implications
Flags must be centralized and reviewable. CPU/FPU flags affect instruction legality and ABI; optimization affects timing and size; section flags affect linker garbage collection; language extensions affect portability. Per-file flag exceptions should have documented reasons.

## Edge cases and failure modes
- Compiling one module with a different ABI.
- Debug and release using different language semantics.
- Enabling fast-math-like assumptions where numerical behavior matters.
- Suppressing warnings globally.
- Forgetting that generated libraries were built with different target flags.

## Verification / debugging
Capture complete command lines and compiler predefined macros. Compare compile databases and final ELF attributes. Maintain a reviewed flag policy and test configuration variants in CI.

## Staff-level takeaway
Flags are source-code-adjacent architecture. A build cannot be reproduced or audited if important compiler assumptions live only in an engineer's workstation configuration.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
