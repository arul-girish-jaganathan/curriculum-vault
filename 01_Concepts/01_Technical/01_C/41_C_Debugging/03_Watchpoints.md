# Watchpoints

> Canonical C topic note — chapter 41.

## Definition
A watchpoint stops execution when a selected memory location is accessed or modified. Unlike a source breakpoint, which targets control flow, a watchpoint targets data behavior. Watchpoints are debugger facilities, not ISO C language features.

## Mechanism and language rules
Many processors provide debug comparators that match an address, access type, and sometimes access size. A write watchpoint can reveal which instruction corrupts a variable. A read watchpoint can reveal unexpected consumers. Exact size, alignment, address range, and comparator count are architecture-specific.

The important distinction is **source object versus physical address**. A C object may move between registers and memory under optimization. If `x` is register-resident, a hardware memory watchpoint cannot observe every logical change to `x` because no memory write occurs.

```c
struct state {
    uint32_t mode;
    uint32_t count;
};

static struct state s;
```
A watchpoint on `s.count` is useful for finding an unexpected writer, but only while the object actually resides at that stable address.

## Embedded implications
Watchpoints are powerful for stack corruption, buffer overruns, MMIO access, and ownership violations, but target hardware often has very few resources. A watched MMIO address can be especially dangerous: observing accesses to a peripheral register may alter timing or interact with clear-on-read/status semantics.

For DMA, a CPU watchpoint may not detect a DMA engine writing the buffer because the transfer does not execute a CPU load/store instruction. Use DMA descriptors, peripheral status, memory poisoning, MPU faults, trace, or post-transfer validation instead.

### Alignment and granularity
Some debug units require naturally aligned addresses and support only certain access sizes. A request to watch one byte may consume a comparator that matches a larger aligned region, depending on the architecture.

## Edge cases and failure modes
- Optimized variables can be unavailable or register-resident.
- Compiler-generated stores may make the apparent source writer different from the logical assignment.
- A watchpoint may trigger repeatedly because of polling or stack traffic.
- DMA, another core, or a peripheral may modify memory without CPU debug-watchpoint support.
- Hardware watchpoint resources can be exhausted.
- Watching a shared variable in concurrent code can stop execution before the race reproduces naturally.

## Verification / debugging
When searching for memory corruption, first establish the object lifetime and exact address. Record the watchpoint access type and width. When it triggers, inspect the PC, instruction, stack frame, register values, and caller chain. Then determine whether the access is the intended source-level operation or compiler-generated support code.

For difficult corruption, surround buffers with guard values and periodically validate them. Combine this with sanitizers on host builds and MPU/watchpoint facilities on target builds.

## Staff-level takeaway
Watchpoints answer a precise question: **which execution agent touched this location, and when?** They do not prove that the C object model is being respected. For DMA, multicore, MMIO, optimized code, or lifetime bugs, combine debugger evidence with ownership, synchronization, linker/map information, and target trace rather than relying on one watchpoint.

## Related
[[00_Chapter_Index]]
[[02_Breakpoints]]
[[06_Memory_inspection]]
[[10_Fault_localization]]
