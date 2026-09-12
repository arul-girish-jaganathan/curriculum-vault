# Registers

> Canonical C topic note — chapter 41.

## Definition
CPU registers are processor-local storage used for operands, addresses, status, control state, and calling-convention values. ISO C does not expose a portable register model. Register names, preservation rules, exception state, and debugger access are target-specific.

## Mechanism and language rules
The ABI assigns roles to registers: argument/return registers, caller-saved registers, callee-saved registers, stack pointer, link/return state, and sometimes a frame pointer. The optimizer decides which C values occupy registers and can reuse them aggressively.

`register` in C is only a request related to address-taking and optimization latitude; it does not give portable control over a physical register. Modern compilers generally perform register allocation independently.

A debugger may show a source variable in a register, but the value can be stale, unavailable, or represented through a location expression. At an exception boundary, the CPU may automatically save a subset of registers while software saves additional context.

## Embedded implications
Register inspection is essential for hard faults, ABI bugs, context switches, interrupt entry, and low-level peripheral drivers. On an ARM Cortex-M-like system, a fault investigation commonly needs the stacked PC, LR, xPSR, SP, general registers, and fault-status registers.

Be careful with special registers: status/control registers can affect privilege, interrupt masking, memory access, or exception behavior. Writing them through a debugger is not equivalent to observing them and can destabilize the target.

### Example
```c
uint32_t add(uint32_t a, uint32_t b)
{
    return a + b;
}
```
The ABI may pass `a` and `b` in registers and return the result in another register. There may be no stack copy of either argument.

## Edge cases and failure modes
- Register values shown after a fault may represent exception entry state, not the last source statement.
- Caller-saved registers may be destroyed by a call by design.
- Optimized code may reuse one register for several unrelated source variables.
- Lazy floating-point context handling can make exception state architecture-specific.
- Inline assembly with incorrect clobbers can corrupt compiler assumptions.
- Register windows or banked registers on some architectures complicate interpretation.

## Verification / debugging
Record the exact architecture, ABI, compiler version, optimization flags, and image. When a value is suspicious, inspect both registers and the corresponding instruction. Disassemble around the PC and identify which register the instruction reads or writes. For a crash, preserve the complete exception context before executing recovery code.

For C/assembly interfaces, verify argument types, return types, register clobbers, stack alignment, and callee-saved register preservation against the ABI.

## Staff-level takeaway
Registers are where the abstract C machine meets the processor ABI. A senior engineer should be able to reconstruct a failing C operation from PC + instruction + register state, and recognize when a debugger's source variable view is only an approximation of the machine state.

## Related
[[00_Chapter_Index]]
[[04_Call_stacks]]
[[06_Memory_inspection]]
[[../36_C_Linkage_ABI/00_Chapter_Index]]
