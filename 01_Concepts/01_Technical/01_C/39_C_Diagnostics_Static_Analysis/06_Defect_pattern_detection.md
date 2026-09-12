# Defect pattern detection

> Canonical C topic note — chapter 39.

## Definition
Defect-pattern detection searches for recurring syntactic or semantic shapes associated with defects: unchecked return values, dangerous casts, missing bounds checks, double release, use-after-release patterns, suspicious shifts, and unsafe string operations.

## Mechanism and language rules
Pattern rules range from simple AST matching to dataflow and interprocedural reasoning. High-quality rules distinguish actual contracts from superficial syntax.

## Embedded implications
Firmware-specific patterns include MMIO access-width mistakes, interrupt-shared state without synchronization, unchecked DMA lengths, timeout omissions, integer truncation at hardware boundaries, and unsafe register read-modify-write sequences.

## Edge cases and failure modes
A pattern can be safe under a local invariant that the analyzer cannot see. Conversely, a superficially safe pattern can fail when the invariant is not actually enforced. Avoid blanket suppressions.

## Verification / debugging
For each finding, identify the violated contract, reproduce if practical, and document the fix pattern. Prefer APIs that make unsafe states hard to express.

## Staff-level takeaway
The highest-value static rules encode architectural failure modes, not merely stylistic preferences. Build a rule set around the product's real defect history.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
