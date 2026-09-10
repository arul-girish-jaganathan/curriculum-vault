# Copilot Instructions for curriculum-vault

## Repository Purpose

This is **arul-girish-jaganathan/curriculum-vault**: an Obsidian vault for **Embedded Systems Engineering curriculum**, study materials, and personal technical knowledge base. It serves as a canonical reference for embedded systems concepts, from fundamentals (C, C++, DSA, Computer Architecture) to specialized domains (ARM, RTOS, Linux, Drivers, Security, etc.) and advanced topics (FPGA, Edge AI/ML, PCB design, systems engineering).

## Canonical Knowledge Base

- **Markdown/Obsidian is the canonical format** for all curriculum content.
- All technical knowledge, study notes, and references live as `.md` files in organized domain directories.
- The actual repository filesystem is **the single source of truth** — never assume older structures or outdated chapter lists from prior discussions.
- Files are organized hierarchically: `01_Concepts/01_Technical/{NN_Domain}/{concept_files}`.

## Repository Structure

The repository currently spans **38+ technical domains** under `01_Concepts/01_Technical/`, including:

- **01_C** through **04_Computer_Architecture**: Language and foundational CS concepts
- **05_ARM** through **15_Debugging**: Platform-specific, OS, and tooling knowledge
- **16_Performance** through **20_Testing**: Quality, reliability, and validation
- **21_System_Design** through **28_Networking**: Architecture and protocols
- **29_DSP** through **38_Edge_AI_ML_for_Embedded**: Specialized domains

There is also a separate **02_Engineering_\u0026_Business_Leadership** domain, and structural directories like `00_Index/` for navigation and `06_Resume/` for professional materials.

## Canonical Concepts and Contextual Notes

### Canonical Notes
- **Canonical notes** are concrete, single-topic files (e.g., "00_Chapter_Index.md", "01_Variable_Scope.md") that serve as the authoritative reference for a specific concept.
- Each canonical note should be **substantive, well-researched, and developed in depth** rather than a placeholder or boilerplate outline.
- Canonical notes should cite authoritative sources (standards, specifications, official documentation) and distinguish between **language/standard guarantees**, **compiler behavior**, **ABI/platform behavior**, **CPU/hardware behavior**, and **OS/RTOS behavior**.

### Contextual Notes
- **Contextual notes** may include observations, cross-references, or integration points that connect multiple canonical concepts.
- Contextual notes are preserved; they provide valuable bridges between domains and should not be deleted merely because they appear short or supplementary.
- Never blindly delete existing contextual knowledge under the assumption it is outdated or low-value.

### Indexes and Navigation
- **Chapter index files** (e.g., `00_Chapter_Index.md` within domain folders) provide structured navigation and topic lists.
- Index files should list canonical concepts and topics, facilitate cross-domain discovery, and be kept in sync with actual subdomain content.
- Index files themselves may be sparse until content is actively developed; do not mistake an incomplete index for a reason to delete links or topics.

## Obsidian Wikilinks

- **Obsidian wikilinks** (e.g., `[[Topic]]` or `[[Topic|display text]]`) are the canonical linking mechanism within this vault.
- Wikilinks **must be preserved** and used correctly to maintain cross-references between concepts.
- All wikilink targets **must point to real, existing canonical notes**; do not create links to nonexistent files.
- When adding or modifying links, verify that the target file exists and is semantically appropriate.
- When a concept should be linked but the canonical note does not yet exist, prefer to create the note in the appropriate existing domain rather than orphaning the reference.

## External Links and References

- **External links** (URLs to official standards, documentation, specifications) must be **accurate and current**.
- Prefer official/authoritative sources (ISO/C standard, ARM documentation, Linux kernel docs, RTL libraries) over blogs or secondary sources when verifying technical claims.
- **Never fabricate or invent** URLs, version numbers, section numbers, or technical specifications.
- When in doubt about correctness of a reference, defer to verifiable, authoritative sources.

## Duplicate Canonical Concepts

