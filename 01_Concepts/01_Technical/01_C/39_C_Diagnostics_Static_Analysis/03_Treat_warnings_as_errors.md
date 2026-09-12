# Treat warnings as errors

> Canonical C topic note — chapter 39.

## Definition
Treating selected warnings as errors makes diagnostic cleanliness a build correctness gate. It prevents new suspicious constructs from silently entering the product.

## Mechanism and language rules
Use `-Werror`-style policies selectively where supported, while allowing carefully documented exceptions for third-party/generated code. A compiler upgrade can introduce new warnings, so policy ownership and migration procedures are necessary.

## Embedded implications
This control is valuable in firmware because a warning can represent an ABI mismatch, truncation, incorrect format, or unreachable safety path. It also prevents warning debt from becoming too large to review.

## Edge cases and failure modes
- Breaking every build when a compiler update adds a benign diagnostic.
- Suppressing the entire warning class to restore CI.
- Treating vendor/generated code as product code without a boundary.

## Verification / debugging
Keep the warning policy version-controlled. Record exceptions with scope and rationale. Upgrade compilers in a controlled branch and review diagnostic deltas before release.

## Staff-level takeaway
Warnings-as-errors is effective when paired with exception discipline and toolchain governance. The objective is a trusted gate, not a permanently fragile build.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
