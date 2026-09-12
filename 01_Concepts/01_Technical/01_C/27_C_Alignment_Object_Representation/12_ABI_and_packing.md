# 12: ABI and Packing

## Definition
ABI (Application Binary Interface) and Packing refer to the standardized rules governing how data types are laid out in memory across function call boundaries, shared libraries, and hardware architectures, and how `#pragma pack` (or `__attribute__((packed))`) modifies default structural padding to eliminate padding bytes.

## Scope and Boundaries
- **Covers:** ABI layout rules, `#pragma pack`, `__attribute__((packed))`, unaligned access penalties, and cross-compiler compatibility.
- **Does not cover:** Dynamic memory allocation, CPU cache lines ([[11_Cache_line_alignment]]), or standard alignment requirements ([[01_Alignment_requirements]]).

## Why Does It Exist
Default C structure padding optimizes for speed but wastes memory and breaks binary compatibility with external protocols:
- **Packed Structures:** `#pragma pack(1)` removes all padding bytes, forcing members to pack contiguously. This is essential for parsing fixed-format network headers and hardware register maps.
- **ABI Compatibility:** Functions compiled by different compilers or toolchain versions must agree on structure layout, calling conventions, and type alignments to prevent catastrophic memory corruption.

## Mechanism and Language Rules
- **Pragma Pack Syntax:**
  ```c
  #pragma pack(push, 1)
  struct packed_header {
      uint8_t  magic;
      uint32_t version;
  };
  #pragma pack(pop)
  ```
- **GCC Attribute Syntax:** `struct __attribute__((packed)) packed_header { ... };`
- **Unaligned Member Danger:** Members of packed structures are unaligned by default if their natural alignment exceeds 1 byte. Taking the address of a packed struct member (`&packed_struct.version`) creates an unaligned pointer; dereferencing it directly can trigger hardware faults.

## Examples
```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#pragma pack(push, 1)
struct unpacked_vs_packed {
    uint8_t  a;
    uint32_t b; /* Immediately follows a with zero padding */
};
#pragma pack(pop)

int main(void) 
{
    printf("Size of packed struct: %zu bytes (Expected: 5)\n", sizeof(struct unpacked_vs_packed));

    struct unpacked_vs_packed pkt = { .a = 0x55, .b = 0xDEADBEEF };

    /* DANGER: Taking address of unaligned member b */
    uint32_t val;
    memcpy(&val, &pkt.b, sizeof(val)); /* Safe copy avoiding unaligned dereference */

    printf("Safely extracted unaligned field b: 0x%08X\n", val);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Directly dereferencing a pointer to an unaligned member of a packed structure (`uint32_t *p = &packed.b; *p;`) on a strict-alignment CPU architecture.

## Edge Cases and Failure Modes
- **Hidden Performance Penalty:** On x86_64, accessing packed unaligned members compiles into slower multi-cycle unaligned load instructions. On ARM Cortex-M0, it triggers a HardFault exception.
- **ABI Mismatch:** Passing a packed struct across a shared library (`.so` / `.dll`) boundary compiled with different packing pragmas corrupts the stack and memory layouts.

## Embedded Implications
- **Memory-Mapped I/O Registers:** Hardware peripheral register maps are frequently defined using packed structures or precise padding offsets to align registers with hardware documentation.

## Firmware Review Angle
- **Ban Direct Packed Member Pointers:** Audit all uses of packed structures; strictly forbid passing pointers to packed members into functions expecting aligned pointers. Enforce `memcpy` extraction.
- **Verify Pragma Push/Pop:** Ensure every `#pragma pack(push, 1)` is paired with `#pragma pack(pop)` to prevent packing corruption across header files.

## Compiler, ABI, and Toolchain Implications
- **ABI Standardization:** Compilers enforce platform ABIs (e.g., ARM AAPCS, System V AMD64 ABI) to ensure binary compatibility across compiled object files.

## Performance, Memory, Timing, and Power
- **Memory Savings:** Packed structures eliminate padding bytes entirely, reducing RAM and storage footprint for network packet buffers and binary files.

## Verification / Debugging
- **Compiler Warnings:** Enable `-Waddress-of-packed-member` (GCC/Clang) to catch dangerous unaligned pointer acquisition at compile time.

## Safety, Security, and Reliability
- **Safety Compliance:** Unaligned access faults are a common cause of unexpected embedded system resets in safety-critical deployments.

## Trade-offs and Alternatives
- **Packing vs. Manual Unpacking:** Packed structures offer clean syntax at the risk of unaligned access faults; manual byte shifting / `memcpy` offers 100% safety and portability across all architectures.

## Staff-Level Takeaway
`#pragma pack` is a powerful tool for interfacing with binary file formats and network protocols, but it is a double-edged sword. Never dereference pointers to packed members directly on strict-alignment architectures; always extract them safely via `memcpy`.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Alignment_requirements]]
- [[06_Padding_bytes]]
- [[09_Serialization_hazards]]
