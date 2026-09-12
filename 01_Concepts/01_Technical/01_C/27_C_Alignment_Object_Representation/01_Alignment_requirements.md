# 01: Alignment Requirements

## Definition
Alignment requirements dictate the memory addresses at which objects of a given type can be stored. An alignment is an integer value (always a power of two) representing the number of bytes between successive valid memory addresses for an object type. If an object's memory address is a multiple of its alignment requirement, it is considered properly aligned.

## Scope and Boundaries
- **Covers:** Fundamental alignment, hardware address constraints, unaligned access faults, and performance penalties.
- **Does not cover:** Explicit alignment forcing ([[03_Alignas]]), operator querying ([[02_Alignof]]), or dynamic memory allocation alignment ([[../25_C_Dynamic_Memory/05_Alignment_guarantees]]).

## Why Does It Exist
Hardware architectures are optimized to access memory in aligned words (e.g., 4 bytes on 32-bit buses, 8 bytes on 64-bit buses):
- **Bus Efficiency:** A 64-bit CPU reads a double-word in a single memory bus cycle if aligned to an 8-byte boundary.
- **Hardware Faults:** Strict alignment architectures (ARM Cortex-M0/M3 unaligned traps, SPARC, MIPS) raise hardware bus faults (HardFault) or alignment exceptions upon unaligned load/store operations.
- **Performance:** On architectures permitting unaligned access (x86_64), unaligned loads can cross cache line boundaries, causing severe performance penalties and microcode assistance stalls.

## Mechanism and Language Rules
- **Fundamental Alignment:** ISO C guarantees that every complete object type has a fundamental alignment requirement supported by the target ABI (e.g., `_Alignof(char)` is 1, `_Alignof(int)` is typically 4, `_Alignof(double)` is 4 or 8).
- **Strict Alignment:** An address `p` is strictly aligned to alignment `A` if `(uintptr_t)p % A == 0`.
- **Unaligned Access Prohibition:** Dereferencing an unaligned pointer resulting from an improper cast (`(int *)char_ptr`) violates alignment constraints and triggers undefined behavior.

## Examples
```c
#include <stdio.h>
#include <stdalign.h>
#include <stdint.h>

struct unaligned_trap_demo {
    char a;       /* Alignment: 1, Size: 1 */
    int b;        /* Alignment: 4, Size: 4 (Requires 3 bytes padding before b) */
};

int main(void) 
{
    struct unaligned_trap_demo demo;
    
    printf("Address of struct: %p\n", (void *)&demo);
    printf("Address of char a: %p\n", (void *)&demo.a);
    printf("Address of int b:  %p\n", (void *)&demo.b);
    
    /* Checking strict alignment manually */
    uintptr_t b_addr = (uintptr_t)&demo.b;
    if (b_addr % _Alignof(int) == 0) {
        printf("Member b is properly aligned.\n");
    } else {
        printf("Member b is unaligned!\n");
    }
    
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Dereferencing a pointer that does not meet the target type's alignment requirements is undefined behavior.
- **Implementation-Defined:** The exact fundamental alignment values for standard types (e.g., whether `long double` requires 8, 12, or 16-byte alignment) are implementation-defined.

## Edge Cases and Failure Modes
- **Packed Struct Casts:** Casting an unaligned buffer (e.g., network packet payload) directly to a complex struct pointer (`struct header *h = (struct header *)buf;`) causes unaligned access faults on embedded microcontrollers.
- **Pointer Arithmetic Traps:** Advancing a `char *` by 1 and casting to `uint32_t *` creates an unaligned 32-bit pointer.

## Embedded Implications
- **Cortex-M Faults:** On ARM Cortex-M3/M4/M7 cores, unaligned word/half-word accesses can be enabled, but unaligned multi-word `LDM`/`STM` instructions or unaligned bitband operations fault immediately. Cortex-M0 faults on any unaligned access by default.
- **DMA Alignment:** DMA controllers require strict source and destination alignment matching bus widths.

## Firmware Review Angle
- **Audit Raw Casts:** Flag all casts from generic buffers (`uint8_t *` or `void *`) to typed pointers (`uint32_t *`, `struct foo *`).
- **Check Struct Layouts:** Verify that structure members are naturally aligned to avoid accidental unaligned member access.

## Compiler, ABI, and Toolchain Implications
- **ABI Rules:** The processor ABI defines the minimum alignment for every primitive type. Compilers automatically insert padding bytes into structures to satisfy ABI alignment rules.

## Performance, Memory, Timing, and Power
- **Bus Cycles:** Properly aligned accesses complete in a single bus cycle. Unaligned accesses require split bus transactions or trap handling, multiplying execution latency.

## Verification / Debugging
- **Compiler Flags:** Enable `-Wcast-align` to catch unsafe pointer alignment casts at compile time.
- **Sanitizers:** Use UndefinedBehaviorSanitizer (`-fsanitize=undefined`) to catch runtime alignment faults instantly.

## Safety, Security, and Reliability
- **Safety Critical Standards:** MISRA C:2012 Rule 11.3 forbids casts between a pointer to object type and a pointer to a different object type that violates alignment.
- **Reliability:** Alignment errors cause silent memory corruption or hard system crashes in field deployments.

## Trade-offs and Alternatives
- **Unaligned Access vs. Safe Copying:** Use `memcpy` to copy unaligned byte streams into local typed variables; `memcpy` compiles into highly efficient unaligned load/store sequences on modern CPUs without violating C strict aliasing or alignment rules.

## Staff-Level Takeaway
Alignment requirements are physical contracts between software data structures and computer memory hardware buses. Violating these contracts results in performance degradation on desktop CPUs and fatal hardware exceptions on embedded microcontrollers. Always treat memory alignment as a first-class architectural concern.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_Alignof]]
- [[03_Alignas]]
- [[10_DMA_alignment]]
- [[12_ABI_and_packing]]
