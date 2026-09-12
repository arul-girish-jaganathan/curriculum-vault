# Suppression discipline

## Definition
**Suppression discipline** is the controlled process for silencing a diagnostic only when the finding is understood, the underlying code is intentionally acceptable, and the exception is documented and bounded. Suppression is a risk decision, not a cleanup operation.

## Scope and boundaries
Suppression mechanisms are tool-specific: source annotations, configuration files, generated-code filters, or command-line options. Prefer the narrowest mechanism that does not hide unrelated findings.

## Mechanism and language rules
A useful suppression record contains:

```text
rule/finding + location + reason + invariant/evidence + owner + review condition
```

For example, a deliberate conversion may be acceptable because a validated protocol field is known to fit a smaller type. The evidence should be explicit rather than “this is safe.”

## Embedded implications
Firmware commonly has justified exceptions for register access, compiler extensions, packed protocol formats, startup assembly, or vendor headers. These are exactly the areas where broad suppression can hide serious defects. Keep third-party suppression boundaries separate from application code.

## Edge cases and failure modes
- Global suppression for convenience.
- Suppression copied into unrelated code.
- A deviation survives after the implementation changes.
- Suppression reason describes syntax but not the safety invariant.
- Tool upgrades silently reinterpret suppression directives.

## Verification / debugging
Review suppressions periodically. Require owners for high-risk deviations. CI should detect malformed or stale suppressions where the analyzer supports it. Prefer a source-level wrapper or typed abstraction that eliminates repeated exceptions.

## Performance, memory, timing and power
Suppressions affect analysis time and signal quality, not target runtime. Eliminating the need for repeated exceptions can simplify code and reduce long-term maintenance cost.

## Staff-level takeaway
A suppression should read like a **mini design decision**: what was found, why it is acceptable, what proves that, and when the exception must be reconsidered.