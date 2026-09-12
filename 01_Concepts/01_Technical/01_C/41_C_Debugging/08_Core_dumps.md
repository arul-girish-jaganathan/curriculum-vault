# Core dumps

> Canonical C topic note — chapter 41.

## Definition
A core dump is a captured snapshot of process state after a fatal failure, typically containing memory, registers, mappings, and metadata needed for post-mortem analysis. Core dumps are primarily hosted-OS concepts; bare-metal firmware normally needs an explicitly designed crash record instead.

## Mechanism and language rules
A core records implementation-level state, not a direct representation of the C abstract machine. A debugger combines the core with the exact executable and debug symbols to reconstruct threads, stacks, variables, and instruction locations.

Useful state includes:
- program counter and stack pointer;
- general registers and status state;
- thread list and stacks;
- loaded-module mappings;
- selected memory regions;
- signal/fault metadata;
- executable and build identifiers.

The executable must match the crash. A symbol file from another build can produce plausible but false source locations.

## Embedded implications
Bare-metal systems can implement a compact crash dump containing exception registers, fault status, stack pointers, a bounded stack window, reset reason, task identity, and selected diagnostic counters. Store it in retention RAM, battery-backed RAM, EEPROM, or a reserved flash region according to product requirements.

The record must be robust against power loss and repeated faults. Include a magic value, format version, length, sequence number, payload checksum/CRC, and build/image identifier. Avoid writing excessive data to flash on every reset because of endurance limits.

### Example crash record
```c
struct crash_record {
    uint32_t magic;
    uint32_t version;
    uint32_t pc;
    uint32_t sp;
    uint32_t status;
    uint32_t reason;
    uint32_t crc;
};
```
The exact register set and ABI are target-specific; the format should be deliberately versioned.

## Edge cases and failure modes
- A corrupted stack can make unwinding impossible.
- The crash handler itself can fault and overwrite evidence.
- Cached or DMA-owned data may not represent the latest state.
- Reset/power sequencing can erase volatile crash data.
- An incorrect symbol file creates misleading backtraces.
- Recursive fault handling can cause watchdog reset before persistence.

## Verification / debugging
Test crash capture deliberately: null/invalid access where safe, assertion failure, watchdog reset, stack exhaustion, and corrupted-state scenarios. Verify that the crash handler is minimal and uses only facilities known to remain safe after the fault. Validate the stored record after reboot and decode it using the exact build artifact.

For hosted systems, retain the core, executable, shared-library versions, and debug symbols together. For firmware, retain the production image and linker map as immutable artifacts for every released build.

## Staff-level takeaway
A crash dump is only valuable if it preserves the evidence needed to answer **what failed, where, under which build, and with what machine state**. Design crash capture as an observability subsystem with versioning, integrity, bounded resource use, and recovery guarantees—not as an afterthought.

## Related
[[00_Chapter_Index]]
[[04_Call_stacks]]
[[05_Registers]]
[[09_Post_mortem_analysis]]
[[../84_C_Fault_Containment/00_Chapter_Index]]
