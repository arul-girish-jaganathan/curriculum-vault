# 16: C Struct, Union, Enum — Chapter Index

## Definition
This chapter explores aggregate and scalar composite types in C: structures (`struct`), unions (`union`), and enumerations (`enum`). In systems and bare-metal embedded programming, these constructs form the cornerstone of hardware register mapping, wire/packet protocol serialization, state machine modeling, and memory abstraction.

## Scope and Boundaries
Covers: Memory layout, alignment, padding, member access, nested structures, shallow vs deep copying, flexible array members (FAMs), type punning, active union members, anonymous structs/unions (C11), enum underlying types, ABI implications, register mapping, and MISRA C compliance.
Does not cover: C++ classes/inheritance, dynamic memory management internals (`malloc` implementations), or bitwise operations outside bitfields.

## Topics in This Chapter
1. `01_Structure_layout.md`: Alignment requirements, natural alignment, internal/trailing padding, `sizeof`, and `offsetof`.
2. `02_Structure_members.md`: Member syntax, incomplete types, bitfields, storage boundaries, and sign extension traps.
3. `03_Nested_structures.md`: Composition, memory containment, inner address calculation, and container-of idioms.
4. `04_Structure_assignment.md`: Value semantics, memberwise/bitwise copy (`memcpy`), shallow copying, and traps with embedded pointers.
5. `05_Pointer_to_structure.md`: Member access operator (`->`), pointer offsets, indirect mutation, and alignment constraints.
6. `06_Flexible_array_members.md`: C99 flexible array members (`type arr[]`), struct sizing, allocation patterns, and safety constraints.
7. `07_Union_representation.md`: Overlapping memory, maximum member sizing, common initial sequences, and representation layout.
8. `08_Union_active_member_rules.md`: ISO C active member rules, strict aliasing, type punning validity across C99/C11, and GCC extensions.
9. `09_Anonymous_members.md`: C11 anonymous structures and unions, planar field lifting, namespacing, and hardware register overlay idioms.
10. `10_Enumerations.md`: Enum syntax, enumeration constants (`int` type in C), scope, and state machine design.
11. `11_Enum_portability.md`: Underlying integer types, compiler flags (`-fshort-enums`), ABI incompatibility, and fixed-width enum strategies.
12. `12_Protocol_and_register_layouts.md`: Hardware memory-mapped I/O (MMIO), packed structs (`__attribute__((packed))`), endianness, and volatile qualifications.

## Staff-Level Takeaway
Structures and unions define the physical interface between software abstractions and physical memory/hardware buses. Never assume layout or alignment without explicit static assertions (`_Static_assert`) and toolchain-level verification.

## Related Concepts
- `../00_Complete_Topic_Map`
- `01_Structure_layout`
- `07_Union_representation`
- `10_Enumerations`
- `12_Protocol_and_register_layouts`
