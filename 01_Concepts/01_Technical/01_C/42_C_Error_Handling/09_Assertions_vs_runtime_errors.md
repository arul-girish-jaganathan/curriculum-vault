# Assertions vs runtime errors

> Canonical C topic note — Chapter 42. Assertions express programmer/system invariants that should not normally be violated; runtime error handling represents expected environmental or operational failures.

## Definition
An assertion answers “this condition must be true if the program is correct.” Runtime error handling answers “this operation can legitimately fail, and the caller must decide what to do.” Confusing the two produces either fragile production firmware or silently ignored defects.

## Mechanism and language rules
`assert()` is controlled by `NDEBUG`; a disabled assertion does not execute its expression. Therefore an assertion expression must not contain required side effects. `_Static_assert`/`static_assert` checks compile-time constraints and is fundamentally different from runtime `assert`.

### What to reason about
- Is the condition a programmer invariant or an expected failure?
- Must the check exist in production?
- Does the expression have side effects?
- What is the recovery action if the invariant fails?
- Can the system safely continue after violation?

For externally controlled input, hardware timeout, unavailable peripheral, allocation failure, or communication loss, normal error handling is generally appropriate. For impossible internal states, an assertion or fail-stop mechanism may be appropriate.

## Embedded implications
A production assertion may reset, enter a fault handler, capture context, or transition to a safe state. Removing assertions entirely can remove useful diagnostics; leaving expensive assertions in hard real-time paths can violate timing budgets.

### Firmware review angle
Define assertion policy by subsystem and safety level. Safety-critical systems may require production checks even when they are not implemented using the standard `assert()` macro. The important property is explicit invariant checking and defined failure containment.

## Edge cases and failure modes
- Side effects disappear under `NDEBUG`.
- An assertion is used to validate user/network input and causes unnecessary resets.
- A runtime failure is asserted instead of recovered.
- Assertion failure itself performs unsafe logging or allocation.

## Example pattern
```c
status_t queue_push(queue_t *q, item_t item)
{
    assert(q != NULL);          /* programmer contract */
    if (q->count == QUEUE_CAPACITY) {
        return STATUS_FULL;     /* expected runtime condition */
    }
    q->items[q->count++] = item;
    return STATUS_OK;
}
```
Whether `q == NULL` should be an assertion or runtime error depends on the API contract and safety policy.

## Verification / debugging
Build with and without `NDEBUG` and verify that required behavior is unchanged. Test all expected runtime failures and deliberately violate key invariants in a controlled environment to validate fault capture and recovery.

Staff-level questions:
- What class of failure is this?
- What happens in production when the condition is violated?
- Does the check protect a safety boundary or merely aid debugging?

## Staff-level takeaway
Use assertions to expose **broken assumptions** and runtime errors to represent **expected operational failure**. The distinction should be explicit in API and safety contracts, not left to individual coding style.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
