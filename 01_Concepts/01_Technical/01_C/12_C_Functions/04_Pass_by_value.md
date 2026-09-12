# 04: Pass by Value

## Definition
Pass-by-value is the fundamental argument passing evaluation strategy in C where the actual argument expression is fully evaluated, and an independent, isolated copy of that value is assigned to the function's formal parameter. In ISO C (C99 §6.5.2.2p4), modifying the formal parameter inside the callee has zero effect on the caller's argument object.

## Scope and Boundaries
*   **Covers:** Scalar copying, struct/union copying mechanics, value isolation guarantees, and stack-allocation overhead of large value copies.
*   **Does not cover:** Emulating pass-by-reference using pointers (see [[06_Pointer_parameters]]), array decay mechanisms (see [[05_Array_parameter_adjustment]]), or return value copies (see [[07_Returning_values]]).

## Why Does It Exist
Pass-by-value is the core safety invariant of procedural programming in C:
*   **Isolation:** Callee functions cannot mutate caller variables, preventing unexpected side effects and maintaining local reasoning.
*   **Re-entrancy:** Functions can safely modify their own parameter copies as local scratchpad variables without breaking concurrent callers or re-entrant executions.

## Mechanism and Language Rules
1.  **Complete Copying:** When an argument is passed, memory storage is allocated for the parameter in the callee's frame (or mapped to a register), and the argument's bits are copied.
2.  **Mutation Isolation:** `param = new_value;` modifies only the callee's local parameter storage.
3.  **Aggregates (Structs/Unions):** Passing a struct by value copies the entire memory layout of the struct, including internal member padding, element by element (as if via `memcpy`).
4.  **Arrays Exception:** Arrays cannot be passed by value directly; they automatically decay into pointers to their first elements (see [[05_Array_parameter_adjustment]]).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

static void modify_local_copy(int32_t x)
{
    x = 100; /* Only mutates local parameter copy */
}

static int32_t example_pass_by_value(void)
{
    int32_t val = 42;
    modify_local_copy(val);
    return val; /* Guaranteed to remain 42 */
}

/* Passing struct by value */
struct Config {
    uint32_t timeout;
    uint32_t retries;
};

static void update_timeout(struct Config cfg)
{
    cfg.timeout = 500U; /* Caller's struct remains unaffected */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Passing an uninitialized object by value to a function (reading indeterminate representation).
*   **Implementation-Defined Behavior:** The register vs. stack allocation strategy for large struct values passed by value (defined by the target ABI).
*   **Guaranteed by ISO C:** Total isolation of caller objects when passed by value.

## Edge Cases and Failure Modes
*   **Shallow Copy Traps:** If a struct contains a pointer member, passing the struct by value copies the pointer address, not the pointed-to buffer. Mutating data through that pointer modifies shared memory, breaking isolation assumptions.
*   **Stack Exhaustion:** Passing large structs by value (e.g., `struct SensorMatrix` of 256 bytes) silently duplicates the entire struct on the call stack, rapidly consuming limited MCU stack RAM and causing silent stack overflow.

## Embedded Implications
*   **Stack Consumption:** In embedded systems with minimal stack sizes (e.g., 1 KB or 2 KB FreeRTOS tasks), passing large structures by value is a catastrophic reliability hazard.
*   **Copy Overhead:** Large struct copies generate implicit `memcpy` or multi-cycle register load/store loops, disrupting execution determinism in real-time control loops.

## Firmware Review Angle
1.  **Struct Copy Audit:** Flag any function accepting a `struct` by value larger than 16 bytes (or 2 architectural words). Mandate `const StructType *` instead.
2.  **Parameter Scratchpad Use:** While permitted, modifying formal parameters as local scratchpads can confuse reviewers. Recommend using explicit local variables instead.
3.  **Uninitialized Arguments:** Ensure caller variables passed by value are fully initialized.

## Compiler, ABI, and Toolchain Implications
*   **Scalar Register Mapping:** Scalar types (`int`, `float`, pointers) pass in general-purpose registers without memory overhead.
*   **Small Struct Optimizations:** Modern ABIs (AAPCS, System V AMD64) allow structs <= 16 bytes to be packed into registers (`R0-R1` on ARM, `RAX/RDX` on x86) rather than copied to the stack.
*   **Implicit By-Reference Lowering:** If a struct is too large for registers, the compiler's ABI lowering implicitly allocates stack space, copies the struct, and passes an internal pointer to the copy.

## Performance, Memory, Timing, and Power
*   **Zero Cost for Scalars:** Passing scalars by value incurs zero copy penalty when registers are used.
*   **Memory Bandwidth Degradation:** Passing large structs by value consumes memory bus bandwidth, evicts CPU cache lines, and increases dynamic power consumption due to continuous SRAM read/write cycles.

## Verification / Debugging
*   **Compiler Flags:** Use `-Wpadded` to detect unexpected struct padding that gets unnecessarily copied during pass-by-value.
*   **Stack Usage Analysis:** Use `-fstack-usage` (GCC) to inspect stack frame inflation caused by pass-by-value structs.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 9.1:* An object shall not be read before being set.
*   **Reliability Risk:** Silent stack exhaustion on microcontrollers lacking hardware stack overflow detection (e.g., Cortex-M0 without MPU).

## Trade-offs and Alternatives
*   **Pass-by-Value vs. Pass-by-Const-Pointer:**
    *   *Pass-by-value:* Complete isolation, optimal for small scalars (<= 8 bytes).
    *   *Pass-by-const-pointer (`const T *`):* Zero copy overhead, passes only an address (4/8 bytes), but requires pointer dereference and risks aliasing.

## Staff-Level Takeaway
Pass-by-value provides rock-solid immutability guarantees for callers, but scales poorly for aggregates. Staff engineers must enforce an architectural threshold: all scalar types are passed by value; all structs larger than 2 CPU words must be passed via `const T *` to prevent stack bloat and eliminate memory copy overhead.

## Related Concepts
*   [[03_Parameter_passing]]
*   [[06_Pointer_parameters]]
*   [[08_Returning_structures]]
*   [[Stack Frame Architecture and ABI]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
