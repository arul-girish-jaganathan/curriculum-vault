# Assertions, Diagnostics and Attributes

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_assert_macro|assert macro]]
- [[02_Static_assertions|Static assertions]]
- [[03_Static_assert|_Static_assert]]
- [[04_Noreturn|Noreturn]]
- [[05_deprecated_style_attributes|deprecated-style attributes]]
- [[06_fallthrough_annotations|fallthrough annotations]]
- [[07_Unused_diagnostics|Unused diagnostics]]
- [[08_Compiler_attributes|Compiler attributes]]
- [[09_Diagnostic_pragmas|Diagnostic pragmas]]
- [[10_Build_mode_assertions|Build-mode assertions]]
- [[11_Safety_critical_assertion_policy|Safety-critical assertion policy]]
- [[12_Contract_documentation|Contract documentation]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
