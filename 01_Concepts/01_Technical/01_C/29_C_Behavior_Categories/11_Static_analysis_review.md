# 11: Static Analysis Review

## Definition
Static Analysis Review refers to the systematic evaluation of C source code using automated static analysis tools (e.g., Clang-Tidy, Coverity, Polyspace, PC-lint, CodeQL) to detect constraint violations, undefined behavior paths, security vulnerabilities, and style infractions without executing the code.

## Scope and Boundaries
- **Covers:** Automated static analysis tool suites, rule checkers (MISRA C, CERT C), syntax tree inspection, and vulnerability hunting.
- **Does not cover:** Dynamic runtime sanitizers (ASan/UBSan) or manual compiler diagnostics.

## Why Does It Exist
Human code reviewers miss subtle undefined behavior and security edge cases:
- **Exhaustive AST Inspection:** Static analyzers construct complete abstract syntax trees and call graphs, exploring execution paths across entire codebases.
- **Standard Compliance:** Automated checkers enforce rigorous automotive and aerospace coding standards like MISRA C:2012 and SEI CERT C.

## Mechanism and Language Rules
- **Pattern Matching & Data Flow:** Analyzers perform data flow analysis to track uninitialized variables, null pointer dereference paths, and buffer overflows.
- **Zero False Positives Goal:** Production static analysis pipelines configure rule sets to minimize noise and highlight high-confidence defects.

## Examples
```c
/* Static analyzers flag potential null pointer dereferences */
#include <stdlib.h>
#include <stdint.h>

void process_buffer(size_t len) 
{
    uint8_t *buf = (uint8_t *)malloc(len);
    
    /* Static analyzer flags missing null check on buf! */
    buf[0] = 0xAA; /* Potential null pointer dereference UB */
    
    free(buf);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **UB Identification:** Static analyzers excel at flagging latent undefined behavior paths (e.g., shift counts exceeding bit widths, invalid pointer arithmetic).

## Edge Cases and Failure Modes
- **False Positives / Alert Fatigue:** Poorly configured static analysis tools generate thousands of false positive warnings, causing developers to ignore the output entirely.

## Embedded Implications
- **MISRA Compliance Gates:** Embedded CI/CD pipelines use static analyzers as mandatory gating mechanisms to block non-compliant code from merging.

## Firmware Review Angle
- **Integrate Static Analysis:** Ensure static analysis is embedded directly into build pipelines, running on every pull request with zero tolerance for high-severity rule violations.

## Compiler, ABI, and Toolchain Implications
- **Compilation Database:** Modern static analyzers leverage `compile_commands.json` compilation databases to analyze exact compiler flags and include paths.

## Performance, Memory, Timing, and Power
- **Build-Time Cost:** Static analysis increases build time significantly, but runs asynchronously in CI/CD server runners without affecting target firmware execution performance.

## Verification / Debugging
- **Suppressions:** Where false positives occur, use tool-specific suppression annotations (e.g., `// cppcheck-suppress ...`) accompanied by detailed engineering justifications.

## Safety, Security, and Reliability
- **Certification Prerequisite:** Static analysis compliance reports are mandatory deliverables for functional safety certifications (ISO 26262, DO-178C, IEC 62304).

## Trade-offs and Alternatives
- **Static vs. Dynamic Analysis:** Static analysis inspects all possible paths at build time but can produce false positives; dynamic sanitizers test actual execution paths with zero false positives but require test coverage.

## Staff-Level Takeaway
Static analysis is your automated safety net. Combine strict compiler warnings with advanced static analyzers and MISRA C checks to catch undefined behavior before code ever reaches hardware.

## Related Concepts
- [[00_Chapter_Index]]
- [[04_Undefined_behavior]]
- [[05_Constraint_violations]]
- [[08_Compiler_diagnostics]]
