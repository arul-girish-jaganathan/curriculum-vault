# Volatile barriers

## Definition
`volatile` tells the C implementation that accesses to a volatile-qualified object are observable according to the language rules and must not be optimized away or freely treated like accesses to ordinary memory. It is commonly required for memory-mapped registers and certain hardware-visible state. **It is not a general compiler barrier, CPU memory barrier, atomicity guarantee, or thread-synchronization primitive.**

## Scope and boundaries
A volatile access is a C-level side effect. It does not automatically order unrelated non-volatile operations, make multi-byte accesses atomic, establish inter-core visibility, or flush CPU/store buffers. Those properties require atomics and/or target-specific memory-ordering instructions as appropriate.

## Mechanism and language rules
Example:

```c
#define UART_STATUS (*(volatile uint32_t *)0x40000000u)

while ((UART_STATUS & 1u) == 0u) {
    /* wait */
}
```

The compiler must perform the required volatile reads rather than caching `UART_STATUS` as an ordinary variable.

### Volatile and access frequency
The abstract C rules constrain observable volatile accesses, but they do not turn every source expression into a one-instruction hardware transaction. A volatile access can still be wider/narrower or otherwise target-dependent according to the implementation and ABI. Hardware register access width must therefore match the MCU specification.

### Volatile versus atomics
For communication between C threads, use `_Atomic` objects and appropriate memory orders. For an ISR/main-loop relationship, `volatile` may be necessary for hardware-visible state, but atomicity and ordering still need separate analysis.

## Embedded implications
Volatile is fundamental for MMIO, status registers, interrupt flags, DMA-updated memory where the C abstract-machine contract is explicitly used for such access, and certain low-level control interfaces. It should not be sprinkled over entire driver structures without understanding the hardware and concurrency contract.

A compiler barrier such as an implementation-specific empty inline assembly with a `"memory"` clobber has a different purpose: it constrains compiler reordering across the barrier. A CPU memory barrier constrains the hardware memory system. These are three distinct concepts.

## Edge cases and failure modes
- Assuming `volatile` makes `counter++` atomic.
- Assuming volatile orders writes to normal RAM relative to a peripheral.
- Assuming volatile solves cache coherency.
- Using volatile instead of `_Atomic` for shared threads.
- Accessing a hardware register with the wrong width.
- Using `volatile` to mask a data-race bug rather than defining ownership and synchronization.

## Verification / debugging
Inspect generated assembly to confirm required accesses occur. Check compiler documentation for the exact volatile guarantees. For concurrent code, use ThreadSanitizer on host builds where applicable and review the C memory model. For hardware ordering, consult the processor reference manual and inspect barrier instructions in disassembly.

## Performance, memory, timing and power
Volatile accesses inhibit useful optimization: loads may be repeated and stores cannot simply be discarded. Excessive volatile use can increase bus traffic, execution time, and power. Conversely, missing volatile can remove a required hardware interaction entirely.

## Staff-level takeaway
Use the **weakest mechanism that exactly expresses the requirement**: volatile for required volatile accesses, atomics for C concurrency, compiler barriers for compiler-ordering requirements, and CPU/device barriers for hardware ordering. Calling all of these “a volatile barrier” hides the most important engineering distinction.