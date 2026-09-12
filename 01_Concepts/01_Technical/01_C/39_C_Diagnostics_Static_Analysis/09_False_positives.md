# False positives

## Definition
A **false positive** is a diagnostic that reports a defect pattern that is not actually a defect in the analyzed program under its real assumptions. Managing false positives is essential because excessive noise causes engineers to ignore or suppress useful findings.

## Scope and boundaries
A finding can be technically plausible under the analyzer's model while being impossible under a documented hardware or API invariant. The correct response is not automatically “the tool is wrong”; first determine which assumption differs between tool and system.

## Mechanism and language rules
Common causes include incomplete interprocedural knowledge, function-pointer targets, generated code, macros, unknown external effects, conservative alias analysis, missing annotations, and configuration-dependent behavior.

A useful triage classification is:

```text
true defect | false positive | intentional/deviation | tool/configuration issue
```

## Embedded implications
Hardware guarantees frequently create assumptions that general static analyzers cannot infer: a register has a constrained range, an address is aligned by linker placement, an ISR cannot run during a critical section, or a bootloader guarantees a structure version. These assumptions should be documented and, where possible, encoded as assertions or analyzer contracts.

## Edge cases and failure modes
- Blanket suppression of a noisy rule.
- Marking a real defect as false because the hardware “usually” guarantees something.
- Configuration mismatch causing the analyzer to see the wrong code path.
- A generated wrapper hides a real unsafe operation.
- False-positive rates are measured, but false negatives are ignored.

## Verification / debugging
For each disputed finding, identify the analyzer assumption and provide evidence. Improve the analyzer model, add a precise annotation, constrain the input, or document a deviation. Track recurring false positives by rule and module to identify systemic configuration problems.

## Performance, memory, timing and power
False-positive management has no target runtime cost but significantly affects engineering throughput. Reducing noise allows more CPU time to be spent investigating high-consequence defects.

## Staff-level takeaway
The objective is not the lowest finding count; it is the **highest useful signal**. Treat every suppression as a statement about an invariant that should have evidence behind it.