# LeakSanitizer

## Definition
**LeakSanitizer (LSan)** detects memory leaks by identifying allocated objects that remain unreachable from the program's considered roots at shutdown or another analysis point. It is commonly integrated with AddressSanitizer in host test environments.

## Scope and boundaries
Leak detection is most meaningful for dynamically allocated memory. It does not automatically imply that every retained allocation is a bug: caches, global ownership, intentionally persistent objects, and allocator internals may remain reachable. Embedded systems also commonly use static allocation, pools, or custom allocators that require different analysis.

## Mechanism and language rules
A conceptual model is:

```text
allocation -> ownership graph -> program termination -> reachability scan
```

If an allocated block has no path from the roots considered by the runtime, LSan can report its allocation stack. The C language itself does not define a leak detector; this is a testing/runtime facility.

## Embedded implications
LSan is especially useful for host-side testing of parsers, protocol sessions, configuration handling, and lifecycle code. For firmware, the more important question may be bounded allocation behavior: whether memory use grows over repeated reconnects, error recovery, or task restart cycles.

Custom RTOS heaps, static pools, and persistent allocations may not be represented accurately by standard host leak tooling.

## Edge cases and failure modes
- Intentional process-lifetime allocations are reported as leaks.
- A custom allocator is not visible to the sanitizer.
- Ownership is retained through global state and therefore not considered leaked.
- The test exits before the relevant lifecycle completes.
- A host allocator behavior differs from the target allocator.

## Verification / debugging
Run lifecycle tests repeatedly, especially success/error/retry paths. Record allocation and deallocation ownership. For embedded targets, instrument the allocator with allocation counts, high-water marks, pool occupancy, and failure counters.

## Performance, memory, timing and power
LSan adds runtime and memory overhead during tests but no production cost when disabled. Its main embedded value is finding unbounded resource growth before deployment.

## Staff-level takeaway
Do not reduce “memory safety” to leaks. For embedded systems, combine leak detection with ownership analysis, bounded allocation policy, allocator instrumentation, and long-duration soak tests.