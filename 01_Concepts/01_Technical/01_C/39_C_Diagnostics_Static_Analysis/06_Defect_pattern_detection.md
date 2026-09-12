# Defect pattern detection

## Definition
**Defect pattern detection** identifies source constructs that frequently correlate with bugs, vulnerabilities, or maintainability failures. Unlike purely syntax-oriented warnings, pattern detection encodes engineering knowledge such as unchecked return values, suspicious memory operations, dangerous conversions, missing bounds checks, or incorrect API sequences.

## Scope and boundaries
A pattern is evidence, not proof. The same construct can be valid in one context and defective in another. High-quality rules therefore combine syntax, types, control flow, dataflow, and project-specific contracts.

## Mechanism and language rules
Examples include:

```c
memcpy(dst, src, len); /* rule asks: are dst/src/len mutually valid? */
```

A strong analyzer can trace `len` to determine whether it is bounded by the destination size. Other patterns include unchecked allocator results, use-after-close/resource misuse, suspicious shifts, integer truncation, ignored error codes, and incorrect locking sequences.

## Embedded implications
Firmware-specific patterns include ISR calling blocking APIs, accessing non-reentrant drivers from multiple contexts, writing read-only configuration, unsafe DMA buffer ownership, missing timeout handling, unchecked hardware status, and incorrect register read-modify-write sequences. Project-specific APIs should be modeled so the analyzer understands ownership and preconditions.

## Edge cases and failure modes
- A simple syntactic pattern generates many irrelevant findings.
- A dangerous operation is hidden behind a wrapper the analyzer does not understand.
- Macros produce different code in different configurations.
- Generated/vendor code overwhelms application findings.
- A suppression hides a recurring architectural defect.

## Verification / debugging
Prioritize rules by consequence and confidence. Validate high-severity findings through code review, targeted tests, or a minimal reproducer. Add custom rules for repeated defects found in incident reviews, then measure whether the rule catches future instances without excessive noise.

## Performance, memory, timing and power
Static pattern checks add analysis time but no target runtime cost. Preventing a memory or concurrency defect can save substantial debug and field-recovery effort.

## Staff-level takeaway
Turn recurring defects into **executable engineering knowledge**. When a bug appears repeatedly, ask whether its pattern can be detected automatically and enforced at the earliest practical stage.