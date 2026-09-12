# Core dumps

> Canonical C topic note — chapter 41.

## Definition
A core dump is a persistent snapshot of selected process memory and CPU state captured when a program terminates abnormally or when an explicit diagnostic mechanism requests a snapshot. Core dumps are mainly associated with hosted operating systems, but embedded firmware can implement analogous crash records containing registers, stack, selected RAM, fault status, and build identity.

A dump is valuable because it changes debugging from an interactive reproduction problem into an offline evidence-analysis problem.

## Mechanism and language rules
A useful crash artifact contains enough information to reconstruct:

`fault reason + CPU state + executable identity + call context + relevant memory`

Hosted systems may provide process mappings, threads, signal information, registers, memory segments, and executable/library references. The precise contents depend on the operating system and dump policy.

Core analysis still depends on ABI/debug metadata. Symbols, unwind information, and the exact executable are necessary to turn raw addresses into meaningful source-level evidence.

### Crash dump versus log
A text log records selected observations chosen before failure. A dump can preserve raw machine state that the original logging code did not predict. The trade-off is storage size, privacy/security exposure, capture cost, and persistence reliability.

## Embedded implications
Bare-metal products often implement a bounded crash record rather than a traditional OS core file. A robust record may include:

- magic/version/length fields;
- firmware build ID or image hash;
- reset/fault reason;
- PC, SP, LR/return state and general registers;
- architecture fault-status registers;
- selected stack bytes around the saved frame;
- task/CPU identity where applicable;
- watchdog/reset counters;
- selected application state;
- CRC/authentication metadata.

The record should be designed for power-loss safety and bounded write time. Do not attempt to dump all RAM from an ISR or fault handler into slow storage unless the platform explicitly supports it.

### Crash-record example
```c
struct crash_record {
    uint32_t magic;
    uint16_t version;
    uint16_t size;
    uint32_t build_id;
    uint32_t reason;
    uint32_t pc;
    uint32_t sp;
    uint32_t lr;
    uint8_t  stack[128];
    uint32_t crc;
};
```
Version and size fields permit future evolution. The record should have a defined validity protocol so a partially written record is ignored safely.

## Edge cases and failure modes
- The crash occurs while writing the dump, producing a partial record.
- Stack corruption makes symbolic unwinding unreliable.
- The dump and executable do not match.
- A reboot clears volatile memory before capture completes.
- Sensitive keys or customer data are unintentionally persisted.
- Repeated crashes wear nonvolatile storage.
- Fault handlers themselves dereference invalid pointers and recursively fault.
- Cache/DMA activity changes memory while the dump is being collected.

## Verification / debugging
Validate the crash artifact as a product feature, not merely a debugger convenience:

1. Force representative faults deliberately.
2. Verify record integrity after warm and cold resets.
3. Check versioning and CRC/authentication behavior.
4. Decode PC/registers using the exact firmware symbols.
5. Confirm the stack region is sufficient for common fault chains.
6. Test interrupted/power-loss writes.
7. Test storage exhaustion and repeated crash behavior.

For hosted applications, archive the executable, shared-library versions, debug symbols, and build metadata together with the dump.

## Staff-level takeaway
A core dump is a contract between the crashing system and the engineers who will diagnose it later. Design the contract around **minimum sufficient evidence, build identity, integrity, privacy, bounded capture cost, and future decodeability**. For embedded products, a small well-designed crash record often provides more field value than an impractical full-memory dump.

## Related
[[00_Chapter_Index]]
[[04_Call_stacks]]
[[05_Registers]]
[[06_Memory_inspection]]
[[09_Post_mortem_analysis]]
[[12_Debugging_production_firmware]]
[[../84_C_Fault_Containment/00_Chapter_Index]]
