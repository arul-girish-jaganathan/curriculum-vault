# 05: Pointer to Structure

## Definition
A pointer to a structure (`struct T *`) holds the memory address of a structure instance. It provides the primary mechanism for pass-by-reference semantics, dynamic data management, and indirect member access in C via the arrow operator (`->`).

## Scope and Boundaries
Covers: Syntax and semantics of `->`, pointer arithmetic, alignment requirements, and strict aliasing boundaries.
Does not cover: Opaque pointers (Pimpl idiom), function pointers, or generic `void *` pointers.

## Why Does It Exist
C passes function parameters by value. Passing pointers to structures avoids copying large memory buffers, enables functions to modify caller state, and allows efficient traversal of complex graph, tree, and linked-list data structures.

## Mechanism and Language Rules
1. **Syntactic Equivalence:** The arrow operator `ptr->member` is syntactically equivalent to `(*ptr).member`.
2. **Base Address Equivalence:** A pointer to a structure points to the same memory location as its first declared member:
   `(void *)ptr == (void *)&(ptr->first_member)`.
3. **Pointer Arithmetic:** Incrementing a struct pointer (`ptr++`) advances the address by exactly `sizeof(*ptr)` bytes, automatically accounting for internal and trailing padding.
4. **Alignment Enforcement:** A `struct T *` must satisfy the alignment requirement of `struct T`, which equals the maximum alignment of any of its individual members.

## Examples
```c
#include <stdint.h>
#include <stddef.h>
#include <assert.h>

struct TelemetryFrame {
    uint32_t seq_id;
    int16_t  temperature;
    uint8_t  battery_pct;
};

static void update_telemetry(struct TelemetryFrame * const frame, int16_t new_temp) {
    /* Guard against null pointers */
    if (frame == NULL) {
        return;
    }
    /* Arrow operator cleanly accesses fields */
    frame->temperature = new_temp;
}

static void iterate_frames(struct TelemetryFrame *frames, size_t count) {
    for (size_t i = 0; i < count; ++i) {
        /* Pointer arithmetic advances by sizeof(struct TelemetryFrame) */
        (frames + i)->seq_id = (uint32_t)i;
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Null Pointer Dereference:** Dereferencing a `NULL` struct pointer (`ptr->member`) causes Undefined Behavior (on Cortex-M, triggering a HardFault or MemManage fault).
- **Misaligned Pointer Cast:** Casting an arbitrary byte address to `struct T *` and dereferencing it causes Undefined Behavior if the address violates `alignof(struct T)`.

## Edge Cases and Failure Modes
- **Strict Aliasing Violations:** Casting between unrelated structure pointers (`struct A *` to `struct B *`) and dereferencing them breaks C99 strict aliasing rules, causing aggressive compiler optimizations to emit incorrect code.
- **Dangling Pointer Access:** Accessing a struct through a pointer after its stack frame has returned or heap memory has been freed.

## Embedded Implications
- **Memory-Mapped Registers (MMIO):** Base addresses of peripheral register blocks are cast to volatile structure pointers:
  `#define UART0 ((volatile struct UART_Regs *)0x4000C000UL)`.
- **Fault Trapping:** An uninitialized struct pointer containing `0x00000000` dereferenced in bare metal without an MPU can silently corrupt the vector table at address `0x0`.

## Firmware Review Angle
- Ensure all pointer parameters are qualified with `const` if the function does not intend to mutate the target structure (`const struct T *`).
- Verify pointers cast from raw byte buffers (e.g., communication payloads) are strictly verified for proper alignment before dereferencing.

## Compiler, ABI, and Toolchain Implications
- Compilers translate `ptr->member` into a base-plus-offset load/store instruction: `LDR R1, [R0, #offset]`. If `offset` exceeds architecture immediate limits, the compiler emits extra instructions.

## Performance, Memory, Timing, and Power
- Passing pointers requires a single 32-bit/64-bit register, minimizing overhead.
- Indirection can cause CPU pipeline stalls if the pointed-to memory is not present in cache.

## Verification / Debugging
- Static analysis checks for null dereferences (`-Wnull-dereference`).
- Run with UndefinedBehaviorSanitizer (`-fsanitize=alignment,null`).

## Safety, Security, and Reliability
- MISRA C:2012 Rule 11.3: A cast shall not be performed between a pointer to object type and a pointer to a different object type.
- MISRA C:2012 Rule 18.1: A pointer resulting from arithmetic on a pointer operand shall address an element of the same array.

## Trade-offs and Alternatives
- Pointers provide speed and mutability at the cost of potential aliasing hazards and null-pointer dereferences.

## Staff-Level Takeaway
Structure pointers are the backbone of systems architecture in C. Enforce `const` correctness vigorously, validate buffer alignment before casting, and configure the MPU to trap null pointer dereferences at runtime.

## Related Concepts
- `01_Structure_layout`
- `04_Structure_assignment`
- `12_Protocol_and_register_layouts`
