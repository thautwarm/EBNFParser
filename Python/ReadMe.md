


# EBNFParser
Parse Many, Any, Every
---------

### What is EBNFParser?

EBNFParser is a framework for parsing easily.

Sometimes we need make `Domain Specific Language`s, sometimes we need to transform Language A to Language B, for example, `Matlab` to `Python`, `R` to `Julia`, `Python` to `Lisp` and so on.

Sometimes the transformation could be quite difficult because different languages differ in quite different features.

If the obstacles lie mostly in the grammars, EBNFParser can help you get it over easily.

If you want to parse something, just write a EBNF file and use this tool.

### Instance1:Self-Examination

```BNF
Expr    ::= Or ('|' Or)*
Or      ::= AtomExpr+

AtomExpr::= Atom [Trailer] 
Atom    ::= Str | Name | '[' Expr ']' | '(' Expr ')' 



Equals ::= Name LitDef Str | Name Def Expr

Trailer::= '*' | '+' | '{' Number{1 2} '}'
Stmt   ::= ('\n'* Expr* '\n'*)*


LitDef := ':='
Def    := '::='
Str    := R'"[\w|\W]*?"'
Name   := R'[a-zA-Z_][a-zA-Z0-9]*'
Number := R'\d+'
```
**P.S**  
The grammar of the EBNF is not same as the standard one, there are some additional ones for writing parser generator easilier.  
1. `:=` is a literal symbol to define `Literal` symbol, you have to use it in this way : `Name := Str`, where  
    * `Name` can be matched with *Regular Expression* `[a-zA-Z]{0,1}[a-zA-Z_]*`.
    * `Str` can be matched with `R{0,1}'[\w|\W]*?'`. If `Str` starts with a `R`, it means that we will use *Regular Expression* to do pattern matching.
2. `X{1 2}` means that `X` should be repeated at least 1 time and at most 2 times.  
`X{2}` means that `X` should be repeated at least 2 times.


To be continue.
================








