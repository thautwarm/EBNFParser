#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 01:29:38 2017

@author: misakawa
"""

import re
def reMatch(x, make = lambda x:x, escape = False):
    
    re_ = re.compile( re.escape(x) if escape else x)
    def _1(ys):
        if not ys: return None
        r = re_.match(ys[-1])
        if not r : return None
        a, b = r.span()
        if a!=0 : raise Exception('a is not 0')
        if b is not len(ys[-1]):
            return None
        return 1, ys[-1]
    return _1

class Liter:
    def __init__(self, i, name = None):
        self.f = reMatch(i)
        self.name = name
    def match(self, objs, partial = True):
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                return r
            return None
        
class ELiter:
    def __init__(self, i, name = None):
        self.f = reMatch(i, escape = True)
        self.name = name
    def match(self, objs, partial = True):
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                return r
            return None
    


class recur:pass
def redef(self, *args, **kwargs):
    self.__init__(*args, **kwargs)
    return self
    
from collections import deque
class mode(deque):
    def setName(self, name):
        self.name = name
        return self



def lim_0(a):
    return a if a>0 else 0
    
class ast:
    def __init__(self, *ebnf, name = None):
        
        self.name     = name
        self.parent   = None
        self.possibles: 'list[mode[ast, re]]' = \
                    [ mode([self if e is recur else e for e in es]) for es in ebnf ] 
        
    
    def setP(self, parent): self.parent = parent; parent.append(self); return self
    
    def match(self, objs, partial = True):
        
        res   = mode().setName(self.name)
        N     = len(objs)
        count = 0
        
        goto  = False
        # debug
#        for i, possible in enumerate(self.possibles):
        # ===
        
        for possible in self.possibles:
            for thing in list(possible)[::-1]:
                
                
                r = thing.match(objs[:lim_0(N-count)], partial = partial)
                
                # debug
                print(f"{self.name} - loc <1>:", r)
                
                # ===
                
                
                if not r:
                    # nexr possible
                    res.clear()
                    count = 0
                    goto = True
                    break
                
                a, b = r
                count +=  a
                
                if b:
                    if isinstance(thing, Seq):
                        res.extendleft(b)
                    else:
                        res.appendleft(b)
            else:
                goto = False
                
            if goto : 
                # debug
#                print(f'{self.name} -goto from', thing.name)
                # ===
                continue
            
#            print(i)                
            return count, res
        
                
                    
class Seq(ast):
    def __init__(self, *ebnf, name = None, atleast = 1):
        super(Seq, self).__init__(*ebnf, name = name)
        self.atleast = atleast
        
    def match(self, objs, partial = True):
        
        N = len(objs)
        res = mode().setName(self.name)
        if not objs:
            if self.atleast is 0:
                return 0 , None
            return None
        count = 0
        
        # debug
#        i = 0
        # ===
        
        while True:
            
            # debug
#            i+=1
#            if i>20:raise
            # ===
            
            
            r = super(Seq, self).match(objs[:lim_0(N-count)], partial = True)
            if not r:
                break

            a , b = r
            
            if b:
                res.extendLeft(b)
            
            count += a
            
        if len(res) < self.atleast:
            return  None
        
        return count, res
                
                    
                
            
    
                
            
    
    
    