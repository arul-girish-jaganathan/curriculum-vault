# 02: Macro Expansion

## Definition
Macro expansion is the recursive process by which the preprocessor substitutes macro identifiers with their replacement token lists. In ISO C, macro replacement occurs for object-like macros (identifiers replaced by tokens) and function-like macros (identifiers with parameter lists enclosed in parentheses).

## Scope and Boundaries
Covers: Object-like and function-like expansion, argument prescan, recursive expansion prevention, the `do { ... } while(0)` idiom, and side-effect hazards.
Does not cover: Stringification (see `04_Stringification`) or Token pasting (see `05_Token_pasting`).

## Why Does It Exist
Macros eliminate boilerplate, provide cross-platform code generation, and enable zero-overhead parameterization where inline functions were historically unsupported or when manipulating lexical tokens.

## Mechanism and Language Rules
1. **Argument Prescan:** Before macro arguments are substituted into the macro body, each argument is fully macro-expanded, EXCEPT when preceded by `#` (stringize) or adjacent to `##` (token paste).
2. **Rescanning for Further Replacement:** After the replacement list replaces the macro invocation, the resulting token sequence is rescanned for additional macro names to expand.
3. **Self-Referential Disabling:** If the name of the macro being expanded is encountered during rescanning, it is marked as "disabled" (not expanded again). This prevents infinite recursive loops.
4. **Statement Safety (`do-while(0)`):** Multi-statement function-like macros must be wrapped in `do { ... } while(0)` to function correctly in dangling-else statements and semicolon-terminated contexts.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* HAZARD: Operator Precedence Trap */
#define BAD_SQUARE(x)       x * x
#define GOOD_SQUARE(x)      ((x) * (x))

/* HAZARD: Multi-statement macro without do-while(0) */
#define BAD_RESET_PERIPH()      periph_disable();           periph_reset()

/* CORRECT: Idiomatic do-while(0) wrapper */
#define SAFE_RESET_PERIPH()     do {                            periph_disable();           periph_reset();         } while(0)

static void test_expansion(void) {
    /* BAD_SQUARE(1 + 2) expands to: 1 + 2 * 1 + 2 = 5! */
    assert(BAD_SQUARE(1 + 2) == 5);

    /* GOOD_SQUARE(1 + 2) expands to: ((1 + 2) * (1 + 2)) = 9 */
    assert(GOOD_SQUARE(1 + 2) == 9);

    /* Dangling-else failure mode: */
    int condition = 0;
    if (condition)
        SAFE_RESET_PERIPH(); /* Correctly parses with trailing semicolon */
    else
        (void)0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Evaluating a macro argument with side effects multiple times (e.g., `GOOD_SQUARE(i++)` expands to `((i++) * (i++))`) invokes Undefined Behavior due to unsequenced side effects on `i`.

## Edge Cases and Failure Modes
- **Double Evaluation Bug:** When a function-like macro evaluates an argument more than once (e.g., `#define MAX(a, b) (((a) > (b)) ? (a) : (b))`), passing function calls or expressions like `MAX(read_adc(), 100)` causes multiple hardware reads.
- **Semicolon Swallowing:** Writing `#define FOO() { a(); b(); }` breaks when written as `if (c) FOO(); else bar();` because the compiler treats the trailing semicolon as an empty statement between the `if` block and `else`.

## Embedded Implications
- **Hardware Register Volatility:** If a macro reads a hardware register multiple times during expansion (`#define IS_READY() (REG_SR & READY_BIT)`), the register state may change between evaluations.
- **Static Inlines Preferred:** Modern embedded compilers optimize `static inline` functions better than macros, retaining full type safety, warning diagnostics, and debugger visibility.

## Firmware Review Angle
- Confirm all macro parameters are enclosed in parentheses in the replacement list: `((a) + (b))`.
- Confirm the entire macro expression is wrapped in outer parentheses.
- Ensure all multi-statement macros use `do { ... } while(0)`.
- Flag any macro argument evaluated more than once.

## Compiler, ABI, and Toolchain Implications
- Compiler front-ends expand macros entirely before building the Abstract Syntax Tree (AST). The type checker never sees the macro identifier—only its expanded tokens.

## Performance, Memory, Timing, and Power
- Macros generate inline code; overuse of large macros leads to code bloat in Flash (ROM).
- Unlike static inline functions, the compiler cannot enforce a unified stack frame or out-of-line fallback for code size optimization.

## Verification / Debugging
- GCC/Clang: Compile with `-g3` to embed preprocessor macro definitions directly into DWARF debug symbols, allowing GDB to expand macros via `macro expand MACRO_NAME(x)`.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.7: Expressions resulting from the expansion of macro parameters shall be enclosed in parentheses.
- MISRA C:2012 Directive 4.9: A function should be used in preference to a function-like macro where they are interchangeable.

## Trade-offs and Alternatives
- **Function-Like Macro vs. `static inline`:** `static inline` functions provide strict type checking, eliminate double-evaluation side effects, and are visible in debuggers. Reserve macros for conditional compilation, stringification, or token manipulation.

## Staff-Level Takeaway
A function-like macro is a blunt lexical instrument. Wrap arguments and entire bodies in parentheses, encapsulate statements with `do { ... } while(0)`, and mandate `static inline` functions for arithmetic and logic whenever type checking and single-evaluation semantics are required.

## Related Concepts
- `04_Stringification`
- `05_Token_pasting`
- `../18_C_Typedef/08_Typedef_vs_macro`
