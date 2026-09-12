# 11: When Inline Functions Are Safer

## Definition
`static inline` functions are true C language functions defined in header files whose bodies the compiler may embed directly at the call site. Standardized in ISO C99, `static inline` functions provide all the zero-overhead performance benefits of function-like macros while enforcing full compile-time type safety, single-evaluation semantics, and debugger visibility.

## Scope and Boundaries
Covers: Comparison between function-like macros and `static inline` functions, type safety, side-effect prevention, compiler diagnostics, and valid remaining use cases for macros.
Does not cover: C++ inline semantics or compiler linkage optimizations (LTO).

## Why Does It Exist
For decades, function-like macros were used to avoid function call overhead. However, macros suffer from precedence bugs, double-evaluation hazards, lack of type checking, and poor debuggability. C99 `static inline` functions were introduced to make function-like macros obsolete for executable logic.

## Comparison Matrix
| Feature | Function-Like Macro | `static inline` Function |
| :--- | :--- | :--- |
| **Type Safety** | None (lexical replacement) | Strict compile-time type checking |
| **Argument Evaluation** | Multiple times if duplicated | Exactly once (guaranteed) |
| **Operator Precedence** | Vulnerable without parentheses | Immune (parsed by compiler AST) |
| **Debugger Stepping** | Cannot step inside (single step) | Full interactive source stepping |
| **Compiler Warnings** | Obscure expanded-token errors | Clear function prototype errors |
| **Addressable** | No (cannot take pointer) | Yes (can pass as function pointer) |
| **Scope / Encapsulation**| Global preprocessor namespace | Controlled C function scope |

## Examples
```c
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

/* FRAGILE: Function-like macro */
#define MACRO_CLAMP(v, lo, hi)     (((v) < (lo)) ? (lo) : (((v) > (hi)) ? (hi) : (v)))

/* SAFE & ROBUST: static inline function */
static inline int32_t clamp_i32(int32_t val, int32_t min_val, int32_t max_val) {
    if (val < min_val) return min_val;
    if (val > max_val) return max_val;
    return val;
}

/* Another example: Bit manipulation */
static inline uint32_t reg_set_bits(uint32_t reg, uint32_t mask) {
    return reg | mask;
}

static void test_comparison(void) {
    int i = 5;
    /* Safe from multiple evaluation: i++ executes strictly once */
    int32_t res = clamp_i32(i++, 0, 10);
    assert(res == 5);
    assert(i == 6); /* Exactly one increment */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Unlike macros, `static inline` functions obey all standard C calling conventions, integer promotions, and sequence point rules.

## Edge Cases and Failure Modes
- **When Macros Are Still Required:**
  1. **Stringification and Token Pasting:** Functions cannot stringize (`#`) or paste tokens (`##`).
  2. **Compile-Time Metaprogramming:** Macros like `ARRAY_SIZE(arr)` require `sizeof` evaluation on arrays before pointer decay occurs.
  3. **Caller Context Introspection:** Capturing `__FILE__` and `__LINE__` at the call site for assertions and logging.
  4. **Code Generation:** X-Macro dispatch tables.

## Embedded Implications
- **Zero Assembly Difference:** When compiled with optimization (`-O2`, `-Os`), modern compilers emit the identical machine instructions for a `static inline` function as they do for a macro.
- **Out-of-Line Fallback:** If code size optimization (`-Os`) determines that inlining a function in 50 places wastes too much Flash, the compiler can automatically emit a single shared copy, saving Flash space. Macros cannot do this.

## Firmware Review Angle
- Ask the fundamental question: **"Can this macro be written as a `static inline` function?"** If yes, reject the macro and mandate `static inline`.
- Reserve function-like macros strictly for operations that are impossible with inline functions.

## Compiler, ABI, and Toolchain Implications
- `static inline` gives the function internal linkage; each translation unit receives its own inlined copy, eliminating duplicate symbol linker errors.

## Performance, Memory, Timing, and Power
- Identical runtime performance and power profile to macros, with superior code size management under `-Os`.

## Verification / Debugging
- Debuggers can set breakpoints inside `static inline` functions and inspect local parameter values cleanly.

## Safety, Security, and Reliability
- MISRA C:2012 Directive 4.9: A function should be used in preference to a function-like macro where they are interchangeable.

## Trade-offs and Alternatives
- `static inline` requires explicit types (e.g., `clamp_i32` vs `clamp_f32`). In C11, type-generic dispatch can be achieved safely using `_Generic` macros wrapping `static inline` functions.

## Staff-Level Takeaway
Default to `static inline` functions for all executable logic. They eliminate multiple evaluation hazards, provide type safety, enable debugger stepping, and generate identical assembly. Restrict function-like macros exclusively to compile-time context capture (`__LINE__`), stringification, token pasting, and X-Macros.

## Related Concepts
- `02_Function_like_macros`
- `04_Multiple_evaluation`
- `12_Macro_review_checklist`
