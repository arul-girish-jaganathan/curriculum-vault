# 11: Array Bounds and Safety

## Definition
Array bounds define the valid range of indices ($0$ through $N-1$) for an array of extent $N$. In ISO C (C99 §6.5.6), referencing an array element outside these boundaries constitutes an out-of-bounds access and invokes undefined behavior. ISO C does **not** provide native runtime bounds checking.

## Scope and Boundaries
*   **Covers:** Boundary invariants, out-of-bounds consequences, buffer over-read and overflow exploits, static bounds checking, and defensive bounds validation patterns.
*   **Does not cover:** One-past-the-end pointer mechanics (see [[13_C_Pointers/08_One_past_the_end]]), array decay (see [[03_Array_to_pointer_decay]]), or dynamic bounds mitigation (MPU configurations).

## Why Does It Exist
C was designed for raw execution speed and direct hardware control:
*   **Zero Abstraction Penalty:** Omitting automatic bounds checking eliminates hidden conditional branches on every array access.
*   **Predictable Execution:** Real-time embedded systems achieve cycle-level determinism by eliminating hardware-level bounds exceptions.
*   **Trade-off:** Shifting the burden of bounds verification entirely onto the software engineer.

## Mechanism and Language Rules
1.  **Valid Index Range:** For an array declared as `T arr[N]`:
    *   Valid index expressions: $0 \le i \le N - 1$.
    *   Valid address range: `&arr[0]` through `&arr[N]` (the one-past-the-end sentinel).
2.  **No Language Traps:** Reading `arr[N]` or `arr[-1]` is syntactically valid C, but violates language semantics and triggers undefined behavior immediately.
3.  **Subscript Identity:** `arr[i]` is identical to `*(arr + i)`. If `i` is negative or $\ge N$, the pointer arithmetic creates an invalid address reference.
4.  **Static Boundary Enforcement:** In C11, bounds-checking interfaces (Annex K, e.g., `memcpy_s`) were introduced, but are optional and widely criticized; architectural safety patterns are preferred.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define TABLE_CAPACITY 16U

static const uint16_t g_lut[TABLE_CAPACITY] = { 0 };

/* Correct: Strict defensive bounds check before access */
static bool read_lut_safe(size_t index, uint16_t *out_val)
{
    if (index >= TABLE_CAPACITY || out_val == NULL) {
        return false; /* Boundary violation prevented */
    }

    *out_val = g_lut[index];
    return true;
}

/* Incorrect: Out-of-bounds read vulnerability */
static uint16_t unsafe_read(size_t index)
{
    return g_lut[index]; /* DANGER: If index >= 16, undefined behavior */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Reading or writing an array element using an index $< 0$ or $\ge N$.
*   **Optimizer Exploitation:** Modern compilers assume out-of-bounds array access never occurs. If a loop relies on reading past an array to encounter a sentinel, the compiler may optimize away surrounding safety logic or reorder memory operations.

## Edge Cases and Failure Modes
*   **Off-By-One Boundary Bugs:** Writing `<=` instead of `<` in loop conditions (`for (size_t i = 0; i <= N; ++i)`) accesses the one-past-the-end element, corrupting the adjacent stack or heap byte.
*   **Signed Integer Underflow:** Using signed `int` for indices: passing `i = -1` bypasses naive upper-bound checks (`if (i < MAX)`) and accesses memory preceding the array. Always use `size_t` for array indexing.

## Embedded Implications
*   **Stack Smashing / HardFaults:** Local stack array overruns corrupt the function's Link Register (LR) or stored Program Counter (PC), triggering a HardFault upon return.
*   **Global Variable Corruption:** Overwriting past the bounds of an array in `.data`/`.bss` silently alters unrelated state flags, sensor calibration values, or RTOS task structures without immediate crashes, creating undebuggable intermittent failures.

## Firmware Review Angle
1.  **Unsigned Index Types:** Verify that all array indices are unsigned (`size_t`, `uint32_t`) to prevent negative index exploits.
2.  **Explicit Precondition Checks:** Ensure any index derived from external inputs (UART, CAN, SPI, user input) is validated against array capacity prior to use.
3.  **Audit Loop Limits:** Inspect loop termination conditions to ensure `<` is used with element count limits, never `<=`.

## Compiler, ABI, and Toolchain Implications
*   **Stack Canaries:** The compiler inserts canaries (`-fstack-protector-strong`) between local arrays and control flow data to abort execution if an overflow occurs.
*   **Static Boundary Warnings:** Compilers emit `-Warray-bounds` when array indices can be statically proven to exceed declared extents.

## Performance, Memory, Timing, and Power
*   **Branch Cost:** Manual bounds checks (`if (i >= CAP)`) introduce a branch. On modern pipelined MCUs, predictable branches cost 1 cycle; mispredicted branches cost 2-3 cycles.
*   **Determinism:** Eliminating language-level bounds exceptions ensures loop execution times remain mathematically deterministic.

## Verification / Debugging
*   **Sanitizers:** Compile host unit tests with AddressSanitizer (`-fsanitize=address`) and UndefinedBehaviorSanitizer (`-fsanitize=bounds`).
*   **Static Analysis:** Formal verification tools (Astrée, Polyspace) prove absence of out-of-bounds array accesses mathematically.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.1:* A pointer resulting from arithmetic on a pointer operand shall address elements of the same array.
*   **Security Vulnerabilities:**
    *   CWE-121: Stack-based Buffer Overflow.
    *   CWE-125: Out-of-bounds Read (e.g., Heartbleed vulnerability).
    *   CWE-787: Out-of-bounds Write.

## Trade-offs and Alternatives
*   **Manual Bounds Checking vs. Span Envelopes:**
    *   *Manual Checking:* Fast, but prone to human omission.
    *   *Span Data Structure:* Packaging array pointer and capacity into a `Span` struct and accessing solely via verified helper functions guarantees continuous safety.

## Staff-Level Takeaway
Bounds enforcement in C is entirely the programmer's responsibility. Staff engineers must enforce three mandatory defenses: compile with `-Warray-bounds` and `-fstack-protector-strong`, mandate `size_t` for all index variables, and enforce boundary validations at every interface boundary where external inputs convert into array indices.

## Related Concepts
*   [[01_Array_declaration]]
*   [[10_sizeof_arrays]]
*   [[13_C_Pointers/07_Pointer_arithmetic]]
*   [[13_C_Pointers/08_One_past_the_end]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
