# Source-level debugging

> Canonical C topic note — chapter 41.

## Definition
Source-level debugging maps machine execution back to C source using debug information such as DWARF. It lets an engineer inspect source variables, frames, expressions, and control flow while the CPU executes instructions. The mapping is a debugging aid, not part of ISO C semantics: the compiler is free to transform code as long as the observable behavior remains valid under the language rules.

## Mechanism and language rules
A compiler emits executable code plus debug metadata. The debugger uses symbols, line tables, type information, frame information, and variable-location descriptions to answer questions such as “which source line owns this PC?” and “where is `x` currently stored?”

A source variable may be:
- in a register;
- in a stack slot;
- optimized into another expression;
- constant-propagated;
- split across locations;
- eliminated because it has no observable effect.

Therefore a debugger displaying `x = 10` does not mean a memory location containing `10` necessarily exists. A source line can correspond to several instruction ranges, and one instruction can represent several source operations after optimization.

### Compile-time versus runtime
Debug information normally does not change the C abstract machine. Compiler options such as `-g`, optimization level, frame-pointer policy, link-time optimization, and debug-info format determine how accurately a debugger can reconstruct source intent.

## Embedded implications
For MCU firmware, source-level debugging crosses the boundary between C and hardware state. Inspect:
- stack and heap regions from the linker map;
- MMIO registers using the debugger's target-aware views;
- interrupt context and exception frames;
- peripheral ownership and DMA buffers;
- memory regions with different cache, protection, or access properties.

A halt can itself perturb the system: watchdogs may expire, peripherals may continue running, timing relationships disappear, and an interrupt race may vanish. Debug builds can also alter code placement and timing.

### Example
```c
static uint32_t checksum(const uint8_t *p, size_t n)
{
    uint32_t sum = 0U;
    for (size_t i = 0; i < n; ++i)
        sum += p[i];
    return sum;
}
```
At `-O0`, `sum`, `i`, and `p` often have obvious locations. At higher optimization, `i` may live in a register and `sum` may never be materialized in RAM.

## Edge cases and failure modes
- “Variable optimized out” is not evidence of a compiler bug.
- Stepping can appear to jump backward or skip lines because of instruction scheduling and line-table ranges.
- Inlined functions may create multiple logical frames.
- Undefined behavior can make debugger observations misleading because the compiler no longer has to preserve intuitive execution.
- Reading a volatile MMIO register in a debugger can have hardware side effects.
- Inspecting invalid pointers may trigger a bus fault on the target.
- A stale ELF/image mismatch makes every source-level observation suspect.

## Verification / debugging
Use a reproducible binary and record the exact compiler, flags, linker script, image hash, and debug-symbol file. Confirm the PC belongs to the expected image before interpreting a line number. Compare source view with disassembly when a variable or branch behaves unexpectedly.

Useful evidence includes compiler warnings, sanitizer runs on host builds, debugger watch expressions, disassembly, map files, trace timestamps, and target fault registers.

## Staff-level takeaway
Treat source-level debugging as a reconstruction problem: **source intent → compiler transformation → instructions → hardware state**. When those layers disagree, do not immediately trust the source view. Establish the exact binary, optimization assumptions, ABI/frame rules, and hardware state, then use disassembly and instrumentation to prove the execution path.

## Related
[[00_Chapter_Index]]
[[02_Breakpoints]]
[[04_Call_stacks]]
[[07_Optimized_code_debugging]]
[[../37_C_Compiler_Optimization/00_Chapter_Index]]
