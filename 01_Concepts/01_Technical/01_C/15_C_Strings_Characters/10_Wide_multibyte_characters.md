# 10: Wide Multibyte Characters

## Definition
Wide and multibyte character systems represent text spanning character sets beyond basic 8-bit ASCII. In ISO C (C99 §7.24 and §7.27), a wide character (`wchar_t`, `char16_t`, `char32_t`) represents a code point in a uniform integer bit-width, whereas a multibyte character (e.g., UTF-8) represents a code point using a variable sequence of one or more 8-bit bytes.

## Scope and Boundaries
*   **Covers:** `wchar_t`, `char16_t`, `char32_t`, UTF-8 literals (`u8""`), conversion functions (`mbstowcs`, `wcstombs`, `c16rtomb`), and memory footprints.
*   **Does not cover:** Basic 8-bit ASCII characters (see [[01_Character_types]]), standard string copying (see [[06_String_copying]]), or international localization fonts.

## Why Does It Exist
Modern computing requires global language and symbol support:
*   **Unicode Standardization:** Representing alphabets, symbols, and emoji across international products.
*   **UTF-8 Universal Encoding:** Space-efficient transmission of international text over networks and communication buses while retaining backwards compatibility with 7-bit ASCII.
*   **Fixed-Width Processing:** Facilitating random-access indexing and text layout in GUI displays via fixed-width wide characters.

## Mechanism and Language Rules
1.  **`wchar_t` (Implementation-Defined Size):**
    *   Defined in `<stddef.h>`.
    *   Size is platform-dependent: 2 bytes (UTF-16) on Windows; 4 bytes (UTF-32) on Linux and most ARM toolchains.
2.  **C11 Fixed-Width Character Types (`<uchar.h>`):**
    *   `char16_t`: Unsigned integer of at least 16 bits, representing UTF-16 code units (`u"text"`).
    *   `char32_t`: Unsigned integer of at least 32 bits, representing UTF-32 code units (`U"text"`).
3.  **UTF-8 String Literals (C11):**
    *   `u8"text"`: Defines an array of UTF-8 encoded `char` (or `char8_t` in C23), terminated by `'\0'`.
4.  **Conversion APIs:** Functions like `mbstowcs` (multibyte to wide string) and `mbrlen` parse variable-width multibyte streams into wide character values based on the active locale.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stddef.h>
#include <uchar.h>
#include <stdint.h>

/* UTF-8 string literal: backward compatible with char* */
static const char *g_utf8_label = u8"Temp: 25°C";

/* Wide character string */
static const wchar_t g_wide_label[] = L"Temp: 25°C";

static size_t example_wide_size(void)
{
    /* Demonstrates memory footprint difference */
    size_t utf8_bytes = sizeof("Temp: 25°C");     /* ~12 bytes */
    size_t wide_bytes = sizeof(g_wide_label);      /* 11 * sizeof(wchar_t) = 44 bytes on 32-bit */

    return utf8_bytes + wide_bytes;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Implementation-Defined Behavior:** The size and signedness of `wchar_t`. The encoding scheme used for wide character literals (`L'a'`).
*   **Undefined Behavior:** Modifying wide string literals. Passing invalid state structures to restartable conversion routines (`mbrtowc`).
*   **Portability Pitfall:** Code assuming `sizeof(wchar_t) == 2` breaks when compiled on embedded GCC where `wchar_t` is 4 bytes.

## Edge Cases and Failure Modes
*   **The `wchar_t` RAM Multiplier:** Storing large user interface text tables as `wchar_t` in Flash or RAM on a microcontroller multiplies storage requirements by 2x or 4x compared to UTF-8.
*   **Byte-Indexing UTF-8 Strings:** In UTF-8, characters vary from 1 to 4 bytes. Accessing the $N$-th character via array subscript `str[n]` accesses the $N$-th *byte*, which may be an intermediate continuation byte, breaking glyph rendering on LCD screens.

## Embedded Implications
*   **Graphical Display Engines:** Embedded GUI frameworks (e.g., LVGL, TouchGFX) standardize internally on **UTF-8** strings for API parameters and label rendering, converting to glyph bitmaps via font lookups.
*   **Flash ROM Scarcity:** Wide strings (`wchar_t[]`) consume up to 4 bytes per character in Flash. Avoid wide strings; store international text as compact UTF-8 strings.
*   **Conversion Library Bloat:** Linking standard conversion functions (`mbstowcs`) pulls in large C-library localization tables, inflating binary ROM size by 20-50 KB.

## Firmware Review Angle
1.  **Enforce UTF-8 over `wchar_t`:** Reject `wchar_t` for storage and network transfer; mandate UTF-8 (`u8""` or standard `char *`).
2.  **No Direct UTF-8 Indexing:** Verify that GUI rendering code does not assume 1 byte equals 1 character when computing string lengths or truncating text.
3.  **Exclude Heavy Unicode Tables:** Verify linker map files to ensure full Unicode normalization/conversion tables are not inadvertently linked into bare-metal builds.

## Compiler, ABI, and Toolchain Implications
*   **Short Wchar Flag:** GCC provides `-fshort-wchar` to force `sizeof(wchar_t) == 2`. Using this breaks ABI compatibility with standard precompiled static libraries compiled with 4-byte `wchar_t`.
*   **Toolchain Sizing:** Verify whether your target ABI specifies `wchar_t` as `unsigned int` (ARM standard) or `unsigned short`.

## Performance, Memory, Timing, and Power
*   **Memory Footprint:** UTF-8 compresses standard ASCII to 1 byte per character, conserving precious microcontroller Flash and RAM.
*   **Processing Latency:** Fixed-width `char32_t` allows $O(1)$ random access, while UTF-8 requires sequential $O(N)$ decoding to find character boundaries.

## Verification / Debugging
*   **GDB Inspection:** GDB prints wide strings using `print (wchar_t*)p`.
*   **Compiler Warnings:** Use `-Wconversion -Wpedantic`.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 21.19:* The functions from `<locale.h>` shall not be used.
    *   *Rule 21.20:* The wide character and multibyte functions from `<wchar.h>` shall not be used unless required.
*   **Security Hazards:**
    *   CWE-176: Improper Handling of Unicode and Non-Standard Character Encodings. Buffer length miscalculations on multi-byte UTF-8 boundaries cause memory corruption.

## Trade-offs and Alternatives
*   **UTF-8 vs. `wchar_t` (UTF-32):**
    *   *UTF-8:* Memory-efficient, universal network compatibility, variable byte width.
    *   *UTF-32 (`char32_t`):* Fixed 4-byte width, trivial indexing, massive memory bloat.
    *   *Staff Recommendation:* Store and transmit text as UTF-8; decode on-the-fly only when rendering individual font glyphs.

## Staff-Level Takeaway
`wchar_t` is a non-portable architectural hazard due to compiler-dependent sizing (2 vs. 4 bytes) and massive memory bloat. Staff engineers must standardize embedded firmware on UTF-8 for international text storage, ban `-fshort-wchar` to preserve ABI compatibility, and ensure text layout engines never index multi-byte character sequences as raw byte offsets.

## Related Concepts
*   [[01_Character_types]]
*   [[03_String_literals]]
*   [[04_Null_termination]]
*   [[11_Buffer_sizing]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
