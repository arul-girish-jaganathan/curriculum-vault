# 11: Freestanding Limitations

## Definition
Freestanding limitations refer to the constraints imposed on multithreading in freestanding C implementations. Under ISO C11/C17/C23, a C execution environment is classified as either **hosted** (operating system present with full standard library) or **freestanding** (bare-metal, firmware, bootloaders, kernel space). In freestanding environments, multithreading support (`<threads.h>`) is almost universally absent.

## Scope and Boundaries
- **Covers:** ISO C freestanding vs. hosted definitions, `__STDC_HOSTED__`, `__STDC_NO_THREADS__`, bare-metal concurrency, and RTOS boundaries.
- **Does not cover:** Hosted POSIX systems, dynamic memory allocators in hosted OSes, or userspace thread scheduling.

## Why Does It Exist
The ISO C standard recognizes that many C programs run on bare metal without an operating system:
- **No Underlying OS Scheduler:** Threads require an execution scheduler, stack allocators, timer interrupts, and context-switching logic—features that do not exist on a bare MCU without an RTOS.
- **Standard Library Pruning:** ISO C mandates that freestanding implementations are only required to supply a minimal subset of headers (`<float.h>`, `<iso646.h>`, `<limits.h>`, `<stdalign.h>`, `<stdarg.h>`, `<stdbool.h>`, `<stddef.h>`, `<stdint.h>`, `<stdnoreturn.h>`, and parts of `<stdatomic.h>`). `<threads.h>` is **not** part of freestanding C.

## Mechanism and Language Rules
- **Hosted Conformance Macro:**
  - `__STDC_HOSTED__ == 1`: Hosted implementation (full standard library expected).
  - `__STDC_HOSTED__ == 0`: Freestanding implementation (bare-metal, no OS runtime guaranteed).
- **Mandatory Threads Macro:** In freestanding implementations, `__STDC_NO_THREADS__` is universally defined to `1`.
- **Atomics in Freestanding:** While `<threads.h>` is omitted, lock-free atomics from `<stdatomic.h>` *may* be supported in freestanding environments if the target architecture provides hardware atomic instructions (e.g., `LDREX`/`STREX` on ARMv7-M/v8-M, or `lr.w`/`sc.w` on RISC-V).
- **Memory Footprint Realities:** A full C11 thread implementation requires a thread control block, per-thread stack allocation, and reentrant runtime data structures—resources that can easily exceed total available SRAM on constrained MCUs (e.g., Cortex-M0+ with 8 KB RAM).

## Examples
```c
/* Bare-Metal / Embedded Concurrency Strategy */
#include <stdint.h>
#include <stdbool.h>

#if defined(__STDC_HOSTED__) && __STDC_HOSTED__ == 1
    #error "This firmware module is intended strictly for Freestanding environments!"
#endif

#if defined(__STDC_NO_THREADS__) || !defined(__STDC_HOSTED__)
/* In freestanding, we achieve concurrency via hardware interrupts + atomic rings,
   not preemptive C11 threads */
#include <stdatomic.h>

#define RING_SIZE 64

typedef struct {
    uint8_t buffer[RING_SIZE];
    atomic_size_t head;
    atomic_size_t tail;
} lockfree_spsc_queue_t;

static lockfree_spsc_queue_t uart_rx_queue;

void uart_isr_handler(void) 
{
    /* ISR acting as concurrent producer */
    uint8_t rx_byte = *((volatile uint8_t *)0x4000C000); /* UART Data Reg */
    size_t current_tail = atomic_load_explicit(&uart_rx_queue.tail, memory_order_relaxed);
    size_t next_tail = (current_tail + 1) % RING_SIZE;

    if (next_tail != atomic_load_explicit(&uart_rx_queue.head, memory_order_acquire)) {
        uart_rx_queue.buffer[current_tail] = rx_byte;
        atomic_store_explicit(&uart_rx_queue.tail, next_tail, memory_order_release);
    }
}

bool read_rx_byte(uint8_t *byte) 
{
    /* Main loop acting as consumer */
    size_t current_head = atomic_load_explicit(&uart_rx_queue.head, memory_order_relaxed);
    if (current_head == atomic_load_explicit(&uart_rx_queue.tail, memory_order_acquire)) {
        return false; /* Queue empty */
    }
    *byte = uart_rx_queue.buffer[current_head];
    atomic_store_explicit(&uart_rx_queue.head, (current_head + 1) % RING_SIZE, memory_order_release);
    return true;
}
#endif
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined References:** Attempting to `#include <threads.h>` in a freestanding environment results in a fatal preprocessor error (header not found) or unresolved linker symbols (`thrd_create`, `mtx_lock`).
- **Atomic Emulation Traps:** If `<stdatomic.h>` is used on a freestanding MCU lacking hardware atomic instructions, the compiler may emit calls to runtime helper functions (e.g., `__atomic_fetch_add_4`). If the BSP does not provide these symbols, the link step fails.

