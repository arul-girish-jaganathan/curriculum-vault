# fallthrough annotations

> Canonical C topic note — chapter 35.

## Definition
A fallthrough annotation documents an intentional transition from one `switch` case to the next without a `break`, allowing compilers and static analyzers to distinguish deliberate control flow from a likely defect. C23 standardizes the `[[fallthrough]]` attribute for this purpose; compiler-specific annotations existed earlier.

## Mechanism and language rules
A normal switch case can fall through:
```c
switch (state) {
case START:
    init_hw();
    /* intentional fallthrough */
case RUN:
    service_hw();
    break;
}
```
In C23, `[[fallthrough]];` is an attribute declaration that communicates intent. It does not itself perform control flow; removing it does not change the machine-level branch semantics.

The annotation is therefore different from `break`: `break` changes execution, while `[[fallthrough]]` documents existing execution.

### What to reason about
- Verify that the annotation is attached where the selected language mode permits it.
- Make the fallthrough path obvious and minimal.
- Do not annotate an accidental missing `break` merely to silence warnings.
- Check compiler/static-analyzer behavior across supported versions.

## Embedded implications
Fallthrough is useful in state machines and command decoders where several states intentionally share processing. Clear annotations reduce maintenance risk without adding runtime cost.

In safety-sensitive firmware, prefer explicit grouping or helper functions when fallthrough would make state transitions difficult to review. The important property is that reviewers can prove exactly which cases execute which side effects.

### Firmware review angle
Treat new fallthrough as a control-flow review item. Compare optimized assembly only when timing matters; the annotation itself should not materially affect runtime code generation.

## Edge cases and failure modes
A common defect is a missing `break` caused by inserting code into an existing case. Another is placing a comment that says “fallthrough” but using a spelling unsupported by the project's analyzer, producing either a false warning or false confidence.

Be especially careful when declarations, initialization, or cleanup are introduced between cases.

## Example pattern
```c
switch (event) {
case RX_HEADER:
    parse_header();
    [[fallthrough]];
case RX_PAYLOAD:
    parse_payload();
    break;
case RX_ERROR:
    recover_link();
    break;
}
```

## Verification / debugging
Compile with `-Wimplicit-fallthrough`-style diagnostics where supported and require intentional transitions to use the project's standard annotation. Add branch-coverage tests proving both the fallthrough and non-fallthrough paths.

## Staff-level takeaway
An intentional fallthrough is a control-flow contract for humans and tools. The best annotation is one that makes a future maintainer immediately understand that the missing `break` is deliberate.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
