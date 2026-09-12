# Cleanup on failure

> Canonical C topic note — Chapter 42. Failure cleanup restores ownership and releases resources acquired before an operation failed. In C, cleanup is explicit, so every acquired resource needs a clear release path.

## Definition
Cleanup covers memory, locks, file descriptors, peripheral handles, DMA channels, interrupts, clocks, buffers, and temporary state. The central invariant is: every successfully acquired resource is eventually released or deliberately transferred to another owner.

## Mechanism and language rules
C has no automatic destructor mechanism. Cleanup can use structured control flow, common `goto cleanup` exits, helper functions, or explicit state machines. `goto` to a cleanup label is often clearer and safer than deeply nested error handling when acquisition steps are ordered.

### What to reason about
- Which resources have been acquired at each failure point?
- Is cleanup safe if initialization was only partial?
- Is release idempotent?
- Does cleanup require the same lock or hardware state that failed?
- Can cleanup itself fail?
- Does cleanup preserve the original error?

Do not release a resource that was never acquired, and do not overwrite the primary failure merely because cleanup encountered a secondary error unless the contract requires that behavior.

## Embedded implications
Cleanup may include disabling DMA, stopping a peripheral, clearing interrupts, releasing clocks, and returning buffers to pools. Incorrect order can leave hardware active after software believes it has stopped.

### Firmware review angle
Represent acquisition state explicitly and document cleanup ordering. For safety-critical systems, analyze cleanup under power failure, timeout, reset, and concurrent access.

## Edge cases and failure modes
- Double free or double release.
- Cleanup of partially initialized hardware.
- DMA continues after buffer release.
- Original failure overwritten by cleanup failure.
- Lock released by the wrong ownership context.

## Example pattern
```c
status_t start(device_t *dev)
{
    status_t st = STATUS_OK;
    bool clock_on = false;
    bool irq_enabled = false;

    st = clock_enable(dev);
    if (st != STATUS_OK) goto cleanup;
    clock_on = true;

    st = irq_setup(dev);
    if (st != STATUS_OK) goto cleanup;
    irq_enabled = true;

    return STATUS_OK;

cleanup:
    if (irq_enabled) irq_teardown(dev);
    if (clock_on) clock_disable(dev);
    return st;
}
```
The flags encode which cleanup actions are valid.

## Verification / debugging
Inject failures after each acquisition step and verify that no resource leaks or double releases occur. Track pool counts, DMA ownership, interrupt enables, and peripheral states before and after failure.

Staff-level questions: Is cleanup complete for every path? Is the ordering hardware-safe? Can cleanup fail or block? Does the function preserve the root cause?

## Staff-level takeaway
Robust cleanup is **state-aware rollback**, not a collection of `free()` calls. Model partial acquisition explicitly and make every failure path converge on a verifiable ownership state.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
