# Core dumps

> Canonical C topic note — Chapter 41. A core dump is a captured snapshot of process or firmware execution state used for post-mortem analysis. The format and capture mechanism are platform-specific, but the analysis principles apply broadly.

## Definition
A core dump preserves selected memory and CPU state after abnormal termination so engineers can analyze a failure without reproducing it interactively. On hosted systems this may include stacks, mappings, registers, and selected memory segments. Embedded systems commonly implement a smaller crash record in reserved RAM, flash, external storage, or a diagnostic transport.

## Mechanism and language rules
A dump records machine state; it does not preserve the full C abstract-machine history. The analyst reconstructs likely execution from PC, stack, registers, memory, symbols, logs, and invariants.

### What to reason about
- Is the captured PC the faulting instruction or an architecture-specific exception location?
- Which stack is captured and which execution context was active?
- Are memory regions complete, sampled, compressed, or omitted?
- Does the dump correspond to the exact firmware image and symbols?
- Can corrupted stack or heap metadata make unwinding unreliable?
- Could privacy/security policy prohibit retaining particular memory regions?

A dump must distinguish **captured evidence** from **derived interpretation**. Preserve raw values wherever possible.

## Embedded implications
MCUs rarely have the storage capacity for a desktop-sized core. A useful embedded crash record often contains reset/fault reason, PC, SP, link/return state, status registers, selected general registers, task/ISR identity, stack window, event breadcrumbs, and firmware build ID.

Persistent flash storage introduces wear, power-failure risks, and record-integrity requirements. Reserved RAM may survive watchdog resets but not all power cycles.

### Firmware review angle
Define a fixed crash-record schema, version it, include a CRC or equivalent integrity check, and ensure the fault handler has bounded execution time. Avoid complex allocation, formatted I/O, or locks in the failure path.

## Edge cases and failure modes
- **Incomplete capture:** fault handler crashes or watchdog resets before saving state.
- **Wrong symbols:** a valid PC is mapped against a different build.
- **Stack corruption:** backtrace is partially or wholly false.
- **Power loss:** volatile crash state disappears.
- **Sensitive data:** raw RAM can contain credentials or customer information.

## Example pattern
```c
struct crash_record {
    uint32_t magic;
    uint32_t version;
    uint32_t pc;
    uint32_t sp;
    uint32_t status;
    uint32_t reset_reason;
};
```
The structure should have a documented binary schema and integrity mechanism; it is an example of a compact record, not a portable ABI specification.

## Verification / debugging
Force controlled faults in a staging image and verify that the record survives the intended reset type, is not overwritten on normal boot, and can be decoded with the exact build artifacts. Test malformed records and interrupted writes.

During analysis, first validate the record, firmware identity, and raw register state; only then perform symbolic unwinding and source interpretation.

Staff-level questions: What minimum state is required to identify the failure class? How much storage and write time can the fault path consume? Can the record be trusted after partial power loss?

## Staff-level takeaway
A crash dump is valuable only when it is **self-identifying, integrity-protected, bounded, and symbolizable**. Design it as a durable evidence format, not as an ad-hoc collection of debugger fields.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
