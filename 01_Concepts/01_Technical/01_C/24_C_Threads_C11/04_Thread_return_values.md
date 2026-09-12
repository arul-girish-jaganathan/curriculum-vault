# 04: Thread Return Values

## Definition
Thread return values in C11 represent the completion status of a concurrent thread. A thread returns an `int` value either by executing a `return` statement in its top-level `thrd_start_t` entry routine, or by invoking `thrd_exit(int res)`. This integer status is harvested synchronously by another thread via `thrd_join`.

## Scope and Boundaries
- **Covers:** `thrd_start_t` return conventions, `thrd_exit()`, capturing return codes via `thrd_join()`, and standard return constants (`thrd_success`, `thrd_error`).
- **Does not cover:** Complex data structures returned from threads, heap management for thread payloads, or thread cancellation mechanisms ([[09_Thread_cancellation_boundaries]]).

## Why Does It Exist
Concurrent tasks must convey their execution outcome:
- **Error Propagation:** The spawning thread or orchestrator needs to know if the child thread completed its computation successfully, ran out of memory, or timed out.
- **POSIX vs C11 Realignment:** POSIX `pthread_join` returns `void *`, which frequently tempted developers to cast pointers to integers unsafely or leak heap-allocated result objects. C11 mandates an `int` return type, enforcing simple, robust exit status transmission.

## Mechanism and Language Rules
- **Entry Signature:** `int (*thrd_start_t)(void *)` — return value must be an `int`.
- **Explicit Exit:** `_Noreturn void thrd_exit(int res);`
  - Terminates the calling thread immediately.
  - Returns `res` to any thread performing `thrd_join` on it.
  - Flushes and executes destructors for any non-NULL thread-local objects.
- **Implicit Exit:** Returning an `int` from the top-level thread function is semantically equivalent to calling `thrd_exit(return_value)`.
- **Harvesting Result:**
  ```c
  int exit_status = 0;
  thrd_join(thread_id, &exit_status);
  ```
  If `&exit_status` is `NULL`, the exit status is discarded.
- **Main Thread Exit:** Returning from `main()` or calling `exit()` terminates the entire process, including all running threads, regardless of their return values.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>

#define ERR_SENSOR_TIMEOUT  (-1)
#define ERR_BUFFER_OVERFLOW (-2)
#define TASK_OK             (0)

static int sample_sensor_task(void *arg) 
{
    int *sensor_id = (int *)arg;
    if (!sensor_id) {
        thrd_exit(ERR_SENSOR_TIMEOUT); /* Early termination via thrd_exit */
    }

    if (*sensor_id < 0) {
        return ERR_BUFFER_OVERFLOW;    /* Standard return */
    }

    /* Simulate normal work */
    return TASK_OK;
}

int main(void) 
{
    thrd_t worker;
    int id = 42;

    if (thrd_create(&worker, sample_sensor_task, &id) != thrd_success) {
        return EXIT_FAILURE;
    }

    int task_result = 0;
    if (thrd_join(worker, &task_result) != thrd_success) {
        fprintf(stderr, "Failed to join worker\n");
        return EXIT_FAILURE;
    }

    if (task_result != TASK_OK) {
        printf("Thread failed with error code: %d\n", task_result);
        return EXIT_FAILURE;
    }

    printf("Thread executed successfully.\n");
    return EXIT_SUCCESS;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Pointer as Integer (UB risk):** Attempting to cast a dynamic heap pointer to `int` and return it via `thrd_exit((int)ptr)` produces undefined or truncated behavior on 64-bit systems where `sizeof(void *) == 8` and `sizeof(int) == 4`.
- **Uncaptured Detached Returns:** The return value of a detached thread is discarded; reading or capturing it is impossible.

## Edge Cases and Failure Modes
- **Complex Result Marshalling:** If a thread needs to return large datasets, it cannot use the `int` return mechanism directly. It must store results in a caller-allocated context structure passed via `void *arg`, or allocate heap memory and store the pointer in that context struct.
- **Premature Termination via `exit()`:** If a worker thread calls standard `exit()` instead of `thrd_exit()`, the entire application terminates immediately, bypassing other threads' joins and cleanups.

## Embedded Implications
- **Status Register Emulation:** In embedded control systems, integer return values map directly onto system health codes or fault register masks.
- **Low Footprint:** Passing an integer through registers avoids heap allocation for thread outcome reporting, preserving deterministic timing.

## Firmware Review Angle
- **No Pointer Casting:** Strictly verify that developers do not cast addresses or pointers to `int` to pass results out of `thrd_exit`.
- **Audit All Join Sites:** Ensure the caller inspects the retrieved `int` status code and does not simply check that `thrd_join` returned `thrd_success`.
- **Ensure Bounded Enums:** Define an enumeration of valid thread exit codes rather than using arbitrary magic integers.

## Compiler, ABI, and Toolchain Implications
- **Register Storage:** The return value of a thread entry point is passed according to the standard ABI integer return register (e.g., `EAX` on x86, `R0` on ARM).
- **`_Noreturn` Optimization:** Compilers exploit `_Noreturn` on `thrd_exit()` to optimize register usage and omit prologue/epilogue restoration code.

## Performance, Memory, Timing, and Power
- **Zero Overhead:** Transferring the integer exit code via `thrd_join` has zero dynamic memory cost and incurs no cache pollution.
- **Registers vs Memory:** The runtime caches the integer exit code inside the thread's internal OS kernel or library context structure until `thrd_join` extracts it.

## Verification / Debugging
- **Valgrind / TSan:** Sanitizers verify that the destination integer memory passed to `thrd_join` is correctly initialized by the join operation.
- **GDB Breakpoints:** Setting breakpoints on `thrd_exit` allows inspection of local thread state before resources are unmapped.

## Safety, Security, and Reliability
- **Safety Standard Rules:** Unchecked thread exit codes violate MISRA and safety directives. The orchestrator must handle error states deterministically (e.g., initiate graceful fallback or reset).
- **Fault Concealment:** Ignoring thread return values masks worker crashes, memory allocations failures, or peripheral timeouts.

## Trade-offs and Alternatives
- **`int` Return Code vs Out-Parameter Context:**
  - *`int` Return:* Simple, safe, standard-enforced, register-passed; strictly limited to scalar status codes.
  - *Context Structure:* Allows returning arbitrary structs, buffers, and metrics; requires strict lifetime management to avoid data races.

## Staff-Level Takeaway
C11's decision to restrict thread return values to `int` is a deliberate architectural improvement over POSIX's `void *`. It establishes a clean separation: use the return value strictly for completion status and error categorization; use shared context structures (synchronized via join or atomics) for actual data payloads.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_thrd_create]]
- [[02_thrd_join]]
- [[03_thrd_detach]]
- [[12_Thread_safe_module_design]]
