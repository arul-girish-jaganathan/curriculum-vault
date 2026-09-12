# Volatile MMIO

> Canonical C topic note — Chapter 44. Memory-mapped I/O is a target-specific mechanism commonly expressed with `volatile` qualified accesses. `volatile` makes compiler-visible accesses observable; it does not by itself provide atomicity, inter-core synchronization, or device ordering.

## Definition
MMIO maps peripheral registers into an address space accessible by CPU instructions. A volatile-qualified lvalue tells the compiler that accesses cannot be optimized away or freely merged as ordinary memory operations.

## Mechanism and language rules
The C standard's `volatile` semantics are about evaluation and observable accesses, not the hardware protocol behind an address. Access width, side effects, ordering, barriers, and address validity come from the target.

### What to reason about
- Is the address a real register on this MCU revision?
- What access width is required?
- Is the register read-only, write-only, read-to-clear, write-one-to-clear, or command-like?
- Does hardware require a barrier after a write?
- Can an ISR or other core access the same register?
- Is the compiler allowed to use an access size different from the intended bus transaction?

## Embedded implications
A `volatile uint32_t` access may still be incorrect if the register requires 16-bit access or special sequencing. Read-modify-write can lose events on status registers, and a debugger read can have side effects.

### Firmware review angle
Centralize register definitions and document access semantics. Use device-provided atomic aliases and target-specific barrier primitives where required rather than treating `volatile` as a universal synchronization solution.

## Edge cases and failure modes
- Missing `volatile` allows required accesses to disappear or be merged.
- `volatile` is used to “fix” a data race.
- Wrong access width triggers a bus fault or corrupts adjacent state.
- Read-to-clear register is inspected unnecessarily.
- Device ordering requirements are omitted.

## Example pattern
```c
#define UART_STATUS (*(volatile uint32_t *)0x40000000u)

uint32_t uart_status(void)
{
    return UART_STATUS;
}
```
The address and width are illustrative only; production code must use the target's documented register map.

## Verification / debugging
Compare declarations with the reference manual, inspect generated assembly for access width, and use hardware traces when ordering matters. Test reset values, side effects, concurrent events, and low-power transitions.

Staff-level questions: What does `volatile` guarantee here, and what does it not? What barrier or atomic operation is additionally required? Can hardware change the register between CPU read and write?

## Staff-level takeaway
`volatile` is an **access-visibility qualifier, not a synchronization primitive**. MMIO correctness requires the complete hardware contract: address, width, side effects, ordering, atomicity, and ownership.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
