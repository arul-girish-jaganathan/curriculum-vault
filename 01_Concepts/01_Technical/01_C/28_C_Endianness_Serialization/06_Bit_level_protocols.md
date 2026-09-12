# 06: Bit-Level Protocols

## Definition
Bit-level protocols involve packing multiple logical fields into individual bits or sub-byte bit ranges within a byte stream or hardware register. In C, this is implemented either using standard bit-fields (`struct` bitfields) or explicit bitwise masking and shifting operations.

## Scope and Boundaries
- **Covers:** Bit-packing, bitfields, bitwise masks, shifts, and sub-byte protocol layout.
- **Does not cover:** Full byte integer serialization ([[03_Integer_serialization]]) or floating-point encodings ([[07_Floating_serialization]]).

## Why Does It Exist
Bandwidth-constrained communication links (CAN bus, RF telemetry, sensor registers, network headers) frequently pack data into sub-byte fields to conserve bits:
- **Bit Conservation:** Representing boolean flags, 3-bit mode selectors, or 12-bit analog readings without wasting entire bytes.
- **Hardware Register Mappings:** Microcontroller peripheral control registers use precise bit layouts.

## Mechanism and Language Rules
- **Bit-Field Portability Trap:** C standard bit-fields (`unsigned int field : 3;`) have **implementation-defined** layout ordering (left-to-right vs. right-to-left bit allocation) and padding rules, making them non-portable across different compilers for wire protocols.
- **Bitwise Masking Alternative:** Professional systems programmers avoid C bit-fields for wire protocols, using explicit bitwise shifts and masks (`&`, `|`, `<<`, `>>`) to guarantee cross-compiler determinism.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

/* 
 * Packing 3 fields into a 16-bit word:
 * Bits [15:12] : Mode (4 bits)
 * Bits [11:1]  : Value (11 bits)
 * Bit  [0]     : Enable Flag (1 bit)
 */
uint16_t pack_control_word(uint8_t mode, uint16_t value, uint8_t enable) 
{
    uint16_t word = 0;
    word |= ((uint16_t)(mode & 0x0F) << 12);
    word |= ((uint16_t)(value & 0x7FF) << 1);
    word |=  ((uint16_t)(enable & 0x01));
    return word;
}

void unpack_control_word(uint16_t word, uint8_t *mode, uint16_t *value, uint8_t *enable) 
{
    *mode   = (uint8_t)((word >> 12) & 0x0F);
    *value  = (uint16_t)((word >> 1)  & 0x7FF);
    *enable = (uint8_t)(word          & 0x01);
}

int main(void) 
{
    uint16_t encoded = pack_control_word(0x0A, 512, 1);
    printf("Packed 16-bit word: 0x%04X
", encoded);

    uint8_t m;
    uint16_t v;
    uint8_t e;
    unpack_control_word(encoded, &m, &v, &e);
    printf("Unpacked: Mode=0x%X, Value=%u, Enable=%u
", m, v, e);

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** C standard bit-field memory layout ordering is completely implementation-defined. Never use struct bit-fields for network wire protocols.
- **Undefined Behavior:** Shifting by amounts greater than or equal to the width of the operand type (e.g., shifting a `uint32_t` by 32 or more).

## Edge Cases and Failure Modes
- **Sign Extension in Shifts:** Right-shifting a signed integer can propagate sign bits unpredictably. Always perform bit-level protocol extraction using unsigned types (`uint16_t`, `uint32_t`).

## Embedded Implications
- **Hardware Register Access:** Using explicit bitwise masks (`REG |= (1 << 5)`) is standard practice for configuring embedded microcontroller peripherals safely.

## Firmware Review Angle
- **Ban Struct Bitfields for Wire Protocols:** Flag any use of `struct` bitfields in network packet definitions due to cross-compiler layout divergence; enforce explicit bitwise masking.

## Compiler, ABI, and Toolchain Implications
- **Bitwise Instruction Optimization:** Compilers optimize bitmasking and shifting operations into hardware bit-test and bit-clear instructions (`bt`, `bclr`, `ands`).

## Performance, Memory, Timing, and Power
- **Efficiency:** Bitwise packing achieves maximum protocol compactness with zero dynamic memory overhead.

## Verification / Debugging
- **Unit Testing:** Validate bit-packing routines against boundary mask values (`0x0000`, `0xFFFF`) to ensure zero bit overlapping.

## Safety, Security, and Reliability
- **Deterministic Encoding:** Explicit bitwise masking guarantees identical packet bit patterns across all compiler toolchains and target architectures.

## Trade-offs and Alternatives
- **Bitwise Shifts vs. C Bitfields:** Bitwise shifts provide 100% portable, deterministic control over wire layout; C bitfields offer clean syntax but are non-portable across compilers.

## Staff-Level Takeaway
Never use C struct bit-fields for wire protocols or persistent storage formats because their bit allocation order is implementation-defined. Always implement sub-byte bit-level protocols using explicit bitwise shifts and masks.

## Related Concepts
- [[00_Chapter_Index]]
- [[03_Integer_serialization]]
- [[05_Explicit_field_encoding]]
- [[12_Portable_serialization_helpers]]
