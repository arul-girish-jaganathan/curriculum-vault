# AI Maintenance Plan

## Purpose

This repository is maintained as a long-term Obsidian knowledge base. Repository-wide maintenance must be evidence-driven, reproducible, reviewable, and conservative with existing knowledge.

## Current state

- Repository: `arul-girish-jaganathan/curriculum-vault`
- Default branch: `master`
- Current maintenance branch: `work/ai-maintenance-2026-09`
- GitHub currently reports repository size at approximately 25 MB; this is repository metadata size, not a count of Markdown files.
- Copilot credits are exhausted; maintenance is therefore being continued with direct GitHub repository tooling where possible.
- The maintenance branch is 12 commits ahead of `master` and has not been merged.
- The repository has not been declared globally complete or fully audited.

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

## Validation caveats

The repository contains maintenance scripts intended to support repository-wide checks, but their results must be treated according to what they actually implement. In particular:

- Orphan detection based on incoming wikilinks can flag legitimate entry points.
- Filename/stem duplicate detection does not prove semantic duplication.
- Wikilink validation must account for note stems, relative paths, headings, aliases, and Obsidian resolution semantics.
- A validator that merely prints findings is not equivalent to a passing quality gate.
- A report is not evidence of complete execution unless it was actually run against the repository revision being audited.
- GitHub API inspection may be unable to execute repository-local scripts; GitHub Actions is the canonical execution path when enabled.

## Domain completion standard

A domain can only be marked `VALIDATED` when its substantive canonical topics have been reviewed and developed to an appropriate depth, cross-links are validated, indexes are synchronized, obvious placeholders are resolved or explicitly staged, and the resulting evidence is recorded in repository status/change logs.

A roadmap, file count, or previous agent completion message is not evidence of substantive completion.
