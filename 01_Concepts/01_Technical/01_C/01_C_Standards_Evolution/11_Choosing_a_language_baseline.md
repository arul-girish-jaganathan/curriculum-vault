# Choosing a Language Baseline

A language baseline is the explicit set of C rules and implementation features a product supports. It should be chosen as an engineering constraint, not as a slogan such as “modern C”.

## Decision inputs
Consider:
- required C standard revision;
- compiler and linker support;
- target MCU/CPU and ABI;
- freestanding or hosted environment;
- standard-library availability;
- static-analysis and coding-standard support;
- safety/certification constraints;
- binary compatibility and bootloader interfaces;
- team familiarity and maintenance horizon.

## Feature policy
A strong baseline can permit a standard revision while restricting individual features for good reasons. For example, a project may permit designated initializers but restrict VLAs because stack bounds must be statically demonstrated. The restriction should be recorded as policy, not rediscovered during code review.

## Migration
When upgrading a baseline, measure source diagnostics, generated image size, RAM, timing, startup behavior and ABI compatibility. Compile old and new configurations where practical and use regression tests to establish behavioral equivalence.

## Embedded-specific rule
Never use a language baseline to hide hardware dependencies. `volatile`, memory barriers, packed layouts, compiler attributes and inline assembly may be necessary, but each crosses from ISO C into implementation or hardware contracts and should be documented accordingly.

## Staff-level view
The best baseline is the smallest stable contract that supports product needs while maximizing analyzability and maintainability. Record both the positive feature set and the explicitly prohibited or target-specific subset.

## Related
- [[05_C23_modernization]]
- [[06_Feature_test_macros]]
- [[07_Hosted_vs_freestanding]]
- [[12_Standards_watch]]
