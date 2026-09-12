# Corpus management

> Canonical C topic note — chapter 40.

## Definition
A fuzzing corpus is the collection of inputs used as seeds and retained for future exploration and regression. Corpus quality affects coverage, execution speed, and reproducibility.

## Mechanism and language rules
Start with valid, malformed, boundary, and historically problematic inputs. Deduplicate by coverage where the fuzzing engine supports it. Keep confirmed crashers as regression cases even if they are not optimal exploration seeds.

## Embedded implications
Include protocol versions, feature flags, maximum lengths, truncated packets, unusual encodings, and field boundary values relevant to firmware. Do not store sensitive production data without sanitization and governance.

## Edge cases and failure modes
- Corpus growing without useful coverage.
- Deleting regression inputs during minimization.
- Inputs dependent on external state.
- Forgetting to version corpus changes with parser changes.

## Verification / debugging
Measure coverage and execution rate before/after corpus changes. Preserve minimized regressions separately from exploration seeds. Archive corpus snapshots for release and security testing where appropriate.

## Staff-level takeaway
A corpus is accumulated engineering knowledge. Manage it like test code: version it, prune it deliberately, and preserve inputs that represent discovered failure modes.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
