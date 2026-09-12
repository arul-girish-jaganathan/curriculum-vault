# 10: Checksums and Framing

## Definition
Checksums and framing represent the mechanisms used to delimit packet boundaries in a continuous byte stream (framing) and verify data integrity against transmission errors, bit flips, and corruption (checksums/CRCs).

## Scope and Boundaries
- **Covers:** Packet framing markers, SLIP/COBS framing, CRC16/CRC32 checksum verification, and error detection.
- **Does not cover:** Cryptographic signatures (HMAC/SHA) or error-correcting codes (ECC).

## Why Does It Exist
Raw serial streams (UART, TCP byte streams) lack built-in message boundaries and error detection:
- **Packet Framing:** Without explicit start/end markers or length headers, a receiver cannot determine where one packet ends and the next begins in a continuous byte stream.
- **Error Detection:** Electromagnetic interference and transmission noise corrupt bits; checksums and cyclic redundancy checks (CRCs) allow receivers to detect corrupted packets and drop them instantly.

## Mechanism and Language Rules
- **Framing Protocols:** Using SLIP (Serial Line Internet Protocol) escape characters or COBS (Consistent Overhead Byte Stuffing) to frame binary packets within raw byte streams.
- **CRC Calculation:** Running CRC16 or CRC32 algorithms over the serialized payload and appending the checksum to the packet trailer.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

/* Simple Fletcher-16 checksum implementation */
uint16_t calculate_fletcher16(const uint8_t *data, size_t count) 
{
    uint16_t sum1 = 0;
    uint16_t sum2 = 0;

    for (size_t index = 0; index < count; ++index) {
        sum1 = (sum1 + data[index]) % 255;
        sum2 = (sum2 + sum1) % 255;
    }

    return (sum2 << 8) | sum1;
}

int main(void) 
{
    uint8_t packet_payload[] = { 0x01, 0x02, 0x03, 0x04, 0x05 };
    uint16_t checksum = calculate_fletcher16(packet_payload, sizeof(packet_payload));

    printf("Calculated Fletcher-16 Checksum: 0x%04X\n", checksum);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Accessing payload buffers beyond calculated framing lengths during checksum verification.

## Edge Cases and Failure Modes
- **Frame Synchronization Loss:** If noise corrupts framing delimiters, the receiver loses synchronization and drops subsequent valid packets until re-sync occurs.

## Embedded Implications
- **UART / SPI Streaming:** Microcontroller firmware receiving sensor data over UART streams must use robust framing and CRC validation to reject corrupted bytes caused by electrical interference.

## Firmware Review Angle
- **Mandatory CRC Validation:** Ensure every incoming packet is validated against its appended CRC before processing payload contents.

## Compiler, ABI, and Toolchain Implications
- **Lookup Table Optimization:** CRC calculations are optimized using precomputed lookup tables (e.g., 256-entry CRC32 tables) placed in read-only ROM (`const`) to maximize execution speed.

## Performance, Memory, Timing, and Power
- **CPU Cost:** CRC computation requires iterating over payload bytes; lookup-table implementations achieve high throughput suitable for high-speed serial links.

## Verification / Debugging
- **Fault Injection:** Test framing and checksum parsers by deliberately injecting bit flips and truncated bytes into test packet streams.

## Safety, Security, and Reliability
- **Data Integrity:** Guarantees that corrupted or maliciously modified packets are rejected instantly before reaching critical control logic.

## Trade-offs and Alternatives
- **Checksum vs. CRC vs. Cryptographic Hash:** Checksums (Fletcher/Sum) detect simple errors cheaply; CRCs detect burst errors efficiently; cryptographic hashes (SHA-256) provide security against tampering at high CPU cost.

## Staff-Level Takeaway
Never trust raw serial or network byte streams without packet framing and robust CRC/checksum verification. Integrity validation is the final defense against transmission corruption.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_Explicit_field_encoding]]
- [[09_Versioned_wire_formats]]
