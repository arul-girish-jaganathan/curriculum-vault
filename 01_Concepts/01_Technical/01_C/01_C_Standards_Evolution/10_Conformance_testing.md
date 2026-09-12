# Conformance Testing

Conformance testing asks whether a program, compiler configuration or implementation behaves according to the applicable specification. For C, this requires separating language conformance from platform behavior and product requirements.

## What to test
A useful C conformance strategy includes syntax and semantic acceptance, required diagnostics, defined behavior, implementation-defined choices, library availability, integer and floating-point properties, and selected edge cases relevant to the supported profile.

## Embedded profile
A bare-metal product should not be judged as if it were a hosted desktop application. Define the supported C profile first: standard revision, freestanding/hosted environment, compiler, ABI, library subset, permitted extensions and project coding rules.

## Compile-time probes
Use `_Static_assert` and small compile probes to establish properties such as type sizes, alignment assumptions and feature availability. These checks turn hidden assumptions into build failures.

## Runtime and integration evidence
Runtime tests should cover boundaries that the language alone cannot prove: startup behavior, interrupt interaction, DMA ownership, peripheral register semantics, timing and persistent data. Those are system-level contracts, not ISO C conformance claims.

## Evidence discipline
A passing test proves the tested configuration and behavior; it does not prove universal portability. Record compiler version, flags, target, library, optimization level and relevant hardware conditions with the result.

## Staff-level view
Conformance is most valuable when it creates a reproducible contract. A small, maintained probe suite can prevent compiler upgrades and platform migrations from silently changing assumptions.

## Related
- [[08_Implementation_defined_behavior]]
- [[11_Choosing_a_language_baseline]]
- [[39_C_Diagnostics_Static_Analysis]]
- [[57_C_Analyzability_Conformance_Testability]]
