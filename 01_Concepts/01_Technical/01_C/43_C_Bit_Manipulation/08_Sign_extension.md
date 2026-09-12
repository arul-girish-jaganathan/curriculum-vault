# Sign extension

> Canonical C topic note — Chapter 43. Sign extension preserves a signed value's mathematical value when representing it in a wider signed type by propagating the sign bit.

## Definition
A signed `N`-bit value is sign-extended to a wider width by copying its sign bit into the newly added high bits. In C, the safe conceptual operation is conversion from a signed type to a wider signed type when the destination can represent every source value. Raw bit-field extraction requires more care because the extracted field may initially be unsigned.

## Mechanism and language rules
Integer promotions and conversions determine the actual C value; they are not merely bit-copy operations. If a small signed integer is promoted to `int`, the result preserves its value. Right-shifting a negative signed integer, however, is implementation-defined, so do not use it as a portable sign-extension primitive without an explicit contract.

### What to reason about
- What is the source width and signedness?
- Is the destination wide enough for every value?
- Is the value a mathematical signed integer or merely a packed bit field?
- Does integer promotion already perform the required extension?

## Embedded implications
Sign extension matters when decoding signed sensor values, instruction encodings, ADC fields, protocol fields, and hardware registers narrower than the CPU word. Incorrect extension can turn `-1` into a large positive value and break control limits.

### Firmware review angle
Use explicit masks and casts at representation boundaries. For a signed field extracted from a packet, first isolate the field, then convert according to a documented signed representation rather than relying on implementation-specific shifts.

## Edge cases and failure modes
- Converting an unsigned field to a signed type when the value is not representable.
- Assuming right shift of a negative value is portable sign extension.
- Forgetting integer promotions in expressions involving `int8_t`/`uint8_t`.
- Confusing two's-complement bit patterns with the complete C portability model.

## Example pattern
```c
int32_t widen(int16_t x)
{
    return (int32_t)x;
}
```
This preserves the value because every `int16_t` value is representable in `int32_t` on implementations providing those exact widths.

For a 12-bit signed protocol field, the representation contract should explicitly define how the sign bit maps to the mathematical range before conversion.

## Verification / debugging
Test zero, positive maximum, negative one, most-negative value, and field boundary patterns. Compare decoded values against a reference implementation and inspect casts/conversions with compiler warnings enabled.

## Staff-level takeaway
Separate **value conversion** from **bit-pattern reconstruction**. Let C's defined integer conversions perform sign extension where appropriate, and make packed-field signedness explicit at the protocol/hardware boundary.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
