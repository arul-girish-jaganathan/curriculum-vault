# 08: Copying Representations

## Definition
Copying representations refers to duplicating raw object bytes (`memcpy`, `memmove`, `unsigned char` loops) versus copying logical values (assignment operators `=`). Representational copying duplicates exact bit sequences, whereas value copying assigns semantic values according to type rules.

## Scope and Boundaries
- **Covers:** `memcpy` vs. assignment, raw byte duplication, struct copying, and trap representation propagation.
- **Does not cover:** Union type-punning ([[../26_C_Lifetime_Aliasing/08_Union_aliasing_nuances]]), strict aliasing rules, or dynamic memory allocation.

## Why Does It Exist
Understanding the distinction between representational copying and value copying is essential for writing robust memory manipulation code:
- **Padding and Unused Bits:** Assignment copies value representations (padding bytes may or may not be copied, and their values are unspecified). `memcpy` copies the entire object representation byte-for-byte, including padding and trap representations.
- **Performance:** `memcpy` compiles into highly optimized vector instructions (`rep movsb`, AVX load/store blocks), outperforming manual member-by-member assignment for large structs.

## Mechanism and Language Rules
- **`memcpy` Guarantee:** `memcpy(dest, src, n)` copies `n` bytes of the object representation from `src` to `dest`. It is fully compliant with strict aliasing rules.
- **Assignment vs. `memcpy`:** `*dest = *src;` performs a semantic value copy, whereas `memcpy(dest, src, sizeof(*src))` performs a exact representational byte copy.

## Examples
```c
#include <stdio.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    uint32_t id;
    uint8_t status;
    /* padding bytes */
    uint16_t checksum;
} packet_t;

void clone_packet(packet_t *dest, const packet_t *src) 
{
    /* Representational copy: duplicates exact bytes including padding */
    memcpy(dest, src, sizeof(packet_t));
}

int main(void) 
{
    packet_t p1 = { .id = 42, .status = 1, .checksum = 0x1234 };
    packet_t p2;

    clone_packet(&p2, &p1);

    printf("Cloned Packet ID: %u, Checksum: 0x%04X\n", p2.id, p2.checksum);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Using `memcpy` with overlapping source and destination memory buffers (use `memmove` instead).
- **Undefined Behavior:** Passing null pointers or incorrect byte sizes to `memcpy`.

## Edge Cases and Failure Modes
- **Overlapping Buffers (`memcpy` UB):** Using `memcpy` when `dest` and `src` overlap causes undefined behavior and silent memory corruption in optimized builds. Always use `memmove` for overlapping regions.

## Embedded Implications
- **Fast Buffer Duplication:** `memcpy` is heavily optimized in embedded toolchain runtime libraries (often implemented in hand-written assembly utilizing ARM Neon or hardware copy engines).

## Firmware Review Angle
- **Audit Overlapping Copies:** Check all `memcpy` calls to ensure source and destination pointers never overlap; flag and replace with `memmove` where overlap is possible.

## Compiler, ABI, and Toolchain Implications
- **Builtin Optimization:** Modern compilers (GCC, Clang, MSVC) recognize `memcpy` as a compiler builtin and inline it directly into optimized store/load instructions, eliminating function call overhead.

## Performance, Memory, Timing, and Power
- **Vectorized Copying:** `memcpy` leverages wide CPU registers (128-bit, 256-bit) to copy memory blocks with maximum bus bandwidth.

## Verification / Debugging
- **AddressSanitizer:** ASan detects out-of-bounds reads/writes and overlapping buffer violations in `memcpy`/`memmove`.

## Safety, Security, and Reliability
- **Memory Safety:** Always verify buffer size parameters to prevent buffer overflow vulnerabilities during representational copying.

## Trade-offs and Alternatives
- **`memcpy` vs. Assignment:** Use assignment (`=`) for clear, type-safe semantic copying of scalars and small structs; use `memcpy` for large buffers, dynamic objects, and generic memory blocks.

## Staff-Level Takeaway
Representational copying via `memcpy` is the gold standard for duplicating raw object bytes safely and efficiently in C. Respect buffer overlap rules by using `memmove` when in doubt.

## Related Concepts
- [[00_Chapter_Index]]
- [[04_Object_representation]]
- [[05_Unsigned_char_inspection]]
- [[09_Serialization_hazards]]
