# Call stacks

> Canonical C topic note — chapter 41.

## Definition
A call stack is the runtime chain of active function invocations, represented by stack frames containing some combination of saved registers, return addresses, arguments, local storage, and unwind metadata. C defines function calls and automatic objects, but the exact stack layout and calling convention are implementation/ABI properties.

## Mechanism and language rules
A normal call transfers control to a callee and establishes an activation record according to the target ABI. The compiler may use a frame pointer or omit it, keep values in registers, reuse stack slots, inline calls, perform tail calls, or eliminate frames entirely.

A debugger reconstructs the call chain from:
1. the current PC and stack/register state;
2. ABI conventions;
3. frame/unwind metadata;
4. debug symbols.

A correct-looking source call stack is therefore evidence produced by several layers, not a direct C-language guarantee.

## Embedded implications
Stack analysis is central to MCU reliability. Calculate worst-case stack consumption across nested calls, interrupt preemption, RTOS tasks, fault handlers, and library code. Include compiler-generated spills, alignment padding, interrupt stacking, floating-point context, and alternate exception stacks where applicable.

A stack overflow may overwrite another task's stack, global data, saved context, or control-flow state before becoming visible. Guard patterns and MPU stack regions can turn silent corruption into an actionable fault.

### Example
```c
static void service(void)
{
    uint8_t scratch[128];
    /* ... */
}

static void task(void)
{
    service();
}
```
The source declares 128 bytes, but the actual frame can be larger due to alignment, saved registers, compiler spills, and ABI requirements.

## Edge cases and failure modes
- Frame-pointer omission makes naive stack walking unreliable.
- Tail-call optimization removes an expected caller frame.
- Inlining creates logical frames without physical calls.
- Corrupted stack memory produces a bogus backtrace.
- An exception frame is not necessarily an ordinary C frame.
- Mixed C/assembly code can violate debugger unwind assumptions.
- A stack trace from the wrong binary is meaningless.

## Verification / debugging
For a crash, capture PC, SP, LR/return state, status registers, and the relevant exception frame before attempting recovery. Validate that SP lies inside an expected stack region and that return addresses point into executable memory. Compare the trace against the linker map and disassembly.

For capacity, measure high-water marks using a known fill pattern or hardware stack monitoring. Combine static call-graph analysis with worst-case interrupt nesting rather than relying on average runtime usage.

## Staff-level takeaway
A stack trace is a hypothesis about control flow. Trust it only after validating the binary, ABI, stack pointer, unwind metadata, and memory integrity. For embedded architecture, stack budget is a resource contract spanning C code, compiler behavior, interrupts, RTOS context switching, and fault handling.

## Related
[[00_Chapter_Index]]
[[05_Registers]]
[[06_Memory_inspection]]
[[08_Core_dumps]]
