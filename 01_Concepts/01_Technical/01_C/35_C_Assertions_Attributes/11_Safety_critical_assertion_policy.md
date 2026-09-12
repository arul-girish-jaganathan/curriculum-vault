# Safety-critical assertion policy

> Canonical C topic note — chapter 35.

## Definition
A safety-critical assertion policy defines which assumptions may be asserted, what happens when an assertion fails, which contexts permit diagnostics, and how failures are recorded and contained. In safety-critical firmware, `assert` is only one implementation mechanism; the real artifact is the system-level failure contract.

## Mechanism and language rules
Separate three classes:
1. **Build-time invariants** — reject with `_Static_assert` or configuration checks.
2. **Defensive runtime checks** — validate recoverable or externally influenced conditions explicitly.
3. **Impossible-state invariants** — detect programming/design failures and enter a defined safe state.

A policy should specify whether production assertions remain enabled, how diagnostic data is captured, and whether failure leads to reset, degraded operation, safe-state transition, or controlled shutdown.

### What to reason about
- Never let an assertion's side effects be required for correctness.
- Define behavior for task, ISR, startup, and fault-handler contexts.
- Bound diagnostic execution time and memory use.
- Consider watchdogs and repeated-failure loops.

## Embedded implications
A failed assertion can occur when clocks, RAM, flash, peripherals, or RTOS services are not fully initialized. Consequently, a generic logging routine may itself be unsafe. A robust design often records a small fixed-size failure record containing an ID, source location or build ID, CPU state, and reset reason, then transitions to the platform's failure state.

For safety systems, “continue after assert” is not automatically safer: continuing with a violated invariant may be more dangerous than controlled reset or shutdown.

### Firmware review angle
Map every assertion class to a safety case and failure reaction. Measure worst-case execution time, stack use, persistent-storage behavior, and watchdog interaction. Ensure production behavior is intentional rather than simply inherited from a debug macro.

## Edge cases and failure modes
Dangerous patterns include formatted logging from a fault context, dynamic allocation during failure handling, attempting to recover after corrupted global state, and repeatedly writing the same persistent failure record until flash wears out.

Do not assert on normal communication errors or malformed external input unless the policy explicitly defines those conditions as impossible.

## Example pattern
```c
static void invariant_failed(uint16_t id)
{
    fault_record_minimal(id);
    disable_nonessential_activity();
    system_reset_or_safe_state();
    for (;;) {
        /* Watchdog or hardware safety mechanism owns final recovery. */
    }
}
```

## Verification / debugging
Inject assertion failures in every supported execution context. Verify the resulting reset reason, persistent record, watchdog behavior, and next-boot handling. Perform power-loss testing if records are stored in nonvolatile memory.

## Staff-level takeaway
A safety assertion is not just a macro. It is a deliberate failure-management path whose timing, persistence, reset behavior, and safety consequence must be specified and verified.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
