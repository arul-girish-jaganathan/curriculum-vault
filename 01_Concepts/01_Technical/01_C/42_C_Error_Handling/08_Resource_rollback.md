# Resource rollback

> Canonical C topic note — Chapter 42. Rollback restores externally visible state when a multi-step operation cannot complete. Cleanup releases resources; rollback additionally undoes state changes already committed to hardware or persistent data.

## Definition
If an operation changes state through steps A, B, and C and C fails, rollback attempts to return the system to a defined prior state. Full rollback is not always possible, so the contract must distinguish atomic, partially applied, and compensating behavior.

## Mechanism and language rules
C provides no transactional primitive for arbitrary resources. The implementation must record enough state to undo completed steps and execute compensating operations in reverse dependency order.

### What to reason about
- Which state changes are reversible?
- What information is needed to restore the previous state?
- Can rollback itself fail?
- Is the prior state externally observable?
- Is the operation idempotent?
- Does persistence require journaling or commit markers?

A robust design defines an explicit state machine rather than scattering ad-hoc undo operations across error branches.

## Embedded implications
Rollback can apply to peripheral configuration, power sequencing, communication sessions, firmware updates, and configuration storage. Hardware may have irreversible actions, such as triggering an external actuator or consuming a one-time command; these cannot be rolled back and require a different failure contract.

### Firmware review angle
For nonvolatile configuration, use transactional records, versioning, CRC, and commit markers rather than assuming a failed write can simply be undone. For hardware sequences, identify which transitions are irreversible before designing recovery.

## Edge cases and failure modes
- Rollback uses stale state and restores the wrong configuration.
- A rollback step fails, leaving a partially restored system.
- Concurrent actors modify state during the transaction.
- Power loss occurs during rollback.
- An irreversible action was performed before failure.

## Example pattern
```c
typedef enum { ST_IDLE, ST_PREPARED, ST_ACTIVE } state_t;

status_t activate(void)
{
    if (prepare_hw() != STATUS_OK) return STATUS_IO;
    if (start_hw() != STATUS_OK) {
        (void)restore_hw();
        return STATUS_IO;
    }
    return STATUS_OK;
}
```
The real contract must define whether `restore_hw()` can fail and what state remains if it does.

## Verification / debugging
Inject failures after each state transition and test rollback under reset/power interruption where applicable. Verify idempotence and that concurrent access is blocked or coordinated during the transaction.

Staff-level questions:
- Is rollback actually possible for every side effect?
- What is the defined state after rollback failure?
- Would a state machine or journal be clearer?

## Staff-level takeaway
Rollback is a **state-restoration contract**, not merely cleanup. Explicitly model reversible and irreversible effects and define a safe degraded state when complete restoration is impossible.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
