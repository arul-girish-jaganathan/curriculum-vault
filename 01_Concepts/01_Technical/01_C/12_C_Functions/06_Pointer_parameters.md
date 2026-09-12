# 06: Pointer Parameters

## Definition
A pointer parameter is a formal parameter of a pointer type (`T *`) that receives the memory address of an object. In ISO C (C99 §6.7.5.1), pointer parameters enable indirect object mutation across function boundaries (emulating pass-by-reference) and provide zero-copy access to large data aggregates.

## Scope and Boundaries
*   **Covers:** Pass-by-reference emulation, in/out/inout parameter patterns, const qualification of pointed-to data, pointer aliasing, and the `restrict` qualifier.
*   **Does not cover:** Pointer to pointer parameters (see [[13_C_Pointers/10_Pointer_to_pointer]]), array parameter decay (see [[05_Array_parameter_adjustment]]), or null pointer validation (see [[13_C_Pointers/04_Null_pointers]]).

## Why Does It Exist
Because C is strictly pass-by-value:
*   **Callee Mutation (Out Parameters):** Returning multiple computed values or updating caller data structures in place.
*   **Zero-Copy Aggregate Access:** Passing pointers to large structs avoids copying data on the stack.
*   **Hardware Interface Binding:** Passing addresses of memory-mapped registers or DMA buffers directly to drivers.

## Mechanism and Language Rules
1.  **Address Copying:** The pointer variable itself is passed by value (copied into the callee's register or frame).
2.  **Indirection:** Modifying `*param` mutates the memory object owned by the caller. Modifying `param` itself only mutates the callee's local address copy.
3.  **Const Correctness:**
    *   `const T *param`: Read-only input buffer. Callee cannot modify the caller's data through this pointer.
    *   `T * const param`: Callee cannot redirect the pointer variable to point elsewhere, though `*param` is mutable.
    *   `const T * const param`: Completely immutable pointer and pointee.
4.  **The `restrict` Qualifier (C99):** `T * restrict param` asserts that for the lifetime of the function, the pointed-to object will be accessed solely through that pointer, unlocking vectorization and aggressive register caching.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdbool.h>

/* Correct: Read-only input buffer + Out-parameter */
static bool parse_record(const uint8_t *input_bytes, size_t len, uint32_t *out_val)
{
    if (input_bytes == NULL || out_val == NULL || len < 4) {
        return false;
    }
    *out_val = ((uint32_t)input_bytes[0] << 24) |
               ((uint32_t)input_bytes[1] << 16) |
               ((uint32_t)input_bytes[2] << 8)  |
               ((uint32_t)input_bytes[3]);
    return true;
}

/* Correct: Vector math with restrict asserting no aliasing */
static void vector_add(float * restrict dst, const float * restrict src, size_t n)
{
    for (size_t i = 0; i < n; ++i) {
        dst[i] += src[i];
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Dereferencing a pointer parameter that is `NULL`, uninitialized, dangling, or unaligned. Violating the `restrict` contract by accessing memory through another aliasing pointer within the same function scope.
*   **Constraint Violation:** Passing a `const T *` argument into a parameter declared as `T *` without an explicit cast.
*   **Implementation-Defined:** Calling conventions for pointer passing across system boundaries.

## Edge Cases and Failure Modes
*   **Lifetime Mismatch (Stack Pointer Leak):** Returning a pointer to an automatic variable or storing a pointer parameter to local caller stack memory into a global variable creates a catastrophic use-after-free vulnerability.
*   **Hidden Pointer Aliasing:** If a caller passes the same buffer as both source and destination (`vector_add(buf, buf, 10)`), but the parameters are marked `restrict`, the compiler's reordered vectorized instructions will produce data corruption.
*   **Silent Const Stripping:** Explicitly casting `(Type *)` on a `const Type *` parameter allows writes to `.rodata` Flash, triggering hardware HardFaults.

## Embedded Implications
*   **Zero-Copy Drivers:** Embedded communication stacks (Ethernet, CAN, USB) pass packet descriptors via pointer parameters to achieve zero-copy packet throughput.
*   **Hardware Alignment:** Microcontrollers lacking unaligned access support (e.g., Cortex-M0) will crash with a UsageFault if an unaligned pointer parameter is cast to a wider integer type and dereferenced.
*   **Atomic Modifications:** Mutating shared RAM through pointer parameters inside ISRs requires atomic operations or critical section guards to prevent data tearing.

## Firmware Review Angle
1.  **Mandate `const`:** Ensure all pointer parameters used exclusively for reading data are declared `const Type *`.
2.  **Null Checks:** Verify whether public API pointer parameters are guarded against `NULL` prior to dereferencing.
3.  **Audit `restrict`:** Verify that functions using `restrict` parameters cannot be called with overlapping memory blocks.

## Compiler, ABI, and Toolchain Implications
*   **Strict Aliasing Analysis:** The compiler assumes pointers of incompatible types do not point to the same memory location, allowing aggressive reordering of loads and stores.
*   **Register Passing:** Pointer parameters are passed in general-purpose registers (`R0-R3` on ARM).

## Performance, Memory, Timing, and Power
*   **Cycle Efficiency:** Passing a 4-byte or 8-byte pointer takes 1 cycle, avoiding multi-cycle struct copies.
*   **Cache Penalty:** Pointer dereferences incur latency if the pointed-to memory is not in CPU L1/SRAM cache.

## Verification / Debugging
*   **Compiler Flags:** Use `-Wcast-qual -Wnonnull -Wnull-dereference`.
*   **Sanitizers:** Compile unit tests with AddressSanitizer (`-fsanitize=address`) and UndefinedBehaviorSanitizer (`-fsanitize=undefined`).

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 8.13:* A pointer parameter pointing to an object should be declared pointing to `const` if the object is not modified.
*   **Security Hazards:**
    *   CWE-476: NULL Pointer Dereference.
    *   CWE-416: Use After Free.

## Trade-offs and Alternatives
*   **Pointer Parameters vs. Return Value:** Returning small data structures (<= 8 bytes) by value in registers is often faster than passing pointer out-parameters because it eliminates memory writes and aliasing barriers.

## Staff-Level Takeaway
Pointer parameters are the gateway for both high-performance zero-copy APIs and memory corruption exploits. Staff engineers must enforce const-correctness on every input pointer, validate pointer lifetimes across asynchronous boundaries, and carefully evaluate whether returning small structs by value provides cleaner, safer semantics than out-pointer parameters.

## Related Concepts
*   [[03_Parameter_passing]]
*   [[04_Pass_by_value]]
*   [[07_Returning_values]]
*   [[13_C_Pointers/01_Pointer_declarations]]
*   [[13_C_Pointers/06_const_pointer_combinations]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
