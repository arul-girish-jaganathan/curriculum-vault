# Post-mortem analysis

> Canonical C topic note — chapter 41.

## Definition
Post-mortem analysis diagnoses a failure from evidence captured after execution has stopped or the system has reset. The goal is to reconstruct the failure timeline, identify the earliest violated assumption, and produce evidence-backed corrective action.

## Mechanism and language rules
Start from facts: build identity, reset/fault reason, PC, stack pointer, registers, logs, timestamps, memory snapshots, and environmental conditions. Map the failing PC to the exact binary, then reconstruct the call path and relevant data flow.

Do not confuse correlation with causation. A crash at `foo()` does not prove `foo()` introduced the defect; it may simply be where earlier memory corruption became fatal.

For C defects, explicitly consider lifetime, bounds, initialization, integer conversion, aliasing, concurrency, alignment, and undefined behavior. A debugger snapshot is evidence of machine state, not a replacement for language-level reasoning.

## Embedded implications
Embedded post-mortem systems must work without a live debugger. Useful fields include reset reason, exception type, PC/LR/SP, task/ISR context, fault-status registers, image ID, boot count, watchdog counters, recent event IDs, and bounded stack/memory windows.

Build a timeline such as:
`boot → configuration → event A → buffer allocation/ownership → event B → fault → reset → crash record readout`.

This often exposes sequencing errors that a single backtrace cannot.

### Example reasoning
If a faulting PC is in `memcpy`, do not stop at “memcpy crashed.” Verify the source/destination addresses, length, object bounds, ownership, and the instruction that produced those arguments. Then find the earlier operation that supplied the invalid range.

## Edge cases and failure modes
- Crash data may itself be corrupted by stack overflow.
- Logs can be misleading if timestamps wrap or clocks stop during low-power states.
- Optimized code may make source variables unavailable.
- Multiple faults can overwrite the original failure record.
- Watchdog resets may leave no direct fault PC.
- Logging can alter timing and hide races.

## Verification / debugging
Preserve immutable artifacts: executable, symbols, map file, compiler/toolchain version, configuration, and source revision. Create a decoder for crash records and test it against known injected faults. Maintain a normalized failure signature based on build ID, fault type, PC region, and key state rather than relying on free-form log text.

When analyzing a defect, write an explicit chain: **symptom → observation → hypothesis → experiment → result → root cause**. Record rejected hypotheses as well.

## Staff-level takeaway
Good post-mortem debugging scales beyond one engineer's debugger session. The architecture should make failures reproducible, identifiable, decodable, and comparable across field units. The objective is not merely to locate the crash but to identify the first broken invariant and prevent recurrence.

## Related
[[00_Chapter_Index]]
[[08_Core_dumps]]
[[10_Fault_localization]]
[[12_Debugging_production_firmware]]
