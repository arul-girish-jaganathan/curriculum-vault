# assert macro

> Canonical C topic note — chapter 35.

## Definition
`assert` is a macro defined by `<assert.h>` that checks a scalar expression when assertions are enabled. If the expression compares equal to zero, the implementation reports a diagnostic and calls `abort()`; when `NDEBUG` is defined before `<assert.h>` is included, the standard assertion mechanism is disabled. The exact diagnostic text and termination details are implementation-defined. `assert` is a debugging/contract mechanism, not a recovery mechanism.

## Mechanism and language rules
The expression is evaluated when assertions are enabled, so it may have side effects. This makes `assert(x++)` dangerous: compiling with `NDEBUG` can remove the increment entirely and change program behavior. Therefore an assertion must not contain required work.

```c
#include <assert.h>

assert(ptr != NULL);
assert(len <= BUFFER_SIZE);
```

The expression is converted to a scalar truth value. A false assertion normally results in diagnostic output followed by `abort()`. The macro may evaluate its argument zero times when disabled. `NDEBUG` affects `assert` at preprocessing time, so build configuration and include ordering matter.

### What to reason about
- Never put required state updates, I/O, locking, reference counting, or MMIO writes inside an assertion.
- Distinguish an invariant check from an input-validation/error-handling path.
- Consider whether evaluating the expression itself can fault or invoke non-reentrant code.
- Verify whether the assertion remains enabled in the production configuration.

## Embedded implications
On firmware, a failed assertion may stop the CPU, reset the device, enter a fault loop, or invoke a platform-specific diagnostic hook. Logging a large formatted message from an assertion can consume substantial flash, stack, CPU time, and power.

Assertions should be designed around the system's failure policy: fail-stop for safety-critical invariant violations, controlled degradation for recoverable faults, or telemetry-and-reset for field devices. ISR assertions must avoid unsafe reporting paths.

### Firmware review angle
Compare Debug, Release, manufacturing, bootloader, and safety builds. Check `NDEBUG`, linker dead-code removal, stack usage, watchdog interaction, and whether assertion handlers are reachable from interrupt/fault contexts.

## Edge cases and failure modes
Common defects include side effects in the expression, assuming assertions validate external input, using assertions for security checks that disappear in production, and relying on a particular diagnostic string.

A subtle trap is:
```c
assert(config != NULL);
use(config);       /* still executes with NDEBUG */
```

If `config == NULL` is a real runtime error, use explicit validation instead.

## Example pattern
```c
static bool queue_push(queue_t *q, item_t item)
{
    assert(q != NULL);
    assert(q->count <= QUEUE_CAPACITY);
    /* No required side effects belong in either assertion. */
    return queue_push_impl(q, item);
}
```

## Verification / debugging
Build once with assertions enabled and once with `-DNDEBUG`; inspect the generated code and test both paths. Use static analysis to flag assertion side effects and test that the failure handler records enough context without recursively failing.

## Staff-level takeaway
Treat `assert` as an executable statement of an invariant. A Staff engineer should be able to identify which conditions are impossible by design, which are valid runtime errors, and which failure policy applies when an invariant is violated.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
