# Fault containment

> Canonical C topic note — Chapter 42. Fault containment limits the consequences of an error so that one failed component does not corrupt unrelated state or compromise the entire system.

## Definition
Containment is an architectural property implemented through boundaries, ownership, validation, state machines, watchdogs, MPU/MMU protections, process/task separation, and controlled recovery. ISO C itself does not provide fault containment; C code participates in a larger execution environment.

## Mechanism and language rules
Containment begins by identifying what may fail and what must remain trustworthy. A failure contract should specify detection, containment boundary, recovery action, and resulting state. Memory safety defects such as out-of-bounds writes can defeat software containment unless hardware protection or stronger verification catches them.

### What to reason about
- Which state can the failing component modify?
- Which resources must remain available for recovery?
- Can corrupted data cross the API boundary?
- Is recovery idempotent?
- What evidence must survive the fault?

Do not assume that returning an error contains a fault if memory may already be corrupted.

## Embedded implications
Typical containment boundaries include RTOS tasks, protected memory regions, peripheral ownership, communication parsers, and independent watchdog domains. A driver failure may be contained by resetting one peripheral rather than rebooting the whole MCU, provided shared state is still trustworthy.

### Firmware review angle
Define a degraded state that is safer than continuing with uncertain state. For safety-related functions, determine whether isolation must be hardware-enforced. Recovery paths need their own timing, stack, and power-failure analysis.

## Edge cases and failure modes
- Corrupted control data escapes the intended boundary.
- Recovery uses the same failed resource and loops.
- Fault handler relies on a corrupted stack or heap.
- A shared singleton defeats task-level isolation.
- Partial hardware reset leaves stale peripheral state.

## Example pattern
```c
status_t comm_service_step(void)
{
    status_t st = parser_step();
    if (st != STATUS_OK) {
        parser_reset();
        return STATUS_DEGRADED;
    }
    return STATUS_OK;
}
```
This is only containment if `parser_reset()` and all parser-owned state are trustworthy and isolated from unrelated services.

## Verification / debugging
Inject malformed inputs, timeouts, memory pressure, and peripheral failures. Verify that the fault stays within the intended boundary and that recovery reaches a known state. Use MPU faults, watchdog resets, and fault-injection tests where supported.

Staff-level questions:
- What is the smallest effective containment boundary?
- Which state remains trustworthy after failure?
- Is recovery safer than reset?
- What hardware protection is required?

## Staff-level takeaway
Containment is **about limiting blast radius**, not merely returning an error. Establish explicit ownership and protection boundaries and define a recovery state that remains safe even when local state is suspect.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
