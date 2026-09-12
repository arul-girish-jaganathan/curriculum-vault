# Breakpoints

> Canonical C topic note — chapter 41.

## Definition
A breakpoint is a debugger-controlled condition that suspends CPU execution when a selected instruction address or event is reached. Breakpoints are not part of ISO C; they are implemented by processor debug logic, operating-system facilities, debugger software, or explicit instrumentation.

The fundamental question is not merely “where do I stop?” but **whether stopping preserves the system behavior that produced the fault**.

## Mechanism and language rules
A source breakpoint is resolved approximately as:

`source file + line → debug line table → address range → machine instruction(s)`

The mapping depends on the exact executable and its debug information. A source statement may map to several instructions, while several statements can map to one instruction range after optimization.

### Software breakpoints
A common software breakpoint replaces an instruction with a trap instruction, records the original instruction, and restores or single-steps it when execution resumes. This requires the target memory to be writable and executable in the required way. Flash, ROM, execute-only memory, protected code, or shared instruction memory can make software patching unavailable or undesirable.

### Hardware breakpoints
Debug hardware can compare the program counter against a small number of programmed addresses. Hardware breakpoints generally avoid modifying program memory but are finite and architecture-specific.

### Conditional and temporary breakpoints
A conditional breakpoint stops only when a predicate evaluates true. A temporary breakpoint removes itself after a selected hit. Complex conditions can consume significant debugger/target resources or produce unsafe side effects if they require evaluating target expressions.

### Function and exception breakpoints
Modern debuggers may also stop on function entry, shared-library events, exception vectors, signals, or catchpoints. On bare-metal systems, equivalent facilities often mean trapping on reset handlers, fault handlers, or selected ISR entry points.

## Embedded implications
MCU debugging introduces timing and resource constraints:

- Hardware breakpoint comparators are limited.
- Software breakpoints may not work in flash/ROM or protected regions.
- A halted core may leave DMA, timers, watchdogs, peripherals, or another CPU running.
- An ISR breakpoint can destroy latency and alter interrupt nesting.
- A breakpoint can prevent a watchdog from being serviced and create a secondary reset.
- A debug halt can hide a race by changing scheduling and bus timing.

For safety or real-time firmware, prefer non-halting evidence for timing-sensitive failures: trace packets, GPIO transitions, cycle counters, event ring buffers, hardware trace, or captured fault state.

### Example investigation
```c
int process_packet(const uint8_t *buf, size_t len)
{
    if (len > RX_CAPACITY) {
        ++error_count;
        return -1;
    }
    return decode_packet(buf, len);
}
```
A breakpoint on the error path can establish whether an invalid length reaches this layer. Inspect the caller, buffer ownership, and decoded length. If the defect disappears under the breakpoint, suspect timing, concurrency, uninitialized state, or an external producer rather than concluding that the breakpoint “fixed” the program.

## Edge cases and failure modes
- Breakpoint cannot bind because the function was inlined or eliminated.
- A breakpoint lands on a shared instruction generated for multiple source locations.
- Software breakpoint insertion fails because the memory cannot be patched safely.
- A conditional expression reads MMIO or otherwise changes target state.
- Stopping in a high-rate ISR causes missed deadlines.
- Stopping one core while another accesses shared data produces misleading observations.
- An early boot fault occurs before the debugger attaches.
- The breakpoint changes code bytes in a region checked by a bootloader or integrity monitor.

## Verification / debugging
Before interpreting a stop:

1. Confirm the loaded image and symbol file match exactly.
2. Determine whether the breakpoint is hardware or software.
3. Check available hardware breakpoint resources.
4. Record the hit count and exact PC.
5. Inspect surrounding instructions, not only the source line.
6. Remove or replace the breakpoint when testing timing-sensitive hypotheses.

For intermittent bugs, compare behavior in three modes: normal execution, intrusive debugging, and non-intrusive instrumentation. Differences between the first two are useful evidence of observer effect.

## Staff-level takeaway
Use breakpoints as controlled experiments. For deterministic control-flow defects they are excellent; for races, DMA corruption, watchdog resets, power-state bugs, and hard real-time violations they can destroy the evidence. A senior engineer chooses the least invasive observation method that can answer the specific hypothesis.

## Related
[[00_Chapter_Index]]
[[01_Source_level_debugging]]
[[03_Watchpoints]]
[[07_Optimized_code_debugging]]
[[12_Debugging_production_firmware]]
