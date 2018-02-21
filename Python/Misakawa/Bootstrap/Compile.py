#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 20:01:18 2017

@author: misakawa
"""

Compile = True
from .Ast import ast_for_stmts
from .Parser import Stmt, token
from ..ObjectRegex.Node import MetaInfo
from ..ErrorFamily import handle_error
parser = handle_error(Stmt)
tokenTemplate = """
import re
{tokendef}
"""
parserTemplate = """
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
from etoken import token 
import re
namespace     = globals()
recurSearcher = set()
{define}
{parser_compile}
"""


def compile(ebnf_text, language_name):
    info = dict(raw = [], regex = [])
    stmts = parser(token.findall(ebnf_text), MetaInfo(), partial=False)
    res, tks, to_compile = ast_for_stmts(stmts, info)
#    print(res)
    if isinstance(tks, dict):
        tks = sorted(tks['raw'])[::-1] + tks['regex']
        tokendef = f"token = re.compile('|'.join([{','.join(tks)}])).findall"
    else:
        tokendef = tks.strip(" ")
    astParser_compile = lambda name : f"{name}.compile(namespace, recurSearcher)"
    parser_compile = '\n'.join(map(astParser_compile, to_compile))
    define         = '\n'.join(res)
    return parserTemplate.format(define = define, parser_compile = parser_compile, tokendef = tokendef), tokenTemplate.format(tokendef = tokendef)
        

      
