# 29_C_Behavior_Categories: Chapter Index

## Overview
C Behavior Categories define the formal classifications of program execution semantics established by the ISO C standard (ISO/IEC 9899). Understanding how the standard categorizes behavior—ranging from strictly defined and implementation-defined to unspecified and undefined behavior—is essential for writing portable, robust, and secure systems code. This chapter explores behavior semantics, constraint violations, Annex J mappings, compiler optimizer exploitation of undefined behavior, diagnostic strategies, defensive coding, embedded UB hazards, and systematic behavior classification workflows.

## Chapter Directory
- [[01_Defined_behavior]] — ISO C standard-mandated behavior with predictable, portable outcomes across all conforming implementations
- [[02_Implementation_defined_behavior]] — Behavior left to individual compiler/hardware vendors, required to be documented
- [[03_Unspecified_behavior]] — Behavior where the standard provides multiple valid options without mandating which one occurs
- [[04_Undefined_behavior]] — Behavior without mandates from the standard; permits compiler optimization exploitation, security vulnerabilities, and unpredictable runtime faults
- [[05_Constraint_violations]] — Syntax and semantic rule infractions requiring diagnostic message output by conforming translators
- [[06_Annex_J_style_thinking]] — Navigating Annex J (Portability) to audit platform dependencies and compiler variance
- [[07_Optimizer_exploitation]] — How modern optimizers leverage undefined behavior to eliminate checks and alter control flow
- [[08_Compiler_diagnostics]] — Warnings, errors, `-Werror`, and compiler diagnostic reporting mechanics
- [[09_Portable_defensive_coding]] — Writing defensive code resilient against implementation shifts and silent bugs
- [[10_Embedded_UB_examples]] — Classic embedded UB triggers (volatile misuse, unaligned access, interrupt races)
- [[11_Static_analysis_review]] — Leveraging static analyzers (Clang-Tidy, Coverity, Polyspace) to catch UB and constraint violations
- [[12_Behavior_classification_workflow]] — A staff-level engineering workflow for classifying, evaluating, and eliminating hazardous code patterns

## Related Chapters
- [[../00_Complete_Topic_Map]]
- [[../26_C_Lifetime_Aliasing]]
- [[../27_C_Alignment_Object_Representation]]
