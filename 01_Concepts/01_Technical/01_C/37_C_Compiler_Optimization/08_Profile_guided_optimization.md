# Profile-guided optimization

## Definition
**Profile-guided optimization (PGO)** uses measured execution behavior to guide compiler decisions. Instead of optimizing solely from static heuristics, the compiler can learn which branches are hot, which functions are frequently called, and which paths dominate execution, then optimize code layout and transformations accordingly.

## Scope and boundaries
PGO is implementation-specific. Typical workflows instrument a build, execute representative workloads, collect profile data, and rebuild using that profile. The profile is only useful if the workload represents real product behavior; optimizing for an unrepresentative benchmark can make the deployed system worse.

## Mechanism and language rules
A conceptual workflow is:

```text
source -> instrumented build -> representative execution -> profile data -> optimized build
```

The compiler may use branch probabilities, call frequencies, value profiles, and hot/cold function information. It can influence inlining, block layout, code placement, register allocation, and other decisions.

### Correctness remains independent of the profile
A profile never grants permission to execute undefined behavior or violate a C contract. It changes optimization priorities, not semantics.

## Embedded implications
PGO can be useful for firmware with stable workloads such as protocol stacks, media pipelines, control algorithms, or boot/application split images. It can improve common-case latency and code locality. But embedded systems often have hard real-time requirements where optimizing the average path is insufficient. A rare but safety-critical path may need bounded timing even if it is cold in the profile.

Instrumentation itself can disturb timing, memory footprint, power, cache behavior, and interrupt latency. The collection environment therefore needs to be designed carefully.

## Edge cases and failure modes
- Training data does not represent field workloads.
- Instrumentation changes timing enough to alter behavior.
- Rare safety/fault paths become heavily deprioritized.
- Profile data becomes stale after major source or configuration changes.
- Build reproducibility is weakened if profiles are not versioned and associated with the exact source/toolchain.

## Verification / debugging
Record the source revision, compiler version, target configuration, workload, and profile-generation method. Compare optimized and non-PGO binaries using size reports, disassembly, branch statistics, and target measurements. Test cold paths explicitly rather than assuming they remain correct because they were rarely executed during training.

## Performance, memory, timing and power
PGO can improve hot-path instruction locality and reduce branch misprediction on capable CPUs. It may increase code complexity or move cold paths into separate regions. On MCUs without sophisticated branch prediction, gains may come mainly from layout and inlining rather than prediction. Measure worst-case latency, not only average throughput.

## Staff-level takeaway
PGO is valuable when you can define a representative workload and an objective measurement. Treat profile data as an engineering artifact with provenance, not as an invisible compiler setting. In real-time firmware, combine average-case optimization with explicit worst-case timing validation.