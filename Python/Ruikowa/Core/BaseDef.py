#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 17:46:02 2017

@author: misakawa
"""
import warnings
from ..ErrorFamily import *
# ====== Define Generic Type Params =============

WarningInfo ="""
                You're trying to visit the elems that've been deprecated.
                If it occurred when you're using EBNFParser, report it as 
                a BUG at 
                `https://github.com/thautwarm/EBNFParser`. Thanks a lot!
            """


# ======

Undef = None
class Const:
    def __new__(self):
        raise ObjectUsageError("You're trying to new an instance with a module.")
    UnMatched  = None
    NameFilter = 0
    RawFilter  = 1
    RegexFilter= 2


class RecursiveFound(Exception):
    def __init__(self, node):
        self.node =  node
        self.possibilities = []
    def add(self, possibility):
        self.possibilities.append(possibility)

    def __str__(self):
        s = '=====\n'
        s+=self.node.name+'\n'
        s+='\n'.join(a.name +' | '+str([c.name for c in b])
                        for a,b in self.possibilities)
        return s


class Recur:
    def __new__(self, name, count):
        return (name, count)

class Trace:
    def __init__(self,
                 trace  = Undef,
                 length = Undef):
        self.length  = length     if length is not Undef else\
                       len(trace) if trace  is not Undef else\
                       0
        self.content = trace if trace is not Undef else\
                       []
        self._Mem    = len(self.content)


    def __iter__(self):
        yield from [elem for elem in self.content[:self.length]]


    def __getitem__(self, item):
        if isinstance(item, int):
            if item >= self.length:
                warnings.warn(WarningInfo)
            return self.content[item]
        elif isinstance(item, slice):
            if item.stop > self.length:
                warnings.warn(WarningInfo)
            return self.content[item]



    def append(self, elem):
        # reuse the memory cache
        if self.length==self._Mem:
            self.length += 1
            self._Mem   += 1
            self.content.append(elem)
        elif self.length < self._Mem:
            self.content[self.length] = elem
            self.length += 1

    def new(self, constructor):
        # just can be used for Type `Trace[Contrainer[T]]`
        # reuse the memory cache
        if self.length==self._Mem:
            self.length += 1
            self._Mem   += 1
            self.content.append(constructor())
        elif self.length < self._Mem:
            self.content[self.length].length = 0
            self.length += 1

    def pop(self):
        self.length -= 1
        assert self.length>=0
            
    def where(self, obj):
        for idx, elem in enumerate(self.content[:self.length]):
            if elem is obj:
                return idx
        return Undef


        
    
    

