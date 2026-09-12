# CI quality gates

> Canonical C topic note — chapter 39.

## Definition
A CI quality gate turns diagnostics and analysis into enforceable release criteria. A useful gate measures defect risk, not merely whether a tool executed successfully.

## Mechanism and language rules
Typical gates include clean compilation, selected warnings as errors, static-analysis severity limits, MISRA/CERT findings, sanitizer tests, unit coverage, image-size limits, and artifact provenance. Each gate needs an owner and an explicit exception process.

## Embedded implications
Firmware gates should include all supported configurations and the exact production build. Memory-map overflow, ABI mismatch, generated-code drift, and target-specific diagnostics must not be hidden behind a host-only green build.

## Edge cases and failure modes
- Gates that check only one build variant.
- Unreviewed suppressions bypassing analysis.
- Flaky hardware-in-loop tests blocking unrelated work.
- Measuring coverage without meaningful fault assertions.

## Verification / debugging
Keep gate configuration version-controlled. Make failures actionable and archive reports. Periodically test that intentionally introduced defects fail the expected gate; otherwise a gate may exist only on paper.

## Staff-level takeaway
A quality gate is a tested control. Its effectiveness should itself be demonstrated through seeded defects, audits, and trend metrics.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
