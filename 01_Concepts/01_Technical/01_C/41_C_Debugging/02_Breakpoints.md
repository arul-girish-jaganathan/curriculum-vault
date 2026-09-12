# Breakpoints

> Canonical C topic note — chapter 41.

## Definition
A breakpoint is a debugger-controlled condition that stops CPU execution when a selected instruction or event is reached. The C language does not define breakpoints; they are supplied by debug hardware, a debugger, an operating system, or instrumentation.

## Mechanism and language rules
The common software-breakpoint model replaces an instruction with a trap instruction, remembers the original instruction, and restores it when execution resumes. Hardware breakpoints instead use processor debug comparators to match an instruction address, and often data accesses. Exact counts and capabilities are architecture-specific.

A source breakpoint is translated approximately as:
`C source location → debug line table → address range → machine instruction`.

A breakpoint therefore depends on the exact ELF/image and debug information. Multiple source statements can map to one instruction, and optimized code can move, merge, inline, or eliminate operations.

### Conditional and temporary breakpoints
A conditional breakpoint evaluates a predicate each time the breakpoint is hit. A temporary breakpoint removes itself after the first stop. Conditions involving function calls can change program state and can be unsafe in firmware.

## Embedded implications
On MCUs, breakpoint resources are limited. Software breakpoints may be impossible in flash, execute-only memory, ROM, or protected regions. Hardware breakpoint comparators are finite. Halting the core may not halt timers, DMA, watchdogs, other cores, or external devices.

A breakpoint inside a high-rate ISR can distort latency dramatically. For timing-sensitive firmware, prefer trace, GPIO instrumentation, counters, or non-halting logging.

### Example investigation
```c
if (rx_len > sizeof(rx_buf)) {
    error_count++;
    return -1;
}
```
Set a breakpoint on the error path, then inspect `rx_len`, the caller, and the buffer ownership. If the fault disappears when stopped, suspect a race or timing dependency rather than assuming the breakpoint fixed the bug.

## Edge cases and failure modes
- Breakpoint cannot bind because the code was inlined or removed.
- A breakpoint lands on a shared instruction generated for several source lines.
- Software breakpoint patching fails because memory is read-only or not writable.
- A conditional expression has side effects.
- A breakpoint in an interrupt handler causes missed deadlines or watchdog resets.
- Stopping one core while another continues can create misleading shared-memory observations.
- Breakpoints inserted after startup may miss an early boot failure.

## Verification / debugging
Confirm the loaded image and symbols match. Check whether the breakpoint is hardware or software and how many resources remain. For intermittent failures, compare behavior with and without breakpoints. If halting changes behavior, replace the breakpoint with a tracepoint-like mechanism: timestamped ring-buffer events, GPIO edges, ETM/trace where available, or counters sampled after failure.

## Staff-level takeaway
Choose breakpoints based on the failure's temporal properties. A breakpoint is excellent for deterministic control-flow bugs but can destroy the evidence for concurrency, real-time, watchdog, DMA, and power-state bugs. Senior debugging asks not only “where should I stop?” but “will stopping preserve the system behavior I am trying to observe?”

## Related
[[00_Chapter_Index]]
[[03_Watchpoints]]
[[07_Optimized_code_debugging]]
[[12_Debugging_production_firmware]]
