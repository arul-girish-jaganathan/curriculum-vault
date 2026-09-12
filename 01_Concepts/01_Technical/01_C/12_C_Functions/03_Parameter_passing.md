# 03: Parameter Passing

## Definition
Parameter passing is the language and ABI mechanism by which argument values supplied at a function call site are bound to the formal parameters of the target function. In ISO C (C99 §6.5.2.2), all arguments are passed strictly by value, with the physical transfer mechanism defined by the target architecture's Application Binary Interface (ABI).

## Scope and Boundaries
*   **Covers:** Conceptual parameter evaluation, ABI register vs. stack assignment, argument conversion rules, order of argument evaluation, and parameter memory lifetimes.
*   **Does not cover:** Pass-by-value mechanics in isolation (see [[04_Pass_by_value]]), array parameter adjustment (see [[05_Array_parameter_adjustment]]), or pointer parameters (see [[06_Pointer_parameters]]).

## Why Does It Exist
Procedural computation requires feeding input data into parameterized routines:
*   **Reusability:** Allowing a single block of code to operate on variable inputs.
*   **Isolation:** Ensuring callee routines cannot unintentionally corrupt caller state.
*   **Hardware Mapping:** Leveraging high-speed CPU registers for fast argument transfer.

## Mechanism and Language Rules
1.  **Strict Value Semantics:** Every argument expression is evaluated, and a copy of its value is assigned to the corresponding formal parameter.
2.  **Unspecified Evaluation Order:** In ISO C, the order in which function arguments are evaluated is unspecified. In `f(a(), b())`, the compiler is free to evaluate `a()` first or `b()` first.
3.  **Sequence Points:** There is a sequence point after the evaluation of all function arguments and the function designator, immediately before the actual call (C99 §6.5.2.2p10).
4.  **Prototype Conversion:** If a prototype is in scope, argument values are implicitly converted to the type of the formal parameter as if by assignment.
5.  **Lifetime:** Formal parameters have automatic storage duration. Their lifetimes begin upon function entry and terminate upon function return.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

static int32_t step_value(int32_t *counter)
{
    return ++(*counter);
}

static int32_t compute(int32_t a, int32_t b)
{
    return a - b;
}

static int32_t example_eval_order(void)
{
    int32_t count = 0;
    /* HAZARD: Unspecified evaluation order of arguments */
    /* Could evaluate left-to-right or right-to-left */
    return compute(step_value(&count), step_value(&count));
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Unspecified Behavior:** The order of evaluation of argument expressions. Writing code that relies on left-to-right evaluation order produces non-portable results.
*   **Undefined Behavior:** Modifying a scalar object more than once without an intervening sequence point across argument evaluations (e.g., `f(i++, i++)`). Calling a function with mismatched argument types when no prototype is present.
*   **Implementation-Defined:** How parameters are placed into physical CPU registers or spilled onto the call stack (governed by the platform ABI).

## Edge Cases and Failure Modes
*   **Evaluation Order Side Effects:** If arguments have interdependent side effects (e.g., `func(read_fifo(), read_fifo())`), the order of data read from hardware FIFOs varies between GCC, Clang, and optimization levels.
*   **Parameter Aliasing:** If two pointer parameters point to the same physical object, mutations through one parameter alter the object referenced by the other, violating developer assumptions of parameter isolation.

## Embedded Implications
*   **AAPCS (ARM Architecture Procedure Call Standard):** On 32-bit ARM (Cortex-M), the first four 32-bit arguments are passed in registers `R0-R3`. Any additional arguments are pushed onto the call stack. Designing functions with 4 or fewer parameters eliminates stack access overhead.
*   **Interrupt Latency:** Functions with many parameters require stack pushes during the prologue, increasing stack frame allocation time and register pressure during time-critical ISR execution.

## Firmware Review Angle
1.  **Argument Count:** Verify whether functions with > 4 parameters can be refactored or grouped into a `const` configuration struct pointer to prevent stack spilling on ARM/RISC-V.
2.  **Side Effects in Calls:** Strictly prohibit calling functions with multiple arguments that have mutating side effects (e.g., `process(get_data(), get_data())`).
3.  **Aliasing Verification:** Check whether pointer parameters can alias, and qualify with `restrict` if mutual exclusion is guaranteed by design.

## Compiler, ABI, and Toolchain Implications
*   **Register Passing:** Compilers assign arguments to architectural registers first (`R0-R3` on ARM, `a0-a7` on RISC-V, `RDI/RSI/RDX/RCX/R8/R9` on x86_64).
*   **Stack Spilling:** Arguments that exceed available register capacity are written to caller-allocated stack parameter areas.
*   **Optimization:** Inlining functions eliminates parameter passing entirely, allowing the compiler to perform cross-boundary register reuse.

## Performance, Memory, Timing, and Power
*   **Cycle Cost:** Passing arguments in registers costs 0 extra memory cycles. Stack-passed parameters require memory store (`STR`) instructions in the caller and load (`LDR`) instructions in the callee.
*   **Cache & Bus Traffic:** Avoiding stack parameters reduces SRAM bus contention, preserving power and improving deterministic timing.

## Verification / Debugging
*   **Compiler Warnings:** Use `-Wclobbered -Wsequence-point`.
*   **GDB Disassembly:** Inspect the function call site (`call` or `BL`) to verify whether parameters are loaded via `MOV`/`LDR` into registers or pushed to the stack.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 13.1:* Initializer lists shall not contain persistent side effects.
    *   *Rule 13.2:* The value of an expression and its persistent side effects shall be the same under all permitted evaluation orders.
*   **Security Vulnerabilities:** Parameter evaluation side effects cause hard-to-reproduce timing bugs and protocol desynchronization in cryptographic or communication decoders.

## Trade-offs and Alternatives
*   **Individual Parameters vs. Struct Encapsulation:** Individual scalar parameters (<= 4) maximize register utilization. Passing large structs should always be done via `const StructType *` to avoid stack-copy overhead.

## Staff-Level Takeaway
Parameter passing at the C language level is strictly pass-by-value, but at the machine level, it is a hardware register allocation problem. Staff engineers should architect APIs around the target ABI: limit hot-path functions to 4 scalar arguments to maximize register residency, and eliminate side effects from function call argument lists to avoid unspecified evaluation order traps.

## Related Concepts
*   [[04_Pass_by_value]]
*   [[06_Pointer_parameters]]
*   [[11_Calling_conventions]]
*   [[Stack Frame Architecture and ABI]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
