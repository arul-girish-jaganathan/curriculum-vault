# LeakSanitizer

> Canonical C topic note — chapter 40.

## Definition
LeakSanitizer (LSan) detects memory that remains allocated without a reachable ownership path at process termination or an explicit leak check, depending on the runtime integration.

## Mechanism and language rules
The runtime identifies allocated blocks and scans roots/references to determine reachability. A report is evidence of an allocation-lifetime problem, but intentional caches or process-lifetime allocations may require explicit policy.

## Embedded implications
Long-running firmware has no normal process exit, so leak detection is often performed in host tests or through custom allocator telemetry. Embedded memory leaks are especially serious because heap capacity is finite and fragmentation can eventually become a field failure.

## Edge cases and failure modes
- Confusing retained ownership with a leak.
- Testing only short-lived scenarios.
- Ignoring fragmentation when total allocated bytes look acceptable.
- Assuming LSan can model every embedded allocator.

## Verification / debugging
Run repeated lifecycle tests under LSan. Pair reports with ownership documentation and allocation-site traces. For firmware, add allocation counters, high-water marks, failure injection, or bounded/static allocation policies.

## Staff-level takeaway
For embedded systems, the strongest leak strategy is often architectural: bounded lifetimes and explicit ownership first, dynamic leak detection second.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
