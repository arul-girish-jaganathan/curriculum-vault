# False positives

> Canonical C topic note — chapter 39.

## Definition
A false positive is a tool finding that does not represent a defect under the actual program contract. False positives are inevitable in approximate static analysis; unmanaged noise destroys trust in the tool.

## Mechanism and language rules
Findings may be conservative because the analyzer cannot prove aliasing, ownership, range, or path constraints. A finding can also be technically valid but irrelevant to the product's threat or safety scope.

## Embedded implications
Hardware registers, interrupt paths, generated code, RTOS primitives, and vendor SDKs frequently require analysis models or documented assumptions. The answer should be to improve the model or boundary, not indiscriminately suppress diagnostics.

## Edge cases and failure modes
- Suppressing a whole rule because one case is safe.
- Copying suppression annotations without understanding them.
- Ignoring repeated findings until real defects become indistinguishable from noise.

## Verification / debugging
Classify each finding as defect, justified exception, analyzer limitation, or configuration error. Prefer narrow suppressions with rationale and expiry/review ownership.

## Staff-level takeaway
A trusted analyzer is one whose high-severity findings are taken seriously. False-positive management is therefore a safety mechanism, not administrative cleanup.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
