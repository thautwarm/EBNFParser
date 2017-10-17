#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:16:02 2017

@author: misakawa
"""

from ..ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser
lit = LiteralParser 

Str    = lit("[RK]{0,1}'[\w|\W]*?'", name = 'Str')
Name   = lit('[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\.]*', name = 'Name')
Number = lit('\d+',name = 'Number')

NEWLINE= lit('\n', name = 'NEWLINE')

LBB = lit.Eliteral('{', name = 'LBB')
LB  = lit.Eliteral('[', name = 'LB')
LP  = lit.Eliteral('(', name = 'LP')
RBB = lit.Eliteral('}', name = 'RBB')
RB  = lit.Eliteral(']', name = 'RB')
RP  = lit.Eliteral(')', name = 'RP')

SeqStar = lit.Eliteral('*', name = 'SeqStar')
SeqPlus = lit.Eliteral('+', name = 'SeqPlus')

Def     = lit.Eliteral('::=', name = 'Def')
LitDef  = lit.Eliteral(':=', name = 'LitDef')
OrSign  = lit.Eliteral("|",   name = 'OrSign')

Throw   = lit.Eliteral('Throw', name = 'Throw') 
using   = lit.Eliteral('using', name = 'usingSign')
Codes   = lit('\{\{[\w\W]+?\}\}', name = 'Codes')

namespace     = globals()
recurSearcher = set()

Using = AstParser(
        [using, SeqParser([Name],[Codes], atmost = 1)],
        name = 'Using')

Expr = AstParser(
    [Ref('Or'),
     SeqParser([OrSign, Ref('Or')],
               atleast=0)
     ],
    name = 'Expr')
Or = AstParser(
    [SeqParser([Ref('AtomExpr')],
               atleast=1)
     ],
    name = 'Or')

AtomExpr =  AstParser(
    [Ref('Atom'), SeqParser([Ref('Trailer')])],
    name = 'AtomExpr')

Atom = AstParser(
    [Str],
    [Name],
    [LP, Ref("Expr"), RP],
    [LB, Ref("Expr"), RB],
    name = 'Atom')

Equals = AstParser(
    [Name, LitDef, SeqParser([Str], atleast=1)],
    [Name, SeqParser([Throw,SeqParser([Name])],atmost = 1),Def, Ref("Expr")],
    name = 'Equals')


Trailer = AstParser(
    [SeqStar],
    [SeqPlus],
    [LBB, SeqParser(
        [Number],
        atleast=1,
        atmost =2
        ),           RBB],
    name = 'Trailer')

Stmt  = AstParser(
            [SeqParser([Using], atmost = 1),
             SeqParser([
                        SeqParser([NEWLINE]),
                        SeqParser([Ref('Equals')]),
                        SeqParser([NEWLINE])
                       ]),
            ],
            name = 'Stmt', toIgnore = {'NEWLINE'})

Stmt.compile(namespace, recurSearcher)


import re as _re
def _escape(*strs):
    return '|'.join([_re.escape(str) for str in strs])
token = _re.compile('|'.join(
        [
        "[RK]{0,1}'[\w\W]*?'",
        '\{\{[\w\W]+?\}\}',
        _escape('|',
                '{',
                '}',
                '[',
                ']',
                '(',
                ')',
                '+',
                '*',
                ':=',
                '::=',
                '.'),
        "[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\.]*",
        "\d+","\n",
        ]
        ))








