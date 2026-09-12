# Host-target differential testing

## Definition
**Host-target differential testing** compares the behavior of the same C logic or test vectors across a host implementation and the embedded target. Differences can reveal assumptions about integer width, endianness, alignment, ABI, compiler behavior, or hardware dependencies.

## Scope and boundaries
The comparison is strongest for deterministic pure functions: encoders/decoders, checksums, parsers, state transitions, and numerical routines. It is not valid to expect identical timing, pointer values, floating-point environment, or hardware side effects across platforms.

## Mechanism and language rules
Define a common input/output contract:

```text
input vector -> host implementation
             -> target implementation
             -> normalize observable result -> compare
```

For binary protocols, compare exact bytes. For numerical algorithms, define acceptable tolerance and floating-point environment explicitly.

## Embedded implications
This technique is excellent for validating firmware protocol stacks against a host reference model. It can catch target-only truncation, signedness, padding, endian, and serialization defects. It is also useful for bootloader image validation and cryptographic test vectors where exact outputs are specified.

## Edge cases and failure modes
- Host and target intentionally use different integer sizes.
- Structure padding is compared instead of serialized fields.
- Undefined behavior produces divergent but apparently plausible outputs.
- Floating-point differences are treated as failures without a defined tolerance.
- Hardware-dependent behavior is accidentally included in the comparison.

## Verification / debugging
Use shared golden vectors and record both outputs. When they differ, reduce to the smallest input and inspect types, object representation, alignment, and generated assembly. Run host sanitizers on the same vectors to determine whether the discrepancy comes from undefined behavior.

## Performance, memory, timing and power
Host execution can process large vector sets quickly; target execution validates the real architecture. Differential tests can therefore provide high confidence without requiring all fuzzing and sanitization to run on the MCU.

## Staff-level takeaway
Define **what must be identical and what is allowed to differ** before building a differential test. The comparison is only as strong as its contract.