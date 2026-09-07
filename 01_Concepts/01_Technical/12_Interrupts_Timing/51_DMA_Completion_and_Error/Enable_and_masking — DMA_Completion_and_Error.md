# Enable and masking — DMA Completion and Error

## Concept
**Enable and masking** in the context of **DMA Completion and Error** should be understood from the observable event through the final required response. Keep separate the hardware event, controller state, CPU/OS entry, handler execution, deferred work, and deadline completion.

## Mechanism
Reason using: **event source → capture/latch → qualification → enable/mask → priority/routing → interrupt/exception entry → handler → source acknowledgement → deferred work or return**. The exact sequence depends on the architecture and software stack.

## Timing
Track arrival time, controller latency, masking, higher-priority interference, handler WCET, deferred-work delay, queueing/backlog and end-to-end deadline. Average latency is not a worst-case guarantee.

## Embedded consequences
Examine nesting, critical sections, bus/cache contention, DMA ownership, clock changes, low-power wakeup, reset/reinitialization, burst traffic and overload. For periodic behavior, distinguish relative delay from absolute scheduling and accumulated phase error.

## Example
A data-ready event is latched by a peripheral, routed to the interrupt controller, and eventually serviced by an ISR. The ISR performs the bounded critical work, acknowledges the source in the required order, transfers data ownership, and signals deferred processing. The important requirement is usually end-to-end response, not only ISR-entry latency.

## Failure modes
Look for lost events, repeated/storming interrupts, stale status, wrong trigger polarity, excessive masking, wrong priority assumptions, unbounded ISR work, queue overflow, timer drift, counter wraparound, and instrumentation-induced timing changes.

## Debugging
Correlate hardware and software evidence: GPIO/scope or logic analyzer, cycle counters, trace timestamps, OS tracing, and driver state. Record distributions and outliers under controlled load. Explain observed maxima and test corner conditions.

## Staff review
Answer: What is the timing contract? What is the worst-case path? Which parts are architectural guarantees versus implementation choices? What operations are legal in this context? What happens when arrival rate exceeds service rate? How is the claim verified across load, clock, thermal, power and recovery corners?

## Reference
See [[Source_Backbone]] and verify target-specific behavior against the CPU/MCU reference manual and applicable RTOS/OS documentation.
