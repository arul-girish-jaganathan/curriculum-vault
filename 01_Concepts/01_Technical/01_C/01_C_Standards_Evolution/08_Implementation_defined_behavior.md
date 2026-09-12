# Implementation-Defined Behavior

Implementation-defined behavior is behavior for which the C implementation chooses one of multiple permitted possibilities and documents its choice. This is different from undefined behavior: the implementation is not free to do anything; it has a specified choice that should be documented.

## Why it matters
Embedded portability frequently crosses implementation-defined boundaries: integer representations and widths, character signedness, right-shift behavior for negative values in relevant language rules, sizes and alignments of types, floating-point characteristics, and other implementation properties.

## Engineering rule
Never infer an implementation-defined property from the CPU name alone. Establish it from authoritative compiler documentation, target ABI documentation, headers, or a small conformance probe.

## Example: `char` signedness
Whether plain `char` behaves as signed or unsigned is an implementation choice. Code that stores a byte and later compares it with negative values can therefore change behavior across targets. Use `unsigned char` when the semantic object is raw byte data and document character-text semantics separately.

## Embedded consequences
Implementation-defined choices affect serialization, register fields, checksum code, protocol parsing, persistent storage and ABI boundaries. A change of compiler or target can turn a latent assumption into a field defect without any source-level change.

## Verification pattern
For each portability-sensitive property:
1. identify the ISO rule;
2. identify the implementation choice;
3. record the chosen value for the supported toolchain;
4. add a compile-time assertion or build-time check when practical;
5. test the boundary behavior.

## Common misconception
“Implementation-defined means non-portable and therefore bad” is too simplistic. A product can intentionally depend on an implementation-defined property if the supported platform is controlled and the dependency is documented and verified.

## Staff-level view
Treat implementation-defined behavior as an explicit architecture dependency. The problem is not the dependency itself; the problem is an undocumented dependency that silently changes when the toolchain or target changes.

## Related
- [[07_Hosted_vs_freestanding]]
- [[09_Undefined_behavior_and_portability]]
- [[11_Choosing_a_language_baseline]]
