#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:23:04 2017

@author: misakawa
"""

INDENT_UNIT = ' '*4
class Ast(list):

    def __init__(self, meta, name):
        super(Ast, self).__init__()
        self.name = name
        self.meta = meta


    def appendleft(self, obj):
        self.reverse()
        self.append(obj)
        self.reverse()

    def __str__(self):
        return self.dump()
    def dump(self, indent = 0):
        next_indent = indent+1
        return """{INDENT}{NAME}[
{CONTENT}
{INDENT}]""".format(INDENT =INDENT_UNIT*indent,
                    NAME   = self.name,
                    CONTENT='\n'.join(
                                    [
                                    "{NEXT_INDENT}\"{STR}\"".format(NEXT_INDENT=INDENT_UNIT * next_indent, STR=node)
                                    if isinstance(node, str) else \
                                        node.dump(next_indent)

                                    for node in self
                                    ]))

    def dumpToJSON(self):
        return dict(name = self.name,
                    value= [node if isinstance(node, str) else\
                            node.dumpToJSON()
                            for node in self],
                    meta = self.meta)
