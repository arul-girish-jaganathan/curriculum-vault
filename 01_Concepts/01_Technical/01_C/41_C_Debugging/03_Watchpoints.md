# Watchpoints

> Canonical C topic note — Chapter 41. A watchpoint stops or records execution when a selected memory location changes or is accessed. It is debugger functionality, not an ISO C feature, and is tightly constrained by target debug hardware.

## Definition
A watchpoint observes a data address or address range. A **write watchpoint** detects modification, a **read watchpoint** detects access, and an **access watchpoint** detects either. Some targets implement this with data watchpoint comparators; others use software instrumentation or emulation.

A watchpoint is especially useful when the question is “who changed this object?” rather than “where is this function called?”

## Mechanism and language rules
The debugger programs hardware comparators or instruments execution. The C program continues to obey its normal semantics; the watchpoint merely observes or interrupts execution at selected machine accesses.

### What to reason about
- What exact address and access size is monitored?
- Is the compiler using a different representation of the source object?
- Is the target comparator byte-, halfword-, word-, or range-granular?
- Could another core, DMA engine, or peripheral modify the memory without the CPU comparator seeing it?
- Is the monitored object `volatile`, atomic, shared with an ISR, or ordinary RAM?
- Does the watchpoint consume scarce hardware resources?

A watchpoint on an optimized-away variable may be impossible. A watchpoint on a structure member must account for its actual address and size, padding, and possible compiler transformations.

## Embedded implications
Hardware watchpoints are excellent for corruption bugs but are limited on many MCUs. DMA writes may not trigger a CPU data watchpoint, and bus masters can change memory independently. Cache coherency can further complicate what the CPU observes.

A watchpoint that halts on every packet-buffer write can destroy real-time behavior. Prefer narrow address ranges and carefully chosen trigger conditions.

### Firmware review angle
Document whether the watchpoint observes CPU accesses only or all bus masters. When investigating corruption, combine watchpoints with ownership tracking, DMA descriptors, MPU faults, canaries, and event logs.

## Edge cases and failure modes
- **False confidence:** DMA/peripheral writes bypass CPU watchpoint hardware.
- **Granularity mismatch:** a comparator may cover a larger region than intended.
- **Read-side effects:** watching MMIO reads can perturb hardware behavior.
- **Optimization:** the source object may be split or eliminated.
- **Resource exhaustion:** multiple watchpoints may exceed available comparators.

## Example pattern
```c
struct state {
    uint32_t sequence;
    uint32_t status;
};

static struct state g_state;

void update(void)
{
    g_state.status = STATUS_READY;
}
```
A useful experiment is to watch the address of `g_state.status` for writes and capture the exact PC at each trigger. Then map that PC back to the instruction and call path.

## Verification / debugging
Confirm the monitored address from the debugger and map file, then inspect the generated store instruction. If no trigger occurs despite observed corruption, consider DMA, another core, cache effects, memory remapping, or an incorrect address.

Use canaries and periodic integrity checks when interactive watchpoints are impossible. Validate the diagnostic method on a known-good target before relying on it for a field failure.

Staff-level questions: Which agents can write this memory? Does the hardware watchpoint cover them? What is the trigger granularity and timing cost? Can ownership be proven independently?

## Staff-level takeaway
A watchpoint is powerful only when its **observation boundary matches the actual writer set**. Always identify CPU, ISR, DMA, peripheral, and other-core writers before concluding that a watchpoint proves causality.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
