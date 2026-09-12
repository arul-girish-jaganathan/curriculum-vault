# 05: Explicit Field Encoding

## Definition
Explicit field encoding is the architectural practice of serializing and deserializing protocol messages field by field into a flat, platform-independent byte stream using explicit bit-shifting, fixed-width types, and defined wire offsets.

## Scope and Boundaries
- **Covers:** Field-by-field encoding, wire protocol design, stateless parsers, and explicit offset management.
- **Does not cover:** Raw structure dumping ([[04_Structure_serialization_pitfalls]]), socket API integration ([[02_Byte_order_conversion]]), or automatic schema compilers.

## Why Does It Exist
To achieve absolute portability and robustness across heterogeneous systems, software must decouple in-memory object representations from wire-format protocols:
- **Padding Elimination:** Field encoding packs data contiguously into byte arrays, eliminating compiler padding holes entirely.
- **Endianness Control:** Every integer field is explicitly converted to network byte order during serialization and host order during deserialization.
- **Type Safety:** Maps wire data directly into standard fixed-width types (`uint8_t`, `uint16_t`, `uint32_t`).

## Mechanism and Language Rules
- **Encoding API Design:**
  - `size_t encode_packet(uint8_t *buf, size_t buflen, const app_packet_t *pkt);`
  - `bool decode_packet(app_packet_t *pkt, const uint8_t *buf, size_t buflen);`
- **Bounds Checking:** Every serialization and deserialization function must validate buffer lengths strictly to prevent buffer overflows.

## Examples
```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    uint32_t sensor_id;
    uint16_t reading;
    uint8_t  status_flags;
} sensor_msg_t;

/* Explicit encoding into a flat wire buffer */
size_t msg_serialize(uint8_t *buf, size_t cap, const sensor_msg_t *msg) 
{
    if (cap < 7) return 0; /* Required wire size: 4 + 2 + 1 = 7 bytes */

    /* Sensor ID (Big-Endian 32-bit) */
    buf[0] = (msg->sensor_id >> 24) & 0xFF;
    buf[1] = (msg->sensor_id >> 16) & 0xFF;
    buf[2] = (msg->sensor_id >> 8)  & 0xFF;
    buf[3] =  msg->sensor_id        & 0xFF;

    /* Reading (Big-Endian 16-bit) */
    buf[4] = (msg->reading >> 8)    & 0xFF;
    buf[5] =  msg->reading          & 0xFF;

    /* Flags (8-bit) */
    buf[6] =  msg->status_flags;

    return 7;
}

/* Explicit decoding with strict bounds validation */
bool msg_deserialize(sensor_msg_t *msg, const uint8_t *buf, size_t len) 
{
    if (len < 7) return false;

    msg->sensor_id = ((uint32_t)buf[0] << 24) |
                     ((uint32_t)buf[1] << 16) |
                     ((uint32_t)buf[2] << 8)  |
                     (uint32_t)buf[3];

    msg->reading = ((uint16_t)buf[4] << 8) |
                   (uint16_t)buf[5];

    msg->status_flags = buf[6];

    return true;
}

int main(void) 
{
    uint8_t wire[16];
    sensor_msg_t out = { .sensor_id = 0xABCDEF01, .reading = 1024, .status_flags = 0x03 };

    size_t written = msg_serialize(wire, sizeof(wire), &out);
    printf("Explicitly serialized %zu bytes.
", written);

    sensor_msg_t in;
    if (msg_deserialize(&in, wire, written)) {
        printf("Deserialized: ID=0x%08X, Reading=%u, Flags=0x%02X
", in.sensor_id, in.reading, in.status_flags);
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Accessing input byte buffers beyond `len` bounds during deserialization.

## Edge Cases and Failure Modes
- **Truncated Packets:** Receiving a partial packet stream where `len < expected_size` must be detected and rejected gracefully rather than causing memory faults.

## Embedded Implications
- **Zero-Copy Parsers:** For high-throughput embedded packet processing, explicit decoding fills internal context structs safely from DMA receive rings.

## Firmware Review Angle
- **Audit Bounds Checks:** Ensure every deserialization function verifies buffer length parameters before reading array indices.

## Compiler, ABI, and Toolchain Implications
- **Independent Layout:** Explicit encoding guarantees that compiled binaries remain interoperable across different compilers, optimization flags, and CPU architectures.

## Performance, Memory, Timing, and Power
- **Deterministic Cost:** Fixed-size bit-shifting serialization executes in deterministic, bounded CPU cycles with zero dynamic memory allocation.

## Verification / Debugging
- **Fuzz Testing:** Feed malformed, truncated, and oversized byte streams into `msg_deserialize` to verify parser robustness against memory exploits.

## Safety, Security, and Reliability
- **Defensive Engineering:** Bulletproof input validation protects systems from malformed wire inputs and buffer overflow attacks.

## Trade-offs and Alternatives
- **Explicit Encoding vs. Schema Frameworks:** Explicit encoding requires writing boilerplate packing/unpacking code, but incurs zero runtime overhead and requires no external code generators.

## Staff-Level Takeaway
Explicit field encoding is the hallmark of professional systems engineering. By serializing data field-by-field into flat byte arrays, you eliminate padding bugs, endianness mismatches, and platform dependencies entirely.

## Related Concepts
- [[00_Chapter_Index]]
- [[03_Integer_serialization]]
- [[04_Structure_serialization_pitfalls]]
- [[06_Bit_level_protocols]]
