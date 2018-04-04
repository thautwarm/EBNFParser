#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:16:52 2017

@author: misakawa
"""
from ..ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralNameParser, LiteralNameValueParser
from ..ObjectRegex.Tokenizer import Tokenizer
from ..ObjectRegex.MetaInfo import MetaInfo

Str = LiteralNameParser('Str')
Name = LiteralNameParser('Name')
Number = LiteralNameParser('Number')
Codes = LiteralNameParser('Codes')

namespace = globals()
recurSearcher = set()

TokenIgnore = AstParser(
    [('keyword', 'ignore'),
     '[',
     SeqParser([Name], [Str]),
     ']'],
    name='TokenIgnore')

Prefix = AstParser(
    [('keyword', 'as'), Name],
    name='Prefix')

Of = AstParser(
    [('keyword', 'of'), Name],
    name='Of')

Stmts = AstParser(
    [SeqParser([Ref('TokenIgnore')],
               [Ref('TokenDef')],
               at_most=1),
     SeqParser([Ref('Equals')])],
    name='Stmts')

TokenDef = AstParser(
    [('keyword', 'deftoken'), SeqParser([Name], [Codes], at_most=1, at_least=1)],
    name='TokenDef')

Equals = AstParser(
    [Name, SeqParser([Ref('Prefix')], [Ref('Of')], at_most=1), ':=', SeqParser([Str]), ';'],
    [Name, SeqParser([Ref('Throw')], at_most=1), '::=', Ref('Expr'), ';'],
    name='Equals')

Throw = AstParser(
    [('keyword', 'throw'),
     '[',
     SeqParser([Name], [Str]),
     ']'
     ],
    name='Throw')

Expr = AstParser(
    [Ref('Or'), SeqParser(['|', Ref('Or')])],
    name='Expr')

Or = AstParser(
    [SeqParser([Ref('AtomExpr')], at_least=1)],
    name=' Or')

AtomExpr = AstParser(
    [Ref('Atom'), SeqParser([Ref('Trailer')])],
    name='AtomExpr')

Atom = AstParser(
    [Str],
    [Name],
    ['[', Ref('Expr'), ']'],
    ['(', Ref('Expr'), ')'],
    name='Atom')

Trailer = AstParser(
    ['+'],
    ['*'],
    ['{', SeqParser([Number], at_least=1, at_most=2), '}'],
    name='Trailer')

Stmts.compile(namespace, recurSearcher)
