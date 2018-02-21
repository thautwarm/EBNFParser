#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 20:03:23 2017

@author: misakawa
"""

from Ruikowa.ObjectRegex.Node import Ast, Ref, LiteralParser, CharParser, SeqParser, AstParser
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from Ruikowa.Core.BaseDef import Trace
a = LiteralParser('a', name = 'a')
c = LiteralParser('c', name = 'c')
d = LiteralParser('d', name = 'd')
ASeq = AstParser([Ref('U'), d],[a], name = 'ASeq')
U    = AstParser([Ref('ASeq'), c],  name = 'U')
namespace = globals()
seset     = set()
ASeq.compile(namespace, seset)
x = MetaInfo()
print('test result => ')
print(ASeq.match(['a', 'c','d','c','d','k'], x))