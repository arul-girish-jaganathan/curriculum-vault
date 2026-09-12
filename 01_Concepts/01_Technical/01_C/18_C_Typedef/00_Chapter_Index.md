# 18: C Typedef — Chapter Index

## Definition
The `typedef` specifier creates synonym names (aliases) for existing types within the C type system. It does not introduce new independent, strong types; rather, it introduces identifiers into the ordinary identifier namespace that can be used identically to their underlying type specifications. In systems, kernel, and embedded software, `typedef` is the central mechanism for type abstraction, hardware portability, opaque encapsulation, and callback modeling.

## Scope and Boundaries
Covers: Primitive aliases, struct/union aliasing idioms, opaque pointer handles, function pointer signatures, pointer-hiding hazards, array typedefs, qualifier propagation rules (`const`, `volatile`), macro vs typedef semantics, domain-driven API readability, MISRA C compliance, toolchain ABI stability, and architectural naming conventions.
Does not cover: C++ strong typedefs / `using` alias templates, preprocessor token concatenation, or link-time symbol aliasing (`__attribute__((alias))`).

## Topics in This Chapter
1. `01_Basic_typedefs.md`: Aliasing primitive types, portable width abstractions (`uint32_t`), and scope boundaries.
2. `02_Struct_typedefs.md`: Tagged structs, anonymous struct typedefs, self-referential definitions, and forward declarations.
3. `03_Opaque_typedefs.md`: Information hiding, incomplete types, handle patterns, and compile-time encapsulation.
4. `04_Function_pointer_typedefs.md`: Callback signatures, dispatch tables, interrupt vector typing, and syntax de-obfuscation.
5. `05_Pointer_typedefs.md`: Pointer-hiding anti-patterns, const qualifier hazards, and readability degradation.
6. `06_Array_typedefs.md`: Fixed-size buffer aliases, decay mechanics, dimension preservation, and parameter passing traps.
7. `07_Qualified_typedefs.md`: Interaction with `const`, `volatile`, and `restrict`, top-level vs. low-level qualification, and qualifier stripping bugs.
8. `08_Typedef_vs_macro.md`: Lexical macro substitution vs. AST-aware typedefs, multi-variable declarations, and scope control.
9. `09_Readable_API_typedefs.md`: Domain-driven semantic aliases (e.g., `tick_t`, `status_code_t`), type clarity, and cognitive load reduction.
10. `10_MISRA_oriented_typedef_usage.md`: Essential type categories, MISRA C:2012 Rule 5.6, Rule 8.1, and compliance frameworks.
11. `11_ABI_implications.md`: Equivalence under the type system, mangling/debugging symbols, ABI stability, and calling convention invariance.
12. `12_Naming_strategy.md`: Suffix conventions (`_t`, `_handle_t`), POSIX namespace conflicts (`_t` reservation), and enterprise naming standards.

## Staff-Level Takeaway
`typedef` establishes architectural contracts and hardware portability boundaries. Treat `typedef` as an abstraction tool: use it to decouple code from native bit widths, encapsulate private implementations via opaque pointers, and simplify complex function signatures. Avoid using `typedef` to hide pointers or create decorative aliases that obscure basic type semantics.

## Related Concepts
- `../16_C_Struct_Union_Enum/01_Structure_layout`
- `../16_C_Struct_Union_Enum/05_Pointer_to_structure`
- `../12_Function_pointers`
- `../00_Complete_Topic_Map`
