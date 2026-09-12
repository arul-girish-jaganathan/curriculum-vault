# 03: Conditional Inclusion

## Definition
Conditional inclusion directives (`#if`, `#ifdef`, `#ifndef`, `#elif`, `#else`, `#endif`) control whether blocks of source code text are passed to the compiler or stripped from the compilation stream. Conditions are evaluated during preprocessing using integer constant expressions.

## Scope and Boundaries
Covers: Arithmetic preprocessor expressions, `#ifdef` vs `#if defined()`, short-circuit logic, integer promotion rules during preprocessing, and target feature selection.
Does not cover: Runtime `if` statements or dead-code elimination by compiler optimization passes.

## Why Does It Exist
Embedded software must target heterogeneous hardware boards, chip silicon revisions, debug/release configurations, and testing environments from a single unified codebase. Conditional inclusion allows selective compilation of hardware-specific code without memory or runtime overhead.

## Mechanism and Language Rules
1. **Pre-processing Numbers:** In `#if` and `#elif` directives, integer constant expressions are evaluated. Variables, structs, and `sizeof` DO NOT exist; any identifier that is not a macro resolves implicitly to `0`.
2. **Integer Promotions:** All preprocessor arithmetic is evaluated using the widest supported integer types (`intmax_t` and `uintmax_t` in C99).
3. **The `defined` Operator:** `defined(MACRO)` evaluates to `1` if `MACRO` is currently defined, and `0` otherwise. Allows compound logical expressions (`#if defined(A) && !defined(B)`).
4. **Short-Circuit Evaluation:** Preprocessor logical operators `&&` and `||` short-circuit identically to runtime C expressions.

## Examples
```c
#include <stdint.h>

#define BOARD_REV_A  1
#define BOARD_REV_B  2
#define TARGET_BOARD BOARD_REV_B

/* Clean conditional compilation with defined() */
#if defined(DEBUG) && (DEBUG > 0)
    #define LOG_DEBUG(msg) print_serial("[DEBUG] " msg "
")
#else
    #define LOG_DEBUG(msg) ((void)0)
#endif

/* Multi-branch board configuration */
#if (TARGET_BOARD == BOARD_REV_A)
    #define PIN_STATUS_LED  12u
#elif (TARGET_BOARD == BOARD_REV_B)
    #define PIN_STATUS_LED  15u
#else
    #error "Invalid or undefined TARGET_BOARD!"
#endif
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **The Implicit Zero Trap:** In an `#if` expression, an undefined identifier is silently replaced with `0`. If a typo occurs (e.g., `#if TYPO_FLAG`), the branch evaluates to false without any compiler warning.
- **Undefined Expansion of `defined`:** Using `defined` inside macro expansions (e.g., `#define IS_DEF(x) defined(x)`) exhibits Undefined Behavior in ISO C99 §6.10.1.

## Edge Cases and Failure Modes
- **`#ifdef` on Value Zero:**
  ```c
  #define ENABLE_FEATURE 0
  #ifdef ENABLE_FEATURE
      /* SURPRISE: This code COMPILES! ENABLE_FEATURE is defined! */
      run_feature();
  #endif
  ```
  Using `#ifdef` tests definition, NOT boolean truth. Always use `#if ENABLE_FEATURE` or `#if (ENABLE_FEATURE == 1)`.

## Embedded Implications
- **Compile-Time Feature Selection:** Firmware images for 32KB flash MCUs cannot afford to link unused drivers. Conditional compilation ensures inactive peripheral code (e.g., CAN, USB) is stripped entirely before compilation, consuming zero flash bytes.

## Firmware Review Angle
- Check for `#ifdef` used on macros assigned numeric boolean values (`#define FOO 0`). Enforce `#if FOO` or `#if (FOO != 0)`.
- Use `-Wundef` compiler flag to treat undefined identifiers inside `#if` expressions as build-breaking errors.
- Ensure every conditional inclusion block terminates with clear end-comments: `#endif /* TARGET_BOARD */`.

## Compiler, ABI, and Toolchain Implications
- Code eliminated by conditional inclusion is discarded prior to parsing; syntax errors and invalid identifiers inside excluded blocks will never trigger compiler errors (unless the preprocessor syntax itself is malformed).

## Performance, Memory, Timing, and Power
- Zero runtime impact. Code inside false branches contributes zero bytes to RAM/Flash.

## Verification / Debugging
- Use `unifdef` command-line utility to simplify and audit deeply nested conditional codebases.
- GCC/Clang: `-dD` outputs active macro definitions alongside preprocessed code.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.9: All identifiers used in the controlling expression of `#if` or `#elif` preprocessing directives shall be subject to evaluation under operand `defined`. (Strictly enforce `-Wundef`).
- MISRA C:2012 Rule 20.14: All `#else`, `#elif` and `#endif` preprocessor directives shall reside in the same file as the `#if` or `#ifdef` directive to which they are related.

## Trade-offs and Alternatives
- **`#if` vs `if (DEBUG_BUILD)`:** C99 static dead-code elimination via `if (IS_ENABLED(FEATURE))` provides compiler type-checking of both branches while still discarding unreferenced code during optimization, avoiding "bit-rot" in uncompiled branches.

## Staff-Level Takeaway
Never use `#ifdef` for boolean configuration flags. Use numeric definition (`#define ENABLE_FEATURE 1` / `0`), enable `-Wundef` to catch spelling errors, and prefer compile-time C expressions (`if (FEATURE_ENABLED)`) where code bloat allows to prevent bit-rot in dormant code paths.

## Related Concepts
- `01_File_inclusion`
- `07_Feature_detection`
- `10_Preprocessor_diagnostics`
