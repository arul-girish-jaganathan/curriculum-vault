# 09: Variable Length Arrays

## Definition
A Variable Length Array (VLA) is an array whose extent (dimension) is evaluated at runtime based on the value of a non-constant integer expression. Introduced as mandatory in ISO C (C99 §6.7.5.2), VLAs were made **optional** in ISO C11 (via the macro `__STDC_NO_VLA__`) and are heavily restricted or banned in production and embedded systems.

## Scope and Boundaries
*   **Covers:** VLA syntax, automatic stack allocation semantics, variably modified types, `sizeof` runtime evaluation, and compiler deprecation.
*   **Does not cover:** Flexible array members (see [[08_Flexible_array_members]]), fixed-size arrays (see [[01_Array_declaration]]), or dynamic heap allocation (`malloc`).

## Why Does It Exist
C99 introduced VLAs to bridge the gap with scientific languages (like Fortran):
*   **Dynamic Matrix Computation:** Permitting numerical algorithms to allocate local matrices matching runtime dataset dimensions without calling `malloc`.
*   **Convenience:** Syntactic simplicity of stack-allocated temporary arrays with runtime sizing.

## Mechanism and Language Rules
1.  **Storage Scope:** VLAs can **only** have automatic storage duration (block scope). Declaring a VLA at file scope (static or global) is a constraint violation.
2.  **No Initializers:** A VLA cannot have an initializer list (`int a[n] = {0};` is a compile-time constraint violation).
3.  **Runtime `sizeof`:** Unlike standard arrays, applying `sizeof` to a VLA evaluates at **runtime**, executing code to compute `n * sizeof(ElementType)`.
4.  **Variably Modified Types:** Types derived from VLAs (such as pointers to VLAs: `int (*p)[n]`) are called variably modified (VM) types and are retained in C11 even if full VLA stack allocations are unsupported.
5.  **Optional Status (C11):** If the implementation defines `__STDC_NO_VLA__ == 1`, the compiler does not support variable-length stack arrays.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

#if !defined(__STDC_NO_VLA__)
static uint32_t example_vla(size_t count)
{
    /* DANGEROUS: Allocates runtime-sized buffer on the stack */
    uint32_t vla_buffer[count];

    /* Runtime evaluation of sizeof */
    size_t byte_size = sizeof(vla_buffer);

    for (size_t i = 0; i < count; ++i) {
        vla_buffer[i] = (uint32_t)i;
    }

    return vla_buffer[0] + (uint32_t)byte_size;
}
#endif
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Passing a non-positive integer (zero or negative) as the size of a VLA. Supplying a size that exceeds available stack memory (causes an immediate, untrappable stack overflow).
*   **Constraint Violation:** Declaring a VLA with `static` or `extern` storage class. Initializing a VLA at its point of declaration.
*   **Implementation-Defined / Optional:** Whether full VLA support is implemented under C11/C17/C23.

## Edge Cases and Failure Modes
*   **Untrappable Stack Exhaustion:** If an untrusted caller supplies `count = 1000000`, the stack pointer (`SP`) is decremented past the physical RAM boundary. Unlike `malloc()`, which returns `NULL` on failure, a VLA provides **no failure reporting mechanism**; it silently crashes the CPU via a HardFault or memory corruption.
*   **Side Effects in `sizeof`:** Because `sizeof(vla)` is evaluated at runtime, any expressions with side effects inside the `sizeof` operator (e.g., `sizeof(int[n++])`) are executed at runtime, breaking the compile-time identity of `sizeof`.

## Embedded Implications
*   **Strictly Banned in Firmware:** In embedded systems, stack sizes are statically fixed (e.g., 512 bytes to 4 KB). Using a VLA inside a deeply nested call chain or ISR is a catastrophic design flaw that guarantees random system reboots.
*   **Static Stack Analysis Invalidation:** Tools that calculate Maximum Stack Depth (like GCC `-fstack-usage`) cannot compute fixed upper bounds when VLAs are present, invalidating functional safety certifications.

## Firmware Review Angle
1.  **Zero-Tolerance Enforcement:** Compile with `-Wvla -Werror=vla` to automatically fail builds containing any VLA declarations.
2.  **Audit Function Signatures:** Check for hidden variably modified parameter types.
3.  **Replace with Bounded Static Storage:** Replace VLAs with fixed-capacity arrays sized to worst-case specifications with runtime boundary checks.

## Compiler, ABI, and Toolchain Implications
*   **Dynamic Stack Allocation (`alloca` lowering):** Compilers lower VLAs by emitting instructions that dynamically adjust the stack pointer (`SUB SP, SP, R0`), requiring a dedicated Frame Pointer (`R7` or `R11`) to restore the stack on function return.
*   **Frame Pointer Register Eviction:** Forcing a frame pointer consumes a general-purpose register that would otherwise be available for compiler optimizations.

## Performance, Memory, Timing, and Power
*   **Non-Deterministic Execution:** Dynamic stack frame adjustments take variable CPU cycles, degrading real-time determinism.
*   **Stack Fragmentation:** Interleaving VLAs with block-scoped automatic variables prevents compilers from overlapping stack reuse slots.

## Verification / Debugging
*   **Compiler Flags:** Enforce `-Werror=vla`.
*   **Static Analyzers:** Static analysis suites (Polyspace, Coverity) immediately flag VLAs as critical safety violations.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.8:* Variable-length arrays shall not be used.
*   **Linux Kernel Ban:** The Linux kernel completely eliminated all VLAs from the entire codebase due to security vulnerabilities and stack-overflow risks.
*   **Security Vulnerabilities:**
    *   CWE-400: Uncontrolled Resource Consumption.
    *   CWE-770: Allocation of Resources Without Limits or Throttling.

## Trade-offs and Alternatives
*   **VLA vs. Bounded Fixed Buffer vs. Heap:**
    *   *VLA:* Unsafe, untrappable failure, non-standard optional C11 feature.
    *   *Fixed-Size Array (`buffer[MAX_N]`):* Deterministic, statically analyzable stack depth, 100% safe when paired with an assertion: `assert(n <= MAX_N);`.
    *   *Heap (`malloc`):* Returns `NULL` on failure, but introduces dynamic fragmentation.

## Staff-Level Takeaway
VLAs are a failed experiment in ISO C that have been repudiated by modern systems engineering. They provide no error handling, destroy static stack analysis, and invite catastrophic stack overflow exploits. Staff engineers must ban VLAs project-wide via `-Werror=vla` and enforce bounded, compile-time buffer allocations.

## Related Concepts
*   [[01_Array_declaration]]
*   [[08_Flexible_array_members]]
*   [[10_sizeof_arrays]]
*   [[Stack Frame Architecture and ABI]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
