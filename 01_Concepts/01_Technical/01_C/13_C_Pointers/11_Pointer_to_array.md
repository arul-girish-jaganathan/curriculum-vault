# 11: Pointer to Array

## Definition
A pointer to an array is a pointer object that points to an entire array as a single contiguous object, rather than to an individual element. In ISO C (C99 §6.7.5.2), it is declared with explicit parentheses around the pointer declarator: `T (*p)[N];`. Its pointee type is the array type `T[N]`, meaning pointer arithmetic scales by the size of the entire array (`N * sizeof(T)`).

## Scope and Boundaries
*   **Covers:** Syntax of `T (*p)[N]`, difference between pointer-to-array and array-of-pointers, multi-dimensional array navigation, decayed array pointers, and pointer arithmetic scaling.
*   **Does not cover:** Arrays of pointers (see [[10_Pointer_to_pointer]]), single-dimensional array decay (see [[03_Address_of_and_dereference]]), or variable-length arrays (VLAs) in detail (see [[Variable Length Arrays]]).

## Why Does It Exist
Multi-dimensional arrays in C are stored in contiguous row-major memory:
*   **Preserving Dimensions Across Functions:** Passing a 2D array (`int matrix[3][4]`) to a function decays the array into a pointer to its first element—which is an entire row (`int (*)[4]`).
*   **Stride-Safe Navigation:** A pointer to an array encodes the row stride directly in the type system, ensuring that pointer increments step over entire rows accurately.
*   **Memory Efficiency:** Unlike an array of pointers (which requires separate pointer tables and memory allocations), a pointer to an array traverses contiguous blocks with zero pointer-table overhead.

## Mechanism and Language Rules
1.  **Declaration Syntax:**
    *   `int (*p)[5];`: Pointer to an array of 5 `int`s. (Parentheses bind `*` to `p`).
    *   `int *p[5];`: Array of 5 pointers to `int`. (Brackets have higher precedence than `*`).
2.  **Decay Semantics:** Given `int matrix[3][5];`, evaluating the identifier `matrix` decays to a pointer to its first row: type `int (*)[5]`, with value `&matrix[0]`.
3.  **Address Equivalence vs. Type Difference:**
    *   `matrix`: Evaluates to `int (*)[5]` (points to row 0).
    *   `&matrix`: Evaluates to `int (*)[3][5]` (points to entire matrix).
    *   `matrix[0]`: Evaluates to `int *` (points to element `matrix[0][0]`).
    *   All three evaluate to the exact same physical byte address, but each has entirely different type semantics and pointer arithmetic strides.
4.  **Arithmetic Scaling:** For `int (*p)[5];`, `p + 1` advances the address by `5 * sizeof(int)` bytes.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

#define COLS 4U
#define ROWS 3U

/* Correct: Function receiving pointer to 2D array row */
static int32_t sum_row(const int32_t (*row)[COLS])
{
    int32_t total = 0;
    for (size_t j = 0; j < COLS; ++j) {
        total += (*row)[j]; /* Dereference row, then index element */
    }
    return total;
}

