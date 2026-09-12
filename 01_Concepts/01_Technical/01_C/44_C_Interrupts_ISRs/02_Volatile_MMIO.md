# Volatile MMIO

> Canonical C topic note — Chapter 44. Memory-mapped I/O exposes hardware registers through addresses interpreted by implementation-specific mechanisms. `volatile` prevents the compiler from treating accesses as ordinary removable/mergeable memory operations, but it does not guarantee atomicity or inter-device ordering.

## Definition
A typical register is declared through a `volatile` qualified type so every required access remains an observable operation to the implementation. Exact address mapping, register width, access permissions, side effects, and barriers are target-specific.

## Mechanism and language rules
`volatile` is a C qualifier. It tells the implementation that accesses to the object are observable and must follow the volatile access requirements. It does not mean “hardware register,” “atomic,” “thread-safe,” or “memory barrier.”

### What to reason about
- Is the register read/write-only or read/write?
- What access width does the hardware require?
- Are reads destructive?
- Are reserved bits required to be preserved or written as zero?
- Is ordering relative to other devices required?
- Is a compiler barrier or CPU/device memory barrier needed?

## Embedded implications
MMIO errors can cause lost interrupts, unintended commands, bus faults, or peripheral corruption. `reg |= mask` may perform a read-modify-write that is invalid for write-one-to-clear status registers.

### Firmware review angle
Keep register definitions centralized and use vendor-provided access abstractions when available. Separate compiler visibility (`volatile`) from CPU/bus ordering and synchronization requirements.

## Edge cases and failure modes
- Missing `volatile` allows required hardware observations to be optimized away.
- Excessive `volatile` prevents useful optimization and can increase timing.
- `volatile` does not make a multi-instruction register update atomic.
- Reading status registers can clear events.
- Wrong access width can trigger undefined hardware behavior even though the C expression is valid.

## Example pattern
```c
typedef struct {
    volatile uint32_t STATUS;
    volatile uint32_t CONTROL;
} uart_regs_t;

#define UART ((uart_regs_t *)0x40000000u)
```
The address and layout are illustrative and must come from the target memory map.

## Verification / debugging
Compare source declarations with the reference manual and inspect generated load/store width. Test reset values, side effects, reserved bits, and interrupt races. Add architecture-specific barriers only where the hardware programming model requires them.

## Staff-level takeaway
`volatile` is a **compiler-observability contract**, not a universal hardware synchronization primitive. Correct MMIO requires combining C qualification with target access width, register semantics, concurrency, and memory-ordering rules.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
