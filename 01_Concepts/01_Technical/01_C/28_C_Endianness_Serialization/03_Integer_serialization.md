# 03: Integer Serialization

## Definition
Integer serialization is the process of converting multi-byte integer values into an ordered stream of individual bytes (and vice versa) for storage or transmission, independent of host memory layout, compiler padding, or CPU endianness.

## Scope and Boundaries
- **Covers:** Bit-shifting packing/unpacking, fixed-width byte streams, endian-neutral serialization, and overflow prevention.
- **Does not cover:** Structure padding ([[04_Structure_serialization_pitfalls]]), floating-point serialization ([[07_Floating_serialization]]), or socket API wrappers ([[02_Byte_order_conversion]]).

## Why Does It Exist
Relying on direct pointer casts or socket wrappers is insufficient for complex file formats or custom binary streams:
- **Endian Independence:** Explicit byte shifting guarantees identical wire output whether executed on x86, ARM, or big-endian mainframes.
- **Alignment Safety:** Byte-by-byte serialization completely bypasses hardware alignment restrictions ([[../27_C_Alignment_Object_Representation/01_Alignment_requirements]]), preventing unaligned access faults on constrained microcontrollers.

## Mechanism and Language Rules
- **Packing (Serialization):** Extract bytes using bitwise right-shift and bitwise AND, storing them into an `unsigned char` buffer sequentially.
- **Unpacking (Deserialization):** Reconstruct integers by reading bytes sequentially, shifting them left, and performing bitwise OR combinations.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

/* Serialize a 32-bit unsigned integer into a byte buffer in Big-Endian order */
void serialize_u32_be(uint32_t val, uint8_t *buf) 
{
    buf[0] = (uint8_t)((val >> 24) & 0xFF);
    buf[1] = (uint8_t)((val >> 16) & 0xFF);
    buf[2] = (uint8_t)((val >> 8)  & 0xFF);
    buf[3] = (uint8_t)(val         & 0xFF);
}

/* Deserialize a 32-bit unsigned integer from a Big-Endian byte buffer */
uint32_t deserialize_u32_be(const uint8_t *buf) 
{
    return ((uint32_t)buf[0] << 24) |
           ((uint32_t)buf[1] << 16) |
           ((uint32_t)buf[2] << 8)  |
           (uint32_t)buf[3];
}

int main(void) 
{
    uint8_t buffer[4];
    uint32_t original = 0xDEADBEEF;

    serialize_u32_be(original, buffer);
    uint32_t restored = deserialize_u32_be(buffer);

    printf("Original: 0x%08X -> Restored: 0x%08X\n", original, restored);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Left-shifting signed integers into sign bits or causing signed overflow during serialization arithmetic. Always perform serialization using `uint32_t` or `uint64_t`.

## Edge Cases and Failure Modes
- **Buffer Overflow:** Writing past the end of the destination byte buffer if buffer length validation is omitted.

## Embedded Implications
- **Protocol Parsers:** Essential for parsing custom sensor data packets over SPI/I2C where packet structures are unaligned and endianness must be strictly enforced.

## Firmware Review Angle
- **Audit Shift Operations:** Ensure all shift operands are cast to unsigned types (`uint32_t`, `uint64_t`) to prevent arithmetic sign extension bugs.

## Compiler, ABI, and Toolchain Implications
- **Optimization of Shifts:** Compilers optimize manual shift-and-OR byte packing into efficient load/store and byte-swapping machine instructions.

## Performance, Memory, Timing, and Power
- **Efficiency:** Manual bit-shifting incurs minimal CPU overhead while guaranteeing 100% portability and alignment safety.

## Verification / Debugging
- **Unit Testing:** Write round-trip unit tests covering boundary values (`0x00000000`, `0xFFFFFFFF`, `0x7FFFFFFF`) to verify serialization correctness.

## Safety, Security, and Reliability
- **Robustness:** Eliminates platform-dependent serialization discrepancies, ensuring data persistence and network resilience.

## Trade-offs and Alternatives
- **Bit-Shifting vs. Cast-and-Swap:** Bit-shifting is 100% safe against alignment faults and endianness bugs; cast-and-swap relies on host alignment assumptions and requires careful handling.

## Staff-Level Takeaway
Explicit bit-shifting into byte arrays is the most robust, portable, and alignment-safe method for integer serialization in C. Never compromise integer serialization with raw pointer casts.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_Byte_order_conversion]]
- [[04_Structure_serialization_pitfalls]]
- [[12_Portable_serialization_helpers]]
