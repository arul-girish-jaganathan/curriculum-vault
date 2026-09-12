# ISR stack usage

> Canonical C topic note — Chapter 44. ISR stack sizing must account for compiler-generated frames, hardware exception frames, local objects, nesting, and any RTOS/context-switch interaction.

## Definition
ISR stack usage is the additional stack consumption caused by interrupt entry and handler execution. ISO C does not define a stack or ISR frame; the target architecture and ABI do.

## Mechanism and language rules
At entry, hardware may push registers/status information. The compiler then creates a handler frame according to the interrupt calling convention. Calls from the ISR can add further frames. Nested interrupts multiply the active context.

### What to reason about
- Hardware-saved frame size.
- Compiler prologue/epilogue size.
- Maximum local-variable and callee stack use.
- Maximum call depth.
- Maximum nesting depth.
- Alignment requirements.

## Embedded implications
Stack overflow can corrupt task state, global data, heap metadata, or exception frames and may produce misleading downstream faults. A debugger's observed stack depth is not a worst-case bound.

### Firmware review angle
Use linker-defined stack bounds, guard regions, high-water marks, static stack analysis, and worst-case nesting assumptions. Repeat analysis after compiler or optimization changes.

## Edge cases and failure modes
- Large local arrays in an ISR.
- Deep library call chains hidden behind one helper.
- Floating-point context increasing exception frame cost.
- Nested high-priority interrupts exhausting stack.
- Debug build frames being larger than release frames or vice versa.

## Example pattern
```c
void SPI_IRQHandler(void)
{
    uint8_t sample[16];
    capture_spi(sample, sizeof sample);
    queue_from_isr(sample);
}
```
The array and all callees contribute to worst-case stack usage; copying it into another context may also require additional storage.

## Verification / debugging
Fill stack memory with a known pattern and measure high-water mark under maximum interrupt load. Combine this with static call-graph analysis and deliberate nesting stress.

## Staff-level takeaway
ISR stack usage is a **worst-case composition problem**, not an average measurement. Account for hardware frames, compiler frames, calls, nesting, and optimization when establishing a safety margin.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
