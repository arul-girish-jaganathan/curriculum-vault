# DMA ownership

> Canonical C topic note — Chapter 45. DMA ownership defines which agent may read or modify a buffer or descriptor at each point in time. It is the central invariant for safe asynchronous memory access.

## Definition
CPU software and a DMA engine are independent agents. Ownership must transition explicitly: CPU prepares memory, publishes it to DMA, DMA operates, completion returns ownership to CPU, and only then may software consume or reuse the object.

## Mechanism and language rules
C object lifetime and aliasing rules still apply, but C alone cannot describe a peripheral's access. A pointer passed to a DMA engine can remain hardware-relevant after the initiating function returns, so storage duration must cover the entire device-use interval.

### What to reason about
- Who owns the buffer now?
- Which agent can write it?
- When is ownership transferred?
- What ordering makes the transfer visible?
- Is the address valid in the device address space?
- What happens on timeout, abort, reset, and error?

Never reuse memory merely because the CPU has finished its own code path; hardware completion is the release event.

## Embedded implications
Ownership bugs cause stale data, overwrites, duplicated packets, descriptor corruption, and sporadic failures. Ring buffers need per-slot ownership, while scatter-gather systems need ownership for every descriptor and referenced buffer.

### Firmware review angle
Represent ownership states explicitly in documentation or state fields. Define legal transitions and assert that only the owner modifies ownership-controlled data.

## Edge cases and failure modes
- CPU modifies a DMA-owned buffer.
- Timeout returns ownership before hardware actually stops.
- Peripheral reset leaves DMA active.
- Descriptor is returned to a pool while hardware still references it.
- Cache state makes ownership metadata appear inconsistent.

## Example pattern
```c
typedef enum {
    BUF_CPU,
    BUF_DMA
} buffer_owner_t;

struct dma_buffer {
    uint8_t data[512];
    buffer_owner_t owner;
};
```
The state field documents intent; synchronization and hardware enforcement still require platform-specific mechanisms.

## Verification / debugging
Instrument ownership transitions with buffer IDs and sequence numbers. Inject delayed completion, timeout, abort, and reset. Use assertions in debug builds to reject illegal transitions.

Staff-level questions: What event transfers ownership? Is that event authoritative? Can hardware continue after timeout? What memory and address-space barriers accompany the transition?

## Staff-level takeaway
DMA safety starts with one rule: **only the current owner may modify or repurpose a resource**. Make ownership transitions explicit and prove the release event before reuse.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
