# Bitfield-free protocol code

> Canonical C topic note — Chapter 43. Protocol representations should normally be encoded explicitly as bytes and masks rather than relying on implementation-dependent C bit-field layout.

## Definition
C bit-field allocation order, packing, alignment, and related layout properties are implementation-dependent. A wire protocol is an external representation contract, so its byte order and field positions should be explicit.

## Mechanism and language rules
Use `uint8_t` arrays or another precisely specified representation. Extract and insert fields with shifts and masks, and serialize multi-byte integers with explicit endian rules. Do not cast an arbitrary packet buffer to a struct and assume that its in-memory layout equals the wire format.

### What to reason about
- Byte order and bit numbering.
- Field width and valid range.
- Alignment and object representation.
- Padding and structure layout.
- Integer promotions.
- Bounds before every read/write.
- Versioning and backward compatibility.

## Embedded implications
Explicit parsing avoids unaligned accesses on strict architectures and makes protocol behavior independent of compiler packing rules. It also lets the parser reject malformed lengths before data reaches allocation, indexing, or hardware control paths.

### Firmware review angle
Separate wire-format code from internal C structures. Centralize endian helpers and validate every field against protocol limits. Treat the wire format as an ABI that must remain stable across firmware releases.

## Edge cases and failure modes
- Struct padding inserts unexpected bytes.
- Bit-field allocation order differs across targets.
- Unaligned pointer casts fault.
- Host endianness is assumed accidentally.
- Integer promotions alter an intermediate shift.
- Malicious length fields cause out-of-bounds access.

## Example pattern
```c
static uint16_t get_be16(const uint8_t p[2])
{
    return ((uint16_t)p[0] << 8) | (uint16_t)p[1];
}

static void put_be16(uint8_t p[2], uint16_t v)
{
    p[0] = (uint8_t)(v >> 8);
    p[1] = (uint8_t)v;
}
```
The wire representation is explicit and contains no packing assumption.

## Verification / debugging
Use golden vectors, round-trip tests, boundary values, malformed lengths, cross-endian tests, and cross-compiler builds. Fuzz parsers with invalid field combinations and truncated packets.

Staff-level questions: What is the external ABI? Can a new compiler or MCU decode old packets? Are every field width and endian rule explicit? Does the parser validate before using untrusted data?

## Staff-level takeaway
Treat protocol data as an **external ABI**. Explicit byte-level serialization makes representation, validation, portability, and evolution visible and testable.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
