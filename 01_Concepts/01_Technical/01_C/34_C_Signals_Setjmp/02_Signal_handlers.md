# Signal handlers

> Canonical C topic note — chapter 34.

## Definition
A signal handler is a function installed to execute when a particular signal is delivered. In ISO C the handler has the form `void handler(int)`, and `signal()` associates that function with a signal. `SIG_DFL` requests the default action and `SIG_IGN` requests ignoring the signal when permitted.

A handler executes in an asynchronous context. Its most important property is therefore not its normal function-call syntax, but the severe restrictions on what it may safely observe, modify, call, and synchronize with.

## Mechanism and language rules
A typical lifecycle is:

1. Install the handler before the event can matter.
2. Program execution continues normally.
3. A signal is generated.
4. The implementation invokes the registered handler with the signal number.
5. The handler performs only permitted, minimal work.
6. On return, execution continues according to the signal semantics and implementation.

The handler's parameter identifies the signal, but the application should not infer more information than the implementation contract provides.

### What to reason about
- The handler must have a compatible function type.
- Handler execution is asynchronous relative to ordinary program flow.
- Only operations permitted by the signal model should be performed in the handler.
- Access to shared state must use the special guarantees applicable to signal handlers; `volatile` alone does not make arbitrary communication safe.
- A handler can interrupt code that currently owns a lock or is manipulating library-global state.
- Installing a handler is not the same as establishing a synchronization protocol.

The standard's rules around signal-handler access are deliberately narrow. Objects that may be communicated safely with a handler are a special case; ordinary mutable global data must not be treated as automatically safe merely because it is global.

## Embedded implications
If an embedded libc supports signals, keep handlers tiny. A useful pattern is **capture → record minimal state → return**. Let the main loop, task, or supervisor perform the expensive recovery.

Do not assume that a signal handler can safely call a logging stack, allocate memory, take an RTOS mutex, access a peripheral driver, or invoke arbitrary libc routines. Those operations may depend on implementation details and can deadlock or corrupt state if they interrupt code already using the same subsystem.

### Firmware review angle
Review:
- handler stack consumption;
- nesting and masking behavior;
- whether the handler can interrupt a critical section;
- whether the handler touches MMIO with required ordering;
- whether the handler shares state with foreground code;
- reset and watchdog interactions;
- worst-case execution time and repeated delivery.

## Edge cases and failure modes
Bad patterns include:
- calling `printf()` from a handler;
- calling `malloc()` or `free()`;
- acquiring a mutex held by interrupted code;
- manipulating complex data structures;
- performing unbounded loops;
- assuming only one signal can arrive;
- installing handlers after a race window already exists;
- using non-atomic ordinary state as a communication channel.

A subtle failure is handler re-entry or nested delivery where supported. A handler that is correct for one invocation may fail if state is shared across invocations without an explicit design.

## Example pattern
```c
#include <signal.h>

static volatile sig_atomic_t event_pending;

static void handler(int signo)
{
    (void)signo;
    event_pending = 1;
}
```

The handler records a small event and leaves the real work to normal execution.

## Verification / debugging
Use fault injection or a host test harness to deliver signals at inconvenient points: during I/O, shutdown, allocation, and critical sections. Verify that the handler remains bounded and does not call unsafe APIs.

For embedded implementations, inspect the libc/RTOS documentation and generated code rather than assuming POSIX behavior. Measure handler stack use and latency if the target actually supports signals.

Staff-level review questions:
- Can the handler be reduced to a flag or event record?
- Which exact functions are permitted in this implementation's handler context?
- Can it interrupt code holding a resource it needs?
- What happens on repeated or nested delivery?

## Staff-level takeaway
A signal handler should be designed as an asynchronous interrupt to program invariants: **do the minimum necessary and defer work**. If substantial work is required, a normal event/message mechanism is usually a safer architecture.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
