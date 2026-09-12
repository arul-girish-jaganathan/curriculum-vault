# Debugging production firmware

> Canonical C topic note — chapter 41.

## Definition
Production-firmware debugging means diagnosing failures on released or release-like devices where a live debugger, unrestricted RAM access, full logging, and easy reproduction may be unavailable. The objective is actionable evidence without violating safety, security, timing, storage, or recovery requirements.

Production observability is therefore a design problem, not an afterthought.

## Mechanism and language rules
Useful diagnostic mechanisms include:

- persistent crash records;
- structured event IDs and ring buffers;
- counters and watermarks;
- assertions with controlled failure policy;
- watchdog breadcrumbs;
- exception/fault handlers;
- trace buffers;
- health/diagnostic telemetry;
- controlled diagnostic interfaces.

Every artifact must carry an immutable firmware identity. A source revision alone is insufficient if compiler version, optimization, linker layout, generated configuration, libraries, or build flags differ.

### Bounded observability
A good production diagnostic has explicit budgets:

```text
RAM ≤ defined limit
CPU overhead ≤ defined limit
flash writes ≤ wear budget
ISR work ≤ latency budget
persistent record ≤ fixed maximum
privacy exposure ≤ approved data class
```

Prefer compact typed values over free-form strings in constrained paths. Stable event IDs make field data comparable across units and releases.

```c
struct event {
    uint32_t id;
    uint32_t timestamp;
    uint32_t arg0;
    uint32_t arg1;
};
```
Document the meaning and units of every argument. Do not allow a released firmware to change event semantics without versioning.

## Embedded implications
A production diagnostic architecture should support several contexts:

- normal task/thread execution;
- interrupt context;
- exception/fault context;
- early boot;
- low-power/resume paths;
- watchdog/reset recovery.

A RAM ring buffer can retain recent events without expensive storage writes. On a fatal fault, persist only essential evidence: build identity, reason, PC/SP/LR, selected registers, fault status, and a bounded stack/memory region.

Design persistence for power loss and repeated failures. Use validity markers, length/version fields, CRC or equivalent integrity checks, and wear-aware storage management.

### Safety and security boundaries
Never treat diagnostic memory as automatically safe to upload. Stack and RAM dumps can contain keys, credentials, user information, proprietary data, or security state. Define collection and transport policy explicitly.

## Edge cases and failure modes
- Logging changes timing and hides races.
- Fault handlers recursively fault while trying to collect state.
- Flash writes fail during low-voltage or brownout conditions.
- Repeated watchdog resets overwrite the original evidence.
- Storage wear accumulates under crash loops.
- Clock wrap, clock-source changes, or deep sleep disturb event ordering.
- Firmware updates change crash-record formats.
- Symbols for a released binary are lost, making PC values difficult to decode.
- Unbounded diagnostic output causes memory or bandwidth exhaustion.

## Verification / debugging
Before release, inject representative failures and verify:

1. the diagnostic record is generated;
2. it survives the intended reset/power path;
3. corruption is detected rather than decoded as valid;
4. build IDs select the exact symbol set;
5. stack/register capture is sufficient for common failures;
6. watchdog and recovery paths remain bounded;
7. repeated crashes do not exhaust storage;
8. sensitive information is not unintentionally persisted or transmitted.

Maintain a symbolization pipeline that maps `build ID + PC` to the exact source/disassembly location. Archive released ELF/debug artifacts securely and correlate failure signatures with hardware revision, configuration, firmware, and environmental conditions.

## Staff-level takeaway
Production debugging must be designed before the field failure occurs. Define **what evidence survives, how it is versioned, how it is protected, how it is decoded, and what resource budget it costs**. The strongest embedded products make failures self-describing enough that an engineer can reconstruct the violated invariant without attaching a debugger to the original device.

## Related
[[00_Chapter_Index]]
[[08_Core_dumps]]
[[09_Post_mortem_analysis]]
[[10_Fault_localization]]
[[11_Debugger_scripting]]
[[../84_C_Fault_Containment/00_Chapter_Index]]
[[../39_C_Diagnostics_Static_Analysis/00_Chapter_Index]]
