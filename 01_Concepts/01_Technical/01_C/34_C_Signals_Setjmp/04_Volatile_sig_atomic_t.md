# Volatile sig_atomic_t

> Canonical C topic note — chapter 34.

## Definition
`sig_atomic_t` is an integer type provided by `<signal.h>` for objects that can be accessed atomically in the signal-handler communication model. Declaring such an object `volatile` additionally tells the compiler that its value may change for reasons outside ordinary program flow and that accesses are observable according to volatile semantics.

A common portable pattern is:

```c
static volatile sig_atomic_t event_pending;
```

The two keywords solve different problems: **`sig_atomic_t` addresses signal-context atomicity; `volatile` addresses compiler visibility/optimization.** Neither is a general-purpose substitute for C11 atomics or a memory barrier.

## Mechanism and language rules
The type `sig_atomic_t` is implementation-defined in its exact representation but is an integer type suitable for the required signal communication. The handler can store a simple state, and normal execution can inspect it.

`volatile` means that accesses to the object are observable side effects under the language rules. It does not mean that every expression involving the object is a hardware atomic transaction, nor does it impose a C11 inter-thread memory order.

### What to reason about
- Prefer a single flag/state value over complex shared structures.
- Keep each handler access compatible with the signal model.
- `x++` is conceptually a read-modify-write operation and should not be casually treated as equivalent to a simple atomic store.
- A flag can communicate that **something happened**, but cannot necessarily count how many events occurred.
- Multiple signals may coalesce depending on the implementation, so a Boolean pending flag can intentionally lose multiplicity.
- C11 `_Atomic` is a different abstraction and should not be substituted without checking signal-specific guarantees and implementation support.

## Embedded implications
This pattern is useful when an embedded libc supports signals, but on bare metal the more common analogue is an ISR-to-main-loop flag. In that case, use the target's documented atomicity and interrupt model rather than assuming `sig_atomic_t` provides ISR synchronization.

For MMIO, `volatile` may be necessary to prevent inappropriate elimination/merging of accesses, but MMIO semantics also depend on the compiler, architecture, bus, and peripheral specification. `sig_atomic_t` has no special meaning for a hardware register.

### Firmware review angle
Check:
- width and alignment of the chosen state;
- whether a single load/store is actually atomic on the target;
- whether the consumer can miss an event between testing and clearing it;
- whether interrupt masking or stronger synchronization is required;
- whether the state survives low-power transitions and reset as intended.

## Edge cases and failure modes
Common misconceptions:
- **"volatile means thread-safe."** False.
- **"sig_atomic_t means interrupt-safe everywhere."** False; it is a C signal facility type.
- **"A volatile flag counts events."** Usually false; repeated events can collapse into one pending state.
- **"volatile provides memory ordering."** Not in the C11 atomic-memory-model sense.
- **"Read-modify-write is automatically safe."** Do not assume this from the type alone.

A second subtle issue is clearing the flag. If the consumer reads and clears it while a new signal arrives, the event may be lost unless the protocol is explicitly designed for coalescing or uses a stronger queue/counter mechanism.

## Example pattern
```c
#include <signal.h>

static volatile sig_atomic_t pending;

static void handler(int signo)
{
    (void)signo;
    pending = 1;
}

int main(void)
{
    while (!pending) {
        /* Wait or perform normal work. */
    }

    pending = 0;
    /* Handle the event outside the signal context. */
}
```

## Verification / debugging
Stress the producer/consumer boundary with repeated signal delivery. Verify the intended semantics: **edge notification**, **level notification**, or **counted events**. If event multiplicity matters, a flag is probably insufficient.

For embedded ports, inspect generated assembly for the flag access and verify interrupt masking, bus width, and ordering assumptions against the MCU reference manual.

Staff-level questions:
- What exactly is guaranteed by `sig_atomic_t` on this implementation?
- Why is `volatile` present?
- Can events be lost, and is that acceptable?
- Is the producer a signal handler, ISR, thread, DMA engine, or something else?
- What synchronization primitive is actually required by that producer?

## Staff-level takeaway
Use `volatile sig_atomic_t` as a **small signal-to-normal-flow communication mechanism**, not as a universal synchronization primitive. Explicitly define whether events may coalesce and keep the protocol simpler than the handler context.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
