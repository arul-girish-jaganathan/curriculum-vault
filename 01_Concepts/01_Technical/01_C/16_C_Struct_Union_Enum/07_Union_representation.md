# 07: Union Representation

## Definition
A union is an aggregate type capable of holding at most one member at any given time. Unlike structures, all members within a union share the same base memory address. The size of a union is determined by the size of its largest member, padded to satisfy the alignment of its most strictly aligned member.

## Scope and Boundaries
Covers: Union memory footprint, alignment inheritance, member overlap, common initial sequences, and representation layout.
Does not cover: Active member rules and type punning legality (see `08_Union_active_member_rules`) or anonymous unions (see `09_Anonymous_members`).

## Why Does It Exist
Unions serve two architectural purposes in systems programming:
1. **Memory Conservation:** Allowing mutually exclusive data fields to share the exact same RAM storage.
2. **Multi-representation Modeling:** Facilitating low-level inspection of identical memory words as distinct structures or primitive types.

## Mechanism and Language Rules
1. **Zero Offset for All Members:** Every member starts at offset 0:
   `(void *)&u == (void *)&(u.member_a) == (void *)&(u.member_b)`.
2. **Size Calculation:** `sizeof(union U)` is at least as large as the largest member.
3. **Trailing Padding:** If the largest member's size is not an even multiple of the union's strictest member alignment, trailing padding is added.
4. **Common Initial Sequence:** ISO C allows inspecting the common initial sequence of two standard-layout structures contained within a union, regardless of which is active.

## Examples
```c
#include <stdint.h>
#include <stddef.h>
#include <assert.h>

union Register32 {
    uint32_t full_word;
    struct {
        uint16_t low;
        uint16_t high;
    } halves;
    uint8_t bytes[4];
};

static_assert(sizeof(union Register32) == 4, "Union must be 4 bytes");
static_assert(offsetof(union Register32, full_word) == 0, "Must be offset 0");
static_assert(offsetof(union Register32, halves) == 0, "Must be offset 0");
static_assert(offsetof(union Register32, bytes) == 0, "Must be offset 0");
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Byte Order:** In the example above, which byte of `full_word` corresponds to `bytes[0]` depends on target endianness (little-endian vs big-endian).
- **Padding Invariance:** Overwriting a smaller member leaves the remaining bytes of a larger member with unspecified values.

## Edge Cases and Failure Modes
- **Endianness Traps:** Code assuming `bytes[0]` is the most significant byte fails completely when ported from big-endian to little-endian (e.g., PowerPC/ARM to x86).
- **Alignment Mismatches:** Placing a 64-bit member in a union elevates the alignment requirement of the entire union to 8 bytes, causing padding when embedded in structures.

## Embedded Implications
- **Register Slicing:** Commonly used in HALs to read a 32-bit status register as a single word or as individual byte/half-word lanes without bit-shift instructions.
- **Variant Buffers:** Used for event queues in RTOS environments where a single queue slot must accommodate timer events, network events, or user I/O events without dynamic allocation.

## Firmware Review Angle
- Verify that code accessing sub-words or byte slices within a union accounts for processor endianness.
- Ensure union size assertions are locked with `_Static_assert`.

## Compiler, ABI, and Toolchain Implications
- ABI rules pass unions in integer registers if their size is less than or equal to the register word size. Otherwise, they are passed via stack reference.

## Performance, Memory, Timing, and Power
- Unions achieve 100% memory sharing for mutually exclusive states, critical for microcontrollers with minimal RAM (e.g., <= 2KB).

## Verification / Debugging
- Debuggers can display all union representations simultaneously: in GDB, `print u` shows every member's interpretation of the underlying memory.

## Safety, Security, and Reliability
- Uncontrolled access to non-active union members can expose uninitialized memory or corrupted bit patterns.
- Always encapsulate unions inside tagged structures (tagged unions) with an explicit discriminator enum.

## Trade-offs and Alternatives
- **Union vs. Void Pointer:** Unions provide compile-time bounded polymorphic storage without requiring dynamic memory allocations or loss of type safety.

## Staff-Level Takeaway
A union guarantees overlapping base addresses and memory conservation. When using unions to slice data words, always isolate endianness dependencies using conditional compilation or abstraction macros.

## Related Concepts
- `01_Structure_layout`
- `08_Union_active_member_rules`
- `10_Enumerations`
