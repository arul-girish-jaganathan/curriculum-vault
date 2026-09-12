# Sentinel values

> Canonical C topic note — Chapter 42. A sentinel is a reserved value that represents a special condition such as failure, end-of-sequence, absence, or “not found.” The contract must guarantee that the sentinel cannot be confused with valid data.

## Definition
Typical sentinels include `NULL` for pointer absence, `EOF` for a stream condition, `-1` for selected integer-returning APIs, or a project-specific constant. The C language does not assign universal meanings to arbitrary sentinel values; the API contract does.

## Mechanism and language rules
The sentinel must be representable in the return type and outside the valid data domain. A common mistake is selecting a value that is valid today but may become valid after future range expansion.

### What to reason about
- Is the sentinel outside the complete valid domain?
- Is signedness conversion safe?
- Does the caller test before converting the result?
- Can zero be both valid data and failure?
- Is the sentinel preserved across wrappers and ABI boundaries?

For pointers, `NULL`/a null pointer constant represents a null pointer value; it is not necessarily a bit pattern of all zero bytes. Do not infer pointer representation from integer zero without considering the C rules and target ABI.

## Embedded implications
Sentinels are cheap and deterministic, which suits small APIs and ISR-adjacent code. But overloaded status/data values can create silent bugs in telemetry, packet parsing, sensor readings, or register values where the full numeric range is valid.

### Firmware review angle
Prefer explicit status plus output when the full value domain is required. Reserve sentinel ranges intentionally in protocols and document them as part of the wire contract.

## Edge cases and failure modes
- `-1` converted to unsigned becomes a large positive value.
- `0` may be a valid sensor measurement.
- A pointer sentinel can be mishandled after integer conversion.
- A future protocol revision can make the old sentinel a valid payload.
- A caller may forget to check the sentinel before dereferencing or indexing.

## Example pattern
```c
#define INDEX_NOT_FOUND (-1)

int find_id(const uint16_t *ids, size_t count, uint16_t wanted)
{
    for (size_t i = 0; i < count; ++i) {
        if (ids[i] == wanted) {
            return (int)i;
        }
    }
    return INDEX_NOT_FOUND;
}
```
This design requires `count` to fit in `int`. If that cannot be guaranteed, return a status separately or use a representation that safely covers the complete index domain.

## Verification / debugging
Test every boundary around the valid domain and the sentinel. Compile with signed/unsigned warnings enabled. Review all wrappers for preservation of the sentinel and test protocol compatibility when ranges evolve.

Staff-level questions:
- Is the sentinel mathematically outside the valid domain?
- What happens after integer promotion/conversion?
- Would a status/output pair communicate the contract more clearly?

## Staff-level takeaway
A sentinel is safe only when its **collision with valid data is impossible by contract**. Prove that property at API design time and protect it with type choices, warnings, and boundary tests.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
