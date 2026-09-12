# Atomic flags

> Canonical C topic note — Chapter 44. An atomic flag is a small shared state used to communicate between an ISR and another execution context without a data race. C11 atomics define atomicity and memory ordering; target interrupt mechanisms still determine whether the operation is practical and safe.

## Definition
A flag such as “event pending” can be set by an ISR and consumed by a task. A `_Atomic` object prevents conflicting accesses from constituting a C data race and can provide defined ordering through the selected memory order.

## Mechanism and language rules
Atomicity is distinct from `volatile`. An atomic load/store can be ordered using `memory_order_relaxed`, `acquire`, `release`, or stronger orders. If the ISR and task exchange only one independent event bit, relaxed operations may be enough; if the flag publishes other data, release/acquire ordering may be required.

### What to reason about
- Which contexts access the object?
- Is the object genuinely atomic on the target?
- Does the flag publish associated data?
- What memory order is required for that data dependency?
- Can events be coalesced or lost?
- Is ISR support for the chosen atomic implementation guaranteed?

## Embedded implications
A flag is cheap, but a single bit can represent only “at least one event” unless the protocol counts events. Repeated interrupts between task polls can therefore be coalesced.

### Firmware review angle
Use counters or queues when event multiplicity matters. Verify compiler/runtime support for C11 atomics in the target environment; some implementations may use locks or library calls for non-native atomic widths, which can be unsuitable in an ISR.

## Edge cases and failure modes
- Plain `volatile` flag creates a data race.
- Flag clears an event that arrived immediately after the read.
- Multiple events are silently coalesced.
- Atomic operation is not lock-free and invokes unsuitable runtime code.
- Associated data is read without acquire ordering.

## Example pattern
```c
#include <stdatomic.h>

static _Atomic bool event_pending;

void IRQ_Handler(void)
{
    atomic_store_explicit(&event_pending, true, memory_order_release);
}

void service(void)
{
    if (atomic_exchange_explicit(&event_pending, false,
                                 memory_order_acquire)) {
        process_event();
    }
}
```
The exact ISR support and memory-order choice must match the data-publishing contract.

## Verification / debugging
Stress event bursts, verify no data race under sanitizer-supported host tests, and inspect generated code for target ISR paths. Test whether event coalescing is acceptable and measure atomic operation cost.

Staff-level questions: Is a flag enough to preserve event count? Is release/acquire actually needed? Does the target implement this atomic operation without a hidden lock?

## Staff-level takeaway
An ISR flag is a **synchronization protocol**, not merely a variable. Define event multiplicity, memory ordering, target atomic support, and associated-data ownership explicitly.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