static int32_t example_matrix(void)
{
    int32_t matrix[ROWS][COLS] = {
        { 1,  2,  3,  4 },
        { 5,  6,  7,  8 },
        { 9, 10, 11, 12 }
    };

    /* matrix decays to pointer to its first row: int32_t (*)[4] */
    int32_t (*row_ptr)[COLS] = matrix;

    /* row_ptr + 1 advances by exactly sizeof(int32_t) * 4 bytes (16 bytes) */
    row_ptr++;

    return sum_row(row_ptr); /* Sums second row: 5 + 6 + 7 + 8 = 26 */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:**
    *   Dereferencing a pointer to an array out of allocated array bounds.
    *   Casting an incompatible flat array pointer (e.g., `int *`) to `int (*)[N]` and accessing elements if alignment or bounds are violated.
*   **Constraint Violation:** Attempting to assign `int *` to `int (*)[N]` without an explicit cast. Mismatched array size parameters (e.g., assigning `int (*)[4]` to `int (*)[5]`) is a type incompatibility constraint violation.

## Edge Cases and Failure Modes
*   **Parentheses Omission:** Omitting parentheses turns `int (*p)[5]` into `int *p[5]`. The former is a single 4-byte/8-byte pointer; the latter is an array of 5 pointers (20 or 40 bytes), causing stack bloat and syntax compilation failures.
*   **Row Bounds Flattening:** Flattening multi-dimensional arrays by casting `matrix` to `int *` bypasses compiler boundary checking across rows and can confuse static analysis tools tracking buffer bounds.
*   **VLA Dimensions:** In C99, `void func(int n, int (*p)[n])` uses a Variable Length Array pointer. If `n` is negative or causes stack exhaustion, behavior is undefined.

## Embedded Implications
*   **Display Framebuffers:** Embedded graphical displays (TFT/OLED) are organized as 2D pixel matrices (e.g., `uint16_t frame[240][320]`). Frame manipulation functions pass pointers to scanlines using pointers to arrays:
    ```c
    void process_scanline(uint16_t (*line)[320]);
    ```
*   **DMA Stride Configurations:** Configuring 2D DMA transfers requires programming physical row pitch/stride. Pointers to arrays guarantee that row strides remain compile-time invariant constants.
*   **Contiguous Hardware Tables:** Look-up tables with fixed-length records benefit from pointers to arrays because data is guaranteed contiguous in Flash, avoiding the pointer table indirection of ragged arrays.

## Firmware Review Angle
1.  **Declaration Syntax Verification:** Double check parentheses in declarations to ensure `(*p)[N]` was not intended to be `*p[N]`.
2.  **Dimension Matching:** Ensure that hardcoded array dimensions (`COLS`) match hardware peripheral or communication frame specifications.
3.  **No Dynamic Sizing via VLA:** Ensure pointer-to-array declarations use fixed compile-time constants for sizes, avoiding VLAs on memory-constrained embedded targets.

## Compiler, ABI, and Toolchain Implications
*   **Hardware Multiplication:** Accessing `p[i][j]` requires computing `base + (i * N + j) * sizeof(T)`. Compilers optimize `i * N` using hardware multipliers or shift-add sequences if `N` is a constant.
*   **ABI Passing:** Pointers to arrays are passed in standard pointer registers (e.g., `R0` on ARM) just like scalar pointers.

## Performance, Memory, Timing, and Power
*   **Zero Pointer Overhead:** Pointers to arrays navigate 2D memory structures without allocating auxiliary pointer look-up tables in RAM, saving memory.
*   **Cache Line Contiguity:** All elements in a multi-dimensional array referenced via `int (*)[N]` are strictly contiguous in physical RAM, ensuring maximum cache efficiency and burst-read throughput.

## Verification / Debugging
*   **Compiler Warnings:** Compilers flag dimension mismatches with `-Wpointer-sign` and type incompatibility errors.
*   **GDB Inspection:** GDB understands array pointers: `print *row_ptr` prints the entire array row in formatted brackets (`{5, 6, 7, 8}`).
*   **Static Analysis:** Static analysis tools verify that row and column indices never exceed declared bounds.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.5:* Array parameter declarations shall contain at most two levels of indirection.
    *   *Rule 18.1:* Out-of-bounds pointer arithmetic is strictly prohibited.
*   **Security Vulnerabilities:** Buffer overflows frequently occur when calculating offsets in multi-dimensional buffers manually. Utilizing pointers to arrays allows the compiler to enforce row stride safety.

## Trade-offs and Alternatives
*   **Pointer to Array vs. Array of Pointers:**
    *   `int (*p)[N]` (Pointer to Array): Single allocation, strictly contiguous, zero pointer table overhead, fixed row length.
    *   `int *p[N]` (Array of Pointers): Multiple allocations, non-contiguous, pointer table overhead, allows ragged (variable length) rows.
    *   In embedded firmware, prefer `int (*p)[N]` for performance and memory predictability.

## Staff-Level Takeaway
A pointer to an array encapsulates both address and row dimension within C's type system. Staff engineers should leverage `T (*p)[N]` when passing contiguous matrix or buffer data to functions. It guarantees compile-time verification of row strides, ensures physical memory contiguity, and prevents the memory fragmentation associated with arrays of pointers.

## Related Concepts
*   [[01_Pointer_declarations]]
*   [[07_Pointer_arithmetic]]
*   [[10_Pointer_to_pointer]]
*   [[Variable Length Arrays]]
*   [[Memory Alignment and Padding]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
