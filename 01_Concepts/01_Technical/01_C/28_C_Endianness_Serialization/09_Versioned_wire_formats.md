# 09: Versioned Wire Formats

## Definition
Versioned wire formats represent an architectural strategy for designing binary serialization protocols that can evolve over time while maintaining strict backward and forward compatibility between different software versions.

## Scope and Boundaries
- **Covers:** Protocol version headers, TLV (Type-Length-Value) encoding, backward compatibility, and extensible message design.
- **Does not cover:** Static fixed-size serialization ([[05_Explicit_field_encoding]]) or cryptographic signing.

## Why Does It Exist
Software systems evolve; protocol message layouts inevitably change as new features are added:
- **Backward Compatibility:** Newer software versions must be able to parse older packet formats without crashing.
- **Forward Compatibility:** Older software versions must gracefully handle or ignore new fields introduced by newer protocol versions.
- **Graceful Failure:** Rejecting unsupported protocol versions explicitly rather than experiencing undefined memory corruption.

## Mechanism and Language Rules
- **Version Magic Header:** Every binary packet begins with a magic byte sequence and an explicit protocol version number (`uint8_t version`).
- **TLV (Type-Length-Value) Encoding:** Encoding optional fields as Type, Length, and Value triples allows parsers to skip unrecognized fields safely.
- **Fixed Header with Variable Payload:** Placing a fixed-size header containing a total payload length enables parsers to validate message boundaries before extraction.

## Examples
```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define PROTOCOL_MAGIC   0x42530123
#define CURRENT_VERSION  2

typedef struct {
    uint32_t magic;
    uint8_t  version;
    uint16_t payload_len;
} packet_header_t;

bool parse_packet_header(const uint8_t *buf, size_t len, packet_header_t *hdr) 
{
    if (len < 7) return false;

    hdr->magic = ((uint32_t)buf[0] << 24) |
                 ((uint32_t)buf[1] << 16) |
                 ((uint32_t)buf[2] << 8)  |
                 (uint32_t)buf[3];

    if (hdr->magic != PROTOCOL_MAGIC) {
        return false; /* Invalid magic bytes */
    }

    hdr->version = buf[4];
    hdr->payload_len = ((uint16_t)buf[5] << 8) | buf[6];

    if (hdr->version > CURRENT_VERSION) {
        printf("Warning: Packet version %u is newer than supported version %u\n", hdr->version, CURRENT_VERSION);
        /* Depending on policy, can either parse subset or reject */
    }

    return true;
}

int main(void) 
{
    uint8_t mock_wire[] = { 0x42, 0x53, 0x01, 0x23, 0x02, 0x00, 0x10 };
    packet_header_t hdr;

    if (parse_packet_header(mock_wire, sizeof(mock_wire), &hdr)) {
        printf("Successfully parsed v%u packet with payload length %u\n", hdr.version, hdr.payload_len);
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Assuming incoming protocol structures match the latest software version without checking version header fields.

## Edge Cases and Failure Modes
- **Protocol Downgrade Attacks:** Insecure protocol negotiations where an attacker forces communication to fall back to vulnerable legacy wire formats.

## Embedded Implications
- **Firmware Update Payloads:** Over-the-air (OTA) firmware update binary headers require strict versioning and checksum validation to prevent bricking microcontrollers with incompatible images.

## Firmware Review Angle
- **Verify Version Checks:** Ensure every packet parser validates magic numbers and version fields before attempting field extraction.

## Compiler, ABI, and Toolchain Implications
- **Extensible Structs:** Avoid fixed raw structs; use tagged unions and TLV parsers to handle evolving data structures robustly.

## Performance, Memory, Timing, and Power
- **Parsing Overhead:** TLV and version-checking incur minimal parsing overhead while delivering bulletproof system upgradability.

## Verification / Debugging
- **Compatibility Testing:** Test v1 parsers with v2 packets and vice versa to guarantee robust backward and forward compatibility.

## Safety, Security, and Reliability
- **Resilience:** Prevents catastrophic system crashes and memory corruption when disparate software versions communicate over shared networks.

## Trade-offs and Alternatives
- **Fixed Headers vs. TLV Encoding:** Fixed headers are fast and lightweight for strict real-time telemetry; TLV encoding provides maximum extensibility for complex protocols.

## Staff-Level Takeaway
Never design a binary protocol without a magic header and an explicit version field. Versioned wire formats are essential for maintaining backward and forward compatibility across lifecycle updates.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_Explicit_field_encoding]]
- [[10_Checksums_and_framing]]
