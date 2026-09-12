# Recovery boundaries

> Canonical C topic note — chapter 34.

## Definition
A **recovery boundary** is the architectural point at which a failure or asynchronous event is converted into a controlled, well-defined continuation path. In C, `setjmp()`/`longjmp()` can implement such a boundary, but the boundary is safe only when lifetime, resource ownership, asynchronous state, and invariants are explicitly defined.

A good recovery boundary answers: **what can be recovered, what state is discarded, who owns cleanup, and where execution resumes?**

## Mechanism and language rules
A recovery boundary should have one owner for the saved context and a clearly scoped set of operations that can cross it. With `setjmp()`:

```text
enter boundary
   ↓
setjmp() establishes recovery point
   ↓
perform bounded operation
   ↓
failure ──> longjmp()
              ↓
       restore execution context
              ↓
       validate/reset state
              ↓
       recovery decision
```

The jump itself does not restore arbitrary program state. Memory contents, peripheral state, locks, allocations, file state, DMA activity, and application invariants remain whatever the failure left behind unless the recovery code explicitly repairs them.

### What to reason about
- The target stack frame must still be active.
- Every bypassed cleanup must be classified as safe-to-abandon, recoverable, or unrecoverable.
- Recovery should establish a known-good state before normal operation resumes.
- Partial operations need transactional boundaries where possible.
- Recovery from asynchronous signals/faults may have additional restrictions beyond ordinary `longjmp()`.
- A recovery point is not a substitute for a state machine when failures can occur at many layers.

## Embedded implications
Embedded recovery is harder because software interacts with persistent hardware state. A failed operation may have left:
- a peripheral enabled;
- DMA active;
- an interrupt pending;
- a bus transaction incomplete;
- clocks configured for a temporary mode;
- a watchdog partially serviced;
- locks held by an abandoned path;
- security state changed.

A `longjmp()` that fixes the C stack does not fix these system-level effects.

### Firmware review angle
For each recovery boundary create a recovery checklist:

```text
CPU/C stack      -> valid?
locks            -> released/reset?
heap             -> consistent?
interrupts       -> expected mask/priority?
DMA              -> stopped/reinitialized?
peripherals      -> known state?
protocol state   -> transaction aborted?
telemetry        -> failure recorded?
watchdog         -> intentional outcome?
```

## Edge cases and failure modes
The most dangerous design is **partial recovery**: the code resumes successfully from the C point but leaves hardware or shared state corrupted.

Other failures include recovery loops that repeatedly encounter the same fault, stale pointers to abandoned objects, double cleanup, and recovery paths that themselves depend on the failed subsystem.

A fault handler should not attempt heroic recovery from an invariant violation that makes the software state untrustworthy. Reset can be the safer recovery boundary.

## Example pattern
```c
static int recoverable_transaction(void)
{
    /* Acquire resources in an order that the recovery path can undo. */
    if (prepare() != 0) {
        return -1;
    }

    if (execute() != 0) {
        rollback();
        return -1;
    }

    commit();
    return 0;
}
```

This explicit transaction pattern is often preferable to a non-local jump because cleanup remains visible and reviewable.

## Verification / debugging
Inject failures after every significant acquisition and state transition. Verify that recovery produces the same known-good state as a clean restart of that subsystem.

Use assertions, fault injection, trace markers, reset-reason registers, and persistent diagnostic records to prove recovery behavior on target hardware.

Staff-level questions:
- What invariant defines the recovery boundary?
- Can the boundary guarantee a clean state, or is reset safer?
- Is the recovery mechanism more complex than the failure it handles?
- What evidence proves that all external state is restored?

## Staff-level takeaway
A recovery boundary is a **system invariant**, not merely a `setjmp()` location. Prefer explicit cleanup/state machines where possible; use non-local jumps only when the recovery scope is narrow and fully auditable.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
