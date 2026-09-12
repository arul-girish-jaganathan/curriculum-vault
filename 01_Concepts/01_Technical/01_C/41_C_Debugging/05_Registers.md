# Registers

> Canonical C topic note — Chapter 41. CPU registers are architectural state used for computation, control flow, addressing, and ABI conventions. ISO C does not define a register file; compiler and target architecture determine the mapping from C values to registers.

## Definition
A register is a small, fast storage location inside the CPU. Important debugging registers include the program counter (PC), stack pointer (SP), status/flags register, return-address/link register, general-purpose registers, and sometimes control registers describing fault or privilege state.

A C variable can be represented by a register value rather than RAM. Conversely, a source variable may be spilled between registers and memory during its lifetime.

## Mechanism and language rules
The compiler's register allocator assigns live values to architectural registers while obeying the ABI and instruction constraints. Caller-saved registers may be destroyed by calls; callee-saved registers must be preserved according to the ABI. Debug information can describe register-based variable locations.

### What to reason about
- Which ABI registers carry arguments and return values?
- Which registers are caller- or callee-saved?
- Is the displayed register value from the exact stopped instruction?
- Are flags valid for the instruction sequence being inspected?
- Is the CPU in thread, handler, privileged, or another execution mode?
- Could an exception entry have changed SP or saved machine state?

The instruction pointer must be interpreted with the architecture's instruction width/alignment rules. A fault PC may point to the faulting instruction or, on some architectures/exceptions, require architecture-specific interpretation.

## Embedded implications
Registers expose hardware state that often cannot be inferred from C alone: fault status, interrupt masks, privilege state, MPU configuration, cache controls, peripheral buses, and exception return state. Reading them after a fault can reveal whether a failure was caused by invalid access, alignment, execution protection, or a peripheral event.

### Firmware review angle
Document the target architecture and ABI in fault-analysis procedures. Do not copy register interpretations between MCU families merely because names such as `PC` or `SP` are common.

## Edge cases and failure modes
- **Wrong context:** inspecting the interrupted context instead of the exception-saved context.
- **Register reuse:** assuming a source variable remains in the same register throughout a function.
- **Special register constraints:** some registers have side effects or privileged access requirements.
- **Instruction-address confusion:** compressed/fixed-width instruction sets and exception PC semantics differ.

## Example pattern
```c
uint32_t add_and_publish(uint32_t a, uint32_t b)
{
    uint32_t result = a + b;
    publish(result);
    return result;
}
```
At a call boundary, `a`, `b`, and the return value may occupy ABI-defined registers. A debugger showing a register is therefore often more meaningful than looking for a corresponding stack slot.

## Verification / debugging
At a fault, capture PC, SP, status, link/return state, general registers, and architecture-specific fault-status registers before attempting recovery. Preserve the raw numeric values so later tooling can reinterpret them.

Map the PC to the exact binary, disassemble around it, and identify which registers feed the faulting instruction's address/data operands. Validate register meanings against the processor reference manual and ABI documentation.

Staff-level questions: Which state is hardware-saved automatically? Which state must the handler save? Can the diagnostic code itself corrupt the evidence?

## Staff-level takeaway
Registers are the bridge between **C-level intent and actual CPU state**. Expert debugging starts from architectural state, then reconstructs ABI, instruction, memory, and source-level meaning without assuming every source variable has a stable RAM representation.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
