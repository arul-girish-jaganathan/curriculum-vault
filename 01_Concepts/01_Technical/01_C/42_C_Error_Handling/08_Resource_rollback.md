# Resource rollback

> Canonical C topic note — Chapter 42. Resource rollback returns a partially completed operation to a known safe state when forward progress cannot continue.

## Definition
Rollback differs from simple cleanup: cleanup releases resources, while rollback restores externally visible state. Examples include undoing a configuration change, returning a buffer to a pool, reversing a reservation, or restoring a peripheral to a safe state.

## Mechanism and language rules
Rollback is usually implemented by recording which forward steps succeeded and undoing them in reverse dependency order. Not every operation is reversible; hardware side effects and transmitted data may be irreversible.

### What to reason about
- Which actions are reversible?
- Is rollback order the exact reverse of acquisition/dependency order?
- Can an undo action itself fail?
- Is the operation atomic from the caller's perspective?
- What state is externally visible during partial execution?
- Is retry after rollback safe?

A C function should not claim transactional semantics unless the implementation can actually restore the promised state.

## Embedded implications
Peripheral configuration, clock trees, DMA channels, flash operations, and communication transactions often have irreversible stages. Firmware should distinguish “rollback succeeded,” “rollback partially succeeded,” and “system must enter safe/reset state.”

### Firmware review angle
Define transactional boundaries explicitly. For non-reversible hardware actions, prefer a state machine that moves into a controlled degraded state instead of pretending a full rollback exists.

## Edge cases and failure modes
- Undo performed in the wrong order.
- Rollback assumes a resource that has already failed.
- Hardware side effect cannot be undone.
- Cleanup succeeds but externally visible state remains changed.
- Retry duplicates an operation that was only partially rolled back.

## Example pattern
```c
status_t configure(device_t *d)
{
    status_t st = set_mode(d, MODE_A);
    if (st != STATUS_OK) return st;

    st = enable_feature(d);
    if (st != STATUS_OK) {
        (void)set_mode(d, MODE_SAFE);
        return st;
    }
    return STATUS_OK;
}
```
The example is true rollback only if `MODE_SAFE` is a documented valid recovery state.

## Verification / debugging
Inject failure after each forward step. Verify both software state and actual hardware registers/outputs. Test rollback failure itself and power interruption at each irreversible boundary.

Staff-level questions: What is the transaction boundary? Which effects are irreversible? What is the safe state if rollback fails? Is reset the more reliable recovery mechanism?

## Staff-level takeaway
Rollback is a **state-transition contract**. Only promise reversibility that can be demonstrated, and design an explicit safe outcome for the point where rollback is impossible.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
