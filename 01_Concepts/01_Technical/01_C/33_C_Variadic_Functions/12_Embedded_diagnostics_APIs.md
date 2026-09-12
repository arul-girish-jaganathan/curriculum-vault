# Embedded diagnostics APIs

## Definition
An embedded diagnostics API is a firmware interface for exposing runtime state, faults, assertions, counters, traces, and events to developers, manufacturing tools, field-service systems, or automated test infrastructure.

The API must be designed around embedded constraints: limited RAM/flash, interrupt latency, watchdogs, boot/fault contexts, concurrency, transport availability, and the need to preserve the primary control function when diagnostics fail.

## Scope and Boundaries
* **Covers:** diagnostic API architecture, variadic versus typed interfaces, event records, context restrictions, buffering, and production behavior.
* **Does not cover:** complete variadic mechanics in [[01_va_list]]–[[04_va_end]] or generic logging policy in [[11_Logging_interfaces]].

## Why Does It Exist
Embedded failures are often difficult to reproduce. Diagnostics provide evidence about state transitions, faults, timing, and environmental conditions without requiring a debugger to be attached.

A well-designed API also decouples producers from the physical diagnostic transport. UART can later be replaced by USB, SWD trace, CAN, Ethernet, a flash-backed recorder, or a host-side decoder without changing every call site.

## Mechanism and Language Rules
A robust design commonly separates capture from presentation:

```c
enum diag_id {
    DIAG_BOOT,
    DIAG_SENSOR_FAULT,
    DIAG_WATCHDOG_RESET
};

struct diag_event {
    enum diag_id id;
    unsigned timestamp;
    unsigned value;
};

bool diag_record(const struct diag_event *event);
```

For human-readable diagnostics, a separate variadic API may exist:

```c
void diag_printf(const char *fmt, ...);
```

The typed event path is normally easier to make bounded and deterministic; the formatted path is convenient for engineering builds.

### What to reason about
- Which contexts may call the API: task, ISR, startup, NMI/fault handler?
- What is the maximum execution time in each context?
- Is dynamic allocation permitted?
- What happens when storage is full?
- Can diagnostics block or sleep?
- How are timestamps obtained if the clock is unavailable?
- How are records versioned and decoded after a firmware update?

## Examples

### ISR-safe capture pattern
```c
void uart_rx_isr(void)
{
    struct diag_event event = {
        .id = DIAG_BOOT,
        .timestamp = read_fast_tick(),
        .value = read_uart_status()
    };

    (void)diag_record(&event); /* must be bounded and non-blocking */
}
```

The actual queue must provide the required concurrency guarantees for the target architecture.

### Fault-context principle
A fault handler should capture only operations known to remain valid after the fault: small register snapshots, fault status, stack information, and a bounded persistent record. Calling a complex formatter or filesystem API from the fault path is unsafe unless explicitly designed and verified for that context.

## Undefined, Unspecified, and Implementation-Defined Behavior
The C language does not guarantee that an arbitrary driver, allocator, lock, UART, or clock is usable in an ISR or fault handler. Those are platform contracts.

Variadic APIs inherit type-mismatch risks. Concurrency behavior is likewise outside ordinary single-threaded C semantics unless synchronization/atomicity is explicitly established.

## Edge Cases and Failure Modes
* **ISR overrun:** formatting or blocking output exceeds interrupt latency budget.
* **Logger recursion:** a diagnostic error triggers another diagnostic call.
* **Full queue:** producer blocks unexpectedly or silently loses the most important fault record.
* **Reset during logging:** a record is only partially written.
* **Clock failure:** timestamps become invalid or ambiguous.
* **Version mismatch:** host decoder interprets a new event layout as an old one.
* **Persistent storage wear:** writing every event to flash can exceed endurance limits.
* **Fault context:** normal stack, heap, locks, or peripheral drivers may already be corrupted/unavailable.

## Embedded Implications
The ideal ISR-facing diagnostic primitive is usually allocation-free, lock-free or interrupt-safe according to the system design, bounded in time, and based on preallocated storage.

For production firmware, a compact event ID plus fixed-width fields is often superior to formatted strings. A lower-priority task can decode or transmit events later.

## Firmware Review Angle
Create a context matrix:

| Context | Blocking | Heap | Formatting | Typical action |
|---|---|---|---|---|
| Normal task | policy-dependent | preferably bounded | allowed if budgeted | enqueue/format |
| ISR | no | no | generally no | compact event |
| Fault handler | generally no | no | generally no | minimal snapshot |
| Bootloader | target-dependent | bounded | limited | early diagnostic record |

Every cell should be an explicit product decision, not an assumption inherited from desktop logging.

## Compiler, ABI, and Toolchain Implications
Compiler format checking is valuable for diagnostic wrappers. For machine-readable records, fixed-width integer types and explicit serialization rules make host decoding independent of compiler-specific object layout.

Do not transmit raw C structs across a persistent or external protocol boundary without specifying byte order, field widths, alignment, padding, and versioning.

## Performance, Memory, Timing, and Power
Diagnostic capture should have a known worst-case cost. A ring buffer consumes predictable RAM and avoids repeated allocation. Formatting and transport can be deferred to background execution.

For battery products, logging frequency and radio/flash transmission can dominate energy consumption. Production logging should therefore support rate limits, level filtering, and event sampling.

## Verification / Debugging
Test diagnostics under the conditions where they are most valuable: buffer full, interrupt storms, watchdog resets, transport loss, flash-full conditions, brownout/reboot, and repeated faults.

Measure enqueue latency with a cycle counter or GPIO trace. Check queue high-water marks and prove that the worst diagnostic load cannot starve the safety/control task.

For persistent records, perform power-loss tests during writes and validate CRC/version handling in the host decoder.

## Safety, Security, and Reliability
Diagnostics can leak secrets or sensitive system state. Define which fields are safe to expose and protect debug interfaces in production.

The diagnostic subsystem must be fail-soft: losing a log entry should not normally stop the primary function. If a diagnostic record is safety-relevant, its persistence and integrity requirements must be specified separately.

## Trade-offs and Alternatives
* **Formatted logging:** excellent developer ergonomics, high runtime/resource cost.
* **Typed event records:** compact and deterministic, requires decoder tooling.
* **Trace hardware:** low-overhead timing visibility, target/tool dependent.
* **Persistent fault records:** survive reset, but consume flash endurance and require power-loss-safe storage.
* **Assertions:** immediate detection during development, but production behavior must be deliberately defined.

## Staff-Level Takeaway
Embedded diagnostics should be treated as a separate subsystem with explicit contracts for context safety, bounded resource use, persistence, versioning, security, and failure behavior. A Staff engineer should design diagnostics so the act of observing a failure cannot create a second failure, and should choose typed event capture over general-purpose variadic formatting whenever determinism matters.

## Related Concepts
* [[00_Chapter_Index]]
* [[07_printf_like_APIs]]
* [[10_Type_safety_limitations]]
* [[11_Logging_interfaces]]
* [[01_va_list]]
