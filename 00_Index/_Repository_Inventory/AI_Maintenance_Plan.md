# AI Maintenance Plan

## Purpose

This repository is maintained as a long-term Obsidian knowledge base. Repository-wide maintenance must be evidence-driven, reproducible, reviewable, and conservative with existing knowledge.

## Current state

- Repository: `arul-girish-jaganathan/curriculum-vault`
- Default branch: `master`
- Current maintenance branch: `work/ai-maintenance-2026-09`
- Copilot credits are currently exhausted; repository maintenance is being continued with direct GitHub repository tooling until Copilot usage resets.

## Workflow

1. Inventory the actual filesystem.
2. Repair/verify maintenance automation.
3. Reconcile stale indexes and status dashboards with actual filesystem evidence.
4. Establish domain-level status from repository evidence, not old planning documents.
5. Process exactly one technical domain at a time.
6. Deepen canonical notes while preserving useful existing/contextual knowledge.
7. Validate links, duplicates, orphan status, placeholders, indexes, and unintended changes.
8. Commit coherent batches.
9. Repeat for the next domain.
10. Run cross-domain audits periodically.

## Non-negotiable quality rules

- Never claim complete/full audit/all files processed without programmatic evidence.
- Never fabricate standards, clauses, versions, URLs, or technical guarantees.
- Distinguish standard/language guarantees from compiler, ABI, hardware, OS/RTOS, and project-specific behavior.
- Prefer authoritative sources for externally verifiable technical claims.
- Do not blindly delete or consolidate existing knowledge.
- Avoid shallow AI-generated boilerplate.
- Prefer canonical concepts with contextual links over duplicated explanations.
- Use Obsidian wikilinks only when targets exist or are created intentionally.
- Keep indexes synchronized with the actual filesystem.
- Do not use obsolete curriculum plans as the authoritative domain list.

## Important caveats in existing automation

The original analyzer is useful but must not be treated as a perfect validator. In particular:

- The orphan detector is based on incoming wikilinks and can flag legitimate entry points.
- Duplicate detection is primarily normalized filename matching, not semantic equivalence.
- Wikilink validation currently reduces targets to note stems, which can create false positives/negatives for path-sensitive links and aliases.
- The current shell runner clones the repository into `/tmp` and therefore should not be treated as a canonical local CI mechanism until replaced or made deterministic.
- Repository status must be generated from the actual branch being audited.

These limitations must be repaired before relying on the reports for completion claims.

## Domain completion standard

A domain can only be marked complete when its substantive canonical topics have been reviewed and developed to an appropriate depth, cross-links are validated, indexes are synchronized, obvious placeholders are resolved or explicitly staged, and the resulting evidence is recorded in repository status/change logs.
