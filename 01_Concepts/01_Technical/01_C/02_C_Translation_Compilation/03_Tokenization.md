# Tokenization

Tokenization turns the character stream produced by earlier translation processing into preprocessing tokens and then the lexical elements needed by the C grammar. Understanding this boundary explains why comments, whitespace, literals, identifiers and preprocessing directives behave differently.

## Important categories
C source contains identifiers, keywords, constants, string literals, punctuators and operators, with preprocessing tokens existing at an earlier stage. The compiler's lexer must recognize these according to the active source encoding and language mode.

## Why whitespace is not always cosmetic
Whitespace can separate tokens. Without separation, two intended identifiers can become one token. Comments are replaced during translation processing and can therefore affect token boundaries. String literals and character constants have their own lexical rules and escape processing.

## Embedded implications
Generated register definitions, protocol constants and macro-heavy hardware headers are particularly sensitive to preprocessing and lexical behavior. Compiler extensions may add keywords, attributes or syntax that is unavailable in another compiler.

## Diagnostics
If a compiler reports an apparently nonsensical syntax error far from the actual defect, inspect earlier preprocessing and token boundaries. A missing quote, comment delimiter or macro expansion can shift the parser's view of the remainder of the file.

## Staff-level view
Keep lexical concerns separate from semantic concerns. When debugging a build failure, establish the exact preprocessed source first; then determine whether the failure is lexical, syntactic, semantic, or implementation-specific.

## Related
- [[01_Source_to_translation_unit]]
- [[02_Preprocessing_phase]]
- [[04_Parsing_and_semantic_analysis]]
- [[61_C_Translation_Phases]]
