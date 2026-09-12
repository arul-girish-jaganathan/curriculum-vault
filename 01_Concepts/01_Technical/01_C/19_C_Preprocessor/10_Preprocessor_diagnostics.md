# 10: Preprocessor Diagnostics

## Definition
Preprocessor diagnostics (`#error`, `#warning`, and `#line`) allow developers to control compiler messaging and line mapping directly from the preprocessor. `#error` halts compilation immediately with a specified diagnostic message, while `#warning` emits a non-fatal warning message without terminating the build.

## Scope and Boundaries
Covers: `#error` termination semantics, `#warning` usage, compile-time architectural contract verification, and the `#line` directive.
Does not cover: C11 `_Static_assert` (which evaluates AST constant expressions, not preprocessor tokens).

## Why Does It Exist
Firmware configurations depend on delicate dependencies: hardware clock speeds, bus bandwidths, compatible board revisions, and valid buffer sizes. Preprocessor diagnostics allow the build system to fail fast at the earliest possible stage (Phase 4) with clear, actionable error messages before the compiler attempts semantic analysis.

## Mechanism and Language Rules
1. **`#error` Directive:** Emits the specified sequence of tokens as an error message to `stderr` and terminates compilation immediately.
2. **`#warning` Directive:** Standardized in ISO C23 (and long supported as a compiler extension in GCC, Clang, and MSVC), emits a diagnostic message and continues compilation.
3. **`#line` Directive (§6.10.4):** Changes the preprocessor's internal tracking of `__LINE__` and `__FILE__`:
   `#line 100 "generated_parser.c"`
   Primarily used by code generators (Lex, Yacc, Protobuf) so compiler errors point back to the original generator template.

## Examples
```c
#include <stdint.h>

/* Architectural Configuration Validation */
#if !defined(SYSTEM_CORE_CLOCK_HZ)
    #error "SYSTEM_CORE_CLOCK_HZ must be defined by the board configuration header!"
#elif (SYSTEM_CORE_CLOCK_HZ < 8000000UL)
    #error "Core clock cannot run below 8 MHz for USB operations!"
#endif

/* Preventing Illegal Configuration Combinations */
#if defined(USE_FREERTOS) && defined(USE_THREADX)
    #error "Conflicting RTOS targets: Both USE_FREERTOS and USE_THREADX are defined!"
#endif

/* Deprecation Warnings (C23 or GNU extension) */
#if defined(USE_LEGACY_SPI)
    #warning "USE_LEGACY_SPI is deprecated and will be removed in release v3.0!"
#endif
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- The exact format of the output string emitted by `#error` or `#warning` is implementation-defined, but always contains the user-supplied message tokens.

## Edge Cases and Failure Modes
- **Premature Evaluation:** Attempting to validate struct sizes with `#error` (e.g., `#if sizeof(my_struct_t) > 64 #error ...`) will fail because `sizeof` does NOT exist during preprocessing. Use C11 `_Static_assert` for type and size validations.
- **Unquoted Apostrophes:** Certain compilers handle apostrophes inside unquoted `#error` messages as unclosed character constants (e.g., `#error Can't allocate memory` may fail to parse). Enclose complex messages carefully or avoid unescaped single quotes.

## Embedded Implications
- **Clock Tree Consistency:** In modern microcontrollers (e.g., STM32, ESP32), PLL configuration depends on external crystal (HSE) values. Guarding against illegal HSE frequencies with `#error` prevents flashing firmware with broken UART baud rates.

## Firmware Review Angle
- Verify that every `#if` checking target boards, memory budgets, or clock rates has an `#else #error "Invalid configuration"` fallback.
- Avoid leaving unaddressed `#warning` diagnostics in production build logs.

## Compiler, ABI, and Toolchain Implications
- `#error` halts compilation during Translation Phase 4; no object file (`.o`) is generated.

## Performance, Memory, Timing, and Power
- Absolute zero impact on the binary image. Diagnostic directives are entirely resolved and discarded during preprocessing.

## Verification / Debugging
- Write unit tests for configuration headers by deliberately supplying invalid macro definitions and asserting that the build fails with the expected `#error` message.

## Safety, Security, and Reliability
- Complies with ISO 26262 and DO-178C build verification requirements by enforcing strict compile-time validation of safety configuration invariants.

## Trade-offs and Alternatives
- **`#error` vs. `_Static_assert`:**
  - Use `#error` when checking preprocessor definitions, file inclusions, and macro presence.
  - Use C11 `_Static_assert` when checking types, `sizeof`, struct member offsets, and enum values.

## Staff-Level Takeaway
Fail fast at compile time. Use `#error` liberally in configuration headers to validate mutual exclusivity of options, enforce hardware prerequisites, and protect clock configurations. Reserve `#warning` for deprecation notices, and let `_Static_assert` handle type-aware assertions.

## Related Concepts
- `03_Conditional_inclusion`
- `06_Predefined_macros`
- `../16_C_Struct_Union_Enum/01_Structure_layout`
