# Shifts

> Canonical C topic note — Chapter 43. Shift operators move the value's bits left or right, but their safe use requires precise reasoning about operand promotions, width, signedness, and shift count.

## Definition
`x << n` shifts bits toward higher positions and fills low positions with zeros. `x >> n` shifts toward lower positions. For unsigned operands, the value is interpreted modulo the width; for signed operands, left shift has important restrictions and right shift of negative values is implementation-defined in relevant language versions.

## Mechanism and language rules
Integer promotions occur before shifting. A shift count must be nonnegative and strictly less than the width of the promoted left operand; violating this is undefined behavior. Left-shifting into or beyond the sign/range of a signed type must not be used as an overflow mechanism.

### What to reason about
- What is the promoted operand type?
- What is its width?
- Is the shift count validated?
- Is the value signed or unsigned?
- Is the result representable in the result type?
- Does the operation encode a field, scale a number, or perform arithmetic?

Use unsigned types for bit-level transformations and validate variable shift counts.

## Embedded implications
Shifts implement register fields, masks, fixed-point scaling, serialization, CRCs, and protocol parsing. Hardware often defines exact 8/16/32-bit widths, so accidental promotion to `int` can produce unexpected intermediate behavior.

### Firmware review angle
Keep field width explicit and avoid expressions whose correctness depends on the target's `int` width. For generated register code, validate shift positions against the silicon specification.

## Edge cases and failure modes
- Shift by the type width or greater.
- Negative shift count.
- Left shift of a signed value into an invalid range.
- Unexpected integer promotion of `uint8_t`/`uint16_t`.
- Right shift of a negative signed value assumed to be logical.

## Example pattern
```c
uint32_t field = ((uint32_t)value & 0x1FU) << 8;
```
The cast establishes a 32-bit unsigned left operand before the shift.

## Verification / debugging
Test shift counts 0, 1, width-1, width, and invalid negative values. Enable compiler warnings and use UBSan on host builds where suitable. Inspect generated instructions for timing-critical shifts.

Staff-level questions: What exact width is the operation intended to represent? Could a promotion change the shift domain? Is the shift arithmetic or representation logic?

## Staff-level takeaway
Shift correctness is a **type-and-width problem** before it is a bit-manipulation problem. Establish the operand type, width, and valid count before reasoning about the resulting bit pattern.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
