# Assessment

## Purpose
Build an engineering-grade understanding of **Assessment** for compliance, functional safety, medical-device software lifecycle, medical-device risk management, and FMEA work.

## Scope and Context
Identify the product, lifecycle phase, applicable standard or process, artifact, responsibility, assumptions, and boundaries involved.

## Core Model
- **Claim or objective:** what is being asserted, controlled, verified, or assessed.
- **Risk/failure context:** what hazard, failure mode, nonconformity, or process weakness is relevant.
- **Control:** what design, process, analysis, review, or test reduces the risk.
- **Evidence:** what objective record demonstrates implementation and effectiveness.
- **Traceability:** what upstream/downstream artifacts must remain linked.

## Engineering Questions
1. What exact requirement, hazard, failure mode, risk, or compliance objective is addressed?
2. Which lifecycle process owns it?
3. What evidence demonstrates that the requirement/control has been implemented and verified?
4. Which assumptions or dependencies could invalidate the conclusion?
5. What change would require impact analysis, regression, reassessment, or re-approval?

## Evidence
Typical evidence includes requirements/baselines, architecture/design records, HARA/FMEA/FTA/FMEDA where applicable, source/configuration records, reviews, static analysis, test results, problem reports, CAPA, release records, and assessment/audit records.

## Risk and Failure Reasoning
Distinguish hazard, hazardous situation, harm, fault, error, failure, failure mode, cause, effect, risk estimation, risk evaluation, risk control, and residual risk. Do not treat a checklist item, rating, or document existence as proof that the underlying risk is controlled.

## Verification and Validation
1. Define the requirement/risk/control.
2. Define acceptance criteria.
3. Implement the design/process response.
4. Execute analysis, inspection, test, or review.
5. Record result and configuration identity.
6. Assess anomalies and residual risk.
7. Update traceability and release status.

## Change Impact
Consider functional behavior, hazards/failure modes, classification/ASIL or software-class implications where applicable, risk controls, interfaces, tests/coverage, configuration, supplier/COTS/SOUP implications, and released evidence.

## Cross-Standard Discipline
ISO 26262, IEC 62304, ISO 14971, and FMEA practices overlap in structured lifecycle evidence, traceability, risk reasoning, verification, and change control, but they are not interchangeable. Preserve each standard's own scope, terminology, classification logic, and normative obligations.

## Common Mistakes
- Confusing compliance with proof of safety.
- Copying terminology between standards without checking scope.
- Treating risk ratings as objective truth without defined criteria.
- Updating design artifacts without updating risk/traceability.
- Closing actions without verifying effectiveness.
- Accepting supplier claims without assumptions and evidence.
- Maintaining documents that no longer match the released product.

## Embedded/Software Considerations
For firmware and embedded products, consider memory safety, deterministic timing, concurrency, watchdogs, diagnostics, hardware/software partitioning, boot/update behavior, toolchain configuration, third-party software, and field updates when they affect the applicable claims.

## Staff-Level View
Treat compliance as an evidence architecture around engineering decisions: connect requirements, hazards/failures, controls, architecture, implementation, verification, configuration, change impact, and field feedback into a coherent, reviewable argument.
