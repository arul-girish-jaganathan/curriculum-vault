# 05: Array Parameter Adjustment

## Definition
Array parameter adjustment is the formal language rule in ISO C where any function parameter declared with an array type is automatically adjusted (converted) at compile time by the compiler to a pointer to the array's element type. In ISO C (C99 §6.7.5.3p7), declaring a parameter as `T a[N]` or `T a[]` is strictly rewritten as `T *a`.

## Scope and Boundaries
*   **Covers:** Automatic array-to-pointer parameter adjustment, the loss of array size information (decay), static array bounds (`static [N]`), and type qualifier placement inside array brackets.
*   **Does not cover:** Multi-dimensional array pointers (see [[13_C_Pointers/11_Pointer_to_array]]), general pointer arithmetic (see [[13_C_Pointers/07_Pointer_arithmetic]]), or variable-length arrays (VLAs).

## Why Does It Exist
C arrays are not first-class objects in the language grammar:
*   **Avoid Expensive Stack Copies:** Arrays cannot be assigned or passed by value. Adjusting array parameters to pointers avoids implicitly copying hundreds or thousands of elements onto the call stack.
*   **C Legacy Compatibility:** Maintains syntactic parity with early C compiler designs where array names served purely as address anchors.

## Mechanism and Language Rules
1.  **Syntactic Equivalence:** The following parameter declarations are 100% identical in language semantics:
    *   `void foo(int arr[10]);`
    *   `void foo(int arr[]);`
    *   `void foo(int *arr);`
2.  **Size Discard:** The bound `10` in `int arr[10]` is completely ignored by the compiler for sizing. `sizeof(arr)` inside the function evaluates to `sizeof(int *)` (4 or 8 bytes), NOT `10 * sizeof(int)`.
3.  **C99 `static` Extent Guarantee:**
    *   `void foo(int arr[static 10]);`: Guarantees to the compiler that the argument supplied at the call site will point to the first element of an array containing **at least** 10 elements, non-null.
4.  **Qualifiers Inside Brackets:** Qualifiers placed inside brackets qualify the resulting pointer:
    *   `void foo(int arr[const]);` is identical to `void foo(int * const arr);`.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

/* Proof of parameter adjustment: sizeof evaluates to pointer size */
static size_t example_decay(uint32_t buffer[100])
{
    /* Returns sizeof(uint32_t*), NOT 400 bytes! */
    return sizeof(buffer);
}

/* Correct: C99 static guarantee assert minimal element count */
static uint32_t sum_quad(const uint32_t values[static 4])
{
    /* Compiler assumes values != NULL and contains >= 4 elements */
    return values[0] + values[1] + values[2] + values[3];
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Passing `NULL` or an array with fewer elements than specified to a parameter declared with `[static N]`. Dereferencing elements beyond the actual allocation bounds of the passed array.
*   **Constraint Violation:** Using `static` or type qualifiers inside the brackets of an array parameter outside of function prototypes.
*   **Compiler Warning:** Compilers emit warnings when `sizeof` is used on an adjusted array parameter (`-Wsizeof-array-argument`).

## Edge Cases and Failure Modes
*   **The `sizeof` Trap:** Writing `size_t len = sizeof(arr) / sizeof(arr[0]);` inside a function body calculates `sizeof(pointer) / sizeof(element)` (e.g., `4 / 4 = 1`), causing loops to exit prematurely or process only the first element.
*   **Misleading Bounds:** Writing `void process(int buf[32])` provides a false sense of security; callers can pass an array of 2 elements (`int small[2]; process(small);`) and it will compile without error.

## Embedded Implications
*   **DMA Buffer Passing:** When passing buffers to peripheral drivers (e.g., `spi_transmit(uint8_t buf[])`), the adjusted pointer is copied to DMA configuration registers. Because size is lost, an explicit `size_t length` parameter must always accompany the buffer pointer.
*   **Static Analysis Bounds:** Utilizing `[static N]` enables embedded static analysis tools to verify buffer lengths at compile-time without runtime overhead.

## Firmware Review Angle
1.  **Audit `sizeof` on Parameters:** Search codebases for `sizeof(param)` where `param` was declared as an array.
2.  **Mandate Length Parameters:** Reject functions accepting array parameters without an explicit length parameter, unless the array is terminated by a sentinel (e.g., null-terminated string) or guarded by `[static N]`.
3.  **Prefer Pointer Syntax:** Encourage `Type *buf` instead of `Type buf[]` to make the pointer nature explicit to maintainers.

## Compiler, ABI, and Toolchain Implications
*   **Code Generation:** The generated assembly is identical whether declared as `int *p` or `int p[100]`. Pointers are passed via standard argument registers (`R0`).
*   **Optimization with `static`:** Declaring `[static N]` informs the optimizer that the pointer is non-null, allowing it to eliminate null checks and vectorize loops safely.

## Performance, Memory, Timing, and Power
*   **Zero Stack Overhead:** Arrays never incur stack copy overhead when passed to functions because only the address is transferred.
*   **Register Efficiency:** Passing an array address consumes exactly one register.

## Verification / Debugging
*   **Compiler Flags:** Use `-Wsizeof-array-argument` to catch erroneous `sizeof` invocations on decayed array parameters.
*   **Static Analyzers:** Clang Static Analyzer checks `[static N]` bounds at call sites.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.5:* Array parameter declarations shall contain at most two levels of indirection.
    *   *Rule 8.2:* Function types shall be in prototype form.
*   **Security Vulnerabilities:**
    *   CWE-119: Memory Buffer Overflow. Assuming the parameter maintains array size checks invites buffer overrun vulnerabilities.

## Trade-offs and Alternatives
*   **Array Syntax vs. Pointer + Length:**
    *   `void f(int a[])`: Misleading; implies array bounds that do not exist.
    *   `void f(int *a, size_t len)`: Clear, idiomatic, explicitly binds lifetime and bounds.
    *   `void f(struct ArraySpan span)`: Safe encapsulation of pointer and size in a single structure.

## Staff-Level Takeaway
Array parameter adjustment is an illusion: C functions never receive arrays; they receive pointers. Staff engineers should discourage pseudo-array parameter syntax (`T a[]`) in favor of explicit pointer-and-length pairs (`T *a, size_t len`) or encapsulated span structs, reserving `T a[static N]` strictly for APIs where static analysis guarantees minimal buffer extent.

## Related Concepts
*   [[03_Parameter_passing]]
*   [[06_Pointer_parameters]]
*   [[13_C_Pointers/01_Pointer_declarations]]
*   [[13_C_Pointers/07_Pointer_arithmetic]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
