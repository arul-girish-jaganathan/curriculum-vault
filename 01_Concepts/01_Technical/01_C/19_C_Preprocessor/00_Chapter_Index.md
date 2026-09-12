# 19: C Preprocessor — Chapter Index

## Definition
The C Preprocessor (CPP) is a macro processor that operates on the source code text prior to syntactical and semantic compilation. Operating strictly across Translation Phases 1 through 4 of ISO C, it performs lexical manipulations including header file inclusion, conditional compilation, macro substitution, stringification, token concatenation, and pragma dispatching. In systems and embedded engineering, it constitutes the foundational configuration layer for cross-compilation, hardware abstraction, and feature toggling.

## Scope and Boundaries
Covers: Translation phases 1–4, file inclusion search algorithms (`#include`), macro expansion rescanning rules, operator precedence hazards, conditional directives (`#if`, `#ifdef`, `defined`), stringification (`#`), token pasting (`##`), standard/compiler predefined macros, feature detection macros (`__has_include`, `__has_builtin`), include guards vs `#pragma once`, diagnostic directives (`#error`, `#warning`, `#line`), intermediate output inspection (`-E`), and architectural macro hygiene.
Does not cover: C++ templates, compiler AST generation (Translation Phase 7), or linker script pre-processing.

## Topics in This Chapter
1. `01_File_inclusion.md`: `#include <...>` vs `#include "..."`, include paths (`-I`, `-isystem`), circular inclusion, and file search resolution.
2. `02_Macro_expansion.md`: Object-like vs function-like macros, rescanning rules, argument prescan, side-effect hazards, and the `do { ... } while(0)` idiom.
3. `03_Conditional_inclusion.md`: `#if`, `#elif`, `#else`, `#endif`, `#ifdef`, `#ifndef`, integer constant expressions, and the `defined` operator.
4. `04_Stringification.md`: The `#` operator, stringizing rules, whitespace collapsing, escape sequences, and two-level stringification macros.
5. `05_Token_pasting.md`: The `##` operator, token concatenation, identifier synthesis, macro indirection evaluation traps, and placemarker tokens.
6. `06_Predefined_macros.md`: Standard macros (`__FILE__`, `__LINE__`, `__DATE__`, `__TIME__`, `__STDC_VERSION__`), reproducibility risks, and compiler-specific target identifiers.
7. `07_Feature_detection.md`: Modern C/C++ feature testing (`__has_include`, `__has_builtin`, `__has_attribute`), and cross-toolchain compiler compatibility layers.
8. `08_Include_guards.md`: Classic `#ifndef`/`#define`/`#endif` guards, `#pragma once` support, multi-include optimization (MIOpt), and header idempotency.
9. `09_Pragma.md`: `#pragma` directive, C99 `_Pragma()` operator, compiler control (`pack`, `section`, `weak`), and warning suppression.
10. `10_Preprocessor_diagnostics.md`: `#error`, `#warning`, compile-time contract assertions, configuration validation, and `#line` control.
11. `11_Macro_expansion_debugging.md`: Preprocessor output inspection (`gcc -E`), `-dM`, `-dD`, Clang macro expansion backtraces, and macro visualization.
12. `12_Preprocessor_architecture.md`: Architectural boundaries, configuration headers (`config.h`), X-Macros for code generation, and MISRA C preprocessor safety rules.

## Staff-Level Takeaway
The preprocessor is a token-based text transformation pipeline completely blind to C types, scopes, and memory semantics. In professional systems architecture, use it strictly for conditional compilation, hardware configuration, and boilerplate generation (X-Macros). Enforce strict parenthesis encapsulation, prevent side-effect argument evaluation, and minimize macro footprint in public interfaces.

## Related Concepts
- `../18_C_Typedef/08_Typedef_vs_macro`
- `../17_C_Bit_Fields/09_Mask_and_shift_alternatives`
- `../00_Complete_Topic_Map`
