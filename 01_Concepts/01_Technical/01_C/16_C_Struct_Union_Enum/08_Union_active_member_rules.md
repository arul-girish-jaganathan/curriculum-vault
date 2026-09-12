# 08: Union Active Member Rules

## Definition
The "active member" of a union is the member that was most recently written. ISO C specifies that reading from a member other than the active member constitutes type punning. While C99 (via TC3 and Annex J) and modern C standards explicitly permit reading non-active members (reinterpreting the stored representation), doing so across incompatible pointer types or without following language rules risks strict aliasing violations and undefined behavior.

## Scope and Boundaries
Covers: Active member tracking, standard type punning semantics, strict aliasing exemptions, and common initial sequence rules.
Does not cover: C++ type punning rules (C++ strictly forbids union type punning via undefined behavior).

## Why Does It Exist
Type punning allows low-level code to inspect the underlying bit representation of a data type (for instance, reading the IEEE 754 floating-point exponent bits as an integer). Unions provide a controlled language mechanism for this representation switching.

## Mechanism and Language Rules
1. **Writing Activates Member:** Writing to `u.member_a` makes `member_a` the active member.
2. **C99/C11 Type Punning:** ISO C99 TC3 footnote 95 explicitly states that accessing a non-active member reinterprets the object representation. Under ISO C, union type punning through the union object itself is well-defined.
3. **Strict Aliasing Rule:** ISO C forbids accessing an object of one type through a pointer of an incompatible type. Accessing via union member syntax (`u.m2`) is valid; casting pointers to union members (`*(int *)&u.float_val`) violates strict aliasing.
4. **Common Initial Sequence:** If two structs share a common initial sequence of types, you may inspect those fields in either struct within a union, even if that struct is not active.

## Examples
```c
#include <stdint.h>
#include <assert.h>

union FloatBits {
    float    f;
    uint32_t u;
};

/* Legal C99/C11 Type Punning via direct union access */
static uint32_t get_float_bits(float val) {
    union FloatBits fb;
    fb.f = val; /* fb.f is now active */
    return fb.u; /* Well-defined in C99+: reads underlying IEEE 754 bit pattern */
}

/* ILLEGAL: Strict Aliasing Violation */
static uint32_t illegal_pun(float val) {
    /* UB: Dereferencing float through uint32_t pointer */
    return *(uint32_t *)&val; 
}

/* Safe alternative: memcpy (always legal) */
static uint32_t safe_pun_memcpy(float val) {
    uint32_t u;
    __builtin_memcpy(&u, &val, sizeof(u));
    return u;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Trap Representations:** Reading a non-active member that contains a bit pattern invalid for its type (e.g., an invalid pointer or signaling NaN) invokes Undefined Behavior or CPU traps.
- **Strict Aliasing Violation:** Punning via pointers rather than the union object directly causes GCC/Clang with `-O2/-O3` to optimize away read/write dependencies, leading to silent memory corruption.

## Edge Cases and Failure Modes
- **C vs C++ Incompatibility:** Union type punning is fully legal in ISO C99+, but undefined behavior in ISO C++. Code shared across C and C++ compilers will break under C++.
- **Compiler Pointer Reordering:** Casting pointers extracted from unions can cause compilers to reorder writes past reads.

## Embedded Implications
- **Fast IEEE 754 Inspection:** Embedded math libraries use union punning to inspect floating-point sign and exponent bits for fast classification (`isnan`, `isinf`).
- **Network Deserialization:** Punning packed union headers over raw UART/SPI buffers without `memcpy` can trigger unaligned access faults on ARM Cortex-M0/M3 cores.

## Firmware Review Angle
- Reject any pointer-casting type punning (`*(uint32_t *)&my_float`). Enforce either direct union member access or `memcpy`.
- Confirm that the compiler operates with `-fstrict-aliasing` awareness, and check if codebases use `-fno-strict-aliasing` as an architectural crutch.

## Compiler, ABI, and Toolchain Implications
- GCC and Clang treat direct union member access as an explicit aliasing barrier.
- Modern compilers optimize `memcpy` of 4-byte or 8-byte types into a single register move with zero function call overhead.

## Performance, Memory, Timing, and Power
- Direct union punning and small-size `memcpy` compile to zero-overhead register moves on modern optimizing toolchains.

## Verification / Debugging
- Compile with `-fstrict-aliasing -Wstrict-aliasing=2` to catch invalid pointer-based aliasing.
- Use Clang UndefinedBehaviorSanitizer (`UBSan`).

## Safety, Security, and Reliability
- MISRA C:2012 Rule 19.2: The union keyword should not be used. (Strictly restricted in ASIL-D / DO-178C environments; requires safety deviations).

## Trade-offs and Alternatives
- **Union Punning vs. `memcpy`:** `memcpy` is 100% portable across both C and C++, never violates strict aliasing, and optimizes down to a single instruction on modern compilers.

## Staff-Level Takeaway
For representation reinterpretation, prefer `memcpy` over union type punning for complete portability across C and C++ toolchains. If using unions, access members strictly through the union object itself—never via cast member pointers.

## Related Concepts
- `07_Union_representation`
- `05_Pointer_to_structure`
