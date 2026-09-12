# 06: Packed Structs

## Definition
A packed structure is a structure decorated with a compiler attribute (`__attribute__((packed))` or `#pragma pack(1)`) that removes all internal and trailing padding bytes. When applied to structures containing bit fields, it forces the compiler to pack bit fields tightly across natural storage-unit and alignment boundaries.

## Scope and Boundaries
Covers: Packing attributes, byte-boundary crossing, unaligned memory accesses, bus faults, and compiler code bloat.
Does not cover: Struct packing without bit fields (see `16_C_Struct_Union_Enum/01_Structure_layout`).

## Why Does It Exist
In hardware serialization and raw network framing, data fields are often packed without regard for 16-bit or 32-bit CPU bus alignments. Packing forces the compiler to discard natural alignment rules to produce byte-exact spatial layouts.

## Mechanism and Language Rules
1. **Padding Removal:** The compiler inserts zero alignment padding between fields.
2. **Boundary Collapse:** Bit fields inside packed structs are allowed to cross byte and word boundaries arbitrarily.
3. **Unaligned Access Generation:** The compiler assumes members may reside at unaligned addresses and generates byte-level load/store instruction sequences instead of single-word accesses.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Packed struct with bit fields crossing byte boundaries */
struct __attribute__((packed)) PackedTelemetry {
    uint8_t  id       : 6; /* Bits 0..5 of Byte 0 */
    uint16_t reading  : 10;/* Bits 6..7 of Byte 0 + Bits 0..7 of Byte 1 */
    uint8_t  checksum : 8; /* Byte 2 */
};

static_assert(sizeof(struct PackedTelemetry) == 3, "PackedTelemetry must be exactly 3 bytes");

static uint16_t extract_reading(const struct PackedTelemetry *pkt) {
    /* 
     * Reading pkt->reading requires the compiler to fetch Byte 0 and Byte 1,
     * shift and recombine them across the byte boundary.
     */
    return pkt->reading;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Pointer to Packed Member:** Taking the address of an unaligned member in a packed struct (`uint16_t *p = (uint16_t *)&pkt->reading`) and dereferencing it invokes Undefined Behavior in ISO C.

## Edge Cases and Failure Modes
- **Hardware Bus Fault (HardFault):** On architectures that forbid unaligned memory accesses (e.g., ARM Cortex-M0/M0+, or Cortex-M3/M4 when `UNALIGN_TRP` in the CCR is set), dereferencing unaligned pointers generates a hardware fault.
- **Extreme Instruction Bloat:** Accessing a 10-bit field straddling a byte boundary requires 4 to 8 instructions (load byte 1, load byte 2, shift, mask, or) instead of a single 32-bit `LDR`.

## Embedded Implications
- **Severe Performance Degradation:** High-frequency control loops that repeatedly read/write packed bit fields can experience a 500% execution time penalty compared to naturally aligned accesses.
- **DMA Hazards:** Packed structs cannot be directly targeted by DMA engines that mandate 32-bit word-aligned destination buffers.

## Firmware Review Angle
- Check for `-Waddress-of-packed-member` compiler warnings; never take addresses of members within packed structures.
- Audit the assembly output of time-critical paths that interact with packed bit fields to verify instruction overhead.

## Compiler, ABI, and Toolchain Implications
- GCC and Clang handle packed bit-field spanning efficiently, but MSVC and certain DSP compilers have non-standard rules regarding whether `#pragma pack` applies to bit-field containers.

## Performance, Memory, Timing, and Power
- While packed structs minimize RAM consumption (saving 1-2 bytes per instance), they trade off CPU execution cycles, instruction cache utilization, and power consumption due to multi-instruction read-modify-write sequences.

## Verification / Debugging
- Use compiler warning `-Wpacked` to detect unnecessary or inefficient packing.
- AddressSanitizer (`-fsanitize=alignment`) flags illegal unaligned pointer accesses at runtime.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 1.3: Unaligned pointer dereferencing resulting from packed structs is a direct safety violation.

## Trade-offs and Alternatives
- **Packed Bit Fields vs. Manual Byte Deserialization:** Parsing bytes manually via shifts (`uint16_t val = buf[0] >> 6 | (buf[1] << 2)`) avoids compiler packing bugs, eliminates unaligned access hazards, and maintains full code portability.

## Staff-Level Takeaway
Packed bit fields appear convenient for compact data layouts, but they incur heavy instruction bloat and risk hardware bus faults. Never take the address of a packed member, and avoid packed bit fields in performance-critical control loops.

## Related Concepts
- `05_Implementation_defined_layout`
- `07_Protocol_fields`
- `09_Mask_and_shift_alternatives`
