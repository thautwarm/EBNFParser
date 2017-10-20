#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 20:07:44 2017

@author: misakawa
"""

from Ruikowa.Bootstrap.Parser import *
from Ruikowa.ObjectRegex.MetaInfo import *
from Ruikowa.Bootstrap.Ast import ast_for_stmts
words = token.findall(r"""Token {{
def token(input_str):
    return list(input_str)
}}
Stmt Throw ['\n'] ::= (NEWLINE* Equals* NEWLINE*)*
Expr    ::= Or ('|' Or)*
Or      ::= AtomExpr+
AtomExpr::= Atom [Trailer] 
Atom    ::= Str | Name | '[' Expr ']' | '(' Expr ')' 
Equals ::= Name LitDef Str | Name Def Expr
Trailer::= '*' | '+' | '{' Number{1 2} '}'
Def    := '::='
LitDef := ':='
Str    := R'"[\w|\W]*?"'
Name   := R'[a-zA-Z_][a-zA-Z0-9]*'
Number := R'\d+'
NEWLINE:= '\n'""")
meta = MetaInfo()
res = Stmt.match(words, meta)
print(res)
