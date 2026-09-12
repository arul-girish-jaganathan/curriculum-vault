# String formatting

## Definition
String formatting converts typed values into character sequences using interfaces such as `snprintf`, `sprintf`, `printf`, `fprintf`, and related functions. It is broader than merely printing: formatted output can construct bounded strings for logs, diagnostics, user interfaces, or textual records. The format string defines conversion, width, precision, padding, and representation rules.

## Scope and Boundaries
* **Covers:** `snprintf`, `sprintf`, formatting strings, integer/string/pointer conversions, width and precision, truncation, and safe formatting patterns.
* **Does not cover:** formatted input (`scanf`) or general string manipulation functions.

## Why Does It Exist
Manual string construction is error-prone when values have variable widths or multiple representations. Formatting provides a consistent conversion mechanism for diagnostics and human-readable data while allowing callers to control presentation.

## Mechanism and language rules
`snprintf` writes at most `n` bytes including the terminating null byte when `n > 0`. Its return value is the number of characters that would have been produced excluding the null terminator, allowing the caller to detect truncation when the return value is nonnegative and at least the buffer capacity.

Conversion syntax includes flags, field width, precision, length modifiers, and a conversion specifier. Integer formatting should use `<inttypes.h>` macros for fixed-width integer types when portability across ABIs matters. `%s` consumes a null-terminated string and therefore cannot protect against an unterminated source by itself.

### What to reason about
- The destination size must be derived from the actual object, not guessed.
- `sprintf` has no size bound and should normally be avoided in safety-sensitive code.
- Truncation is a defined outcome of `snprintf`, not automatically an error; the caller must decide whether partial output is acceptable.
- Format strings are variadic type contracts; mismatched arguments can cause undefined behavior.
- Precision for `%s` can bound the number of characters read from a string, making it useful when constructing defensive output.
- Locale-sensitive formatting should not be allowed to silently change machine-readable records.

## Embedded implications
Formatting is often disproportionately expensive in firmware because integer division, floating-point conversion, buffering, and generic formatting machinery can pull large libc components into flash. It can also consume stack through temporary formatting state.

### Firmware review angle
Use fixed-size buffers and make truncation policy explicit. For high-rate logging, prefer a compact binary event record or preformatted numeric conversion rather than repeatedly invoking full `printf`. Measure flash, RAM, stack, and execution time before allowing formatting in an ISR-adjacent or hard-real-time path.

## Edge cases and failure modes
- `snprintf(buf, sizeof buf, "%s", src)` is safe with respect to destination bounds but still requires `src` to be a valid accessible null-terminated string.
- A return value larger than the buffer does not mean the buffer contains that many characters.
- `snprintf` returning a negative value indicates an encoding/output error in implementations where such errors are possible; do not cast it to `size_t` before checking.
- `%p`, integer length modifiers, and fixed-width integer formatting must follow the required argument types.
- Using a format string derived from untrusted input can create a format-string vulnerability.

## Example pattern
```c
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

static int make_message(char *dst, size_t cap, uint32_t count)
{
    int n = snprintf(dst, cap, "count=%" PRIu32, count);

    if (n < 0) {
        return -1;
    }
    return ((size_t)n < cap) ? 0 : 1; /* 1 = truncated */
}
```

## Verification / debugging
Test exact-fit, one-byte-too-small, zero-capacity, empty-string, maximum-integer, negative-integer, and malformed-input cases. Enable format warnings and review every format string/argument pair. Use map files to quantify the cost of adding formatting and a cycle counter/GPIO trace to quantify runtime cost on the target.

## Staff-level takeaway
Safe string formatting is primarily about bounding output, preserving type contracts, and defining what truncation means. A Staff engineer should avoid making generic formatting the hidden foundation of deterministic firmware logging or protocol generation; use a narrower representation when the system requires predictable resource usage.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[02_Formatted_output]]
[[15_C_Strings_Characters/00_Chapter_Index]]
