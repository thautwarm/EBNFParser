#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:23:04 2017

@author: misakawa
"""

from .Tokenizer import Tokenizer
from typing import List, Union, Sequence, Iterator, Collection

if False:
    from .MetaInfo import MetaInfo

INDENT_UNIT = ' ' * 4


class Ast(list):
    # List[Union[Tokenizer, Ast]]

    def __init__(self, meta: 'MetaInfo', name: str):
        list.__init__(self)
        self.name = name
        self.meta = meta

    def appendleft(self, obj):
        self.reverse()
        self.append(obj)
        self.reverse()

    def __iter__(self) -> 'Iterator[Union[Tokenizer, Ast]]':
        return list.__iter__(self)

    def __getitem__(self, item) -> 'Union[Tokenizer, Ast]':
        return list.__getitem__(self, item)

    def __str__(self):
        return self.dump()

    def dump(self, indent=0):
        next_indent = indent + 1
        return """{INDENT}{NAME}[
{CONTENT}
{INDENT}]""".format(INDENT=INDENT_UNIT * indent,
                    NAME=self.name,
                    CONTENT='\n'.join(
                        node.dump(next_indent)
                        if isinstance(node, Ast) else \
                            "{NEXT_INDENT}{STR}".format(NEXT_INDENT=INDENT_UNIT * next_indent, STR=node)

                        for node in self
                    ))

    def dump_to_json(self):
        return dict(name=self.name,
                    value=tuple(node.dump_to_json() for node in self))
