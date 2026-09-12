# 21: C Headers, APIs, and Translation Units — Chapter Index

## Definition
A translation unit (TU) is the ultimate unit of compilation in C, consisting of a single source file (`.c`) combined with all headers transitively included by it via `#include`, prior to compiler parsing. Headers (`.h`) serve as interface contracts declaring public prototypes, types, and macros without allocating storage. In embedded and systems architecture, the rigorous partitioning of public vs. private interfaces, translation unit scoping, linkage control, and dependency direction dictates system modularity, rebuild scalability, and binary stability.

## Scope and Boundaries
Covers: Translation unit anatomy, public vs. private headers, self-sufficiency, include guards, `extern` declarations, definition ownership, opaque encapsulation, dependency DAGs, circular include mitigation, API versioning, linkage control (`static` vs `extern`), and embedded module boundaries.
Does not cover: Linker script layout or C++ modules.

## Topics in This Chapter
1. `01_Public_headers.md`: Interface contracts, exposure boundaries, zero implementation leakage, and client stability.
2. `02_Private_headers.md`: Intra-module interfaces, private structures, hardware layout concealment, and translation unit firewalls.
3. `03_Include_guards.md`: Multiple inclusion avoidance, guard naming conventions, idempotency, and MIOpt compiler optimization.
4. `04_External_declarations.md`: `extern` functions and variables, header-based declaration rules, and avoiding multiple definition traps.
5. `05_Definition_ownership.md`: The One Definition Rule in C, single translation unit storage ownership, and bss/data symbol allocation.
6. `06_Opaque_interfaces.md`: Incomplete type pointers (handles), compiler isolation, ABI stability, and heap/pool encapsulation.
7. `07_Header_self_sufficiency.md`: The compile-alone test, prerequisite inclusion ordering, and self-contained header discipline.
8. `08_Dependency_direction.md`: Layered architectures, acyclic dependencies (DAG), High-level to Low-level flow, and inversion principles.
9. `09_Circular_include_avoidance.md`: Mutually recursive structures, forward declarations, tag decoupling, and architecture refactoring.
10. `10_API_versioning.md`: Semantic versioning, deprecation macros, ABI symbol stability, and migration wrappers.
11. `11_Linkage_hygiene.md`: External vs. internal linkage (`static`), tentative definitions, and minimizing global namespace pollution.
12. `12_Embedded_module_boundaries.md`: Hardware abstraction layers (HAL), driver boundaries, interrupt decoupling, and MISRA C interface compliance.

## Staff-Level Takeaway
Headers are formal architectural contracts; translation units are independent compilation silos. Maintain strict dependency direction, enforce complete header self-sufficiency, declare variables once in headers with `extern` and own them in exactly one `.c` file, and hide internal driver layouts behind opaque handle pointers.

## Related Concepts
- `../18_C_Typedef/03_Opaque_typedefs`
- `../19_C_Preprocessor/01_File_inclusion`
- `../19_C_Preprocessor/08_Include_guards`
- `../00_Complete_Topic_Map`
