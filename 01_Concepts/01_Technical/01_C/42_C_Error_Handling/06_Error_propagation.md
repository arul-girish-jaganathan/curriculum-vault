# Error propagation

> Canonical C topic note — Chapter 42. Error propagation preserves failure meaning while moving it across call boundaries. Good propagation prevents low-level errors from being silently lost or translated into misleading success.

## Definition
A lower layer detects a failure; an upper layer decides whether to handle, translate, retry, contain, degrade, or propagate it. Propagation is therefore both a control-flow and architecture decision.

## Mechanism and language rules
C provides no exception mechanism. Propagation is normally explicit through return values, output/status structures, `errno`, callbacks, global diagnostic state, or project-specific mechanisms. Each method has different concurrency, lifetime, and observability implications.

### What to reason about
- Who is responsible for handling this failure?
- Is the error still actionable at the next layer?
- Does translation preserve root cause and context?
- Is retry safe and bounded?
- Has any output/resource state become partially valid?
- Can the error cross a thread/ISR/asynchronous boundary safely?

Avoid converting every failure into a generic `ERROR`; information loss makes recovery and diagnosis harder.

## Embedded implications
Driver failures may need translation into subsystem status while retaining hardware detail for diagnostics. A timeout may mean retry, reset, or permanent degradation depending on the peripheral state.

### Firmware review angle
Define an error taxonomy and translation boundaries. Propagation paths should have bounded time and stack usage and must not accidentally turn transient failures into infinite retry loops.

## Edge cases and failure modes
- Swallowed error followed by apparent success.
- Retry of a non-idempotent operation causing duplication.
- Error translation loses the underlying fault code.
- Error state stored globally and overwritten by another task.
- Asynchronous completion reports failure after the caller has released context.

## Example pattern
```c
status_t service_start(void)
{
    status_t st = driver_start();
    if (st != STATUS_OK) {
        return map_driver_status(st);
    }
    return STATUS_OK;
}
```
A useful `map_driver_status()` preserves distinctions required by the service contract rather than collapsing everything to one value.

## Verification / debugging
Build a failure matrix showing each lower-layer error, its translated value, caller action, and final user/system behavior. Test every path, including timeout, partial completion, retry, reset, and repeated failure.

Staff-level questions: Where should this error be handled? What information must survive? Is the propagation path bounded and concurrency-safe? Can the system distinguish transient from terminal failure?

## Staff-level takeaway
Error propagation should preserve **meaning, ownership, and recovery intent**. Define translation boundaries deliberately and retain enough information to diagnose and safely recover from the original failure.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
