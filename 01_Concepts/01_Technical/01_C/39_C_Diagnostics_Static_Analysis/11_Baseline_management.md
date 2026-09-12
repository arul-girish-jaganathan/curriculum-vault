# Baseline management

> Canonical C topic note — chapter 39.

## Definition
A static-analysis baseline records known existing findings so CI can enforce that new defects do not increase the accepted debt. It is a migration mechanism, not a permanent safety exemption.

## Mechanism and language rules
Baselines should identify stable finding fingerprints, locations, rule IDs, and tool versions. Prefer tracking defects and deviations explicitly when practical because line-based fingerprints can become stale after refactoring.

## Embedded implications
Baselines allow legacy firmware to adopt stronger analysis without blocking all development. New and modified code can be held to a stricter gate while historical findings are retired progressively.

## Edge cases and failure modes
- Baseline silently accepting a newly introduced defect with a matching fingerprint.
- Never reducing baseline size.
- Updating tool versions without reviewing changed findings.
- Storing baselines outside source control.

## Verification / debugging
Track baseline count and age. Require review for additions. Periodically rebuild from a clean analysis and retire resolved findings. Pin analyzer versions or explicitly review version changes.

## Staff-level takeaway
A baseline should trend toward zero or a controlled, justified residual—not become a second database of ignored defects.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
