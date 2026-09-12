# Bit set/clear/toggle

> Canonical C topic note — Chapter 43. Set, clear, and toggle operations are common transformations of an integer bitfield, but MMIO registers require hardware-specific semantics beyond ordinary C bitwise behavior.

## Definition
For a mask `m`: set with `x |= m`; clear with `x &= ~m`; toggle with `x ^= m`; test with `(x & m) != 0`. These operate on ordinary integer objects according to C's integer promotions and bitwise rules.

## Mechanism and language rules
The compound assignment reads the left operand, performs the operation, and stores the result. Therefore it is a read-modify-write sequence at the machine level unless the compiler can use a specialized instruction. It is not automatically atomic with respect to another thread, ISR, or hardware agent.

### What to reason about
- Is the object shared concurrently?
- Is it ordinary RAM or MMIO?
- Does `~m` have the intended width after promotions?
- Are multiple bits represented by one mask?
- Does the hardware provide atomic set/clear/toggle registers?

## Embedded implications
For ordinary RAM shared with an ISR, `flags |= MASK` can race with an ISR clearing another flag. For MMIO, read-modify-write may lose write-one-to-clear events or alter reserved bits.

### Firmware review angle
Use atomic hardware aliases or critical sections when required. For software flags shared between contexts, use an appropriate atomic type/operation or a concurrency protocol rather than assuming a single C statement is indivisible.

## Edge cases and failure modes
- Clearing with `~MASK` can affect unintended high bits if width is implicit.
- Read-modify-write loses concurrent changes.
- Toggling a status bit with `^=` may be meaningless for hardware state machines.
- A macro may evaluate its register argument multiple times.

## Example pattern
```c
#define FLAG_RX_READY (UINT32_C(1) << 3)

flags |= FLAG_RX_READY;
flags &= ~FLAG_RX_READY;
flags ^= FLAG_RX_READY;
```
For a 32-bit `flags`, the mask type should be chosen deliberately.

## Verification / debugging
Test each operation with zero, all-one, adjacent-bit, and concurrent-update cases. For MMIO, inspect the vendor-defined write semantics and generated bus accesses. Use race analysis or atomic instrumentation for shared RAM.

## Staff-level takeaway
Set/clear/toggle syntax is easy; the engineering question is whether the **read-modify-write transaction is valid for the ownership and hardware model**. Treat atomicity and register semantics as first-class requirements.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
