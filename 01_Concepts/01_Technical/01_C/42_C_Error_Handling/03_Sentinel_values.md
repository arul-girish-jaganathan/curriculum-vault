# Sentinel values

> Canonical C topic note — Chapter 42. A sentinel is a reserved value that represents a special condition such as failure, end-of-sequence, or absence of an object. Its safety depends on proving that the sentinel cannot be confused with valid data.

## Definition
Common examples include `NULL` for pointer absence, `-1` for an index/error result, zero-length indicators, and protocol-specific marker values. The sentinel must belong to the return-value domain and have an unambiguous interpretation.

## Mechanism and language rules
A sentinel is safe only if the valid-value domain excludes it or the API carries enough context to distinguish it. Signed/unsigned conversions are a frequent source of bugs: returning `-1` from a function whose type is `size_t` produces a large unsigned value rather than a negative result.

### What to reason about
- Is the sentinel representable in the declared return type?
- Can a valid object/data value equal the sentinel?
- Are signedness conversions involved?
- Is the caller required to check before using the result?
- Does zero mean “empty,” “success,” or “not found” in this API?
- Is the sentinel preserved through serialization or ABI boundaries?

Prefer an explicit status plus output parameter when every data value is potentially valid.

## Embedded implications
Sentinels are efficient and avoid extra storage, which is attractive in constrained firmware. However, hardware registers and protocol fields often use all bit patterns, making sentinel reservation impossible without sacrificing valid states.

### Firmware review angle
For driver APIs, document whether `0`, `UINT_MAX`, `NULL`, or another marker is a valid result. Consider enums/status-plus-output when the data domain is exhaustive.

## Edge cases and failure modes
- `-1` converted to a huge `size_t`.
- A valid packet length equals the chosen marker.
- `NULL` is checked too late and dereferenced first.
- Sentinel meaning changes across abstraction layers.
- A serialized sentinel collides with legitimate wire data.

## Example pattern
```c
int find_channel(uint32_t id)
{
    for (int i = 0; i < CHANNEL_COUNT; ++i) {
        if (channels[i].id == id) {
            return i;
        }
    }
    return -1;
}
```
The caller must keep the result in a signed type and check it before indexing.

## Verification / debugging
Test the minimum, maximum, and sentinel values explicitly. Compile with conversion/sign warnings. Use boundary-value tests and static analysis to find unchecked sentinel paths.

Staff-level questions: Is the sentinel outside the complete valid domain? Would a future extension make it valid? Is a status-plus-output interface clearer and safer?

## Staff-level takeaway
A sentinel is a **compressed contract**. It saves representation overhead only when the reserved value is provably unambiguous and callers consistently validate it before use.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
