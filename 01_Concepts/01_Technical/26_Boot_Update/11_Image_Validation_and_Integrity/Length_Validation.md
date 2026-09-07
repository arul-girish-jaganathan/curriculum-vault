# Length Validation

## Purpose
Develop a practical, engineering-grade understanding of **Length Validation** within the boot and firmware-update lifecycle.

## Core Model
- **State:** identify the current boot/update state and the persistent metadata that records it.
- **Trust:** identify the trust anchor, verification boundary, and security assumptions.
- **Artifact:** identify the image/package/metadata being consumed and how it is validated.
- **Transition:** define how the system moves between states and what makes the transition atomic or reversible.
- **Failure behavior:** define detection, containment, rollback, recovery, and safe-state behavior.

## Key Questions
1. What must be true before this stage can execute?
2. What hardware, firmware, storage, network, key, or configuration dependencies exist?
3. What exact data proves the next stage/image is valid and compatible?
4. What happens on reset, watchdog, brownout, power loss, corruption, interruption, or timeout?
5. Can the device recover without human intervention?

## Contracts
Define:
- image/header/manifest format;
- version and compatibility rules;
- memory and storage ownership;
- boot arguments and configuration;
- cryptographic trust requirements;
- timing and watchdog expectations;
- persistent state semantics;
- rollback and recovery policy.

## Failure Modes
Consider:
- wrong boot source;
- corrupt or incomplete image;
- invalid address or memory layout;
- signature/key/trust failure;
- version or hardware incompatibility;
- power loss during write or activation;
- repeated boot failure;
- watchdog reset;
- damaged boot metadata;
- storage exhaustion or wear;
- network interruption;
- compromised signing/update infrastructure.

## Debugging and Evidence
Useful evidence includes:
- reset cause and boot counters;
- early console output;
- image headers/manifests;
- hashes/signatures and verification results;
- slot/boot metadata;
- register state and memory maps;
- flash contents;
- boot traces;
- update logs and telemetry;
- exact firmware/toolchain/release identifiers.

## Security and Trust
Separate:
- integrity from authenticity;
- verified boot from measured boot;
- transport security from image security;
- device identity from signing authority;
- development/debug access from production trust.

Use fail-closed decisions where a security invariant must not be bypassed.

## Recovery
A robust design defines explicit recovery triggers, recovery images or paths, watchdog behavior, retry limits, rollback conditions, and persistent evidence. Recovery should not silently weaken the security or compatibility policy.

## Testing
Verify positive and negative cases:
- valid and invalid images;
- signature and key failures;
- version/downgrade attempts;
- power cuts during download/write/activation;
- storage corruption;
- network interruptions;
- reset/watchdog at every major state transition;
- repeated failures and boot loops;
- board and hardware revision differences.

## Performance and Resource Impact
Consider boot-stage latency, signature verification cost, hashing/decompression time, flash programming rate, download bandwidth, RAM required for staging, power during update, watchdog windows, and storage endurance.

## Embedded Consequences
Boot/update behavior is tightly coupled to linker scripts, flash layout, vector tables, bootloader/application boundaries, DDR/clock/power initialization, DMA/cache behavior, hardware revisions, manufacturing provisioning, and field recovery.

## Common Mistakes
- Treating the bootloader as simple code without a state machine.
- Updating an image without defining atomic activation.
- Assuming transport encryption provides firmware authenticity.
- Failing to plan power loss at every persistent-state transition.
- Implementing rollback without anti-rollback policy.
- Rotating keys without a migration/recovery path.
- Designing recovery paths that are less secure than the normal boot path.

## Staff-Level View
Treat boot and update as one lifecycle architecture: immutable trust, image format, validation, activation, persistence, recovery, fleet rollout, observability, and incident response must work together. The real objective is not merely “successful flashing,” but a device that remains bootable, trustworthy, recoverable, and maintainable throughout its field lifetime.
