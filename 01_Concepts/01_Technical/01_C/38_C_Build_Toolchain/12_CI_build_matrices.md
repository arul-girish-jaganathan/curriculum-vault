# CI build matrices

## Definition
A **CI build matrix** systematically builds and tests the project across relevant combinations of compiler, target, configuration, optimization, language mode, libraries, and analysis tools. Its purpose is to expose portability and integration defects that one developer build cannot reveal.

## Scope and boundaries
A matrix should be risk-driven rather than combinatorially exhaustive. Each axis exists because changing it can expose a distinct class of defect. The matrix itself is a build-system contract and should be version-controlled.

## Mechanism and language rules
Useful axes may include:

```text
compiler/version × target × debug/release × LTO × feature set
```

Additional jobs can cover host tests, sanitizers, static analysis, size checks, and packaging. Keep the canonical release build separate and obvious.

## Embedded implications
A firmware project may need multiple MCU variants, board revisions, bootloader/application combinations, floating-point ABIs, memory configurations, and feature sets. CI should verify that each supported configuration uses the intended linker script and startup/runtime libraries.

Host sanitizer jobs complement target builds because many target environments cannot cheaply run ASan or UBSan. Target-specific smoke tests remain necessary for MMIO, interrupts, DMA, cache, and timing.

## Edge cases and failure modes
- Matrix combinations are duplicated but not actually distinct.
- Important axes are omitted because “we always build release.”
- Toolchain versions drift between jobs.
- A failing configuration is silently allowed to continue forever.
- CI tests host behavior but never boots the target image.
- Generated artifacts differ between matrix jobs due to hidden environment state.

## Verification / debugging
Document why each matrix axis exists. Cache dependencies without allowing stale inputs to escape the dependency graph. Publish compiler versions, flags, map files, test results, warnings, static-analysis findings, and firmware hashes as artifacts.

## Performance, memory, timing and power
Release matrix jobs should include flash/RAM budgets and, where feasible, target timing benchmarks. Compiler changes can alter performance even when functional tests pass. Track regressions against a known baseline.

## Staff-level takeaway
CI should encode the organization's definition of “supported.” A small, intentional matrix with strong quality gates is more valuable than a huge matrix whose failures are routinely ignored.