# Atomic flags

> Canonical C topic note — Chapter 44. Atomic flags communicate events between execution contexts without data races when implemented with the C atomic model or an equivalent target primitive.

## Definition
An atomic flag can be read and written atomically and with defined memory-order semantics. `volatile bool` alone does not provide this guarantee. ISO C11 atomics provide `_Atomic` types and `<stdatomic.h>` operations, subject to implementation support.

## Mechanism and language rules
Atomic operations prevent conflicting unsynchronized accesses from forming a C data race and can establish ordering relationships. The correct memory order depends on what data the flag publishes or consumes.

### What to reason about
- Is only the flag atomic, or is the data it protects also correctly ordered?
- Is `memory_order_release` used by the producer and `memory_order_acquire` by the consumer where publication is required?
- Is `volatile` needed separately for MMIO?
- Is the atomic operation lock-free on the target?

A flag can signal that data is ready, but the data must be published according to the chosen memory-order relationship.

## Embedded implications
Atomics may compile to a single instruction on simple architectures or require exclusive-access loops/barriers. Some targets may implement certain atomic widths with library routines that have nontrivial latency or may temporarily mask interrupts.

### Firmware review angle
For ISR-to-task signaling, select an atomic type and memory order that match the execution model. If the ISR and main context share a ring buffer, the flag alone does not solve buffer ownership or index synchronization.

## Edge cases and failure modes
- Using a non-atomic payload with an atomic flag but no release/acquire relationship.
- Assuming every atomic width is lock-free.
- Using `volatile` instead of `_Atomic`.
- Using sequential consistency everywhere without understanding cost or need.

## Example pattern
```c
#include <stdatomic.h>

static uint32_t data;
static atomic_bool ready;

void producer(uint32_t value)
{
    data = value;
    atomic_store_explicit(&ready, true, memory_order_release);
}

bool consumer(uint32_t *out)
{
    if (!atomic_load_explicit(&ready, memory_order_acquire)) {
        return false;
    }
    *out = data;
    return true;
}
```
The release/acquire pair publishes `data` to the consumer under the C memory model.

## Verification / debugging
Use ThreadSanitizer on supported host tests, inspect generated atomic sequences, and stress the producer/consumer relationship. On target, measure interrupt latency and verify lock-free assumptions where required.

## Staff-level takeaway
An atomic flag is useful only when its **memory-order relationship and protected state are designed together**. Atomicity of the flag alone does not make the surrounding protocol correct.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
