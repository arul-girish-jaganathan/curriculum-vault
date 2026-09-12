# 09: Locale Sensitive Character APIs

## Definition
Locale-sensitive character APIs are the standard library character classification and transformation functions declared in `<ctype.h>` (e.g., `isalpha`, `isdigit`, `tolower`, `toupper`). In ISO C (C99 §7.4), the behavior of these functions is governed by the current execution locale established via `setlocale()` in `<locale.h>`.

## Scope and Boundaries
*   **Covers:** `<ctype.h>` classification and conversion functions, domain requirements (`unsigned char` or `EOF`), locale dependencies, and embedded ASCII alternatives.
*   **Does not cover:** Wide character classifications (`<wctype.h>`), string collation (`strcoll`), or full Unicode localization libraries (ICU).

## Why Does It Exist
Operating systems serve international user bases:
*   **Linguistic Variations:** Handling culture-specific capitalization and punctuation rules (e.g., German umlauts or French accents).
*   **Abstraction:** Providing standardized character property queries without hardcoding ASCII ranges.

## Mechanism and Language Rules
1.  **Domain Requirement (CRITICAL ISO C RULE):** For all functions in `<ctype.h>`, the argument `c` must be representable as an `unsigned char` or must equal the value of the macro `EOF` (C99 §7.4p1). Passing any other value invokes **undefined behavior**.
2.  **Execution Locale:** In the default `"C"` locale (the only locale guaranteed in bare-metal embedded systems), character behaviors match standard 7-bit US-ASCII.
3.  **Return Semantics:**
    *   Classification functions return a non-zero integer (`true`) if the character matches, or `0` (`false`) if not.
    *   Transformation functions (`tolower`, `toupper`) return the converted character as an `int`, or return the original argument unchanged if no mapping exists.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <ctype.h>
#include <stdbool.h>

/* Correct: Safe ctype usage with mandatory unsigned char cast */
static bool safe_is_digit(char c)
{
    /* Cast to unsigned char prevents UB on signed char architectures */
    return isdigit((unsigned char)c) != 0;
}

/* Correct: Safe lowercase conversion */
static char safe_to_lower(char c)
{
    return (char)tolower((unsigned char)c);
}

/* Incorrect: Undefined behavior trap */
static bool invalid_check(char c)
{
    /* If c < 0 (e.g., c = 0xFF on signed char target), this is UNDEFINED BEHAVIOR */
    return isalpha(c);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior (The Signed Char Trap):** Passing a plain `char` with a negative numerical value (e.g., `(char)0x80` where `char` is signed) to `isdigit(c)`. Most implementations implement `<ctype.h>` as a 256-entry array lookup offset by `+1` (for `EOF = -1`). A negative value $< -1$ reads memory out of bounds preceding the table, causing crashes or memory corruption.
*   **Implementation-Defined Behavior:** Character classifications outside the basic ASCII range (characters $> 127$) in non-default locales.

## Edge Cases and Failure Modes
*   **The Missing `(unsigned char)` Cast:** The most widespread bug in C string parsing. On x86 or ARM targets configured with signed `char`, processing binary or UTF-8 data through `isspace(c)` crashes unpredictably when high-bit bytes are encountered.
*   **The Turkish "I" Problem:** In full-featured OS environments with Turkish locale active, `tolower('I')` does not yield `'i'`, breaking case-insensitive protocol decoders (e.g., HTTP headers).

## Embedded Implications
*   **Locale Overhead:** Full locale support requires multi-kilobyte lookup tables in Flash. Embedded C libraries (e.g., newlib-nano) lock `<ctype.h>` permanently to the `"C"` locale to save ROM.
*   **Table-Driven Overhead:** Calling `isalpha()` generates array lookups in Flash. Simple bitwise or range checks are faster and consume zero Flash table space:
    ```c
    static inline bool is_ascii_digit(char c) { return (c >= '0' && c <= '9'); }
    ```

## Firmware Review Angle
1.  **Mandate `(unsigned char)` Cast:** Every call to `<ctype.h>` functions must wrap its argument in `(unsigned char)`.
2.  **Prefer Explicit ASCII Checks:** For deterministic protocol parsing (AT commands, HTTP, Modbus), mandate explicit ASCII helper functions over `<ctype.h>` to avoid locale sensitivity.
3.  **Reject `setlocale`:** Ensure embedded codebases do not invoke `setlocale()`, which can disrupt parsing logic across RTOS tasks.

## Compiler, ABI, and Toolchain Implications
*   **Lookup Table Lowering:** Standard libraries implement `<ctype.h>` via internal arrays (e.g., `_ctype_ + 1`). Passing negative integers accesses memory before `_ctype_`.
*   **Compiler Built-in Optimization:** GCC and Clang can inline basic ASCII checks (`c >= '0' && c <= '9'`) when optimization is enabled and the `"C"` locale is guaranteed.

## Performance, Memory, Timing, and Power
*   **Memory Footprint:** Custom ASCII range checks require 0 lookup tables in ROM. Standard library locale tables consume 256 to 1024 bytes of Flash.
*   **Cycle Latency:** Simple range checks (`c >= 'a' && c <= 'z'`) execute in 1-2 CPU cycles directly inside registers without memory load operations.

## Verification / Debugging
*   **Sanitizers:** Compile with UndefinedBehaviorSanitizer (`-fsanitize=undefined`) to catch negative arguments passed to `<ctype.h>` routines.
*   **Static Analysis:** Tools like Clang-Tidy (e.g., `bugprone-string-integer-assignment`) flag uncast character inputs.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Directive 4.6:* Typedefs that indicate size and signedness should be used.
*   **Security Vulnerabilities:**
    *   CWE-125: Out-of-bounds Read (via negative array indexing in `<ctype.h>` lookup tables).

## Trade-offs and Alternatives
*   **`<ctype.h>` vs. Hardcoded ASCII Helpers:**
    *   `<ctype.h>`: Standard, internationalizable, prone to undefined behavior if uncast.
    *   *Hardcoded ASCII Helpers:* 100% deterministic, zero table overhead, immune to signedness UB, strictly bounded to ASCII.
    *   *Staff Recommendation:* Use dedicated ASCII range functions for all embedded protocol parsing.

## Staff-Level Takeaway
`<ctype.h>` is a notorious source of undefined behavior because its functions accept `int` but strictly require arguments in the range of `unsigned char` or `EOF`. Staff engineers must mandate explicit `(unsigned char)` casts for all `<ctype.h>` calls or replace them entirely with deterministic, zero-overhead ASCII range macros for embedded protocol parsing.

## Related Concepts
*   [[01_Character_types]]
*   [[02_Character_constants]]
*   [[12_Embedded_string_handling]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
