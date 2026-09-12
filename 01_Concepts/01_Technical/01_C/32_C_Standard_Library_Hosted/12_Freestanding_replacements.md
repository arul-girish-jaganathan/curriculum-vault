# Freestanding replacements

## Definition
Freestanding replacements are target-specific or application-specific mechanisms used when hosted C services such as files, streams, processes, environment variables, or dynamic allocation are unavailable or unsuitable. The C language permits a freestanding implementation to provide a reduced library environment, so embedded systems commonly build explicit drivers, buffers, allocators, logging layers, and startup/runtime services around the core language.

## Scope and Boundaries
* **Covers:** replacing hosted I/O/runtime assumptions with deterministic embedded abstractions.
* **Does not cover:** one particular RTOS, filesystem, libc, or vendor SDK.

## Why Does It Exist
Microcontrollers frequently have no process model, shell, filesystem, or general-purpose terminal. Even when a C library provides hosted-style APIs, their resource cost and timing may be inappropriate. Explicit replacements allow firmware to preserve the useful behavior while making ownership, latency, memory, and failure contracts visible.

## Mechanism and language rules
A good replacement preserves the semantic requirement rather than mechanically recreating the API name. For example, a logging requirement can use a ring buffer plus UART/DMA backend instead of `printf`; configuration persistence can use a transactional NVM service instead of `fopen`; a delay service can use a hardware timer rather than wall-clock file/runtime facilities.

The interface should expose explicit sizes and error results, define ownership and concurrency, and avoid hidden global state where possible.

### What to reason about
- Identify the original requirement: formatting, persistence, input, timing, diagnostics, or process control.
- Separate portable C logic from target-specific device access.
- Make buffer ownership, capacity, lifetime, and synchronization explicit.
- Define whether operations are blocking, bounded, interrupt-safe, or asynchronous.
- Preserve the required semantic guarantee without accidentally preserving expensive hosted behavior.

## Embedded implications
Common replacements include UART/USB/RTT logging, ring-buffered telemetry, filesystem wrappers over flash/SD, NVM key-value stores, hardware timer services, watchdog/reset services, and statically allocated memory pools. DMA-backed designs can improve throughput but introduce alignment/cache/coherency requirements.

### Firmware review angle
Evaluate every replacement against RAM/flash footprint, worst-case execution time, power behavior, ISR interaction, recovery after reset, and failure injection. A replacement is not successful if it merely hides the same unbounded behavior behind a different function name.

## Edge cases and failure modes
- Replacing `printf` with a UART byte loop may still block indefinitely if the receiver is slow.
- A ring buffer without an overflow policy silently loses diagnostics or overwrites critical data.
- A filesystem replacement that writes directly to flash without power-fail recovery can corrupt configuration.
- A custom `malloc` replacement without fragmentation analysis can reproduce the same long-term allocation risks.
- Host-based tests can accidentally exercise the original hosted implementation instead of the embedded replacement.

## Example pattern
```c
#include <stddef.h>

struct log_port {
    int (*submit)(const void *data, size_t len);
};

static int log_text(const struct log_port *port, const char *text)
{
    size_t len = 0U;

    if (port == NULL || port->submit == NULL || text == NULL) {
        return -1;
    }

    while (text[len] != '\0') {
        ++len;
    }

    return port->submit(text, len);
}
```

A production implementation can replace the linear scan with an explicitly sized API; the important architectural point is that the application depends on a capability contract rather than assuming `stdout` exists.

## Verification / debugging
Maintain host and target implementations behind the same narrow interface and run identical functional tests where possible. Add fault injection for queue-full, transport-disconnected, storage-full, power-loss, and timeout conditions. Measure latency, queue depth, dropped messages, flash wear, and stack usage on real hardware.

## Staff-level takeaway
A freestanding replacement should be designed around the product's actual requirement, not around reproducing desktop APIs. Staff-level architecture makes platform boundaries explicit, keeps deterministic paths free of hidden libc behavior, and provides evidence for memory, timing, concurrency, and failure guarantees.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[11_Hosted_only_assumptions]]
[[46_C_Embedded_Patterns/00_Chapter_Index]]
