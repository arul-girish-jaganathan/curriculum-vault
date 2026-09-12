# Embedded alternatives

> Canonical C topic note — chapter 34.

## Definition
For embedded firmware, signals and non-local jumps are often less appropriate than explicit mechanisms designed for deterministic control flow. Common alternatives include return-code propagation, state machines, event queues, supervisor tasks, watchdog reset, fault records, and hardware exception handlers.

The right alternative depends on whether the problem is a recoverable application event, a concurrency event, a driver failure, or evidence that system state is no longer trustworthy.

## Mechanism and language rules
A useful decision hierarchy is:

```text
Recoverable local error?
        │ yes
        ▼
return status / explicit cleanup
        │
        no
        ▼
Cross-context event?
        │ yes
        ▼
queue/flag/message to owning context
        │
        no
        ▼
System invariant corrupted?
        │ yes
        ▼
fault record + controlled reset/safe state
```

These mechanisms preserve structured control flow and make ownership visible.

### What to reason about
- **Return codes:** explicit, composable, easy to test; can become verbose if ignored.
- **State machines:** ideal for protocol and driver recovery; make states and transitions explicit.
- **Event queues:** preserve event identity and decouple producers from consumers.
- **Supervisor tasks:** centralize policy and isolate recovery from low-level drivers.
- **Watchdog reset:** appropriate when forward progress or system invariants cannot be trusted.
- **Fault records:** preserve evidence across reset and support root-cause analysis.
- **`setjmp`/`longjmp`:** useful only for tightly scoped recovery where bypassed state is fully understood.

## Embedded implications
Determinism is often more valuable than brevity. A state machine can be reviewed for worst-case execution time, stack use, memory ownership, and concurrency behavior. A non-local jump makes those properties harder to see.

For ISR/fault contexts, use a minimal capture path and defer processing whenever the system remains trustworthy. If the stack, scheduler, heap, or control state is corrupted, attempting normal recovery may be less safe than recording evidence and resetting.

### Firmware review angle
Compare candidate designs across:

| Criterion | Return/status | State machine | Event queue | `longjmp` | Reset |
|---|---:|---:|---:|---:|---:|
| Control-flow clarity | High | High | High | Low | High |
| Local recovery | High | High | Medium | High | Low |
| Deterministic analysis | High | High | High | Lower | High |
| Resource cleanup | Explicit | Explicit | Explicit | Easy to bypass | Reinitialization |
| Fault containment | Medium | Medium | Medium | Low/medium | High |

## Edge cases and failure modes
Do not choose a watchdog reset merely to hide a recoverable software bug; preserve diagnostic evidence first. Conversely, do not build elaborate recovery logic for a genuinely corrupted system state.

Avoid event flags when event multiplicity matters. Avoid queues when the producer context cannot safely enqueue. Avoid global recovery functions that silently reset unrelated subsystem state.

A common failure mode is mixing mechanisms: an ISR sets a flag, a task calls `longjmp()`, and the recovery path resets hardware owned by another task. Ownership becomes ambiguous and the system is no longer locally verifiable.

## Example pattern
```c
enum state {
    ST_IDLE,
    ST_ACTIVE,
    ST_RECOVER,
    ST_FAULT
};

static enum state st;

static void step(void)
{
    switch (st) {
    case ST_IDLE:
        /* Start operation. */
        break;
    case ST_ACTIVE:
        /* Perform bounded work. */
        break;
    case ST_RECOVER:
        /* Restore a known-good state. */
        break;
    case ST_FAULT:
        /* Stop accepting normal work. */
        break;
    }
}
```

## Verification / debugging
Inject failures into every state transition and verify that the resulting state is deterministic. For reset-based recovery, verify reset reason, retained fault data, boot-time recovery policy, and watchdog timing.

Measure worst-case recovery time and stack usage. Use fault-injection campaigns to distinguish failures that should recover locally from failures that should escalate to system reset.

Staff-level questions:
- What is the smallest mechanism that makes the failure safe?
- Who owns the failed resource?
- Can the state be made explicit instead of jumping around it?
- What evidence must survive reset?
- What failure rate and recovery latency does the product actually require?

## Staff-level takeaway
For embedded systems, prefer **explicit state, explicit ownership, and explicit recovery policy**. Use signals and non-local jumps only behind a well-defined platform boundary and only when they provide a real benefit that structured alternatives cannot provide.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
