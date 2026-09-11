# C89/C90 Heritage

## Why this era still matters
C89/C90 is the historical baseline from which much production C grew. Legacy embedded code often retains declarations-at-block-start, implicit assumptions about integer widths, pre-standard extensions, macro-heavy interfaces, and APIs designed before C99 introduced several modern conveniences. Understanding the baseline explains why older firmware looks different from modern C and prevents accidental modernization that changes behavior.

## Core language ideas
The C90 language already established the central model: objects have types and storage, expressions have values and side effects, pointers represent addresses within the language model, functions form the main unit of control flow, and translation converts source text into executable implementation artifacts. C90 also established the distinction between what the language specifies and what an implementation may choose.

Important C90-era constructs include declarations before statements within a block, `/* ... */` comments, fixed-width assumptions being absent from the standard library, `typedef`, `struct`, `union`, `enum`, `static`, `extern`, function prototypes, and the preprocessor. Function prototypes are particularly important: old-style function declarations without parameter information are not equivalent to a modern prototype.

## Embedded consequences
A C90-looking codebase is not necessarily non-portable, but its assumptions must be made explicit. A driver that assumes `unsigned long` is 32 bits, a register map that relies on implementation layout, or a serialization routine that casts a byte buffer to a structure may compile cleanly while depending on target properties.

C90 heritage also explains why many safety-oriented embedded projects impose a deliberately conservative subset of newer C. The goal is not to reject newer syntax; it is to make object lifetime, conversions, control flow, and interfaces easy to analyze.

## What the standard does not guarantee
ISO C does not guarantee that `char`, `short`, `int`, `long`, and `long long` have the widths commonly associated with a particular CPU. It also does not define a universal ABI, register calling convention, linker script format, MMIO mechanism, interrupt model, cache policy, or exact structure packing used by a compiler-target pair.

Therefore a statement such as “this is 32-bit C” is incomplete. The language standard, implementation, ABI and MCU architecture must be considered separately.

## Migration guidance
When modernizing legacy C, change one semantic boundary at a time. First capture compiler diagnostics, tests, binary size, timing and externally visible behavior. Then replace assumptions with explicit types and contracts. Do not mechanically rewrite declarations, signedness, macros or packed structures without checking ABI and hardware effects.

## Staff-level review questions
- Which parts are genuine C language requirements and which are compiler conventions?
- Which integer-width assumptions are encoded in the design?
- Does modernization alter object representation or ABI?
- Can the old behavior be demonstrated by a test before changing it?

## Related chapters
- [[02_C99_additions]]
- [[07_Hosted_vs_freestanding]]
- [[08_Implementation_defined_behavior]]
- [[09_Undefined_behavior_and_portability]]
