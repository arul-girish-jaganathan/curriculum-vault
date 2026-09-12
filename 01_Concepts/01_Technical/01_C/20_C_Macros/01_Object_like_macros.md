# 01: Object-Like Macros

## Definition
An object-like macro is an identifier defined with `#define` that is replaced by a sequence of tokens whenever encountered in the source code outside of string literals and comments. It takes no parameters and behaves lexically like an untyped constant or symbolic alias.

## Scope and Boundaries
Covers: Constant definitions, explicit literal typing (`U`, `UL`, `ULL`), configuration parameters, memory buffer bounds, and preprocessor token replacement.
Does not cover: Function-like macros (see `02_Function_like_macros`) or `const` variables.

## Why Does It Exist
Object-like macros eliminate magic numbers, centralize configuration tunables (e.g., buffer capacities, timeout limits), and parameterize hardware addresses across different board targets without requiring storage allocation in RAM or Flash.

## Mechanism and Language Rules
1. **Replacement Rule:** The preprocessor replaces the exact identifier with its replacement list throughout Translation Phase 4.
2. **Untyped Replacement:** The macro itself has no C type. The type of the replaced text is determined by the literal's form or the surrounding context.
3. **Integer Literal Suffixes:** Unadorned integer literals default to `int` or `long`. In embedded systems, signedness issues occur unless explicit suffixes are appended:
   - `U` for `unsigned int`
   - `UL` for `unsigned long`
   - `ULL` for `unsigned long long`
4. **No Storage Allocation:** Object-like macros allocate no memory. They exist strictly in the preprocessor's symbol table.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* HAZARDOUS: Untyped literals without suffixes or parentheses */
#define BAD_BUFFER_SIZE     1024
#define BAD_OFFSET          10 + 2
#define BAD_MASK            1 << 31 /* Triggers signed integer overflow! */

/* CORRECT: Parenthesized with explicit integer suffixes */
#define SAFE_BUFFER_SIZE    (1024U)
#define SAFE_OFFSET         (10U + 2U)
#define SAFE_MASK           (1UL << 31U)

/* Hardware base address abstraction */
#define PERIPH_BASE_ADDR    (0x40000000UL)
#define UART0_BASE_ADDR     (PERIPH_BASE_ADDR + 0x1000UL)

static void test_object_macros(void) {
    /* BAD_OFFSET * 2 expands to: 10 + 2 * 2 = 14! */
    assert((BAD_OFFSET * 2) == 14);

    /* SAFE_OFFSET * 2 expands to: (10U + 2U) * 2 = 24 */
    assert((SAFE_OFFSET * 2) == 24);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Signed Integer Overflow:** Defining a mask as `(1 << 31)` on a 32-bit architecture shifts into the sign bit of a signed 32-bit `int`, provoking Undefined Behavior in ISO C. Always use `(1UL << 31U)`.
- **Macro Redefinition:** Defining the same macro identifier twice in the same scope with differing replacement lists triggers a compiler diagnostic error.

## Edge Cases and Failure Modes
- **Operator Precedence Breakage:** Defining `#define TIMEOUT 1000 + 50` leads to math errors when used in expressions like `uint32_t total = TIMEOUT * 2;` (evaluates as `1000 + 50 * 2 = 1100`). Always wrap in parentheses.
- **Accidental String Insertion:** Writing `#define VALUE 42;` with a trailing semicolon injects unwanted semicolons into expressions: `int x = VALUE;` expands to `int x = 42;;` which can break single-statement `if` conditions.

## Embedded Implications
- **Flash vs RAM Footprint:** In contrast to global `const` variables (which may occupy Flash memory in `.rodata`), numeric object-like macros are emitted as immediate operands inside CPU machine instructions (`MOVS R0, #42`), consuming zero data memory.
- **Bitmask Correctness:** Register masks mapped via macros must use unsigned types (`1u << n`) to avoid sign extension bugs when written to 32-bit MMIO registers.

## Firmware Review Angle
- Verify that EVERY numeric macro has an explicit unsigned suffix (`U`, `UL`) if representing sizes, counts, masks, or memory addresses.
- Verify that every compound arithmetic replacement list is enclosed in outer parentheses: `((A) + (B))`.
- Reject any macro ending with a trailing semicolon.

## Compiler, ABI, and Toolchain Implications
- Object-like macros are erased before code generation; they are completely invisible to the linker and ABI.
- Compiling with `-g3` preserves macro definitions inside DWARF debug symbols, enabling debuggers to evaluate macro names in watch expressions.

## Performance, Memory, Timing, and Power
- Absolute zero runtime overhead. Generates inline immediate assembly constants.

## Verification / Debugging
- Compiler warnings: Enable `-Wshift-overflow` and `-Woverflow` to catch missing unsigned suffixes.
- GDB command: `macro expand MACRO_NAME` verifies substitution values.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 12.2: The right-hand operand of a shift operator shall lie in the range 0 to one less than the width in bits of the essential type of the left-hand operand.
- MISRA C:2012 Rule 10.1: Unsigned types must be used for bitwise operations.

## Trade-offs and Alternatives
- **Object Macro vs `static const` / `enum`:**
  - `enum { BUFFER_SIZE = 1024 };` provides a typed, debuggable constant that allocates no RAM.
  - `static const uint32_t BufferSize = 1024U;` provides strict type enforcement and addressability, but may consume `.rodata` Flash space if the compiler decides not to inline.

## Staff-Level Takeaway
Never define a numeric macro without defensive outer parentheses and explicit literal typing suffixes (`U`, `UL`). For scalar integer constants in pure C, prefer anonymous enumerations (`enum { VAL = 100U };`) or `static const` variables to preserve type safety and debugger visibility.

## Related Concepts
- `03_Parentheses_discipline`
- `10_Macro_namespaces`
- `11_When_inline_functions_are_safer`
