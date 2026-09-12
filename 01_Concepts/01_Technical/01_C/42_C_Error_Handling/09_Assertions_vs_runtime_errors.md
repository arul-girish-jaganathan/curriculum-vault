# Assertions vs runtime errors

> Canonical C topic note — Chapter 42. Assertions detect violated programmer/system invariants; runtime errors are expected operational failures that the product must handle. Confusing the two creates unsafe recovery behavior.

## Definition
An assertion expresses a condition that should be true if program invariants and contracts hold. A runtime error represents a condition that can legitimately occur during operation: timeout, unavailable device, invalid external input, memory exhaustion, or lost communication.

## Mechanism and language rules
The C `assert` macro is controlled by `NDEBUG` and is therefore not an appropriate mechanism for required production error handling. A runtime check that protects against external data, hardware state, or normal resource exhaustion must remain active regardless of assertion configuration.

### What to reason about
- Is the condition a programmer invariant or an expected operational condition?
- Does disabling assertions remove a safety-critical check?
- Is recovery defined if the condition fails?
- Can the assertion expression have side effects?
- Does the failure path preserve enough diagnostic state?

Assertions should validate assumptions; normal control flow should handle expected failure.

## Embedded implications
A failed assertion may intentionally reset or enter a safe state, but only after capturing useful evidence and ensuring the fault path is bounded. Hardware timeouts and invalid external frames should normally be handled without treating them as impossible programmer errors.

### Firmware review angle
Maintain separate policies for development assertions, production invariant checks, and operational error handling. Safety-critical checks must not disappear merely because `NDEBUG` is defined.

## Edge cases and failure modes
- Required bounds check hidden inside `assert`.
- Side effect inside an assertion disappears in release builds.
- Expected hardware timeout treated as fatal assertion.
- Assertion handler consumes too much stack or depends on failed services.

## Example pattern
```c
/* Correct: operational validation remains in release builds. */
if (length > sizeof(buffer)) {
    return STATUS_INVALID_LENGTH;
}

/* Appropriate invariant check. */
assert(state != STATE_CORRUPT);
```
The first condition is part of normal error handling; the second states an invariant.

## Verification / debugging
Build with and without `NDEBUG` and compare required safety behavior. Use static analysis to identify side effects in assertions. Fault-inject expected runtime failures and separately inject impossible-state violations.

Staff-level questions: Which checks are required for safety? Which failures are expected? What happens when the assertion handler itself cannot rely on normal services?

## Staff-level takeaway
Use assertions to expose **broken assumptions**, not to implement ordinary error handling. Required runtime checks must remain semantically present in every supported build configuration.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
