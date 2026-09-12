# C Lexical Structure, Names and Literals

## Chapter purpose
Understand how C source is converted into preprocessing tokens and tokens, how identifiers and literals are formed, and why lexical details can affect preprocessing, portability, diagnostics, and embedded toolchains.

## Topics
- [[01_Identifiers|Identifiers and identifier formation]]
- [[02_Keywords|Keywords and language-reserved words]]
- [[03_Reserved_identifiers|Reserved identifiers and namespace hazards]]
- [[04_Integer_constants|Integer constants and suffix/type selection]]
- [[05_Floating_constants|Floating constants and translation-time interpretation]]
- [[06_Character_constants|Character constants and execution character set]]
- [[07_String_literals|String literals and storage/concatenation rules]]
- [[08_Escape_sequences|Escape sequences and source/execution character mapping]]
- [[09_Universal_character_names|Universal character names]]
- [[10_Comments_and_whitespace|Comments, whitespace and token boundaries]]
- [[11_Digraphs_and_trigraphs|Digraphs, legacy trigraphs and portability]]
- [[12_Literal_portability|Literal portability review]]

## Review prompts
- What is the difference between a source character, preprocessing token, and token?
- Which lexical choices depend on the implementation character set or source encoding?
- Can preprocessing change the token stream you think you wrote?
- Which literal forms change type because of suffixes or target width?
- What lexical assumptions could break a cross-compiler or embedded build?
