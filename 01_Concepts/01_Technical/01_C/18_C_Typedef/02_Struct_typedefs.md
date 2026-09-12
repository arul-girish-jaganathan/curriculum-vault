# 02: Struct Typedefs

## Definition
Struct typedefs pair a structure declaration with a type alias, allowing developers to use the alias directly without repeatedly typing the `struct` elaboration tag. C supports several idiom variations: named tags with aliases, anonymous struct typedefs, and forward-declared self-referential structures.

## Scope and Boundaries
Covers: Named vs anonymous struct typedefs, self-referential pointer members (linked lists, trees), forward declarations, and namespace partitioning.
Does not cover: Opaque pointers (see `03_Opaque_typedefs`) or flexible array member specifics (see `16_C_Struct_Union_Enum/06_Flexible_array_members`).

## Why Does It Exist
In C, structure tags reside in their own tag namespace (`struct TagName`), distinct from the ordinary identifier namespace. Without a `typedef`, declaring a structure variable requires writing `struct TagName instance;`. A struct typedef bridges the tag into the ordinary namespace for clean, concise typing.

## Mechanism and Language Rules
1. **Namespace Independence:** The tag namespace (`tags`) and ordinary identifier namespace (`identifiers`) do not collide. Therefore:
   `typedef struct Node Node;` is completely valid and idiomatic.
2. **Anonymous Struct Typedef:** Omitting the tag (`typedef struct { int x; } Point;`) is legal, but prevents forward-declaring the type or creating self-referential pointer members.
3. **Self-Reference Rule:** Inside a structure definition, the typedef name does not exist yet until the declaration closes. Self-referencing members must use the struct tag:
   ```c
   typedef struct Node {
       struct Node *next; /* Valid */
       // Node *prev;     /* ERROR: Node identifier not yet declared */
   } Node;
   ```
4. **C11 Benign Redefinition:** Defining `typedef struct Foo Foo;` across multiple headers is valid in C11 onwards, provided the underlying definition is identical.

## Examples
```c
#include <stddef.h>

/* Recommended: Explicit tag AND matching typedef name */
typedef struct QueueNode {
    struct QueueNode *next; /* Self-reference requires struct tag */
    void *payload;
} QueueNode;

/* Forward declaration for circular references */
typedef struct Task Task;
typedef struct Scheduler Scheduler;

struct Task {
    Scheduler *parent;
    uint32_t   priority;
};

struct Scheduler {
    Task      *current_task;
    uint32_t   task_count;
};
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Anonymous Struct Tag Synthesis:** Compilers synthesize an internal implementation-defined tag name for anonymous structs in DWARF symbols, which can hinder debugging or make forward declaration impossible.

## Edge Cases and Failure Modes
- **Anonymous Struct Forward-Declaration Trap:** An anonymous struct typedef (`typedef struct { ... } Event_t;`) cannot be forward-declared in header files. Any header requiring `Event_t` must include the entire definition.
- **Recursive Typedef Failure:** Attempting to reference the typedef alias inside the structure body before the closing brace causes a compile-time syntax error.

## Embedded Implications
- **Header Coupling:** Anonymous struct typedefs force full struct declarations into public headers, increasing compilation times, exposing private layout details, and bloating rebuild trees across large embedded projects.

## Firmware Review Angle
- Enforce the rule: **Always provide a struct tag matching the typedef alias** (`typedef struct Node Node;`). Avoid anonymous struct typedefs for non-trivial types.
- Check that self-referencing pointers use the struct tag name rather than macro workarounds.

## Compiler, ABI, and Toolchain Implications
- Struct tags and typedefs are purely front-end compile-time abstractions; they produce identical machine code and memory layouts.

## Performance, Memory, Timing, and Power
- No performance or memory impact.

## Verification / Debugging
- Anonymous structs often appear in GDB as `type = struct {...}` or `type = ._anon_0`, making stack traces and memory dumps harder to read compared to explicitly tagged structs (`struct QueueNode`).

## Safety, Security, and Reliability
- MISRA C:2012 Rule 5.7: A tag name shall be a unique identifier across the translation unit.
- Explicit tagging allows static analyzers to track type identity deterministically across compilation units.

## Trade-offs and Alternatives
- **Tagged Struct vs. Anonymous Typedef:** Tagged structs take a few more characters to declare initially, but allow forward declarations, self-references, and clear debugger inspection.

## Staff-Level Takeaway
Never use anonymous struct typedefs in production headers. Always declare structures with explicit tags matching their typedef names (`typedef struct Device Driver DeviceDriver;`). This guarantees support for forward declarations, clean self-reference, and readable debugger call stacks.

## Related Concepts
- `01_Basic_typedefs`
- `03_Opaque_typedefs`
- `../16_C_Struct_Union_Enum/01_Structure_layout`
