# 03: Allocation Order

## Definition
Allocation order refers to the spatial direction and placement policy used by a C compiler when assigning consecutive bit fields into an underlying machine storage unit. ISO C leaves the allocation order (least-significant bit first versus most-significant bit first) completely implementation-defined.

## Scope and Boundaries
Covers: LSB-to-MSB vs. MSB-to-LSB allocation, byte endianness interaction, cross-architecture behavioral differences, and bitfield layout flipping.
Does not cover: Byte-level memory endianness across separate variables.

## Why Does It Exist
Different processor architectures and toolchains prioritize bit positioning differently based on native instruction set architectures. Little-endian processors frequently pack bits starting from the least significant bit, whereas big-endian processors (or networking stacks) often pack from the most significant bit.

## Mechanism and Language Rules
1. **ISO C Ambiguity (§6.7.2.1):** "The order of allocation of bit-fields within a unit (high-order to low-order or low-order to high-order) is implementation-defined."
2. **Independence from Byte Endianness:** Bit-field allocation order is conceptually separate from byte endianness, although compilers generally align them (e.g., little-endian CPUs usually use LSB-to-MSB allocation).
3. **Storage Unit Packing:** When bit fields fit within a single unit, the compiler packs them consecutively. If a bit field does not fit, whether it spills or begins at the next unit is implementation-defined.

## Examples
```c
#include <stdint.h>
#include <stdio.h>

struct Flags {
    unsigned int b0 : 1; /* First declared */
    unsigned int b1 : 1;
    unsigned int b2 : 1;
    unsigned int b3 : 1;
};

/* 
 * On GCC Little-Endian (x86_64, ARM Cortex-M AAPCS):
 * Memory byte representation:
 *   Bit 0: b0
 *   Bit 1: b1
 *   Bit 2: b2
 *   Bit 3: b3
 * 
 * On Big-Endian (PowerPC, SPARC, or MSB-first compilers):
 * Memory byte representation:
 *   Bit 7: b0
 *   Bit 6: b1
 *   Bit 5: b2
 *   Bit 4: b3
 */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Bit Ordering:** Code that assumes `b0` is the least-significant bit (bit 0) exhibits implementation-defined behavior and will fail when compiled on a big-endian or MSB-first toolchain.
- **Portability:** Never assume identical bit-field layout between different compilers (e.g., GCC vs. IAR vs. MSVC) even on the same physical CPU.

## Edge Cases and Failure Modes
- **Protocol Deserialization Inversion:** Sending a struct with bit fields over an SPI/CAN bus causes the receiving device to read the fields in reverse order if compiler allocation conventions diverge.
- **Union Inspection Inversion:** Writing a bit field and reading back the raw byte through a union reveals completely inverted bit positions across different architectures.

## Embedded Implications
- **Hardware Register Mapping Breakdown:** Hardware MMIO registers have immutable physical bit definitions (e.g., Bit 0 is ALWAYS `ENABLE`). Using bit fields to map these registers will fail if the compiler packs from MSB to LSB.
- **Dual-Header Workarounds:** Many legacy stacks (e.g., Linux network headers) define dual layouts with `#if defined(__LITTLE_ENDIAN_BITFIELD)` and `#elif defined(__BIG_ENDIAN_BITFIELD)`. This is notoriously fragile and error-prone.

## Firmware Review Angle
- Search for any bit-field struct that is cast directly to or from a byte array or peripheral address.
- Verify that conditional compilation macros (`__LITTLE_ENDIAN__`) are not being used to paper over non-portable bit-field designs.

## Compiler, ABI, and Toolchain Implications
- ARM AAPCS mandates that bit fields are allocated from the least-significant bit towards the most-significant bit in little-endian mode.
- Certain automotive compilers provide proprietary pragmas (e.g., `#pragma bit_order(msb)`) to alter standard behavior.

## Performance, Memory, Timing, and Power
- Allocation order itself has no performance penalty, but runtime swapping of inverted bit fields introduces significant cycle latency and code bloat.

## Verification / Debugging
- Write a unit test asserting raw byte patterns:
  ```c
  struct Flags f = { .b0 = 1, .b1 = 0, .b2 = 0, .b3 = 0 };
  uint8_t raw = *(uint8_t *)&f;
  assert(raw == 0x01); /* Will fail on MSB-first compilers! */
  ```

## Safety, Security, and Reliability
- Inverting command bits (e.g., swapping `ARM_DISARM` with `IGNITION`) due to compiler bit-allocation differences can lead to catastrophic physical system failures.

## Trade-offs and Alternatives
- **Bit Fields vs. Explicit Shifts:** Explicit bitwise shifts (`(val >> 2) & 0x01`) guarantee byte-exact, endian-independent bit extraction regardless of compiler allocation order.

## Staff-Level Takeaway
Never rely on the compiler's bit-field allocation order for external interfaces. Because ISO C explicitly delegates allocation direction to the implementation, bit fields are fundamentally non-portable across architectures and compilers.

## Related Concepts
- `01_Bit_field_declaration`
- `05_Implementation_defined_layout`
- `09_Mask_and_shift_alternatives`
