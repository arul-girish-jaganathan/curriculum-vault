# Volatile barriers

> Canonical C topic note — chapter 37.

## Definition
`volatile` tells the implementation that accesses to the qualified object are observable and must follow the language's volatile-access rules. It is commonly used for MMIO and objects affected by mechanisms outside ordinary C execution. It is **not** a general compiler barrier, CPU memory barrier, atomicity primitive, or inter-thread synchronization mechanism.

## Mechanism and language rules
```c
volatile uint32_t *status = (volatile uint32_t *)REG_STATUS;
uint32_t s = *status;
```

The compiler must preserve the required volatile accesses; it may still optimize ordinary computations around them within the language rules. A compiler-specific barrier such as an empty inline assembly memory clobber has a different scope, and a hardware barrier such as ARM `dmb`/`dsb` addresses processor ordering rather than merely compiler reordering.

C atomics provide language-level synchronization and atomicity properties that volatile does not provide.

## Embedded implications
For MMIO, use the vendor's prescribed volatile-qualified register definitions and hardware ordering primitives where required. For device protocols, distinguish: (1) compiler visibility, (2) CPU memory ordering, (3) bus/device ordering, and (4) data atomicity. A design may need all four.

A volatile access can have timing and power cost because each access is emitted and may reach a peripheral bus. Repeated polling should therefore have explicit timeout and latency policies.

## Edge cases and failure modes
- `volatile` shared variable used as a thread synchronization flag.
- Assuming a volatile 32-bit access is atomic on every target.
- Assuming volatile creates a CPU memory barrier.
- Applying volatile to a pointer rather than the intended object qualification.
- Using volatile to hide a data race or aliasing defect.

## Verification / debugging
Inspect assembly around MMIO and synchronization points. Read the MCU reference manual for required barrier sequences and access widths. For concurrent code, use C atomics or the RTOS synchronization primitive and test on the target.

## Staff-level takeaway
When reviewing volatile code, ask which boundary it addresses: compiler, CPU, bus, peripheral, or concurrency. If the answer is unclear, `volatile` is probably being asked to solve the wrong problem.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
