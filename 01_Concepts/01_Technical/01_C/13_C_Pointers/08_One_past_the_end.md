# 08: One Past the End

## Definition
The "one-past-the-end" pointer is an address value that points precisely one element beyond the last element of an array object. In ISO C (C99 §6.5.6), the language explicitly guarantees that a pointer can validly point to the element immediately following the final element of an array; however, dereferencing this pointer invokes undefined behavior.

## Scope and Boundaries
*   **Covers:** Semantics of the one-past-the-end address, loop termination conditions, boundary guarantees under ISO C, pointer comparisons at the boundary, and single-object array semantics.
*   **Does not cover:** General pointer arithmetic (see [[07_Pointer_arithmetic]]), general pointer subtraction (see [[09_Pointer_comparison_and_subtraction]]), or out-of-bounds memory corruption bugs (see [[Dynamic Memory Allocation]]).

## Why Does It Exist
Iterating over collections requires an unambiguous sentinel to signal completion without needing separate index counter tracking:
*   **Asymmetric Half-Open Intervals:** Idiomatic C and C++ algorithms represent ranges as `[begin, end)`, where `end` is one past the last valid element.
*   **Mathematical Simplicity:** The number of elements in `[begin, end)` is cleanly given by `end - begin`.
*   **Avoid Special Casing:** Without the one-past-the-end guarantee, the final iteration of a loop stepping a pointer across an array would produce an illegal out-of-bounds pointer upon incrementing past the final element, making idiomatic while/for pointer loops non-compliant.

## Mechanism and Language Rules
1.  **Language Guarantee:** If `p` points to the last element of an array with `N` elements, `p + 1` is guaranteed to be a valid pointer value within the abstract C machine.
2.  **No Dereferencing:** A one-past-the-end pointer does not point to a valid object. Applying the indirection operator `*` to it results in undefined behavior (read or write).
3.  **Comparison Permitted:** A one-past-the-end pointer may be legally compared for equality (`==`, `!=`) or relational ordering (`<`, `<=`, `>`, `>=`) against any other pointer pointing to elements within the same array or its one-past boundary.
4.  **No Increment Past End:** Attempting to add an integer to a one-past-the-end pointer (e.g., `(end_ptr + 1)`) produces an invalid pointer and triggers undefined behavior immediately.
5.  **Single Object Rule:** An individual non-array variable `int x;` is treated as an array of length 1; thus, `&x + 1` is valid as a one-past-the-end pointer.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stddef.h>
#include <stdint.h>

#define ARRAY_SIZE 4U

static uint32_t example_one_past(void)
{
    uint32_t array[ARRAY_SIZE] = { 10U, 20U, 30U, 40U };
    uint32_t sum = 0U;

    /* Correct: end points one-past-the-end of array */
    const uint32_t * const end = array + ARRAY_SIZE;

    for (const uint32_t *p = array; p < end; ++p) {
        sum += *p; /* Dereference is safe for p < end */
    }

    /* At loop termination, p == end (one-past-the-end pointer) */
    return sum;
}

