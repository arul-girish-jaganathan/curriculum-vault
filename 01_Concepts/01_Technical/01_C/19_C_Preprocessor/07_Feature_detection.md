# 07: Feature Detection

## Definition
Feature detection macros are built-in preprocessor operators and predefined identifiers that allow code to introspect the capabilities of the compiler and standard library at compile time. Standardized across modern C and C++ (e.g., `__has_include`, `__has_builtin`, `__has_attribute`, `__has_feature`), they eliminate fragile compiler-version checks in favor of capability-based compilation.

## Scope and Boundaries
Covers: `__has_include`, `__has_builtin`, `__has_attribute`, compiler portability wrappers, and version-checking anti-patterns.
Does not cover: Build-system feature testing (e.g., CMake `check_include_file`).

## Why Does It Exist
Historically, portable code was littered with brittle version comparisons like `#if defined(__GNUC__) && (__GNUC__ > 4 || (__GNUC__ == 4 && __GNUC_MINOR__ >= 8))`. Feature detection allows direct, toolchain-agnostic queries about specific capabilities (e.g., does this compiler support `<stdatomic.h>` or `__builtin_clz`?).

## Mechanism and Language Rules
1. **`__has_include` (C23 / Modern Extension):** Evaluates to `1` in preprocessor conditionals if the specified header can be found and opened, `0` otherwise:
   `#if __has_include(<stdatomic.h>)`.
2. **`__has_builtin` (Clang / GCC 10+):** Evaluates to `1` if the compiler supports a specific intrinsic function:
   `#if __has_builtin(__builtin_bswap32)`.
3. **`__has_attribute`:** Evaluates to `1` if the compiler supports a specific GNU-style attribute (e.g., `packed`, `aligned`).
4. **Fallback Guard Idiom:** To prevent errors on older compilers that do not support feature detection operators, always define fallback stubs before evaluating them.

## Examples
```c
#include <stdint.h>

/* Safe compatibility shim for feature detection */
#ifndef __has_builtin
    #define __has_builtin(x) 0
#endif

#ifndef __has_include
    #define __has_include(x) 0
#endif

#ifndef __has_attribute
    #define __has_attribute(x) 0
#endif

/* Portable Byte-Swap Implementation */
static inline uint32_t portable_bswap32(uint32_t val) {
#if __has_builtin(__builtin_bswap32)
    return __builtin_bswap32(val); /* Single CPU instruction (REV on ARM) */
#else
    /* Fallback portable bit-shift arithmetic */
    return (((val & 0xFF000000u) >> 24) |
            ((val & 0x00FF0000u) >>  8) |
            ((val & 0x0000FF00u) <<  8) |
            ((val & 0x000000FFu) << 24));
#endif
}

/* Optional Header Inclusion */
#if __has_include(<sanitizer/asan_interface.h>)
    #include <sanitizer/asan_interface.h>
    #define ASAN_PRESENT 1
#else
    #define ASAN_PRESENT 0
#endif
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Invoking `__has_include` or `__has_builtin` on older compilers (e.g., pre-GCC 5 or C89/C99 without extensions) triggers a syntax error unless preceded by defensive `#ifndef` shims.

## Edge Cases and Failure Modes
- **Macro Guard Precedence Trap:** Checking `#if defined(__has_include)` is valid in C23, but older GCC versions treat `__has_include` as a special operator rather than an ordinary macro. The standard defensive idiom is `#ifndef __has_include #define __has_include(x) 0 #endif`.
- **False Positives on Header Stubs:** If a build tree contains an empty or broken stub header, `__has_include` evaluates to `1` even though compilation will subsequently fail.

## Embedded Implications
- **Hardware Intrinsics:** Microcontroller firmware relies heavily on intrinsics for count-leading-zeros (`__builtin_clz`), byte reversal (`__builtin_bswap16`), and interrupt toggling. Feature detection allows writing single-source portable drivers that automatically exploit hardware accelerations where available.

## Firmware Review Angle
- Replace hardcoded compiler version checks (`#if __GNUC__ >= 7`) with capability checks (`__has_builtin`).
- Ensure all feature detection uses the standard `#ifndef __has_*` fallback shims to support legacy proprietary cross-compilers (Keil ARMCC, IAR, Cosmic).

## Compiler, ABI, and Toolchain Implications
- Standardized formally in ISO C23; supported as extensions in Clang since 3.0 and GCC since 5.0 (for includes) and 10.0 (for builtins).

## Performance, Memory, Timing, and Power
- Enables seamless fallback from single-cycle hardware CPU instructions to portable software algorithms without manual configuration.

## Verification / Debugging
- Test builds using multiple toolchains (GCC, Clang, IAR) in CI to verify fallback paths compile and pass unit tests cleanly.

## Safety, Security, and Reliability
- Prevents compilation failures when migrating between toolchains in safety-critical pipelines.

## Trade-offs and Alternatives
- **Preprocessor Feature Detection vs. Build-System Probing:** Preprocessor detection is self-contained within source files and requires no CMake/Autotools script support, but is limited to compiler/header-level introspection.

## Staff-Level Takeaway
Abandon brittle compiler version arithmetic (`#if __GNUC__ == ...`). Adopt `__has_builtin` and `__has_include` protected by defensive fallback shims to build clean, self-introspecting, multi-compiler embedded software.

## Related Concepts
- `01_File_inclusion`
- `03_Conditional_inclusion`
- `06_Predefined_macros`
