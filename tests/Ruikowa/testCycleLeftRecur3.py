#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:38:03 2017

@author: misakawa
"""

from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo
import re
token = re.compile("t|\)|\(").findall
namespace     = globals()
recurSearcher = set()
type = LiteralParser('t', name = 'type')
prefix = AstParser([Ref('prefix'),
                    LiteralParser('(', name='LP'),
                    SeqParser([Ref('prefix')]),
                    LiteralParser(')', name='RP')],
                    [Ref('type')], name = 'prefix')
                    
prefix.compile(namespace, recurSearcher)