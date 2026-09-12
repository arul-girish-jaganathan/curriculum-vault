# Implementation availability

> Canonical C topic note — chapter 31.

## Definition
Not every C standard-library facility is equally available on every implementation. The C standard distinguishes hosted and freestanding implementations and permits implementation-defined choices, extensions, omitted optional functionality, and target-specific library subsets. An embedded engineer must therefore distinguish **standard language guarantee**, **library requirement**, **implementation-defined behavior**, **extension**, and **actual target availability**.

A header existing in source code does not prove that every function or behavior expected by a hosted desktop libc exists on a particular MCU toolchain.

## Mechanism and language rules
Availability is determined by the C implementation and its documented environment. A freestanding implementation has a smaller required library environment than a hosted implementation. Individual functions may also depend on compiler, libc configuration, linker support, operating system services, or target runtime hooks.

```c
#include <stdint.h>
#include <stdio.h>

/* The header/API may exist while the runtime capability differs by target. */
```

### What to reason about
- Identify whether the program is hosted or freestanding.
- Separate ISO-required facilities from optional facilities and implementation extensions.
- Check compiler documentation, libc documentation, startup/runtime support, and linker configuration.
- Do not infer behavior from a different platform merely because the API name is identical.
- Treat ABI, calling convention, object sizes, filesystem availability, locale data, threading, and OS services as separate portability dimensions.
- Record assumptions such as `sizeof(time_t)`, floating-point support, `FILE` availability, or errno semantics explicitly when they affect product behavior.

## Embedded implications
Embedded toolchains frequently provide reduced libraries, configurable libc features, `--specs`-style runtime variants, semihosting options, or board-specific system-call stubs. Enabling a seemingly simple API such as formatted I/O can pull in substantial code and data.

A freestanding target may not have a filesystem, process environment, locale database, POSIX layer, or conventional console. Calls can compile successfully but fail at runtime, trap into stubs, invoke semihosting, or add unexpected blocking behavior.

### Firmware review angle
For every library dependency, verify:
- exact compiler and libc version;
- hosted/freestanding model;
- enabled feature/configuration macros;
- linker/runtime dependencies;
- flash/RAM cost;
- blocking and latency behavior;
- reentrancy/thread safety;
- target-specific stubs and failure modes;
- behavior in production versus debugger-attached builds.

## Edge cases and failure modes
A classic trap is testing code under a desktop libc and assuming the same behavior on the MCU. Semihosting is particularly dangerous when accidentally left enabled: a debug session can make I/O appear functional while production execution blocks or faults.

Another trap is treating a compiler extension as portable C. Extensions can be valuable, but their use should be isolated behind documented portability boundaries.

Library availability also changes with link-time configuration. A successful compile does not prove that the final image contains the required implementation or that the target's system hooks behave correctly.

## Example pattern
Hide target-specific facilities behind a small abstraction:

```c
int platform_write(const void *data, size_t len)
{
#if defined(TARGET_MCU)
    return uart_write(data, len);
#else
    return fwrite(data, 1, len, stdout) == len ? 0 : -1;
#endif
}
```

The application depends on a defined product contract rather than an accidental libc capability.

## Verification / debugging
Maintain a target capability matrix covering compiler/libc versions, supported headers/functions, configuration options, code size, and runtime semantics. Build with production linker settings and without a debugger. Inspect the map file and symbol references to detect unexpected libc pulls such as filesystem or semihosting code.

Staff-level questions:
- Is this API required by ISO C on this implementation model?
- What exact runtime provides it?
- What does it cost in flash, RAM, timing, and dependencies?
- What happens when the underlying OS/hardware service is absent?
- Is the behavior identical in release and debugger-attached builds?
- Where is the portability boundary documented?

## Staff-level takeaway
Portable embedded C is not achieved by using standard-looking names alone. A Staff engineer verifies the complete language + compiler + libc + ABI + linker + target-runtime stack and deliberately isolates non-portable services behind small interfaces. Availability is an engineering property that must be verified on the actual production toolchain and hardware.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
