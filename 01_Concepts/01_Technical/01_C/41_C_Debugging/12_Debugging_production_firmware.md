# Debugging production firmware

> Canonical C topic note — Chapter 41. Production debugging must preserve safety, security, timing, privacy, and field reproducibility while collecting enough evidence to explain failures that cannot be reproduced interactively.

## Definition
Production-firmware debugging diagnoses software running in its real deployment configuration: optimized code, real workloads, watchdogs, thermal and power variation, security restrictions, customer data, and limited or no debugger access. The C language semantics do not change, but the observability strategy must be designed into the product.

## Mechanism and language rules
Useful mechanisms include structured event logs, counters, trace IDs, persistent crash records, watchdog breadcrumbs, invariant checks, sampled telemetry, and controlled diagnostic builds. Evidence should distinguish raw observations from interpretation and should identify the exact firmware build.

### What to reason about
- Which image, configuration, bootloader, and hardware revision ran?
- What evidence can be collected without exposing secrets or personal data?
- What CPU, RAM, flash, bandwidth, and latency budget does instrumentation consume?
- Could a diagnostic read/write alter MMIO or timing?
- What evidence separates UB, race, memory corruption, hardware fault, and external disturbance?
- How are records versioned and decoded after future firmware upgrades?

Use compact binary event records in constrained systems and avoid depending on formatted I/O inside fault handlers.

## Embedded implications
Diagnostics consume resources and can themselves create faults. Persistent flash logging requires wear management and power-failure tolerance. Watchdog breadcrumbs can survive software resets but not necessarily power loss. Networked devices add transport security and privacy requirements.

### Firmware review angle
Define diagnostic levels with explicit resource budgets. Every telemetry field should have an owner, schema/version, expected rate, retention policy, and privacy classification. Protect production debug interfaces with the product's security model.

## Edge cases and failure modes
- **Heisenbug:** logging changes timing and hides the race.
- **Log storm:** a failure loop exhausts storage or bandwidth.
- **Secret leakage:** dumps expose credentials or customer data.
- **Version mismatch:** field evidence cannot be symbolized.
- **Recovery loop:** automatic recovery resets before evidence is extracted.
- **Diagnostic deadlock:** fault handling depends on a lock or subsystem that is already broken.

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
The example only illustrates a breadcrumb. A real implementation needs defined concurrency, persistence, atomicity, and integrity rules.

## Verification / debugging
Inject controlled faults in staging and verify capture, persistence, extraction, symbolization, privacy filtering, and recovery. Measure worst-case diagnostic overhead under interrupt and CPU load. Test full storage, malformed records, repeated crashes, power interruption, and firmware upgrades.

Staff-level questions: What minimum evidence makes an incident actionable? What is the worst-case cost? Can another engineer decode it months later? What prevents the diagnostic path from becoming a new failure mode?

## Staff-level takeaway
Production debugging is a **system-design problem**. Build observability into the firmware architecture, keep evidence compact and versioned, preserve security and timing boundaries, and make field failures diagnosable without an interactive debugger.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
