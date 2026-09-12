# Call stacks

> Canonical C topic note — Chapter 41. A call stack is a runtime/ABI mechanism used to represent active calls; the familiar debugger call-stack view is reconstructed from machine state and unwind/debug metadata.

## Definition
A call stack records enough execution state for active function calls to return and preserve required local state. ISO C specifies function-call semantics but does not require a stack, frame pointer, debugger, or particular ABI. Most embedded ABIs implement calls using a stack plus registers, but optimized code may omit traditional stack frames.

## Mechanism and language rules
A typical call sequence saves a return address, establishes any required frame state, preserves callee-saved registers, allocates local storage, and passes arguments according to the ABI. A return reverses the required parts. The exact sequence is target-specific.

A debugger reconstructs frames using frame pointers, unwind tables, prologue analysis, debug metadata, and architecture rules. Tail-call optimization can eliminate a frame. Inlining can eliminate a call boundary entirely. Interrupt entry may add hardware-created exception frames that are not ordinary C call frames.

### What to reason about
- Which registers are caller- vs callee-saved?
- Where are return address and arguments stored?
- Is a frame pointer present?
- Are stack alignment rules satisfied?
- Did stack corruption destroy the unwind chain?
- Are you looking at a task stack, ISR stack, exception stack, or startup stack?

## Embedded implications
Stack depth directly affects RAM sizing. Nested interrupts, RTOS tasks, library calls, recursion, large locals, and compiler-generated temporaries can all consume stack. A stack overflow may corrupt adjacent state before any obvious fault occurs.

Fault handlers often run with a hardware exception frame plus software-saved registers. Correct post-mortem analysis therefore requires knowledge of the MCU exception model and ABI, not just the C source.

### Firmware review angle
Measure worst-case stack depth for each task and interrupt nesting configuration. Do not size from the deepest observed debugger call stack alone. Debug builds can have larger frames and different inlining than production.

## Edge cases and failure modes
- **Corrupt backtrace:** stack overwrite, invalid frame pointer, missing unwind data, or exception-frame confusion.
- **Missing function:** inlining or tail-call optimization removed the expected frame.
- **Impossible locals:** optimized variables may not have stable stack locations.
- **Stack/heap collision:** a growing stack can overwrite dynamically allocated memory.
- **ISR nesting:** an apparently shallow C call chain can sit on top of several nested hardware frames.

## Example pattern
```c
static void leaf(uint32_t x)
{
    volatile uint32_t scratch = x;
    (void)scratch;
}

static void worker(uint32_t x)
{
    leaf(x + 1U);
}

void service(void)
{
    worker(10U);
}
```
The visible frame sequence depends on optimization. `leaf()` may be inlined, and `scratch` may be eliminated unless its volatile access makes it observable.

## Verification / debugging
Capture the program counter, stack pointer, link/return register, fault status, and relevant exception-frame registers during a fault. Validate the stack range and sentinel/high-water mark. Compare debugger unwinding with raw memory and disassembly when the backtrace is suspicious.

Staff-level questions:
- What is the ABI-defined call/return convention?
- What is the measured and statically bounded worst-case stack use?
- Could an interrupt or RTOS context switch change the stack being inspected?
- Is the unwind trustworthy, or merely plausible?

## Staff-level takeaway
A call stack is an **ABI/runtime structure**, while a debugger backtrace is an interpretation of that structure. For embedded reliability, reason from raw stack/register state and ABI rules, then use the symbolic backtrace as a convenient reconstruction.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
