# Call stacks

> Canonical C topic note — Chapter 41. A call stack is a runtime representation of active call frames, but its exact layout is defined by the ABI, compiler, architecture, and runtime—not by ISO C.

## Definition
A call stack records information needed to execute nested calls, commonly including return addresses, saved registers, parameters, local storage, and alignment padding. A debugger reconstructs a call chain using stack memory, registers, symbols, and unwind information.

The C concept of function calls must be separated from a particular frame layout. Optimizing compilers may omit frame pointers, inline calls, use tail calls, reuse stack slots, or keep values in registers.

## Mechanism and language rules
At a call, the ABI determines how arguments and return values are passed and which registers/callee-saved state must be preserved. The callee may allocate a frame and save required state. On return, the caller resumes at the saved return location.

### What to reason about
- What does the target ABI define for SP, return address, arguments, and callee-saved registers?
- Is a frame pointer present?
- Has the compiler performed inlining or tail-call optimization?
- Is stack alignment maintained at every call boundary?
- Could stack corruption make unwinding unreliable?
- Are interrupt/exception frames interleaved with ordinary C frames?

A debugger backtrace is an inference. Its quality depends on valid stack state and usable unwind/debug metadata.

## Embedded implications
MCUs often have small stacks, and an interrupt can consume additional stack on top of a task's frame. Nested exceptions can create hardware-defined exception frames. RTOS context switches replace the active task stack and may require RTOS-aware unwinding.

Stack overflow can corrupt return addresses, saved registers, adjacent task stacks, or global data. Watermarks, guard regions, MPU protection, and high-water measurements are useful defenses.

### Firmware review angle
Treat worst-case call depth, ISR nesting, compiler-generated spills, library calls, and fault-handler paths as part of the stack budget. Do not estimate stack usage from source nesting alone.

## Edge cases and failure modes
- **Corrupt backtrace:** stack or return-address corruption.
- **Missing frame:** inlining or tail-call optimization.
- **Impossible locals:** optimized stack-slot reuse or register allocation.
- **Fault handler confusion:** hardware exception frame interpreted as a normal C frame.
- **RTOS context mismatch:** debugger assumes the wrong active task.

## Example pattern
```c
static int leaf(int x) { return x + 1; }
static int middle(int x) { return leaf(x) * 2; }
static int top(int x) { return middle(x) + 3; }
```
At low optimization, three source-level frames may appear. At higher optimization, one or more calls can be inlined, changing the physical stack while preserving the C result.

## Verification / debugging
Capture SP, PC, link/return register, status register, and the raw stack before relying on a symbolic backtrace. Compare the observed frame shape with the target ABI and exception-entry rules. Use compiler-generated stack-usage reports where available.

For suspected stack overflow, fill unused stack with a pattern and inspect the high-water mark after worst-case nested execution. Combine this with MPU/guard checks where supported.

Staff-level questions: What is the worst-case frame depth? What happens when an interrupt arrives at maximum depth? Can the fault handler itself run safely on the remaining stack?

## Staff-level takeaway
A call stack is an **ABI-level data structure**, not merely a list of C functions. Debug it from raw machine state upward, and budget stack from generated code plus asynchronous execution, not source appearance alone.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
