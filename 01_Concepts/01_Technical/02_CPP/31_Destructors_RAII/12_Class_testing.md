# 31.12 Class testing

## Core idea

**Class testing** is a concrete part of **Destructors and RAII**. Classes combine state and behavior behind an abstraction boundary. The important engineering property is preservation of invariants across the entire object lifetime.

This note is the canonical home for this topic. Other notes should link here rather than duplicate the explanation.

## Syntax / canonical form

Start with the smallest standard form. Add complexity only after the basic form is understood.

```cpp
class Counter {
public:
    void increment() { ++value_; }
    int value() const { return value_; }

private:
    int value_{};
};
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

A compiler warning is an early diagnostic about a suspicious program property. Treating warnings as noise throws away cheap evidence. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Mechanism detail

Breakpoints and stepping show control flow but can perturb timing. In real-time systems, tracing or hardware watchpoints may be safer than interactive halts. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Design implication

Watch expressions are useful when the question is 'when does this value first become wrong?' rather than 'why did the final value look wrong?' The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Failure analysis

The call stack identifies the active chain of responsibility. Pair it with ownership and lifetime information to distinguish caller errors from callee corruption. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Portability note

Sanitizers detect broad classes of memory and undefined-behavior defects but may alter timing and are usually not substitutes for target testing. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Resource analysis

Static analysis can identify paths that tests do not exercise. Its findings still need triage against the actual language and platform contract. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Debugging evidence

A minimal reproducer is valuable because it reduces unrelated state and often changes a vague failure into a deterministic one. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Verification ideas

Root cause is the earliest violated rule that explains the failure. 'Crash in function X' is a symptom; 'object was used after lifetime ended' is a root-cause class. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Embedded scenario

Observability should be designed before the failure occurs: timestamps, state IDs, ownership IDs and fault counters can save days of field debugging. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

### Expert review

Regression tests should preserve every production failure that was important enough to debug. The bug database becomes part of the verification architecture. The specific question for **Class testing** in **31 Destructors RAII** is to make this rule explicit in the code and documentation rather than relying on convention.

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

