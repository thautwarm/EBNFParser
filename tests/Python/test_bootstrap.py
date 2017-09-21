#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:43:26 2017

@author: misakawa
"""

from Misakawa.Bootstrap.Parser import *
from Misakawa.ObjectRegex.Node import MetaInfo
from Misakawa.ErrorFamily import handle_error


def go():
    with open('../bootstrap.ebnf') as f:
        lex = f.read()
    tokens = token.findall(lex)
    parser = handle_error(Stmt.match)
    res = parser(tokens, partial=False)
    print(res)
go()



