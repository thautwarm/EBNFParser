#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:00:43 2017

@author: misakawa
"""

from .Ast import Compiler
from .Parser import Stmts
from ..ObjectRegex.Node import MetaInfo
from ..ErrorHandler import ErrorHandler
from .Token import NameEnum, Tokenizer, token_func

import re as _re
from pprint import pprint as _pprint, pprint
from ..ObjectRegex.Tokenizer import Tokenizer, str_matcher, regex_matcher, char_matcher


def _escape(*strs):
    return '|'.join([_re.escape(str) for str in strs])


parser = ErrorHandler(Stmts.match, token_func)
tokenTemplate = """
import re
{tokendef}
"""
parser_template = """
from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo, DependentAstParser
try:
    from .etoken import token
except:
    from etoken import token
import re
namespace     = globals()
recur_searcher = set()
{define}
{parser_compile}
"""

import re


def compile(src_path, language_name='Unnamed'):
    # info = dict(liter=[], regex=[], keywd=[], char=[])
    stmts = parser.from_file(src_path, MetaInfo(fileName=src_path))
    compiler = Compiler()
    compiler.ast_for_stmts(stmts)
    print('\n'.join(compiler.combined_parsers))
    print('\n'.join(compiler.token_definitions))
    print(compiler.token_spec.to_token_table())
    print(compiler.token_spec.to_name_enum())


    # res, tks, to_compile = ast_for_stmts(stmts, info)

    # if isinstance(tks, dict):
    #     tks = sorted(tks['char'])[::-1] + sorted(tks['liter'])[::-1] + tks['regex']
    #     tokendef = "token = re.compile('|'.join([{Tokens}])).findall".format(Tokens=','.join(tks))
    # else:
    #     tokendef = tks.strip(" ")
    #
    # astParser_compile = lambda name: "{name}.compile(namespace, recur_searcher)".format(name=name)
    # parser_compile = '\n'.join(map(astParser_compile, to_compile))
    # define = '\n'.join(res)
    # return parser_template.format(define=define, parser_compile=parser_compile,
    #                               tokendef=tokendef), tokenTemplate.format(
    #     tokendef=tokendef)
