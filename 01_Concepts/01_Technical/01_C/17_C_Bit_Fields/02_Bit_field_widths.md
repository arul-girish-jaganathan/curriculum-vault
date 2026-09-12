# 02: Bit Field Widths

## Definition
The bit-field width is an integer constant expression following the colon in a bit-field declaration. It specifies the exact number of bits allocated to the member. ISO C establishes strict boundaries on the minimum and maximum permitted width and defines special semantic behavior for zero-width bit fields.

## Scope and Boundaries
Covers: Width constant expression rules, maximum bit limits, zero-width bit field mechanics, storage unit boundary alignment, and truncation semantics.
Does not cover: Dynamic runtime bit extraction or bit masking without bit fields.

## Why Does It Exist
Hardware structures and communication protocols often define arbitrary field sizes (e.g., a 3-bit priority, a 12-bit ADC result, a 20-bit base address). Width specifiers allow exact sizing without requiring developers to manually maintain bit offsets across revisions.

## Mechanism and Language Rules
1. **Constant Expression:** The width must be an integer constant expression with a non-negative value: `width >= 0`.
2. **Width Ceiling:** The width cannot exceed the bit-width of the declared type:
   `width <= sizeof(type) * CHAR_BIT`. (e.g., an `unsigned int` bit field cannot exceed 32 bits on a 32-bit target).
3. **Zero-Width Bit Field (`: 0`):** An unnamed bit field with a width of 0 has a special standard meaning: it instructs the compiler to force alignment to the next storage unit boundary. It cannot have a name.
4. **Value Truncation:** Storing a value exceeding $2^{width} - 1$ in an unsigned bit field results in value truncation / modulo arithmetic ($val \pmod{2^{width}}$).

## Examples
```c
#include <stdint.h>
#include <assert.h>

struct BoundaryAlignment {
    unsigned int a : 4;  /* Bits 0..3 */
    unsigned int b : 4;  /* Bits 4..7 */
    unsigned int   : 0;  /* Forces alignment to next 32-bit storage unit */
    unsigned int c : 4;  /* Starts at bit 0 of next word (offset +4 bytes) */
};

static_assert(sizeof(struct BoundaryAlignment) == 8, "Expected 8 bytes due to zero-width field");

static void test_truncation(void) {
    struct BoundaryAlignment s;
    s.a = 19; /* 19 = 0x13 = 10011b -> truncated to 4 bits: 0011b = 3 */
    assert(s.a == 3);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Exceeding Type Width:** Declaring a width greater than `sizeof(type) * CHAR_BIT` is a constraint violation and must be rejected by the compiler.
- **Negative Width:** Declaring a negative width (e.g., `unsigned int a : -1;`) is a constraint violation.
- **Zero Width on Named Field:** Declaring a named field with width 0 (`unsigned int a : 0;`) violates ISO C constraints.

## Edge Cases and Failure Modes
- **Silent High-Bit Truncation:** Assigning calculated variables to narrow bit fields truncates the upper bits silently without runtime warnings or errors.
- **Off-By-One Field Widths:** Allocating 7 bits for a value whose valid maximum is 128 results in overflow (a 7-bit unsigned field maxes at 127).

## Embedded Implications
- **Zero-Width for Word Alignment:** Zero-width bit fields are useful in memory layouts where groups of flags must be segregated across distinct 32-bit or 16-bit register boundaries.
- **Register Truncation Hazards:** Assigning raw ADC counts or timer values to a bit field smaller than the incoming register width can silently discard critical high bits.

## Firmware Review Angle
- Confirm that every bit field has sufficient width to accommodate the maximum possible domain value (e.g., ensure an enum with 8 states uses at least 3 bits, or 4 bits if future expansion is planned).
- Verify that zero-width bit fields do not inadvertently double the structure size due to trailing storage unit alignment.

## Compiler, ABI, and Toolchain Implications
- The underlying container size assigned to zero-width alignment depends on the declared type: `uint32_t : 0` aligns to the next 32-bit boundary, while `uint8_t : 0` aligns to the next 8-bit boundary.

## Performance, Memory, Timing, and Power
- Truncation on assignment requires the compiler to emit `UBFX` (Unsigned Bit Field Extract) or `BFI` (Bit Field Insert) instructions, adding cycles to verify value masks.

## Verification / Debugging
- Static analysis checks for truncation risks: enable `-Wconversion` or `-Wbitfield-width` in GCC/Clang.
- Assert variable ranges before assigning to narrow bit fields.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 6.2: Signed bit fields shall have a length of at least 2 bits.
- Integer truncation (CWE-197) resulting from narrow bit fields can cause security flaws in authorization or length-checking logic.

## Trade-offs and Alternatives
- **Zero-Width Bit Field vs. Normal Struct Padding:** A zero-width bit field is self-documenting in bit-packed layouts, but normal integer dummy variables provide equal alignment guarantees without obscure bit-field syntax.

## Staff-Level Takeaway
Always size bit fields defensively to account for maximum value ranges. Use zero-width bit fields (`: 0`) deliberately to force storage-unit boundary termination, and guard all assignments from larger types with range validation to avoid silent truncation.

## Related Concepts
- `01_Bit_field_declaration`
- `03_Allocation_order`
- `05_Implementation_defined_layout`
