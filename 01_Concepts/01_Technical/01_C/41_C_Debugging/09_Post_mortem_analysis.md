# Post-mortem analysis

> Canonical C topic note — Chapter 41. Post-mortem analysis reconstructs failure without relying on the live failing process. It combines machine state, symbols, logs, memory artifacts, build metadata, and system history.

## Definition
Post-mortem debugging analyzes a captured failure after execution has stopped or the device has rebooted. It is particularly valuable when reproducing the defect interactively is difficult or impossible. ISO C does not define post-mortem facilities; the evidence format is an engineering and platform contract.

## Mechanism and language rules
A useful workflow separates facts from hypotheses:

1. Validate the artifact and build identity.
2. Validate dump integrity.
3. Decode the machine context.
4. Map addresses to the exact executable.
5. Reconstruct the stack and active execution context.
6. Inspect relevant memory and ownership state.
7. Correlate with event history and reset reason.
8. Form and test causal hypotheses.

### What to reason about
- Which values are direct observations versus debugger-derived interpretations?
- Which memory could already be corrupted?
- Is the PC a valid code address?
- Is the stack within an expected region?
- Could an interrupt or DMA operation explain the state?
- Does the timeline distinguish trigger from consequence?

Never infer causality solely from “the last line shown.” The faulting instruction may be where corruption becomes visible rather than where it originated.

## Embedded implications
Embedded post-mortem systems should preserve reset cause, firmware identity, fault registers, exception context, stack samples, task/ISR identity, and a bounded event history. Ring-buffered event records are often more useful than verbose logs because they preserve the final seconds before failure with predictable storage.

### Firmware review angle
Build decoding tools into CI and test them against synthetic crash records. A diagnostic format that only one engineer can decode is an operational risk. Keep host-side tooling versioned alongside the firmware record definition.

## Edge cases and failure modes
- **Wrong binary:** address-to-source mapping becomes false.
- **Corrupted stack:** unwinding invents plausible but incorrect frames.
- **Secondary failure:** watchdog reset or brownout occurs after the original fault.
- **Timestamp ambiguity:** events from different clocks cannot be naively ordered.
- **Evidence overwrite:** reboot/startup code clears retained RAM before extraction.

## Example pattern
```c
struct breadcrumb {
    uint32_t sequence;
    uint16_t event_id;
    uint16_t data;
};

static struct breadcrumb history[32];
```
A fixed-size ring avoids dynamic allocation and provides deterministic storage. The sequence number lets the host reconstruct wraparound order.

## Verification / debugging
Use synthetic faults to validate the complete chain: capture, reboot, extraction, symbolization, decoding, and report generation. Test corrupted records and mismatched firmware versions. Compare several independent evidence sources before declaring root cause.

Staff-level questions:
- What facts are independently verified?
- What evidence distinguishes root cause from crash symptom?
- Is the artifact reproducible and decodable by another engineer?
- Which additional instrumentation would make the next incident conclusive?

## Staff-level takeaway
Post-mortem debugging is an **evidence reconstruction discipline**. Preserve enough state and history to make failures actionable, but keep capture bounded, versioned, secure, and independent of fragile runtime services.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
