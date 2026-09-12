# 04: Signed Bit Fields

## Definition
A signed bit field is a structure bit field declared with an explicit `signed int` or plain `int` type. It represents a two's complement signed integer bounded by the specified bit-width, where the most significant bit acts as the sign bit.

## Scope and Boundaries
Covers: Two's complement representation in bit fields, sign extension, the infamous 1-bit signed bit-field bug, and range limits.
Does not cover: Floating-point bit-field representations (which are prohibited by ISO C).

## Why Does It Exist
Signed bit fields allow compact storage of signed telemetry metrics (e.g., a small temperature delta between -8°C and +7°C stored in 4 bits) without wasting an entire 8-bit or 32-bit integer.

## Mechanism and Language Rules
1. **Sign Bit:** The highest bit (bit position `width - 1`) represents the sign bit.
2. **Range Formula:** For a signed bit field of width $W$, the representable range in two's complement is:
   $$[-2^{W-1}, 2^{W-1} - 1]$$
3. **Sign Extension:** When a signed bit field is read in an expression, integer promotions automatically sign-extend the value to `int` or `unsigned int`.
4. **The 1-Bit Signed Trap:** A signed bit field of width 1 has a range of:
   $$[-2^{1-1}, 2^{1-1} - 1] = [-1, 0]$$
   It can represent ONLY `-1` and `0`. It CANNOT represent positive `1`.

## Examples
```c
#include <stdio.h>
#include <assert.h>

struct Metrics {
    /* Bug: plain int or signed int with width 1 */
    signed int error_flag : 1; 
    
    /* Correct: 4-bit signed value: Range -8 to +7 */
    signed int temp_delta : 4; 
};

static void test_signed_trap(void) {
    struct Metrics m;
    m.error_flag = 1; /* Assigning 1 */

    /* Trap: 1 is sign-extended to -1! */
    if (m.error_flag == 1) {
        /* This branch NEVER executes! */
        assert(0);
    }

    assert(m.error_flag == -1); /* m.error_flag actually holds -1 */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Plain `int` Bit Field:** Declaring `int flag : 1;` without an explicit `signed` or `unsigned` keyword has implementation-defined signedness. If the compiler defaults to signed, `flag = 1` sets the value to `-1`.
- **Signed Overflow:** Storing a value outside $[-2^{W-1}, 2^{W-1}-1]$ is signed integer overflow, which can invoke Undefined Behavior depending on standard interpretation and toolchain options.

## Edge Cases and Failure Modes
- **Boolean Check Failure:** Code using `if (m.error_flag == 1)` fails silently because the evaluated value is `-1`. Code checking `if (m.error_flag)` happens to work because non-zero evaluates to true, masking the underlying bug until an explicit equality check is introduced.
- **Sign Extension Distortion:** Promoting a negative signed bit field during math operations unexpectedly extends `1`s across the entire 32-bit register.

## Embedded Implications
- **Flag Corruption:** Using plain `int` for 1-bit boolean status fields in RTOS tasks or peripheral drivers causes logic inversions when evaluated against constants like `TRUE` (defined as `1`).

## Firmware Review Angle
- Immediately flag any 1-bit bit field that is declared as `signed int` or plain `int`.
- Verify that every boolean bit field is declared as `unsigned int : 1` or `_Bool : 1`.

## Compiler, ABI, and Toolchain Implications
- GCC and Clang will warn on `signed int : 1` when `-Woverflow` is enabled.
- Clang emits `-Wbitfield-constant-conversion` when assigning `1` to a 1-bit signed bit field.

## Performance, Memory, Timing, and Power
- Reading a signed bit field requires an explicit sign-extension instruction (`SBFX` on ARMv7-M / ARMv8-M), which extracts the bit field and propagates the sign bit across the register in a single cycle.

## Verification / Debugging
- Static analysis (Coverity, PC-lint, Clang-Tidy) catches 1-bit signed bit-field traps.
- Clang-Tidy check: `readability-simplify-boolean-expr` or compiler warning `-Wconstant-logical-operand`.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 6.1: Bit fields shall only be declared with an explicitly signed or unsigned integer type.
- MISRA C:2012 Rule 6.2: Signed bit fields shall have a length of at least 2 bits. (Specifically written to eliminate the 1-bit signed bit-field trap).

## Trade-offs and Alternatives
- If a flag is boolean, use `unsigned int : 1` or C99 `_Bool : 1`. Never allow signedness for booleans.

## Staff-Level Takeaway
Never allow 1-bit signed bit fields under any circumstances. A 1-bit signed field cannot store positive `1`, breaking standard boolean equality logic. Always declare single-bit flags as `unsigned int` or `_Bool`.

## Related Concepts
- `01_Bit_field_declaration`
- `02_Bit_field_widths`
- `12_Safe_bit_field_policy`
