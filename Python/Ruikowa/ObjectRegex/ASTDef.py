#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:23:04 2017

@author: misakawa
"""
from collections import deque
class Ast(deque):

    def __init__(self, meta, name):
        super(Ast, self).__init__()
        self.name = name
        self.meta = meta

    def __str__(self):
        return self.dump()
    def dump(self, indent = 0):

        next_indent = len(self.name)+indent+1
        body        = ("{next_indent}".format(next_indent = ' '*(next_indent))) \
                                      .join([
                                            "\n{indent}'{str}'\n".format(indent=' ' * (next_indent), str=node)
                                            if isinstance(node, str) else \
                                            node.dump(next_indent)
                                            for node in self])

        return "{name}[{body}\n{endl}]".format(name= self.name,
                                               body=body,
                                               endl=' '*indent)
    def dumpToJSON(self):
        return dict(name = self.name,
                    value= [node if isinstance(node, str) else\
                            node.dumpToJSON()
                            for node in self],
                    meta = self.meta)
