# Formatted input

## Definition
Formatted input uses `<stdio.h>` functions such as `scanf`, `fscanf`, `sscanf`, and their `v*` variants to parse character input according to a format string and store converted results through caller-supplied pointers. Unlike formatted output, input conversion writes into application objects, so destination type, lifetime, bounds, and input termination are critical parts of the contract.

## Scope and Boundaries
* **Covers:** `scanf` family semantics, conversion specifiers, assignment suppression, field widths, return values, whitespace behavior, scansets, and bounded input design.
* **Does not cover:** the complete variadic ABI or general parsing architecture, which belongs in adjacent chapters.

## Why Does It Exist
The scanf family provides a concise standard mechanism for converting textual input into typed C objects. It is useful for small hosted utilities and tests, but its implicit parsing rules and pointer-based destinations make it a poor default for untrusted or strict embedded protocol input.

## Mechanism and language rules
Each conversion specifies what input is consumed and what destination type is expected. Except for suppressed conversions and conversions such as `%c`, `%n`, and scansets with their own rules, whitespace in the format can consume an arbitrary amount of input whitespace. Numeric conversions skip leading whitespace automatically.

The destination argument must point to an object of the correct type and sufficient size. Field widths constrain how much input a conversion consumes, but they do not universally mean the same thing as destination capacity; `%s` needs room for the terminating null character in addition to the characters matched.

The return value is the number of assignments successfully performed, excluding suppressed conversions. `EOF` can indicate that input failure occurred before the first conversion could be assigned.

### What to reason about
- Every non-suppressed conversion generally requires a pointer to the exact destination type expected by the format.
- `%d` expects `int *`, `%u` expects `unsigned int *`, `%ld` expects `long *`, `%zu` expects `size_t *`, and similar length-modifier rules matter.
- `%s` without a field width can overflow the destination; `%Ns` limits the input characters but still requires `N + 1` bytes.
- `%c` does not skip leading whitespace unless the format explicitly contains whitespace before it, and it does not append a null terminator.
- `%n` writes the number of characters consumed and can become a security concern when format strings are not fully controlled.
- Always distinguish matching failure from end-of-file and from an application-level invalid value.

## Embedded implications
`scanf` often has poor worst-case behavior for firmware: it can be large, slow, blocking, locale-aware, and difficult to bound. Parsing input from UART, CAN gateways, USB, or network interfaces with scanf can create denial-of-service-like stalls when malformed or incomplete input is received.

### Firmware review angle
Prefer a staged parser: receive a bounded frame, validate its length and syntax, then convert fields explicitly with functions such as `strtoul` or a small integer parser. If scanf is retained for a diagnostic shell, enforce input buffers, field widths, command timeouts, and a maximum line length.

## Edge cases and failure modes
- `scanf("%s", buf)` can overflow `buf`.
- `scanf("%d", &value)` does not prove that the complete input token was valid; trailing characters may remain in the stream.
- A loop such as `while (scanf("%d", &x) != EOF)` can become infinite when matching repeatedly fails without consuming the offending character.
- `%f` in scanf expects `float *`, while `%lf` expects `double *`; this differs from printf where `%f` arguments are passed as `double` because of default argument promotions.
- `%c` can read a newline left by a previous numeric conversion, surprising code that expects a visible character.
- Using a destination pointer to an object that has gone out of lifetime violates the function's contract and can produce memory corruption.

## Example pattern
```c
#include <stdio.h>

static int read_u32(FILE *stream, unsigned int *out)
{
    if (stream == NULL || out == NULL) {
        return -1;
    }

    return (fscanf(stream, "%u", out) == 1) ? 0 : 1;
}
```

For a fixed-size string, use an explicit field width tied to the actual destination size, for example `"%15s"` for a 16-byte buffer, and still validate the resulting token.

## Verification / debugging
Unit-test empty input, whitespace-only input, malformed numeric prefixes, overflow-range numbers, missing delimiters, long strings, and trailing garbage. Verify that every destination is correctly typed and sized. Static analysis and compiler format checking can catch many mismatches, but they cannot prove that a runtime input is semantically acceptable.

For firmware, test incomplete UART frames and deliberately slow input to expose blocking behavior.

## Staff-level takeaway
The scanf family is compact but has a complicated input state machine and weak safety ergonomics. A Staff engineer should treat it as a convenience parser for controlled input, not as a general-purpose protocol parser. For production firmware, explicit bounded tokenization followed by checked conversion usually gives better safety, determinism, diagnostics, and testability.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[15_C_Strings_Characters/00_Chapter_Index]]
[[42_C_Error_Handling/00_Chapter_Index]]
