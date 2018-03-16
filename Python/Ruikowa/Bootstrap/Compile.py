#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:00:43 2017

@author: misakawa
"""

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
from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo, DependentAstParser
try:
    from .etoken import token
except:
    from etoken import token
import re
namespace     = globals()
recurSearcher = set()
{define}
{parser_compile}
"""

import re
def compile(ebnf_text, language_name = 'Unnamed'):
    info = dict(liter=[], regex=[], keywd = [], char = [])
    stmts = parser(token(ebnf_text), MetaInfo(), partial=False)
    res, tks, to_compile = ast_for_stmts(stmts, info)
    #    print(res)

    if isinstance(tks, dict):
        tks = sorted(tks['char'])[::-1]+sorted(tks['liter'])[::-1] + tks['regex']
        tokendef = "token = re.compile('|'.join([{Tokens}])).findall".format(Tokens = ','.join(tks))
    else:
        tokendef = tks.strip(" ")

    astParser_compile = lambda name: "{name}.compile(namespace, recurSearcher)".format(name = name)
    parser_compile = '\n'.join(map(astParser_compile, to_compile))
    define = '\n'.join(res)
    return parserTemplate.format(define=define, parser_compile=parser_compile, tokendef=tokendef), tokenTemplate.format(
        tokendef=tokendef)

