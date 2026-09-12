# 20: C Macros — Chapter Index

## Definition
Macros are compile-time lexical transformation identifiers defined using the `#define` preprocessor directive. They instruct the preprocessor to substitute tokens in source code before semantic analysis and compilation occur. In systems and embedded engineering, macros span the spectrum from simple numeric constants to complex variadic logging facilities and metaprogramming dispatch tables. However, because they lack type awareness, scope boundaries, and execution sequencing, macros introduce severe hazards if designed without defensive discipline.

## Scope and Boundaries
Covers: Object-like and function-like macros, defensive parentheses discipline, multiple evaluation hazards, statement encapsulation, the `do { ... } while(0)` idiom, C99 variadic macros (`__VA_ARGS__`), stringification/token-pasting patterns, enterprise macro namespacing, trade-offs with `static inline` functions, and formal macro review checklists.
Does not cover: General file inclusion (see `19_C_Preprocessor/01_File_inclusion`), conditional inclusion (see `19_C_Preprocessor/03_Conditional_inclusion`), or C++ template metaprogramming.

## Topics in This Chapter
1. `01_Object_like_macros.md`: Constant definitions, configuration flags, literal suffix discipline (`U`, `UL`), and scope pollution.
2. `02_Function_like_macros.md`: Parameterized expansion, call syntax, argument substitution rules, and expression vs. statement roles.
3. `03_Parentheses_discipline.md`: Operator precedence hazards, outer expression encapsulation, argument isolation, and AST parse bugs.
4. `04_Multiple_evaluation.md`: Arguments with side effects (`i++`, hardware reads), cache-invalidation traps, and non-deterministic behavior.
5. `05_Statement_macros.md`: Multi-line blocks, dangling-else traps, semicolon swallowing, and control-flow jumps (`return`, `goto`).
6. `06_do_while_0_idiom.md`: Mechanical syntax justification, AST block isolation, semicolon consumption, and compiler dead-code optimization.
7. `07_Variadic_macros.md`: C99 `...` and `__VA_ARGS__`, GNU `, ## __VA_ARGS__` vs. C23 `__VA_OPT__`, and debug logging architectures.
8. `08_Stringification_macros.md`: Stringize operator (`#`), diagnostic assertion wrappers, and two-level evaluation idioms.
9. `09_Token_pasting_macros.md`: Concatenation operator (`##`), synthetic identifier generation, register dispatch, and two-tier evaluation rules.
10. `10_Macro_namespaces.md`: Identifier collision prevention, library prefixes, uppercase rules, and pollution of global translation units.
11. `11_When_inline_functions_are_safer.md`: Type safety, debugger stepping, single-evaluation semantics, warning diagnostics, and when macros remain strictly necessary.
12. `12_Macro_review_checklist.md`: Industrial audit criteria, MISRA C:2012 compliance rules (Dir 4.9, Rule 20.7), and production PR sign-off gates.

## Staff-Level Takeaway
Macros operate on raw text tokens without understanding types, values, or storage. Every function-like macro must be viewed as an architectural liability that requires defensive parentheses, single-evaluation guarantees, and statement encapsulation. In modern C (C99+), default to `static inline` functions and `const` variables, reserving macros exclusively for conditional compilation, variadic diagnostics, stringification, token pasting, and X-Macro tables.

## Related Concepts
- `../18_C_Typedef/08_Typedef_vs_macro`
- `../19_C_Preprocessor/02_Macro_expansion`
- `../19_C_Preprocessor/12_Preprocessor_architecture`
- `../00_Complete_Topic_Map`
