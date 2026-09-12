# raise/abort

> Canonical C topic note — chapter 34.

## Definition
`raise()` in `<signal.h>` requests delivery of a specified signal to the calling process. `abort()` in the same header requests abnormal program termination and raises `SIGABRT`.

These APIs are related but serve different architectural purposes: `raise()` is an explicit signal-generation mechanism, while `abort()` is a deliberate fail-stop operation. Exact termination behavior, streams, cleanup, and diagnostic output depend on the implementation.

## Mechanism and language rules
`raise(signum)` attempts to generate the specified signal. Its return value reports success or failure according to the C library contract. A signal may be handled, ignored, or take its default action.

`abort()` causes abnormal termination. It does not provide a normal cleanup path equivalent to returning from `main()`. Implementations may perform additional implementation-specific actions such as producing diagnostics or a core dump on hosted systems.

### What to reason about
- `raise()` is synchronous in the sense that the call itself requests a signal; handler execution still follows the implementation's signal semantics.
- The signal identifier must be a valid signal supported by the implementation.
- `abort()` is intended for unrecoverable program failure, not routine error handling.
- Returning from a handler for an abort-related signal does not necessarily make the failure disappear; the standard specifies special behavior around `SIGABRT` and `abort()`.
- Do not infer POSIX-specific semantics such as signal masks or process groups from ISO C alone.

## Embedded implications
On bare-metal systems, `abort()` may map to a board-support fatal path, infinite loop, debugger trap, reset, or a library stub. The resulting behavior is a system architecture decision even when the source calls standard C.

A robust embedded fatal path should capture enough diagnostic state to identify the failure, preserve reset/fault evidence if possible, and then enter a controlled terminal state or reset policy. It should not depend on a large buffered logging stack if the system is already corrupted.

### Firmware review angle
Define the fatal policy explicitly:
- Is `abort()` compiled out, trapped, reset, or logged?
- Is it callable from an ISR/fault context?
- Can it safely write persistent diagnostics?
- What is the watchdog/reset interaction?
- Does production firmware expose sensitive memory through diagnostics?

## Edge cases and failure modes
Hazards include:
- assuming `abort()` performs normal resource cleanup;
- assuming a debugger is always attached;
- assuming a console is available during early boot;
- recursively invoking `abort()` from the fatal path;
- using heap/stdio facilities after memory corruption;
- assuming `raise()` behaves like an ordinary function callback;
- ignoring failure from `raise()` where the return value matters.

A common architectural mistake is to make the fatal handler more complicated than the subsystem that failed.

## Example pattern
```c
#include <signal.h>

static int recoverable_condition(void)
{
    return 0;
}

int main(void)
{
    if (recoverable_condition()) {
        (void)raise(SIGTERM); /* Only if the implementation supports it. */
    }
    return 0;
}
```

For an embedded fatal assertion, a dedicated project-level `fatal_error()` wrapper is often preferable because it can define the platform-specific policy explicitly.

## Verification / debugging
Unit-test `raise()` with a controlled handler and verify return/error behavior. For `abort()`, test the actual embedded fatal path on hardware: confirm reset reason, retained diagnostics, watchdog behavior, and debugger visibility.

Staff-level questions:
- Is the failure recoverable or fail-stop?
- What evidence must survive the failure?
- Can the fatal path operate with corrupted heap, stack, or clocks?
- Is `abort()` the right abstraction or should the product expose a platform-specific supervisor API?

## Staff-level takeaway
Use `raise()` for explicit signal generation when the signal model is genuinely required. Treat `abort()` as a **terminal failure boundary** and design the resulting embedded behavior deliberately rather than inheriting accidental libc behavior.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
