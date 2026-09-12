# 02: Function-Like Macros

## Definition
A function-like macro is an identifier followed immediately by a parenthesized parameter list in its `#define` directive (e.g., `#define MACRO(a, b) ...`). It mimics function call syntax, replacing parameter names in the macro body with the raw un-evaluated argument tokens provided at the call site.

## Scope and Boundaries
Covers: Parameterized macro syntax, argument binding rules, whitespace constraints in definitions, and expression vs. statement roles.
Does not cover: Variadic macros (see `07_Variadic_macros`) or multi-statement idioms (see `06_do_while_0_idiom`).

## Why Does It Exist
Before standard C introduced the `inline` keyword in C99, function-like macros were the only mechanism available for eliminating function call overhead (stack frame setup, register spilling, and branch instructions) in performance-critical inner loops.

## Mechanism and Language Rules
1. **No Whitespace Rule:** In the `#define` directive, there MUST NOT be any whitespace between the macro name and the opening parenthesis `(`.
   - `#define FOO(x)` is a function-like macro.
   - `#define FOO (x)` is an object-like macro whose replacement text starts with `(x)`.
2. **Token Substitution:** Each argument is substituted textually into the macro body wherever the parameter name appears, without type checking or prior evaluation.
3. **Comma As Separator:** Commas inside macro invocations separate arguments, unless the comma is nested inside balanced inner parentheses: `MACRO((a, b), c)` passes two arguments, not three.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Syntax constraint: No space between identifier and '(' */
#define MIN(a, b)           (((a) < (b)) ? (a) : (b))
#define CLAMP(v, lo, hi)    (MIN(MAX((v), (lo)), (hi)))
#define MAX(a, b)           (((a) > (b)) ? (a) : (b))

/* Array element count macro */
#define ARRAY_SIZE(arr)     (sizeof(arr) / sizeof((arr)[0]))

static void test_function_macros(void) {
    int x = 10;
    int y = 20;
    int m = MIN(x, y);
    assert(m == 10);

    uint32_t buffer[16];
    assert(ARRAY_SIZE(buffer) == 16);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Passing an incorrect number of arguments to a non-variadic function-like macro is a constraint violation and halts compilation.
- Preprocessor behavior when a macro parameter appears inside a string literal (`#define STR(x) "x"`) is standard-defined: `x` is NOT replaced; it remains the literal text `"x"`.

## Edge Cases and Failure Modes
- **The Accidental Space Bug:**
  ```c
  #define IS_ODD (x) (((x) & 1) != 0) /* BUG: Space before '(' */
  // IS_ODD(5) expands to: (x) (((x) & 1) != 0)(5) -> Syntax error!
  ```
- **Type-Blind Parameter Matching:** Passing mismatched types or pointers where numbers are expected compiles cleanly through the preprocessor, only to emit confusing errors during semantic analysis.

## Embedded Implications
- **Register Manipulation Wrappers:** Peripheral drivers often use function-like macros for fast atomic manipulation:
  `#define SET_BIT(reg, bit)   ((reg) |= (1UL << (bit)))`.
- **Lack of Calling Overhead:** In microcontrollers operating at 8-48 MHz, eliminating function call overhead in high-rate interrupt handlers (e.g., motor control PWM interrupts) was historically achieved via function-like macros.

## Firmware Review Angle
- Inspect all macro definitions to ensure there is zero whitespace between the macro identifier and the parameter list `(`.
- Verify that every parameter is fully parenthesized wherever it appears in the macro body.
- Check whether the macro can be cleanly rewritten as a `static inline` function.

## Compiler, ABI, and Toolchain Implications
- Unlike real functions, function-like macros have no address, cannot be passed as function pointers, and emit no distinct symbol into object files.

## Performance, Memory, Timing, and Power
- Inlines code directly at call sites. If a large function-like macro is called frequently, it increases code size, potentially causing instruction cache misses and flash footprint exhaustion.

## Verification / Debugging
- Compilers cannot step *into* a macro using standard debugger single-stepping (`step`/`s` in GDB steps over the entire macro).
- Use `gcc -E` to inspect how arguments were substituted into the macro body.

## Safety, Security, and Reliability
- MISRA C:2012 Directive 4.9: A function should be used in preference to a function-like macro where they are interchangeable.
- Function-like macros do not perform type checking on parameters, permitting type confusion and unexpected conversions.

## Trade-offs and Alternatives
- **Function-Like Macro vs `static inline`:** A `static inline` function provides identical zero-overhead performance, but adds full compile-time type checking, single-evaluation guarantees, and seamless debugger stepping.

## Staff-Level Takeaway
Treat function-like macros as a legacy optimization tool. In modern C codebases, replace arithmetic and logical function-like macros with `static inline` functions. Reserve function-like macros exclusively for compile-time operations (like `ARRAY_SIZE`), stringification, or code generation.

## Related Concepts
- `03_Parentheses_discipline`
- `04_Multiple_evaluation`
- `11_When_inline_functions_are_safer`
