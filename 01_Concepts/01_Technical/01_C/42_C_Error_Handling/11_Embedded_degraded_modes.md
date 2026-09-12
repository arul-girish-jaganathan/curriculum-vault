# Embedded degraded modes

> Canonical C topic note — Chapter 42. A degraded mode is an explicitly defined operating state that reduces capability while preserving specified safety, availability, or data-integrity guarantees after a failure.

## Definition
A degraded mode differs from uncontrolled partial failure because its allowed outputs, disabled features, resource ownership, recovery criteria, and user-visible behavior are deliberate. Examples include reduced sensor rate, read-only storage, disabled nonessential features, or a safe actuator state.

## Mechanism and language rules
Represent degraded operation with an explicit state machine or centralized status model. An error code alone does not guarantee that multiple callers will choose compatible recovery actions.

### What to reason about
- What functionality remains guaranteed?
- Which outputs are suppressed, substituted, or forced safe?
- Which resources are released or isolated?
- What condition permits recovery?
- Is recovery automatic, manual, or reset-dependent?
- Is the transition atomic with respect to concurrent observers?

C provides no degraded-mode primitive; the implementation must make state transitions and validity explicit.

## Embedded implications
Degraded behavior must have bounded CPU, stack, power, and communication costs. Recovery retries can consume more resources than the original fault, so retry limits and hysteresis are often required.

### Firmware review angle
Define entry/exit conditions, timeouts, telemetry, user-visible behavior, and persistence across reboot. Ensure safety-critical outputs have a deterministic state in every degraded mode.

## Edge cases and failure modes
- Degraded mode accidentally permits unsafe outputs.
- Recovery occurs before the fault is cleared.
- Multiple subsystems disagree on the current mode.
- Repeated recovery causes a reset storm.
- Degraded path receives less testing than nominal operation.

## Example pattern
```c
typedef enum {
    MODE_NORMAL,
    MODE_DEGRADED,
    MODE_SAFE
} system_mode_t;

static system_mode_t mode;

void on_sensor_failure(void)
{
    mode = MODE_DEGRADED;
}
```
Real designs should centralize transitions and synchronize shared state according to the concurrency model.

## Verification / debugging
Inject each failure and verify state transition, outputs, resource ownership, telemetry, and recovery. Test repeated failures, reboot while degraded, persistent faults, and recovery after partial hardware reset.

Staff-level questions: Which safety property is preserved? Is the state machine complete? What proves recovery is safe? Can the system remain indefinitely in degraded mode without resource exhaustion?

## Staff-level takeaway
A degraded mode is a **contracted operating state**, not “whatever happens after an error.” Design, test, and monitor the degraded path with the same rigor as nominal operation.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
