# Coverage-guided fuzzing

> Canonical C topic note — chapter 40.

## Definition
Coverage-guided fuzzing generates and mutates inputs while retaining cases that exercise new program paths or coverage. It is effective for finding crashes, assertion failures, memory errors, parser defects, and unexpected state transitions.

## Mechanism and language rules
A fuzz target should accept a bounded input and execute deterministic logic. Instrumentation measures coverage; mutations evolve the corpus toward unexplored behavior. Sanitizers make otherwise silent memory/UB defects observable.

## Embedded implications
Protocol decoders, configuration parsers, image/data formats, command interpreters, and boot/update metadata are excellent targets. Hardware access should be isolated behind deterministic interfaces so the core logic can run on a host.

## Edge cases and failure modes
- Fuzzing a huge wrapper instead of the security-critical parser.
- Nondeterministic targets reducing coverage quality.
- No input-size bound.
- Ignoring hangs, resource exhaustion, and logical assertion failures.

## Verification / debugging
Run fuzzing with ASan/UBSan where practical. Preserve crashing inputs, minimize them, and add confirmed regressions to the permanent corpus. Track coverage trends and unique bug signatures.

## Staff-level takeaway
Good fuzzing is an architecture exercise: isolate a deterministic attack surface, instrument it, define failure oracles, and feed discoveries back into regression testing.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
