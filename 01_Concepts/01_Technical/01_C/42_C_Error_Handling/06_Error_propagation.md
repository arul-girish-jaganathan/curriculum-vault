# Error propagation

> Canonical C topic note — Chapter 42. Error propagation preserves failure information while returning through abstraction layers. A good design prevents low-level failures from being silently discarded or incorrectly translated.

## Definition
A caller that cannot handle an error should return, translate, retry, or escalate it according to the contract. Propagation can use return codes, status objects, error enums, or project-specific result structures.

## Mechanism and language rules
Every layer should preserve the distinction between the original cause and the local context. Blindly replacing `STATUS_TIMEOUT` with `STATUS_ERROR` loses diagnostic information. Blindly exposing low-level hardware codes can leak implementation details into stable public APIs.

### What to reason about
- Which failures are recoverable at this layer?
- Is context needed to understand the failure?
- Does translation preserve enough information?
- Are outputs valid after propagation?
- Is retry safe and bounded?

A useful pattern is to keep a stable public status domain while attaching a diagnostic cause/context internally.

## Embedded implications
Propagation paths often cross driver, middleware, service, and application layers. A UART timeout may become a communication-service failure and eventually a degraded operating mode. Retry loops can consume CPU, increase latency, and prevent watchdog servicing if unbounded.

### Firmware review angle
Define ownership of retry policy. The driver should generally report the hardware failure; the service layer decides whether retry is meaningful; the application decides whether degraded operation is acceptable.

## Edge cases and failure modes
- Swallowing an error and returning success.
- Converting all errors to one generic code.
- Retrying non-idempotent operations.
- Infinite retry loops during permanent hardware failure.
- Losing the original error while adding context.

## Example pattern
```c
status_t service_start(void)
{
    status_t st = driver_init();
    if (st != STATUS_OK) {
        record_failure(SERVICE_START, st);
        return st;
    }
    return STATUS_OK;
}
```
The diagnostic record adds context without changing the driver's status semantics.

## Verification / debugging
Create tests for every failure injected at each layer and verify the final observable behavior. Test retry limits, timeout propagation, and degraded-mode transitions. Review status mappings as part of interface compatibility.

Staff-level questions:
- Where is the first layer that can make a meaningful recovery decision?
- Is error context preserved?
- Could retry amplify the failure?
- Does the public API expose implementation details unnecessarily?

## Staff-level takeaway
Error propagation is **information flow plus recovery ownership**. Preserve causality, put retry decisions at the correct abstraction layer, and prevent failures from disappearing at subsystem boundaries.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
