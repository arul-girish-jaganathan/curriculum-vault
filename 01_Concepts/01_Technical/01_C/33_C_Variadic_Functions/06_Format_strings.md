# Format strings

## Definition
A format string is a character sequence interpreted by a formatting API to describe how additional arguments should be consumed and represented. In C, the classic example is the format argument used by `printf`-family functions.

A format string is effectively a compact runtime type-and-presentation contract. The compiler normally cannot enforce the complete contract from the C function prototype alone, so mismatches can become undefined behavior.

## Scope and Boundaries
* **Covers:** conversion specifications, flags, width, precision, length modifiers, argument typing, security, and embedded logging design.
* **Does not cover:** the underlying `va_list` mechanics in [[01_va_list]] or full `printf` implementation behavior in [[07_printf_like_APIs]].

## Why Does It Exist
A single formatting API can serve integers, floating-point values, strings, characters, pointers, and application-defined diagnostic messages without requiring a separate function for every combination. This is convenient for hosted applications and firmware diagnostics, but flexibility comes at the cost of a weaker compile-time type contract.

## Mechanism and Language Rules
A conversion specification generally contains a `%`, optional flags, optional width, optional precision, an optional length modifier, and a conversion specifier. For example:

```c
printf("count=%u id=%" PRIu32 "\n", count, id);
```

The conversion specifier determines how the corresponding variadic argument is consumed. Length modifiers alter the expected argument type, so `%ld` and `%d` are not interchangeable merely because both print integers.

Common conversions include `%d`, `%i`, `%u`, `%x`, `%c`, `%s`, `%p`, `%f`, `%e`, `%g`, and related forms. `*` width or precision consumes an additional `int` argument.

### What to reason about
- What exact argument type does the conversion require?
- Has the argument undergone default argument promotions?
- Is the length modifier correct for the argument type?
- Is `%s` pointing to a valid null-terminated sequence?
- Is the destination bounded when formatting into a buffer?
- Can the format string be influenced by untrusted input?
- Does the implementation support the requested conversion, especially in embedded libc variants?

## Examples

### Safe fixed format
```c
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

void log_id(uint32_t id)
{
    printf("id=%" PRIu32 "\n", id);
}
```

### Dangerous format-string use
```c
/* Never do this with untrusted text. */
printf(user_message);
```

Use a literal format and make user text data:

```c
printf("%s", user_message);
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* A format conversion whose expected argument type is incompatible with the actual variadic argument can produce undefined behavior.
* Passing an invalid `%s` pointer, including a pointer to a non-terminated buffer, can read beyond the intended object.
* `*` width and precision arguments must have the required `int` type.
* The exact supported conversion set and behavior can vary with the selected C library, especially in reduced embedded libraries.
* Integer width assumptions such as treating `uint32_t` as always `unsigned int` are not portable; `<inttypes.h>` macros exist for portable formatted integer output.

## Edge Cases and Failure Modes
* `%p` has a specific pointer contract; do not substitute an integer cast as a casual replacement.
* `%zu` is appropriate for `size_t` in C99 and later environments supporting it.
* Negative width from `*` has defined formatting semantics rather than meaning "invalid width."
* Precision for `%s` can bound how many characters are considered, which can be useful for defensive output.
* A format string stored in writable memory can be corrupted and turn a normal logging operation into a type-confusion or information-disclosure path.
* `sprintf` removes the destination-size safety boundary; prefer `snprintf` for bounded buffers.

## Embedded Implications
Format parsing and conversion can consume substantial flash and CPU time. Floating-point conversions, locale support, wide-character support, and positional features may pull in large library components.

UART logging can block while transmitting characters. Therefore a harmless-looking format statement can introduce milliseconds of latency, priority inversion, or watchdog failures depending on baud rate and output volume.

## Firmware Review Angle
Classify every format path as diagnostic, telemetry, protocol, or user-facing output. Diagnostic logging can tolerate more flexibility; binary protocol encoding usually should not use `printf`-style text formatting because exact field widths, timing, and locale independence matter more.

Measure code-size contribution with the linker map and worst-case output latency with target instrumentation.

## Compiler, ABI, and Toolchain Implications
GCC/Clang-style format attributes can teach the compiler that a custom function follows `printf` semantics, allowing format checking even through project-specific logging wrappers. This is a valuable toolchain contract but is not itself ISO C syntax.

The ABI still determines how the variadic arguments reach the formatter. Length modifiers and promotions must therefore agree with both the source-level format contract and the target calling convention.

## Performance, Memory, Timing, and Power
Parsing a format string, converting values, copying output, and transmitting it can dwarf the cost of the original application operation. `%f` can be particularly expensive on MCUs.

For deterministic systems, pre-encoded event records with numeric IDs and typed payloads often provide better timing and lower flash/RAM cost.

## Verification / Debugging
Enable compiler format warnings and annotate custom printf-like functions where supported. Test minimum/maximum integer values, negative values, `size_t`, fixed-width integers, null strings where the API contract permits them, truncation, width/precision boundaries, and floating-point cases actually used.

Use fuzzing for complex format parsers and compare output against a known-good implementation when portability is important.

## Safety, Security, and Reliability
Never treat external input as a format string. Bound all output buffers. Avoid logging secrets, credentials, keys, or raw memory contents. In safety-critical firmware, define which conversions are allowed and consider a restricted formatter rather than a general-purpose one.

## Trade-offs and Alternatives
* **Use:** controlled human-readable diagnostics.
* **Avoid:** exact binary protocol serialization, hard-real-time paths, and security-sensitive output without strong justification.
* **Alternatives:** typed binary records, generated serializers, fixed-format encoders, or small integer-to-text routines for constrained targets.

## Staff-Level Takeaway
A format string is not merely presentation text; it is a runtime type contract embedded in a string. A Staff engineer should review it like an API schema: prove argument compatibility, bound output, prevent injection, understand libc feature costs, and measure timing before allowing it into critical firmware paths.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[03_va_arg]]
* [[05_Default_argument_promotions]]
* [[07_printf_like_APIs]]
* [[10_Type_safety_limitations]]
