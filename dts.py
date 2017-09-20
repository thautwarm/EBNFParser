#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:48:52 2017

@author: misakawa
dev-test-script
"""

from Python.Misakawa.Bootstrap.Parser import *
from Python.Misakawa.ObjectRegex.Node import MetaInfo
from Python.Misakawa.ErrorFamily import handle_error
def go():
    with open('./selfexamine.ebnf') as f:
        lex = f.read()
    tokens = token.findall(lex)
    parser = handle_error(Stmt.match)
    res = parser(tokens, partial=False)
    print(res)
go()


