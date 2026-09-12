# Feature-Test Macros

Feature-test macros are preprocessor controls used by implementations and libraries to select declarations, interfaces or extensions available under a requested environment. They are implementation/library mechanisms, not a universal ISO C language feature-selection system.

## Why they matter
An embedded build may combine a language standard mode with a vendor libc, POSIX-like layer, RTOS headers and compiler extensions. A macro can change which declarations are visible or which API variant is selected. That makes build configuration part of the effective source interface.

## Critical distinction
Do not confuse:
- the C language standard version selected by the compiler;
- implementation-defined feature macros supplied by the compiler;
- library/platform feature-test macros;
- project-defined configuration macros.

Each has a different authority and compatibility model.

## Good practice
Centralize platform configuration where practical, document required feature macros, and avoid defining implementation-owned macros casually. If a header's API depends on a macro, make that dependency explicit in the build contract.

## Failure modes
Changing include order or compiler flags can expose a different declaration set. A macro mismatch can produce missing prototypes, incompatible declarations, or silently different APIs. In cross-compilation, the host headers and target headers must never be treated as interchangeable.

## Verification
Capture the compiler command line and preprocess representative translation units with `-E` or the toolchain equivalent. Inspect the resulting declarations when diagnosing configuration-dependent behavior.

## Staff-level view
Configuration is code. Reproducible builds require feature-selection inputs to be versioned, reviewable and testable rather than hidden in developer-machine defaults.

## Related
- [[05_C23_modernization]]
- [[07_Hosted_vs_freestanding]]
- [[38_C_Build_Toolchain]]
