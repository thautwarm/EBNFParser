#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 17:46:02 2017

@author: misakawa
"""
import warnings
from typing import List, Tuple, Any, Generic, TypeVar, Union
from ..ErrorFamily import *
# ====== Define Generic Type Params =============

class GenType:
    T = TypeVar('T')
    G = TypeVar('G')
    V = TypeVar('V')


# ======

Undef = None
ControlSign    = object
OperateSign    = object

class Contrl:
    def __new__(self):
        raise ObjectUsageError("You're trying to new an instance with a module.")
    __slots__ = ()
    Matched   = ControlSign()
    GotoLabel = ControlSign() 
class Operate:
    def __new__(self):
        raise ObjectUsageError("You're trying to new an instance with a module.")
    __slots__ = ()
    Next      = OperateSign()
    Last      = OperateSign()
class Const:
    def __new__(self):
        raise ObjectUsageError("You're trying to new an instance with a module.")
    UnMatched = None



class Goto:
    def __new__(self, labelName):
        return (Contrl.GotoLabel, labelName)


class Trace:
    def __init__(self, 
                 objectType,
                 trace      = Undef,
                 length:int = Undef):
        self.length  = length     if length is not Undef else\
                       len(trace) if trace  is not Undef else\
                       0
        self.content = trace if trace is not Undef else\
                       []
        self._Mem    = len(self.content)
        self.objectType=objectType


    def __getitem__(self, item:
                Union[int, 
                      Tuple[object, OperateSign]
                      ]):
        if isinstance(item, int):
            return self.fromIndex(item)

        elif isinstance(item, tuple):
            
            # ===== In case of debugging. =============
            # Just ignore it if it annoys you :)
            assert len(item) is 2 
            assert isinstance(item[0],  self.objectType)
            assert isinstance(item[1],  OperateSign)
            # =========================================
            
            return self.which(item)
        
    def fromIndex(self, i):
        if i >= self.length:
            warnings.warn("""
            You're trying to visit the elems that've been deprecated.
            If it occurred when you're using EBNFParser, report it as 
            a BUG at 
            `https://github.com/thautwarm/EBNFParser`. Thanks a lot!
            """)
        return self.content[i]

    def push(self, elem):
        # reuse the memory cache
        if self.length==self._Mem:
            self.length += 1
            self._Mem   += 1
            self.content.append(elem)
        elif self.length < self._Mem:
            self.content[self.length] = elem
            self.length += 1

    def pop(self):
        self.length -= 1
        assert self.length>=0

    def which(self, tups):
        obj, sign = tups
        idx = self.where(obj)
        if sign is Operate.Last:
            return self.content[idx-1]
        elif sign is Operate.Next:
            return self.content[idx+1]
        else:
            raise Exception("Undef Operate Sign") # incomplete
            
    def where(self, obj):
        for idx, elem in enumerate(self.content):
            if elem is obj:
                return idx
        return Undef


        
    
    

