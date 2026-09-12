# Source-level debugging

> Canonical C topic note — chapter 41.

## Definition
Source-level debugging is the practice of observing and controlling machine execution while presenting the evidence in terms of C source code. A debugger combines the executable image with debug information—commonly DWARF—to map program counters, machine instructions, types, source lines, stack frames, and variable locations.

Source-level debugging is a toolchain facility, not an ISO C language feature. ISO C defines the abstract execution semantics; the compiler and debugger must reconstruct enough correspondence between source intent and generated code to make debugging useful.

## Mechanism and language rules
A useful mental model is:

`C source → preprocessing → compilation → optimization → instruction selection → linking → executable image + debug information → debugger view`

Debug information can contain line tables, lexical scopes, type descriptions, symbol information, call-frame information, and variable-location expressions. The debugger uses these to answer questions such as:

- Which source location corresponds to the current PC?
- What function/frame is active?
- Where is object `x` currently located?
- What source type describes these bytes?
- Which machine instructions implement this statement?

A source object is not guaranteed to exist as a stable RAM location. The compiler may place it in a register, recompute it, merge it with another value, split its lifetime across several locations, constant-propagate it, or eliminate it completely when no observable behavior requires it.

### Source lines are not execution steps
One source statement can compile to many instructions. Conversely, several source statements may share or collapse onto a small instruction range. Instruction scheduling, common-subexpression elimination, inlining, tail calls, and dead-code elimination can make source stepping appear non-linear.

### Optimization and the C abstract machine
The debugger is not a second execution engine. When undefined behavior occurs, the compiler is permitted to assume the invalid case does not happen and may transform code in ways that make intuitive source stepping misleading. Debugging must therefore distinguish:

`language contract violation` → `optimizer consequence` → `observed machine state`.

### Important compiler/debug options
Typical toolchain controls include:

```text
-g                      emit debug information
-O0 / -Og / -O2 / -O3   select optimization level
-fno-omit-frame-pointer retain a conventional frame chain where supported
-g3                     include richer macro/debug detail in toolchains that support it
```

Exact options and debug formats are compiler-specific. A reproducible debug session requires the exact binary, symbols, compiler version, flags, linker script, and relevant generated artifacts.

## Embedded implications
For MCU firmware, source-level debugging crosses directly into hardware state. Correlate C objects with:

- linker-map regions for `.text`, `.rodata`, `.data`, `.bss`, stack, heap, and retained RAM;
- MMIO register definitions and actual target addresses;
- exception and interrupt entry frames;
- DMA descriptors and buffers;
- MPU/MPU-like region permissions and cache attributes where applicable;
- boot stage and image slot information.

A halt is an invasive experiment. Depending on the target, timers, watchdogs, DMA engines, peripherals, other cores, and external devices can continue operating. Consequently, a bug caused by a race, timeout, or hardware interaction may disappear or change under a debugger.

### Example
```c
static uint32_t checksum(const uint8_t *p, size_t n)
{
    uint32_t sum = 0U;
    for (size_t i = 0; i < n; ++i) {
        sum += p[i];
    }
    return sum;
}
```
At low optimization the debugger may show `p`, `n`, `i`, and `sum` as obvious variables. At higher optimization, `p` may live in a register, `i` may be folded into pointer arithmetic, and `sum` may remain solely in a register. The source view is therefore an interpretation of instruction state, not proof that identical C objects exist physically.

## Edge cases and failure modes
- `variable optimized out` is usually a property of code generation, not evidence of corrupted RAM.
- An ELF/image mismatch invalidates line numbers, symbols, and addresses.
- Inlined functions can produce inline frames rather than ordinary call frames.
- Tail-call optimization can remove an expected caller frame.
- Undefined behavior can invalidate assumptions about source order and values.
- Reading a volatile MMIO register from a debugger can have hardware side effects.
- A debugger expression can execute target-side code or trigger memory reads that were not part of the original execution.
- Memory might be inaccessible because the processor is in a different privilege/security state.
- LTO may move code and merge functions across translation-unit boundaries.

## Verification / debugging
Use a disciplined evidence chain:

1. Freeze the exact firmware image and symbol file.
2. Verify image hash/build ID and reset/boot stage.
3. Establish the faulting PC and exception context.
4. Compare source view with disassembly when behavior is surprising.
5. Inspect registers, stack memory, and relevant MMIO state.
6. Check compiler diagnostics and sanitizer results on a host reproduction.
7. Use trace, instrumentation, or a crash record when halting changes timing.

For recurring failures, archive the executable and debug metadata with the firmware artifact. A source commit alone is insufficient when compiler versions, flags, linker scripts, generated headers, or link-time layout can change addresses and optimization.

## Staff-level takeaway
Treat source-level debugging as a reconstruction problem: **source intent → compiler transformation → instructions → CPU state → peripheral/system state**. A strong debugger session proves facts across those layers instead of assuming that the source window is the ground truth. When source and machine views disagree, move downward to disassembly, ABI/frame information, memory maps, and fault registers until the disagreement is explained.

## Related
[[00_Chapter_Index]]
[[02_Breakpoints]]
[[04_Call_stacks]]
[[05_Registers]]
[[07_Optimized_code_debugging]]
[[../37_C_Compiler_Optimization/00_Chapter_Index]]
[[../39_C_Diagnostics_Static_Analysis/00_Chapter_Index]]
