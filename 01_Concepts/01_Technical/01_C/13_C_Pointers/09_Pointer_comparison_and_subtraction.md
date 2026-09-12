# 09: Pointer Comparison and Subtraction

## Definition
Pointer comparison evaluates the relative position or equality of two pointers. Pointer subtraction (difference) calculates the number of elements separating two pointers. Under ISO C (C99 §6.5.8 and §6.5.6), relational comparisons and subtractions are valid **only** if both operands point to elements of the same array object or one past its end. The result of pointer subtraction has the signed integer type `ptrdiff_t`.

## Scope and Boundaries
*   **Covers:** Relational comparisons (`<`, `<=`, `>`, `>=`), equality comparisons (`==`, `!=`), pointer subtraction (`p1 - p2`), the `ptrdiff_t` type, and array boundaries.
*   **Does not cover:** Pointer addition (see [[07_Pointer_arithmetic]]), one-past boundary guarantees (see [[08_One_past_the_end]]), or pointer-to-integer conversions (see [[uintptr_t and intptr_t]]).

## Why Does It Exist
Systems programming requires determining distance and ordering in memory:
*   **Measuring Buffer Consumption:** Subtraction calculates how many items have been pushed to or popped from a buffer.
*   **Range Validation:** Relational comparison ensures a pointer resides within the valid boundaries of an allocated array before performing operations.
*   **Loop Termination:** Half-open ranges (`p < end`) require relational comparisons to cleanly terminate iterations.

## Mechanism and Language Rules
1.  **Equality Comparisons (`==`, `!=`):**
    *   Pointers of compatible types may be compared for equality anywhere.
    *   Any pointer can be compared with a null pointer constant.
    *   Two pointers compare equal if both are null, both point to the same object or function, or both point one past the same array.
2.  **Relational Comparisons (`<`, `<=`, `>`, `>=`):**
    *   Both pointers must point to elements of the same array object or one past the end.
    *   Pointers to members of the same aggregate (struct) compare in the order of member declaration.
    *   Comparing pointers to unrelated objects (e.g., two distinct global variables or different heap allocations) invokes undefined behavior.
3.  **Pointer Subtraction (`p1 - p2`):**
    *   Both operands must point to elements of the same array object or one past its end.
    *   The result is the number of elements between `p1` and `p2`, not the number of bytes.
    *   The result type is `ptrdiff_t`, a signed integer type defined in `<stddef.h>`.
    *   Formula: `(address(p1) - address(p2)) / sizeof(*p1)`.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

static ptrdiff_t example_subtraction(const int32_t *start, const int32_t *end)
{
    /* end and start must point into the same array */
    return end - start; /* Returns element count, not byte count */
}

static bool example_in_range(const int32_t *arr, size_t len, const int32_t *target)
{
    const int32_t *end = arr + len;
    /* Relational comparison valid only within same array bounds */
    return (target >= arr) && (target < end);
}

