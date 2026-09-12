# ISR stack usage

> Canonical C topic note — Chapter 44. ISR stack sizing must account for hardware exception frames, compiler-generated frames, local objects, callees, floating-point context, nesting, and RTOS interactions.

## Definition
ISR stack usage is the additional stack consumed by interrupt entry and handler execution. ISO C does not define the stack layout; the processor architecture, ABI, compiler, interrupt mechanism, and RTOS do.

## Mechanism and language rules
Hardware may push an exception frame, after which compiler-generated prologue code saves additional registers and allocates locals. Calls from the handler add frames, and nested interrupts can create several contexts simultaneously.

### What to reason about
- Hardware-saved frame size.
- Compiler prologue/epilogue.
- Local objects and alignment.
- Maximum transitive call depth.
- Maximum nesting depth.
- Floating-point/vector context.
- Fault-handler stack usage.

## Embedded implications
Stack overflow can corrupt task stacks, globals, heap metadata, return addresses, or exception frames, producing misleading secondary faults. Debugger observations are not worst-case bounds.

### Firmware review angle
Use static stack analysis, linker-defined boundaries, guard regions, MPU protection, and runtime high-water marks. Re-run analysis after compiler, optimization, library, or interrupt-priority changes.

## Edge cases and failure modes
- Large local arrays in an ISR.
- Hidden deep library calls.
- Floating-point use expands saved context.
- High-priority nesting exhausts stack.
- Debug and release frames differ substantially.

## Example pattern
```c
void SPI_IRQHandler(void)
{
    uint8_t sample[16];
    capture_spi(sample, sizeof sample);
    queue_from_isr(sample);
}
```
The local array plus every callee contributes to worst-case stack usage.

## Verification / debugging
Fill the stack with a known pattern and measure high-water mark under worst-case interrupt load. Combine this with compiler stack-usage output and static call-graph analysis. Stress maximum nesting and fault-handler entry.

Staff-level questions: What is the maximum simultaneous frame depth? What context is hardware-saved? Can the fault handler run when the interrupted stack is already near its limit?

## Staff-level takeaway
ISR stack sizing is a **worst-case composition problem**. Account for hardware, compiler, calls, nesting, and exceptional paths rather than relying on observed average depth.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
