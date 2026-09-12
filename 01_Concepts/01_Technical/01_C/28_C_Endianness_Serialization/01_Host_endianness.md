# 01: Host Endianness

## Definition
Host endianness refers to the byte-ordering convention used by a specific host CPU architecture to store multi-byte fundamental types (such as `uint16_t`, `uint32_t`, `uint64_t`) in computer memory. The two primary conventions are **little-endian** (least significant byte stored at the lowest memory address) and **big-endian** (most significant byte stored at the lowest memory address).

## Scope and Boundaries
- **Covers:** Little-endian, big-endian, byte address ordering, runtime endianness detection, and CPU architecture profiles.
- **Does not cover:** Network byte order conversion ([[02_Byte_order_conversion]]), bit-level endianness (bit-fields), or floating-point representation quirks.

## Why Does It Exist
Processor designers make fundamental architectural trade-offs regarding memory addressing:
- **Little-Endian (x86_64, ARM, RISC-V):** Simplifies hardware arithmetic logic units (ALUs) by allowing wider types to be accessed at the same base address regardless of truncation (e.g., casting a `uint32_t *` to a `uint16_t *` keeps the lower bits aligned to the same memory address).
- **Big-Endian (IBM Power, legacy mainframes, network protocols):** Matches human reading order (most significant digits first), simplifying manual debugging memory dumps.

## Mechanism and Language Rules
- **Memory Layout Inspection:** Using `unsigned char *` inspection ([[../27_C_Alignment_Object_Representation/05_Unsigned_char_inspection]]), we can inspect the exact byte order of a multi-byte integer.
- **No ISO C Endianness Keyword:** Standard ISO C provides no native keyword or compile-time macro to query host endianness, though modern compilers (`__BYTE_ORDER__`) define preprocessor macros.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

int main(void) 
{
    uint32_t test_val = 0x01020304;
    unsigned char *p = (unsigned char *)&test_val;

    printf("Host representation of 0x01020304:\n");
    for (int i = 0; i < 4; ++i) {
        printf("Byte %d: 0x%02X\n", i, p[i]);
    }

    if (p[0] == 0x04) {
        printf("Architecture is Little-Endian.\n");
    } else if (p[0] == 0x01) {
        printf("Architecture is Big-Endian.\n");
    } else {
        printf("Architecture is Bi-Endian or Unknown.\n");
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Host endianness is completely implementation-defined by the CPU target architecture.
- **Undefined Behavior:** Assuming host endianness matches network byte order without explicit conversion.

## Edge Cases and Failure Modes
- **Bi-Endian Hardware:** Certain ARM and MIPS processors can be configured dynamically at boot into either little-endian or big-endian mode, making compile-time assumptions dangerous.

## Embedded Implications
- **Peripheral Register Maps:** Microcontroller registers are fixed-endian by hardware design. Drivers must handle byte ordering correctly if communicating across bridges or external coprocessors.

## Firmware Review Angle
- **Audit Endian Assumptions:** Flag any codebase that assumes `sizeof(int)` or byte ordering without explicit conversion checks when communicating over network interfaces or serial buses.

## Compiler, ABI, and Toolchain Implications
- **Predefined Macros:** Modern compilers provide standard preprocessor macros:
  `#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__`

## Performance, Memory, Timing, and Power
- **Zero Runtime Cost:** Runtime branching can be eliminated by using compile-time preprocessor checks to select native byte-swapping instructions (`bswap` on x86, `rev` on ARM).

## Verification / Debugging
- **GDB Inspection:** Use `print /x test_val` and `x/4xb &test_val` to verify memory byte layouts during debugging.

## Safety, Security, and Reliability
- **Cross-Platform Bugs:** Failing to account for host endianness when parsing binary files or network packets causes silent data corruption and protocol deserialization failures.

## Trade-offs and Alternatives
- **Compile-Time vs. Runtime Detection:** Prefer compile-time preprocessor macros (`__BYTE_ORDER__`) over runtime pointer checks to enable dead-code elimination by the compiler.

## Staff-Level Takeaway
Never assume host endianness. All network protocols, binary file formats, and storage standards must explicitly define their byte ordering, and C code must enforce explicit conversions between host and wire endianness.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_Byte_order_conversion]]
- [[03_Integer_serialization]]
- [[../27_C_Alignment_Object_Representation/04_Object_representation]]
