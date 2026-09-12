# 12: Protocol and Register Layouts

## Definition
Protocol and register layouts represent the precise, byte-exact mapping of C data structures directly onto hardware peripheral registers (Memory-Mapped I/O — MMIO) or over-the-wire communication packet frames. This requires mastering structural alignment, compiler packing directives, endianness transformations, and `volatile` qualification.

## Scope and Boundaries
Covers: Struct overlays for MMIO, compiler packing (`__attribute__((packed))`), `#pragma pack`, volatile qualifiers on struct registers, and network endianness transformations.
Does not cover: Operating system socket layers or DMA controller hardware configuration.

## Why Does It Exist
Hardware peripherals and network protocols have rigid byte layouts dictated by silicon designers and RFC specifications. The software must mirror these physical layouts with 100% fidelity without the compiler introducing arbitrary alignment padding or eliding accesses due to optimization.

## Mechanism and Language Rules
1. **Volatile Qualification:** Register structs must be accessed through pointers to `volatile` types to prevent compilers from caching reads or optimizing away writes.
2. **Compiler Packing Directives:** `__attribute__((packed))` (GCC/Clang) or `#pragma pack(push, 1)` (MSVC/cross-compilers) eliminates all internal and trailing padding bytes.
3. **Unaligned Access Penalties:** Accessing a 32-bit field inside a packed struct on architectures that do not support unaligned memory access (such as ARM Cortex-M0) triggers a hardware usage fault (`UsageFault`).
4. **Endianness Transformation:** Network wire formats are predominantly Big-Endian, while most microcontrollers are Little-Endian. Software must use translation intrinsics (`htons`, `htonl`, `__builtin_bswap32`).

## Examples
```c
#include <stdint.h>
#include <stddef.h>
#include <assert.h>

/* 1. Hardware Peripheral Register Map (MMIO) */
typedef struct {
    volatile uint32_t CR1;    /* Offset 0x00: Control Register 1 */
    volatile uint32_t CR2;    /* Offset 0x04: Control Register 2 */
    volatile uint32_t SR;     /* Offset 0x08: Status Register */
    volatile uint32_t DR;     /* Offset 0x0C: Data Register */
    volatile uint32_t RESERVED[4]; /* Reserved hole: 0x10 - 0x1C */
    volatile uint32_t ICR;    /* Offset 0x20: Interrupt Clear */
} USART_TypeDef;

#define USART1 ((USART_TypeDef *)0x40013800UL)

/* 2. Network Protocol Frame: Byte-exact wire layout */
#if defined(__GNUC__) || defined(__clang__)
#define PACKED_STRUCT struct __attribute__((packed))
#else
#define PACKED_STRUCT struct
#pragma pack(push, 1)
#endif

PACKED_STRUCT TelemetryPacket {
    uint8_t  preamble;      /* Offset 0 */
    uint16_t sequence_id;   /* Offset 1 (Unaligned!) */
    uint32_t timestamp;     /* Offset 3 (Unaligned!) */
    uint8_t  checksum;      /* Offset 7 */
};

#if !defined(__GNUC__) && !defined(__clang__)
#pragma pack(pop)
#endif

static_assert(sizeof(struct TelemetryPacket) == 8, "Packet layout must be exactly 8 bytes");
static_assert(offsetof(struct TelemetryPacket, sequence_id) == 1, "Misaligned sequence_id");
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Unaligned Pointer Derivation:** Taking the address of an unaligned member inside a packed struct (`uint32_t *p = &pkt->timestamp;`) produces an unaligned pointer. Dereferencing it invokes Undefined Behavior in ISO C.
- **Packed Struct Codegen:** Compilers handle unaligned reads in packed structs by generating multiple byte-load instructions, substantially degrading performance.

## Edge Cases and Failure Modes
- **HardFault on Cortex-M0:** Executing a standard 32-bit load (`LDR`) on an unaligned address in an ARM Cortex-M0 core triggers an immediate unrecoverable `HardFault`.
- **Missing `volatile`:** Omitting `volatile` from an MMIO register struct allows the compiler optimizer to convert polling loops (`while (!(USART1->SR & RXNE));`) into an infinite empty loop.

## Embedded Implications
- **Explicit Padding Holes:** Always define explicit `RESERVED` array members to bridge register gaps rather than relying on compiler padding.
- **DMA Alignment:** DMA controllers require source/destination addresses aligned to 4, 8, or 32-byte boundaries regardless of packed protocol definitions.

## Firmware Review Angle
- Confirm that every hardware register structure is 100% populated with explicit `volatile uint32_t` fields, including explicit padding for reserved gaps.
- Verify that code never creates raw pointers to unaligned members of packed structures.
- Audit network deserialization paths for byte-swapping functions (`ntohs`, `ntohl`).

## Compiler, ABI, and Toolchain Implications
- `-Waddress-of-packed-member` (GCC/Clang) flags attempts to take the address of unaligned members inside packed structs.

## Performance, Memory, Timing, and Power
- Reading packed structs on architectures without unaligned hardware support requires 4 byte reads and 3 shift-or cycles per 32-bit word, causing a 4x-7x slowdown.
- Register MMIO structs with natural alignment compile to single-cycle `LDR`/`STR` instructions.

## Verification / Debugging
- Enforce layout assertions at build time using `_Static_assert(offsetof(...))` for every critical register and packet field.
- Use oscilloscopes or logic analyzers to verify register write sequencing when optimizing volatile access loops.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 1.3: There shall be no occurrence of undefined behavior (strictly bans unaligned pointer dereferencing).
- Unvalidated wire packets cast to packed structs can trigger buffer overflows if length fields are corrupt.

## Trade-offs and Alternatives
- **Packed Struct Overlay vs. Explicit Byte Serialization:** Casting raw buffers to packed structs is syntactically clean, but explicit byte serialization using shift operators (`buf[0] | (buf[1] << 8)`) is 100% portable, endian-independent, and immune to alignment faults.

## Staff-Level Takeaway
Never take the address of a packed struct member. Model MMIO peripheral blocks using naturally aligned structures qualified with `volatile` and explicit reserved fields. For wire protocols, prefer explicit byte serialization functions over packed structs to ensure portability across heterogeneous architectures.

## Related Concepts
- `01_Structure_layout`
- `05_Pointer_to_structure`
- `07_Union_representation`
- `11_Enum_portability`
