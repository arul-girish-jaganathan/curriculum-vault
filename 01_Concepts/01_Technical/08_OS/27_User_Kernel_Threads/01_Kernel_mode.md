# 27.01 Kernel mode

## Core idea

The kernel is the privileged core that manages hardware resources and mediates protected operations. User programs cross into kernel services through defined interfaces such as system calls.

This is the canonical note for **Kernel mode** inside **User-Level and Kernel-Level Threads**. Other OS notes should link here rather than copy the explanation.

## Mental model

```text
application -> OS abstraction -> kernel mechanism -> hardware resource
```

## Mechanism

Understand the feature by tracing:

```text
request/event
    ↓
OS state transition
    ↓
resource operation
    ↓
scheduler / memory / I/O interaction
    ↓
completion or failure
```

For **Kernel mode**, identify the exact state stored by the kernel, who can change it, what event causes progress, and what other subsystem must cooperate.

## What to know

### Semantics
State the API or operating-system guarantee precisely. Do not confuse “usually implemented this way” with “required by the OS contract.”

### State
Draw the important structures and transitions. For process/scheduler features, identify queues and runnable states. For memory, identify mappings and permissions. For filesystems, identify metadata and block ownership. For synchronization, identify the protected invariant.

### Complexity and cost
Record:
- operation latency;
- memory overhead;
- scheduler/context-switch cost;
- cache/TLB effects;
- I/O amplification;
- contention;
- scaling with process/thread count.

### Failure modes
Check:
- invalid parameters;
- resource exhaustion;
- timeout or blocked execution;
- stale handles;
- deadlock/race;
- memory pressure;
- device failure;
- crash/reboot during an update;
- permission/security violation.

### Debugging

Start from the first observable state violation.

Useful evidence includes:
- process/thread states;
- scheduler traces;
- system-call tracing;
- core dumps;
- page-fault data;
- memory maps;
- lock/queue state;
- I/O traces;
- filesystem metadata;
- hardware counters;
- kernel logs.

### Testing

Use:
1. normal functional cases;
2. boundary/resource-exhaustion cases;
3. concurrent/interleaving cases;
4. fault-injection cases;
5. long-duration/stress cases;
6. performance regression measurements.

### Embedded/systems perspective

For embedded Linux or firmware-adjacent systems, ask whether the mechanism can block, allocate, sleep, depend on virtual memory, depend on cache coherency, or introduce unbounded recovery work.

### Staff-level review

- What requirement justifies this OS mechanism?
- What is the simpler alternative?
- Where is the state stored?
- Who owns the resource?
- What is the worst-case latency?
- What happens under resource exhaustion?
- What kernel/hardware assumptions are being made?
- How is the behavior observed in production?
- What changes on a different architecture or OS implementation?


## Engineering distinctions

Keep these layers separate:

1. **OS contract** — what the operating system API and semantics guarantee.
2. **Kernel implementation** — scheduler structures, locks, caches, page allocators and internal data paths.
3. **Hardware behavior** — MMU/TLB/cache/CPU/I/O device behavior.
4. **Configuration and policy** — priorities, limits, security policy, filesystem mount options, cgroups/quotas, and product choices.

## Complete reasoning checklist

- What state does the mechanism own?
- Which execution context can access it?
- What blocks or wakes execution?
- What memory is allocated and who owns it?
- What happens on failure?
- What is the worst-case latency?
- Which parts depend on the kernel, architecture or device?
- How will production behavior be observed?


## Related

- [[../01_OS_Foundations/00_Chapter_Index|OS Foundations]]
- [[../09_Processes/00_Chapter_Index|Processes]]
- [[../15_Process_Scheduling/00_Chapter_Index|Process Scheduling]]
- [[../49_Memory_Management/00_Chapter_Index|Memory Management]]
- [[../67_File_Systems/00_Chapter_Index|File Systems]]
- [[../80_IO_System/00_Chapter_Index|I/O System]]
- [[../85_Security/00_Chapter_Index|Security]]
- [[../90_Staff_OS/00_Chapter_Index|Staff-Level OS]]

## Source backbone

Primary organization: GeeksforGeeks Operating Systems Tutorial and related OS articles.

https://www.geeksforgeeks.org/operating-systems/operating-systems/