/* Incorrect: Dereferencing one-past-the-end */
static uint32_t invalid_one_past_deref(void)
{
    uint32_t array[ARRAY_SIZE] = { 0 };
    const uint32_t *end = array + ARRAY_SIZE;

    return *end; /* Undefined Behavior: dereferencing one-past-the-end */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:**
    *   Dereferencing a one-past-the-end pointer (`*end`).
    *   Stepping beyond one-past-the-end (`end + 1`).
    *   Subtracting a negative offset that steps past the beginning or past one-past-the-end.
*   **Implementation-Defined / Architecture Risks:** If an array is placed at the absolute top edge of the memory address space (e.g., ending at `0xFFFFFFFF` on a 32-bit architecture), calculating the one-past-the-end pointer causes integer wrap-around to `0x00000000` (NULL), breaking relational comparisons like `p < end`.

## Edge Cases and Failure Modes
*   **Memory Boundary Wrap-Around:** On embedded microcontrollers where internal SRAM or Flash extends to the absolute end of the physical address space (e.g., ending at `0xFFFFFFFF`), allocating an array at the very top of memory causes `array + SIZE` to wrap to `0x00000000`. Loops like `for (p = arr; p < end; p++)` become infinite loops because `p < 0` is false immediately, or memory faults occur.
*   **Off-By-One Dereference:** A classic failure mode in C loops:
    ```c
    for (int *p = arr; p <= end; ++p) { /* Bug: p <= end dereferences end */
        *p = 0;
    }
    ```
*   **One-Before-The-Beginning:** ISO C does **not** provide a symmetric "one-before-the-beginning" pointer guarantee. Writing `arr - 1` triggers undefined behavior immediately, even if never dereferenced.

## Embedded Implications
*   **Linker Script Memory Region Limits:** Embedded linker scripts define memory segments using boundary symbols:
    ```ld
    _sdata = .;
    /* ... data symbols ... */
    _edata = .;
    ```
    Here, `_edata` represents the one-past-the-end address of the `.data` segment. Firmware initialization routines iterate while `dst < &_edata`.
*   **MPU Region Guarding:** When placing memory protection guards (e.g., MPU regions or stack canaries), remember that `end` addresses often fall inside the neighboring memory page or peripheral space. Ensure access permissions do not panic on the address calculation itself.

## Firmware Review Angle
1.  **Loop Boundary Operators:** Scrutinize loop conditions using `<` versus `<=`. Iterations over `[start, end)` must use `p < end` or `p != end`.
2.  **Top-of-Memory Linker Sections:** Check linker scripts to ensure no array or heap section terminates precisely at the maximum 32-bit boundary (`0xFFFFFFFF`).
3.  **Reverse Iteration Checks:** When walking arrays in reverse, ensure developers do not decrement past the first element (`p >= start` followed by `p--` when `p == start` leads to `arr - 1`, which is UB).

## Compiler, ABI, and Toolchain Implications
*   **Pointer Comparison Elimination:** The compiler assumes `p + 1 > p`. If `p + 1` wraps around to `0` at the top of memory, the compiler's optimizer may eliminate boundary checks, assuming wrap-around is impossible under ISO C.
*   **Vectorization and Loop Unrolling:** Compilers rely on the half-open interval `[start, end)` to calculate trip counts: `(end - start) / sizeof(T)`. This allows auto-vectorizers (NEON, SSE) to emit SIMD burst loops without runtime overhead.

## Performance, Memory, Timing, and Power
*   **Instruction Efficiency:** Comparing against an explicit one-past pointer (`p != end`) compiles to a single compare-and-branch instruction (`CMP`, `BNE`), matching register-level pointer increments without separate index math.
*   **No Extra Storage:** The one-past-the-end sentinel requires no additional sentinel object allocation in RAM; it is purely an address value.

## Verification / Debugging
*   **Compiler Sanitizers:** GCC/Clang AddressSanitizer (`-fsanitize=address`) flags one-past-the-end dereferences immediately as a buffer overflow.
*   **GDB Inspection:** In GDB, `print array + ARRAY_SIZE` shows the terminal address. If `p` equals this value, dereferencing must not be permitted.
*   **Static Analysis:** Tools like Clang Static Analyzer detect off-by-one errors where loops terminate with `<=` instead of `<`.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.1:* A pointer resulting from arithmetic shall address an element of the same array or the one-past-the-end element.
*   **Security Vulnerabilities:**
    *   CWE-193: Off-by-one Error.
    *   Dereferencing one-past-the-end on writes corrupts adjacent memory (e.g., heap headers, neighboring variables, or stack frames). On reads, it leaks adjacent data.

## Trade-offs and Alternatives
*   **Pointer Iteration vs. Counter Loops:**
    *   `for (size_t i = 0; i < N; ++i)`: Inherently safe against pointer wrap-around; bounds are clear.
    *   `for (T *p = arr; p < end; ++p)`: Cleaner machine code on simple architectures; avoids recomputing base offsets.
    *   Prefer counter loops unless profiling proves pointer walking produces measurable performance improvements.

## Staff-Level Takeaway
The one-past-the-end pointer is a deliberate mathematical allowance in the C standard designed to support asymmetric ranges `[begin, end)`. A Staff engineer must ensure developers never dereference this sentinel, never decrement before the beginning of an array, and ensure linker scripts leave at least a 1-byte gap at the absolute ceiling of the physical memory map to prevent address wrap-around.

## Related Concepts
*   [[07_Pointer_arithmetic]]
*   [[09_Pointer_comparison_and_subtraction]]
*   [[Linker Scripts and Memory Sections]]
*   [[Storage Duration and Lifetime]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
