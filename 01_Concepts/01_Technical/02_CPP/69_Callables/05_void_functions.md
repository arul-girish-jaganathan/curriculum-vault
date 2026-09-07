# 69.05 void functions

## Core idea

**void functions** is a concrete part of **Lambdas, Function Objects and Callables**. Functions are interfaces between callers and implementations. Parameter passing, return semantics, ownership, lifetime, error policy and timing belong to the contract.

This note is the canonical home for this topic. Other notes should link here rather than duplicate the explanation.

## Syntax / canonical form

Start with the smallest standard form. Add complexity only after the basic form is understood.

```cpp
int clamp(int value, int low, int high)
{
    if (value < low) return low;
    if (value > high) return high;
    return value;
}
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

A function contract is larger than its signature. Preconditions, postconditions, ownership, lifetime, thread-safety, errors and timing can all affect callers. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Mechanism detail

Pass-by-value is not inherently expensive in modern C++. Copy elision and move semantics often make returning values efficient and easier to reason about. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Design implication

References are appropriate when the function requires an existing object; pointers can communicate nullable or optional address semantics when that is meaningful. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Failure analysis

Default arguments live at the call interface and should therefore be treated as API design rather than hidden implementation detail. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Portability note

Overloads should form a coherent family. Ambiguous conversions are a design smell even when the compiler can technically resolve some calls. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Resource analysis

Inline is not an execution guarantee. Compiler heuristics, optimization level and code-generation constraints determine whether a call is actually inlined. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Debugging evidence

Recursive functions trade simple expression for stack depth. Embedded use requires a proof or bound for maximum recursion depth. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Verification ideas

Function pointers and lambdas create callbacks whose lifetime and invocation context must be documented. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Embedded scenario

Exception specifications and error returns change the control-flow contract. Callers need to know whether an operation can fail or block. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

### Expert review

Testing should exercise both function result and contract boundaries, including invalid input, partial failure and repeated lifecycle transitions. The specific question for **void functions** in **69 Callables** is to make this rule explicit in the code and documentation rather than relying on convention.

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