/* Incorrect: Comparing unrelated objects */
static bool invalid_comparison(void)
{
    int a = 10;
    int b = 20;
    /* return &a < &b; */ /* Undefined Behavior: unrelated objects */
    return false;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:**
    *   Subtracting or relationally comparing pointers to unrelated objects (different variables, independent malloc buffers).
    *   Subtracting pointers when the result overflows the range expressible by `ptrdiff_t`.
    *   Performing relational comparisons or subtraction with null pointers.
*   **Implementation-Defined Behavior:** The exact bit width and integer type corresponding to `ptrdiff_t` (commonly `int` on 32-bit systems, `long` on 64-bit systems).
*   **Unspecified Behavior:** Comparing pointers to different members of a `union`.

## Edge Cases and Failure Modes
*   **Flat Address Space Assumption:** In segmented memory architectures (e.g., x86 real mode, DSP far-memory), pointers consist of segment:offset pairs. Comparing or subtracting pointers with different segments without normalization fails completely.
*   **The Flat Memory Trap:** On modern 32-bit/64-bit platforms with flat addressing, engineers mistakenly assume that `&a < &b` is valid because physical memory addresses are flat integers. However, compiler optimizers treat comparison of unrelated pointers as undefined, and can legally eliminate bounds checks or reorder code based on this assumption.
*   **`ptrdiff_t` Overflow:** If an array spans more than half the address space (possible in 16-bit systems or huge 32-bit arrays), subtracting the first element from the last element can mathematically exceed the maximum positive value representable by signed `ptrdiff_t`, producing an overflow and UB.

## Embedded Implications
*   **Circular Ring Buffers:** Ring buffers that track `head` and `tail` pointers directly must never subtract pointers across the circular wrap-around boundary without adjusting for buffer size.
*   **Flash vs. RAM Range Validation:** Validating whether an unknown pointer points into RAM or Flash by comparing it against section boundary symbols:
    ```c
    /* Common in bare-metal systems, but technically outside ISO C */
    extern uint32_t _sram_start, _sram_end;
    bool is_ram = (ptr >= &_sram_start && ptr < &_sram_end);
    ```
    To avoid compiler undefined behavior optimizations on unrelated object comparisons, use integer addresses:
    ```c
    uintptr_t addr = (uintptr_t)ptr;
    bool is_ram = (addr >= (uintptr_t)&_sram_start && addr < (uintptr_t)&_sram_end);
    ```

## Firmware Review Angle
1.  **Unrelated Object Comparison:** Flag any relational comparison (`<`, `>`) between pointers that do not originate from the same array.
2.  **Cast to `uintptr_t` for Bounds Checking:** Ensure that system-wide memory checks (e.g., checking if an address lies in RAM, Flash, or Stack) cast pointers to `uintptr_t` before comparing.
3.  **Format Specifiers:** Ensure `ptrdiff_t` is printed using the `%td` format specifier, never `%d` or `%ld`.
4.  **Null Guard:** Check that neither operand in a subtraction is `NULL`.

## Compiler, ABI, and Toolchain Implications
*   **Division Folding:** Compilers implement `p1 - p2` by emitting a subtraction followed by an arithmetic shift or divide instruction by `sizeof(T)` (e.g., `ASRS R0, R0, #2` for 4-byte integers).
*   **Optimization Assumptions:** GCC and Clang will assume that if `p1 < p2` is evaluated, `p1` and `p2` belong to the same object. The optimizer can propagate this assumption across LTO, potentially eliminating code paths it deems unreachable.

## Performance, Memory, Timing, and Power
*   **Power of 2 Scaling:** Structs or data types whose `sizeof` is a power of 2 (1, 2, 4, 8, 16) allow pointer subtraction to use single-cycle arithmetic right shifts instead of multi-cycle hardware integer division instructions.
*   **Cycle Cost:** On architectures lacking hardware integer divide (e.g., ARM Cortex-M0/M3 without divide or with non-power-of-2 types), pointer subtraction can incur costly software division routines (`__aeabi_idiv`).

## Verification / Debugging
*   **Compiler Flags:** Use `-Wextra` and `-Wsign-conversion` to track `ptrdiff_t` conversions.
*   **Sanitizers:** Compile with UndefinedBehaviorSanitizer (`-fsanitize=pointer-subtract`) to trap illegal pointer subtractions across distinct objects at runtime.
*   **Static Analysis:** Tools enforce MISRA rules prohibiting pointer math and comparison across unrelated storage blocks.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.2:* Subtraction between pointers shall only be applied to pointers that address elements of the same array.
    *   *Rule 18.3:* Relational operators shall not be applied to pointer types except where they point into the same array.
*   **Security Vulnerabilities:** Integer underflows or sign misinterpretations in pointer difference calculations lead to buffer allocations that are too small, enabling heap or stack overflows.

## Trade-offs and Alternatives
*   **Pointers vs. Offsets/Indices:** Tracking positions using integer offsets (`size_t index`) instead of raw pointers eliminates all comparison and subtraction portability traps, as integer comparisons and subtractions are always well-defined.

## Staff-Level Takeaway
Pointer comparisons and subtractions are mathematically bound to the object model of C: they are only valid within a single array allocation. Never compare raw pointers to arbitrary memory blocks directly. For hardware memory region verification, convert the pointers to `uintptr_t` to perform well-defined unsigned integer address comparisons.

## Related Concepts
*   [[07_Pointer_arithmetic]]
*   [[08_One_past_the_end]]
*   [[uintptr_t and intptr_t]]
*   [[Memory Alignment and Padding]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
