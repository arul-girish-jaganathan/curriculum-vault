# 08: Returning Structures

## Definition
Returning a structure is the mechanism by which a function yields an entire aggregate struct value back to its caller. In ISO C (C99 §6.8.6.4), structures are first-class values in return expressions: the entire struct layout is copied from the callee's execution context into the caller's receiving object.

## Scope and Boundaries
*   **Covers:** Small struct returns in registers, large struct returns via hidden pointers (sret), ABI lowering rules, copy overhead, and copy elision.
*   **Does not cover:** Returning scalar values (see [[07_Returning_values]]), returning structure pointers (see [[06_Pointer_parameters]]), or struct packing and alignment (see [[Memory Alignment and Padding]]).

## Why Does It Exist
Real-world routines frequently compute composite results:
*   **Multi-Value Returns:** Returning complex results (e.g., `{int32_t value, bool valid}`) without messy out-pointer parameters.
*   **Clean Mathematical Abstractions:** Modeling composite mathematical concepts (e.g., `Point2D`, `ComplexNumber`, `Vector3D`) as direct, immutable expression values.
*   **Immutability:** Eliminates the pointer aliasing hazards associated with passing mutable destination pointers.

## Mechanism and Language Rules
1.  **Direct Value Semantics:** `struct T result = calculate();` copies the entire structure from the callee to the caller.
2.  **No Partial Copying:** The entire memory image of the struct is transferred, including internal alignment padding bytes.
3.  **ABI Lowering Mechanics:**
    *   *Small Structs (<= 8 or 16 bytes):* Packed into CPU registers (e.g., `R0-R1` on ARM, `RAX:RDX` on x86_64) and returned with zero memory overhead.
    *   *Large Structs (> 16 bytes):* The caller allocates space on its stack frame and passes a hidden pointer (often in `R0` or `RDI`) to the callee. The callee writes the return value directly into that space.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdbool.h>

struct Result {
    int32_t value;
    bool success;
};

/* Small struct: Fits in two 32-bit registers (8 bytes total) */
static struct Result parse_packet(const uint8_t *buf, size_t len)
{
    struct Result res;
    if (buf == NULL || len == 0) {
        res.value = 0;
        res.success = false;
        return res;
    }
    res.value = (int32_t)buf[0];
    res.success = true;
    return res;
}

static void example_caller(void)
{
    uint8_t raw = 0x55;
    struct Result r = parse_packet(&raw, 1);
    if (r.success) {
        /* Process r.value */
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Accessing uninitialized members of a returned struct.
*   **Unspecified Behavior:** The contents of padding bytes within the returned struct are unspecified and may contain uninitialized register/stack bits.
*   **Implementation-Defined Behavior:** The exact size threshold where an ABI switches from register returns to hidden pointer stack returns.

## Edge Cases and Failure Modes
*   **Padding Leak Security Hole:** If a returned struct contains internal padding bytes, returning it across a privilege boundary (e.g., kernel to user space) can leak sensitive uninitialized stack memory. The struct must be `memset` to zero before returning.
*   **Hidden Stack Bloat:** Returning large structs from chained functions causes multiple hidden stack allocations, rapidly blowing through limited microcontroller stack RAM.

## Embedded Implications
*   **AAPCS Struct Limits:** On ARM Cortex-M, structures up to 4 bytes fit in `R0`; structures up to 8 bytes fit in `R0-R1`. Structures larger than 16 bytes immediately trigger hidden pointer stack returns, incurring memory writes.
*   **Safe Functional Patterns:** Small result structures (like `struct { bool ok; uint32_t val; }`) are highly efficient, safe, and modern alternatives to error-code return patterns with out-pointers.

## Firmware Review Angle
1.  **Size Auditing:** Verify that returned structs do not exceed 8 or 16 bytes unless profiled and intended.
2.  **Padding Cleared:** For security-sensitive APIs, verify that structures are zeroed (`memset(&res, 0, sizeof(res))`) before population to prevent information leakage via padding bytes.
3.  **Avoid Chained Large Copies:** Prevent pipelines returning large structures through multiple layers of abstraction.

## Compiler, ABI, and Toolchain Implications
*   **Named Return Value Optimization (NRVO):** Modern C compilers optimize returns by constructing the object directly in the caller's allocated memory space, eliminating redundant intermediate copies.
*   **Hidden First Argument:** For large structs, the ABI transforms the function signature from `Struct f(void)` to `void f(Struct *__return_storage_ptr)`.

## Performance, Memory, Timing, and Power
*   **Register Efficiency:** Small structs are returned with zero instruction overhead beyond scalar returns.
*   **Memory Overhead for Large Structs:** Returning large structs requires `memcpy` operations, consuming CPU cycles and evicting cache lines.

## Verification / Debugging
*   **Compiler Disassembly:** Inspect the function epilogue to determine whether the struct was returned via registers (`MOV R0, ...; BX LR`) or via stack pointer dereference (`STR ..., [R0]`).
*   **Stack Analysis:** Use GCC `-fstack-usage` to detect hidden stack expansion caused by structure returns.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:** Fully compliant with MISRA rules. Returning structures by value is strongly preferred over passing raw mutable pointers because it enforces value semantics.
*   **Security Vulnerabilities:**
    *   CWE-200: Information Exposure (via uninitialized struct padding bytes).

## Trade-offs and Alternatives
*   **Struct Return vs. Output Pointer:**
    *   *Struct Return (Small):* Superior readability, no pointer validation needed, no aliasing issues, register-passed.
    *   *Out-Pointer (`void f(Struct *out)`):* Avoids large memory copies, but introduces pointer verification overhead and aliasing risks.

## Staff-Level Takeaway
Returning small structures (<= 8 or 16 bytes) is an architectural win: it provides modern, immutable multi-value return semantics with zero memory copy overhead under modern ABIs. For large aggregates, avoid structure returns to prevent hidden stack allocation and memory copy overhead on embedded targets.

## Related Concepts
*   [[04_Pass_by_value]]
*   [[07_Returning_values]]
*   [[11_Calling_conventions]]
*   [[Memory Alignment and Padding]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
