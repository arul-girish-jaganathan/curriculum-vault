# Masks

> Canonical C topic note — Chapter 43. A bit mask selects or clears specific bits using integer bitwise operations. Correct masking depends on width, signedness, promotions, and the target register/protocol contract.

## Definition
A mask is an integer value whose set bits identify positions of interest. `x & mask` selects bits; `x | mask` sets selected bits; `x & ~mask` clears selected bits; `x ^ mask` toggles them. C defines bitwise operators on integer types, but hardware register semantics and exact-width assumptions are platform-specific.

## Mechanism and language rules
Integer operands undergo the integer promotions before most bitwise operations. This is why small integer types can produce an `int` result. Unsigned types are generally easiest for raw bit manipulation because their modulo arithmetic and bitwise representation are well defined within the type's width.

### What to reason about
- What is the exact width of the operand?
- Are integer promotions changing the expression type?
- Is the mask unsigned and explicitly sized?
- Could shifting create an invalid operand before the mask is applied?
- Is the value an ordinary object, protocol field, or MMIO register?

For register code, use a type matching the documented register width and avoid accidental read-modify-write of reserved bits.

## Embedded implications
Masks are fundamental for flags, status registers, interrupt enables, protocol fields, and packed metadata. On MMIO, `reg &= ~MASK` performs a read-modify-write and can accidentally clear/write unrelated bits if the hardware has write-one-to-clear or write-one-to-set semantics.

### Firmware review angle
Use named masks derived from the specification. Keep masks in unsigned types such as `UINT32_C(...)` when width matters. Document reserved bits and whether the hardware supports atomic set/clear aliases.

## Edge cases and failure modes
- `~mask` has the promoted operand type, not necessarily the intended register width.
- Signed shifts can introduce implementation-defined or undefined behavior.
- A mask larger than the target register may silently truncate.
- Read-modify-write can lose concurrent hardware changes.

## Example pattern
```c
#include <stdint.h>
#define READY_MASK UINT32_C(1) << 7

uint32_t flags = status;
if ((flags & READY_MASK) != 0U) {
    /* bit 7 is set */
}
```
Parentheses make precedence and intent explicit.

## Verification / debugging
Test masks at bit 0, the highest valid bit, and adjacent bits. Compile with conversion/shift warnings enabled. For MMIO, compare generated accesses with the device reference manual and inspect whether read-modify-write is permitted.

## Staff-level takeaway
Bit masks are simple only when **width, signedness, promotion, and hardware semantics are explicit**. Treat every register mask as part of a machine-level contract, not just an integer expression.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
