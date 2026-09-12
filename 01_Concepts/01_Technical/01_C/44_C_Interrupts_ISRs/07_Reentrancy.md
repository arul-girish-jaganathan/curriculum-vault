# Reentrancy

> Canonical C topic note — Chapter 44. A function is reentrant when concurrent or nested invocations can execute safely without corrupting shared state or depending on a single invocation's mutable context.

## Definition
A function that uses only local state or properly synchronized shared state is easier to make reentrant. Static mutable variables, global buffers, non-reentrant library state, and unsynchronized device access commonly break reentrancy.

## Mechanism and language rules
An ISR can interrupt a task while the task is inside the same function. If the ISR invokes that function again, two invocations overlap. The C language does not automatically protect shared objects; the implementation must establish a valid concurrency model.

### What to reason about
- What mutable state exists between calls?
- Is it static/global or caller-owned?
- Can a callback re-enter the function?
- Are shared accesses atomic and properly ordered?
- Does the function depend on a single hardware transaction in progress?

## Embedded implications
A non-reentrant logger, allocator, protocol parser, or driver can fail when called from both task and ISR contexts. Even if the data race is rare, interrupt timing can expose it.

### Firmware review angle
Prefer context-specific APIs, caller-provided state, or serialized ownership. Avoid hidden global state where practical. Document functions as ISR-safe/reentrant/non-reentrant explicitly.

## Edge cases and failure modes
- Static temporary buffer overwritten by nested call.
- Function-level state changed by an ISR during a task operation.
- Callback re-enters an API while its internal state is inconsistent.
- A lock intended for task context is unusable in an ISR.

## Example pattern
```c
static int parse_state;

int parse_byte(uint8_t b)
{
    parse_state = update_state(parse_state, b);
    return parse_state;
}
```
This function is not inherently reentrant because invocations share `parse_state`. Passing parser state through a caller-owned object is usually clearer.

## Verification / debugging
Search for static/global mutable state in ISR-reachable call graphs. Stress nested invocation and callback re-entry. Use race detectors on host equivalents and target instrumentation for timing-sensitive cases.

## Staff-level takeaway
Reentrancy is a **state ownership property**. Make mutable state explicit, serialize where necessary, and never assume that a function safe in task context remains safe when an interrupt can interrupt and re-enter it.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
