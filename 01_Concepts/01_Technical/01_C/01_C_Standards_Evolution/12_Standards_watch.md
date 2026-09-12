# Standards Watch

Standards watch is the practice of tracking language and library evolution without allowing unreviewed proposals or compiler experiments to become accidental product requirements.

## What to watch
Track published ISO C revisions, corrigenda/technical corrections, WG14 work, compiler support, standard-library implementation status, static-analysis support and relevant safety/security guidance. Keep published standards separate from drafts, proposals and vendor extensions.

## Evidence discipline
A proposal is not a language guarantee. A compiler extension is not ISO C. A feature implemented by one compiler is not automatically portable. Every note in this knowledge base should label these distinctions explicitly.

## Embedded impact
Standards evolution can affect compiler diagnostics, integer facilities, initialization, type-system expressiveness, preprocessing, attributes, bit manipulation, checked arithmetic and library interfaces. Adoption must also consider linker/debugger support, certification evidence, tool qualification and long-term maintenance.

## Practical workflow
Review standards developments periodically, classify them as relevant/not relevant, prototype useful features on host builds, check target compiler support, assess safety/security impact, and only then propose a product baseline change.

## Staff-level view
A standards watch should reduce surprise rather than generate churn. The deliverable is a controlled roadmap: what is available now, what is experimental, what is useful later, and what the organization deliberately will not adopt.

## Related
- [[05_C23_modernization]]
- [[11_Choosing_a_language_baseline]]
- [[51_C_C23_Modernization]]
- [[60_C_Future_Standards_Watch]]
