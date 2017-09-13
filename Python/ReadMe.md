


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
Expr    ::= Or+
Or      ::= AtomExpr ('|' AtomExpr)* 

AtomExpr::= Atom Trailer 
Atom    ::= Name | String | '[' Expr ']' | '(' Expr ')' 


Def    ::= '::='
Equals ::= Name Def Expr

Trailer::= ['*' | '+' | '{' Number{1 2} '}']

Name   ::= R'[a-zA-Z_][a-zA-Z0-9]*'
String ::= R'[\w|\W]*'
Number ::= R'\d+'
```

To be continue.
================








