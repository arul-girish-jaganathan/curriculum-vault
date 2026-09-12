# Source-level debugging

> Canonical C topic note — Chapter 41. Source-level debugging is a correlation technique between C source, generated code, debug metadata, ABI state, and live target state. The debugger observes execution; it does not define C semantics.

## Definition
Source-level debugging maps C source constructs to the executing program through debug information such as DWARF, PDB, or compiler/debugger-specific formats. ISO C does not define breakpoints, stepping, watch windows, stack unwinding, variable display, or debugger expression evaluation.

The useful mental model is:

`C source -> translation -> optimization -> machine code + debug metadata -> CPU execution -> debugger observation`

A source variable is therefore not synonymous with a fixed RAM location. Depending on optimization and ABI, a value can reside in a register, stack slot, several locations over time, be constant-folded, be reconstructed from other values, or have no independently materialized representation. A source line may map to many instruction ranges and an instruction may have imperfect source correspondence.

## Mechanism and language rules
The compiler must preserve the observable behavior required by the C abstract machine, while debug metadata describes how generated instructions relate to source constructs. Optimization can legally change representation and ordering when observable behavior is preserved.

### What to reason about
- **Language semantics:** Is the source program itself defined? Debugging cannot make undefined behavior meaningful.
- **Object lifetime:** A debugger display does not extend an object's lifetime.
- **Object identity:** A displayed value may be reconstructed rather than read from the original object representation.
- **Evaluation:** Debugger-side expression evaluation is separate from the program's original evaluation and may read memory or invoke target-specific mechanisms.
- **Optimization:** Inlining, constant propagation, dead-code elimination, register allocation, tail calls, and loop transforms affect stepping and variable availability.
- **ABI:** Parameters and return values may be held in registers; stack frames may omit frame pointers; unwind metadata may be required for reliable backtraces.
- **Concurrency:** Another thread, ISR, DMA engine, or peripheral can change state between observations.

A strong workflow is: establish the externally visible failure, identify the relevant invariant, capture raw machine state, map addresses to symbols, then interpret source variables in that context.

## Embedded implications
MCU debugging commonly uses SWD/JTAG and a debug probe. Halting the CPU can change interrupt latency, watchdog behavior, peripheral progression, DMA timing, power state, and race windows. Some devices freeze selected peripherals while halted; others continue operating.

Debug builds can also change layout and timing. `-O0` may create stack variables that do not exist in a production `-O2` build, while added logging can remove a race or alter stack pressure.

### Firmware review angle
When a failure is optimization-sensitive, preserve the exact compiler version, flags, linker script, startup code, ELF/debug artifact, map file, image hash, and target configuration. Compare the failing production-equivalent binary against a debug build rather than assuming the debug build is authoritative.

## Edge cases and failure modes
- **Optimized out:** the compiler proved a separate storage location was unnecessary.
- **Wrong source line:** line tables are approximate mappings, not a trace of the abstract machine.
- **Bad backtrace:** stack corruption, tail calls, frame-pointer omission, or missing unwind metadata can defeat unwinding.
- **Stale display:** UI refresh does not guarantee a stable snapshot.
- **MMIO side effects:** inspecting a peripheral register can acknowledge, clear, or otherwise alter hardware state.
- **UB:** after undefined behavior, source-level observations cannot prove what the C abstract machine must have done.

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

At `-O0`, `n` may occupy a stack slot. At `-O2`, `clamp_counter()` may be inlined and `n` may exist only in registers. Both are valid implementations.

## Verification / debugging
Build with debug information and a controlled optimization level for normal source debugging, but retain a production-equivalent build for timing and optimization defects. When stepping becomes confusing, inspect disassembly, registers, raw memory, instruction addresses, and the exact ELF/symbol file.

Useful checks include:
- Confirm the running image hash matches the symbol file.
- Translate the fault PC to an exact instruction and source range.
- Inspect SP, LR/return address, status registers, and relevant ABI argument registers.
- Determine whether the object is optimized, volatile, atomic, shared, or hardware-owned.
- Reproduce with trace, counters, GPIO timing, or persistent fault records if halting changes the bug.

Staff-level questions: What exact binary is running? What source-to-instruction evidence exists? Could the debugger perturb the failure? What independent measurement would falsify the current hypothesis?

## Staff-level takeaway
Treat source-level debugging as a **model-to-machine correlation problem**. The debugger is evidence, not authority. Difficult firmware failures require correlation of C semantics, compiler transformations, ABI state, instruction addresses, memory ownership, interrupt behavior, and timing.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
