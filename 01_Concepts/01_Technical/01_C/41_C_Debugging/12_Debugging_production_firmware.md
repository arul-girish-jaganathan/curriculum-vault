# Debugging production firmware

> Canonical C topic note — chapter 41.

## Definition
Production-firmware debugging means diagnosing failures on released or release-like devices where a live debugger, writable test environment, and unrestricted logging may be unavailable. The design goal is actionable evidence without compromising safety, security, timing, or field reliability.

## Mechanism and language rules
Production observability should capture implementation state while respecting C semantics and target constraints. Useful mechanisms include persistent crash records, structured event logs, counters, assertions, watchdog breadcrumbs, trace buffers, fault handlers, health metrics, and controlled diagnostic commands.

Every record should be associated with an immutable build identity. Source revision alone may be insufficient if compiler, linker, flags, generated configuration, or link inputs differ.

## Embedded implications
Design for:
- bounded RAM use;
- bounded CPU overhead;
- bounded flash writes and wear;
- ISR-safe data collection;
- recovery after faults;
- privacy/security of diagnostic data;
- power-loss tolerance.

A RAM ring buffer can retain the last N events with minimal overhead. On a fatal fault, copy only essential state to persistent storage. On next boot, validate and upload/decode the record, then clear or retire it safely.

### Example event
```c
struct event {
    uint32_t id;
    uint32_t timestamp;
    uint32_t arg0;
    uint32_t arg1;
};
```
Use stable event IDs and documented argument meanings instead of human-readable strings in constrained paths.

## Edge cases and failure modes
- Logging changes timing and can hide races.
- Flash writes during a fault can fail or consume significant time.
- Fault handlers can recursively fault.
- Sensitive memory must not be dumped indiscriminately.
- Firmware updates can make old crash formats difficult to decode.
- Clock reset/wrap and low-power transitions complicate event ordering.
- Watchdog resets may provide only partial context.

## Verification / debugging
Inject representative faults in a controlled build and verify that the production diagnostics identify them. Test power loss during persistence, repeated crashes, corrupted records, version mismatch, full storage, and watchdog recovery.

Maintain a symbolization pipeline that accepts build ID + PC and returns the exact source/disassembly location. Keep released ELF/debug artifacts securely archived. Correlate field signatures with firmware version, hardware revision, configuration, and environmental conditions.

## Staff-level takeaway
Production debugging is an architecture concern. Decide before release what evidence survives a crash, how it is versioned, how it is protected, how it is decoded, and how much overhead it costs. A product that cannot explain its own failures shifts debugging cost from milliseconds of instrumentation to weeks of field investigation.

## Related
[[00_Chapter_Index]]
[[08_Core_dumps]]
[[09_Post_mortem_analysis]]
[[11_Debugger_scripting]]
[[../84_C_Fault_Containment/00_Chapter_Index]]
