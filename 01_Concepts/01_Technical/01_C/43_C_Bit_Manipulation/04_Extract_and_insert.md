# Extract and insert

> Canonical C topic note — Chapter 43. Bit-field extraction and insertion isolate a field at a specified position while preserving unrelated bits. Correctness depends on field width, position, unsigned arithmetic, and range validation.

## Definition
To extract a field, shift it down and mask it. To insert, validate or mask the source value, shift it into position, and combine it with the destination after clearing the old field.

## Mechanism and language rules
A common extraction is `(value >> shift) & mask`. For insertion, `((value & field_mask) << shift)` must be formed in an adequately wide unsigned type. The shift count and source range must be valid before evaluation.

### What to reason about
- What are field width and least-significant-bit position?
- Does `field_mask` describe pre-shift or positioned bits?
- Is the source value truncated intentionally?
- Can shifting overflow the promoted type?
- Are reserved bits protected?
- Is the destination shared or MMIO?

Parameterize helpers carefully; a macro that evaluates an argument more than once can introduce bugs.

## Embedded implications
Register fields and protocol headers frequently require extraction/insertion. Explicit helpers avoid implementation-defined bit-field layout and can make register ownership visible.

### Firmware review angle
Define field constants from the hardware specification and reject values outside documented ranges when truncation would hide a caller bug. For write registers, clear only fields software owns.

## Edge cases and failure modes
- Field width plus shift exceeds the underlying width.
- Signed value is shifted.
- Source is silently truncated when it should be rejected.
- Clearing a field also modifies reserved bits.
- Mask and shift constants describe different widths.

## Example pattern
```c
#define FIELD_MASK 0x1FU
#define FIELD_SHIFT 8U

static uint32_t get_field(uint32_t reg)
{
    return (reg >> FIELD_SHIFT) & FIELD_MASK;
}

static uint32_t put_field(uint32_t reg, uint32_t value)
{
    reg &= ~(FIELD_MASK << FIELD_SHIFT);
    reg |= (value & FIELD_MASK) << FIELD_SHIFT;
    return reg;
}
```
The caller must ensure the constants describe a valid field within 32 bits.

## Verification / debugging
Test zero, maximum field value, one-above-maximum, all-one destination, and adjacent fields. Use compile-time checks or static assertions for field position/width relationships.

Staff-level questions: Should invalid source values be rejected rather than truncated? Who owns neighboring bits? Is this an in-memory word or a hardware register with special write semantics?

## Staff-level takeaway
Field manipulation should make **position, width, range, and ownership** explicit. A compact expression is not inherently safe if its constants permit invalid shifts or unintended neighboring-bit updates.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
