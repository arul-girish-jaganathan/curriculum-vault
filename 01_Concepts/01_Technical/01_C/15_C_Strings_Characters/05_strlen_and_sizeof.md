# 05: Strlen and Sizeof

## Definition
`sizeof` is a compile-time unary operator that evaluates the total memory allocation size of an object or type in bytes. `strlen` is a runtime standard library function (defined in `<string.h>`) that calculates the number of characters in a null-terminated string, excluding the terminating null character.

## Scope and Boundaries
*   **Covers:** Semantic distinctions, compile-time evaluation vs. runtime traversal, performance profiles, and interaction with decayed pointers.
*   **Does not cover:** General array sizeof rules (see [[14_C_Arrays_VLA/10_sizeof_arrays]]), pointer sizeof (see [[13_C_Pointers/01_Pointer_declarations]]), or custom bounded length routines (`strnlen`).

## Why Does It Exist
Software needs to differentiate between buffer capacity and content length:
*   **Capacity (`sizeof`):** How much memory is allocated and available for storage.
*   **Content Length (`strlen`):** How much valid character data is currently stored in that memory.
*   **Algorithmic Correctness:** Confusing capacity with content length leads to buffer overflows or premature string truncation.

## Mechanism and Language Rules
1.  **`sizeof` Operator:**
    *   Evaluated entirely at compile time (except for VLAs).
    *   Returns total allocated storage in bytes (`size_t`).
    *   When applied to a string literal `"abc"`, `sizeof("abc") == 4` (includes `\0`).
    *   When applied to an array `char a[10] = "abc"`, `sizeof(a) == 10`.
    *   When applied to a decayed pointer `char *p`, `sizeof(p) == sizeof(char *)` (4 or 8 bytes).
2.  **`strlen` Function:**
    *   Evaluated at runtime via sequential memory traversal.
    *   Returns the number of characters preceding the first `'\0'`.
    *   `strlen("abc") == 3` (excludes `\0`).
3.  **Return Type:** Both yield results of type `size_t`.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <string.h>
#include <stddef.h>

static void example_diff(void)
{
    char buffer[32] = "System";

    size_t allocated_capacity = sizeof(buffer); /* 32 bytes (compile-time) */
    size_t payload_length    = strlen(buffer); /* 6 bytes  (runtime) */

    (void)allocated_capacity;
    (void)payload_length;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Passing an uninitialized or non-null-terminated character array to `strlen`.
*   **Compile-Time Optimization:** Modern compilers replace `strlen("constant_literal")` with a constant integer at compile time, provided no side effects exist.

## Edge Cases and Failure Modes
*   **The Decayed Buffer Sizing Bug:**
    ```c
    void process(const char buffer[64]) {
        size_t cap = sizeof(buffer); /* BUG: cap is 4 or 8 (pointer size), NOT 64! */
    }
    ```
*   **Off-By-One Allocation:** Sizing dynamic memory using `malloc(strlen(s))` instead of `malloc(strlen(s) + 1)`, omitting space for the null terminator.
*   **Calling `strlen` in Loop Conditions:**
    ```c
    for (size_t i = 0; i < strlen(str); ++i) { ... } /* $O(N^2)$ algorithmic complexity! */
    ```

## Embedded Implications
*   **Watchdog / Latency Traps:** Calling `strlen` on large buffers inside a tight polling loop re-traverses memory on every iteration ($O(N^2)$), causing execution starvation and triggering watchdog resets.
*   **Bounded String Length (`strnlen`):** Embedded firmware should always prefer `strnlen(str, MAX_LEN)` over unbounded `strlen` to guarantee bounded execution time and prevent out-of-bounds reads on corrupted buffers.

## Firmware Review Angle
1.  **Check `strlen` Loop Conditions:** Hoist `strlen` calls outside of loop conditions into an immutable local variable.
2.  **Audit Memory Allocations:** Ensure any buffer allocation based on `strlen` explicitly adds `+ 1` for the null terminator.
3.  **Verify `sizeof` on Function Parameters:** Reject code using `sizeof(param)` where `param` is a decayed character array.

## Compiler, ABI, and Toolchain Implications
*   **Intrinsic Inlining:** Compilers replace `strlen` with target-specific SIMD instructions (e.g., ARM NEON `VLD`/`VCEQ`) or unrolled word-at-a-time null-byte check algorithms.
*   **Zero Cost for `sizeof`:** `sizeof` generates zero machine instructions; it is an immediate constant in the assembly output.

## Performance, Memory, Timing, and Power
*   **Execution Latency:** `sizeof` takes 0 cycles. `strlen` takes $O(N)$ cycles, loading memory lines and consuming bus energy.
*   **Power Consumption:** Frequent unbounded memory scans increase memory bus activity, raising dynamic power draw on low-power battery systems.

## Verification / Debugging
*   **Compiler Warnings:** Use `-Wsizeof-array-argument -Wstringop-overread`.
*   **Static Analysis:** Analyzers flag redundant `strlen` evaluations within loop bodies.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 21.17:* String functions shall not result in buffer overflow or unhandled non-terminated arrays.
*   **Security Vulnerabilities:**
    *   CWE-131: Incorrect Calculation of Buffer Size (forgetting `+ 1`).
    *   CWE-400: Uncontrolled Resource Consumption (quadratic `strlen` loops).

## Trade-offs and Alternatives
*   **`strlen` vs. `strnlen`:** Always use `strnlen(s, maxlen)` in embedded systems to enforce a hard upper bound on memory traversal.
*   **String Objects / Spans:** Storing the length alongside the pointer eliminates `strlen` calls entirely, converting $O(N)$ traversals into $O(1)$ scalar reads.

## Staff-Level Takeaway
`sizeof` measures container capacity at compile time; `strlen` measures payload content at runtime. Staff engineers must mandate `strnlen` over unbounded `strlen`, ensure `+ 1` allocation rules are universally followed, and hoist string length evaluations out of loop predicates to prevent accidental $O(N^2)$ algorithmic disasters.

## Related Concepts
*   [[03_String_literals]]
*   [[04_Null_termination]]
*   [[11_Buffer_sizing]]
*   [[14_C_Arrays_VLA/10_sizeof_arrays]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
