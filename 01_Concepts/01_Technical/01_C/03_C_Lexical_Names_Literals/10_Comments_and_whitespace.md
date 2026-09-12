# Comments, whitespace and token boundaries

## Core idea
Comments and whitespace mostly separate source tokens; they are not runtime operations. During translation, comments are replaced/processed according to the language's lexical rules, so the compiler sees a token stream rather than the visual layout shown in an editor.

## Why it matters
The classic boundary bug is assuming whitespace is optional everywhere. Preprocessor directives, token pasting, stringization, adjacent tokens, and operators with multiple-character spellings all make token boundaries significant.

## Embedded consequences
Generated code and vendor headers often depend heavily on macros. A formatting change can expose a tokenization or preprocessing issue even when the code looks visually equivalent. Keep generated C reproducible and inspect preprocessor output when a macro behaves unexpectedly.

## Failure modes
- Accidental token concatenation after removing whitespace.
- Comment placement changing a preprocessing directive or macro body.
- Missing line terminators affecting directive structure.
- Debug-only comments masking a macro expansion problem.

## Verification
Inspect `-E`/preprocessor output, compiler token/AST dumps where available, and compare generated source rather than only the original file when debugging preprocessing.

## Staff-level takeaway
Visual source is not the compiler's input model. When diagnosing lexical or macro bugs, reason from the resulting preprocessing-token stream.
