# 02: Structure Members

## Definition
Structure members are individual named components within a structure. They may consist of complete object types, arrays, pointers, nested structures, or bitfields. ISO C prohibits incomplete types (such as unsized arrays or forward-declared structures) as members, with the singular exception of flexible array members as the terminal field.

## Scope and Boundaries
Covers: Member declarations, member access operators (`.` and `->`), bitfield declarations, storage unit allocation, sign extension traps, and atomic member semantics.
Does not cover: Pointers to structures (see `05_Pointer_to_structure`), flexible array members (see `06_Flexible_array_members`), or anonymous members (see `09_Anonymous_members`).

## Why Does It Exist
Structure members provide typed modularization of heterogeneous data. Bitfields specifically allow micro-allocation of variable bit widths, essential for packing multiple status flags into discrete hardware register words.

## Mechanism and Language Rules
1. **Type Constraints:** Members must have complete object types at the time of struct definition. A struct cannot contain an instance of itself, but can contain a pointer to its own type.
2. **Bitfields:** Declared using `type [member_name] : width;`.
3. **Bitfield Base Types:** ISO C strictly mandates that bitfields be `_Bool`, `signed int`, `unsigned int`, or implementation-defined types. Plain `int` bitfield signedness is implementation-defined.
4. **No Address-of Bitfields:** You cannot take the address of a bitfield (`&s.bit`) because pointers address byte boundaries, not individual bits.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

struct PeripheralControl {
    /* Explicit signedness prevents implementation-defined traps */
    unsigned int enable      : 1;
    unsigned int mode        : 3;
    unsigned int reserved    : 4;
    signed int   calibration : 8; /* Signed two's complement bitfield */
    uint16_t     threshold;
};

static void configure_peripheral(struct PeripheralControl *ctrl) {
    ctrl->enable = 1u;
    ctrl->mode = 0x05u;
    ctrl->calibration = -12; /* Properly sign-extended */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Bitfield Ordering:** The order of allocation of bitfields within a storage unit (least-significant bit first vs. most-significant bit first) is implementation-defined.
- **Storage Unit Overlap:** Whether a bitfield can cross a storage unit boundary is implementation-defined.
- **Plain `int` Bitfields:** In ISO C, `int b : 1;` may have a range of `[0, 1]` or `[-1, 0]`. Always use `unsigned int` or `signed int`.

## Edge Cases and Failure Modes
- **Bitfield Truncation:** Assigning an out-of-range value (e.g., assigning `7` to an `unsigned int b : 2`) causes value truncation / integer wrap.
- **Data Races on Adjacent Bitfields:** Multiple threads or interrupt routines modifying adjacent bitfields concurrently without locks trigger data races because the processor issues full-word read-modify-write instructions.

## Embedded Implications
- **Hardware Register Mapping Pitfall:** Never map bitfields directly to MMIO registers for peripheral control if the hardware requires atomic word writes, because the compiler generates multi-instruction read-modify-write sequences.
- **Volatile Bitfields:** C standard support for `volatile` bitfields is ambiguous across toolchains. GCC and Clang provide `-fstrict-volatile-bitfields` to enforce bus-width accesses.

## Firmware Review Angle
- Verify that every bitfield is explicitly declared as `unsigned int` or `signed int`—never plain `int`.
- Ensure concurrent ISRs/threads never independently mutate different bitfields residing within the same underlying word.

## Compiler, ABI, and Toolchain Implications
- ABI specifications define whether bitfields are packed left-to-right (MSB) or right-to-left (LSB). ARM AAPCS specifies little-endian bit allocation starting from the least-significant bit.

## Performance, Memory, Timing, and Power
- Bitfield operations require masking, shifting, and read-modify-write cycles, which increase instruction count and execution time compared to full-width variables.

## Verification / Debugging
- Static analysis tools (Coverity, PC-lint, Clang-Tidy) catch signed 1-bit bitfield bugs (`int flag : 1; flag = 1; if (flag == 1)` evaluates to false if signedness treats 1 as -1).

## Safety, Security, and Reliability
- MISRA C:2012 Rule 6.1: Bitfields shall only be declared with an explicitly signed or unsigned integer type.
- MISRA C:2012 Rule 6.2: Signed bitfields shall have a length of at least 2 bits.

## Trade-offs and Alternatives
- **Bitfields vs. Explicit Bitwise Masks:** Explicit bitwise shifts and masks (`#define REG_MODE_MASK (0x07 << 1)`) are strictly portable and architecture-independent, whereas bitfields suffer from compiler-dependent packing order.

## Staff-Level Takeaway
Avoid bitfields for external communication packets and MMIO register interfaces due to layout non-portability. Limit bitfields to internal RAM-constrained state flags, and use explicit bitmasks for hardware interfaces.

## Related Concepts
- `01_Structure_layout`
- `12_Protocol_and_register_layouts`
