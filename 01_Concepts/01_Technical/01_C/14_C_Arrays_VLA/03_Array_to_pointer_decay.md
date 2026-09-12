# 03: Array-to-Pointer Decay

## Definition
Array-to-pointer decay is the implicit conversion in ISO C (C99 §6.3.2.1p3) where an lvalue of array type is automatically converted into an rvalue pointer to the array's initial element (type `T[N]` -> `T *`). The resulting pointer value is the address of the first element (`&arr[0]`).

## Scope and Boundaries
*   **Covers:** The array decay mechanism, pointer conversions in expressions, and the three canonical exceptions where decay does *not* occur.
*   **Does not cover:** Function parameter adjustment (see [[04_Array_parameter_adjustment]]), pointer arithmetic (see [[13_C_Pointers/07_Pointer_arithmetic]]), or pointers to whole arrays (see [[06_Pointer_to_array_types]]).

## Why Does It Exist
Array decay was designed into early C by Dennis Ritchie to avoid treating arrays as first-class composite values:
*   **Performance:** Prevents expensive copies of entire array memory blocks when passing arrays in expressions or function calls.
*   **Uniform Addressing:** Unifies pointer arithmetic and array subscripting under a single mathematical abstraction: `a[i] == *(a + i)`.

## Mechanism and Language Rules
1.  **Decay Rule:** In almost all expressions, an array identifier evaluates to a pointer to its first element: `arr` -> `&arr[0]`.
2.  **The Three Canonical Exceptions (CRITICAL):**
    Array decay does **NOT** occur when the array is:
    *   The operand of the `sizeof` operator: `sizeof(arr)` yields the size of the entire array in bytes, not pointer size.
    *   The operand of the unary `&` (address-of) operator: `&arr` yields a pointer to the entire array (type `T (*)[N]`), not `T **`.
    *   The operand of the `_Alignof` / `alignof` operator: yields the alignment of the array's element type.
    *   (Also: when used to initialize a `char` array with a string literal).
3.  **Loss of Bounds:** Once decayed to `T *`, all compile-time dimension and extent information is permanently erased from the type system.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

static void example_decay(void)
{
    uint32_t arr[10];

    /* 1. Array decays to pointer to first element: type uint32_t * */
    uint32_t *p = arr;
    (void)p;

    /* 2. Exception: sizeof does NOT decay */
    size_t total_bytes = sizeof(arr); /* 40 bytes, NOT sizeof(uint32_t*) */
    (void)total_bytes;

    /* 3. Exception: & does NOT decay */
    /* &arr has type uint32_t (*)[10], NOT uint32_t ** */
    uint32_t (*ptr_to_array)[10] = &arr;
    (void)ptr_to_array;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Attempting to access elements past the original array bounds through a decayed pointer.
*   **Type Invariance:** The numerical address of `arr`, `&arr`, and `&arr[0]` is identical, but their C types and pointer arithmetic strides are completely different.

## Edge Cases and Failure Modes
*   **The `&arr` vs. `arr` Pointer Math Trap:**
    *   `arr + 1`: Advances by `1 * sizeof(ElementType)` (e.g., 4 bytes).
    *   `&arr + 1`: Advances by the size of the **entire array** (`10 * sizeof(ElementType)` = 40 bytes).
*   **Decay in Conditional Operators:** In `cond ? arr1 : arr2`, both arrays decay to pointers, losing their composite array type and sizing.

## Embedded Implications
*   **Peripheral Register Buffers:** When passing hardware buffers to drivers, decay happens instantly:
    ```c
    uint8_t tx_buf[128];
    hal_uart_send(tx_buf); /* tx_buf decays to uint8_t * */
    ```
    Because decay strips length, drivers must require explicit length arguments to avoid transmitting unallocated memory.
*   **Linker Script Array Bounds:** Arrays bounded by linker symbols require explicit address-of operations (`&_sdata`) because the symbols are not C array objects.

## Firmware Review Angle
1.  **Audit Boundary Loss:** Ensure every function receiving a decayed pointer is accompanied by an explicit length parameter.
2.  **Pointer Math on `&arr`:** Scrutinize any arithmetic performed on `&arr`; it scales by the full array size and is usually a bug.
3.  **Parenthesized Expressions:** Verify developers understand the difference between `sizeof(arr)` (total size) and `sizeof(&arr)` (pointer size).

## Compiler, ABI, and Toolchain Implications
*   **Zero-Instruction Conversion:** Array decay generates zero CPU instructions. It is purely a compile-time type-lowering operation.
*   **Register Passing:** The decayed pointer is placed directly in the architecture's argument register (e.g., `R0` on ARM).

## Performance, Memory, Timing, and Power
*   **Zero Memory Overhead:** Decay avoids copying memory blocks on the stack, preserving SRAM bandwidth and dynamic power.
*   **Cache Friendliness:** Operating on decayed pointers preserves spatial locality when traversed sequentially.

## Verification / Debugging
*   **Compiler Warnings:** Use `-Wsizeof-pointer-memaccess` to catch accidental calls like `memset(ptr, 0, sizeof(ptr))` after decay.
*   **GDB Inspection:**
    *   `ptype arr`: displays `uint32_t [10]`.
    *   `ptype +arr`: displays `uint32_t *` (unary `+` forces decay!).

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.1:* A pointer resulting from arithmetic shall address elements of the same array.
*   **Security Vulnerabilities:**
    *   CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer. Loss of array bounds via decay is the primary historical cause of buffer overflow exploits in C.

## Trade-offs and Alternatives
*   **Decayed Pointers vs. Array Spans:** Modern defensive C wraps decayed pointers and lengths into a span struct:
    ```c
    struct Span { const uint8_t *data; size_t len; };
    ```
    This eliminates bounds loss while retaining zero-copy efficiency.

## Staff-Level Takeaway
Array decay is the bridge between contiguous storage and pointer arithmetic. Staff engineers must enforce two rules across code reviews: always recognize the three decay exceptions (`sizeof`, `&`, `_Alignof`), and never pass a decayed array pointer across module boundaries without an explicit, validated length parameter.

## Related Concepts
*   [[01_Array_declaration]]
*   [[04_Array_parameter_adjustment]]
*   [[06_Pointer_to_array_types]]
*   [[10_sizeof_arrays]]
*   [[13_C_Pointers/07_Pointer_arithmetic]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
