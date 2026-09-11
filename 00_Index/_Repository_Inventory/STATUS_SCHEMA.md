# Repository Status Schema

This document defines evidence states used by maintenance automation.

## File state

- `empty`: no non-whitespace content.
- `placeholder`: content is detected as template/scaffold by heuristic rules.
- `meaningful`: contains substantive text according to current analyzer heuristics.
- `index`: navigation or index-like Markdown file.
- `contextual`: useful non-canonical content such as project/bridge/reference material.
- `canonical`: authoritative single-concept note selected after semantic review.

## Validation state

- `UNVERIFIED`: not independently checked.
- `SCANNED`: included in automated repository analysis.
- `REVIEW_REQUIRED`: automated scan found something needing semantic review.
- `VALIDATED`: relevant automated checks and human-quality review support the recorded claim.

## Important principle

Automated classification is evidence, not truth. A script may identify candidates; semantic ownership, canonical status, duplication, and content quality require review.
