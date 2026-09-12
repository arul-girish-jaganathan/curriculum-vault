# 09: Mask and Shift Alternatives

## Definition
The mask-and-shift pattern is the industry-standard methodology for inspecting, setting, clearing, and toggling sub-byte fields using explicit bitwise operators (`&`, `|`, `~`, `^`, `<<`, `>>`) applied to standard fixed-width integer types (`uint8_t`, `uint16_t`, `uint32_t`, `uint64_t`).

## Scope and Boundaries
Covers: Bitmask construction, shift operations, bitfield insertion and extraction idioms, read-modify-write encapsulation, and type safety.
Does not cover: Assembly-level bitband manipulation or compiler-specific bitwise intrinsics.

## Why Does It Exist
Unlike C bit fields, bitwise mask-and-shift operations have strictly defined, 100% portable semantics defined by the ISO C standard. They guarantee exact memory bus access widths, eliminate compiler allocation ambiguities, and are immune to endianness variations within the CPU word.

## Mechanism and Language Rules
1. **Bitmask Definition:** Defined using bit shifts: `(1u << bit_position)`.
2. **Field Extraction:** Shift target bits to the zero position, then mask:
   `val = (reg >> SHIFT) & MASK;`.
3. **Field Insertion (Clear then Set):**
   `reg = (reg & ~(MASK << SHIFT)) | ((val & MASK) << SHIFT);`.
4. **Unsigned Arithmetic:** Bitwise operations must always be performed on `unsigned` integer types to prevent undefined behavior from signed integer overflow or arithmetic right-shift sign extension.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Clean Mask and Shift Architecture */
#define TIMER_CTRL_ENABLE_POS     (0u)
#define TIMER_CTRL_ENABLE_MSK     (0x1u << TIMER_CTRL_ENABLE_POS)

#define TIMER_CTRL_MODE_POS       (1u)
#define TIMER_CTRL_MODE_MSK       (0x7u << TIMER_CTRL_MODE_POS)

#define TIMER_CTRL_PRESCALER_POS  (4u)
#define TIMER_CTRL_PRESCALER_MSK  (0xFu << TIMER_CTRL_PRESCALER_POS)

/* Helper inline functions provide type safety and readability */
static inline uint32_t timer_get_mode(uint32_t reg_val) {
    return (reg_val & TIMER_CTRL_MODE_MSK) >> TIMER_CTRL_MODE_POS;
}

static inline uint32_t timer_set_mode(uint32_t reg_val, uint32_t mode) {
    return (reg_val & ~TIMER_CTRL_MODE_MSK) | ((mode << TIMER_CTRL_MODE_POS) & TIMER_CTRL_MODE_MSK);
}

static void configure_timer(void) {
    uint32_t reg = 0;
    reg |= TIMER_CTRL_ENABLE_MSK;             /* Set enable bit */
    reg = timer_set_mode(reg, 0x05u);         /* Insert 3-bit mode */
    
    assert(timer_get_mode(reg) == 0x05u);
    assert(reg & TIMER_CTRL_ENABLE_MSK);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Shifting by >= Word Width:** Shifting an operand by an amount greater than or equal to its bit-width (`1u << 32` on a 32-bit type) invokes Undefined Behavior.
- **Signed Left Shifts:** Left-shifting a signed negative value or shifting into the sign bit invokes Undefined Behavior in ISO C. Always use unsigned integer constants (`1u`).

## Edge Cases and Failure Modes
- **Missing Unsigned Suffix:** Writing `(1 << 31)` instead of `(1u << 31)` causes signed integer overflow on 32-bit systems, triggering undefined behavior.
- **Operator Precedence Pitfall:** Bitwise operators have lower precedence than comparison operators (`if (reg & MASK == 0)` evaluates as `reg & (MASK == 0)`). Always parenthesize bitwise expressions.

## Embedded Implications
- **Atomic Set/Clear Integration:** Mask-and-shift macros directly translate to hardware bit-set/bit-clear registers (e.g., `GPIO->BSRR = PIN_MASK;`).
- **Deterministic Bus Cycles:** Unlike bit fields, an assignment using a mask-and-shift expression to a `volatile uint32_t *` guarantees exactly one 32-bit bus transaction.

## Firmware Review Angle
- Confirm that every bitmask macro uses an explicit unsigned suffix (`u` or `UL`).
- Check that all compound bitwise expressions are enclosed in parentheses: `((val) & (MASK))`.

## Compiler, ABI, and Toolchain Implications
- Modern optimizing compilers recognize extraction/insertion idioms and automatically synthesize native bitfield instructions (such as `UBFX`, `SBFX`, `BFI` on ARM).

## Performance, Memory, Timing, and Power
- Bitwise masks compile into optimal, deterministic assembly instructions with zero hidden memory fetches.

## Verification / Debugging
- Unit tests can thoroughly exercise mask macros across all bit positions.
- Static analysis flags missing parentheses and signed shift expressions.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 12.2: The right hand operand of a shift operator shall lie in the range zero to one less than the width in bits of the essential type of the left hand operand.
- MISRA C:2012 Rule 10.1: Bitwise operations shall only be performed on operands of unsigned essential type.

## Trade-offs and Alternatives
- Mask and shift requires slightly more boilerplate code than bit fields, but provides complete predictability, thread-safety, and hardware conformance.

## Staff-Level Takeaway
Mask-and-shift operations on fixed-width unsigned integers represent the golden standard for low-level systems engineering. Wrap shifts and masks in well-named inline functions or macros to achieve the readability of bit fields with none of their portability and concurrency risks.

## Related Concepts
- `01_Bit_field_declaration`
- `08_MMIO_bit_fields`
- `10_Atomicity_limitations`
