# C Declarations and Declarators

## Chapter purpose
Build mechanical skill in reading and designing C declarations. A declaration is not merely type information: declaration specifiers and the declarator together describe the declared entity, and small syntactic changes can alter pointer, array, function, storage, and API semantics.

## Topics
- [[01_Declaration_specifiers|Declaration specifiers]]
- [[02_Declarator_grammar|Declarator grammar]]
- [[03_Pointers_in_declarators|Pointers in declarators]]
- [[04_Arrays_in_declarators|Arrays in declarators]]
- [[05_Function_declarators|Function declarators]]
- [[06_Complex_declarations|Complex declarations]]
- [[07_Parameter_declarations|Parameter declarations]]
- [[08_Old_style_declarations|Old-style declarations]]
- [[09_Typedef_names|Typedef names]]
- [[10_Declarator_parsing_workflow|Declarator parsing workflow]]
- [[11_API_declaration_design|API declaration design]]
- [[12_Header_declaration_hygiene|Header declaration hygiene]]

## Review prompts
- What entity does the declarator actually declare?
- Which parts describe the type and which parts select storage/linkage behavior?
- How do parentheses change binding between pointer, array, and function declarators?
- What ABI consequences follow from a declaration crossing a module boundary?
