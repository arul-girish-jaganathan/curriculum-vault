# locale.h

> Canonical C topic note — chapter 31.

## Definition
`locale.h` defines the C locale mechanism. `setlocale` selects or queries locale settings and `localeconv` exposes locale-dependent numeric and monetary formatting information. The standard defines categories such as `LC_CTYPE`, `LC_NUMERIC`, `LC_TIME`, `LC_COLLATE`, `LC_MONETARY`, and `LC_ALL`, but available locale names, data, encodings, and libc support are implementation-specific. The initial locale is the `"C"` locale.

## Mechanism and language rules
```c
#include <locale.h>

if (setlocale(LC_ALL, "C") == NULL) {
    /* Requested locale unavailable. */
}

struct lconv *info = localeconv();
```

Passing a null locale name queries the current setting. A successful `setlocale` returns a library-managed string describing the resulting locale. `localeconv` returns library-managed formatting information.

### What to reason about
- Locale is library/global state rather than metadata attached to each string.
- Categories have distinct effects; `LC_ALL` can change several at once.
- Locale names and installed locale data are not portable assumptions.
- C locale behavior is not equivalent to Unicode or UTF-8 support.
- `localeconv` data is owned by the implementation.
- Concurrent locale changes require implementation-specific consideration.
- Human presentation and machine protocol formatting should normally be separate concerns.

## Embedded implications
Dynamic locale support can add substantial libc code, locale tables, RAM, and initialization complexity. Most embedded protocols require deterministic output and should not depend on mutable process-wide locale state.

For firmware, use explicit protocol encodings, fixed decimal conventions, and explicit character assumptions. Enable locale functionality only when the product genuinely needs localized human-facing behavior.

### Firmware review angle
Check libc/target support, code-size and RAM impact, locale initialization, concurrent access, deterministic boot behavior, and whether serialized data changes when locale state changes.

## Edge cases and failure modes
Do not assume a requested locale such as `en_US.UTF-8` exists on every target. A failed `setlocale` must be handled rather than silently assumed successful.

Locale-sensitive formatting is a poor choice for persistent or wire data because decimal separators, collation, and classification may vary. Global state can also surprise unrelated modules that expect the `"C"` locale.

## Example pattern
Keep machine-readable formatting explicit:

```c
/* A protocol specifies '.' regardless of user locale. */
int format_temperature(char *dst, size_t cap, int milli_celsius)
{
    return snprintf(dst, cap, "%d.%03d",
                    milli_celsius / 1000,
                    milli_celsius % 1000);
}
```

## Verification / debugging
Run tests under every supported locale and compare serialized output byte-for-byte. Measure flash/RAM impact on each MCU configuration and verify failure behavior when locale data is unavailable.

Staff-level review questions:
- Is this output for a human or a machine?
- Can locale state leak across module boundaries?
- What is the deterministic protocol representation?
- What happens if locale selection fails?
- Is the target libc actually providing the required locale data?

## Staff-level takeaway
`locale.h` is a controlled interface to locale-dependent library behavior, not a complete internationalization framework. In embedded systems, isolate it at human-interface boundaries and keep protocols, persistent formats, diagnostics consumed by automation, and device interfaces explicitly deterministic.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
