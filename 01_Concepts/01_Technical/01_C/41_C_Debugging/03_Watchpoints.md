# Watchpoints

> Canonical C topic note — chapter 41.

## Definition
A watchpoint stops execution when a selected memory location is accessed or modified. It is a data-oriented debugging mechanism: breakpoints answer “where did control flow reach?”, while watchpoints answer “which execution caused this memory access?”. Watchpoints are debugger/processor facilities, not ISO C language features.

## Mechanism and language rules
Many CPUs implement debug comparators that match an address, access direction, and sometimes access width. Exact capabilities vary by architecture.

The critical distinction is:

`C object identity ≠ guaranteed physical memory location`

The compiler may keep a variable in a register, recompute it, spill it only temporarily, split its live range, or eliminate it. A memory watchpoint therefore observes **memory traffic**, not every logical change to a C object.

```c
struct state {
    uint32_t mode;
    uint32_t count;
};

static struct state s;
```
A watchpoint on `s.count` is useful while that object has a stable address and CPU stores are the suspected corruption mechanism.

### Access type and width
A write watchpoint is appropriate for unexpected modification; a read watchpoint identifies consumers. Some targets require natural alignment or offer only specific widths. One watchpoint may therefore cover a larger range than expected.

### Software watchpoints
Where hardware support is absent, a debugger may implement a software watchpoint by periodically reading the value and comparing it. This is slower and may miss short-lived changes between samples. It can also perturb timing substantially.

## Embedded implications
Watchpoints are especially useful for:

- stack corruption;
- buffer overrun detection;
- state-machine fields changing unexpectedly;
- ownership violations between tasks;
- accidental writes to control structures;
- locating CPU-side MMIO traffic.

They have important blind spots. A DMA engine, peripheral, coprocessor, or another CPU can modify memory without executing a CPU instruction that a local hardware watchpoint can catch. A cache or bus fabric can further complicate the observation boundary.

Watching MMIO is also risky. Some registers are clear-on-read, pop-on-read, write-one-to-clear, or timing-sensitive. A debugger inspection that reads them can change the hardware state.

### Example
```c
static uint8_t frame[128];

void receive_byte(uint8_t b)
{
    frame[write_index++] = b;
}
```
If `write_index` is unexpectedly large, a watchpoint on a nearby guard word can reveal the first CPU store that crosses the intended boundary. It does not prove that a DMA transfer or another execution agent is not also corrupting memory.

## Edge cases and failure modes
- Optimized variables can be register-resident or unavailable.
- The compiler may emit multiple stores for one source-level assignment.
- A watchpoint may trigger repeatedly on legitimate polling or stack traffic.
- DMA/peripheral/other-core writes may not trigger the CPU's watchpoint logic.
- Hardware comparator resources are limited.
- Watching a shared variable can perturb a race enough to hide it.
- A watched address can become invalid after object lifetime ends or storage is reused.
- Memory attributes, security domains, or debug permissions may prevent observation.

## Verification / debugging
When investigating corruption:

1. Establish the object's lifetime and exact address.
2. Record expected size and alignment.
3. Select read/write/access watch type deliberately.
4. When triggered, capture PC, instruction, registers, stack frame, and access width.
5. Determine whether the instruction corresponds directly to the source assignment.
6. Check DMA descriptors, interrupts, other cores, and peripheral writers.

For persistent buffers, combine watchpoints with guard values, MPU protection where available, host sanitizers, and periodic integrity checks. For large corruption domains, instrument ownership boundaries instead of placing dozens of individual watchpoints.

## Staff-level takeaway
A watchpoint provides a precise physical observation: **a particular memory access occurred at a particular execution point**. It does not by itself prove compliance with C lifetime, aliasing, concurrency, or ownership rules. For DMA and multicore systems, define the complete set of possible writers before concluding that the observed CPU write is the root cause.

## Related
[[00_Chapter_Index]]
[[02_Breakpoints]]
[[06_Memory_inspection]]
[[10_Fault_localization]]
[[../26_C_Lifetime_Aliasing/00_Chapter_Index]]
