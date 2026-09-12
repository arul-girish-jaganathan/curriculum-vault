# Bitfield-free protocol code

> Canonical C topic note — Chapter 43. Explicit byte and bit operations are often preferable to C bit-fields when a protocol representation must be stable across compilers, ABIs, architectures, and optimization levels.

## Definition
C bit-field layout, allocation order, packing, and interactions with underlying integer types are implementation-defined or otherwise implementation-dependent. Protocol code should normally define the wire representation independently and encode/decode it explicitly.

## Mechanism and language rules
A protocol encoder should operate on `uint8_t` byte arrays or another explicitly specified representation. Multi-byte integers should be serialized with explicit shifts/masks or dedicated endian conversion routines. Do not cast a packet buffer to a struct and assume its layout equals the wire format.

### What to reason about
- Byte order.
- Bit numbering.
- Field width and valid range.
- Alignment requirements.
- Padding and structure layout.
- Signedness and integer promotion.
- Bounds before every read/write.

## Embedded implications
Explicit serialization avoids unaligned accesses on architectures that prohibit them and avoids compiler padding surprises. It also makes protocol evolution and compatibility easier to review.

### Firmware review angle
Keep wire-format types separate from internal C structures. Validate lengths before parsing and reject impossible field combinations before using them for allocation, indexing, or hardware commands.

## Edge cases and failure modes
- Struct padding inserts unexpected bytes.
- Bit-field allocation order differs across implementations.
- Unaligned casts fault on some MCUs.
- Endianness is assumed from host architecture.
- Integer promotion changes an intermediate shift.
- Malicious length fields cause out-of-bounds parsing.

## Example pattern
```c
static uint16_t get_be16(const uint8_t p[2])
{
    return ((uint16_t)p[0] << 8) | p[1];
}

static void put_be16(uint8_t p[2], uint16_t v)
{
    p[0] = (uint8_t)(v >> 8);
    p[1] = (uint8_t)v;
}
```
The byte order is explicit and no structure packing assumption is involved.

## Verification / debugging
Use golden byte sequences, round-trip tests, boundary values, malformed lengths, and cross-compiler tests. Inspect generated code when parser performance is critical, but never trade away representation correctness for a guessed optimization.

## Staff-level takeaway
Treat the wire format as an **external ABI**. Explicit serialization makes byte order, field boundaries, alignment, and validation visible and portable, whereas packed C bit-fields are usually a poor substitute for a protocol specification.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
