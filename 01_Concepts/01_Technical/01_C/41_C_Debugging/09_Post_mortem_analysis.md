# Post-mortem analysis

> Canonical C topic note — chapter 41.

## Definition
Post-mortem analysis diagnoses a failure from evidence captured after execution has stopped, crashed, or reset. Its purpose is to reconstruct the failure timeline, identify the earliest violated invariant, separate symptom from cause, and produce evidence-backed corrective action.

A successful post-mortem answers four questions:

1. What happened?
2. What evidence proves it?
3. Which invariant was first violated?
4. What experiment or reproduction confirms causality?

## Mechanism and language rules
Start with immutable facts: firmware/build identity, reset reason, PC, SP, registers, fault status, timestamps, task/ISR context, relevant memory, and environmental conditions. Symbolize addresses only against the exact executable and debug artifacts that produced them.

For C failures, examine the language-level contracts behind the machine symptom:

- object lifetime;
- array bounds and pointer provenance/use;
- initialization;
- integer conversion and range assumptions;
- alignment;
- effective type/aliasing;
- data races and atomicity;
- state-machine invariants;
- resource ownership.

A crash site is not necessarily a fault site. A corrupted pointer may crash in `memcpy`, while the invalid pointer was produced hundreds of instructions earlier.

### Evidence hierarchy
Prefer stronger evidence over narrative:

`fault registers/raw state → exact instruction → arguments/state → preceding event sequence → source hypothesis → design/root cause`.

Logs are useful but can be incomplete or observer-perturbed. A debugger snapshot is machine-state evidence, not proof of C-level legality.

## Embedded implications
Build a timeline such as:

`boot → configuration → event A → ownership transfer → interrupt/DMA activity → event B → invariant violation → fault/reset → crash capture`

Include asynchronous agents explicitly. A race involving an ISR or DMA controller can invalidate a simplistic “last C statement executed” story.

### Example reasoning
If the PC lands inside a copy routine, inspect the source address, destination address, and length at the faulting instruction. Then determine:

```text
Was the address aligned/valid?
Was the object alive?
Was the length derived from a checked source?
Who owned the buffer?
Could DMA/ISR/another core change it concurrently?
Where did the invalid argument first originate?
```

Only after answering those questions should the copy routine itself be considered causal.

## Edge cases and failure modes
- Stack corruption destroys the evidence used for unwinding.
- A watchdog reset leaves no ordinary fault PC.
- Multiple resets overwrite the original crash record.
- Logs can reorder events because of buffering or asynchronous transport.
- Timestamps can wrap or stop across sleep/reset transitions.
- Instrumentation can change timing and hide races.
- Optimized code can eliminate intuitive source variables.
- The crash handler can itself fault or deadlock.

## Verification / debugging
Preserve the executable, symbols, linker map, compiler/toolchain information, configuration, hardware revision, and source revision together with the failure artifact.

Create a reproducible decoder and inject known faults to verify that it identifies the intended PC, register frame, and memory window. Normalize failure signatures around build ID, fault class, PC range, and selected state so large fleets can be clustered.

Document the reasoning chain:

`observation → hypothesis → experiment → result → conclusion`

Include rejected hypotheses; they prevent teams from repeatedly exploring disproven explanations.

## Staff-level takeaway
Post-mortem analysis is a system for converting failure data into causal knowledge. The highest-value output is not “crashed in function X” but **the earliest broken invariant, the evidence proving it, and a preventive design change that makes the failure impossible or diagnosable**.

## Related
[[00_Chapter_Index]]
[[08_Core_dumps]]
[[10_Fault_localization]]
[[12_Debugging_production_firmware]]
[[../29_C_Behavior_Categories/00_Chapter_Index]]
