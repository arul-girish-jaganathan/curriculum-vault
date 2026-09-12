# 05: Multidimensional Arrays

## Definition
A multidimensional array is an array whose elements are themselves arrays. In ISO C (C99 §6.7.5.2), multidimensional arrays are stored in strictly contiguous, row-major order with zero padding between rows, meaning the rightmost index varies fastest in physical memory layout.

## Scope and Boundaries
*   **Covers:** Declaration, row-major memory mapping formulas, 2D/3D indexing, multidimensional decay semantics, and flattened memory traversal.
*   **Does not cover:** Arrays of pointers / jagged arrays (see [[07_Arrays_of_pointers]]), pointers to array types (see [[06_Pointer_to_array_types]]), or dynamic multidimensional allocation.

## Why Does It Exist
Many scientific and hardware domains operate on multi-axis datasets:
*   **Display Framebuffers:** 2D pixel grids (e.g., Display matrices: `pixels[height][width]`).
*   **Mathematical Matrices:** Vector transformations, rotation matrices, and linear filtering.
*   **Memory Efficiency:** Unlike jagged arrays (which require pointer look-up tables), multidimensional arrays are strictly contiguous, consuming zero auxiliary RAM.

## Mechanism and Language Rules
1.  **Row-Major Layout:** For `T arr[R][C]`, row 0 is stored immediately followed by row 1. Element `arr[i][j]` maps physically to address:
    $$	ext{Address}(i, j) = 	ext{Base} + (i 	imes C + j) 	imes 	ext{sizeof}(T)$$
2.  **Decay Semantics:** A 2D array `int m[3][4]` does **not** decay to `int **`. It decays to a pointer to its first element (which is an entire row of 4 ints): `int (*)[4]`.
3.  **Inferred First Dimension:** When initializing, only the first dimension can be omitted: `int m[][2] = {{1, 2}, {3, 4}};` is legal. All subsequent column dimensions must be explicitly specified.
4.  **Row Subscript Equivalence:** `m[i][j]` is mathematically evaluated as `*(*(m + i) + j)`.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

#define ROWS 2U
#define COLS 3U

/* Contiguous row-major storage proof */
static int32_t example_multidim(void)
{
    int32_t matrix[ROWS][COLS] = {
        { 10, 20, 30 },
        { 40, 50, 60 }
    };

    /* Flattened traversal: row 1 begins immediately after row 0 */
    const int32_t *flat_ptr = &matrix[0][0];
    int32_t element_1_0 = flat_ptr[3]; /* matrix[1][0] == 40 */

    return element_1_0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Accessing elements past row/column dimensions (e.g., `matrix[0][5]` on a `3x3` matrix). Although contiguous in RAM, accessing out-of-row bounds invokes undefined behavior under ISO C object boundary rules.
*   **Constraint Violation:** Declaring a multidimensional array where any non-leading dimension is omitted or variable without VLA support.

## Edge Cases and Failure Modes
*   **The Cache-Thrashing Column Stride:** Iterating over columns in the outer loop and rows in the inner loop (`for(j) for(i) arr[i][j]`) strides across memory by `COLS * sizeof(T)` bytes on every step, evicting CPU cache lines and dropping throughput by up to 90%.
*   **Wrong Decay Type:** Casting a 2D array `matrix[3][4]` to `int **` causes an immediate HardFault or crash on dereference, because the CPU treats the integer data at row 0 as a memory address.

## Embedded Implications
*   **Display Scanlines:** Embedded graphical displays use 2D arrays. Rendering horizontal scanlines corresponds directly to contiguous burst writes over SPI/DMA.
*   **Lookup Tables with Multi-Index Keys:** Calibration tables (e.g., `sensor_cal[temperature_band][voltage_band]`) reside in Flash as contiguous multidimensional `const` arrays.

## Firmware Review Angle
1.  **Row-Major Loop Order:** Check all nested loops. The innermost loop must iterate over the rightmost (column) index to maximize cache/memory burst efficiency.
2.  **Column Dimensions Bound:** Verify that functions taking 2D arrays explicitly specify column dimensions in prototypes (`void f(int arr[][COLS])`).
3.  **No `int **` Casts:** Reject any cast of a 2D array to a double pointer.

## Compiler, ABI, and Toolchain Implications
*   **Multiplier Hardware Optimization:** The compiler calculates row offsets using multiply instructions (`MUL`). If `COLS` is a power of 2, the compiler replaces multiplication with a single-cycle arithmetic left shift (`LSL`).
*   **Auto-Vectorization:** Row-major sequential loops enable compilers to emit SIMD/NEON instructions across adjacent row elements.

## Performance, Memory, Timing, and Power
*   **Zero Pointer Table Overhead:** Consumes exactly `ROWS * COLS * sizeof(T)` bytes of memory.
*   **Power of 2 Strides:** Sizing column widths to powers of 2 (e.g., 16, 32, 64) improves indexing speed and reduces instruction cycle counts.

## Verification / Debugging
*   **GDB Inspection:** GDB prints multidimensional arrays with formatted sub-braces: `print matrix` -> `{{10, 20, 30}, {40, 50, 60}}`.
*   **Static Analysis:** Static tools verify that row and column index bounds are strictly respected.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.1:* Out-of-bounds pointer arithmetic is prohibited.
*   **Security Vulnerabilities:** Unchecked row or column indices permit out-of-bounds read/write access to neighboring matrix rows and adjacent memory structures.

## Trade-offs and Alternatives
*   **Multidimensional Array vs. 1D Flattened Buffer:**
    *   `arr[R][C]`: Cleaner multi-index syntax, type-enforced column stride.
    *   `arr[R * C]`: Maximum portability, easier dynamic allocation, manual index math (`i * C + j`).

## Staff-Level Takeaway
Multidimensional arrays are strictly contiguous row-major structures. Staff engineers must mandate row-major traversal order to preserve cache lines, ensure column dimensions are powers of 2 where possible to eliminate hardware division/multiplication, and prevent type confusion between true 2D arrays and arrays of pointers.

## Related Concepts
*   [[01_Array_declaration]]
*   [[03_Array_to_pointer_decay]]
*   [[06_Pointer_to_array_types]]
*   [[07_Arrays_of_pointers]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
