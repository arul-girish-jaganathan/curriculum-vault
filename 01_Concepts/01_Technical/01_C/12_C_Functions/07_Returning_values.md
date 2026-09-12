# 07: Returning Values

## Definition
Returning a value is the mechanism by which a function terminates execution and yields a typed result back to its caller via the `return` statement. In ISO C (C99 §6.8.6.4), the value of the expression in the `return` statement is converted to the function's return type as if by assignment, and passed to the caller's evaluation context.

## Scope and Boundaries
*   **Covers:** Scalar returns, conversion rules upon return, void returns, implicit returns, and execution termination semantics.
*   **Does not cover:** Returning composite structures (see [[08_Returning_structures]]), function pointers as return types (see [[13_C_Pointers/12_Function_pointers]]), or non-returning functions (`_Noreturn`).

## Why Does It Exist
Functions represent mathematical transformations:
*   **Result Propagation:** Yielding computed scalar results, statuses, or resource handles back to the calling context.
*   **Expression Composition:** Allowing function calls to be embedded directly within larger arithmetic and logical expressions (e.g., `x = calc(a) + calc(b);`).
*   **Control Flow Exit:** Early exit from execution blocks when error conditions are detected.

## Mechanism and Language Rules
1.  **Syntax:**
    *   `return expression;` (for non-`void` functions).
    *   `return;` (for `void` functions).
2.  **Assignment Conversion:** The return expression is converted to the function's declared return type as if by: `ReturnType temp = expression; return temp;`.
3.  **Sequence Point:** A sequence point occurs immediately before the function returns to the caller, finalizing all side effects within the return expression.
4.  **Automatic Lifetime Expiration:** All automatic variables declared inside the function cease to exist upon return; their storage is reclaimed.
5.  **Reaching the End:**
    *   Reaching the terminating `}` in a non-`void` function and evaluating the return value in the caller invokes undefined behavior.
    *   Reaching the terminating `}` in a `void` function is equivalent to executing `return;`.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdbool.h>

/* Correct: Immediate return with implicit assignment conversion */
static uint8_t clamp_to_byte(int32_t val)
{
    if (val > 255) {
        return 255U;
    }
    if (val < 0) {
        return 0U;
    }
    return (uint8_t)val; /* Converted to uint8_t */
}

/* Incorrect: Returning pointer to expired stack object */
static const int32_t* invalid_stack_leak(void)
{
    int32_t local_val = 100;
    return &local_val; /* Undefined Behavior: returns pointer to automatic variable */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:**
    *   Caller evaluating the return value of a non-void function that terminated without executing an explicit `return`.
    *   Dereferencing a pointer returned by a function that points to an object with automatic storage duration allocated on the function's stack frame.
*   **Constraint Violation:** Executing `return expr;` inside a function returning `void`. Executing `return;` without an expression inside a non-`void` function.
*   **Implementation-Defined:** Machine register allocation for return values (governed by ABI).

## Edge Cases and Failure Modes
*   **Dangling Stack References:** Returning `&local_variable` is a classic security and stability bug; the stack memory is invalidated and overwritten by subsequent function calls.
*   **Silent Truncation:** Returning a large integer type (`uint32_t`) through a smaller return type (`uint8_t`) silently truncates the value without warnings unless explicit compiler flags are set.

## Embedded Implications
*   **Register Return Mapping:** Under ARM AAPCS, 32-bit scalars return in register `R0`; 64-bit values (`uint64_t`) return in register pair `R0-R1`. This costs zero memory cycles.
*   **Error Code Enums:** Embedded functions frequently return strongly-typed `enum` statuses (`status_t`). Compilers typically optimize these into single 32-bit register transfers.

## Firmware Review Angle
1.  **Exhaustive Returns:** Ensure every logical execution path terminates with an explicit `return` statement.
2.  **No Stack Pointers Returned:** Strictly inspect all returned pointers to ensure they point to static storage, heap, or caller-supplied buffers, never local stack frames.
3.  **Explicit Casts on Truncation:** Require explicit casts if a return statement deliberately narrows an integer type.

## Compiler, ABI, and Toolchain Implications
*   **Register Allocation:** Return values are placed into designated hardware registers (`R0/R1` on ARM, `RAX/RDX` on x86, `a0/a1` on RISC-V).
*   **Tail Call Optimization (TCO):** If a function returns the direct result of another function call (`return helper(x);`), the compiler replaces the call with a jump (`B` or `JMP`), reusing the current stack frame and saving stack RAM.

## Performance, Memory, Timing, and Power
*   **Zero-Cycle Transfer:** Returning scalar values via registers incurs zero memory overhead and no cache line pollution.
*   **Determinism:** Eliminating stack spills during return paths guarantees bounded, deterministic execution timing.

## Verification / Debugging
*   **Compiler Warning Flags:** Enforce `-Wreturn-type -Wreturn-local-addr -Wconversion`.
*   **Static Analyzers:** Tools like Coverity and PC-lint instantly flag returned pointers to stack-allocated variables.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.4:* All exit paths from a function with non-void return type shall have an explicit return statement.
    *   *Rule 17.8:* A function parameter should not be modified.
*   **Security Vulnerabilities:**
    *   CWE-562: Return of Stack Variable Address. Leads to arbitrary code execution when attackers overwrite the reclaimed stack frame.

## Trade-offs and Alternatives
*   **Scalar Return vs. Out-Parameters:** Prefer returning scalar values (or error codes) directly via return values rather than out-parameters; registers are utilized natively, improving readability and optimizer analysis.

## Staff-Level Takeaway
Scalar returns are the cleanest, most efficient data communication mechanism in C. Staff engineers must enforce compile-time flags (`-Werror=return-type`, `-Werror=return-local-addr`) to eliminate missing returns and stack address leaks, leveraging register returns to maximize execution determinism.

## Related Concepts
*   [[01_Function_definition]]
*   [[08_Returning_structures]]
*   [[11_Calling_conventions]]
*   [[Stack Frame Architecture and ABI]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
