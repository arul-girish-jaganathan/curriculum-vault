# C23 Modernization

C23 is the published modern C language revision. It continues the C11/C17 trajectory while cleaning up older language features, adding new facilities, and making several long-standing practices more expressive.

## Modernization themes
Important C23 areas include improved type and constant-expression facilities, `nullptr` for a null pointer constant, `bool` as a built-in spelling, digit separators, attributes, `typeof`-related functionality, `constexpr` objects, improved enumeration and preprocessing facilities, and additions to the standard library. Exact availability still depends on the compiler and library implementation.

## The embedded question
The correct question is not “Can our compiler say C23?” but “Which C23 features are implemented, analyzable and acceptable for this product?” A freestanding MCU environment may provide only part of the hosted library, and a compiler can support extensions beyond the standard while still having incomplete support for newer standard features.

## Migration principles
1. Freeze the current compiler, flags and tests.
2. Enable the new language mode without broad source rewrites.
3. Separate language diagnostics from library/toolchain limitations.
4. Introduce one feature at a time.
5. Measure code size, RAM, timing and generated code where relevant.
6. Update static-analysis and coding-standard rules.
7. Preserve ABI and persistent-data compatibility unless a migration explicitly addresses them.

## Avoid cargo-cult modernization
Replacing every old idiom with the newest syntax can increase review and certification cost without improving the system. Prefer changes that make contracts clearer, eliminate error-prone constructs, improve diagnostics, or solve a known maintainability problem.

## Toolchain reality
The compiler language mode is only one component. Headers, libc, assembler, linker, debugger, static analyzer and build system all participate in the effective development environment. A feature that parses successfully may still be unavailable in the target library or unsuitable for a certified toolchain.

## Staff-level view
Treat language upgrades as controlled platform migrations. Define a supported feature subset, establish compatibility gates, and record exceptions. The objective is predictable engineering, not maximum language-version marketing.

## Related
- [[04_C17_maintenance_release]]
- [[06_Feature_test_macros]]
- [[11_Choosing_a_language_baseline]]
- [[12_Standards_watch]]
