# 05: Implementation-Defined Layout

## Definition
Implementation-defined layout refers to the compiler's autonomy under ISO C to decide how bit fields are arranged, aligned, packed, and padded inside underlying storage units, and whether bit fields are permitted to cross storage-unit boundaries.

## Scope and Boundaries
Covers: Boundary-crossing rules, storage-unit sizing, container alignment, structure padding interaction, and compiler variability.
Does not cover: User-specified byte padding (see `02_Structure_members`).

## Why Does It Exist
C was designed to generate the most efficient machine code for whatever hardware architecture it targets. By leaving bit-field packing details implementation-defined, the C committee allowed compiler writers to align bit-field storage units with the native memory bus operations of the underlying processor.

## Mechanism and Language Rules
1. **Storage Unit Sizing (§6.7.2.1):** The compiler determines the size of the storage unit used to hold bit fields (typically matching the declared integer type, e.g., 8-bit for `uint8_t`, 32-bit for `uint32_t`).
2. **Boundary Crossing (§6.7.2.1):** "Whether a bit-field that does not fit into a storage unit can span more than one storage unit is implementation-defined."
   - Some compilers will split an 8-bit field across two separate 32-bit words if only 4 bits remain in the first word.
   - Other compilers will waste the remaining 4 bits, insert invisible padding, and place the entire 8-bit field in the next storage unit.
3. **Alignment of Struct Containing Bit Fields:** The alignment of a struct containing bit fields is governed by the largest alignment requirement among its declared types (or compiler packing rules).

## Examples
```c
#include <stdint.h>
#include <stddef.h>
#include <assert.h>

struct BoundaryCross {
    uint16_t field_a : 12; /* Fits in 16-bit storage unit */
    uint16_t field_b : 8;  /* 12 + 8 = 20 bits: Does NOT fit in 16 bits! */
};

/* 
 * Compiler Behavior A (No spanning):
 *   field_a takes 12 bits of Word 0 (4 bits wasted as padding).
 *   field_b takes 8 bits of Word 1 (8 bits wasted as padding).
 *   Total sizeof = 4 bytes.
 * 
 * Compiler Behavior B (Spanning permitted):
 *   field_a takes 12 bits of Word 0.
 *   field_b takes 4 bits of Word 0 and 4 bits of Word 1.
 *   Total sizeof = 4 bytes (or 3 bytes if packed).
 */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Memory Footprint:** The `sizeof` a structure containing bit fields cannot be assumed without consulting the compiler manual or verifying via `sizeof`.
- **Internal Holes:** The existence and size of internal padding holes between bit fields when values do not cleanly sum to byte or word boundaries is implementation-defined.

## Edge Cases and Failure Modes
- **Compiler Upgrades:** Upgrading from GCC 9 to GCC 11, or switching from ARM Compiler 5 (armcc) to ARM Compiler 6 (armclang), can silently alter storage unit spanning rules, changing the struct size and corrupting binary data interfaces.
- **Cross-Compiler Structure Sharing:** Sharing header files between an embedded firmware image (compiled with GCC) and a PC desktop test harness (compiled with MSVC) can cause memory offsets to diverge.

## Embedded Implications
- **Hardware Layout Breakage:** Peripheral registers do not span arbitrary word boundaries. If a compiler chooses to span or pad unexpectedly, all subsequent register offsets in the structure become misaligned.

## Firmware Review Angle
- Reject any codebase assuming a fixed struct layout when bit fields cross nominal storage unit boundaries (e.g., where widths sum to non-multiples of 8, 16, or 32).
- Require `static_assert(sizeof(...) == N)` on any struct containing bit fields.

## Compiler, ABI, and Toolchain Implications
- Under the ARM Architecture Procedure Call Standard (AAPCS):
  - A bit-field container is allocated according to the declared type.
  - Bit fields do not cross their container boundaries unless the container is packed.

## Performance, Memory, Timing, and Power
- Spanning boundaries forces the compiler to generate multiple load and store instructions to assemble a single variable value, severely hurting performance.

## Verification / Debugging
- GCC/Clang: Use `-fdump-record-layouts` to output the exact bit and byte offsets computed by the compiler for every struct member.
- In GDB: `ptype /o struct BoundaryCross` inspects internal bit offsets.

## Safety, Security, and Reliability
- Relying on implementation-defined layout violates safety directives across automotive (ISO 26262), aerospace (DO-178C), and medical (IEC 62304) domains.

## Trade-offs and Alternatives
- **Explicit Storage Layouts:** Structure packing with fixed-width integers and manual bit shifts eliminates all implementation-defined layout ambiguities.

## Staff-Level Takeaway
Never assume how a compiler will pack bit fields that exceed storage unit boundaries. If bit fields must be used, group them so that total widths cleanly sum to standard integer boundaries (8, 16, 32 bits), and lock the size with static assertions.

## Related Concepts
- `01_Bit_field_declaration`
- `03_Allocation_order`
- `06_Packed_structs`
