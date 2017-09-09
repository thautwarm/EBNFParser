#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 01:13:47 2017

@author: misakawa
"""

patten_matching = True


                
    
#class fAny(Any):
#    def __init__(self, f, name,  make = lambda x:x):
#        self.f = f
#        self.make = make
#        self.name = name
#    def __eq__(self, v):
#        return self.f(v)
    
    
from collections import deque,Iterable
    
class ast(deque):
    def setName(self,name):
        self.name = name
        return self    


class Any:
    def __init__(self, f):
        self.f = f
    def match(self, objs, partial = True):
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                return r
            return None
        
#        return None
    
class Seq:
    def __init__(self, f, atleast = 1):
        self.f = f
        self.atleast = atleast
    def match(self, objs, partial = True):
        if not objs:
            return None
        res   = ast()
        N     = len(objs)
        count = 0
        while True:
            r = self.f(objs[count:])
            if not r:
                break
            count += r[0]
            res.append(r[1])
            if count >= N:
                break
        if len(res)<self.atleast:
            return None
        if partial or count == len(objs):
            return count, res
        
class recur:pass

#        return None
    
        
#class fSeq(Seq, fAny):
#    def __init__(self, f, name, atleast = 0):
#        self.f = f
#        self.atleast = atleast
#        self.name = name
#    def match(self, objs):
#        res = []
#        count = 0
#        for obj in objs:
#            r = self.f(obj)
#            if r:
#                count += 1
#                res.append(r)
#                continue
#            else:
#                break
#        if count<self.atleast:
#            return None
#        return res 
#
#def getFSeq(atleast = 0):
#    def _1(f, name, make = lambda x:x):
#        return fSeq(f, name, make, atleast = atleast)
#    return _1        
        





class pattern:pass

def redef(self, *args, **kwargs):
    self.__init__(*args, **kwargs)
    return self


class single_pattern(pattern):
    def __init__(self, objs:'all have a method `match` that return (idx, parsed)', name=None):
        self.objs  = ast(objs)
        self.name  = name    
    
    def append(self, obj):
        if isinstance(obj, ast):
            obj = single_pattern(obj, name = self.name)
        self.objs.append(obj)
        return self
    def appendLeft(self,obj):
        if isinstance(obj, ast):
            obj = single_pattern(obj, name = self.name)
        self.objs.appendleft(obj)
        return self
    def match(self, objs, partial = True):
        return patMatch(self, objs, partial=partial)
    
class multi_pattern(pattern):
    def __init__(self, *pats, name = None):
        self.objs = ast([single_pattern(pat, name = name) if isinstance(pat, Iterable)  else pat for pat in pats])
        self.name = name
    
    def append(self, obj):
        if isinstance(obj, ast):
            obj = single_pattern(obj, name = self.name)
        self.objs.append(obj)
        return self
    def appendLeft(self,obj):
        if isinstance(obj, ast):
            obj = single_pattern(obj, name = self.name)
        self.objs.appendleft(obj)
        return self
    
    def match(self,objs, partial = True):
        for pat in self.objs:
            r = pat.match(objs, partial= partial)
            if r:
                return r

#        return None
    

def patMatch(val_obj, var, partial = True):
    print(val_obj.name,'<>' ,var, type(var))
    if not var:
        return None
    res = ast().setName(val_obj.name)
    val = val_obj.objs
    n = len(val); m = len(var)
    i = 0 ;j = 0;
    while i<n:
        r = val[i].match(var[j:])
        
        if not r:
            return None
        a, b = r
        
        if isinstance(val[i], Seq):
            for b_i in b:
                res.append(b_i)
        else:
            res.append(b)
            
        j += a
        i +=1
    if partial:
        return j, res
    if j == m :
        return j, res
    return None
    
        
    
        
            

#def patternMatch(val, var, partial = False):
#    res = []
#    n = len(val); m = len(var)
#    i = 0 ;j = 0;
#    count = 0;
#    while i<n:
#        if isinstance(val[i], pattern):
#            res_r = val[i].match(var[j:])
#            if res_r:
#                if res_r[0]: # if span is 0, do nothing
#                     j += res_r[0]
#                     res.append(res_r[1])
#            else:
#                return None
#        elif isinstance(val[i], Seq):
#            while val[i] == var[j]:
#                res.append(val[i].make(var[j]))
#                count += 1
#                j     += 1
#                if j == m:
#                    if count < val[i].atleast:
#                        return None
#                    if  all(map(lambda x: isinstance(x, Seq) and x.atleast == 0, val[i+1:])):
#                         return j, res
#                    else: 
#                         return None
#            if count < val[i].atleast:
#                return None
#            count = 0
#        else:
#            if val[i] == var[j]:
#                res.append(val[i].make(var[j]))
#                j += 1
#            else:
#                return None
#        i += 1
#    if partial:
#        return j, res
#    if m == j: return j, res
#    else : return None
                
            



            
                 
                
    

    
class PM:
    def __init__(self,*matchvalues):
        self.matchvalues=matchvalues
    def match(self, value, partial = False):
        for matchvalue in self.matchvalues:
            res = patMatch(matchvalue, value, partial=partial)
            if res:
                return res
        return False
            
