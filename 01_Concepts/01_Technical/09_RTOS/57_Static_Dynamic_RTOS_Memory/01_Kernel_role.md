# 57.01 Kernel role

## Core idea

An RTOS provides kernel mechanisms for scheduling, synchronization, timing, and resource management in systems where the timing of events matters. A real-time system is characterized by required timing behavior, not merely by having a fast CPU. citeturn331504search3turn331504search2

This is the canonical note for **Kernel role** within **Static versus Dynamic RTOS Allocation**. Other RTOS notes should link here instead of repeating the same explanation.

## Mental model

```text
hardware event -> ISR -> RTOS synchronization -> task -> application state
```

The diagram is an abstraction. The exact scheduler, data structure, interrupt mechanism and timing depend on the RTOS, CPU architecture and configuration.

## Mechanism

Reason through:
1. What event or API begins the operation?
2. Which task/context changes state?
3. What kernel state must change?
4. When can the scheduler run?
5. What resource is owned or released?
6. What happens if the operation times out or fails?

## Timing

Record:
- nominal execution time;
- worst-case execution time;
- blocking duration;
- interrupt interference;
- scheduler/dispatch latency;
- deadline;
- jitter;
- time-base resolution.

Average latency is not enough for a real-time claim.

## Failure modes

Look for:
- deadlock;
- priority inversion;
- starvation;
- race condition;
- missed timeout;
- queue overflow;
- task stack overflow;
- heap/pool exhaustion;
- stale buffer ownership;
- watchdog reset.

## Debugging

Capture the task state, priority, CPU/core, stack watermark, blocking object, timestamp and relevant interrupt history. Trace tools are particularly valuable because scheduling bugs are often interleaving-dependent. Zephyr's documentation and examples explicitly emphasize tracing synchronization and scheduling behavior in pipeline-style systems. citeturn381180search16

## Verification

Test:
- nominal behavior;
- timeout behavior;
- overload;
- worst-case task ordering;
- priority changes;
- repeated start/stop;
- reset during operation;
- resource exhaustion;
- ISR interaction.

## Embedded perspective

Determine whether the operation is legal in:
- ISR context;
- task context;
- scheduler-disabled context;
- critical section;
- startup/shutdown;
- low-power transition.

Never assume an RTOS API is ISR-safe just because it has an async-looking name; consult the specific RTOS contract.

## API / design review

For this topic, document:
- ownership;
- blocking semantics;
- timeout semantics;
- priority effects;
- ISR usage;
- memory allocation;
- failure return;
- recovery;
- observability.

## Staff-level checkpoint

Explain why this primitive/architecture was selected, what the worst-case timing/resource cost is, what failure mode is created by the choice, and what evidence proves the resulting system meets its timing requirements.

## Related

- [[../01_RTOS_Fundamentals/00_Chapter_Index|RTOS Fundamentals]]
- [[../13_Scheduler_Basics/00_Chapter_Index|Scheduler]]
- [[../23_Interrupts_RTOS/00_Chapter_Index|Interrupts]]
- [[../31_Mutexes/00_Chapter_Index|Mutexes]]
- [[../43_Queues/00_Chapter_Index|Queues]]
- [[../50_Task_Timing/00_Chapter_Index|Task Timing]]
- [[../79_Diagnostics_Tracing/00_Chapter_Index|Diagnostics and Trace]]
- [[../90_Staff_RTOS/00_Chapter_Index|Staff-Level RTOS]]

## Source backbone

GeeksforGeeks RTOS/OS curriculum: https://www.geeksforgeeks.org/operating-systems/real-time-operating-system-rtos/

FreeRTOS documentation: https://www.freertos.org/

Zephyr kernel documentation: https://docs.zephyrproject.org/latest/kernel/services/

Arm Cortex-M / RTOS architecture references: https://developer.arm.com/documentation/

