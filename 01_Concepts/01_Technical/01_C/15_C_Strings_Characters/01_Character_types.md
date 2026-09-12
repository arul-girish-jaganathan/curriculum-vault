# 01: Character Types

## Definition
Character types in ISO C comprise `char`, `signed char`, and `unsigned char`. Under ISO C (C99 §6.2.5p3), these three types are distinct. By definition, `sizeof(char) == 1`, serving as the basic addressable unit of execution memory. The signedness of the plain `char` type is implementation-defined.

## Scope and Boundaries
*   **Covers:** Signedness of `char`, distinct type semantics, character representations, range limits (`CHAR_MIN`, `CHAR_MAX`), and type aliasing exemptions.
*   **Does not cover:** Multi-byte and wide characters (see [[10_Wide_multibyte_characters]]), character constants (see [[02_Character_constants]]), or string literals (see [[03_String_literals]]).

## Why Does It Exist
C targets diverse hardware architectures:
*   **Hardware Architecture Parity:** Allowing compilers to map plain `char` to the CPU's most efficient native byte representation (signed on x86, often unsigned on ARM).
*   **Universal Memory Addressability:** `char *` and `unsigned char *` act as universal inspection pointers exempted from strict aliasing rules, enabling raw memory byte copying.

## Mechanism and Language Rules
1.  **Three Distinct Types:** `char`, `signed char`, and `unsigned char` are three distinct types for type checking and pointer compatibility, even though plain `char` has the same representation and values as either `signed char` or `unsigned char`.
2.  **Implementation-Defined Signedness:** Plain `char` may be signed or unsigned depending on the target architecture and compiler flags (`-funsigned-char` / `-fsigned-char`).
3.  **Basic Execution Character Set:** Guaranteed to fit within a single byte, with the null character (`\0`) having the value zero.
4.  **Aliasing Exemption (ISO C99 §6.5p7):** An object's stored value may be accessed by an lvalue of a character type (`char *`, `signed char *`, `unsigned char *`) without violating strict aliasing rules.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <limits.h>
#include <stdbool.h>

static bool example_char_signedness(void)
{
    /* Evaluates whether plain char is signed on target build */
    return (CHAR_MIN < 0);
}

/* Correct: Strict byte manipulation requires explicit unsigned char */
static void inspect_byte(const unsigned char *raw_byte)
{
    unsigned int val = *raw_byte;
    (void)val;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Implementation-Defined Behavior:** The signedness of plain `char`. The number of bits in a character type (`CHAR_BIT`, guaranteed to be $\ge 8$, exactly 8 on POSIX/modern MCUs).
*   **Undefined Behavior:** Relying on plain `char` sign extension or signed overflow when performing arithmetic.

## Edge Cases and Failure Modes
*   **The Negative Index Trap:** If `char` is signed, casting an ASCII or binary character $> 127$ (e.g., `0xFF`) to `int` sign-extends to a negative number (e.g., `-1`). Using it as an index into a lookup table (`table[c]`) accesses memory before the array, causing an out-of-bounds read.
*   **Type Incompatibility in Prototypes:** Passing `unsigned char *` to a function expecting `char *` triggers a constraint violation warning because they are incompatible pointer types.

## Embedded Implications
*   **ARM vs. x86 Inconsistency:** GCC on x86 defaults to `signed char`, while GCC on ARM Cortex-M defaults to `unsigned char`. Code developed on host simulators that relies on negative char values fails when deployed to ARM target hardware.
*   **Raw Hardware Buffers:** Communication drivers (UART, SPI) and memory pools must strictly use `uint8_t` or `unsigned char`, never plain `char`.

## Firmware Review Angle
1.  **Ban Plain `char` for Numeric Data:** Plain `char` must be reserved strictly for human-readable ASCII text strings. All binary data, byte arrays, and protocol buffers must use `uint8_t` or `unsigned char`.
2.  **Audit Table Lookups:** Verify that character arguments passed to lookup tables or `<ctype.h>` functions are explicitly cast to `(unsigned char)`.
3.  **Compiler Flag Consistency:** Verify cross-compilation toolchain flags (e.g., `-funsigned-char`) across all build variants.

## Compiler, ABI, and Toolchain Implications
*   **Register Promotion:** When passed to functions, character types are promoted to `int` under standard calling conventions (e.g., AAPCS).
*   **Vectorization:** Loop operations on `unsigned char` map directly to SIMD unsigned saturation instructions.

## Performance, Memory, Timing, and Power
*   **Zero Memory Penalty:** Character objects occupy exactly 1 byte.
*   **Branch Elimination:** Using `unsigned char` eliminates unnecessary sign-extension instructions (`SXTB` on ARM) before comparisons and arithmetic.

## Verification / Debugging
*   **Compiler Flags:** Use `-Wpointer-sign -Wtype-limits`.
*   **Static Analysis:** Analyzers flag array accesses where the index is an uncast plain `char`.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Directive 4.6:* Typedefs that indicate size and signedness shall be used (plain `char` permitted only for strings).
    *   *Rule 10.1:* Operands shall not be of an inappropriate essential type.
*   **Security Vulnerabilities:** CWE-125: Out-of-bounds Read due to sign-extended signed char indices.

## Trade-offs and Alternatives
*   **Plain `char` vs. `uint8_t`:**
    *   `char`: Standard C strings (`char *`), standard library interoperability.
    *   `uint8_t`: Defined signedness, guaranteed 8 bits, safe for binary arithmetic.

## Staff-Level Takeaway
Never use plain `char` for raw byte manipulation, cryptographic keys, or communications data. Staff engineers must enforce `uint8_t` / `unsigned char` across all hardware drivers and byte buffers, reserving plain `char` strictly for ASCII text, while ensuring that all table lookup indices derived from text are defensively cast to `unsigned char`.

## Related Concepts
*   [[02_Character_constants]]
*   [[03_String_literals]]
*   [[10_Wide_multibyte_characters]]
*   [[Memory Alignment and Padding]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
