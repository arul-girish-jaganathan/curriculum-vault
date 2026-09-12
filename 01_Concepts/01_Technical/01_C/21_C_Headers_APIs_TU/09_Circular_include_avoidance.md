# 09: Circular Include Avoidance

## Definition
Circular inclusion occurs when two or more header files include each other directly or transitively (e.g., `a.h` includes `b.h`, which includes `a.h`). While include guards prevent infinite preprocessor recursion, circular includes cause premature evaluation failures where struct tags and typedefs are referenced before they have been declared.

## Scope and Boundaries
Covers: Mutual dependencies, incomplete structure forward declarations, tag vs. typedef decoupling, and architectural refactoring.
Does not cover: Linker circular symbol resolution.

## Why Does It Exist
Real-world domain models frequently contain bidirectional relationships: a `Task` owns a `Timer`, and a `Timer` triggers a `Task`. If both header files include each other to access concrete struct layouts, the include guard of the first header terminates inclusion before types are declared, causing compile-time syntax errors.

## Mechanism and Language Rules
1. **Forward Declaration of Struct Tags:** A pointer to a structure does NOT require the structure's full definition:
   `struct Task;` forward-declares `struct Task` as an incomplete type.
2. **Pointer Independence:** `sizeof(struct Task*)` is known to the compiler (4 or 8 bytes) regardless of the members inside `struct Task`.
3. **Decoupling Rule:** Use forward declarations in headers whenever pointers are sufficient; move `#include` directives to implementation `.c` files.

## Examples
```c
/* ================= BROKEN: Circular Include Deadlock ================= */
/* task.h */
#include "timer.h"
typedef struct { Timer_t *timer; } Task_t;

/* timer.h */
#include "task.h"
typedef struct { Task_t *task; } Timer_t;
/* Whichever file is included first fails because the other's typedef isn't ready! */

/* ================= RESOLVED: Forward Tag Declarations ================ */
/* task.h */
#ifndef TASK_H
#define TASK_H

/* Forward declaration of incomplete struct tag */
struct Timer;

typedef struct Task {
    struct Timer *timer; /* Pointer to incomplete tag is 100% legal */
    uint32_t      priority;
} Task_t;

#endif /* TASK_H */

/* timer.h */
#ifndef TIMER_H
#define TIMER_H

struct Task; /* Forward declaration */

typedef struct Timer {
    struct Task *owner_task;
    uint32_t     timeout_ms;
} Timer_t;

#endif /* TIMER_H */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Attempting to evaluate `sizeof` or access members of a forward-declared incomplete struct before its definition is a compile-time constraint violation.

## Edge Cases and Failure Modes
- **Typedef Forward Declaration Trap:** Prior to C11, forward-declaring a typedef alias twice caused compilation failure. In modern C11, benign typedef redefinitions are permitted: `typedef struct Task Task;`.
- **Value Containment:** Forward declarations ONLY work for pointers (`struct T *`). If a struct embeds another struct *by value* (`struct T val;`), the full definition MUST be included.

## Embedded Implications
- Intrusive data structures (e.g., FreeRTOS `TCB_t` and `ListItem_t`) use forward struct tag declarations extensively to maintain mutual references without header deadlock.

## Firmware Review Angle
- When circular dependencies appear, immediately check: Can `#include "other.h"` in the header be replaced with `struct Other;`?
- Reserve concrete `#include` directives for the `.c` implementation files where members are dereferenced.

## Compiler, ABI, and Toolchain Implications
- Forward declarations keep compilation units isolated and reduce the preprocessor token load across large build trees.

## Performance, Memory, Timing, and Power
- Zero runtime impact.

## Verification / Debugging
- GCC/Clang emit `"error: unknown type name"` or `"error: field has incomplete type"` when circular include deadlocks occur.

## Safety, Security, and Reliability
- Clean, acyclic header structures eliminate compiler warning cascades and improve static analyzer accuracy.

## Trade-offs and Alternatives
- **Forward Declaration vs Common Types Header:** If multiple headers share common types, extract the shared types into a standalone `types.h` header included by both.

## Staff-Level Takeaway
Never let headers deadlock in circular includes. If a header only uses pointers to an external struct, forward-declare the tag (`struct Foo;`) and defer the `#include` to the `.c` file. For shared types, extract them into an independent lower-level header.

## Related Concepts
- `03_Include_guards`
- `07_Header_self_sufficiency`
- `08_Dependency_direction`
