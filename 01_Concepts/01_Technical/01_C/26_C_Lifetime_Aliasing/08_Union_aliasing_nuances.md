# 08: Union Aliasing Nuances

## Definition
Union aliasing nuances refer to the rules and platform-specific behaviors surrounding type punning—interpreting the stored value of one union member by reading from another union member. While standard ISO C permits union aliasing, C++ and various compiler extensions treat type punning differently.

## Scope and Boundaries
- **Covers:** Union type punning, ISO C vs. C++ differences, and GCC/Clang extensions.
- **Does not cover:** Strict aliasing rules ([[06_Strict_aliasing]]) or character type access ([[07_Character_type_access]]).

## Why Does It Exist
Unions allow multiple members to share the same memory location. In C99 and later, unions provide a standardized mechanism for type punning without violating strict aliasing rules, bridging low-level hardware interaction with high-level code.

## Mechanism and Language Rules
- **ISO C Rule:** It is legal in ISO C to write to one member of a union and read from another member. The active member is the one most recently written.
- **C++ Incompatibility:** C++ strictly forbids union type punning; reading from a member other than the one last written is undefined behavior in C++.
- **Compiler Extension:** GCC and Clang explicitly support union type punning even in C++ mode as a compiler extension, but standard-compliant C requires awareness of these nuances.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

typedef union {
    uint32_t u;
    float f;
} pun_t;

float reinterpret_bits(uint32_t val) 
{
    pun_t p;
    p.u = val; /* Write to member u */
    return p.f; /* Read from member f: legal in ISO C */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Padding Bits:** Reading a union member when the written member is smaller can expose uninitialized padding bytes, yielding indeterminate values or trap representations.

## Edge Cases and Failure Modes
- **Endianness Dependency:** Union type punning for bit-level reinterpretation (e.g., float to int bits) is sensitive to host CPU endianness.

## Embedded Implications
- **Hardware Register Mapping:** Unions are frequently used in embedded headers to access peripheral control registers both as a combined 32-bit word and as individual bitfield structs.

## Firmware Review Angle
- **Audit Bitfield Portability:** Verify that bitfield union members account for compiler-specific bitfield packing and endianness rules.
- **Prefer `memcpy`:** For strict cross-platform portability and C++ interoperability, prefer `memcpy` over union type punning.

## Compiler, ABI, and Toolchain Implications
- **TBAA Exemption:** Compilers disable strict aliasing assumptions across union members, ensuring writes to one union field invalidate cached reads of another.

## Performance, Memory, Timing, and Power
- **Zero Cost:** Union punning compiles down to direct register sharing or stack/memory re-indexing with zero runtime overhead.

## Verification / Debugging
- **Compiler Warnings:** Ensure `-Wuninitialized` is enabled to catch uninitialized union member reads.

## Safety, Security, and Reliability
- **Standard Compliance:** While valid in ISO C, union punning can cause friction when sharing header files with C++ compilers or strict static analyzers.

## Trade-offs and Alternatives
- **Union Punning vs. `memcpy`:** Union punning is concise in C but non-portable to C++; `memcpy` is universally portable, safe, and fully optimized away by modern compilers.

## Staff-Level Takeaway
Union type punning is explicitly legal in ISO C but frowned upon in C++. Use unions when modeling hardware registers, but for general type reinterpretation, consider `memcpy` or explicit helper functions to maintain clean, cross-language compatibility.

## Related Concepts
- [[00_Chapter_Index]]
- [[06_Strict_aliasing]]
- [[27_C_Alignment_Object_Representation/04_Object_representation]]
