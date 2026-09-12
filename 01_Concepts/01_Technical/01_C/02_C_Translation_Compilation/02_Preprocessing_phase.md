# Preprocessing Phase

The preprocessing phase transforms preprocessing tokens according to directives and macro rules before the compiler performs the later language translation work. It is a source-transformation stage, not a general-purpose C parser.

## Core operations
Important mechanisms include macro replacement, file inclusion, conditional inclusion, pragma handling, predefined macros and diagnostic directives. The result is the input consumed by subsequent translation stages.

## Headers are textual inclusion
A traditional `#include` effectively makes the included header's preprocessing content available in the including translation unit. It does not create a runtime module boundary. Include guards or equivalent mechanisms prevent repeated definitions within a translation unit, while dependency hygiene determines what an API actually exposes.

## Macro expansion
Macro replacement is token-based. Function-like macros can evaluate arguments more than once, so expressions with side effects can produce surprising behavior. Parenthesization prevents many precedence errors but cannot make an inherently unsafe macro safe.

## Conditional compilation
`#if` configuration creates different source programs from the same repository. Therefore each supported configuration is a distinct build variant that may require compilation and test coverage.

## Embedded implications
Board variants, feature switches, bootloader/application builds and debug/release configurations frequently depend on preprocessing. Excessive configuration can multiply the number of effective programs and make defects configuration-specific.

## Debugging
When behavior differs between builds, inspect the preprocessed output and compiler command line. Confirm include search paths, macro definitions and language mode before investigating generated assembly.

## Common failures
- accidental macro collisions;
- missing include guards;
- configuration branches that are never compiled;
- relying on include order for declarations;
- mixing target and host headers;
- hidden behavior controlled by build-system definitions.

## Staff-level view
Treat preprocessing as a program generator. Minimize uncontrolled configuration, make public interfaces explicit, and ensure every supported configuration is represented in CI or another reproducible validation mechanism.

## Related
- [[03_Tokenization]]
- [[06_Object_code_generation]]
- [[19_C_Preprocessor]]
- [[20_C_Macros]]
