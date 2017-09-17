#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:43:26 2017

@author: misakawa
"""

from EBNFParser.Parser.SelfExamine import handle_error, token,Stmt,String,re,Equals
from EBNFParser.Parser.SelfExamine import *


def go():
    with open('../selfexamine.ebnf') as f:
        lex = f.read()
    tokens = token.findall(lex)
    parser = handle_error(Stmt.match)
    res = parser(tokens, partial=False)
    print(res)
go()



