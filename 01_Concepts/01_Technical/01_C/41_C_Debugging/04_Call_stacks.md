# Call stacks

> Canonical C topic note — chapter 41.

## Definition
A call stack is the runtime structure used to preserve function-call state, typically including return information, saved registers, local storage, and temporary state. The exact layout is defined by the ABI and compiler, not by ISO C.

For debugging, a call stack is a reconstruction of active call frames from machine state. A backtrace is therefore only as reliable as the available stack/frame metadata and the integrity of the stack itself.

## Mechanism and language rules
A normal call conceptually creates a relationship like:

`caller → argument passing → callee entry → local frame → return state → caller continuation`

The ABI determines where arguments and return values travel, which registers are caller/callee-saved, how the stack is aligned, and how the return address is represented.

A compiler may use:

- a frame pointer;
- a stack pointer plus offsets;
- frame-pointer omission;
- shrink-wrapped prologues/epilogues;
- tail calls;
- inlining;
- leaf-function optimizations;
- register-only locals.

Therefore “one C function = one visible stack frame” is not a language guarantee.

### Unwinding
Debuggers commonly unwind using frame-pointer chains, DWARF call-frame information, architecture-specific unwind rules, or heuristics. If stack memory is corrupted or the unwinder lacks metadata, a backtrace may stop early or display plausible-looking but false callers.

### Recursion
Recursive C functions create multiple active invocations of the same function. Each invocation has distinct automatic object instances and call state, subject to the usual lifetime and storage rules.

## Embedded implications
Stack analysis is central to MCU reliability because stack memory is finite and often shared with startup/runtime mechanisms. Inspect:

- main/task stack sizes;
- interrupt stack or exception stacking;
- nested interrupt depth;
- compiler-generated call depth;
- RTOS context-switch frames;
- guard regions/canaries;
- bootloader/application stack ownership.

A hard fault may corrupt the very stack required to diagnose it. Capture fault registers and the raw exception frame as early as possible.

### Example
```c
static int parse_level(int x)
{
    if (x <= 0)
        return 0;
    return 1 + parse_level(x - 1);
}
```
The C semantics permit recursion, but target stack consumption depends on ABI frame size, optimization, register allocation, and whether tail-call optimization is applicable.

## Edge cases and failure modes
- Stack overflow corrupts return state and local variables.
- A smashed frame pointer can make a backtrace invalid.
- Tail-call optimization removes an expected frame.
- Inlining removes a physical call while retaining an inline logical frame.
- Interrupt entry can add hardware-created exception state not visible as an ordinary C frame.
- Fault handlers may run with a different stack or privilege level.
- Mixed C/assembly or ABI mismatches can break unwinding.
- LTO can materially change frame structure.

## Verification / debugging
When a backtrace looks suspicious:

1. Record the current PC, SP, LR/return-state register, and architecture fault status.
2. Inspect raw stack bytes around SP.
3. Validate stack bounds and alignment.
4. Compare the reported frame addresses against the linker map.
5. Disassemble the suspected function prologue/epilogue.
6. Check whether frame pointers were omitted and whether unwind metadata exists.
7. Consider stack corruption before trusting a long call chain.

For field failures, save enough registers and stack memory to reconstruct the exception context after reboot.

## Staff-level takeaway
A backtrace is evidence, not truth. Treat it as a hypothesis generated from **ABI + stack bytes + unwind metadata + register state**. When the stack is corrupted, switch from symbolic debugging to raw-state reconstruction and establish the first trustworthy frame before reasoning upward.

## Related
[[00_Chapter_Index]]
[[05_Registers]]
[[06_Memory_inspection]]
[[08_Core_dumps]]
[[../36_C_Linkage_ABI/00_Chapter_Index]]
[[../68_C_Recursion_Stack/00_Chapter_Index]]
