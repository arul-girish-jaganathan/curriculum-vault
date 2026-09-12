# Fault containment

> Canonical C topic note — Chapter 42. Fault containment limits the blast radius of a failure so that one bad component, input, or hardware state does not corrupt unrelated state or compromise the entire system.

## Definition
Containment is an architectural property built from ownership, validation, isolation, protection, state machines, watchdogs, MPU/MMU boundaries, task/process separation, and controlled recovery. ISO C itself does not provide isolation.

## Mechanism and language rules
A containment contract identifies what may fail, what must remain trustworthy, how the failure is detected, and which boundary prevents propagation. Returning an error is insufficient if memory corruption has already escaped the component.

### What to reason about
- What state can the failing component modify?
- Which memory and resources remain trustworthy?
- Can corrupted data cross the API boundary?
- Is recovery idempotent and bounded?
- Can the recovery mechanism depend on the failed component?
- What evidence must survive the fault?

Separate **error handling** from **fault containment**: an error code communicates information, while containment limits damage.

## Embedded implications
Typical boundaries include RTOS tasks, MPU regions, peripheral ownership, communication parser domains, and independent watchdog/recovery domains. A peripheral fault may be isolated by resetting only that peripheral if shared state remains trustworthy.

### Firmware review angle
Choose the smallest effective containment boundary and decide where hardware enforcement is required. Analyze recovery stack, timing, power, and dependency assumptions independently from nominal execution.

## Edge cases and failure modes
- Corrupted control data escapes the intended boundary.
- Recovery uses the same failed resource and loops.
- Fault handler depends on corrupted stack/heap.
- Shared global state defeats task isolation.
- Partial hardware reset leaves stale state.

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
This is containment only if parser-owned state is isolated and `parser_reset()` is trustworthy.

## Verification / debugging
Inject malformed inputs, timeouts, memory pressure, peripheral failures, and repeated recovery attempts. Verify that unrelated outputs remain correct and that recovery reaches a known state.

Staff-level questions: What is the containment boundary? Which state remains trustworthy? What hardware protection is required? What happens if recovery itself fails?

## Staff-level takeaway
Containment is about **limiting blast radius**, not merely returning an error. Make ownership and protection boundaries explicit and design recovery around the state that remains trustworthy after failure.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
