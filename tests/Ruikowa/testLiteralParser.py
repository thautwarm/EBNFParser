#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 20:03:08 2017

@author: misakawa
"""

from Ruikowa.ObjectRegex.Node import Ast, Ref, LiteralParser, CharParser, SeqParser, AstParser
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from Ruikowa.Core.BaseDef import Trace
inputs = ['a', '\n', 'abc']
charParser1 = CharParser('a')
charParser2 = CharParser('\n')
litParser   = LiteralParser.RawFormDealer(rawStr='abc', name = 'ABC')
meta = MetaInfo()
assert charParser1.match(inputs, meta) is 'a'
assert litParser.match(inputs, meta)   is None
assert charParser2.match(inputs, meta) is '\n'
assert litParser.match(inputs, meta)   == 'abc'