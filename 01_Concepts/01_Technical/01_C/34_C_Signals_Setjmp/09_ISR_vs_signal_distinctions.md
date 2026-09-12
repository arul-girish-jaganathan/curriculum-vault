# ISR vs signal distinctions

> Canonical C topic note — chapter 34.

## Definition
An **ISR (interrupt service routine)** is a processor/interrupt-controller entry path used by embedded hardware. A **C signal handler** is a hosted-runtime mechanism defined by `<signal.h>`. Both are asynchronous relative to ordinary application code, but they have fundamentally different contracts.

Understanding this distinction prevents one of the most common embedded-C mistakes: importing assumptions about POSIX/ISO signals into hardware interrupt code.

## Mechanism and language rules
An ISR is normally entered through hardware exception/interrupt machinery. The CPU saves architecture-specific state, selects a vector, changes execution mode as required, and runs an interrupt entry routine. The compiler's C function is only one layer of that mechanism.

A signal handler is entered by the C runtime/operating system according to the implementation's signal model. It has no ISO C guarantee that it corresponds to a hardware interrupt, executes at a particular priority, or runs on a special stack.

### What to reason about
| Property | C signal handler | Hardware ISR |
|---|---|---|
| Defined by | C/OS runtime | CPU + interrupt controller + firmware |
| Entry | runtime-managed | hardware exception path |
| Priority | implementation/OS | hardware/RTOS |
| Stack | runtime-dependent | architecture/RTOS-dependent |
| MMIO | not inherently implied | central use case |
| Masking | signal semantics | interrupt masking/priority |
| Safe API set | signal-specific | ISR/RTOS-specific |
| Portability | hosted implementations | MCU/architecture-specific |

Neither context should call arbitrary application code merely because the C syntax looks like a normal function.

## Embedded implications
For embedded firmware, define explicit execution-context contracts such as:

```text
THREAD_SAFE      callable from normal task context
ISR_SAFE         bounded and legal from interrupt context
FAULT_SAFE       usable after severe CPU/system fault
BOOT_SAFE        usable before full runtime initialization
```

An ISR often must acknowledge hardware quickly, capture data, and defer work to a task. The same high-level architecture as signal handling applies, but the implementation mechanisms differ.

### Firmware review angle
For every ISR review:
- identify interrupt source and priority;
- determine which registers/flags must be acknowledged;
- calculate worst-case latency;
- identify shared state and required synchronization;
- verify nesting and preemption behavior;
- determine whether RTOS APIs are legal in ISR context;
- account for cache, DMA, memory barriers, and peripheral ordering.

## Edge cases and failure modes
Do not assume:
- `volatile` makes ISR communication safe;
- every ISR may block;
- an ISR can call a mutex API;
- a signal handler and ISR can share the same implementation wrapper;
- signal masking is equivalent to disabling CPU interrupts;
- a compiler attribute such as `interrupt` is portable ISO C.

A classic bug is using a driver routine that is task-safe but not ISR-safe. The routine may acquire a lock or wait for hardware, producing deadlock or excessive interrupt latency.

## Example pattern
```c
/* Pseudocode illustrating the architecture, not an ISO C ISR declaration. */
volatile unsigned event_pending;

void peripheral_isr(void)
{
    /* 1. Read/acknowledge hardware. */
    /* 2. Capture minimal state. */
    event_pending = 1;
    /* 3. Defer processing to a task/main loop. */
}
```

## Verification / debugging
Measure ISR entry latency, execution time, nesting depth, and maximum stack use on hardware. Use GPIO timestamping, cycle counters, trace units, or RTOS instrumentation where available.

Staff-level questions:
- Which guarantees come from C and which come from the MCU/RTOS?
- Is the handler bounded under worst-case interrupt load?
- Can it interrupt a critical section that owns resources it touches?
- What is the deferred-work mechanism?

## Staff-level takeaway
Signals and ISRs share the **asynchronous execution problem**, not the same specification. Treat ISR design as a hardware/ABI/RTOS contract layered underneath C, and never infer ISR behavior from ISO signal semantics.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
