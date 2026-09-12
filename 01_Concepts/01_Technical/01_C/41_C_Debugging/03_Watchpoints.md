# Watchpoints

> Canonical C topic note — Chapter 41. A watchpoint observes a target address or value change using debugger/hardware facilities; it is not a C semantic feature.

## Definition
A watchpoint requests a debug event when a memory location is accessed or modified. Implementations may provide data breakpoints for writes, reads, or both, usually through a small number of hardware address comparators. ISO C specifies neither watchpoints nor debugger observation.

A crucial distinction is between the **C object** and the **machine address currently representing it**. A local variable can move between stack and registers, be optimized away, or be split across locations. A hardware watchpoint normally observes an address, so it may not follow a source variable unless the debugger can track its location ranges.

## Mechanism and language rules
Hardware data breakpoints compare an address, access type, and sometimes access size. When the CPU performs a matching load/store, debug logic raises a trap or halt request. Exact capabilities are CPU-specific. Software emulation may single-step instructions and compare memory, but this can be dramatically slower.

### What to reason about
- Is the object actually stored at the watched address for the entire interval?
- Is the access a byte, halfword, word, or larger transaction?
- Can another core, DMA engine, or peripheral modify the location without a CPU instruction?
- Is the variable optimized into a register?
- Does the target support read, write, or access watchpoints?
- Could the debugger itself read the location and trigger a side effect?

`volatile` tells the compiler that accesses are observable according to the C implementation; it does **not** create a debugger watchpoint and does not make a multi-instruction update atomic.

## Embedded implications
Watchpoints are powerful for locating memory corruption, especially stack overwrites, unexpected register writes, and ownership violations. However, hardware slots are scarce. Watching a structure or array may consume resources or require alignment/size constraints. A DMA engine writing RAM generally does not execute a CPU store, so a CPU data watchpoint may not catch it.

MMIO watchpoints are especially risky. Reading a status register can clear flags, advance FIFOs, acknowledge interrupts, or otherwise alter hardware state. Prefer non-destructive trace or peripheral-specific event mechanisms when available.

### Firmware review angle
For shared buffers, determine whether the writer is CPU, ISR, DMA, another core, or a peripheral. For optimized code, inspect the variable's location ranges and disassembly. If a watchpoint works only at `-O0`, the debugging method may be tied to an artificial memory representation.

## Edge cases and failure modes
- **Watchpoint does not trigger:** DMA/peripheral writes may bypass CPU debug comparators.
- **Too many watchpoints:** target hardware may expose only a few comparator resources.
- **False attribution:** the watched address can be reused after an object's lifetime ends.
- **Partial access:** a wider store can trigger a watchpoint even when the source statement appears unrelated.
- **Compiler optimization:** a source variable may no longer have a stable address.
- **Race sensitivity:** stopping at the first write can hide the timing that causes the corruption.

## Example pattern
```c
struct state {
    uint32_t magic;
    uint16_t length;
    uint16_t flags;
};

static struct state s;

void update_flags(uint16_t flags)
{
    s.flags = flags;
}
```
A write watchpoint on `s.flags` can identify unexpected CPU writers. If corruption still occurs without a CPU watchpoint hit, investigate DMA, buffer overruns, MPU faults, or another bus master.

## Verification / debugging
Start with a suspected invariant such as “only `update_flags()` writes this field.” Set a hardware write watchpoint, reproduce the fault, inspect the call stack and instruction that caused the event, and record the address and access width. Then verify all other writers statically and inspect DMA descriptors/bus ownership if relevant.

Staff-level questions:
- Who owns the memory at the instant of failure?
- Can a non-CPU bus master modify it?
- Is the watched object lifetime stable?
- Does the debugger intervention alter timing?
- What evidence would distinguish overwrite, use-after-lifetime, DMA corruption, and race?

## Staff-level takeaway
Use watchpoints to test a **specific ownership or mutation hypothesis**, not as a substitute for understanding the memory model. In embedded systems, always account for non-CPU writers, scarce hardware comparators, MMIO side effects, optimization, and the possibility that halting changes the race.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
