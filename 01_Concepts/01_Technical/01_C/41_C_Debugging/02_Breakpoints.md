# Breakpoints

> Canonical C topic note — Chapter 41. A breakpoint is a debugger-controlled execution stop. It is an observation mechanism outside ISO C, and its implementation, availability, and timing effects depend on the CPU, debug architecture, probe, compiler output, and debugger.

## Definition
A breakpoint causes execution to stop when a selected instruction address or source location is reached. A source breakpoint is translated through debug information into one or more machine-code locations. A function breakpoint resolves a symbol; a hardware breakpoint usually compares the program counter against an address, while a software breakpoint modifies executable code when the target permits it.

The key distinction is between **source intent** and **machine location**. One C line can produce multiple locations, and an inlined function can produce instances at several addresses.

## Mechanism and language rules
Breakpoints do not change ISO C rules, but they can change the execution environment. A software breakpoint may replace an instruction with a trap instruction and restore it when continuing. Hardware breakpoints use dedicated debug comparators and usually avoid code modification.

### What to reason about
- Is the selected source line actually represented in the current optimized binary?
- Is the breakpoint hardware- or software-based?
- How many hardware breakpoint resources are available?
- Does setting it modify flash/RAM or require a debug monitor?
- Can the breakpoint be hit by multiple threads or cores?
- Does stopping execution alter watchdog, interrupt, DMA, or peripheral behavior?

A conditional breakpoint may evaluate a condition each time the location is reached; this can be much more expensive than a simple instruction-address stop.

## Embedded implications
On MCUs, hardware instruction breakpoints are limited resources. Flash-resident code may require hardware comparators because modifying flash is impractical or slow. Some probes implement flash breakpoints through temporary patches, while some CPUs provide dedicated debug resources.

Halting can cause missed deadlines, watchdog expiry, changed interrupt ordering, stalled communication, or altered peripheral state. A breakpoint is therefore inappropriate for diagnosing every real-time failure.

### Firmware review angle
Record the exact breakpoint type and target configuration when reproducing a timing-sensitive bug. Prefer non-halting trace or instrumentation when the failure depends on latency, races, or external bus activity.

## Edge cases and failure modes
- **Breakpoint never hits:** the function was optimized away, inlined elsewhere, or the symbol file does not match the image.
- **Too many breakpoints:** hardware resources are exhausted.
- **Breakpoint changes behavior:** halting changes timing or causes watchdog/reset behavior.
- **ROM/flash restriction:** software patching is unavailable or unsafe.
- **Conditional breakpoint perturbation:** evaluating the condition may add significant latency.

## Example pattern
```c
static void process_packet(const uint8_t *data, size_t length)
{
    if (length > MAX_PACKET) {
        return;
    }
    consume(data, length); /* useful source breakpoint candidate */
}
```
In optimized code, the call may be inlined, transformed, or absent if its observable effect is eliminated. Break on the generated function or instruction address when necessary.

## Verification / debugging
First verify the image and symbol file match. Then inspect the resolved address and instruction bytes. If a source breakpoint behaves unexpectedly, disassemble the surrounding range and set an address breakpoint on the exact instruction.

For embedded diagnosis, test both “halted” and “running” behavior. If the defect disappears only when a breakpoint is present, switch to counters, trace, GPIO timestamps, watchpoints, or persistent breadcrumbs.

Staff-level questions: How many breakpoint resources are available? What timing distortion does the breakpoint introduce? Is the breakpoint observing the real production path or a debug-only code shape?

## Staff-level takeaway
Use breakpoints as **controlled experiments**, not merely convenient stops. Understand their machine-level implementation and explicitly account for their effect on timing, concurrency, watchdogs, and hardware state.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