## Edge Cases and Failure Modes
- **Hidden Dynamic Allocation:** Naively porting a C11 threads wrapper to an RTOS on an MCU with no heap memory pool results in silent `thrd_nomem` failures.
- **Interrupt Preemption Hazards:** Developers used to mutexes often assume `mtx_lock` can protect variables shared with ISRs. In freestanding environments, mutexes cannot be used in ISRs; interrupt masking (`__disable_irq()`) or lock-free atomics must be used.

## Embedded Implications
- **Cooperative State Machines:** Freestanding embedded systems achieve concurrency without threads via event-driven finite state machines (FSMs), Super-Loops, or cooperative coroutines (Protothreads).
- **Static Stack Sizing:** In RTOS-based freestanding environments, each task's stack must be statically allocated and bound to the RTOS task handle at compile time to avoid heap fragmentation.

## Firmware Review Angle
- **Reject `<threads.h>` in Bare-Metal:** Flag any inclusion of `<threads.h>` in bare-metal BSP or driver code.
- **Verify ISR Concurrency Boundaries:** Ensure communication between interrupt handlers and foreground loops utilizes lock-free single-producer single-consumer queues or critical section interrupt disables.
- **Audit Lock-Free Support:** Use `ATOMIC_INT_LOCK_FREE` and `atomic_is_lock_free()` to verify that atomic types do not generate hidden software locks.

## Compiler, ABI, and Toolchain Implications
- **Toolchain Options:** Compiling with `-ffreestanding` informs GCC/Clang that hosted standard library facilities are unavailable.
- **Runtime Libs:** Embedded toolchains (ARM GNU Toolchain, LLVM embedded) package `newlib` or `picolibc`, which stub out or omit threading primitives unless explicitly configured with RTOS hooks.

## Performance, Memory, Timing, and Power
- **Zero Thread Overhead:** Bare-metal super-loops incur zero context-switch overhead, zero TCB memory overhead, and zero thread-local storage overhead.
- **Ultra-Low Latency:** Interrupt-driven concurrency provides deterministic sub-microsecond response times, unlike preemptive thread schedulers which introduce jitter.

## Verification / Debugging
- **Hardware Debuggers:** Use JTAG/SWD probes (J-Link, ST-Link) to inspect bare-metal call stacks and peripheral registers directly.
- **Linker Map Files:** Inspect the `.map` output file to ensure that no multithreading runtime libraries or unexpected heap blocks were pulled in by the linker.

## Safety, Security, and Reliability
- **Determinism:** Freestanding event loops and static RTOS architectures are vastly easier to certify under safety standards (DO-178C DAL-A, ISO 26262 ASIL-D) than dynamic C11 thread spawning.
- **Stack Guarantees:** Static allocation enables formal worst-case execution time (WCET) and stack usage analysis via tools like AbsInt or static call-graph analyzers.

## Trade-offs and Alternatives
- **C11 Threads vs. Bare-Metal Super-Loop:**
  - *C11 Threads:* Preemptive, structured, high-level; high memory footprint, non-deterministic latency, unavailable on bare-metal.
  - *Super-Loop / Interrupts:* Zero overhead, fully deterministic, minimal RAM; manual state management, complex multi-stage workflows.
- **RTOS Tasks:** Zephyr, FreeRTOS, and embOS provide deterministic priority-based scheduling specifically engineered for freestanding MCU constraints.

## Staff-Level Takeaway
`<threads.h>` belongs to the hosted world. In freestanding firmware, true concurrency is driven by hardware interrupts, DMA channels, and CPU event loops. Do not fight the freestanding environment by attempting to shoehorn heavy hosted threading abstractions into bare metal; build on hardware-supported atomics and deterministic state machines.

## Related Concepts
- [[00_Chapter_Index]]
- [[07_Thread_local_storage]]
- [[10_C11_thread_portability]]
- [[12_Thread_safe_module_design]]
