# Registers

> Canonical C topic note — chapter 41.

## Definition
CPU registers are small, fast architectural storage locations used for values, addresses, control state, arguments, return values, and execution state. C itself does not expose a portable register model; the `register` storage-class specifier does not grant reliable control over allocation. Debuggers expose registers because they are part of the target architecture and ABI.

## Mechanism and language rules
A debugging session should distinguish at least four register classes conceptually:

- general-purpose registers used for computation and addressing;
- special registers such as stack pointer and program counter;
- status/control registers containing flags or processor mode;
- ABI-defined argument, return-value, and callee/caller-saved registers.

The ABI determines how C values are mapped into registers during calls. A source variable may therefore appear in a register rather than memory.

### Compiler allocation
The optimizer performs register allocation based on liveness, interference, calling conventions, instruction constraints, and target cost models. A variable may move between registers and stack slots during its lifetime. Debug metadata can describe these location changes, but not every optimized state is recoverable in a simple form.

### Volatile and registers
`volatile` affects the language-level requirement for accesses to volatile-qualified objects; it does not mean a value must reside in a hardware register or prevent all unrelated optimization. MMIO debugging must use the target hardware model and the correct volatile object definitions.

## Embedded implications
Register inspection is often the fastest route from a fault to its hardware cause. For MCU faults, capture:

- PC/program counter;
- SP/stack pointer;
- LR or equivalent return state;
- general-purpose registers;
- processor status/flags;
- exception/fault status registers;
- control/security registers relevant to the fault;
- special peripheral registers implicated by the code.

Interpretation must account for exception-entry behavior. Some architectures automatically push a subset of registers before entering a fault handler; others use architecture-specific exception frames.

### Example
If the debugger shows:

```text
r0 = 0x00000000
r1 = 0x20001000
pc = <address in memcpy-like code>
```
that does not prove that the corresponding C parameter was a stable object with that exact value throughout the function. Validate the instruction at `pc`, ABI register convention, and debug location metadata.

## Edge cases and failure modes
- A source variable can move between registers and memory.
- Optimized variables may be reconstructed only from an expression, not a single register.
- Register contents may be overwritten by an exception prologue before the handler reads them.
- Debuggers can display architectural aliases differently from the manual.
- Lazy FPU context handling can make floating-point register state conditional.
- Security/privilege transitions can expose a different register view.
- Compiler-generated register use can make source-level stepping unintuitive.
- Looking at a register after returning from a fault handler can lose the original exception context.

## Verification / debugging
Always interpret a register together with the instruction that uses it:

1. Disassemble at the current PC.
2. Identify the instruction operands.
3. Check ABI meaning at call boundaries.
4. Inspect the stack/exception frame for the saved pre-fault state.
5. Compare the register value with the expected memory/object representation.
6. Check whether the instruction is part of compiler-generated prologue, epilogue, sanitizer code, or runtime support.

For post-mortem debugging, capture registers before any logging code can substantially modify them.

## Staff-level takeaway
Registers are the bridge between the C-level hypothesis and the actual machine state. Do not ask only “what is this variable?”; ask **which instruction produced this value, which ABI rule gave it this register, and whether the value is pre-fault or post-fault state?**

## Related
[[00_Chapter_Index]]
[[01_Source_level_debugging]]
[[04_Call_stacks]]
[[06_Memory_inspection]]
[[../36_C_Linkage_ABI/00_Chapter_Index]]
