# 01: Bit Field Declaration

## Definition
A bit-field declaration defines a structure member with a compile-time fixed width in bits using the syntax `type [member_name] : width;`. It instructs the compiler to allocate storage within an underlying machine storage unit (typically word or byte) rather than assigning the full natural alignment and size of the declared type.

## Scope and Boundaries
Covers: Declaration syntax, permitted standard types, unnamed fields, storage allocation units, and addressability rules.
Does not cover: Dynamic width calculations (which are illegal in C), runtime bit shifting, or bit fields outside of structures/unions.

## Why Does It Exist
Early computing architectures suffered severe memory constraints (kilobytes or words of memory). Bit fields were introduced to allow C programmers to pack multiple boolean flags or small integer ranges into single memory words without writing manual shift and mask operations.

## Mechanism and Language Rules
1. **Permitted Types (ISO C99/C11 §6.7.2.1):** A bit field shall have a type that is a qualified or unqualified version of `_Bool`, `signed int`, `unsigned int`, or an implementation-defined type.
2. **Plain `int` Ambiguity:** In ISO C, whether a bit field declared as plain `int` is treated as signed or unsigned is implementation-defined.
3. **No Address-of Operator (`&`):** A bit field cannot be addressed via the address-of operator `&`. Because pointers in C address byte boundaries, taking `&s.field` is a constraint violation and will not compile.
4. **Unnamed Bit Fields:** A bit field declared without an identifier (`unsigned int : 3;`) provides padding within the storage unit without introducing an accessible name.
5. **No Arrays or Pointers:** You cannot declare an array of bit fields or a pointer to a bit field.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

struct SystemFlags {
    unsigned int is_initialized : 1;
    unsigned int error_code     : 4;
    unsigned int                : 3; /* Unnamed padding: skips 3 bits */
    unsigned int power_mode     : 2;
    _Bool        watchdog_fed   : 1; /* C99 _Bool bit field */
};

static void configure_flags(struct SystemFlags *flags) {
    flags->is_initialized = 1u;
    flags->error_code     = 0x07u;
    flags->power_mode     = 0x02u;
    flags->watchdog_fed   = true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Plain `int` Signedness:** Compilers like GCC for ARM treat plain `int : width` as signed, meaning `int flag : 1` holds `0` or `-1`, breaking standard boolean assumptions.
- **Extended Types:** Many compilers (GCC, Clang, Keil) support `uint8_t`, `uint16_t`, or `uint64_t` as bit-field types as a compiler extension, but this is implementation-defined by ISO C.

## Edge Cases and Failure Modes
- **Constraint Violation on `sizeof`:** Calling `sizeof(flags.error_code)` or `offsetof(struct SystemFlags, error_code)` causes a compile-time constraint violation.
- **Pointer Taking:** Passing a bit field as a reference parameter (`func(&flags.is_initialized)`) triggers a compiler error.

## Embedded Implications
- **Memory Footprint Optimization:** Packing 8 discrete state booleans into a single 1-byte storage unit saves valuable internal SRAM on microcontrollers.
- **Register Read-Modify-Write:** Assigning to a single bit field generates CPU load-mask-or-store instructions, which are not atomic and can corrupt adjacent bits if modified by interrupts.

## Firmware Review Angle
- Check that no bit field uses plain `int`. Every bit field must be explicitly declared `unsigned int` or `signed int`.
- Ensure unnamed bit fields are explicitly documented if they are intended to skip reserved bits.

## Compiler, ABI, and Toolchain Implications
- ABI rules define what container size is used. Under ARM AAPCS, declaring `unsigned int : 4` uses a 32-bit container, while declaring `uint8_t : 4` (if supported) uses an 8-bit container.

## Performance, Memory, Timing, and Power
- Reading or writing a bit field incurs instruction cycle overhead: the CPU must execute logical bit-shifts (`LSR`, `LSL`) and bit-masks (`AND`, `ORR`, `BFI` on ARM Cortex).
- Code size increases compared to reading a dedicated naturally aligned byte.

## Verification / Debugging
- Debuggers often display bit fields properly, but expression watches cannot evaluate addresses of bit fields.
- Compiler warnings: `-Wpedantic` flags implementation-defined bit-field types.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 6.1: Bit fields shall only be declared with an explicitly signed or unsigned integer type.
- MISRA C:2012 Rule 6.2: Signed bit fields shall have a length of at least 2 bits.

## Trade-offs and Alternatives
- **Bit Fields vs. Bit Masks:** Bit fields provide cleaner member-access syntax (`flags.ready = 1`) but forfeit deterministic memory layout and atomicity.

## Staff-Level Takeaway
Never declare bit fields with plain `int`. Always use explicit `unsigned int` or `signed int`. Keep in mind that bit fields are accessors, not distinct memory objects: they cannot be addressed, sized, or passed by reference.

## Related Concepts
- `02_Bit_field_widths`
- `04_Signed_bit_fields`
- `12_Safe_bit_field_policy`
