# 12: Function API Contracts

## Definition
A function API contract is the complete architectural specification of preconditions, postconditions, invariants, error behaviors, re-entrancy guarantees, and lifetime expectations governing the caller-callee relationship. While ISO C enforces basic type-signature contracts, defensive API engineering formalizes semantic invariants through defensive checks, assertions, qualifiers, and modern attribute annotations.

## Scope and Boundaries
*   **Covers:** Preconditions and postconditions, design-by-contract, assertions (`assert`), defensive parameter validation, thread safety/re-entrancy, ownership transfers, and C23 attribute contracts.
*   **Does not cover:** Abstract interface definitions (see [[02_Function_declaration]]), error code definitions in isolation, or RTOS synchronization primitives.

## Why Does It Exist
Type systems in C are intentionally weak:
*   **Boundary Enforcement:** A type system can enforce that a parameter is an `int *`, but cannot verify that it is non-null, points to at least 16 elements, or represents valid memory.
*   **Defensive Robustness:** Preventing undefined behavior, buffer overflows, and race conditions before invalid inputs propagate into system internals.
*   **Self-Documenting Code:** Explicit contracts reduce ambiguity during integration between different engineering teams.

## Mechanism and Language Rules
1.  **Preconditions:** Obligations the caller must satisfy before calling the function (e.g., `ptr != NULL`, `len > 0`).
2.  **Postconditions:** Guarantees the function delivers upon return, provided preconditions were met (e.g., `return >= 0`, out-buffer fully written).
3.  **Invariants:** System states that remain true before and after execution (e.g., interrupt state restored, mutex unlocked).
4.  **Static Contracts (C Attributes):**
    *   `__attribute__((nonnull))`: Warns if null constants are passed.
    *   `__attribute__((warn_unused_result))` (C23 `[[nodiscard]]`): Mandates callers check return status codes.
    *   `[static N]` array syntax: Requires callers pass an array with at least `N` elements.
5.  **Dynamic Contracts:** Runtime validation utilizing defensive branching (`if (!valid) return ERR;`) and assertions (`assert(invariant)`).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <assert.h>

typedef enum {
    STATUS_OK = 0,
    STATUS_ERR_INVALID_PARAM,
    STATUS_ERR_BUFFER_OVERFLOW
} status_t;

/* Formal Contract:
 * Preconditions: buf != NULL, out_len != NULL, max_len > 0
 * Postconditions: On STATUS_OK, *out_len <= max_len
 * Caller must check return value: [[nodiscard]]
 */
#if __STDC_VERSION__ >= 202311L
[[nodiscard]]
#elif defined(__GNUC__)
__attribute__((warn_unused_result))
#endif
static status_t fill_telemetry(uint8_t *buf, size_t max_len, size_t *out_len)
{
    /* 1. Precondition validation */
    if (buf == NULL || out_len == NULL || max_len < 4) {
        return STATUS_ERR_INVALID_PARAM;
    }

    /* 2. Operational work */
    buf[0] = 0xAA;
    buf[1] = 0xBB;
    buf[2] = 0xCC;
    buf[3] = 0xDD;
    *out_len = 4;

    /* 3. Postcondition invariant assertion */
    assert(*out_len <= max_len);

    return STATUS_OK;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Violating API contracts where the implementation assumes valid state (e.g., passing invalid handles or dangling buffers).
*   **Compiler Optimization Traps:** If an API uses `__attribute__((nonnull(1)))`, the compiler's optimizer assumes the pointer parameter is never null, and may optimize out defensive runtime checks (`if (ptr == NULL)`) inside the function!

## Edge Cases and Failure Modes
*   **Defensive Check Erasure:** Using non-null attributes alongside defensive runtime null checks can backfire: optimizers running with `-fdelete-null-pointer-checks` will eliminate the runtime checks.
*   **Contract Incompleteness:** Failing to document who owns dynamically allocated memory (caller vs. callee) leads to memory leaks or double-free bugs.
*   **Assertion Misuse in Production:** Placing code with side effects inside `assert()` (e.g., `assert(write_reg() == OK);`). When `NDEBUG` is defined for release builds, the entire statement is stripped, breaking system functionality.

## Embedded Implications
*   **Re-entrancy and Thread Safety:** Embedded functions callable from both thread mode and interrupt handlers (ISRs) must explicitly declare re-entrancy contracts:
    *   No unshielded static local variables.
    *   Critical sections or atomic locks around shared hardware peripherals.
*   **Fail-Safe Error Strategies:** In mission-critical firmware, contract violations must transition the system into a deterministic safe state (e.g., disabling PWM motor drivers) rather than silently returning error codes.

## Firmware Review Angle
1.  **Enforce `nodiscard`:** Ensure every function returning an error code or status enum is marked with `[[nodiscard]]` or `__attribute__((warn_unused_result))`.
2.  **No Side Effects in Asserts:** Audit all `assert()` statements to verify they contain pure invariant checks without operational assignments.
3.  **Explicit Ownership Contracts:** Verify documentation specifies memory allocation/deallocation ownership across API boundaries.

## Compiler, ABI, and Toolchain Implications
*   **Contract Warnings:** Attributes enable compile-time diagnostics during build time for incorrect argument bindings.
*   **Dead Code Elimination:** The compiler aggressively optimizes paths based on declared API constraints (e.g., assuming functions marked `__attribute__((pure))` do not mutate global state).

## Performance, Memory, Timing, and Power
*   **Assertion Overhead:** Debug build assertions add minor ROM/RAM overhead. Production builds compile assertions away (`-DNDEBUG`), restoring maximum performance and deterministic timing.
*   **Defensive Checking Penalty:** Adding branch checks to inner-loop functions adds CPU cycle latency. Design contracts to validate at public boundaries and use assertions internally.

## Verification / Debugging
*   **Static Analysis:** Tools like Clang-Tidy enforce contract compliance across calling translation units.
*   **Runtime Sanity Monitoring:** Enable hardware watchdog timers to trap software that hangs when contract violations occur.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.7:* The value returned by a function having non-void return type shall be used.
    *   *Directive 4.14:* The validity of values received to the program shall be checked.
*   **Security Vulnerabilities:**
    *   CWE-252: Unchecked Return Value.
    *   CWE-754: Improper Check for Unusual or Exceptional Conditions.

## Trade-offs and Alternatives
*   **Defensive Checking Everywhere vs. Boundary Validation:** Checking every single parameter in private static functions causes code bloat and degrades performance. Robust architectures validate aggressively at external public API boundaries and use assertions for internal invariants.

## Staff-Level Takeaway
A function API contract is an architectural boundary that must be enforced by both static attributes and runtime design. Staff engineers should mandate `[[nodiscard]]` for all status returns, enforce boundary-level input sanitization, ban operational side effects inside assertions, and rigorously document concurrency and memory ownership invariants.

## Related Concepts
*   [[01_Function_definition]]
*   [[02_Function_declaration]]
*   [[07_Returning_values]]
*   [[Stack Frame Architecture and ABI]]
*   [[Interrupt Handling and ISRs]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
