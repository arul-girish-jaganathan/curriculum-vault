# Keywords and language-reserved words

## Core idea
Keywords are reserved tokens with predefined grammatical meaning in C. Their presence is recognized during translation; they are not ordinary identifiers available for application naming.

## Why this matters
A keyword participates in grammar and constraints, not merely in naming. Standard evolution can add or retire keywords, which is why code written for one language version or compiler extension may conflict with another baseline.

## Embedded consequences
A project-wide language baseline should be explicit. Toolchain flags such as a selected C standard mode affect which features and diagnostics are accepted. Generated code and vendor headers may depend on implementation extensions, so a clean build requires a documented language mode rather than an assumed compiler default.

## Traps
- Treating a compiler extension keyword as portable ISO C.
- Mixing C and C++ assumptions.
- Letting headers silently depend on a compiler-specific language mode.
- Assuming acceptance by one compiler proves standard conformance.

## Verification
Compile representative feature tests under every supported compiler and language mode. Record the selected standard in the build system and make CI reject accidental language-mode drift.

## Staff-level takeaway
Language version is an architectural dependency. Make it reproducible at the build boundary instead of allowing individual developers or IDE defaults to choose the effective C dialect.
