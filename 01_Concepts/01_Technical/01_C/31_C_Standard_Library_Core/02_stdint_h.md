# 02: stdint.h

## Definition
`<stdint.h>` defines integer types with explicitly constrained widths and ranges when the implementation supports them. Its core facilities are exact-width types such as `uint32_t`, minimum-width types such as `uint_least32_t`, fast types such as `uint_fast32_t`, and pointer-capable integer types such as `uintptr_t` when provided.

## Scope and Boundaries
* **Covers:** exact-width, minimum-width, fast-width, maximum-width, and integer-pointer types; corresponding limit macros.
* **Does not cover:** floating-point types, ABI-specific register typedefs, or assumptions that every named width exists on every implementation.

## Why Does It Exist
Portable embedded software needs to distinguish “exactly 32 bits” from “at least 32 bits” and from “whatever is fastest.” Standard integer-width types let firmware express that intent without assuming that `int`, `long`, or `unsigned long` have a particular width.

## Mechanism and Language Rules
1. **Exact-width types:** `intN_t` and `uintN_t` exist only when the implementation has a corresponding integer type with exactly N bits and no padding bits.
2. **Minimum-width types:** `int_leastN_t` and `uint_leastN_t` are guaranteed to provide at least N value bits.
3. **Fast types:** `int_fastN_t` and `uint_fastN_t` provide at least N value bits and are selected for efficient access on the target.
4. **Maximum-width types:** `intmax_t` and `uintmax_t` can represent every value of every signed or unsigned integer type respectively.
5. **Pointer-sized integer types:** `intptr_t`/`uintptr_t`, when defined, can represent converted object pointers and support round trips back to the pointer type.
6. **Limit macros:** macros such as `UINT32_MAX` communicate the actual supported range rather than a guessed one.

## Examples
```c
#include <stdint.h>
#include <stddef.h>

static uint32_t read_le32(const uint8_t bytes[4])
{
    return ((uint32_t)bytes[0])       |
           ((uint32_t)bytes[1] << 8U) |
           ((uint32_t)bytes[2] << 16U) |
           ((uint32_t)bytes[3] << 24U);
}

static uintptr_t object_address(const void *p)
{
    return (uintptr_t)p;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* An exact-width typedef may simply be unavailable; code must not assume `uint32_t` exists on every conforming implementation.
* Converting an integer to an integer type that cannot represent the value follows the language's unsigned modulo or implementation-defined/implementation-specific rules for signed conversions; do not use casts as range validation.
* `uintptr_t` is optional. Portable code must not require it in environments that do not provide it.
* Integer-to-pointer representations are implementation-defined; a numeric address should not be treated as universally interchangeable with a C pointer.

## Edge Cases and Failure Modes
* `uint8_t` is often useful for byte-level protocols, but “byte” in C is the unit `char`, not necessarily 8 bits; exact-width 8-bit types only exist when the implementation supports them.
* Printing fixed-width integers with `printf` requires the `<inttypes.h>` format macros rather than guessed format specifiers.
* Unsigned arithmetic wraps modulo 2^N only for the mathematical width of that unsigned type; intermediate promotions can change the type involved.
* Using `uint32_t` for quantities that can exceed 32 bits introduces a hidden architectural ceiling.

## Embedded Implications
* **Registers:** Fixed-width types make memory-mapped register definitions and protocol fields explicit, but `volatile` and access width requirements remain separate concerns.
* **Protocols:** Use exact-width types for serialized fields when the protocol specifies those widths.
* **Portability:** Avoid assuming `uint32_t` maps to a CPU register efficiently on every architecture; use fast types where performance dominates and the exact width is not contractual.
* **Pointer storage:** `uintptr_t` is useful for diagnostic address values or APIs requiring integer storage, but it does not turn arbitrary integer constants into valid pointers.

## Firmware Review Angle
1. Verify each integer type reflects the semantic requirement: width, range, speed, or portability.
2. Inspect every cast at hardware and protocol boundaries for narrowing.
3. Check compiler format warnings for logging and telemetry.
4. Test on at least one target with a different native integer width when portability matters.

## Compiler, ABI, and Toolchain Implications
The typedefs map to implementation-defined underlying types and therefore participate directly in the ABI. Changing a target ABI, compiler mode, or data model can change the representation of `size_t` and standard integer types. Compiler warnings such as `-Wconversion` and `-Wsign-conversion` are useful for exposing unintended changes in rank and signedness.

## Performance, Memory, Timing, and Power
Exact-width integers can improve predictability but are not automatically the fastest representation. An 8-bit access may require extra instructions on a 32-bit MCU, while an aligned native-width access can be cheaper. Use `uint_fastN_t` where the API needs a minimum range but not an exact representation. Measure generated code rather than assuming the typedef name predicts performance.

## Verification / Debugging
* Use `_Static_assert(sizeof(uint32_t) == 4, "protocol requires 32-bit uint32_t");` when a project genuinely depends on it.
* Use `<inttypes.h>` macros such as `PRIu32` for portable diagnostics.
* Inspect generated assembly for hot register-access paths.
* Run boundary tests using every limit macro relevant to the interface.

## Safety, Security, and Reliability
Integer truncation is a common source of buffer-overflow and protocol parsing vulnerabilities. Keep arithmetic in a type wide enough for the complete calculation, validate untrusted lengths before narrowing, and make signedness explicit at API boundaries. Fixed-width types improve reviewability but do not prevent overflow by themselves.

## Trade-offs and Alternatives
* **Use exact-width types when:** a format, register definition, or externally visible binary interface mandates a width.
* **Use least-width types when:** a minimum range is required and storage efficiency matters.
* **Use fast-width types when:** performance matters more than exact representation.
* **Use native types when:** the semantic domain is naturally `int`/`unsigned` and the width is not contractual.

## Staff-Level Takeaway
`<stdint.h>` is an intent language. A Staff engineer should distinguish representation contracts from value-range requirements and performance preferences. The right typedef is the one whose guarantee matches the interface contract; using fixed-width types everywhere without considering arithmetic promotions, ABI, and target efficiency is just another form of cargo culting.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_stddef_h]]
* [[../10_C_Conversions_Promotions/00_Chapter_Index]]
* [[../28_C_Endianness_Serialization/00_Chapter_Index]]
* [[../27_C_Alignment_Object_Representation/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*