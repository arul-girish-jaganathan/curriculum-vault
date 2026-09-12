# Environment and process interfaces

## Definition
Hosted C implementations expose environment/process-related interfaces such as `getenv`, `system`, `atexit`, `exit`, `_Exit`, `quick_exit`, `abort`, `at_quick_exit`, and `EXIT_SUCCESS`/`EXIT_FAILURE`. These APIs connect the C abstract program to the host execution environment. They are meaningful primarily in hosted systems; process creation, shell execution, environment variables, and termination behavior are heavily dependent on the operating system and C runtime.

## Scope and Boundaries
* **Covers:** environment lookup, program termination, exit handlers, `system`, and the boundary between ISO C and host OS behavior.
* **Does not cover:** POSIX process APIs such as `fork`/`exec`, signals, or OS-specific environment management in depth.

## Why Does It Exist
Hosted applications need a standardized way to communicate with the execution environment: retrieve configuration, return a program status, register cleanup, and optionally request execution of a command through the host environment.

## Mechanism and language rules
`getenv` searches the implementation-provided environment for a named string and returns a pointer to a string value or `NULL`. The returned storage is managed by the implementation; callers must not free or modify it, and subsequent environment-related operations may invalidate or alter the result according to the implementation.

`exit` performs normal program termination including registered `atexit` handlers and stream cleanup as specified by the C implementation. `_Exit` terminates without the normal cleanup sequence. `abort` causes abnormal termination. `quick_exit` performs the quick-termination sequence registered with `at_quick_exit` rather than normal `atexit` processing.

`system` passes a command string to the host command processor if one exists; its security and execution semantics are platform-dependent.

### What to reason about
- Environment variables are external mutable state; do not treat `getenv` as a compile-time constant.
- The lifetime and mutability rules of a `getenv` result differ from ordinary application-owned strings.
- `exit` is not equivalent to returning from every possible function; it terminates the process/program.
- `atexit` handlers execute in reverse registration order and should not rely on objects whose lifetime has already ended.
- `system` introduces an external command interpreter boundary and should never be treated as a portable subprocess API.
- Embedded firmware often has no meaningful process/environment model at all.

## Embedded implications
Bare-metal firmware normally does not have environment variables, shells, or process termination. An embedded C library may omit these APIs, stub them, route them to a monitor, or implement them as non-returning reset/halt behavior. `exit` may therefore map to a board-specific fatal handler rather than process teardown.

### Firmware review angle
Define explicitly what a “termination” operation means on the target: reset, watchdog recovery, safe-state transition, debugger break, or permanent halt. Do not import desktop assumptions into safety-critical firmware. `system` should generally be absent from production firmware unless a real command interpreter is part of the product design.

## Edge cases and failure modes
- Holding a `getenv` result indefinitely while assuming its storage is immutable can create stale-data bugs.
- Calling `exit` from a context that must preserve hardware safety state can bypass required application-level shutdown sequencing.
- `atexit` is not a general-purpose real-time cleanup mechanism.
- `system` with untrusted input can become command injection.
- Cleanup handlers can run in an unexpected order if multiple libraries register them.
- A freestanding implementation may not provide the hosted execution model these interfaces assume.

## Example pattern
```c
#include <stdlib.h>

static int configuration_enabled(void)
{
    const char *value = getenv("FEATURE_X");
    return value != NULL && value[0] == '1';
}
```

For embedded code, replace this environment lookup with an explicit configuration-provider interface whose source and lifetime are defined by the product architecture.

## Verification / debugging
Test missing variables, empty variables, changed environment state, and termination-handler ordering on hosted systems. For embedded targets, inspect the linker map to determine whether these APIs pull in host-runtime code, and test the concrete reset/halt behavior rather than relying on the function name.

Security review should treat every externally influenced environment value as untrusted configuration and every `system` call as a command-execution boundary.

## Staff-level takeaway
Environment/process interfaces mark the boundary between portable C and the host runtime. A Staff engineer should identify that boundary explicitly and provide an embedded abstraction for configuration and termination instead of pretending that a desktop process model exists on a microcontroller.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[34_C_Signals_Setjmp/00_Chapter_Index]]
