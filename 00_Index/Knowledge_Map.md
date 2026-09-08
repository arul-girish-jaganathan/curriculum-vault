---
title: "Knowledge Map"
type: "index"
status: "active"
purpose: "Show how concepts depend on and reinforce one another."
last_updated: "2026-09-05"
---

# Knowledge Map

> [!summary]
> This is the **relationship map**, not another textbook. Canonical concept pages are the nodes; this page explains the important paths.

## 1. Core Learning Chain

```text
C / C++
   ↓
DSA
   ↓
Computer Architecture
   ↓
ARM
   ↓
Embedded Systems
   ↓
Memory
   ↓
OS / RTOS / Linux
   ↓
Concurrency + Interrupts + Timing
   ↓
Drivers + Protocols
   ↓
Debugging + Performance
   ↓
Power + Security + Safety + Testing
   ↓
System Design
   ↓
Software Architecture
   ↓
Staff Engineering Practice
```

## 2. Low-Level Foundation

```text
C
├── Pointers
├── Arrays
├── Object Lifetime
├── Function Pointers
├── Volatile
├── Atomics
└── Undefined Behavior
        ↓
Memory
├── Stack
├── Heap
├── Alignment
├── Fragmentation
└── Cache Effects
        ↓
DMA
        ↓
Cache Coherency
        ↓
Concurrency
```

## 3. Real-Time Path

```text
Interrupt
   ↓
ISR
   ↓
Deferred Work
   ↓
RTOS Scheduling
   ↓
Priority / Blocking
   ↓
Priority Inversion
   ↓
Worst-Case Timing
   ↓
Jitter / Deadline
   ↓
Determinism
```

## 4. Debugging Path

```text
Symptom
  ↓
Reproduce
  ↓
Collect Evidence
  ├── Logs
  ├── Registers
  ├── Trace
  ├── Logic Analyzer
  ├── Oscilloscope
  └── Debugger
  ↓
Form Hypotheses
  ↓
Eliminate Alternatives
  ↓
Root Cause
  ↓
Fix
  ↓
Regression
  ↓
Prevention
  ↓
Reusable Knowledge
```

## 5. Performance Path

```text
Requirement
  ↓
Latency / Throughput / Deadline
  ↓
Measure
  ↓
CPU + Memory + Cache + I/O + Concurrency
  ↓
Optimization
  ↓
Measure Again
  ↓
Regression Check
```

## 6. System Design Path

```text
Requirements
  ↓
Constraints
  ↓
Architecture
  ↓
Component Boundaries
  ↓
Interfaces
  ↓
Data Flow
  ↓
Concurrency
  ↓
Timing / CPU / Memory / Power Budgets
  ↓
Failure Modes
  ↓
Observability
  ↓
Testing
  ↓
Update / Maintenance
```

## 7. Cross-Domain Anchors

### Ownership

Typical links:

- [[Pointers]]
- [[Memory Lifetime]]
- [[DMA]]
- [[Concurrency]]
- [[Driver Architecture]]
- [[RAII]]

### Time

Typical links:

- [[Timers]]
- [[Interrupt Latency]]
- [[RTOS Scheduling]]
- [[Timeouts]]
- [[Counter Wraparound]]
- [[Jitter]]
- [[Deadline Analysis]]

### Determinism

Typical links:

- [[WCET]]
- [[Scheduling]]
- [[Interrupts]]
- [[Memory Allocation]]
- [[Lock Contention]]

### Failure & Recovery

Typical links:

- [[Watchdog]]
- [[Fault Handling]]
- [[Driver Recovery]]
- [[Boot Recovery]]
- [[Firmware Update]]
- [[Power-Loss Recovery]]

### Observability

Typical links:

- [[Logging]]
- [[Tracing]]
- [[Metrics]]
- [[Crash Dump]]
- [[Health Monitoring]]
- [[Debugging]]

## 8. Project-to-Concept Mapping

A project should strengthen several canonical concepts.

```text
Project
├── Performance issue
│   ├── Performance
│   ├── Cache
│   └── DMA
├── Concurrency issue
│   ├── RTOS
│   ├── Synchronization
│   └── Race Condition
└── Hardware issue
    ├── Protocol
    ├── Signal Integrity
    └── Debugging
```

## 9. Interview-to-Concept Mapping

Example:

```text
"Design a UART driver"
          ↓
UART
├── Driver Architecture
├── Interrupts
├── DMA
├── Ring Buffer
├── Concurrency
├── Error Recovery
├── Timing
└── Testing
```

Interview questions should point back to canonical concepts rather than duplicate them.

## 10. Graph Rules

1. Prefer meaningful links over excessive links.
2. Link concepts when understanding one improves understanding of another.
3. Do not link every noun.
4. Do not create empty placeholder notes just to make links.
5. Canonical concepts should remain the center of the graph.
6. Company-specific and project-specific notes should point into the graph.
