# 10: Inline Functions

## Definition
An inline function is a function suggested to the compiler for inlining—replacing the function call site directly with the body of the function code to eliminate call overhead. In ISO C (C99 §6.7.4), the `inline` function specifier provides language semantics that govern whether a function definition serves purely as an inline candidate or generates an externally linkable symbol.

## Scope and Boundaries
*   **Covers:** The `inline` specifier, `static inline`, `extern inline`, GNU89 vs. C99 inline semantics, compiler optimization heuristics, and cross-TU inlining.
*   **Does not cover:** Macro expansion (see [[Object-like and Function-like Macros]]), Link-Time Optimization (LTO) mechanics, or compiler-specific attributes like `__attribute__((always_inline))`.

## Why Does It Exist
Before C99, developers used function-like preprocessor macros to eliminate call overhead for small routines:
*   **Type Safety:** Macros lack type checking, create multiple evaluation side effects (`SQUARE(x++)`), and degrade debugger visibility.
*   **Performance:** `inline` gives the performance benefits of macros while preserving full type checking, scope rules, and single-evaluation semantics.

## Mechanism and Language Rules
1.  **Compiler Discretion:** The `inline` keyword is purely a compiler hint. The compiler is free to ignore it and generate a regular call.
2.  **The Three C99 Linkage Forms:**
    *   `static inline`: Defined in header files. Every translation unit (TU) gets its own private inline copy or static out-of-line definition if not inlined. No linker symbol collisions. (The standard C idiom).
    *   `inline` (without `static` or `extern`): Provides an inline definition for the local TU, but does **not** generate an external symbol for link resolution. An external non-inline definition must exist elsewhere in the program if an out-of-line call is needed.
    *   `extern inline`: Forces the generation of an externally visible code symbol in that TU, satisfying references from other TUs.
3.  **Modifiable Modifiers:** An `inline` function cannot define modifiable objects with `static` storage duration (C99 §6.7.4p3).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

/* Correct: Canonical static inline header pattern */
static inline uint32_t bit_mask(uint8_t bit_index)
{
    return (1UL << bit_index);
}

/* Correct: Eliminates call overhead while preserving type safety */
static inline int32_t min_int32(int32_t a, int32_t b)
{
    return (a < b) ? a : b;
}

static uint32_t example_use(uint8_t pin)
{
    /* Expanded in-place by optimizer: zero instruction call overhead */
    return bit_mask(pin);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Calling an `inline` function whose address is taken when no external definition exists in any translation unit to satisfy the reference.
*   **Compiler Differences (GNU89 vs. C99):** In old GNU89 semantics (GCC `< 4.3`), `extern inline` meant the exact opposite of C99: it provided an inline definition without emitting an external symbol. This caused massive migration bugs when C99 became default.
*   **Implementation-Defined:** The specific heuristic thresholds used by compilers to accept or reject inlining requests.

## Edge Cases and Failure Modes
*   **Code Bloat:** Inlining large functions inside frequently executed code multiplies binary ROM size, displacing other critical code from CPU instruction caches and degrading overall system performance.
*   **Static Local Variable Trap:** Declaring a `static` local variable inside a `static inline` function generates an independent, unshared static instance in every translation unit that includes the header.

## Embedded Implications
*   **MMIO Accessors:** Peripheral register reads/writes are universally written as `static inline` functions in modern HALs (e.g., CMSIS `__NVIC_EnableIRQ`):
    ```c
    static inline void mmio_write32(uintptr_t addr, uint32_t val) {
        *(volatile uint32_t *)addr = val;
    }
    ```
    This delivers zero function call latency while retaining strict type safety.
*   **Cache Thrashing:** Excessive inlining in MCUs with instruction caches (e.g., Cortex-M7) blows out the small I-cache (typically 16-32 KB), turning small loops into memory stall bottlenecks.

## Firmware Review Angle
1.  **Enforce `static inline`:** Ensure header-declared utility functions use `static inline`. Pure `inline` without `static` should be rejected.
2.  **Function Size Check:** Reject inlining on functions larger than 5-10 lines or functions containing loops/switches unless profiling justifies it.
3.  **No Static Locals in Headers:** Ban `static` local variables inside inline header functions.

## Compiler, ABI, and Toolchain Implications
*   **Optimization Dependencies:** Inlining only functions when optimization is enabled (`-O1`, `-O2`, `-O3`, `-Os`). Under `-O0`, compilers generate standard function calls unless `__attribute__((always_inline))` is used.
*   **Link-Time Optimization (LTO):** LTO eliminates the need for manual inlining across translation units by allowing the compiler to inline normal `extern` functions during link time.

## Performance, Memory, Timing, and Power
*   **Zero Call Overhead:** Eliminates `BL`/`RET` instructions and stack frame setup/teardown cycles.
*   **Constant Folding:** Inlining exposes argument constants directly to the callee's body, triggering aggressive compile-time constant propagation and dead code elimination.
*   **ROM Bloat vs. Cache Efficiency:** Micro-inlining reduces ROM size (by eliminating prologue/epilogue instructions), but macro-inlining inflates ROM size.

## Verification / Debugging
*   **Compiler Flags:** Use `-Winline` to alert when a function marked `inline` could not be inlined by the compiler.
*   **GDB Stepping:** Modern DWARF debug information tracks inlined subroutines, allowing debuggers to step through inlined functions as if they were real calls.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 8.10:* An inline function shall be declared with the `static` storage class.
*   **Security Advantages:** Eliminating preprocessor macros in favor of `static inline` functions prevents double-evaluation bugs and type-evasion exploits.

## Trade-offs and Alternatives
*   **`static inline` vs. Preprocessor Macros:** `static inline` functions provide 100% of the speed advantages of macros with full type safety, scope isolation, and debuggability. Always prefer `static inline` over function-like macros.

## Staff-Level Takeaway
`static inline` in header files is the gold standard in modern C for high-frequency utility routines and hardware register accessors. Staff engineers must enforce `static inline` across all HAL header definitions, ban function-like macros that compute values, and prevent code bloat by keeping inline bodies strictly bounded to trivial operations.

## Related Concepts
*   [[01_Function_definition]]
*   [[02_Function_declaration]]
*   [[Compiler Optimization and Inlining]]
*   [[Object-like and Function-like Macros]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
