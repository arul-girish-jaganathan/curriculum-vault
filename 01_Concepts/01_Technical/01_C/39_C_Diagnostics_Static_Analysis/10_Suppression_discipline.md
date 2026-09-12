# Suppression discipline

> Canonical C topic note — chapter 39.

## Definition
Suppression discipline is the controlled process for excluding a known, justified analyzer or compiler finding without hiding unrelated defects.

## Mechanism and language rules
A good suppression identifies rule, location/scope, reason, evidence, owner, and review condition. Prefer source-local or module-local suppression over global disablement. If the tool supports baselines, use them for legacy debt rather than making every finding permanently invisible.

## Embedded implications
Suppression is particularly sensitive in safety/security code. A deviation around a register access may be valid, while the same broad rule suppression could hide unsafe pointer arithmetic elsewhere.

## Edge cases and failure modes
- File-wide disablement for one line.
- No rationale or expiry.
- Suppressions copied after refactoring to unrelated code.
- Treating tool limitations as proof of safety.

## Verification / debugging
Review suppressions as code. CI should detect unexplained additions, stale suppressions, and policy violations. Re-run analysis after tool upgrades to see whether old suppressions remain necessary.

## Staff-level takeaway
Every suppression spends part of the project's defect-detection budget. Spend it narrowly and record why.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
