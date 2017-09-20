#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:48:52 2017

@author: misakawa
dev-test-script
"""

from Misakawa.Bootstrap.Parser import *
from Misakawa.ObjectRegex.Node import MetaInfo, Ast
from Misakawa.ErrorFamily import handle_error

_compose_eq = 0
_literal_eq = 1
_newline    = 2
def go():
    with open('../selfexamine.ebnf') as f:
        lex = f.read()
    tokens = token.findall(lex)
    parser = handle_error(Stmt.match)
    res = parser(tokens, partial=False)
    print(res)

    
    return res
res = go()

def grpFunc(stmt : Ast):
   return  _newline if stmt.name == 'NEWLINE' else  \
           _literal_eq if stmt[2].name == 'Str' else \
           _compose_eq
