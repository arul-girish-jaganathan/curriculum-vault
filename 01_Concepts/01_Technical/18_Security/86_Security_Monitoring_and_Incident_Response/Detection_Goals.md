# Detection Goals

## Purpose
Build a precise security mental model for **Detection Goals**, including what must be protected, what an attacker can influence, where trust changes, and which controls meaningfully reduce risk.

## Core Model
- **Asset / security property:** identify the data, capability, service, key, code, or availability objective at stake.
- **Attacker capability:** define remote/local/physical/privileged assumptions instead of relying on vague attacker models.
- **Trust boundary:** identify where untrusted input or lower-trust code crosses into a more privileged or sensitive component.
- **Security mechanism:** distinguish prevention, detection, containment, recovery, and compensating controls.
- **Evidence:** state what would prove the control is actually enforced.

## Threat Questions
1. What can an attacker control, observe, replay, corrupt, or exhaust?
2. What assumptions does the design make about identity, integrity, freshness, availability, or physical access?
3. Where is input parsed or interpreted?
4. Which component has the authority to enforce the security invariant?
5. What happens when a check fails, a key is unavailable, or a component is compromised?

## Attack Surface
Consider APIs, parsers, IPC, DMA, MMIO, debug ports, boot stages, update channels, network services, device nodes, firmware images, credentials, manufacturing interfaces, and dependencies as applicable.

## Security Controls
- Authenticate before trusting identity.
- Authorize every security-sensitive operation at the enforcement boundary.
- Validate untrusted data before use.
- Minimize privileges and isolate components.
- Protect secrets and keys with an explicit lifecycle.
- Use cryptographic primitives through reviewed libraries and correct protocols.
- Add integrity, replay, rollback, and provenance checks where required.
- Design failure behavior to avoid silently reducing security.

## Verification
A security control is credible when:
- its enforcement point is identified;
- negative tests demonstrate rejection of invalid states;
- privilege boundaries are exercised;
- malformed and adversarial inputs are tested;
- logs/telemetry can reveal important failures;
- production configuration preserves the intended security posture.

## Failure Modes
Common failures include missing authorization, parser confusion, trust-boundary violations, fail-open behavior, key leakage, rollback/downgrade acceptance, excessive privilege, unsafe debug access, race conditions, memory corruption, information disclosure, and insecure recovery paths.

## Embedded / Systems Considerations
For embedded products, explicitly consider boot ROM and bootloader trust, firmware authenticity, secure storage, debug lifecycle, DMA and peripheral isolation, interrupt-driven state changes, physical attack assumptions, OTA behavior, manufacturing provisioning, and field recovery.

## Tradeoffs
Security controls can affect performance, memory, boot time, power, debuggability, manufacturing cost, field-serviceability, and safety. Make the trade explicit and identify compensating controls where a strong control cannot be applied.

## Staff-Level View
Treat security as a system property rather than a collection of checkboxes. Connect threat models, architecture, implementation, build provenance, verification evidence, deployment controls, incident response, and long-term vulnerability management into one lifecycle.
