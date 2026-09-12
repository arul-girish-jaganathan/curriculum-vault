# 04: Array Parameter Adjustment

## Definition
Array parameter adjustment is the formal transformation rule in ISO C (C99 §6.7.5.3p7) wherein any function parameter declared with an array type is automatically converted by the compiler into a pointer to the array's element type. In ISO C, `T a[N]`, `T a[]`, and `T *a` declare identical parameter types.

## Scope and Boundaries
*   **Covers:** Parameter rewriting rules, loss of array type inside functions, the C99 `static` array parameter extent guarantee, and `[const]` pointer qualification inside brackets.
*   **Does not cover:** General array decay in expressions (see [[03_Array_to_pointer_decay]]), multidimensional row adjustments (see [[05_Multidimensional_arrays]]), or calling conventions (see [[12_C_Functions/11_Calling_conventions]]).

## Why Does It Exist
Array parameter adjustment exists to prevent accidental pass-by-value of whole memory blocks:
*   **Language Consistency:** C prohibits arrays from being passed by value. Adjusting parameter declarations at the grammar level guarantees that function calls only pass 4-byte or 8-byte pointer addresses.
*   **Syntactic Flexibility:** Allows programmers to document intended buffer sizes in function signatures even though the compiler treats them as pointers.

## Mechanism and Language Rules
1.  **Syntactic Equivalence:**
    *   `void func(uint32_t buf[64]);` -> rewritten as -> `void func(uint32_t *buf);`
    *   `void func(uint32_t buf[]);`   -> rewritten as -> `void func(uint32_t *buf);`
2.  **Ignored Extent:** The integer constant `64` in `buf[64]` is completely discarded by the compiler. Calling `func(small_buf)` where `small_buf` has 2 elements compiles without errors.
3.  **`sizeof` Invalidation:** Inside the function body, `sizeof(buf)` evaluates to `sizeof(uint32_t *)` (4 or 8 bytes), NOT `64 * sizeof(uint32_t)`.
4.  **C99 `static` Extent Specifier:**
    *   `void func(uint32_t buf[static 16]);`: Guarantees to the compiler that the argument supplied will point to a valid, non-null buffer containing **at least** 16 elements.
5.  **Qualifiers inside Brackets:**
    *   `void func(int a[const 10]);` -> rewritten as -> `void func(int * const a);`.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

/* Proof of adjustment: sizeof evaluates to pointer size */
static size_t verify_adjustment(const uint32_t buffer[128])
{
    /* Evaluates to sizeof(uint32_t*), NOT 512 bytes */
    return sizeof(buffer);
}

/* Correct: C99 static guarantee */
static uint32_t process_quad(const uint32_t data[static 4])
{
    /* Guaranteed data != NULL and data has >= 4 elements */
    return data[0] + data[1] + data[2] + data[3];
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Passing `NULL` or a buffer with fewer than `N` elements to a parameter declared with `[static N]`. Dereferencing elements past the actual buffer allocation length.
*   **Compiler Warning:** Modern compilers emit `-Wsizeof-array-argument` when `sizeof` is invoked on an adjusted array parameter.

## Edge Cases and Failure Modes
*   **The Array Size Calculation Bug:**
    ```c
    void process(uint8_t packet[256]) {
        size_t n = sizeof(packet) / sizeof(packet[0]); /* Bug: n = 4 or 8, NOT 256! */
    }
    ```
*   **False Sense of Security:** Believing `void write_channel(int ch[4])` enforces that only 4-element arrays can be passed. Any pointer of type `int *` will be accepted silently.

## Embedded Implications
*   **Peripheral Driver Interfaces:** Firmware APIs that accept buffers must pair the adjusted pointer with an explicit byte/element count:
    ```c
    void i2c_master_transmit(uint8_t *tx_buf, size_t len);
    ```
*   **Static Analysis Enforcement:** Using `[static N]` enables embedded static analyzers (e.g., Coverity, PC-lint) to detect buffer overruns at call sites without runtime checks.

## Firmware Review Angle
1.  **Reject `sizeof` on Parameters:** Flag any occurrence of `sizeof(param)` where `param` is a function argument.
2.  **Mandate Length Arguments:** Reject array parameter declarations that omit an explicit length parameter unless `[static N]` is used.
3.  **Prefer Explicit Pointer Syntax:** Mandate `T *buf` instead of `T buf[]` in function prototypes to eliminate false assumptions of array bounds retention.

## Compiler, ABI, and Toolchain Implications
*   **ABI Register Allocation:** Adjusted parameters are passed in standard argument registers (e.g., `R0` on ARM AAPCS).
*   **Optimizer Assumptions with `static`:** The compiler assumes `[static N]` pointers are never `NULL`, optimizing away downstream null checks (`if (buf == NULL)` is eliminated).

## Performance, Memory, Timing, and Power
*   **Zero Memory Overhead:** Passing adjusted array pointers consumes zero stack memory for buffer contents.
*   **Pipeline Efficiency:** Passing addresses directly in registers avoids caller-side stack store cycles.

## Verification / Debugging
*   **Compiler Flags:** Enforce `-Wsizeof-array-argument -Warray-bounds`.
*   **Static Analysis:** Use Clang Static Analyzer to verify call site buffer bounds against `[static N]` declarations.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.5:* The declaration of an array parameter shall not contain more than two levels of indirection.
*   **Security Vulnerabilities:** CWE-120: Buffer Copy without Checking Size of Input. Assuming the function parameter enforces array size creates exploitable buffer overruns.

## Trade-offs and Alternatives
*   **Raw Pointer vs. Array Syntax vs. Span Struct:**
    *   `T a[]`: Misleading syntax.
    *   `T *a, size_t n`: Clear, idiomatic C.
    *   `struct T_Span`: Encapsulated pointer and length; highest safety.

## Staff-Level Takeaway
Array parameter syntax is syntactic sugar that conceals a raw pointer. Staff engineers should ban pseudo-array parameter syntax (`T a[]`) in favor of explicit pointer-and-length pairs (`T *a, size_t len`), reserving `T a[static N]` strictly for specialized interfaces where call sites are validated via static analysis.

## Related Concepts
*   [[01_Array_declaration]]
*   [[03_Array_to_pointer_decay]]
*   [[12_C_Functions/03_Parameter_passing]]
*   [[12_C_Functions/05_Array_parameter_adjustment]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
