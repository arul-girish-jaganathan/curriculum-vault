# ThreadSanitizer

## Definition
**ThreadSanitizer (TSan)** dynamically detects many data races and synchronization errors in multithreaded programs. It instruments memory accesses and synchronization operations, then reports conflicting accesses that occur without a valid happens-before relationship under the modeled concurrency system.

## Scope and boundaries
TSan is primarily a host-platform testing tool. Support for embedded targets is limited and highly architecture/runtime dependent. It cannot prove absence of all races and may not understand custom synchronization, inline assembly, interrupt semantics, or hardware concurrency correctly.

## Mechanism and language rules
Consider:

```c
int ready;
int value;

/* One thread writes value/ready while another reads them. */
```

If accesses to shared objects lack proper synchronization, TSan can report the conflicting locations and call stacks. In portable C, `_Atomic` operations and mutex/thread primitives establish the relevant synchronization; `volatile` does not.

## Embedded implications
A strong embedded workflow compiles portable concurrency logic for a host process and runs it under TSan. This can find races in queues, state machines, worker threads, and shared configuration. ISR/main-loop concurrency remains a separate target concern because an interrupt is not simply another C11 thread.

Custom RTOS primitives need correct annotations/modeling or targeted tests; otherwise TSan may not recognize their synchronization semantics.

## Edge cases and failure modes
- Assuming TSan can model interrupt races or DMA.
- Using volatile and believing the race is fixed.
- Custom atomics/assembly are invisible to the analyzer.
- Race manifests only under a workload not exercised by the test.
- False confidence because one schedule happened to be clean.

## Verification / debugging
Run deterministic and stress tests under TSan, especially around queues, shutdown, initialization, and error paths. Preserve both conflicting stack traces. Replace custom synchronization with standard primitives in host tests where feasible, or explicitly model its semantics.

## Performance, memory, timing and power
TSan can impose very high CPU and memory overhead, making it unsuitable for production firmware and many real-time target environments. Its purpose is to explore concurrency bugs under controlled test conditions.

## Staff-level takeaway
Use TSan to validate the **C-level concurrency contract**, while separately validating ISR, DMA, cache, and hardware synchronization on the target. A race detector complements rather than replaces architectural concurrency design.