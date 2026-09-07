# 61.12 Embedded suitability

## Core idea

**Embedded suitability** is a concrete part of **Iterators and Iterator Categories**. Containers define storage and access policy. Size, capacity, locality, allocation and invalidation rules are as important as the member-function names.

This note is the canonical home for this topic. Other notes should link here rather than duplicate the explanation.

## Syntax / canonical form

Start with the smallest standard form. Add complexity only after the basic form is understood.

```cpp
std::vector<int> values{3, 1, 2};
std::sort(values.begin(), values.end());
```

## Mechanism

Reason about the topic in this sequence:

```text
source construct
    ↓
type / overload / template selection
    ↓
object or program state
    ↓
library / compiler operation
    ↓
observable result
```

Do not confuse the abstract C++ rule with one compiler's generated implementation.

## What can go wrong

The common failures are hidden assumptions:
- lifetime shorter than the use;
- implicit conversion changes the value or overload;
- allocation occurs where the caller expected none;
- a container operation invalidates retained addresses;
- shared state is accessed without the required synchronization;
- the code relies on an implementation or ABI detail as though it were portable.

## Boundary cases

Check empty inputs, minimum and maximum values, failed operations, object destruction, repeated use, concurrent use where applicable, and platform changes.

For resource-bearing features, also check what happens during partial initialization and cleanup.

## Debugging

Find the **first violated invariant**, not the last visible symptom.

Useful evidence includes compiler diagnostics, debugger state, call stacks, memory inspection, sanitizer reports, traces and generated assembly. Reproduce the defect with the smallest input that still demonstrates it.

## Testing

A useful test set contains:

1. Normal valid use.
2. Boundary values and transitions.
3. Invalid or failure cases.
4. Repeated use and lifecycle transitions.
5. Compile-time checks when the property is static.
6. Target-level verification when the CPU, ABI, timing or hardware changes the behavior.

## Performance and resources

Measure the resource that matters:
- CPU time or cycles;
- code size;
- RAM;
- stack;
- allocations;
- cache behavior;
- lock hold time;
- worst-case latency.

The existence of a convenient abstraction does not prove that it has no runtime cost.

## Embedded interpretation

For embedded systems ask:

**Context:** Can this execute in startup, task, worker or ISR context?

**Memory:** Is storage static, stack-based or dynamically allocated? What alignment is required?

**Timing:** Can it block, allocate, retry or scale with input size?

**Hardware:** Does correctness depend on cache, MMIO, DMA, endianess or ABI behavior?

**Recovery:** What is the safe behavior when the operation fails after the system has already changed state?

## Design contract

Document:
- preconditions;
- postconditions;
- ownership;
- lifetime;
- error behavior;
- concurrency assumptions;
- blocking behavior;
- allocation behavior;
- observability.

## Staff-level questions

1. What requirement makes this mechanism necessary?
2. What is the simplest alternative?
3. Which parts are guaranteed by standard C++?
4. Which parts depend on compiler, ABI or target?
5. What is the worst failure mode?
6. What is the worst-case resource cost?
7. How would the design change if the target or compiler changed?
8. What evidence proves the implementation is correct?

## Related

- [[../90_Staff_Level_Cpp/00_Chapter_Index|Staff-Level C++]]
- [[../89_Performance_Safety/00_Chapter_Index|Performance, Safety and Verification]]
- [[../88_Embedded_Cpp/00_Chapter_Index|Embedded C++]]

## Source backbone

Primary curriculum: LearnCpp.com — https://www.learncpp.com/

Supplementary breadth: GeeksforGeeks C++ — https://www.geeksforgeeks.org/cpp/c-plus-plus/

This note is original study material organized from those curricula, not a verbatim copy.

## Deep Study

### Semantic boundary

Embedded C++ has a smaller margin for hidden work. Allocation, locking, virtual dispatch, formatting and library calls should be treated as explicit resource decisions. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Mechanism detail

Interrupt context changes the legal operation set. Blocking, unbounded loops and many library abstractions are inappropriate in an ISR. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Design implication

DMA means the device can access memory without the CPU executing an instruction for each transfer. Ownership and visibility therefore cross a hardware boundary. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Failure analysis

volatile is useful for certain observable hardware accesses but is not a replacement for synchronization between threads and is not a universal memory barrier. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Portability note

Memory placement can be part of correctness. Vectors, boot metadata, calibration data, DMA buffers and application sections may have linker-defined regions. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Resource analysis

Worst-case timing matters more than average timing for deadline-driven firmware. Analyze retries, lock contention, cache misses and variable-length processing. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Debugging evidence

Fixed-capacity data structures make memory budgets explicit and can eliminate fragmentation. Their APIs should expose what happens when capacity is exhausted. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Verification ideas

Safety-critical code benefits when the language feature, coding rule, static analysis rule and test evidence all point to the same invariant. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Embedded scenario

Hardware abstraction should isolate register layout and access policy from business logic so simulation and host tests can exercise higher layers. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Expert review

Field failures need observability that survives deployment: reset reason, fault code, state-machine state, recent events and bounded diagnostic history are often more useful than verbose logs. The specific question for **Embedded suitability** in **61 Iterators** is to make this rule explicit in the code and documentation rather than relying on convention.

### Extended worked case

```cpp
struct SubsystemState
{
    std::uint32_t value{};
    bool valid{};
};

SubsystemState state{};
state.value = 10;
state.valid = true;
```

Take this small state object and apply the topic under study. Ask what changes if the object is copied, moved, referenced, shared, destroyed early, accessed concurrently, or placed behind a module boundary. This exercise is deliberately generic: the answer depends on the concrete topic and is where the topic's real rules must be applied.

### Practical checklist

- What is guaranteed by the C++ standard?
- What comes from the standard library?
- What comes from the compiler or ABI?
- What comes from the target hardware or OS?
- What must remain true before and after the operation?
- Who owns the relevant state?
- What is the lifetime?
- Can the operation fail?
- Can it allocate or block?
- What evidence proves the chosen implementation is correct?

