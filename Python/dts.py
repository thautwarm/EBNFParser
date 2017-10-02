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
from Misakawa.Bootstrap.Ast import ast_for_stmts
from Misakawa.Bootstrap.Compile import compile as bootstrap_comp

with open('../bootstrap.ebnf') as f:
        lex = f.read()
s= bootstrap_comp(lex, '')
with open('bs.py','w') as f:f.write(s)

           
           
#Expr = AstParser([Ref('Or'),
#                  SeqParser([LiteralParser.Eliteral('|', name = '\'|\''),Ref('Or')], 
#                             atleast = 0, atmost = None)], name = 'Expr')
#Or = AstParser([SeqParser([Ref('AtomExpr')], 
#                           atleast = 1, atmost = None)], name = 'Or')
