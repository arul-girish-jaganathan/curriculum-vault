# Formatted output

## Definition
Formatted output is the family of `<stdio.h>` interfaces that convert C values into character sequences according to a format string. The core interfaces are `printf`, `fprintf`, `sprintf`, `snprintf`, and their `v*` variants. The format string is a runtime description of expected argument types and presentation rules; it is not type-checked by the C language itself in the same way as an ordinary function prototype.

## Scope and Boundaries
* **Covers:** format strings, conversions, flags, width, precision, length modifiers, return values, `printf`/`fprintf`/`snprintf`, and variadic argument contracts.
* **Does not cover:** the full variadic-function ABI, which belongs in Chapter 33, or filesystem buffering details beyond what formatted output needs.

## Why Does It Exist
Embedded and hosted programs frequently need to turn integers, floating-point values, pointers, and text into human-readable diagnostics or protocol-adjacent representations. Formatted output provides a standardized interface instead of requiring every application to implement decimal conversion, padding, alignment, and field formatting independently.

## Mechanism and language rules
A call such as `printf("id=%lu\\n", value)` uses a format string to determine how the variadic arguments are fetched. The fixed parameter list gives the compiler limited information; the format string supplies the remaining type contract. Default argument promotions apply to variadic arguments, so `float` becomes `double` and integer types narrower than `int` are promoted according to the usual rules.

Important conversions include `%d`/`%i` for signed integer values, `%u` for unsigned, `%x`/`%X` for hexadecimal, `%c`, `%s`, `%p`, and floating conversions such as `%f`. Length modifiers (`hh`, `h`, `l`, `ll`, `j`, `z`, `t`, `L`) select the expected argument type. `snprintf` limits writes to a supplied destination size and is usually the preferred bounded string-formatting primitive.

### What to reason about
- The format specifier and actual argument type must agree with the variadic contract; mismatches can be undefined behavior.
- `%p` expects a `void *`; use the required conversion rather than guessing that every pointer representation is interchangeable in a variadic call.
- `%s` requires a pointer to a null-terminated character sequence; it does not carry a length.
- `snprintf` returns the number of characters that would have been written, excluding the terminating null character, when successful. A return value greater than or equal to the destination size indicates truncation.
- A zero-sized destination with `snprintf` can be used for sizing, provided the destination pointer rules of the implementation are respected.
- Locale can affect some formatted representations on hosted implementations; protocol formatting should not accidentally depend on ambient locale.

## Embedded implications
Formatted output can be one of the largest accidental flash consumers in firmware. Integer conversion, floating-point formatting, locale support, buffering, and reentrancy support may pull substantial portions of libc into the image. Floating-point formatting is particularly expensive on many embedded toolchains.

`printf` may also introduce blocking latency through UART/USB output and can make timing-sensitive code nondeterministic. Prefer bounded, purpose-built diagnostic encoders for high-rate telemetry and protocol paths.

### Firmware review angle
Inspect the map file to determine what the chosen libc implementation actually links. Compare `%f` versus integer/scaled-unit formatting, and measure worst-case execution time for long messages. Verify behavior across 32-bit and 64-bit builds because length modifiers and integer widths matter.

## Edge cases and failure modes
- `printf("%d", unsigned_value)` is not a harmless signed/unsigned presentation choice; the variadic type contract is wrong.
- `printf("%s", buffer)` is unsafe if `buffer` is not guaranteed to be null-terminated.
- `sprintf` has no destination-size limit and can overflow the destination object.
- Assuming `snprintf` returns the number actually stored causes incorrect truncation handling.
- `%zu` is the portable way to print a `size_t`; hard-coding `%u` assumes a particular representation.
- Logging attacker-controlled strings as format strings (`printf(user_input)`) creates format-string vulnerabilities.
- Output generated for a machine protocol should not depend on localized decimal conventions.

## Example pattern
```c
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

static int format_status(char *dst, size_t cap, uint32_t id)
{
    int n = snprintf(dst, cap, "id=%" PRIu32, id);
    if (n < 0) {
        return -1;
    }
    if ((size_t)n >= cap) {
        return 1; /* truncated */
    }
    return 0;
}
```

## Verification / debugging
Enable compiler format checking where supported, such as GCC/Clang `-Wformat -Wformat-security -Wformat-signedness`. Unit-test every truncation boundary and verify negative, maximum-width, zero, and large-value cases. Review format strings as API contracts, not as presentation-only text.

For firmware, compare map-file size before and after enabling formatted output and measure latency with a GPIO trace or cycle counter when it runs in performance-sensitive paths.

## Staff-level takeaway
Formatted output is a type-unsafe variadic interface wrapped in a powerful mini-language. A Staff engineer should control the format contract, destination bounds, error/truncation semantics, code-size impact, and timing behavior. Use it freely for controlled diagnostics, but isolate it from deterministic protocol and real-time paths unless its cost is measured and accepted.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[33_C_Variadic_Functions/00_Chapter_Index]]
