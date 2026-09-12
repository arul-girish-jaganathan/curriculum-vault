# 03: Dangling Pointers

## Definition
A dangling pointer is a pointer that references a memory address where the original object's lifetime has ended. Accessing or dereferencing a dangling pointer results in undefined behavior, frequently leading to silent data corruption, crashes, or severe security exploits.

## Scope and Boundaries
- **Covers:** Stack frame invalidation, pointer persistence past scope exit, and detection strategies.
- **Does not cover:** Heap use-after-free bugs ([[04_Use_after_free]]) or strict aliasing violations ([[06_Strict_aliasing]]).

## Why Does It Exist
C gives developers direct control over memory addresses without automatic garbage collection or lifetime tracking. When an object is destroyed (e.g., a stack frame pops), pointers referencing that address are not automatically nulled by the runtime.

## Mechanism and Language Rules
- **Stack Exits:** Returning the address of a local automatic variable creates a dangling pointer immediately upon function return.
- **Scope Collapse:** Storing the address of a nested block variable in an outer scope pointer causes dangling references once the inner block exits.
- **Invalidation:** C standard rules dictate that using a pointer whose referenced object has expired is undefined behavior.

## Examples
```c
#include <stdio.h>

int *gp;

void store_local(void) 
{
    int x = 100;
    gp = &x; /* gp now dangles once store_local returns */
}

int main(void) 
{
    store_local();
    /* Undefined Behavior: *gp accesses expired stack storage */
    /* printf("%d\n", *gp); */
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Reading from or writing to a dangling pointer. Even comparing dangling pointers for equality can trigger undefined behavior under strict compiler evaluations.

## Edge Cases and Failure Modes
- **Phantom Values:** Immediately after a function returns, the stack frame memory may still retain the old values, tricking developers into thinking the code works until a subsequent function call overwrites the stack.

## Embedded Implications
- **ISR Stack Corruption:** Storing pointers to local variables in interrupt callback tables creates dangling references when the originating function exits, leading to random system crashes.

## Firmware Review Angle
- **Nullify on Exit:** Enforce coding standards where pointers are immediately set to `NULL` when their referenced object's scope terminates.
- **Static Analysis:** Use compiler warnings (`-Wreturn-local-addr`) to catch stack address returns.

## Compiler, ABI, and Toolchain Implications
- **Compiler Diagnostics:** GCC and Clang emit `-Wreturn-local-addr` warnings when returning addresses of stack variables.

## Performance, Memory, Timing, and Power
- **Zero Runtime Overhead:** Preventing dangling pointers is purely a compile-time and architectural discipline with zero runtime cost.

## Verification / Debugging
- **Sanitizers:** ASan detects stack use-after-return when local frame addresses escape their scope.

## Safety, Security, and Reliability
- **Arbitrary Code Execution:** Attackers exploit dangling pointers to overwrite stack control structures (like return addresses), enabling control flow hijacking.

## Trade-offs and Alternatives
- **Safe Abstractions:** Passing ownership explicitly or returning values by copy instead of pointer eliminates dangling stack references entirely.

## Staff-Level Takeaway
Dangling pointers are ticking time bombs in C codebases. Establish rigorous code review gates to ensure pointers never outlive their target objects, and adopt the habit of nullifying pointers immediately upon object destruction.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Object_lifetime]]
- [[04_Use_after_free]]
