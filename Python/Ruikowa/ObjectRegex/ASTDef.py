#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:23:04 2017

@author: misakawa
"""

class Ast:
    """To Store Ast Structures(Parsed)."""
    
    name = None
    def __init__(self, meta, *v, type = list, name = None):
        if type not in (list, str): raise ErrorFamily.UnsolvedError("Ast value type must be `list` or `str`.")
        self.value = type(*v)
        self.name  = name
        self.meta  = meta # (count, row_idx)
        
    def __getitem__(self, v):
        return self.value.__getitem__(v)
    
    def __iter__(self):
        if self.type is list:
            yield from self.value
        else:
            yield self.value
    
    @property
    def type(self):
        return self.value.__class__

    def append(self, v):
        self.value.append(v)

    def clear(self):
        self.value.clear()

    def extend(self, v):
        self.value.extend(v.value if isinstance(v, Ast) else v)
        
    def __len__(self):
        return len(self.value)
        
    def dump(self, indent = 0):
        
        endl = ' '*indent
        if self.type is str:
            value = 'NEWLINE' if self.value is '\n' else self.value
            return f"{self.name}[{value}]\n{endl}"
        else:
            next_indent  = len(self.name)+indent+1
            body = f"\n{' '*(next_indent)}".join(map(lambda x:x.dump(next_indent), self))
            return f"{self.name}[{body}\n{endl}]"
        
    def dumpToJSON(self):
        JSON = dict(name  = self.name,
                    value = self.value if self.type is str else [value.dumpToJSON() for value in self.value],
                    meta  = self.meta
                    )
        return JSON

    def __str__(self):
        return self.dump(0)