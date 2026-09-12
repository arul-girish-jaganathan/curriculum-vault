# 04: Object Representation

## Definition
The object representation of an object of type `T` is the sequence of `sizeof(T)` objects of type `unsigned char` occupying the storage inhabited by the object. It encompasses value bits, padding bytes, sign bits, and implementation-defined bit configurations (such as trap representations).

## Scope and Boundaries
- **Covers:** Object bytes, value representation vs. object representation, padding bytes, and memory layout inspection.
- **Does not cover:** Bit-fields layout quirks ([[06_Padding_bytes]]), floating-point trap representations ([[07_Trap_representations]]), or strict aliasing rules ([[../26_C_Lifetime_Aliasing/06_Strict_aliasing]]).

## Why Does It Exist
Understanding object representation is fundamental for low-level systems programming, network serialization, cryptography, and debugging:
- **Bit-Level Inspection:** Allows developers to examine the exact byte patterns of numbers, pointers, and structures.
- **Raw Memory Operations:** Explains how functions like `memcpy` and `memcmp` operate purely on the level of object representations.

## Mechanism and Language Rules
- **Value Representation vs. Object Representation:** The *value representation* is the set of bits that contribute to calculating the mathematical value. The *object representation* includes value bits plus any padding bytes, sign bits, and unused bits.
- **Addressability:** Every byte of an object representation has a unique memory address.
- **Strict Aliasing Exception:** ISO C explicitly guarantees that inspecting an object's representation via pointers to `char`, `signed char`, or `unsigned char` is completely exempt from strict aliasing rules.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

int main(void) 
{
    uint32_t val = 0x12345678;
    unsigned char *bytes = (unsigned char *)&val;

    printf("Object representation of 0x12345678 (hex bytes):\n");
    for (size_t i = 0; i < sizeof(val); ++i) {
        printf("Byte %zu: 0x%02X\n", i, bytes[i]);
    }
    
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Endianness (whether the least significant byte is stored at the lowest memory address) determines the byte order in object representations.
- **Undefined Behavior:** Accessing uninitialized padding bytes or assuming structures have zero padding bytes without verification is undefined behavior.

## Edge Cases and Failure Modes
- **Padding Byte Garbage:** Copying a struct containing padding bytes using `memcmp` can yield unexpected non-zero comparisons even if all meaningful fields are identical, because padding bytes contain uninitialized garbage values.
- **Endianness Traps:** Assuming big-endian byte order on little-endian hardware during binary network packet deserialization.

## Embedded Implications
- **Protocol Parsers:** When parsing raw byte buffers from sensors or communication buses, treating structs directly as object representations fails if padding bytes or compiler packing differences exist.

## Firmware Review Angle
- **Struct Comparison Hazards:** Flag any use of `memcmp` on structures containing padding bytes; recommend field-by-field comparison or explicit zero-initialization (`memset(&s, 0, sizeof(s))`).

## Compiler, ABI, and Toolchain Implications
- **Layout Determinism:** The compiler determines exact object layout based on target ABI rules, alignment requirements, and member ordering.

## Performance, Memory, Timing, and Power
- **Zero Overhead Inspection:** Examining object representations via `unsigned char *` compiles into direct memory load instructions.

## Verification / Debugging
- **Memory Dump Inspection:** Use GDB (`x/8xb &my_struct`) to inspect object representations during debugging sessions.

## Safety, Security, and Reliability
- **Information Leakage:** Serializing raw object representations (including padding bytes) to persistent storage or network sockets can leak uninitialized stack/heap memory contents, posing a security vulnerability.

## Trade-offs and Alternatives
- **Raw Representation vs. Serialized Structs:** Avoid transmitting raw object representations across network boundaries; use explicit serialization functions that pack fields individually to eliminate padding and endianness hazards.

## Staff-Level Takeaway
An object in C is not just an abstract mathematical value; it is a concrete sequence of bytes residing in memory. Mastering object representation is what separates systems programmers from application developers.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_Unsigned_char_inspection]]
- [[06_Padding_bytes]]
- [[08_Copying_representations]]
- [[09_Serialization_hazards]]
