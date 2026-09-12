# 03: thrd_detach

## Definition
`thrd_detach` is the C11 thread management function that disassociates the target thread from the caller and marks its storage for automatic reclamation upon termination. Once a thread is detached, another thread cannot synchronize with its completion via `thrd_join`, nor can its exit return code be obtained.

## Scope and Boundaries
- **Covers:** Asynchronous thread execution, background daemon threads, automatic stack/TCB resource reclamation, and detached state transitions.
- **Does not cover:** Synchronous joining ([[02_thrd_join]]), thread cancellation ([[09_Thread_cancellation_boundaries]]), or thread creation ([[01_thrd_create]]).

## Why Does It Exist
Not all concurrent workloads follow the structured fork-join model:
- **Fire-and-Forget Operations:** Background telemetry logging, asynchronous socket draining, audio streaming, or peripheral house-keeping tasks often operate independently of the initiating thread.
- **Preventing Zombie Accumulation:** If a thread is created to perform an asynchronous task and the creator has no interest in waiting for it, detaching ensures that memory and OS resources are freed immediately when the thread finishes, without requiring a join.

## Mechanism and Language Rules
- **Function Signature:** `int thrd_detach(thrd_t thr);`
- **Return Values:** Returns `thrd_success` on success, or `thrd_error` if the operation failed.
- **Irreversibility:** Detaching a thread is irreversible. A detached thread can never be transitioned back into a joinable state.
- **Resource Cleanup Guarantee:** When a detached thread terminates (either by returning from its entry function or calling `thrd_exit`), all runtime resources (stack memory, thread control block) are automatically reclaimed by the runtime.
- **Self-Detachment:** A running thread can safely detach itself using `thrd_detach(thrd_current())`.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    uint32_t sensor_id;
    float reading;
} telemetry_pkt_t;

static int telemetry_logger(void *arg) 
{
    telemetry_pkt_t *pkt = (telemetry_pkt_t *)arg;
    if (pkt) {
        /* Process and record telemetry in the background */
        printf("Logging Telemetry: Sensor %u = %.2f\n", pkt->sensor_id, pkt->reading);
        
        /* Heap-allocated payload must be freed by detached worker */
        free(pkt);
    }
    return thrd_success;
}

int dispatch_telemetry(uint32_t sensor_id, float value) 
{
    telemetry_pkt_t *pkt = malloc(sizeof(telemetry_pkt_t));
    if (!pkt) {
        return -1;
    }
    pkt->sensor_id = sensor_id;
    pkt->reading = value;

    thrd_t bg_thread;
    if (thrd_create(&bg_thread, telemetry_logger, pkt) != thrd_success) {
        free(pkt);
        return -1;
    }

    /* Detach immediately: resources reclaim automatically on thread exit */
    if (thrd_detach(bg_thread) != thrd_success) {
        /* Thread is still running; cleanup logic must handle error */
        return -1;
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Join on Detached):** Calling `thrd_join` on a thread handle that has already been detached results in undefined behavior.
- **Undefined Behavior (Multiple Detach):** Calling `thrd_detach` multiple times on the same `thrd_t` handle is undefined behavior.
- **Process Termination Truncation:** If `main()` exits or `exit()` is invoked while detached threads are actively running, those detached threads are abruptly terminated without running stack unwinding or local cleanups.

## Edge Cases and Failure Modes
- **Use-After-Free via Stack Sharing:** Passing pointers to automatic (stack) variables of the spawning function into a detached thread is a severe defect. The spawning function will return immediately, invalidating its stack frame while the detached thread runs.
- **Orphaned Memory Leaks:** If a detached thread allocates heap memory or acquires OS file descriptors and crashes, is truncated, or fails to free them prior to returning, those resources leak permanently for the process duration.
- **Process Exit Race:** When `main()` finishes, all detached threads vanish instantly mid-instruction, risking corrupted shared state, truncated files, or half-flushed buffers.

## Embedded Implications
- **Stack Budget Exhaustion:** If fire-and-forget threads are spawned faster than they terminate (e.g., during bursty event bursts), RTOS heap or task pools will exhaust rapidly.
- **Static Tasks Preferred:** In embedded systems, permanent daemon tasks are typically created once at system boot and never destroyed or detached dynamically.

## Firmware Review Angle
- **Audit Memory Ownership:** Verify that every parameter passed to a detached thread has clear, exclusive ownership transferred to that thread (e.g., dynamic allocation freed inside the thread routine).
- **Check for Stack References:** Strict ban on passing stack addresses to detached threads.
- **Validate Clean Shutdown:** Check how the system stops detached workers during reboot, firmware update, or power failure transitions.

## Compiler, ABI, and Toolchain Implications
- **No Join Optimization:** Compilers treat detached thread entry points as roots of independent call trees.
- **Resource Destructors:** Thread-local storage (`thread_local`) destructors will still execute when a detached thread terminates.

## Performance, Memory, Timing, and Power
- **Reduced Synchronization Latency:** The creator thread incurs zero blocking overhead; it creates, detaches, and resumes execution immediately.
- **Dynamic Allocations:** Frequent creation and detachment of short-lived threads introduces memory fragmentation and scheduler thrashing.

## Verification / Debugging
- **TSan Tracking:** ThreadSanitizer tracks detached threads, but data race warnings can be harder to diagnose due to the absence of join-time happens-before edges.
- **Debugger Overhead:** In GDB, detached threads may appear and disappear unpredictably; use `set print thread-events off/on` to monitor lifetimes.

## Safety, Security, and Reliability
- **Safety Standard Non-Compliance:** Coding standards like MISRA C discourage detached threads because non-deterministic thread lifespans hinder formal schedulability analysis (e.g., Rate Monotonic Analysis).
- **Silent Failures:** Since exit codes cannot be collected from detached threads, errors occurring inside them are swallowed unless explicitly logged or broadcast via a global health monitor.

## Trade-offs and Alternatives
- **`thrd_detach` vs. `thrd_join`:** `thrd_join` provides deterministic lifecycle control, error reporting, and completion barriers; `thrd_detach` reduces coupling and memory retention at the cost of visibility.
- **Dedicated Queue Worker:** Instead of detaching dozens of short-lived threads, create a single long-lived worker thread that reads tasks off a lock-free or mutex-guarded ring buffer.

## Staff-Level Takeaway
`thrd_detach` breaks structured concurrency. Once detached, a thread becomes an independent actor with no supervisor to collect its errors or synchronize its termination. Use `thrd_detach` sparingly, primarily for persistent background services. For task-based execution, prefer a bounded worker thread pool where lifecycles are monitored and orderly shutdown can be enforced.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_thrd_create]]
- [[02_thrd_join]]
- [[04_Thread_return_values]]
- [[12_Thread_safe_module_design]]
