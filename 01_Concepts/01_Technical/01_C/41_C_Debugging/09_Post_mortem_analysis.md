# Post-mortem analysis

> Canonical C topic note — Chapter 41. Post-mortem analysis reconstructs a failure after execution has stopped or the system has rebooted. It combines raw evidence with C semantics, generated code, ABI knowledge, and system history.

## Definition
Post-mortem analysis examines crash records, core dumps, logs, trace, memory snapshots, registers, firmware metadata, and environmental information without requiring the original process to remain live. The objective is to reconstruct the sequence and identify the earliest defensible causal mechanism.

## Mechanism and language rules
Evidence has different confidence levels. A raw PC or captured register is direct evidence; a symbolic function name is a derived interpretation; a proposed root cause is a hypothesis. C undefined behavior, data races, lifetime violations, and corrupted memory can make later observations unreliable.

### What to reason about
- What was captured directly versus inferred?
- Is the image/symbol set exact?
- Does the stack unwind consistently with the ABI?
- Which memory regions could have been corrupted earlier?
- What concurrent agents could have modified state?
- Are timestamps from comparable clocks and do they wrap?

Use a timeline: last-known-good state -> invariant violation -> suspected corruption -> faulting instruction -> reset/recovery.

## Embedded implications
Embedded post-mortem data may be tiny. Event IDs, monotonic counters, reset reasons, watchdog breadcrumbs, and selected memory windows can be more useful than verbose logs. Fault records must survive the intended reset path and be distinguishable from stale records.

### Firmware review angle
Create a documented decoder that accepts firmware build ID, architecture, record version, and raw bytes. Keep production artifacts long enough to analyze field failures after software has moved on.

## Edge cases and failure modes
- **Secondary fault:** the crash handler itself faults and obscures the original state.
- **Stale record:** normal boot reuses old crash data as if it were new.
- **Clock mismatch:** events appear out of order.
- **Symbol mismatch:** a correct PC is mapped to the wrong source.
- **Overinterpretation:** a plausible story is mistaken for proven causality.

## Example pattern
```text
Evidence:
  PC = 0x08012344
  SP = 0x20007F10
  reset_reason = WATCHDOG
  last_event = RX_COPY_BEGIN

Hypothesis:
  RX buffer corruption caused a later invalid pointer.

Required proof:
  instruction disassembly + stack validation + buffer ownership history.
```
The hypothesis is deliberately separate from the evidence.

## Verification / debugging
Start with integrity and identity checks. Symbolize the PC against the exact ELF. Inspect the faulting instruction and its operands, validate stack plausibility, then correlate with event history and memory ownership.

Attempt reproduction only after forming a falsifiable hypothesis. Convert a confirmed mechanism into a regression test, invariant, static-analysis rule, or permanent diagnostic.

Staff-level questions: Which conclusion is directly proven? What evidence is missing? Could a different fault produce the same observed record? How can uncertainty be reduced without disturbing the production system?

## Staff-level takeaway
Excellent post-mortem analysis is **forensic engineering**: preserve raw evidence, separate facts from hypotheses, validate binary identity, reconstruct execution from the ABI upward, and explicitly track uncertainty until the root cause is demonstrated.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