- **Avoid creating duplicate canonical notes** for the same concept.
- If a concept appears to belong in multiple domains, assess the relationship:
  - Is this a **true duplicate** that should be consolidated or linked?
  - Is this a **specialization** of a more general concept (e.g., "ARM NEON instructions" vs. "SIMD")?
  - Should the note be placed in a single authoritative domain with cross-links from related domains?
- When duplicates are discovered, consolidate content and preserve links to the canonical location.

## Missing Important Concepts

- **Missing important concepts may be created** in the appropriate existing domain when they are needed.
- Prefer to create new notes within existing domain folders (e.g., a new 01_Concepts/01_Technical/NN_Domain/ topic) rather than creating new top-level domains.
- When proposing to add a new concept, verify that no equivalent canonical note already exists (check for wikilinks, cross-references, and naming variations).

## Preserving Existing Knowledge

- **Do not delete or rewrite existing knowledge** merely because it appears short, old, duplicated-looking, or contextual.
- Short or sparse content often indicates early-stage development or specialized context; it is not a reason for removal.
- All knowledge has been intentionally preserved and authored; changes must have strong technical or organizational justification.
- When in doubt, **preserve and link** rather than delete and consolidate.

## Substantive Development

- **Trivial topics should not be padded** with irrelevant boilerplate sections (e.g., "Introduction", "Conclusion", "Further Reading" templates).
- **Substantial topics must be developed deeply**, covering:
  - **Language/standard guarantees** (e.g., C++ standard behavior, memory model guarantees)
  - **Compiler/toolchain behavior** (e.g., GCC optimizations, Clang ABI differences)
  - **ABI/platform behavior** (e.g., ARM calling conventions, x86 stack layout)
  - **CPU/MCU/hardware behavior** (e.g., cache coherency, instruction timing, interrupt latency)
  - **OS/RTOS behavior** (e.g., Linux scheduling, FreeRTOS task switching)
  - **Project/product policy** (e.g., coding standards, project-specific conventions)

## Technical Integrity

- **Technical claims must never be fabricated**, guessed, or inferred without evidence.
- **Standards, specifications, versions, clauses, URLs, and guarantees must never be invented**; when in doubt, verify against authoritative sources or mark the claim as uncertain.
- **Embedded-systems implications** (performance, memory, timing, power, reliability, safety, security, debugging) must be included where technically relevant.
- **Staff/Principal-level reasoning** should be included when addressing complex tradeoffs, architectural decisions, or implications.

## Change Validation

Every substantial batch of changes (e.g., adding multiple concepts, restructuring domains, consolidating duplicates) **must be validated** for:

1. **Broken Obsidian links**: No wikilinks should point to nonexistent files.
2. **Duplicate canonical notes**: No two files should cover the same canonical concept authoritative.
3. **Orphaned important notes**: No substantive concept should be left without navigation or cross-links.
4. **Index/navigation consistency**: Chapter indexes and domain structures should reflect actual content.
5. **Accidental placeholder content**: No empty or placeholder files should be committed unless explicitly staging a concept.
6. **Unintended deletions**: No knowledge should be removed without clear justification and backup verification.

**Use scripts or automated analysis** (e.g., link validation, duplicate detection by filename/content hash) rather than manual inspection when the repository contains thousands of files.

## Prohibited Claims

- **Never claim** the repository is "complete", "fully audited", "all files processed", or "all links validated" unless this has actually been verified programmatically.
- Honesty about coverage and audit status is essential for long-term maintenance.

## Preferred Approach

1. **Inspect the actual filesystem** programmatically before proposing changes.
2. **Preserve existing organization** unless there is strong evidence that restructuring is necessary.
3. **Never perform massive destructive restructuring** merely to make the repository look cleaner or to conform to an assumed ideal structure.
4. **Make changes in coherent, reviewable batches** that can be independently validated.
5. **Prefer scripts and automated analysis** over manual inspection for repositories with tens of thousands of files.

## Working with This Repository

- When in doubt about whether to add, modify, or delete content, **consult the filesystem and existing patterns**.
- Treat the repository as a **living, carefully curated knowledge base**, not a template to be reshaped.
- Assume all existing content has been preserved for good reason; changes should be additive or clarifying rather than destructive.
- Always validate changes against the intended use case: a deep, authoritative reference for embedded systems engineering.
