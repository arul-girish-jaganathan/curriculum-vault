# Host-target differential testing

> Canonical C topic note — chapter 40.

## Definition
Differential testing compares behavior of two implementations or environments for the same inputs. In embedded C, a host implementation can be compared with the target implementation to reveal portability and representation differences.

## Mechanism and language rules
The comparison requires a defined oracle: decoded fields, serialized bytes, state transitions, checksums, or mathematical results. Differences may be legitimate when behavior is implementation-defined, so first classify the C rule and target contract.

## Embedded implications
This approach is powerful for parsers, encoders, cryptographic wrappers, fixed-point algorithms, and protocol state machines. It can expose endianness, width, alignment, signedness, and floating-point assumptions without requiring every input to run on hardware.

## Edge cases and failure modes
- Treating host behavior as the specification.
- Comparing undefined behavior instead of defined outputs.
- Ignoring target-specific rounding or integer widths.
- Using nondeterministic timestamps/randomness in the comparison.

## Verification / debugging
Generate the same corpus for host and target, compare canonical outputs, and classify every mismatch. Add each confirmed portability defect as a regression test.

## Staff-level takeaway
Differential testing is strongest when the oracle is derived from the product contract, not whichever implementation happened to be written first.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
