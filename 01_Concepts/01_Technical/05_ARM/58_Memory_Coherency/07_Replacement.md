# 58.07 Replacement

## Core idea

Caches reduce latency but introduce locality, invalidation, coherency and determinism considerations.

This note is the canonical home for **Replacement** inside **Cache Coherency and Multi-Core Memory**. Other notes should link here instead of repeating this explanation.

## Mechanism

The architecture is best understood through four layers:

```text
instruction / register operation
        ↓
architectural state transition
        ↓
memory / exception / privilege effects
        ↓
observable software or hardware behavior
```

Caches reduce latency but introduce locality, invalidation, coherency and determinism considerations. The architectural contract should be stated before the implementation detail.
Separate architecture guarantees from microarchitectural behavior and SoC integration choices.
For concurrency or shared-memory behavior, distinguish atomicity, visibility, ordering and coherency.
For fault/debug work, collect architectural state before changing configuration or restarting the target.
For performance work, measure the actual implementation and workload instead of inferring cost from opcode names alone.

## Canonical example

```asm
// Illustrative ARM-style pseudocode/assembly shape
MOV     w0, #1
ADD     w1, w0, #2
STR     w1, [x2]
```

The exact instruction legality, operand width and addressing form must be checked against the target execution state and ISA version.

## Boundary cases

- Reset or first-use state.
- Maximum/minimum operand values.
- Alignment boundary.
- Exception or interrupt arriving between operations.
- Concurrent access by another CPU or DMA agent.
- Security-state or privilege transition.
- Cache/TLB state different from the nominal test.
- Unsupported or optional architectural feature.

## Failure modes

Typical failures arise when software assumes a microarchitectural behavior is architectural, when memory ordering is inferred from one core's observation, when a cache-coherent assumption is applied to a non-coherent DMA path, or when an exception frame/register convention is misread.

## Debugging

Capture:
1. PC/instruction address.
2. Relevant general-purpose/system registers.
3. Fault syndrome/status.
4. Memory attributes and translation state when relevant.
5. Interrupt/security/exception context.
6. Target revision and enabled architectural extensions.

Disassembly, debugger register views, CoreSight trace and PMU evidence answer different questions and should be combined rather than substituted for one another.

## Verification

Use:
- architectural reference documentation;
- assembler/disassembler round trips;
- cycle/performance measurements on the real core;
- fault injection where applicable;
- stress tests for concurrency;
- hardware-in-the-loop validation for MMIO/DMA/interrupt behavior.

## Performance and resource analysis

For embedded ARM systems, track:
- cycles;
- worst-case latency;
- interrupt latency;
- instruction and data cache behavior;
- TLB behavior;
- memory bandwidth;
- code size;
- stack usage;
- power/wakeup cost.

Do not label an instruction or feature “fast” without identifying the target implementation and workload.

## Embedded perspective

Ask whether the feature runs during boot, normal task execution, interrupt context, secure context, hypervisor context or power-management transitions. The safe design space changes with execution context.

## Staff-level review

- What requirement drives the feature?
- Which ARM profile and architectural revision is assumed?
- Which properties are architectural versus implementation-specific?
- What happens on the failure path?
- What is the worst-case timing/resource cost?
- How is behavior observed in production?
- How does the design change on a different Cortex/SoC?

## Related

- [[../01_ARM_Overview/00_Chapter_Index|ARM Architecture Overview]]
- [[22_Memory_Types/00_Chapter_Index|Memory Types]]
- [[30_EXceptions_Overview/00_Chapter_Index|Exceptions]]
- [[40_Debug_Architecture/00_Chapter_Index|Debug Architecture]]
- [[84_ISA_Compiler/00_Chapter_Index|Compiler to ISA]]
- [[90_Staff_ARM/00_Chapter_Index|Staff-Level ARM]]

## Source

Primary architectural reference: https://developer.arm.com/documentation/
