#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:16:52 2017

@author: misakawa
"""

from ..ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser
lit = LiteralParser
Str    = lit("[A-Z]{0,1}'[\w|\W]*?'", name = 'Str', isRegex=True)
Name   = lit('[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\.]*', name = 'Name', isRegex=True)
Number = lit('\d+', name = 'Number', isRegex=True)
LBB =    CharParser('{')
LB  =    CharParser('[')
LP  =    CharParser('(')
RBB =    CharParser('}')
RB  =    CharParser(']')
RP  =    CharParser(')')
ENDM=    CharParser(';')

SeqStar = CharParser('*')
SeqPlus = CharParser('+')

Def     = lit('::=')
LitDef  = lit(':=')
OrSign  = CharParser("|")

ThrowSign   = lit('Throw')
TokenSign   = lit('Token')

Codes       = lit('\{\{[\w\W]+?\}\}', isRegex=True)

AstStr    = AstParser([Str], name = 'AstStr')
namespace     = globals()
recurSearcher = set()



Throw = AstParser(
        [ThrowSign,
         LB, SeqParser([Name], [Str]), RB],
        name = 'Throw')

TokenDef = AstParser(
        [TokenSign,
         SeqParser([Name], [Codes], atmost=1)],
        name = 'TokenDef')


Expr = AstParser(
    [Ref('Or'),
     SeqParser([ OrSign, Ref('Or')],
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
    [AstStr],
    [Name],
    [LP, Ref("Expr"), RP],
    [LB, Ref("Expr"), RB],
    name = 'Atom')

Equals = AstParser(
    [Name, LitDef, Str, ENDM      ],
    [Name, SeqParser([Ref('Throw')], atmost =1),
           Def, Ref('Expr'), ENDM ],
    name = 'Equals')


Trailer = AstParser(
    [SeqStar],
    [SeqPlus],
    [LBB, SeqParser(
        [Number],
        atleast=1,
        atmost =2
        ),
     RBB],
    name = 'Trailer')

Stmt  = AstParser(
            [SeqParser([Ref('TokenDef')], atmost = 1),
             SeqParser([
                        SeqParser([Ref('Equals')])]),
            ],
            name = 'Stmt')

Stmt.compile(namespace, recurSearcher)


import re as _re
def _escape(*strs):
    return '|'.join([_re.escape(str) for str in strs])
token = _re.compile('|'.join(
        [
        "[A-Z]{0,1}'[\w\W]*?'",
        '\{\{[\w\W]+?\}\}',
        _escape('|',
                '{',
                '}',
                ';',
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
        "\d+",
        ]
        ))








