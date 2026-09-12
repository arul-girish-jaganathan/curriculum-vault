# printf-like APIs

## Definition
A printf-like API is an interface that follows the calling and formatting model of the C `printf` family, commonly accepting a format string followed by variadic arguments. Standard examples include `printf`, `fprintf`, `sprintf`, `snprintf`, and their `v*` counterparts such as `vprintf` and `vsnprintf`.

A project-specific logger can expose the same semantic contract while directing output to UART, SWO, USB, a ring buffer, a file, or a network transport.

## Scope and Boundaries
* **Covers:** API layering, `printf`/`vprintf` relationships, bounded formatting, return values, compiler checking, and embedded design.
* **Does not cover:** fundamental `va_list` operations in [[01_va_list]]–[[04_va_end]] or the complete format grammar in [[06_Format_strings]].

## Why Does It Exist
A `printf`-style interface gives a common human-readable diagnostic language. The `v*` family is especially useful when a wrapper needs to receive an already initialized `va_list` and delegate formatting without reimplementing argument traversal.

## Mechanism and Language Rules
A common architecture is:

```c
#include <stdarg.h>
#include <stdio.h>

static int log_printf(const char *fmt, ...)
{
    va_list ap;
    int result;

    va_start(ap, fmt);
    result = vprintf(fmt, ap);
    va_end(ap);
    return result;
}
```

The fixed parameter (`fmt`) establishes the boundary before `...`. `va_start` initializes traversal, `vprintf` consumes it, and `va_end` terminates it.

For a custom output sink, `vsnprintf` is often a better building block: format into a bounded buffer, then transmit the resulting bytes through the project's transport layer.

### What to reason about
- Is the format string trusted and type-correct?
- Is output bounded?
- Does the function return an actual length, a would-have-written length, or an error code?
- Does the wrapper preserve `va_list` lifetime and ownership correctly?
- Is the output path blocking, reentrant, thread-safe, and ISR-safe?
- What libc features does linking the formatter introduce?

## Examples

### Bounded logger
```c
static int log_message(char *buf, size_t cap, const char *fmt, ...)
{
    va_list ap;
    int n;

    va_start(ap, fmt);
    n = vsnprintf(buf, cap, fmt, ap);
    va_end(ap);

    if (n < 0)
        return -1;
    if ((size_t)n >= cap)
        return 1; /* output was truncated */
    return 0;
}
```

### Layered logging
```c
static void backend_vlog(const char *fmt, va_list ap)
{
    /* The backend consumes the traversal; caller must not assume it is reusable. */
    vprintf(fmt, ap);
}
```

If the caller needs to use the same arguments again, it must create an independent copy before delegation.

## Undefined, Unspecified, and Implementation-Defined Behavior
* A wrapper inherits the format-string type requirements of the underlying API.
* Reusing a `va_list` after a helper has consumed it without an appropriate copy is not portable.
* `sprintf` can overflow the destination object because it has no capacity parameter.
* `snprintf`/`vsnprintf` truncation semantics must be handled correctly; a return value equal to or larger than the destination capacity indicates that the complete output did not fit.
* A negative return value indicates an encoding/output error according to the API's contract; applications must not interpret it as a successful length.

## Edge Cases and Failure Modes
* **Nested wrappers:** several layers can accidentally consume the same `va_list`.
* **Two-pass formatting:** use an independent `va_list` copy for a sizing pass followed by a formatting pass.
* **Null buffer:** respect the exact `snprintf` contract and target library behavior rather than assuming every implementation treats every pointer/capacity combination identically.
* **Truncation:** decide whether truncation is acceptable, an error, or a telemetry event.
* **Recursion:** logging an error from inside the logging backend can recurse indefinitely.
* **Deadlocks:** a logger that takes a mutex and is called from an error path that already holds the same lock can deadlock.

## Embedded Implications
A printf-like logger can become a system-wide dependency on libc, heap use, locale, floating-point conversion, locks, and an output transport. On a small image, this may be a significant architectural cost.

The output backend must be designed separately from formatting. Formatting in a task and enqueueing a bounded record is usually safer than writing synchronously from an ISR.

## Firmware Review Angle
Check whether logging is permitted in interrupts, fault handlers, boot code, and watchdog recovery paths. Define severity levels, rate limits, buffer ownership, drop behavior, and backpressure policy.

A good review also asks whether a production build can compile logging out or replace it with compact event IDs without changing functional behavior.

## Compiler, ABI, and Toolchain Implications
Custom printf-like wrappers can use compiler-specific format attributes to receive compile-time checking. The attribute should be part of the build/toolchain contract and applied consistently to wrappers.

The underlying `v*` interface depends on the target ABI through `va_list`; changes in compiler, floating-point ABI, or architecture must therefore be tested rather than assumed compatible.

## Performance, Memory, Timing, and Power
Formatting has variable execution time based on field width, numeric magnitude, floating-point conversions, and output length. Transmission adds another potentially unbounded latency component.

A production embedded logger should often separate:
1. event capture,
2. serialization/formatting,
3. transport,
4. storage or upload.

This lets high-priority code perform only the minimum bounded work.

## Verification / Debugging
Unit-test every wrapper with valid and invalid boundary cases. Test truncation, large values, long strings, format mismatches, nested wrappers, and repeated traversal requirements.

Use map-file analysis to measure flash/RAM impact and GPIO/cycle-counter instrumentation to measure worst-case logging latency on the actual MCU.

## Safety, Security, and Reliability
Treat format strings as executable contracts. Never allow untrusted text to become the format string. Avoid logging sensitive information and define behavior when buffers are exhausted or the transport is unavailable.

For safety-critical products, logging should never be allowed to compromise the primary control loop or fault-recovery mechanism.

## Trade-offs and Alternatives
* **Use printf-like APIs:** for flexible human-readable diagnostics.
* **Use `v*` APIs:** when implementing wrappers that already receive `va_list`.
* **Prefer typed event APIs:** for deterministic production telemetry.
* **Prefer generated encoders:** for stable machine-readable data.

## Staff-Level Takeaway
A printf-like function is not just a convenience wrapper; it is an architectural dependency on variadic calling conventions, formatting semantics, libc size, and output transport. A Staff engineer should isolate that dependency behind a controlled interface, make bounds and failure behavior explicit, and keep the critical firmware path independent of formatting latency.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[04_va_end]]
* [[06_Format_strings]]
* [[08_Variadic_macros]]
* [[11_Logging_interfaces]]
* [[12_Embedded_diagnostics_APIs]]
