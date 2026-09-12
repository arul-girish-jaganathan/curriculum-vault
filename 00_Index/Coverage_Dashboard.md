---
title: "Coverage Dashboard"
type: "index"
status: "active"
purpose: "Track curriculum completeness, content quality, interview coverage, and evidence gaps."
last_updated: "2026-09-11"
---

# Coverage Dashboard

> [!summary]
> This page answers: **What is actually covered, what has been reviewed, and where are the evidence-backed gaps?**

## 1. Coverage Definitions

- **Planned** — topics represented by the actual repository curriculum/index structure, not an obsolete hard-coded domain list.
- **Created** — canonical/content files that exist.
- **Reviewed** — content explicitly reviewed for depth/technical integrity.
- **Canonical** — notes selected as the authoritative concept source after semantic review.
- **Quality status** — evidence-backed state recorded by the repository maintenance ledger.

## 2. Current Evidence State

| Scope | Evidence state | Notes |
|---|---|---|
| Repository inventory | SCANNED | Inventory and analysis tooling exists. |
| Maintenance automation | SCANNED | Initial analyzer plus deterministic checks exist; limitations are documented. |
| C domain | AUDIT_REQUIRED | Prior substantive work exists, but completion and validation were not independently established before Copilot credits were exhausted. |
| Other technical domains | NOT_STARTED / UNVERIFIED | Do not infer completion from the presence of skeleton files or old planning documents. |

## 3. Domain Status

The authoritative domain list is the actual filesystem under `01_Concepts/01_Technical/`.

Use `00_Index/_Repository_Inventory/DOMAIN_STATUS.md` for evidence-based domain state.

This dashboard intentionally does **not** hard-code the old 30-domain planning list because the repository has evolved beyond it.

## 4. Quality Gate

A domain must not be marked `VALIDATED` until evidence supports:

- actual topic structure reviewed
- substantive canonical notes developed where required
- useful existing knowledge preserved
- broken links checked
- duplicate candidates reviewed
- orphan candidates reviewed
- placeholder/empty files accounted for
- indexes/navigation synchronized
- technical claims checked for standard/compiler/ABI/hardware/OS distinctions
- relevant examples, mechanisms, failures, debugging, and trade-offs covered
- no accidental unrelated changes

## 5. Question / Interview Coverage

Question-bank completeness is tracked separately from concept coverage. A domain being technically developed does not imply that its question bank is complete.

## 6. Evidence Rules

Never mark a domain complete from:

- file count alone
- directory existence
- an agent's unverified completion message
- old planning documents
- placeholder generation

Completion requires repository evidence.
