# Breakpoints

> Canonical C topic note — Chapter 41. A breakpoint is a debugger/target mechanism, not a C language feature. Its meaning depends on the CPU debug architecture, probe, debugger, memory type, and build.

## Definition
A breakpoint requests that execution stop or trap when a selected instruction address or event is reached. A **source breakpoint** is translated from a C source location into one or more machine-code addresses using debug information. ISO C defines none of this behavior.

The important chain is:

`C line -> debug line table -> instruction address -> breakpoint mechanism -> debug exception/halt`

A source line can map to several addresses because of branches, inlining, macro expansion, or optimization. Conversely, optimized instructions may have no convenient one-to-one source statement.

## Mechanism and language rules
Common breakpoint mechanisms include hardware instruction comparators, software breakpoints that replace an instruction with a trap instruction, and debugger-specific flash breakpoint facilities. Hardware breakpoints generally avoid modifying program memory and are valuable for read-only flash. Software breakpoints can be problematic in ROM/flash or when code integrity matters.

Conditional breakpoints typically stop only when a condition is true. Depending on the debugger, evaluating that condition may require reading target memory/registers or executing target-side helper code. The condition itself can therefore be expensive or unsafe when applied to MMIO or time-sensitive firmware.

### What to reason about
- Which exact instruction address is selected?
- Does the target support a hardware breakpoint at that address?
- Is the code in flash, RAM, ROM, or a dynamically generated region?
- Has inlining or optimization created multiple valid locations?
- Is the breakpoint inside an ISR, fault handler, or critical timing path?
- Can another core, DMA engine, or peripheral continue while the CPU is halted?

A breakpoint stops **execution**, not necessarily the whole system.

## Embedded implications
Halting an MCU can violate watchdog deadlines, increase interrupt latency, allow UART FIFOs to overflow, pause a producer while DMA continues, or alter a race condition. Some debug configurations freeze selected timers or peripherals; others do not. Therefore “it works when debugging” is weak evidence for a real-time bug.

Hardware breakpoint resources are finite. On many MCUs, only a small number of instruction comparators are available, and some debuggers transparently fall back to less desirable mechanisms. Flash breakpoints may consume erase/program operations or require RAM shadowing.

### Firmware review angle
For timing-sensitive bugs, prefer trace, event counters, GPIO timestamps, ITM/SWO where available, ETM/trace where supported, or persistent fault records. Use breakpoints for state inspection when stopping the system is known to be safe.

## Edge cases and failure modes
- **Breakpoint never hits:** the source line may have been optimized away, the function may not be called, or the debug image may not match the running image.
- **Wrong instruction:** a source location can correspond to several instruction ranges.
- **Breakpoint disappears:** limited hardware slots or debugger reprogramming can remove it.
- **Conditional breakpoint changes behavior:** the condition adds memory accesses or latency.
- **Breakpoint in flash changes image state:** software breakpoint patching can alter code bytes.
- **ISR breakpoint causes cascading faults:** prolonged halt may allow watchdog, peripherals, or external devices to reach unexpected states.

## Example pattern
```c
static volatile uint32_t error_count;

void record_error(uint32_t code)
{
    error_count++;
    log_error(code);
}
```
A breakpoint on `error_count++` may correspond to several instructions: load, increment, and store. If the variable is shared with an ISR, stopping between those instructions can expose an intermediate machine state that ordinary source-level reasoning hides.

## Verification / debugging
Confirm the ELF/debug artifact matches the flashed image. Inspect the disassembly around the source location and check breakpoint allocation. For an embedded target, document whether the watchdog, timers, DMA, and interrupts run during halt. If a conditional breakpoint is used, verify that the condition does not read destructive MMIO registers or introduce unacceptable latency.

Staff-level questions:
- What hypothesis does this breakpoint test?
- What observable result would falsify the hypothesis?
- Is halting behavior representative of field behavior?
- Is a trace/counter/fault-record solution safer?
- Are breakpoint resources shared with other debugging features?

## Staff-level takeaway
A breakpoint is an **instrumentation intervention**. Use it deliberately: understand what stops, what continues, what state can change while halted, and how compiler optimization maps the source location to instructions. For production-like failures, prefer non-intrusive evidence when timing and concurrency matter.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
