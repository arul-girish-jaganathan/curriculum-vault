# 09: Serialization Hazards

## Definition
Serialization hazards refer to the portability bugs, data corruption issues, and security vulnerabilities that arise when C object representations (raw structs, integers, floats) are directly serialized to disk, network sockets, or shared memory without accounting for endianness, padding bytes, type widths, and alignment differences.

## Scope and Boundaries
- **Covers:** Endianness mismatches, padding byte pollution, type width divergence (`long`, `int`), and wire protocol design.
- **Does not cover:** In-memory object representations ([[04_Object_representation]]) or dynamic memory allocation.

## Why Does It Exist
In-memory object representations are optimized for CPU execution speed, not network portability:
- **Endianness Divergence:** Little-endian architectures (x86_64, ARM) store least significant bytes first; big-endian architectures (network byte order, certain mainframes) store most significant bytes first.
- **Padding Hazards:** Struct padding bytes contain uninitialized garbage that corrupts wire protocols if raw structs are dumped directly.
- **Type Width Variations:** `long` is 32 bits on Windows 64-bit (`LLP64`) and 64 bits on Linux 64-bit (`LP64`).

## Mechanism and Language Rules
- **Field-by-Field Serialization:** Safe serialization requires packing data field by field into fixed-width types (`uint32_t`, `uint16_t`) and applying explicit endianness conversion (`htonl`, `ntohl`, or manual shifts).
- **No Raw Struct Dumps:** `write(fd, &my_struct, sizeof(my_struct));` is non-portable and hazardous.

## Examples
```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

/* Safe serialization structure */
typedef struct {
    uint32_t message_id;
    uint16_t payload_len;
    uint8_t  flags;
} __attribute__((packed)) wire_header_t;

/* Manual field-by-field serialization to byte buffer */
size_t serialize_header(uint8_t *buf, uint32_t id, uint16_t len, uint8_t flags) 
{
    /* Convert to network byte order (Big Endian) manually or via htons/htonl */
    buf[0] = (id >> 24) & 0xFF;
    buf[1] = (id >> 16) & 0xFF;
    buf[2] = (id >> 8) & 0xFF;
    buf[3] = id & 0xFF;

    buf[4] = (len >> 8) & 0xFF;
    buf[5] = len & 0xFF;

    buf[6] = flags;

    return 7; /* Exact wire size, zero padding holes */
}

int main(void) 
{
    uint8_t wire_buf[16];
    size_t written = serialize_header(wire_buf, 0x12345678, 512, 0x01);
    printf("Serialized %zu bytes to wire buffer.\n", written);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Casting unaligned byte streams directly to multi-byte typed pointers during deserialization.
- **Implementation-Defined:** Native integer sizes and endianness of the host CPU.

## Edge Cases and Failure Modes
- **Cross-Platform Deserialization Failure:** Sending a serialized binary struct generated on a little-endian x86 machine to a big-endian embedded telemetry receiver without byte swapping results in complete data corruption.
- **Information Disclosure:** Raw struct serialization transmitting padding bytes leaks kernel/heap memory contents.

## Embedded Implications
- **Telemetry & CAN Bus:** Embedded systems communicating over CAN bus, UART, or Ethernet must serialize telemetry packets explicitly byte-by-byte to guarantee protocol compliance.

## Firmware Review Angle
- **Ban Raw Struct I/O:** Flag and reject any code writing raw C structures (`fwrite(&s, sizeof(s), 1, fp)`) or reading them from network/file streams. Enforce explicit serialization/deserialization APIs.

## Compiler, ABI, and Toolchain Implications
- **Compiler Extensions:** `#pragma pack` or `__attribute__((packed))` assist in reducing struct size, but explicit serialization remains the only 100% portable solution across divergent architectures.

## Performance, Memory, Timing, and Power
- **Serialization Overhead:** Field-by-field serialization incurs minor CPU overhead for shifts and masks, but guarantees absolute cross-platform reliability and security.

## Verification / Debugging
- **Protocol Fuzzing:** Test deserialization routines with malformed byte streams to ensure out-of-bounds lengths and invalid headers are handled gracefully.

## Safety, Security, and Reliability
- **Security Vulnerabilities:** Improper deserialization is a primary vector for buffer overflows, integer overflows, and remote code execution exploits in networked firmware.

## Trade-offs and Alternatives
- **Manual Serialization vs. Serialization Libraries:** Manual serialization is lightweight and zero-dependency; schema-based serialization libraries (Protocol Buffers, FlatBuffers) offer robust evolution and safety at the cost of code footprint.

## Staff-Level Takeaway
Never serialize raw in-memory C structures directly to persistent storage or network links. In-memory representations are internal implementation details of the compiler and host CPU; wire protocols require explicit, platform-independent field-by-field serialization.

## Related Concepts
- [[00_Chapter_Index]]
- [[04_Object_representation]]
- [[06_Padding_bytes]]
- [[12_ABI_and_packing]]
