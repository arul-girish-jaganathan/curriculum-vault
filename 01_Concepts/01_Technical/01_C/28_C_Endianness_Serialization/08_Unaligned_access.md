# 08: Unaligned Access

## Definition
Unaligned access refers to reading or writing multi-byte data values from memory addresses that are not evenly divisible by the data type's alignment requirement (e.g., reading a 4-byte `uint32_t` from an address ending in `0x1` instead of a multiple of 4).

## Scope and Boundaries
- **Covers:** Unaligned memory reads/writes, network packet buffer parsing, hardware faults, and safe copying strategies.
- **Does not cover:** General alignment requirements ([[../27_C_Alignment_Object_Representation/01_Alignment_requirements]]) or structure packing ([[../27_C_Alignment_Object_Representation/12_ABI_and_packing]]).

## Why Does It Exist
Network packets and binary file streams often pack multi-byte integers at arbitrary byte offsets, creating unaligned data streams:
- **Hardware Traps:** On strict alignment architectures (ARM Cortex-M0, SPARC), dereferencing an unaligned pointer triggers a hardware exception (`HardFault`).
- **Performance Penalties:** On flexible architectures (x86_64), unaligned loads cross cache line boundaries, causing severe performance stalls.

## Mechanism and Language Rules
- **The Unaligned Danger:**
  ```c
  /* DANGEROUS: Causes unaligned access fault or performance penalty */
  uint32_t val = *(uint32_t *)(net_packet_buf + offset);
  ```
- **The Safe Solution:** Use `memcpy` to copy bytes from unaligned buffers into local properly-aligned variables. Modern compilers optimize `memcpy` into efficient unaligned load instructions.

## Examples
```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

/* Safely read a 32-bit big-endian integer from an unaligned buffer offset */
uint32_t safe_read_u32_be(const uint8_t *buf) 
{
    uint32_t val;
    /* memcpy avoids unaligned pointer dereference undefined behavior */
    memcpy(&val, buf, sizeof(uint32_t));
    
    /* Convert from network byte order */
    return ntohl(val);
}

int main(void) 
{
    uint8_t unaligned_wire[8] = { 0x00, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE };
    
    /* Offset 1 is unaligned for a 32-bit integer */
    uint32_t parsed = safe_read_u32_be(unaligned_wire + 1);
    
    printf("Parsed unaligned value: 0x%08X\n", parsed);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Direct pointer dereferencing of unaligned memory addresses violates C alignment constraints and triggers undefined behavior or hardware faults.

## Edge Cases and Failure Modes
- **Cortex-M HardFaults:** Running packet parsing code with direct pointer casts on ARM Cortex-M0/M3 microcontrollers will instantly crash the system with a HardFault exception.

## Embedded Implications
- **Network Stack Parsing:** Ethernet and CAN packet buffers are inherently unaligned when headers precede variable-length payloads. `memcpy` extraction is mandatory.

## Firmware Review Angle
- **Audit Pointer Casts on Buffers:** Flag any pointer cast from raw byte buffers (`uint8_t *`) to multi-byte integer or struct pointers; mandate `memcpy` extraction.

## Compiler, ABI, and Toolchain Implications
- **Compiler Optimization:** Compilers recognize `memcpy` on unaligned byte arrays and emit single unaligned load/store instructions (`movdqu` on x86, unaligned `ldr` on ARM) without incurring function call overhead.

## Performance, Memory, Timing, and Power
- **Efficiency:** `memcpy` provides the perfect balance of safety, portability, and maximum hardware performance for unaligned buffer access.

## Verification / Debugging
- **Sanitizers:** UndefinedBehaviorSanitizer (`-fsanitize=undefined`) detects runtime alignment faults resulting from unsafe pointer casts.

## Safety, Security, and Reliability
- **Crash Prevention:** Eliminates hardware alignment exceptions, ensuring robust embedded operation in hostile or network-heavy environments.

## Trade-offs and Alternatives
- **`memcpy` vs. Manual Shift-and-OR:** `memcpy` is concise and fast; manual shift-and-OR byte assembly is equally safe against alignment faults and handles endianness conversion simultaneously.

## Staff-Level Takeaway
Never dereference pointers cast from unaligned byte buffers. Always use `memcpy` or manual byte shifting to extract values safely from network and file streams.

## Related Concepts
- [[00_Chapter_Index]]
- [[03_Integer_serialization]]
- [[../27_C_Alignment_Object_Representation/01_Alignment_requirements]]
- [[../27_C_Alignment_Object_Representation/12_ABI_and_packing]]
