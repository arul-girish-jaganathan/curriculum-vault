# Control-flow hazards

> Canonical C topic note — chapter 34.

## Definition
Non-local control flow introduces execution paths that are not represented by ordinary C call/return structure. Signals can asynchronously enter a handler; `longjmp()` can bypass intermediate returns. These mechanisms create **control-flow hazards** when resource ownership, object lifetime, or invariants depend on normal structured execution.

## Mechanism and language rules
Normal C control flow provides an approximately lexical model:

```text
call -> callee -> return -> caller
```

A signal can interrupt this model, while `longjmp()` creates a direct transfer:

```text
A -> B -> C
     ^     |
     |_____|
       jump
```

The compiler must preserve the semantics of these constructs, but it cannot infer application-level cleanup obligations that C does not encode.

### What to reason about
- Which stack frames can be bypassed?
- Which automatic objects are still alive at the destination?
- Which variables can have indeterminate values after a non-local jump?
- Which locks, allocations, transactions, and hardware states are live?
- Can an asynchronous handler interrupt a non-reentrant subsystem?
- Does static analysis understand the transfer, or will reviewers need explicit annotations?

Control-flow complexity is a safety concern even when the behavior is technically defined. The question is not only **"is this legal C?"** but **"can humans and tools prove every path?"**

## Embedded implications
Firmware often has hidden control-flow dependencies: watchdog recovery, interrupt dispatch, scheduler context switches, fault handlers, boot phases, and peripheral state machines. Non-local jumps can cross those boundaries without restoring their invariants.

For safety-oriented systems, prefer explicit status propagation, state machines, supervisor tasks, and reset-based recovery. These make failure edges visible in code review and static analysis.

### Firmware review angle
Build a control-flow graph for every use of `longjmp()` or asynchronous handler. Mark:
- resource acquisition/release;
- critical-section entry/exit;
- interrupt masking;
- peripheral transactions;
- ownership transfer;
- logging/telemetry;
- watchdog operations.

Then prove that every non-local edge preserves the required invariants.

## Edge cases and failure modes
Typical hazards:
- skipped cleanup causing leaks or deadlocks;
- double cleanup after partial recovery;
- stale pointers into abandoned stack state;
- compiler-visible variables differing from programmer intuition after `longjmp()`;
- handler recursion or re-entry;
- recovery from an already-corrupted stack;
- fault paths that invoke the same broken service that caused the fault.

A particularly dangerous anti-pattern is `goto`/`longjmp`/signal use chosen merely to reduce indentation. Control-flow syntax should serve a verifiable architecture, not cosmetic convenience.

## Example pattern
```c
static int process(void)
{
    int rc = acquire();
    if (rc != 0) {
        return rc;
    }

    rc = operate();
    if (rc != 0) {
        release();
        return rc;
    }

    release();
    return 0;
}
```

Explicit cleanup makes the recovery path visible and is generally easier to analyze than non-local transfer.

## Verification / debugging
Enable compiler warnings and static analysis. Draw the control-flow graph for exceptional paths. Test injected failures at every cleanup boundary. Use debugger backtraces carefully because a non-local jump intentionally changes the normal call stack relationship.

Staff-level questions:
- Does the architecture remain understandable without the non-local jump?
- Which invariants are implicit today?
- Can ownership be represented structurally instead?
- What happens if the failure occurs inside the recovery path itself?

## Staff-level takeaway
The core risk of non-local control flow is **hidden edges in the program's proof of correctness**. Prefer mechanisms whose failure paths are explicit, bounded, and mechanically analyzable.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
