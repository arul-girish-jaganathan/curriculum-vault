# 07: Protocol Fields

## Definition
Protocol fields represent discrete binary elements inside over-the-wire network packets, bus frames (CAN, SPI, I2C), or telemetry messages. Using C bit fields to map protocol headers directly onto wire buffers is a well-known anti-pattern in systems programming due to compiler-dependent bit-allocation order and endianness divergences.

## Scope and Boundaries
Covers: Network byte order, CAN bus frames, telemetry packet serialization, cross-platform wire incompatibilities, and bit-field failure modes.
Does not cover: Higher-level protocol state machines or socket APIs.

## Why Does It Exist
Software engineers coming from application development often assume that declaring a struct matching the RFC or ICD bit-field table allows zero-copy casting of incoming packet buffers directly into structured data.

## Mechanism and Language Rules
1. **No Wire Guarantees:** ISO C makes zero guarantees that a bit field declared in C will match the physical bit layout of an external specification.
2. **Double Inversion Hazard:** Wire protocols typically specify Network Byte Order (Big-Endian) with bits numbered from MSB (Bit 7) to LSB (Bit 0). Little-endian microcontrollers with LSB-to-MSB compiler packing invert both the byte order AND the internal bit order.
3. **Compiler Divergence:** Compiling the identical protocol struct with two different toolchains (e.g., GCC on Linux vs. IAR on an MCU) can produce incompatible wire representations.

## Examples
```c
#include <stdint.h>
#include <string.h>
#include <assert.h>

/* FRAGILE ANTI-PATTERN: Protocol mapped via Bit Fields */
struct FragileIpv4Header {
#if defined(LITTLE_ENDIAN_BITFIELD)
    uint8_t ihl     : 4;
    uint8_t version : 4;
#elif defined(BIG_ENDIAN_BITFIELD)
    uint8_t version : 4;
    uint8_t ihl     : 4;
#else
#error "Undefined bitfield order!"
#endif
    uint8_t tos;
    uint16_t total_length;
};

/* ROBUST PATTERN: Explicit Serialization via Byte Math */
struct RobustIpv4Header {
    uint8_t  version;
    uint8_t  ihl;
    uint8_t  tos;
    uint16_t total_length;
};

static void deserialize_ipv4(const uint8_t *buf, struct RobustIpv4Header *hdr) {
    /* Explicit, endian-safe, compiler-independent extraction */
    hdr->version      = (buf[0] >> 4) & 0x0F;
    hdr->ihl          = buf[0] & 0x0F;
    hdr->tos          = buf[1];
    hdr->total_length = ((uint16_t)buf[2] << 8) | (uint16_t)buf[3];
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Casting a raw network byte stream pointer (`uint8_t *`) to a struct bit-field pointer (`struct FragileIpv4Header *`) violates strict aliasing and alignment rules, invoking Undefined Behavior.

## Edge Cases and Failure Modes
- **CAN Bus DLC Corruption:** Mapping a CAN identifier and payload via bit fields results in swapped priority IDs and inverted payloads when communicating between nodes with different CPU architectures.
- **Compiler Optimization Breakage:** The compiler may reorder or combine adjacent bit-field reads, causing race conditions if the buffer is written via DMA concurrently.

## Embedded Implications
- **Zero-Copy Serialization Illusion:** The apparent performance gain of zero-copy struct casting is offset by the risk of corrupted communication packets and hardware bus faults.

## Firmware Review Angle
- Strictly reject any pull request that defines wire protocols, telemetry packets, or file formats using C bit fields.
- Enforce explicit serialization and deserialization functions (`pack()` and `unpack()`) that use shift and mask operations on standard integer types.

## Compiler, ABI, and Toolchain Implications
- Different versions of the GCC compiler have historically changed bit-field packing rules on ARM targets (e.g., transitions between AAPCS and legacy APCS).

## Performance, Memory, Timing, and Power
- Manual bit unpacking compiles into fast, pipeline-friendly instructions (`LDRB`, `LSR`, `AND`) that are easily unrolled and optimized by the compiler without memory aliasing penalties.

## Verification / Debugging
- Send known test vectors (golden packets) across the communication interface and verify byte-for-byte equality across different compilation targets.

## Safety, Security, and Reliability
- Heartbleed-style vulnerabilities and buffer over-reads can occur when corrupted bit fields misreport payload lengths in network headers.

## Trade-offs and Alternatives
- **Bit Fields vs. Serialization Buffers:** Writing `serialize()` and `deserialize()` functions requires slightly more code up front, but provides 100% deterministic, portable, and secure communication.

## Staff-Level Takeaway
Never use C bit fields for over-the-wire protocols, bus frames, or persistent file storage. Bit fields represent in-memory abstractions, not physical wire formats. Always serialize and deserialize external packets using explicit shifts and masks on byte buffers.

## Related Concepts
- `03_Allocation_order`
- `06_Packed_structs`
- `09_Mask_and_shift_alternatives`
