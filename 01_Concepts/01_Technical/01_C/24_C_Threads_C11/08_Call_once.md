# 08: Call Once

## Definition
`call_once` is the C11 thread-safe initialization primitive declared in `<threads.h>`. It ensures that a specified initialization function is invoked exactly once across the lifetime of the application, regardless of how many concurrent threads attempt the invocation simultaneously. It relies on a state flag of type `once_flag` initialized via `ONCE_FLAG_INIT`.

## Scope and Boundaries
- **Covers:** `call_once`, `once_flag`, `ONCE_FLAG_INIT`, idempotent subsystem initialization, and execution memory fences.
- **Does not cover:** General mutex locking ([[05_Mutexes]]), recursive initialization, or condition variables ([[06_Condition_variables]]).

## Why Does It Exist
Lazy initialization of shared resources (e.g., hardware drivers, global lookup tables, cryptographic engines) in multithreaded environments is notoriously prone to race conditions:
- **Double-Checked Locking Hazard:** Naive attempts to check a flag, lock a mutex, and initialize suffer from subtle memory ordering bugs unless sophisticated atomic fences are used.
- **Portability:** C11 `call_once` provides a bulletproof, standardized equivalent to POSIX `pthread_once` and C++ `std::call_once`.
- **Zero-Boilerplate Idempotence:** Handles mutex acquisition, execution serialization, memory synchronization, and completion marking automatically.

## Mechanism and Language Rules
- **Function Prototype:** `void call_once(once_flag *flag, void (*func)(void));`
- **Initialization Macro:** `once_flag flag = ONCE_FLAG_INIT;`
- **Execution Semantics:**
  - The first thread calling `call_once` executes `func()`.
  - Concurrent threads calling `call_once` block until `func()` completes.
  - Subsequent calls by any thread after `func()` has completed return immediately without executing `func()`.
- **Memory Synchronization:** The completion of `func()` in the initializing thread synchronizes-with all subsequent returns from `call_once` using that flag across all threads. Any memory writes performed by `func()` are guaranteed visible to all callers.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    double lookup_table[256];
    int is_ready;
} engine_config_t;

static engine_config_t g_config;
static once_flag g_config_initialized = ONCE_FLAG_INIT;

static void initialize_engine(void) 
{
    printf("Initializing shared engine lookup table...\n");
    for (int i = 0; i < 256; ++i) {
        g_config.lookup_table[i] = i * 3.141592653589793;
    }
    g_config.is_ready = 1;
}

double query_engine(int index) 
{
    /* Thread-safe, lazy initialization */
    call_once(&g_config_initialized, initialize_engine);
    
    /* Memory written during initialize_engine is guaranteed visible */
    if (index >= 0 && index < 256) {
        return g_config.lookup_table[index];
    }
    return 0.0;
}

static int worker(void *arg) 
{
    int worker_id = (int)(intptr_t)arg;
    double val = query_engine(worker_id * 10);
    printf("Worker %d read value: %.2f\n", worker_id, val);
    return 0;
}

int main(void) 
{
    thrd_t threads[4];
    for (intptr_t i = 0; i < 4; ++i) {
        thrd_create(&threads[i], worker, (void *)i);
    }
    for (int i = 0; i < 4; ++i) {
        thrd_join(threads[i], NULL);
    }
    return EXIT_SUCCESS;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Recursive Call):** If `func` directly or indirectly calls `call_once` with the same `once_flag`, recursive deadlock or undefined behavior occurs.
- **Undefined Behavior (Improper Initialization):** Failing to initialize `once_flag` with `ONCE_FLAG_INIT` (e.g., leaving it uninitialized on the stack) causes undefined behavior.
- **Undefined Behavior (Exceptional Termination):** If `func` terminates via `thrd_exit` or `exit`, the state of the `once_flag` is unspecified or undefined in subsequent calls.

## Edge Cases and Failure Modes
- **Function Takes No Arguments:** `func` must have the signature `void (*)(void)`. You cannot pass parameters directly. Any context must be passed via static variables.
- **Failed Initialization:** If `initialize_engine()` fails (e.g., out of memory), `call_once` still marks the flag as executed! It does **not** retry on failure. If initialization can fail, `call_once` is insufficient; manual mutex-protected initialization with retry logic is required.

## Embedded Implications
- **Deterministic Booting:** In hard real-time systems, lazy initialization introduces non-deterministic execution spikes (jitter) for the unlucky thread that triggers the init. Staff engineers usually prefer eager initialization during pre-scheduler board boot.
- **ROM/BSS Footprint:** `once_flag` typically occupies a single atomic integer (4 bytes), making it extremely lightweight.

## Firmware Review Angle
- **Static Storage Duration:** Ensure `once_flag` variables have static storage duration (file static or global). Never allocate `once_flag` on a local stack.
- **Check for Failure Handling:** Confirm that the initialization function cannot fail. If it can fail, flag this as an architectural defect because `call_once` will not re-run.
- **Audit Initialization Order:** Verify that `func` does not depend on other uninitialized singletons, preventing hidden circular dependencies.

## Compiler, ABI, and Toolchain Implications
- **Acquire-Release Semantics:** The fast path of `call_once` checks the flag using an atomic acquire load. If already initialized, it executes zero locks, returning in ~1-3 nanoseconds.
- **Futex Backing:** The slow path (initial execution or contention) uses a mutex or OS futex to block contending threads.

## Performance, Memory, Timing, and Power
- **Fast Path:** Nearly zero overhead after initial execution; performs a single atomic load with acquire memory ordering.
- **Contention Window:** The blocking window only exists during the very first run of `func()`. Subsequent calls execute concurrently without serialization.

## Verification / Debugging
- **ThreadSanitizer:** Validates that data written inside `func()` is safely synchronized with readers across all calling threads.
- **Testing Concurrency:** Launch hundreds of threads simultaneously targeting the same `call_once` site to verify that `func` executes exactly once.

## Safety, Security, and Reliability
- **Eliminates Race Conditions:** Eliminates ad-hoc, broken double-checked locking patterns that plague junior concurrent codebases.
- **MISRA Compliance:** Widely accepted as the safest mechanism for multithreaded singletons and lookup tables.

## Trade-offs and Alternatives
- **`call_once` vs. Eager Init in `main()`:** Eager initialization in `main()` before threads are spawned eliminates the need for synchronization flags entirely. However, `call_once` is essential for modular libraries that cannot dictate the application's `main()` startup sequence.
- **`call_once` vs. Mutex + Flag:** `call_once` is vastly more performant on the fast path than acquiring a mutex on every query.

## Staff-Level Takeaway
`call_once` is the only standard-sanctioned way to perform lazy initialization in C11. However, remember its critical limitation: it has no failure recovery. Use `call_once` strictly for operations guaranteed to succeed (e.g., math tables, static configurations); for operations that can fail (network sockets, hardware init), use an explicit mutex with error states and retry semantics.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_Mutexes]]
- [[10_C11_thread_portability]]
- [[12_Thread_safe_module_design]]
