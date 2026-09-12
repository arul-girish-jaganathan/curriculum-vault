# 10: Sizeof Arrays

## Definition
The `sizeof` operator applied to an array object yields the total size of the array in bytes. In ISO C (C99 §6.5.3.4), an array object is one of the strictly defined exceptions to array decay: when an array identifier is the operand of `sizeof`, it does **not** decay into a pointer, evaluating instead to the total memory footprint: `N * sizeof(ElementType)`.

## Scope and Boundaries
*   **Covers:** Byte size calculations, element count idioms, multidimensional size evaluation, decay pitfalls, and compile-time constant evaluation.
*   **Does not cover:** Runtime `sizeof` evaluation on VLAs (see [[09_Variable_length_arrays]]), flexible array member sizing (see [[08_Flexible_array_members]]), or pointer sizing (see [[13_C_Pointers/01_Pointer_declarations]]).

## Why Does It Exist
Safe memory manipulation requires querying physical extent:
*   **Compile-Time Element Counting:** Safely deriving array length without hardcoding magic numbers.
*   **Buffer Operations:** Supplying accurate byte lengths to memory functions (`memset`, `memcpy`, DMA configurations).
*   **Automatic Scaling:** Ensuring that if an array's type is changed (e.g., from `uint16_t` to `uint32_t`), all buffer operations scale automatically.

## Mechanism and Language Rules
1.  **Byte Size Calculation:** For a declared array `T arr[N]`, `sizeof(arr)` evaluates to `N * sizeof(T)`.
2.  **Canonical Element Count Idiom:**
    ```c
    #define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))
    ```
    This expression evaluates at compile time to an integer constant expression of type `size_t`.
3.  **Compile-Time Invariance:** Except for VLAs, `sizeof` expressions are evaluated entirely by the compiler front-end; they produce zero runtime CPU instructions.
4.  **Multidimensional Total Size:** For `T m[R][C]`, `sizeof(m)` evaluates to `R * C * sizeof(T)`. `sizeof(m[0])` yields the byte size of a single row (`C * sizeof(T)`).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))

static const uint32_t g_coefficients[8] = { 1, 2, 3, 4, 5, 6, 7, 8 };

static size_t example_sizeof(void)
{
    /* 1. Total byte size: 8 * 4 = 32 bytes */
    size_t total_bytes = sizeof(g_coefficients);

    /* 2. Number of elements: 32 / 4 = 8 */
    size_t count = ARRAY_SIZE(g_coefficients);

    return total_bytes + count;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Compile-Time Guarantee:** Guaranteed by ISO C to evaluate to a constant of type `size_t`.
*   **Compiler Extension (Type Checking):** Modern toolchains provide type-safe array count macros (e.g., Linux kernel `ARRAY_SIZE`) that intentionally cause a division-by-zero compile error if applied to a raw pointer.

## Edge Cases and Failure Modes
*   **The Decayed Pointer Trap:** The single most common bug with `sizeof`:
    ```c
    void process(uint32_t arr[32]) {
        size_t bytes = sizeof(arr); /* BUG: Evaluates to sizeof(uint32_t*), 4 or 8 bytes! */
    }
    ```
*   **Double Evaluation Safety:** In `#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))`, the operand `a` is evaluated within `sizeof` unevaluated contexts, so expressions like `ARRAY_SIZE(arr)` do not generate side-effect hazards.

## Embedded Implications
*   **DMA Transfer Configuration:** DMA registers require transfer lengths in bytes or words. Using `sizeof(dma_buf)` ensures the transfer length exactly matches the memory block without manual synchronization bugs.
*   **Zeroing Hardware Buffers:** Clearing communication buffers via `memset(buf, 0, sizeof(buf))` is safe **only** while `buf` remains an undayed array in the local scope.

## Firmware Review Angle
1.  **Audit `sizeof` on Pointers:** Use static analysis tools to verify `sizeof` is never called on an adjusted array parameter inside a function body.
2.  **Type-Safe Macro Enforcement:** Replace bare `sizeof(a)/sizeof(a[0])` with a type-safe macro that rejects pointers:
    ```c
    #define ARRAY_SIZE(a)         ((sizeof(a) / sizeof((a)[0])) /         (size_t)(!(sizeof(a) == sizeof(void *))))
    ```
3.  **Buffer Sizing Invariants:** Ensure `memset` and `memcpy` calls reference the target array object using `sizeof(dest_array)` rather than hardcoded sizes.

## Compiler, ABI, and Toolchain Implications
*   **Zero Cycle Overhead:** `sizeof(array)` is completely resolved during translation; it is an immediate constant operand in generated assembly.
*   **Dead Code Elimination:** Comparisons like `if (ARRAY_SIZE(arr) > 10)` are evaluated at compile time, allowing optimizers to eliminate dead branches entirely.

## Performance, Memory, Timing, and Power
*   **Zero ROM/RAM Overhead:** Generates no machine instructions or runtime look-up tables.
*   **Optimal Determinism:** Eliminates dynamic loop-bound queries or pointer arithmetic checks.

## Verification / Debugging
*   **Compiler Flags:** Use `-Wsizeof-pointer-div` and `-Wsizeof-array-argument` to catch pointer/array sizing errors.
*   **Compile-Time Assertions:** Validate array extents using static assertions:
    ```c
    _Static_assert(ARRAY_SIZE(g_coefficients) == 8, "Coefficient count mismatch");
    ```

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Directive 4.6:* Typedefs that indicate size and signedness should be used.
*   **Security Vulnerabilities:** Under-allocating buffers due to `sizeof(pointer)` errors results in classic heap and stack buffer overflow exploits.

## Trade-offs and Alternatives
*   **`sizeof` vs. Explicit Length Constants:**
    *   *`sizeof(arr)` / `ARRAY_SIZE(arr)`:* Automatically synchronizes with array declaration modifications; single source of truth.
    *   *Explicit Constant (`#define CAP 8`):* Required when dimension must be shared across external interfaces without exposing array definitions.

## Staff-Level Takeaway
`sizeof` is the only mechanism that preserves total array footprint before decay occurs. Staff engineers must enforce compile-time `_Static_assert` validations against array footprints, ban `sizeof` on decayed function parameters via compiler warning flags, and implement type-safe `ARRAY_SIZE` macros project-wide.

## Related Concepts
*   [[01_Array_declaration]]
*   [[03_Array_to_pointer_decay]]
*   [[04_Array_parameter_adjustment]]
*   [[11_Array_bounds_and_safety]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
