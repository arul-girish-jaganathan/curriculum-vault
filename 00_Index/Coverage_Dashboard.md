---
title: "Coverage Dashboard"
type: "index"
status: "active"
purpose: "Track curriculum completeness, content quality, interview coverage, and evidence gaps."
last_updated: "2026-09-05"
---

# Coverage Dashboard

> [!summary]
> This page answers: **Have we actually covered the curriculum, and where are the gaps?**

## 1. Coverage Definitions

- **Concept Coverage** — planned concepts that have been created
- **Quality Coverage** — created concepts reviewed/canonicalized
- **Question Coverage** — distinct questions completed in the 100-question bank
- **Evidence Coverage** — project/debug/design evidence linked to the domain

## 2. Master Dashboard

| # | Domain | Planned | Created | Reviewed | Canonical | Coverage | Q100 | Evidence | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 01 | Embedded C | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 02 | Embedded C++ | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 03 | DSA | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 04 | Computer Architecture | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 05 | ARM | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 06 | Embedded Systems | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 07 | Memory | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 08 | OS | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 09 | RTOS | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 10 | Linux | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 11 | Concurrency | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 12 | Interrupts & Timing | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 13 | Drivers & BSP | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 14 | Protocols | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 15 | Debugging | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 16 | Performance | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 17 | Power & Thermal | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 18 | Security | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 19 | Safety & Reliability | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 20 | Testing | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 21 | System Design | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 22 | Software Architecture | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 23 | Design Patterns | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 24 | Toolchain | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 25 | HW/SW Integration | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 26 | Boot & Update | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 27 | Storage | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 28 | Networking | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 29 | DSP | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |
| 30 | Engineering Leadership | — | 0 | 0 | 0 | 0% | 0/100 | None | Not Started |

## 3. 100-Question Standard

| Question Class | Target |
|---|---:|
| Foundation / mechanics | 20 |
| Senior application | 20 |
| Staff reasoning | 20 |
| Debugging / failure analysis | 15 |
| System / design | 15 |
| Principal extension | 10 |
| **Total** | **100** |

A question only counts if it tests a meaningfully different skill, mechanism, scenario, failure mode, or design decision.

## 4. Gap Types

- `CONCEPT` — missing concept
- `DEPTH` — shallow explanation
- `MECHANISM` — internals unclear
- `CODE` — implementation missing
- `DEBUG` — failure analysis missing
- `PERF` — performance missing
- `TIMING` — timing/determinism missing
- `POWER` — power missing
- `SECURITY` — security missing
- `SAFETY` — safety/reliability missing
- `DESIGN` — design reasoning missing
- `TRADEOFF` — alternatives/trade-offs missing
- `EVIDENCE` — no personal/project evidence
- `SOURCE` — source/verification needed
- `DUPLICATE` — content duplicated elsewhere

## 5. Completion Criteria

A domain should not be marked complete until:

- [ ] Planned concepts are covered
- [ ] Core mechanisms are explained
- [ ] Examples/code exist where useful
- [ ] Failure modes are covered
- [ ] Debugging approach exists
- [ ] Timing/resource/performance implications are covered
- [ ] Trade-offs are covered
- [ ] 100-question bank is complete
- [ ] Project evidence is linked where applicable
- [ ] Important claims have appropriate sources
- [ ] Major duplicates are removed
