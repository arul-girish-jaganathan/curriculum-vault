# 03: Nested Structures

## Definition
A nested structure is a structure that contains an instance of another structure as a member. Nested structures enable hierarchical data modeling, strict encapsulation, and clean abstraction boundaries while preserving a deterministic, contiguous memory footprint.

## Scope and Boundaries
Covers: Structure containment, memory layout of nested aggregates, initialization syntax, inner member access, and the `container_of` pattern.
Does not cover: Pointers to external structures (reference containment) or anonymous nested structures (see `09_Anonymous_members`).

## Why Does It Exist
Complex systems (e.g., network stacks, device drivers, RTOS kernels) require compositional data modeling. Nested structures allow shared common headers (such as message metadata or doubly linked list nodes) to be embedded directly inside concrete payload structures.

## Mechanism and Language Rules
1. **Value Containment:** The nested structure is embedded inline by value, not by pointer. Its storage is contiguous within the outer structure.
2. **Alignment Propagation:** The outer structure inherits the alignment requirements of its strictest nested member.
3. **Compound Initialization:** Initialized using braced nested lists: `struct Outer o = { .inner = { .a = 1, .b = 2 } };`.
4. **Addressing and Invariance:** The offset of the nested structure within the parent is a compile-time constant.

## Examples
```c
#include <stddef.h>
#include <stdint.h>
#include <assert.h>

/* Intrusive linked list node pattern */
struct ListNode {
    struct ListNode *next;
    struct ListNode *prev;
};

struct SensorData {
    uint32_t timestamp;
    float reading;
    struct ListNode node; /* Nested aggregate */
};

/* The canonical container_of macro */
#define container_of(ptr, type, member)     ((type *)((char *)(ptr) - offsetof(type, member)))

static void process_node(struct ListNode *n) {
    struct SensorData *sensor = container_of(n, struct SensorData, node);
    sensor->reading = 0.0f;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Invoking `container_of` with a pointer that does not point to a valid member of an enclosing structure instance triggers Undefined Behavior upon dereference or offset calculation out of bounds.

## Edge Cases and Failure Modes
- **Initialization Truncation:** Omitting inner braces in complex nested initializers can cause accidental zero-initialization or misaligned positional assignments under older C standards.
- **Alignment Gaps:** Nesting a struct with large alignment constraints inside a loosely packed outer struct introduces internal padding before the nested aggregate.

## Embedded Implications
- **Intrusive Data Structures:** Widely used in Linux kernel, FreeRTOS, and Zephyr. Intrusive linked lists embed `ListNode` directly inside driver structs, eliminating dynamic memory allocations for list nodes.
- **Cache Locality:** Inline containment guarantees that fetching the parent struct pulls the nested header into the same L1 cache line.

## Firmware Review Angle
- Verify that `container_of` is used with verified non-null pointers.
- Check that the nested member type is completely defined before the parent structure declaration.

## Compiler, ABI, and Toolchain Implications
- ABI calling conventions treat structures containing nested structures identically to a flattened sequence of fields regarding register passing limits.

## Performance, Memory, Timing, and Power
- Inline nesting avoids pointer indirection overhead, reduces heap fragmentation, and improves CPU prefetch efficiency.

## Verification / Debugging
- GDB supports nested traversal: `print sensor.node.next`.
- Compile with `-Wmissing-braces` to catch improperly formatted nested struct initializers.

## Safety, Security, and Reliability
- Intrusive structures reduce reliance on dynamic memory allocators (`malloc`), aligning with safety standards (MISRA C:2012 Rule 21.3) that mandate static allocation in safety-critical systems.

## Trade-offs and Alternatives
- **Nesting by Value vs. Nesting by Pointer:** Nesting by value ensures zero heap overhead and single-block allocation, but couples the size of the outer struct to the inner struct.

## Staff-Level Takeaway
Use value-nested structures for intrusive containers and shared protocol headers. Master the `container_of` idiom to achieve type-safe, allocation-free polymorphism in bare-metal C.

## Related Concepts
- `01_Structure_layout`
- `05_Pointer_to_structure`
- `09_Anonymous_members`
