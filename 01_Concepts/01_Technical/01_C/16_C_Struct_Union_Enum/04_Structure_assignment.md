# 04: Structure Assignment

## Definition
Structure assignment is the direct copying of an entire structure's value to another structure of the exact same type using the assignment operator (`=`). ISO C defines this operation as a memberwise shallow copy equivalent to a raw memory copy (`memcpy`) across the size of the structure.

## Scope and Boundaries
Covers: Assignment semantics (`a = b`), parameter passing by value, function return by value, and shallow copy mechanics.
Does not cover: Deep copying of referenced pointer targets or custom assignment operators (which C does not support).

## Why Does It Exist
Before C gained structure assignment in early standardization, programmers were forced to manually copy fields or invoke `memcpy`. Direct assignment enables concise, type-safe value propagation and simplifies immutable data passing.

## Mechanism and Language Rules
1. **Type Identity:** The left-hand and right-hand operands must possess the exact same unqualified structure type.
2. **Shallow Copy:** All members, including pointers and arrays embedded in the struct, are copied by value. For pointer members, only the memory address is copied—not the pointed-to object.
3. **Padding Invariance:** Whether structure assignment copies uninitialized padding bytes is unspecified by ISO C. Compilers frequently emit word-sized block copies (`LDRM`/`STRM` or `memcpy`) that overwrite padding.

## Examples
```c
#include <stdint.h>
#include <assert.h>

struct Vector3D {
    float x;
    float y;
    float z;
};

struct Packet {
    uint32_t id;
    uint8_t *payload; /* Pointer member: shallow copy liability */
};

static void test_assignment(void) {
    struct Vector3D a = {1.0f, 2.0f, 3.0f};
    struct Vector3D b;
    b = a; /* Pure value copy: safe */
    assert(b.y == 2.0f);

    uint8_t buffer[16] = {0};
    struct Packet p1 = { .id = 1, .payload = buffer };
    struct Packet p2;
    p2 = p1; /* Shallow copy: p2.payload points to the same buffer */
    p2.payload[0] = 0xAA;
    assert(p1.payload[0] == 0xAA); /* Side-effect aliasing */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Overlapping Assignment:** Assigning a structure to itself (`s = s;`) is valid, but assigning between overlapping structures via pointers without identical types invokes Undefined Behavior.
- **Padding Mutation:** Compilers may or may not preserve padding byte values during structure assignment.

## Edge Cases and Failure Modes
- **Dangling Pointers / Double Free:** If a structure owning dynamically allocated memory is assigned to another variable, both instances point to the same memory. Freeing both leads to a double-free security vulnerability (CWE-415).
- **Hidden Pass-by-Value Overhead:** Passing large structures to functions by value silently triggers expensive stack allocation and block memory copying.

## Embedded Implications
- **Stack Overflow:** Large structure value assignments or passing large structures by value on an MCU with an 8KB stack can trigger instant silent stack overflow and hard faults.
- **DMA Register Overwrite:** Assigning a structure directly to a dereferenced MMIO pointer can generate non-atomic unaligned byte writes that violate peripheral bus width requirements.

## Firmware Review Angle
- Flag any structure assignment or pass-by-value where `sizeof(struct) > 16` bytes. Pass by `const struct *` instead.
- Audit structures containing pointer members to ensure that copies are either explicitly managed (deep copy) or forbidden by API design.

## Compiler, ABI, and Toolchain Implications
- ABI conventions (such as ARM AAPCS) dictate that structs up to 4 words (16 bytes) are returned in core registers (`R0-R3`). Structs larger than 16 bytes are returned via a hidden pointer passed in `R0`, writing directly to the caller's stack frame.

## Performance, Memory, Timing, and Power
- Small struct assignment (<= 16 bytes) optimizes into 2 to 4 register moves.
- Large struct assignment compiles to `memcpy`, adding call overhead, instruction cache pollution, and CPU execution cycles.

## Verification / Debugging
- Static analysis flags functions returning large structures by value.
- Inspect disassembly to confirm if the compiler optimized a copy or generated a full `memcpy` call.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 12.1 and Rule 17.8 advise caution regarding side effects during expression evaluation and pass-by-reference preferences for large objects.

## Trade-offs and Alternatives
- **Pass-by-Value vs. Pass-by-Pointer-to-Const:** Passing `const T *` avoids copying and protects stack depth, but introduces a pointer indirection and potential aliasing overhead.

## Staff-Level Takeaway
Treat structure assignment as a fast, shallow memory blit. Never use value semantics for structures that own resources (pointers, file handles, DMA buffers). Enforce `const T *` parameters across all architectural APIs for structures larger than 16 bytes.

## Related Concepts
- `01_Structure_layout`
- `05_Pointer_to_structure`
