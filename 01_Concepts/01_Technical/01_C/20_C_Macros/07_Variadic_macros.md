# 07: Variadic Macros

## Definition
A variadic macro is a function-like macro that accepts a variable number of arguments using an ellipsis (`...`) as the final parameter. Standardized in ISO C99, the variable arguments are accessible in the macro replacement list via the special identifier `__VA_ARGS__`.

## Scope and Boundaries
Covers: C99 `...` and `__VA_ARGS__`, the empty-argument trailing comma hazard, GNU `, ## __VA_ARGS__` extension, ISO C23 `__VA_OPT__`, and logging frameworks.
Does not cover: C standard library variadic runtime functions (`<stdarg.h>`, `va_list`).

## Why Does It Exist
Diagnostics, telemetry logging, and formatted output functions (like `printf`) require variable argument lists. Variadic macros allow developers to inject compile-time metadata (`__FILE__`, `__LINE__`, module tags) into logging calls without duplicating formatting code.

## Mechanism and Language Rules
1. **C99 Ellipsis Syntax:** The parameter list ends with `...`. The arguments matching the ellipsis are substituted at `__VA_ARGS__`.
2. **The Trailing Comma Problem (Pre-C23):**
   ```c
   #define LOG(fmt, ...) printf(fmt, __VA_ARGS__)
   LOG("Hello"); /* Expands to: printf("Hello", ); -> SYNTAX ERROR: Trailing comma! */
   ```
3. **GNU Extension `, ## __VA_ARGS__`:** GCC and Clang provide an extension where `##` preceding `__VA_ARGS__` deletes the preceding comma if `__VA_ARGS__` is empty.
4. **C23 Standard Solution (`__VA_OPT__`):** ISO C23 introduces `__VA_OPT__(,)`, which expands to its contents only if `__VA_ARGS__` is non-empty:
   `#define LOG(fmt, ...) printf(fmt __VA_OPT__(,) __VA_ARGS__)`.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

/* Portable Logging Architecture across C Standard Revisions */

#if defined(__STDC_VERSION__) && (__STDC_VERSION__ >= 202311L)
    /* ISO C23 Standard Solution: __VA_OPT__ */
    #define SYS_LOG(level, fmt, ...)         printf("[%s] " fmt "
", level __VA_OPT__(,) __VA_ARGS__)
#elif defined(__GNUC__) || defined(__clang__)
    /* GCC/Clang Extension: Token paste comma deletion */
    #define SYS_LOG(level, fmt, ...)         printf("[%s] " fmt "
", level, ## __VA_ARGS__)
#else
    /* Strictly compliant C99 (requires at least one variable argument) */
    #define SYS_LOG(level, fmt, ...)         printf("[%s] " fmt "
", level, __VA_ARGS__)
#endif

static void test_variadic(void) {
    /* Invocation with variable arguments */
    SYS_LOG("INFO", "Telemetry reading: %d mV", 3300);

    /* Invocation with ZERO variable arguments */
    SYS_LOG("WARN", "System idle");
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Invoking a C99 variadic macro with fewer arguments than parameters (excluding the ellipsis) is a constraint violation.
- `, ## __VA_ARGS__` is a non-standard compiler extension; compiling with `-std=c99 -pedantic` emits a warning unless using C23 `__VA_OPT__`.

## Edge Cases and Failure Modes
- **Zero-Argument Breakage in Pure C99:** Pure C99 does not support omitting variable arguments without leaving a trailing comma. Code compiled across strict non-GNU compilers will fail on `SYS_LOG("INFO", "Message")`.
- **String Concatenation Pitfall:** Writing `#define LOG(fmt, ...) printf(fmt "
", ...)` assumes `fmt` is a string literal. If the caller passes a variable `char *`, compilation fails.

## Embedded Implications
- **Compile-Time Log Stripping:** Variadic macros allow completely compiling out debug logging statements to save Flash space in release firmware:
  ```c
  #if defined(DEBUG_BUILD)
      #define DBG_PRINT(...)  printf(__VA_ARGS__)
  #else
      #define DBG_PRINT(...)  ((void)0)
  #endif
  ```
  When disabled, `((void)0)` consumes zero CPU cycles and leaves zero strings in `.rodata`.

## Firmware Review Angle
- Check that logging macros handle zero variable arguments portably (using `__VA_OPT__` or `, ## __VA_ARGS__`).
- Confirm that disabled debug macros expand to `((void)0)` so that trailing semicolons parse cleanly.

## Compiler, ABI, and Toolchain Implications
- Variadic macro expansion occurs in Phase 4; arguments are passed directly to the target variadic function (e.g., `vprintf`), adhering to the target ABI's variadic calling conventions (stack-spilled registers).

## Performance, Memory, Timing, and Power
- If logging is compiled out, variadic macros generate zero assembly and zero flash usage.
- If enabled, formatting and transmitting variadic strings over UART consumes significant CPU time and bus bandwidth.

## Verification / Debugging
- Use `gcc -E` to inspect how variable argument lists expand across single and multiple parameters.

## Safety, Security, and Reliability
- Format string vulnerabilities (CWE-134) can occur if caller input is passed directly to the format parameter of a variadic macro.

## Trade-offs and Alternatives
- **Variadic Macro vs Wrapper Function:** A wrapper function taking `va_list` requires runtime overhead, whereas a variadic macro inlines metadata (`__FILE__`, `__LINE__`) directly at compile time.

## Staff-Level Takeaway
Variadic macros are essential for zero-cost diagnostic logging frameworks. Use `__VA_OPT__` for modern C23 compliance, fall back gracefully to `, ## __VA_ARGS__` on GCC/Clang, and ensure disabled log levels expand to `((void)0)` to eliminate Flash bloat in production builds.

## Related Concepts
- `02_Function_like_macros`
- `06_do_while_0_idiom`
- `08_Stringification_macros`
