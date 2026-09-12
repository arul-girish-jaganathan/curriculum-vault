# Warning levels

> Canonical C topic note — chapter 39.

## Definition
Warning levels are compiler-specific collections of diagnostics, ranging from conservative defaults to aggressive suspicious-code checks. Their names and exact contents vary by compiler and version.

## Mechanism and language rules
A robust policy combines broad baseline warnings with selected high-value diagnostics. Examples include conversion, sign comparison, format, prototype, shadowing, and control-flow warnings. “Maximum warnings” is not a portable technical definition.

## Embedded implications
Different target compilers may produce different warnings for the same C source. A multi-compiler project should define semantic expectations rather than assuming identical warning sets.

## Edge cases and failure modes
- Enabling a broad preset without reviewing its false-positive profile.
- Suppressing a warning globally to fix one legacy module.
- Treating warning-count equality across compilers as a quality metric.

## Verification / debugging
Document compiler/version-specific flags and test them in CI. Review new warnings after compiler upgrades and classify them by defect risk.

## Staff-level takeaway
Warning levels are policy inputs. Optimize for defect detection and maintainability, not for a particular number of enabled switches.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
