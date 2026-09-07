# Device Cache

## Purpose
Develop a practical, engineering-grade understanding of **Device Cache** as part of an embedded and systems storage architecture.

## Core Model
- **Data:** what information is stored, its size, layout, ownership, and lifetime.
- **Media:** the physical or virtual storage mechanism and its limits.
- **Path:** application -> filesystem or API -> block/MTD layer -> driver/controller -> media, as applicable.
- **Consistency:** what must survive crashes, resets, power loss, or partial operations.
- **Performance:** latency, throughput, queueing, bandwidth, CPU cost, memory cost, and background work.
- **Reliability:** endurance, retention, corruption, recovery, redundancy, and field lifetime.

## Key Questions
1. What are the capacity, latency, throughput, endurance, retention, and power requirements?
2. Where is the authoritative state kept?
3. What happens during partial writes, reset, power loss, timeout, media failure, or firmware update?
4. Which layer owns ordering, caching, retries, integrity, and recovery?
5. What evidence proves the design behaves correctly on the real target?

## Data and Ownership
Define:
- logical versus physical addressing;
- block/page/erase-block relationships;
- buffer ownership and DMA lifetime;
- metadata and versioning;
- persistent state transitions;
- synchronization and durability semantics.

## Failure Modes
Consider:
- media wear and bad blocks;
- ECC correction and uncorrectable errors;
- read/program/erase failures;
- power-loss corruption;
- torn writes and stale metadata;
- filesystem inconsistency;
- controller reset or timeout;
- queue saturation;
- thermal throttling;
- storage exhaustion;
- incompatible update or migration.

## Debugging and Evidence
Useful evidence includes:
- block/MTD/NVMe/UFS/eMMC traces;
- filesystem metadata and mount state;
- I/O latency distributions;
- queue depth and completion timing;
- media health information;
- bad-block/ECC counters;
- flash contents and metadata;
- power-cut and reset evidence;
- exact software, firmware, board, and media revision.

## Integrity and Recovery
Separate:
- data integrity from durability;
- filesystem consistency from application correctness;
- transport errors from media errors;
- detection from recovery.

For persistent metadata, define atomic commit points, versioning, checksums, redundant records, rollback, and recovery behavior.

## Performance
Analyze the full data path rather than one layer. Consider:
- caching and writeback;
- queue depth and schedulers;
- read-ahead;
- DMA and copies;
- memory bandwidth;
- flash program/erase latency;
- write amplification;
- garbage collection;
- thermal and power effects.

## Reliability and Endurance
Account for:
- write volume and workload shape;
- wear leveling;
- spare/overprovisioned capacity;
- retention temperature;
- ECC margin;
- program/erase cycles;
- power-cycle count;
- background scrubbing;
- field health monitoring.

## Security
Where relevant, include encryption, integrity protection, key storage, access control, secure erase, debug access, device identity, and secure update. Do not assume encryption automatically provides integrity or recovery.

## Embedded Consequences
Storage design is tightly coupled to boot, OTA, linker/image layout, manufacturing provisioning, RAM constraints, power-loss behavior, DMA/cache coherency, RTOS/Linux stacks, and field diagnostics.

## Testing
Validate:
- normal read/write behavior;
- full and near-full media;
- power loss at critical points;
- bad blocks and ECC events;
- resets during I/O;
- long endurance/soak workloads;
- performance under queue pressure;
- thermal and voltage corners;
- filesystem recovery;
- update/rollback scenarios.

## Common Mistakes
- Treating nominal capacity as usable capacity.
- Benchmarking only empty or freshly formatted media.
- Ignoring cache state and queue depth.
- Assuming `fsync()` alone proves end-to-end durability without understanding the storage stack.
- Ignoring flash translation layers and write amplification.
- Treating a filesystem as the whole storage architecture.
- Designing recovery without testing actual interrupted writes.

## Staff-Level View
Treat storage as a lifecycle architecture spanning data semantics, media physics, controllers, software layers, integrity, performance, endurance, security, recovery, and field observability. The goal is durable system behavior across years of writes, failures, updates, and hardware variation.
