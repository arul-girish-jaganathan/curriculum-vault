# Embedded degraded modes

> Canonical C topic note — Chapter 42. A degraded mode deliberately reduces functionality while preserving a defined safety and availability boundary after a failure.

## Definition
A degraded mode is an explicitly designed operating state entered when full service cannot be provided. It differs from an uncontrolled partial failure because the allowed behavior, disabled features, resource ownership, and recovery criteria are known.

## Mechanism and language rules
Represent degraded states with an explicit state machine or status model. Error codes alone are insufficient if multiple callers can independently choose incompatible recovery actions.

### What to reason about
- What functionality remains guaranteed?
- Which outputs are suppressed or substituted?
- What resources are released or isolated?
- What condition permits recovery?
- Is recovery automatic, manual, or power-cycle dependent?

C does not define a degraded-mode mechanism; the implementation must make state transitions and data validity explicit.

## Embedded implications
Examples include reduced sensor rate after a peripheral fault, read-only operation after storage failure, disabling a nonessential feature after memory pressure, or entering a safe actuator state after communication loss. The degraded state must have bounded CPU, stack, power, and communication costs.

### Firmware review angle
Define entry/exit conditions, hysteresis, timeout policy, telemetry, and user-visible behavior. Avoid automatic recovery storms where repeated retries repeatedly consume scarce resources.

## Edge cases and failure modes
- A degraded mode accidentally enables unsafe outputs.
- Recovery occurs before the underlying fault is actually cleared.
- Multiple subsystems disagree about the current mode.
- A latched fault is cleared without preserving evidence.
- The degraded path has less test coverage than the normal path.

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
Real designs should centralize transition policy and protect shared state according to their concurrency model.

## Verification / debugging
Inject each supported failure and verify the exact state transition, outputs, resource usage, telemetry, and recovery behavior. Test repeated failures, reboot during degraded mode, and recovery when the fault persists.

Staff-level questions:
- What safety property does the degraded mode preserve?
- What evidence proves recovery is safe?
- Can the mode be represented and tested as a finite state machine?

## Staff-level takeaway
A degraded mode is a **contracted operating state**, not “whatever happens after an error.” Make the reduced capability explicit and ensure the degraded path is at least as rigorously tested as the nominal path.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
