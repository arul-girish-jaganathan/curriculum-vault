# Sign extension

> Canonical C topic note — Chapter 43. Sign extension preserves a signed value's numerical meaning when representing it in a wider signed type by extending the sign bit into the newly added high bits.

## Definition
For a two's-complement `N`-bit value, a negative value has high bit one; widening it to a larger signed type conceptually fills new high bits with ones. Positive values fill them with zeros. In C, the exact result follows the rules for integer promotions and conversions, not a hand-written assumption about bit patterns.

## Mechanism and language rules
Converting a signed integer to a wider signed integer preserves its value when the destination can represent it. Problems arise when programmers first treat a narrow byte as unsigned, shift it, or convert it through an unintended type.

### What to reason about
- Is the source logically signed or an unsigned bit pattern?
- What is the source width and destination width?
- What integer promotions occur?
- Is the source actually a C signed integer or a serialized field?
- Is the representation assumption explicitly two's complement where required?

For protocol fields, parse the field width explicitly before interpreting its sign.

## Embedded implications
Sign extension appears in ADC values, packed sensor formats, instruction decoding, DSP data, and peripheral registers containing signed subfields. Incorrect extension can turn a negative measurement into a large positive value.

### Firmware review angle
Separate **bit-pattern extraction** from **numeric interpretation**. Extract an unsigned field first, then apply an explicit sign interpretation with a known field width.

## Edge cases and failure modes
- Treating an unsigned byte containing `0xFF` as `-1` without conversion.
- Shifting a signed value without proving the operation is valid.
- Sign-extending from the wrong field width.
- Mixing signed and unsigned arithmetic after extension.

## Example pattern
```c
static int32_t sign_extend12(uint16_t raw)
{
    raw &= 0x0FFFU;
    if ((raw & 0x0800U) != 0U) {
        return (int32_t)raw - 0x1000;
    }
    return (int32_t)raw;
}
```
The arithmetic expresses the signed 12-bit interpretation without relying on a signed shift trick.

## Verification / debugging
Test zero, maximum positive, minimum negative, `-1`, and values around the sign boundary. Compare against a mathematical reference and inspect intermediate types with compiler warnings.

Staff-level questions: Is the input a numeric signed object or a raw bit field? What field width defines the sign bit? Could implicit unsigned conversion change later comparisons?

## Staff-level takeaway
Sign extension is safest when **representation and numeric interpretation are separated**. Extract the exact field width first, then convert it under an explicit signed-value contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
