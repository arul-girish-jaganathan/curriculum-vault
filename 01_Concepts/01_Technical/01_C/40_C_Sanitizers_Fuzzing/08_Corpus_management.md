# Corpus management

## Definition
A **fuzzing corpus** is the collection of seed and discovered inputs used to guide future exploration. Corpus management keeps useful structural diversity while preventing redundant or low-value inputs from consuming storage and execution time.

## Scope and boundaries
A corpus is not simply a folder of random files. Inputs should represent meaningful protocol states, formats, boundary cases, and previously discovered paths. Exact management mechanisms vary by fuzzer.

## Mechanism and language rules
A typical lifecycle is:

```text
seeds -> mutations -> new coverage -> corpus candidates -> minimize/deduplicate
```

Useful seeds include valid examples, malformed examples, boundary lengths, version variants, and field combinations. Retain crash reproductions separately from ordinary exploration corpus.

## Embedded implications
Firmware protocol fuzzing benefits from seeds captured from real devices, conformance suites, field traces with sensitive data removed, and hand-crafted boundary cases. For bootloaders and persistent metadata, include valid images and intentionally corrupted headers.

Do not allow proprietary credentials, production secrets, or personally identifying payloads to enter a shared corpus.

## Edge cases and failure modes
- Corpus becomes huge without increasing coverage.
- Sensitive production data is retained indefinitely.
- Only valid inputs are seeded, so error paths remain unexplored.
- Corpus changes are not versioned, making regressions hard to reproduce.
- Deduplication removes semantically distinct cases that happen to share coarse coverage.

## Verification / debugging
Track corpus provenance and periodically measure coverage contribution. Keep a stable regression corpus for CI separate from an exploratory corpus. Promote every fixed crash into a deterministic regression test.

## Performance, memory, timing and power
Smaller high-value corpora reduce startup and mutation overhead. Corpus minimization should preserve important coverage and semantic diversity rather than merely minimizing file count.

## Staff-level takeaway
Treat the corpus as **test knowledge**. Curate it, version it, sanitize it, and convert important discoveries into permanent regression artifacts.