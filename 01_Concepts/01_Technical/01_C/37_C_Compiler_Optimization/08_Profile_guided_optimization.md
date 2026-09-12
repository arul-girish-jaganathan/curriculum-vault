# Profile-guided optimization

> Canonical C topic note — chapter 37.

## Definition
Profile-guided optimization (PGO) uses measured execution profiles to guide compiler decisions such as inlining, branch layout, hot/cold partitioning, and code placement. It is an implementation/toolchain technique, not part of ISO C.

## Mechanism and language rules
A representative workflow is instrumented build → representative workload → profile collection → optimized rebuild using profile data. Sampling-based approaches can obtain similar information without instrumentation. The quality of the workload matters because the compiler is optimizing for observed behavior.

PGO can improve instruction-cache locality and branch prediction by identifying likely paths. It can also change which functions are inlined and how cold error paths are laid out.

## Embedded implications
PGO is useful when a firmware product has stable workloads and tight CPU/flash constraints. However, a profile from a lab may not represent field conditions, startup, fault recovery, low-power transitions, or worst-case real-time paths. Instrumentation can distort timing and memory use.

For safety-critical firmware, PGO should be treated as a controlled build input with reproducible provenance. Do not optimize away rare safety paths merely because they were absent from the profile; compiler optimization must still preserve their defined semantics.

## Edge cases and failure modes
- Training on unrealistic traffic.
- Using stale profile data after major source changes.
- Optimizing average behavior while worsening worst-case latency.
- Letting instrumentation affect timing-sensitive measurements.
- Failing to archive profile-generation configuration with the release.

## Verification / debugging
Measure before and after PGO on representative targets and workloads. Compare code size, hot-path cycles, branch behavior, interrupt latency, and worst-case timing. Rebuild deterministically from the same source/toolchain/profile inputs.

## Staff-level takeaway
PGO converts production-like behavior into optimization evidence. The engineering question is not “does PGO make it faster?” but “is the profile representative of the workload and compatible with the system's worst-case and release-governance requirements?”

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
