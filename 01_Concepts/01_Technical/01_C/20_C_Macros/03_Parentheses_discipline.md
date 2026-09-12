# 03: Parentheses Discipline

## Definition
Parentheses discipline is the defensive programming practice of systematically wrapping every macro parameter and the overall macro replacement expression in parentheses. Because preprocessor substitution occurs at the lexical token level before operator precedence rules are applied, missing parentheses alter the compiler's Abstract Syntax Tree (AST), producing subtle and catastrophic runtime bugs.

## Scope and Boundaries
Covers: Parameter-level parentheses, expression-level outer parentheses, operator precedence hazards, and bitwise/relational parsing bugs.
Does not cover: Statement-level macro encapsulation (see `06_do_while_0_idiom`).

## Why Does It Exist
In C, operator precedence is notoriously complex (15 distinct precedence levels). In particular, bitwise operators (`&`, `|`, `^`) have *lower* precedence than relational and equality operators (`<`, `==`). When macro arguments contain operators, omitting parentheses causes neighboring operators at the call site to bind to sub-expressions in unintended ways.

## Mechanism and Language Rules
1. **Rule 1: Enclose Every Parameter:** Every occurrence of a macro parameter in the replacement list must be enclosed in parentheses: `(x)`.
2. **Rule 2: Enclose the Entire Expression:** The entire replacement expression must be enclosed in outer parentheses: `((x) + (y))`.
3. **Lexical Binding Hazard:** Without outer parentheses, surrounding code binds to the edges of the macro:
   `MACRO * 5` becomes `x + y * 5`, evaluating as `x + (y * 5)`.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

/* ================= THE PRECEDENCE HAZARDS ================= */

/* Hazard 1: Missing parameter parentheses */
#define BAD_SQUARE(x)       ((x) * x)    /* Second 'x' unprotected! */
#define SAFE_SQUARE(x)      ((x) * (x))

/* Hazard 2: Missing outer expression parentheses */
#define BAD_ADD(a, b)       (a) + (b)
#define SAFE_ADD(a, b)      ((a) + (b))

/* Hazard 3: Bitwise operator precedence trap */
/* '==' has higher precedence than '&' */
#define BAD_CHECK_FLAG(reg, mask)   (reg) & (mask) == (mask)
#define SAFE_CHECK_FLAG(reg, mask)  (((reg) & (mask)) == (mask))

static void test_parentheses(void) {
    /* 1. Parameter hazard: BAD_SQUARE(1 + 2) -> ((1 + 2) * 1 + 2) = 5! */
    assert(BAD_SQUARE(1 + 2) == 5);
    assert(SAFE_SQUARE(1 + 2) == 9);

    /* 2. Outer expression hazard: BAD_ADD(2, 3) * 4 -> (2) + (3) * 4 = 14! */
    assert((BAD_ADD(2, 3) * 4) == 14);
    assert((SAFE_ADD(2, 3) * 4) == 20);

    /* 3. Bitwise trap: BAD_CHECK_FLAG(0xFF, 0x01) expands to: 
     *    (0xFF) & ((0x01) == (0x01)) -> 0xFF & 1 = 1 (Evaluates true for ANY non-zero reg!) 
     */
    uint32_t status_reg = 0x02; /* Bit 0 is clear */
    /* BAD_CHECK_FLAG(status_reg, 0x01) evaluates as: 0x02 & (0x01 == 0x01) -> 0x02 & 1 = 0 (looks correct here) */
    /* But if checking a multi-bit mask: */
    uint32_t val = 0x04;
    assert(SAFE_CHECK_FLAG(val, 0x04) == true);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Missing parentheses do not cause undefined behavior in the language sense; they alter the AST and produce well-defined but entirely unintended arithmetic and logical computations.

## Edge Cases and Failure Modes
- **Cast Expressions:** `#define TO_PTR(x) (uint32_t *)x` breaks when dereferenced: `*TO_PTR(a)` becomes `*(uint32_t *)a` (correct), but `TO_PTR(a)->field` becomes `(uint32_t *)a->field` (dereferences `a->field` before casting!).
  *Fix:* `#define TO_PTR(x) ((uint32_t *)(x))`.
- **Ternary Operator Precedence:** Omitting parentheses around conditional expressions allows assignment operators at the call site to hijack the branches.

## Embedded Implications
- **Register Bit Checks:** Register polling loops often read hardware flags using macros. Missing parentheses around bitwise masks lead to status checks evaluating incorrectly, resulting in infinite loops or skipped data packets.

## Firmware Review Angle
- Mechanically check every macro parameter in the replacement list: is it wrapped in `(...)`?
- Mechanically check the entire replacement list: is the outermost structure enclosed in `(...)`?
- Flag any macro combining bitwise and comparison operators without explicit inner grouping.

## Compiler, ABI, and Toolchain Implications
- Modern compilers (GCC and Clang) provide warning flags like `-Wparentheses` to detect ambiguous unparenthesized expressions, but they cannot catch all macro expansion hazards.

## Performance, Memory, Timing, and Power
- Parentheses are purely syntactic. They dictate AST tree construction and produce zero assembly instructions, zero runtime latency, and zero code size penalty.

## Verification / Debugging
- Static analysis tools (Coverity, PC-lint, Clang-Tidy `bugprone-macro-parentheses`) automatically flag unparenthesized macro parameters and replacement expressions.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.7 (Required): Expressions resulting from the expansion of macro parameters shall be enclosed in parentheses.

## Trade-offs and Alternatives
- **Parentheses Discipline vs `static inline`:** Even with strict parentheses, macros cannot fix multiple-evaluation bugs. `static inline` functions enforce both precedence and evaluation safety.

## Staff-Level Takeaway
Parentheses discipline is non-negotiable. Wrap every macro parameter and wrap the entire macro body. Treat any macro lacking complete parenthesis isolation as a critical defect during code reviews.

## Related Concepts
- `01_Object_like_macros`
- `02_Function_like_macros`
- `04_Multiple_evaluation`
- `12_Macro_review_checklist`
