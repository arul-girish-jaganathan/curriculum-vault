# 04: Multiple Evaluation

## Definition
Multiple evaluation occurs when a function-like macro references a parameter multiple times in its replacement list. If the caller passes an argument expression that contains side effects (e.g., increment/decrement operators, volatile reads, or non-idempotent function calls), those side effects execute multiple times, leading to corrupted data and non-deterministic behavior.

## Scope and Boundaries
Covers: Parameter duplication hazards, side-effect expansion (`i++`, `read_fifo()`), sequence point violations, and mitigation patterns.
Does not cover: Multiple statement execution (see `06_do_while_0_idiom`).

## Why Does It Exist
Unlike true C functions—which evaluate each argument exactly once during parameter binding before executing the function body—macros perform textual substitution. Every occurrence of a parameter identifier in the macro body causes another distinct evaluation of the caller's expression.

## Mechanism and Language Rules
1. **Textual Duplication:** If parameter `x` appears twice in the macro replacement list (e.g., `#define SQUARE(x) ((x) * (x))`), the caller's expression is copied twice into the AST.
2. **Unsequenced Side Effects (ISO C99 §6.5):** If an expression with side effects (like `i++`) is evaluated multiple times without intervening sequence points, the behavior is undefined.
3. **No Intermediate Storage:** Standard ISO C macros cannot create temporary variables to capture argument values without using statement blocks or compiler extensions.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* CLASSIC HAZARD: Arguments evaluated twice */
#define MIN(a, b)       (((a) < (b)) ? (a) : (b))
#define SQUARE(x)       ((x) * (x))

/* Mock hardware FIFO read function (side effect: pops front item) */
static int g_fifo_data = 5;
static int pop_fifo(void) {
    return g_fifo_data++;
}

static void test_multiple_eval(void) {
    int i = 1;
    /* SQUARE(i++) expands to: ((i++) * (i++)) */
    /* UNDEFINED BEHAVIOR: i modified twice without sequence point! */
    // int sq = SQUARE(i++); 

    int a = 10;
    int b = 5;
    /* MIN(a++, b) expands to: (((a++) < (b)) ? (a++) : (b)) */
    /* If condition is false, 'a' is incremented ONCE.
       If condition is true, 'a' is incremented TWICE! */
    int m = MIN(a++, b);
    assert(a == 11); /* Condition was false: a incremented once */

    /* HARDWARE DESTRUCTION: pop_fifo() called multiple times! */
    int val = MIN(pop_fifo(), 10);
    /* pop_fifo() was evaluated TWICE: once for comparison, once to return! */
    (void)val;
    (void)m;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Passing an expression with side effects (e.g., `SQUARE(i++)`) invokes Undefined Behavior in ISO C due to multiple unsequenced modifications of the same scalar object.

## Edge Cases and Failure Modes
- **Hardware FIFO Draining:** Calling `MIN(uart_read(), threshold)` causes `uart_read()` to be called twice if it is the minimum, discarding a byte of incoming hardware data.
- **Hidden Performance Degradation:** Passing an expensive calculation (e.g., `MIN(compute_fft(), limit)`) causes the expensive algorithm to run twice, halving system throughput.

## Embedded Implications
- **Volatile Register Corruption:** Reading a volatile register clears status flags or advances hardware states (e.g., reading an ADC data register). Multiple evaluation of a volatile register argument causes the hardware state machine to advance unexpectedly.

## Firmware Review Angle
- Search for any macro parameter that appears more than once in the replacement list (`MIN`, `MAX`, `ABS`, `CLAMP`).
- Verify that call sites never pass expressions with side effects (`++`, `--`, function calls, volatile reads).
- Strongly advocate replacing all multiple-parameter macros with `static inline` functions.

## Compiler, ABI, and Toolchain Implications
- GCC and Clang provide a non-standard extension called "Statement Expressions" (`({ ... })`) that allows capturing arguments in local variables using `typeof`:
  ```c
  #define SAFE_MIN(a, b) ({       __typeof__(a) _a = (a);       __typeof__(b) _b = (b);       _a < _b ? _a : _b;   })
  ```
  While effective, statement expressions are non-standard ISO C and violate MISRA C.

## Performance, Memory, Timing, and Power
- Duplicate evaluation multiplies execution time and CPU energy consumption, especially when the argument contains math functions or peripheral reads.

## Verification / Debugging
- Compiler warnings: `-Wsequence-point` catches unsequenced modifications in macros like `SQUARE(i++)`.
- Clang-Tidy: `bugprone-macro-repeated-side-effects` flags multiple evaluation hazards automatically.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.7 and Directive 4.9: Prohibit function-like macros that evaluate arguments more than once or have side-effect liabilities.

## Trade-offs and Alternatives
- **Macro vs `static inline` Function:** A `static inline` function guarantees that every argument is evaluated strictly once before execution, completely eliminating multiple evaluation hazards.

## Staff-Level Takeaway
Never permit function-like macros that evaluate parameters more than once (`MIN`, `MAX`, `SQUARE`) in production codebases. Replace them with type-safe `static inline` functions to guarantee single-evaluation semantics and protect hardware states from accidental mutation.

## Related Concepts
- `02_Function_like_macros`
- `03_Parentheses_discipline`
- `11_When_inline_functions_are_safer`
