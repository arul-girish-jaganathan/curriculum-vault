# Digraphs, legacy trigraphs and portability

## Core idea
C has alternate token spellings called digraphs. Historical C also defined trigraphs, but they were removed in C23. This makes language-version awareness relevant even for apparently obscure lexical syntax.

## Why this matters
A codebase can compile under one standard mode and fail under another because lexical support changed. Legacy code generators, preprocessor-heavy sources, and unusual punctuation can therefore create migration hazards.

## Embedded consequences
Embedded projects commonly retain old compiler baselines for years. During compiler migration, explicitly test lexical compatibility rather than assuming a newer compiler's default mode behaves like the historical build.

## Failure modes
- Old source relies on removed legacy lexical features.
- Code review misses alternate token spellings.
- Different compiler standard modes produce different preprocessing behavior.

## Verification
Compile representative legacy sources in both the old and target language modes. Make the selected standard explicit in the build and keep migration-only compatibility code isolated.

## Staff-level takeaway
Language evolution includes lexical changes. A migration plan should test source grammar and preprocessing, not just semantic feature compatibility.
