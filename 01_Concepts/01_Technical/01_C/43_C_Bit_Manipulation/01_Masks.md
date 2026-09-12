# Masks

> Canonical C topic note — Chapter 43. A bit mask selects, clears, sets, or tests a defined subset of bits. Correct mask code depends on integer width, promotions, signedness, shift rules, and the hardware or protocol contract being represented.

## Definition
A mask is an integer value whose bit pattern identifies positions of interest. Common operations are `value & mask` for selection/testing, `value | mask` for setting, `value & ~mask` for clearing, and `value ^ mask` for toggling.

## Mechanism and language rules
Use unsigned integer types for low-level bit manipulation unless signed semantics are specifically required. Integer promotions apply to operands narrower than `int`, and `~` operates on the promoted type. A mask should therefore be constructed with the intended width rather than relying on implicit signed arithmetic.

### What to reason about
- What is the exact width of the value and mask?
- Are operands promoted before the operation?
- Does `~mask` contain unwanted high bits after promotion?
- Is the bit position within range?
- Is the operation a normal RAM update or a hardware register access?
- Can another agent modify the same word between read and write?

Prefer `UINT32_C(...)`, fixed-width types, and width-aware helper macros when portability matters.

## Embedded implications
Masks are fundamental for registers, status words, protocol fields, permission flags, and packed state. On MMIO registers, `reg |= mask` is safe only when read-modify-write is permitted by the hardware specification.

### Firmware review angle
Define field masks and positions from one authoritative register description. Avoid magic hexadecimal constants that obscure field meaning. Consider atomic set/clear aliases when concurrent hardware modification is possible.

## Edge cases and failure modes
- Wrong-width mask silently leaves or changes unrelated bits.
- `~mask` affects bits outside the intended field.
- Shift count equals or exceeds operand width.
- Signed shifting introduces implementation-defined or undefined behavior.
- Read-modify-write loses a concurrently occurring hardware event.

## Example pattern
```c
#include <stdint.h>

#define READY_MASK UINT32_C(1) << 5

uint32_t set_ready(uint32_t status)
{
    return status | READY_MASK;
}

int is_ready(uint32_t status)
{
    return (status & READY_MASK) != 0U;
}
```
The mask has an explicit intended width.

## Verification / debugging
Test zero, all-one, adjacent-bit, maximum-position, and unrelated-bit cases. Compile with conversion and sign warnings. For registers, compare every operation with the peripheral's access semantics and inspect generated accesses when needed.

Staff-level questions: What invariant does each mask encode? Could future hardware reuse reserved bits? Is the operation atomic with respect to all writers?

## Staff-level takeaway
A mask is simple syntax hiding a **representation contract**. Make width, field ownership, reserved bits, and concurrency explicit before accepting low-level bit operations as correct.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
