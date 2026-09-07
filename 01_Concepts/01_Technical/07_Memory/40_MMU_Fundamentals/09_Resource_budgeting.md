# 40.09 Resource budgeting

## Core idea

Memory is a hierarchy of storage technologies and access paths. Capacity, latency, bandwidth, power, persistence and protection vary by level, so memory architecture is a systems problem rather than a single component choice.

This is the **canonical note** for **Resource budgeting** inside **MMU Fundamentals**. Other memory notes should link here rather than copy the explanation.

## Mental model

```text
application / firmware
        ↓
objects and buffers
        ↓
allocators / mappings / caches
        ↓
memory controller / interconnect
        ↓
physical storage
```

At every layer, ask what the unit of allocation/access is, who owns it, how long it exists, and what ordering or protection rules apply.

## Mechanism

Analyze the topic in five steps:

1. Identify the memory object or region.
2. Identify the agent accessing it: CPU, DMA, peripheral, another core or kernel.
3. Identify the access path and translation/caching layers.
4. Identify ownership, visibility, alignment and protection.
5. Identify the completion/failure condition.

## Example

```text
Producer
   |
   v
[ bounded buffer ]
   |
   +--> consumer
   |
   +--> DMA / other agent
```

A working implementation must define who may write the buffer, who may read it, when ownership changes, how visibility is established and what happens when the consumer falls behind.

## Important distinctions

### Storage versus lifetime
Allocated bytes can outlive an object. Reusing storage does not make old pointers valid.

### Capacity versus bandwidth
A large memory does not imply fast memory. Capacity answers “how much”; bandwidth answers “how much per unit time.”

### Latency versus throughput
A memory system can sustain high bandwidth while having poor single-access latency.

### Coherency versus ordering
Coherency concerns whether agents see a consistent cache-line value; ordering concerns how operations become observable relative to one another.

### Protection versus safety
A protected access violation is useful only when software actually responds safely. Memory protection reduces blast radius but does not fix ownership bugs.

## Boundary cases

- zero/empty buffers;
- maximum allocation size;
- alignment boundary;
- object lifetime ending during deferred work;
- DMA completion racing with CPU reuse;
- cache-line sharing;
- memory pressure;
- power interruption during persistent writes;
- page faults or translation faults;
- ECC/parity errors.

## Failure modes

A strong root-cause statement should name the violated memory rule:

```text
symptom
  -> first incorrect memory state
  -> violating access/ownership rule
  -> missing prevention or detection
```

Examples include stale cache data, out-of-bounds writes, double release, stack exhaustion, fragmented heap, incorrect DMA ownership, wrong page attributes and race-induced corruption.

## Debugging

Collect evidence appropriate to the layer:

- address and size of the access;
- owning subsystem;
- object/buffer lifetime;
- stack pointer and stack watermark;
- allocator metadata;
- page-table/MPU attributes;
- cache state or maintenance history;
- DMA descriptor state;
- fault registers;
- trace timestamps;
- memory bandwidth/cache/TLB counters.

The first invalid access is more valuable than the final corrupted state.

## Testing

A complete memory test strategy includes:
- nominal allocations/accesses;
- boundary sizes;
- exhaustion;
- lifetime transitions;
- concurrency;
- DMA handoff;
- reset/power-loss scenarios;
- corruption/fault injection;
- performance stress.

Use static checks and sanitizers on host builds where possible, then verify hardware-specific behavior on the target.

## Performance

Measure the actual bottleneck:

```text
CPU -> cache -> TLB -> interconnect -> controller -> memory
```

A cache miss may not be a DRAM miss; a DRAM request may wait in a controller queue; a page fault can add operating-system work on top of the hardware path.

## Embedded perspective

For embedded systems, record:
- memory map;
- peak RAM;
- stack high-water marks;
- heap/pool usage;
- DMA-visible regions;
- cacheability;
- interrupt context;
- worst-case latency;
- low-power behavior;
- persistent-memory endurance.

## Design contract

Every important buffer should have a documented contract:

| Property | Required answer |
|---|---|
| Owner | Which subsystem can modify it? |
| Lifetime | When is it valid? |
| Size | What is the maximum valid range? |
| Alignment | What boundary is required? |
| Visibility | Which agents can observe writes? |
| Synchronization | Which barrier/lock/event is required? |
| Allocation | Static, pool or dynamic? |
| Failure | What happens when unavailable? |
| Recovery | How is corruption/timeout handled? |

## Staff-level review

1. What memory requirement drives the architecture?
2. What is the peak, not average, memory footprint?
3. What is the worst-case latency?
4. Where can allocation fail?
5. Which agents access the memory concurrently?
6. What makes ownership unambiguous?
7. Which properties depend on CPU/SoC/OS implementation?
8. How is corruption or exhaustion observed?
9. What happens during reset, power loss or partial failure?
10. What changes when the platform or workload scales?

## Related

- [[../01_Memory_Fundamentals/00_Chapter_Index|Memory Fundamentals]]
- [[../30_Cache_Fundamentals/00_Chapter_Index|Cache Fundamentals]]
- [[../40_MMU_Fundamentals/00_Chapter_Index|MMU Fundamentals]]
- [[../51_DMA_Memory/00_Chapter_Index|DMA and Memory Ownership]]
- [[../58_RTOS_Memory/00_Chapter_Index|RTOS Memory]]
- [[../82_Memory_Debugging/00_Chapter_Index|Memory Debugging]]
- [[../90_Staff_Memory/00_Chapter_Index|Staff-Level Memory]]

## Source backbone

- C/C++ language and standard-library memory concepts: https://en.cppreference.com/
- Embedded/CPU architecture references: https://developer.arm.com/documentation/
- OS and Linux memory concepts: https://www.kernel.org/doc/html/latest/
- General DSA/engineering cross-checks: https://www.geeksforgeeks.org/
