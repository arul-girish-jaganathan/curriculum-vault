# Debugging production firmware

> Canonical C topic note — Chapter 41. Production debugging must preserve safety, security, timing, and field reproducibility while collecting enough evidence to diagnose failures that cannot be recreated on a bench.

## Definition
Production-firmware debugging is diagnosis of software running in its real deployment configuration. Unlike a lab debug build, the system may have full optimization, restricted debug access, watchdogs, security controls, customer workloads, thermal/power variation, and no opportunity to halt execution.

## Mechanism and language rules
The C language remains the same, but observability must be engineered around it. Useful mechanisms include structured logs, counters, trace IDs, persistent crash records, watchdog breadcrumbs, sampled telemetry, invariant checks, and controlled diagnostic builds.

### What to reason about
- What exact firmware image and configuration ran?
- Can the failure be identified without exposing sensitive data?
- Does instrumentation preserve timing and memory budgets?
- Could a diagnostic read/write alter MMIO state?
- What is the retention and update strategy for evidence?
- Can the evidence distinguish UB, race, hardware fault, and external disturbance?

Use stable event IDs and compact binary payloads when bandwidth and storage are constrained. Do not depend on a full logging stack inside a fault handler.

## Embedded implications
Production diagnostics consume flash, RAM, CPU cycles, communication bandwidth, and sometimes power. Persistent flash logs require wear management. Networked devices add privacy and security concerns. Debug ports may need to be disabled or access-controlled in shipped products.

Watchdog reset handling should preserve the last known execution breadcrumbs before reboot. Brownouts and hard power loss require different strategies because software may not get time to save state.

### Firmware review angle
Define diagnostic levels with explicit budgets. Every telemetry field should have an owner, schema/version, expected rate, and privacy classification. Diagnostic paths must not accidentally become a second untested application.

## Edge cases and failure modes
- **Heisenbug:** logging changes timing enough to remove the fault.
- **Log storm:** a fault loop exhausts storage or communication bandwidth.
- **Secret leakage:** dumps expose credentials, keys, or customer data.
- **Version mismatch:** field data cannot be symbolized with the correct image.
- **Recovery loop:** an automatic recovery mechanism repeatedly resets before evidence is extracted.

## Example pattern
```c
static volatile uint32_t last_event;

static void record_event(uint32_t id)
{
    last_event = id;
}

void service(void)
{
    record_event(0x1201U);
    /* bounded operation */
    record_event(0x1202U);
}
```
For real systems, prefer an ownership-safe event buffer and atomic/concurrency rules appropriate to the execution context; the example only illustrates the diagnostic idea.

## Verification / debugging
Inject controlled faults in a staging build and verify capture, persistence, symbolization, extraction, and privacy controls. Measure diagnostic overhead under worst-case interrupt/load conditions. Test repeated failures, full storage, malformed records, power interruption, and firmware upgrades.

Staff-level questions:
- What minimum evidence turns an incident into a root-cause candidate?
- What is the operational cost of collecting it?
- How will another engineer decode it six months later?
- What prevents diagnostics from creating a new failure mode?

## Staff-level takeaway
Production debugging is a **system-design problem**. Build observability into the firmware architecture, keep evidence compact and versioned, preserve timing and security boundaries, and make every field failure capable of producing actionable evidence without requiring an interactive debugger.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
