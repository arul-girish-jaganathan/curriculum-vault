# 02: Character Constants

## Definition
A character constant is an integer constant composed of one or more characters enclosed in single quotes (e.g., `'a'`, `'\n'`). In ISO C (C99 §6.4.4.4), an integer character constant has type `int` (unlike C++, where it has type `char`), and its value is the numerical execution character set mapping of the character.

## Scope and Boundaries
*   **Covers:** Single-character constants, escape sequences, multi-character constants, type differences (`int` in C vs. `char` in C++), and prefix types (`u8'`, `L'`, `u'`, `U'`).
*   **Does not cover:** String literals (see [[03_String_literals]]), wide character arrays (see [[10_Wide_multibyte_characters]]), or character type signedness (see [[01_Character_types]]).

## Why Does It Exist
Programmers need symbolic, readable representations of individual character values:
*   **Readability:** Writing `'A'` instead of hardcoded magic number `65` (ASCII).
*   **Portability:** Decoupling source code from the target's underlying execution character encoding.
*   **Control Characters:** Representing non-printable escape sequences (`'\r'`, `'\n'`, `'\t'`) symbolically.

## Mechanism and Language Rules
1.  **Type is `int` (Critical ISO C Rule):** The expression `'a'` has type `int`. Consequently, `sizeof('a') == sizeof(int)` (typically 4 bytes on 32-bit systems), NOT 1.
2.  **Value Mapping:** The value of `'a'` is determined by the target execution character set (almost universally ASCII/UTF-8 in modern systems).
3.  **Escape Sequences:**
    *   Simple: `\'`, `\"`, `\?`, `\\`, `\a`, `\b`, `\f`, `\n`, `\r`, `\t`, `\v`.
    *   Octal: `\ooo` (up to 3 octal digits).
    *   Hexadecimal: `\xhh` (arbitrary hexadecimal digits, terminating at the first non-hex character).
4.  **Multi-Character Constants:** Constructs like `'AB'` or `'abcd'` are permitted by ISO C, have type `int`, and have implementation-defined values.
5.  **C11/C23 Prefixes:**
    *   `u8'a'`: UTF-8 character constant (type `unsigned char` in C23).
    *   `L'a'`: Wide character constant (type `wchar_t`).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stddef.h>
#include <stdbool.h>

static bool example_char_const_rules(void)
{
    /* In ISO C, sizeof('a') evaluates to sizeof(int), NOT 1 */
    bool is_int_sized = (sizeof('a') == sizeof(int));

    /* Escape sequences evaluate to fixed values */
    char cr = '\r';
    char nl = '\n';

    (void)cr;
    (void)nl;
    return is_int_sized;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Implementation-Defined Behavior:** The value of an integer character constant containing more than one character (e.g., `'ABCD'`). The value of a character constant containing a character not in the basic execution character set.
*   **Undefined Behavior:** A hexadecimal escape sequence whose value exceeds the range of the character type.

## Edge Cases and Failure Modes
*   **C vs. C++ Incompatibility:** In C, `sizeof('a') == sizeof(int)`. In C++, `sizeof('a') == sizeof(char) == 1`. Code compiled conditionally across both languages that uses `sizeof('a')` produces structural divergences.
*   **Multi-Character Endianness Trap:** Writing `uint32_t tag = 'ABCD';` produces different 32-bit integer values on Big-Endian vs. Little-Endian architectures, breaking file format parsers.
*   **Unbounded Hex Escapes:** In `"\x12" "34"`, the hex escape consumes hex digits until a non-hex character is reached; separating adjacent literal components prevents overflow.

## Embedded Implications
*   **Protocol Sentinels:** Embedded protocols frequently check framing delimiters using character constants:
    ```c
    if (rx_byte == '\n' || rx_byte == '\r') { process_packet(); }
    ```
*   **Magic Number Flags:** In firmware bootloaders, packing four characters into an integer (FourCC) via `'BOOT'` is common, but must be replaced by explicit bitwise shifts for endian safety:
    ```c
    #define MAGIC_BOOT (((uint32_t)'B' << 24) | ((uint32_t)'O' << 16) | ...)
    ```

## Firmware Review Angle
1.  **Ban Multi-Character Constants:** Reject code containing `'ABCD'`; enforce explicit byte arrays or endian-safe shift macros.
2.  **Check `sizeof('c')` Assumptions:** Verify that developers do not write code assuming `sizeof('a') == 1`.
3.  **Hex Escape Boundaries:** Scrutinize hex escape sequences to ensure they do not accidentally consume following valid hex characters.

## Compiler, ABI, and Toolchain Implications
*   **Constant Folding:** Character constants are evaluated entirely at compile-time as immediate integer operands (`MOVS r0, #65`).
*   **Execution Character Set Mapping:** Compilers support `-fexec-charset=...` to remap character constant numerical values at compile time.

## Performance, Memory, Timing, and Power
*   **Zero Memory Footprint:** Generates immediate instruction operands; consumes zero RAM or Flash memory lookup space.
*   **Single-Cycle Comparisons:** Character comparisons map directly to single-cycle immediate compare instructions (`CMP r0, #10`).

## Verification / Debugging
*   **Compiler Flags:** Use `-Wmultichar -Wpedantic`.
*   **Disassembly Inspection:** Verify that comparisons against character constants compile to immediate constants.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 10.1:* Operands shall not be of an inappropriate essential type.
    *   *Rule 10.3:* The value of an expression shall not be assigned to an object with a narrower essential type.
*   **Reliability Risk:** Endian-dependent evaluation of multi-character constants causes protocol decoders to misbehave across processor variants.

## Trade-offs and Alternatives
*   **Character Constants vs. Hex Literals:**
    *   `'A'`: Clear semantic intent for human-readable ASCII protocols.
    *   `0x41U`: Explicit numerical byte representation for binary protocols and hardware registers.

## Staff-Level Takeaway
In ISO C, character constants are of type `int`. Staff engineers must prohibit multi-character constants (`'ABCD'`) due to architecture-specific endian hazards, enforce explicit bit-shifting for protocol magic words, and ensure that character constant comparisons are applied strictly to ASCII text streams.

## Related Concepts
*   [[01_Character_types]]
*   [[03_String_literals]]
*   [[04_Null_termination]]
*   [[10_Wide_multibyte_characters]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
