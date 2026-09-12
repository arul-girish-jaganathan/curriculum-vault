# 01: Object Lifetime

## Definition
Object lifetime in ISO C is the portion of program execution during which storage is guaranteed to be reserved for a specific object. An object begins its lifetime when it is allocated or its storage is initialized, and its lifetime ends when its storage is deallocated, reused, or its enclosing scope exits.

## Scope and Boundaries
- **Covers:** Object creation, activation, lifetime boundaries, storage reuse, and scope termination.
- **Does not cover:** Storage duration categories ([[02_Storage_duration]]), heap allocation functions ([[../25_C_Dynamic_Memory/01_malloc]]), or strict aliasing rules ([[06_Strict_aliasing]]).

## Why Does It Exist
The C memory model requires explicit bounds on when an object exists so that:
- **Storage Reuse:** The compiler and memory manager can safely recycle memory blocks previously assigned to dead variables or freed allocations.
- **Optimization Guarantees:** Compilers can track whether values can change or remain constant based on whether an active object exists at a given memory address.
- **Safety Verification:** Establishing strict boundaries prevents programs from inspecting or modifying memory when no valid object occupies it.

## Mechanism and Language Rules
- **Beginning of Lifetime:** An object's lifetime begins when storage is obtained and any initializers associated with the declaration are evaluated.
- **End of Lifetime:**
  - Automatic objects: End when execution leaves their enclosing block scope.
  - Allocated objects: End when explicitly passed to `free()` or `realloc()`.
  - Static/Thread objects: End when program or thread execution terminates.
- **Storage Reuse:** Once an object's lifetime ends, any pointer that pointed to the old object becomes a dangling pointer. If new storage is allocated at the same address, a new object begins its lifetime, but old pointers do not automatically bind to it unless updated.

## Examples
```c
#include <stdio.h>

int *get_dangling_ptr(void) 
{
    int local_var = 42;
    return &local_var; /* ERROR: local_var lifetime ends when function exits */
}

int main(void) 
{
    int *ptr = get_dangling_ptr();
    /* Undefined Behavior: accessing memory outside object lifetime */
    /* printf("Value: %d\n", *ptr); */
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Accessing the value of an object outside its lifetime (before it begins or after it ends) is undefined behavior.
- **Indeterminate Values:** Accessing an automatic object before its initializer is evaluated yields an indeterminate value.

## Edge Cases and Failure Modes
- **Returning Stack Addresses:** Returning pointers to automatic variables is a classic lifetime bug.
- **Storage Overlap:** Writing into memory after an object's lifetime has ended can corrupt newly created objects occupying the same stack frame or heap slot.

## Embedded Implications
- **ISR Stack Frames:** Interrupt service routines operating on stack frames must complete before the interrupted task exits its scope, preventing lifetime mismatch issues.
- **Hardware Register Mapping:** Volatile memory mapped registers have unique lifetime semantics managed by hardware rather than C storage rules.

## Firmware Review Angle
- **Inspect Return Paths:** Verify that functions never return pointers to automatic (stack-allocated) variables.
- **Audit Pointer Reuse:** Ensure pointers are reset to `NULL` immediately after object destruction or deallocation.

## Compiler, ABI, and Toolchain Implications
- **Register Allocation:** Compilers reuse stack slots and registers aggressively once an object's lifetime ends.
- **Lifetime Markers:** Modern compilers emit dwarf lifetime debug info (`llvm.lifetime.start`/`end`) to optimize stack frame size.

## Performance, Memory, Timing, and Power
- **Automatic Cleanup:** Automatic objects incur zero runtime deallocation overhead because stack pointer adjustment reclaims them instantly.

## Verification / Debugging
- **AddressSanitizer (ASan):** Detects stack-use-after-scope and heap-use-after-free bugs by poisoning memory outside valid object lifetimes.

## Safety, Security, and Reliability
- **Information Leakage:** Dead stack frames retaining sensitive cryptographic keys or passwords can leak information if accessed via stale pointers.

## Trade-offs and Alternatives
- **Automatic vs. Dynamic:** Automatic storage provides speed and zero overhead but restricted lifetime; dynamic storage provides extended lifetime at the cost of manual management.

## Staff-Level Takeaway
An object's lifetime is an inviolable contract with the compiler. Once an object's lifetime ends, the memory address is merely raw bytes. Treat expired pointers as toxic; any dereference after lifetime expiration triggers undefined behavior.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_Storage_duration]]
- [[03_Dangling_pointers]]
- [[04_Use_after_free]]
