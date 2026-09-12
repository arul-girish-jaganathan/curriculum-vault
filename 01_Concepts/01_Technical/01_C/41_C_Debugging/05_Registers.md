# Registers

> Canonical C topic note — Chapter 41. CPU registers are machine-level state. C describes abstract values and operations; it does not expose a portable register model except through implementation extensions and objects such as volatile MMIO.

## Definition
Register inspection is the debugger's view of CPU registers such as general-purpose registers, stack pointer, program counter, status/control registers, and architecture-specific exception registers. Their names, widths, preservation rules, and meanings are defined by the target architecture and ABI, not ISO C.

## Mechanism and language rules
The compiler maps C values to registers, stack locations, constants, or optimized-away representations. A function parameter may begin in an argument register; a return value may occupy a designated return register; callee-saved registers must survive calls when required by the ABI. Register allocation changes with optimization, inlining, instruction scheduling, and register pressure.

### What to reason about
- Which instruction produced the value currently displayed?
- Is the register caller-saved and therefore overwritten by a call?
- Does the ABI assign a special meaning to the register?
- Is the displayed value stale or asynchronously modified?
- Are you inspecting CPU registers or peripheral registers mapped into memory?
- During a fault, is the register set the pre-exception context or the handler's context?

A debugger showing `r0 = 5` does not prove that a C variable currently has value 5 unless the debug location information and instruction point establish that relationship.

## Embedded implications
Registers are often the fastest route to diagnosing faults. On ARM Cortex-M, for example, the PC, LR, SP, xPSR, fault status registers, and stacked exception context can identify the failing instruction and exception path. Other architectures have different conventions.

Control/status registers can be privileged, banked, side-effecting, or write-sensitive. Reading or writing them through a debugger can alter system state. Peripheral registers should be treated separately from CPU registers and interpreted using the device reference manual.

### Firmware review angle
Record the architecture, core revision, ABI, compiler version, and exact instruction address. Do not copy a register-debugging recipe from one MCU family to another without verifying exception and ABI details.

## Edge cases and failure modes
- **Wrong context:** examining handler registers instead of the interrupted code's stacked context.
- **Register reuse:** optimized code reuses a register for a different source variable.
- **Lazy state saving:** floating-point or extended context may be saved conditionally.
- **Special registers:** status/control registers can have privileged or side-effecting access.
- **Debug read changes behavior:** some target registers are destructive-on-read.

## Example pattern
```c
static uint32_t add(uint32_t a, uint32_t b)
{
    return a + b;
}
```
At a call boundary, the ABI may place `a` and `b` in registers and the result in a return register. The exact registers are architecture-specific. At higher optimization, the entire function may collapse into a single instruction or be inlined.

## Verification / debugging
Disassemble around the PC and correlate each instruction with the ABI. For a fault, first preserve the raw register frame before attempting recovery. Decode status bits using the target vendor's documentation. Use debugger register views for observation, not as a substitute for architectural knowledge.

Staff-level questions:
- Which registers are architecturally defined and which are ABI conventions?
- Which state belongs to the faulting context?
- What evidence ties a register to a C value?
- Could an MMIO read or debugger action change the state?

## Staff-level takeaway
Register debugging becomes reliable when you reason **instruction-by-instruction through the ABI and exception model**. Source symbols are a convenience layer; raw register state plus disassembly is the authoritative evidence for machine-level failures.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
