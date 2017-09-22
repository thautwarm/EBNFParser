#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:43:26 2017

@author: misakawa
"""

from Misakawa.Bootstrap.Parser import *
from Misakawa.ObjectRegex.Node import MetaInfo, Ast
from Misakawa.ErrorFamily import handle_error
from Misakawa.Bootstrap.Ast import ast_for_stmts
from Misakawa.Bootstrap.Compile import compile as bootstrap_comp
with open('../tests/lisp.ebnf') as f:
        lex = f.read()
s= bootstrap_comp(lex, '')
with open('../parser_gen(lisp).py','w') as f:f.write(s)





