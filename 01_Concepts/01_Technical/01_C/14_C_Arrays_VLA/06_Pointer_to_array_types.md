# 06: Pointer to Array Types

## Definition
A pointer to an array type is a pointer object that points to an entire array as a single contiguous entity, rather than pointing to an individual element. In ISO C (C99 §6.7.5.2), it is declared with parentheses binding the asterisk to the pointer identifier: `T (*p)[N];`. Its pointee type is the aggregate type `T[N]`.

## Scope and Boundaries
*   **Covers:** Declaration syntax `T (*p)[N]`, type semantics, arithmetic scaling by the entire array size, 2D array row binding, and the address-of array operator (`&arr`).
*   **Does not cover:** Arrays of pointers (see [[07_Arrays_of_pointers]]), decayed scalar pointers (see [[03_Array_to_pointer_decay]]), or dynamic matrices.

## Why Does It Exist
Navigating multidimensional arrays safely requires encoding row extents into the type system:
*   **Preserving Dimensions Across Functions:** When passing a 2D array (`int m[3][4]`) to a function, it decays to a pointer to its first row: `int (*)[4]`.
*   **Stride-Safe Stepping:** Incrementing the pointer steps across entire rows with mathematical guarantees against stride mismatch.
*   **Aggregate Pointing:** Distinguishing a pointer to a single scalar (`int *`) from an anchor pointing to an entire structured block (`int (*)[N]`).

## Mechanism and Language Rules
1.  **Declaration Precedence:**
    *   `T (*p)[N];`: Pointer to an array of `N` elements of type `T`.
    *   `T *p[N];`: Array of `N` pointers to type `T` (brackets bind before `*`).
2.  **Pointer Arithmetic Scaling:** For `T (*p)[N];`, evaluating `p + 1` advances the memory address by exactly:
    $$\Delta = N 	imes 	ext{sizeof}(T)	ext{ bytes}$$
3.  **Obtaining the Pointer:** Applying unary `&` to an array `T arr[N]` yields `T (*)[N]`.
4.  **Dereferencing:**
    *   `*p`: Evaluates to the array itself (which immediately decays to `T *` pointing to element 0 in expressions).
    *   `(*p)[i]`: Accesses element `i` of the referenced array.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

#define ROW_WIDTH 4U

/* Function receiving pointer to an entire row array */
static int32_t sum_row(const int32_t (*row)[ROW_WIDTH])
{
    int32_t sum = 0;
    for (size_t i = 0; i < ROW_WIDTH; ++i) {
        sum += (*row)[i];
    }
    return sum;
}

static int32_t example_pointer_to_array(void)
{
    int32_t grid[2][ROW_WIDTH] = {
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 }
    };

    /* grid decays to pointer to its first row: int32_t (*)[4] */
    int32_t (*row_ptr)[ROW_WIDTH] = grid;

    /* row_ptr + 1 advances by 4 * sizeof(int32_t) = 16 bytes */
    row_ptr++;

    return sum_row(row_ptr); /* Sums row 1: 5 + 6 + 7 + 8 = 26 */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Stepping a pointer to an array past the boundary of a multidimensional array object and dereferencing it.
*   **Constraint Violation:** Assigning a decayed scalar pointer (`int *`) to an array pointer (`int (*)[N]`) without an explicit cast. Assigning incompatible array pointers (e.g., `int (*)[4]` to `int (*)[5]`).

## Edge Cases and Failure Modes
*   **Omitted Parentheses:** Forgetting parentheses turns `int (*p)[10]` into `int *p[10]`. The former is a single 4-byte/8-byte pointer; the latter is an array of 10 pointers (40/80 bytes), completely altering memory layout and crashing the build.
*   **Dimension Mismatch in APIs:** If a library updates a buffer row width from 16 to 32, callers passing old array pointers trigger compiler type mismatch errors, catching stride errors at compile time.

## Embedded Implications
*   **DMA 2D Transfers:** Many embedded DMA controllers support 2D transfers (block transfers with source/dest pitch). Pointers to arrays provide compile-time verification that buffer strides match DMA pitch registers.
*   **Display Framebuffer Scanlines:** TFT LCD drivers process display frames row-by-row using scanline pointers:
    ```c
    void LCD_DrawScanline(const uint16_t (*line)[320]);
    ```

## Firmware Review Angle
1.  **Check Parentheses:** Double check declarations to verify `(*p)[N]` was written rather than `*p[N]`.
2.  **Row Dimension Synchronization:** Ensure row extent `N` in `T (*p)[N]` is tied to a central `#define` rather than a magic number.
3.  **Arithmetic Verification:** Verify that pointer increments (`p++`) are intended to step by entire rows rather than individual elements.

## Compiler, ABI, and Toolchain Implications
*   **Single-Register Passing:** Pointers to arrays are regular addresses passed in a single general-purpose register (`R0` on ARM).
*   **Index Calculation Folding:** Accesses like `(*p)[i]` compile directly to base-plus-scaled-index instructions (`LDR R0, [R1, R2, LSL #2]`).

## Performance, Memory, Timing, and Power
*   **Zero RAM Overhead:** Does not allocate pointer tables; operates directly on raw contiguous blocks.
*   **Cache Stride Efficiency:** Moving row by row preserves spatial cache locality.

## Verification / Debugging
*   **GDB Inspection:** In GDB, `print *row_ptr` outputs the entire row formatted within braces: `{5, 6, 7, 8}`.
*   **Compiler Type Checks:** Compilers strictly enforce row width matching, preventing buffer stride bugs at compile time.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.5:* The declaration of an array parameter shall not contain more than two levels of indirection.
*   **Security Advantages:** Prevents stride errors where callers accidentally access unaligned row boundaries.

## Trade-offs and Alternatives
*   **Pointer to Array vs. Flat Pointer + Math:**
    *   `T (*p)[N]`: Type-safe stride, clean `p[i][j]` syntax, compile-time bound enforcement.
    *   `T *p` + `i * N + j`: Manual indexing; flexible for dynamic widths, but prone to arithmetic and stride bugs.

## Staff-Level Takeaway
A pointer to an array elevates row stride into C's type system. Staff engineers should enforce `T (*p)[N]` when passing contiguous matrix blocks or framebuffer scanlines to ensure the compiler verifies row strides at compile time without incurring pointer-table memory overhead.

## Related Concepts
*   [[03_Array_to_pointer_decay]]
*   [[05_Multidimensional_arrays]]
*   [[07_Arrays_of_pointers]]
*   [[13_C_Pointers/11_Pointer_to_array]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
