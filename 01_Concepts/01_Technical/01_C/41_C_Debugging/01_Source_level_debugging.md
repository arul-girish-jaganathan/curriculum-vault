# Source-level debugging

> Canonical C topic note — Chapter 41. This note treats the debugger as an observation tool, not as part of the C language semantics. The source program, generated machine code, ABI, debug information, and target state must be kept conceptually separate.

## Definition
Source-level debugging is the process of relating C source constructs to the executing program through debug information such as DWARF, PDB, or compiler/debugger-specific formats. A breakpoint on a C line, a displayed local variable, and a source-level call stack are conveniences derived from compiler-generated metadata; ISO C does not define debugger behavior, breakpoint semantics, register display, or the accuracy of debug information.

The central distinction is:

`C source -> translation/optimization -> machine instructions + debug metadata -> CPU execution -> debugger observation`

A debugger can therefore show an expression, variable, or source line that is useful but not literally identical to a runtime object. Optimized code may eliminate, split, merge, reorder, or keep a value only in a register. A source line can correspond to multiple instruction ranges, and one instruction can be associated with more than one source location.

## Mechanism and language rules
The compiler emits machine code and debug metadata while applying the language rules and permitted optimizations. Debug metadata normally maps instruction addresses to source files/lines and describes variable locations or location ranges. It does not make an object exist at runtime when the optimizer has proven that no observable behavior requires it.

### What to reason about
- **Language semantics:** Is the C program itself defined? A debugger cannot repair undefined behavior.
- **Object identity:** A source variable may occupy a stack slot, register, several locations over time, or no physical location.
- **Lifetime:** A local object is meaningful only during its lifetime; a debugger's stale display does not extend that lifetime.
- **Evaluation:** Inspecting an expression may cause debugger-side evaluation or memory reads and should not be confused with the original program evaluation.
- **Optimization:** `-O2`/`-O3`, inlining, constant propagation, dead-code elimination, register allocation, and tail calls can make source stepping non-linear.
- **ABI:** Parameter and return values may be in registers rather than memory; stack frames may omit a traditional frame pointer.
- **Concurrency:** A thread or ISR can change state between observations; a watch window is not a synchronization primitive.

A useful debugging hierarchy is: first establish the failing externally observable behavior, then identify the relevant state, then establish the instruction path that produced it, and only then interpret source-level variables.

## Embedded implications
On MCUs, source debugging commonly occurs through SWD/JTAG and a hardware debug architecture. Halting the core can change timing, peripheral behavior, watchdog servicing, interrupt latency, DMA progress, and race behavior. Some peripherals continue operating while the CPU is halted; others can be frozen by debug configuration.

Debug information increases artifact size even when it is separated from the production image. Breakpoints and watchpoints are constrained by the target: hardware breakpoints may be limited in number, flash breakpoints may require patching or a debug probe algorithm, and data watchpoints are often limited to a few address comparators.

### Firmware review angle
Compare debug and release builds when investigating an optimization-sensitive defect. Do not conclude that a defect is absent because a debug build works. Preserve the exact compiler version, flags, linker script, startup code, map file, image hash, and debug artifact used for the failing binary.

## Edge cases and failure modes
1. **“Variable says optimized out.”** This can be correct; the compiler proved that a memory representation was unnecessary.
2. **Source line appears to execute twice.** Multiple instruction ranges can share line metadata, or control flow may legitimately return to the line.
3. **Incorrect-looking call stack.** Frame-pointer omission, tail calls, corrupted stack memory, or missing unwind metadata can break unwinding.
4. **Debugger changes the bug.** Halting, single-stepping, or reading a volatile peripheral register can alter timing or device state.
5. **Stale register display.** The debugger UI may not have refreshed, or the register may change asynchronously.
6. **Undefined behavior investigation.** Once UB occurs, source-level observations cannot be used as proof of what the C abstract machine “must” do.

## Example pattern
```c
static uint32_t clamp_counter(uint32_t value, uint32_t limit)
{
    if (value > limit) {
        value = limit;
    }
    return value;
}

void service(void)
{
    uint32_t n = read_counter();
    n = clamp_counter(n, 100U);
    publish_count(n);
}
```

At `-O0`, `n` may have a stack location. At `-O2`, `clamp_counter()` may be inlined and `n` may live entirely in registers. The source remains valid while its physical representation changes.

## Verification / debugging
Use `-g` plus a controlled optimization level for ordinary source debugging, but retain a production-equivalent build for reproducing timing and optimization defects. Inspect disassembly when source stepping becomes misleading. Use debugger commands to examine registers, raw memory, stack frames, and instruction addresses rather than trusting one UI field.

A Staff-level review should ask:
- What exact binary is running?
- Which source line-to-address mapping is being used?
- Is the observed variable optimized, volatile, atomic, shared with an ISR, or DMA-owned?
- Could halting the CPU change the failure?
- Can the hypothesis be validated with trace, GPIO timing, counters, logging, or a post-mortem dump without stopping the system?

## Staff-level takeaway
Treat source-level debugging as a **model-to-machine correlation problem**. The debugger is evidence, not authority. For difficult embedded failures, correlate C semantics, compiler transformations, ABI state, instruction addresses, memory ownership, interrupt behavior, and target timing before deciding what the source-level display means.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
