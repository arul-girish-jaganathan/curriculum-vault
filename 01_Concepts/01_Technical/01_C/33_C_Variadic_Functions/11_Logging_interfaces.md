# Logging interfaces

## Definition
A logging interface is the software boundary through which firmware or applications emit diagnostic events, messages, values, and fault information. A C implementation may use fixed parameters, variadic arguments, `printf`-style formatting, binary event records, or a combination of these.

A production-grade logger is more than a formatting function: it defines severity, ownership, buffering, concurrency, timestamps, transport, overflow behavior, and whether logging is permitted in critical execution contexts.

## Scope and Boundaries
* **Covers:** logging API shape, severity, buffering, variadic wrappers, concurrency, context, and production embedded design.
* **Does not cover:** detailed variadic mechanics in [[01_va_list]] or format grammar in [[06_Format_strings]].

## Why Does It Exist
Diagnostics are essential for bring-up, field failures, validation, and post-mortem analysis. A central logging interface prevents every module from inventing a different output mechanism and allows the backend to change without rewriting application code.

## Mechanism and Language Rules
A simple typed interface might be:

```c
enum log_level { LOG_ERROR, LOG_WARN, LOG_INFO, LOG_DEBUG };

void log_event(enum log_level level,
               unsigned event_id,
               unsigned value);
```

A flexible human-readable interface can instead use:

```c
void log_printf(enum log_level level, const char *fmt, ...);
```

The second form is convenient but introduces a variadic type contract and formatting cost. A mature architecture often captures compact typed events first and performs expensive formatting later in a lower-priority context.

### What to reason about
- Is the API blocking or non-blocking?
- Is it safe from ISR and fault-handler contexts?
- What happens when the log buffer is full?
- Is the timestamp monotonic, wall-clock, or absent?
- Can logging recurse or deadlock?
- Does logging allocate memory dynamically?
- Can production builds disable verbose levels without changing functional behavior?

## Examples

### Compact event capture
```c
struct log_event {
    unsigned event_id;
    unsigned value;
    unsigned timestamp;
};

static bool log_try_push(const struct log_event *event)
{
    /* Bounded enqueue into a preallocated ring buffer. */
    return true;
}
```

The exact queue implementation is system-specific, but the architectural idea is to keep event capture small and bounded.

### Human-readable wrapper
```c
static void log_info(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    /* Format or enqueue according to the backend policy. */
    va_end(ap);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
The C language does not define a general logging subsystem. Behavior such as UART transmission, thread synchronization, buffering, timestamps, persistence, and output transport belongs to the platform/application.

Variadic logging inherits all of the type-contract risks of `va_arg` and format strings. Library I/O behavior also depends on the selected libc and target.

## Edge Cases and Failure Modes
* **Buffer full:** choose drop-oldest, drop-newest, blocking, overwrite, or escalation explicitly.
* **Recursive logging:** an error inside the logger can recursively call itself.
* **Deadlock:** logging while holding a mutex can deadlock if the backend takes the same lock.
* **ISR logging:** blocking UART output can violate interrupt latency budgets.
* **Fault handler:** normal heap, locks, clocks, or drivers may be unavailable after a severe fault.
* **Sensitive data:** logs can expose credentials, keys, personal data, or memory contents.
* **Format mismatch:** wrappers can hide format strings from compiler checking unless configured correctly.

## Embedded Implications
A logger should be designed around the worst context from which it may be called. If ISR support is required, the ISR-facing operation should normally be a bounded, allocation-free enqueue into preallocated storage.

Transport and formatting should run later in a task/background context. This separates hard timing constraints from potentially expensive string conversion and I/O.

## Firmware Review Angle
Define a logging matrix covering context, maximum execution time, memory use, allowed levels, and backend behavior. Verify that production configuration cannot accidentally enable a high-volume debug path in a timing-critical component.

## Compiler, ABI, and Toolchain Implications
If the interface is printf-like, compiler-specific format annotations can restore static checking. Build-time logging macros can inject file/line/function metadata.

ABI changes matter when the logger is a shared binary component or when a host tool consumes records. Prefer stable fixed-width event fields for machine-readable logs.

## Performance, Memory, Timing, and Power
The main costs are formatting, buffering, transport, synchronization, and storage. A 115200-baud UART, for example, has a finite byte rate; a long diagnostic message can occupy a timing window much larger than the CPU formatting itself.

Compact event IDs can reduce bandwidth and flash/RAM usage substantially. Logging should also have rate limits to prevent a fault from producing an uncontrolled storm.

## Verification / Debugging
Test logger behavior under buffer saturation, concurrent producers, disabled backends, transport failure, watchdog pressure, and fault recovery. Measure ISR enqueue time and background formatting time separately.

Use trace timestamps, GPIO instrumentation, queue high-water marks, and linker map analysis to establish actual resource usage.

## Safety, Security, and Reliability
Logs are part of the attack and failure surface. Define access controls for sensitive logs, scrub secrets, prevent format-string injection, and ensure logging cannot prevent the safety function from running.

A failure in the logging subsystem should degrade diagnostics, not take down the primary control path.

## Trade-offs and Alternatives
* **Printf logging:** easy to read, flexible, relatively expensive and weakly typed.
* **Binary events:** compact and deterministic, but require decoding tools.
* **Trace buffers:** excellent for timing analysis, but require target-specific tooling.
* **Typed event APIs:** strongest application contract and good for production firmware.

## Staff-Level Takeaway
Logging is an architecture, not a `printf` call. A Staff engineer should define execution-context rules, bounded resource usage, overflow policy, concurrency semantics, security boundaries, and deployment configuration. The best logger preserves observability without becoming part of the failure being diagnosed.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[06_Format_strings]]
* [[07_printf_like_APIs]]
* [[12_Embedded_diagnostics_APIs]]
