# Async-signal-safety

> Canonical C topic note — chapter 34.

## Definition
**Async-signal-safety** is the requirement that code executing in a signal handler remain valid when it interrupts an arbitrary point in normal execution. A function that is safe for ordinary calls is not automatically safe when called asynchronously.

ISO C defines a restricted signal-handler environment. POSIX adds a substantially larger, explicitly documented async-signal-safe function set. These must not be conflated.

## Mechanism and language rules
The central hazard is interruption of shared execution state. Suppose normal code is halfway through updating a library object, owns a lock, or has temporarily changed global invariants. A signal handler executes at that point. If the handler invokes the same subsystem, it can observe inconsistent state or wait forever.

For portable C, handler code should be limited to operations for which the C standard gives the required signal guarantees, with communication normally performed through an appropriately declared `volatile sig_atomic_t` object or another implementation-specific mechanism with documented guarantees.

### What to reason about
- `volatile` prevents certain compiler optimizations of accesses but is not a general atomicity or memory-ordering primitive.
- `sig_atomic_t` identifies an integer type whose accesses have the required atomicity property for signal-handler communication under the C signal model.
- A library function must not be assumed safe merely because it is reentrant in ordinary multithreaded code.
- Allocators, stdio, locks, locale state, and other stateful subsystems are common danger areas.
- `errno`, thread-local state, and signal masks are platform-specific concerns unless the implementation documents stronger guarantees.

The important distinction is **reentrancy versus asynchronous signal safety**. A function can be reentrant yet still depend on resources or operations that are unsuitable for asynchronous interruption.

## Embedded implications
On embedded systems, the closest architectural analogue is ISR-safe code. The same principle applies: the asynchronous context should do minimal bounded work and communicate an event to normal execution.

However, an ISR and a C signal handler are not interchangeable. ISR safety depends on CPU exception rules, interrupt controller behavior, RTOS critical sections, memory ordering, and vendor APIs. Signal safety depends on the C runtime's signal model.

### Firmware review angle
Build a context matrix for every callable API:

| API | Thread/task | ISR | Signal handler | Fault handler |
|---|---|---|---|---|
| bounded register write | usually | target-dependent | implementation-dependent | target-dependent |
| allocator | usually | no | no assumption | generally no |
| stdio/logger | usually | generally no | no assumption | generally no |
| flag/event store | yes | if designed | if permitted | target-dependent |

Require the owner of each subsystem to document its context restrictions.

## Edge cases and failure modes
Typical failures:
- deadlock because the handler interrupts code holding a lock;
- allocator corruption because allocation was interrupted and re-entered;
- recursive logging because the logger itself triggered the signal;
- partially updated state observed by the handler;
- stack exhaustion from unexpectedly deep handler paths;
- hidden calls to unsafe functions through wrappers.

A wrapper such as `fatal_log()` is not automatically safe just because its body appears small. Review its complete call graph, including formatting, allocation, locks, drivers, and output backends.

## Example pattern
```c
#include <signal.h>

static volatile sig_atomic_t shutdown_requested;

static void on_signal(int signo)
{
    (void)signo;
    shutdown_requested = 1;
}

static void service(void)
{
    if (shutdown_requested) {
        /* Perform complex cleanup here, outside the handler. */
    }
}
```

## Verification / debugging
Create a host test that repeatedly injects signals while executing library operations. Run with sanitizers where supported, then inspect deadlocks, corrupted state, and missed events.

For firmware-like environments, review call graphs and mark APIs with context annotations such as `TASK_ONLY`, `ISR_SAFE`, or `SIGNAL_SAFE`. Static analysis can then reject accidental crossings.

Staff-level questions:
- Is the safety claim based on ISO C, POSIX, or vendor documentation?
- Is every transitive function call safe?
- What shared state can be interrupted?
- What is the bounded worst-case handler time?
- What happens if the event arrives again before the first one is processed?

## Staff-level takeaway
Async-signal-safety is fundamentally about **interruption of invariants**. The robust pattern is to make the asynchronous path tiny, bounded, and explicit, and defer complex work to a context designed to perform it safely.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
