#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 10:56:12 2017

@author: misakawa
"""

import re

from copy import deepcopy
class MetaInfo(dict):
    
    def __init__(self, count=0 , rdx=0, trace = None):
        self['count'] = count
        self['trace'] = trace if trace else []
        self['rdx']   = rdx
        self['last_count'] = 0
        self['history'] = []
    
    
    @property
    def branch(self):
        self['history'].append((self.count, self.rdx, len(self.trace)))
        return self
    
    @property
    def rollback(self):
        try:
            count, rdx, length = self['history'].pop()
        except IndexError:
            return None
        self.count = count
        self.rdx   = rdx
        self.trace = self.trace[:length]
        return self
    
        
    
    @property
    def last_count(self):
        return self['last_count']
    
    @last_count.setter
    def last_count(self, v):
        self['last_count'] += v
        return self
    

  
    
    @property
    def count(self):
        return self['count']
    
    @count.setter
    def count(self,v):
        self['count'] = v
        return self
    
    @property
    def trace(self):
        return self['trace']
    
    @trace.setter
    def trace(self,v):
        self['trace'] = v
        return self
    
    @property
    def rdx(self):
        return self['rdx']
    
    @rdx.setter
    def rdx(self,v):
        self['rdx'] = v
        return self
    


    
    
    
def reMatch(x, make = lambda x:x, escape = False):
    
    re_ = re.compile( re.escape(x) if escape else x )
    def _1(y):
        if not y: return None
        r = re_.match(y)
        if not r : return None
        a, b = r.span()
        if a is not 0 : raise Exception('a is not 0')
        if b != len(y):
            return None
        return y
    return _1

class Liter:
    def __init__(self, i, name = None):
        self.f = reMatch(i)
        self.name = name
        self.has_recur = False
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info: meta_info = MetaInfo()
        if not objs[meta_info.count:]: return None
        r = self.f(objs[meta_info.count])
        if r is None or (not partial and len(objs) != 1):
            return None
        
        if r == '\n':
            meta_info.rdx += 1
        meta_info.count += 1
        
        return r
    
class ELiter:
    def __init__(self, i, name = None):
        self.f = reMatch(i, escape = True)
        self.name = name
        self.has_recur = False
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info: meta_info = MetaInfo()
        if not objs[meta_info.count:]: return None
        r = self.f(objs[meta_info.count])
        if r is None or (not partial and len(objs) != 1):
            return None
        
        if r == '\n':
            meta_info.rdx += 1
        meta_info.count += 1
        
        return r
    


class recur:
    def __init__(self, name):
        self.name = name


def redef(self, *args, **kwargs):
    self.__init__(*args, **kwargs)
    return self
    
class mode(list):
    def setName(self, name):
        self.name = name
        return self


    
        


class ast:
    def __init__(self, compile_closure, *ebnf, name = None):
        self.name     = name
        self.possibilities= []
        self.has_recur = False
        self.cache    = ebnf
        self.compile_closure = compile_closure
        self.compiled = False

    
    @property
    def compile(self):
        if self.compiled: return self
        for es in self.cache:
            self.possibilities.append([])
            for e in es:
                if e is recur:
                    self.possibilities[-1].append(self)
                    
                    if not self.has_recur:
                        self.has_recur = True
                elif isinstance(e, recur):
                    e = self.compile_closure[e.name]
                    self.possibilities[-1].append(e)
#                    if not self.has_recur:
#                        self.has_recur = e.has_recur
                elif isinstance(e, ast):
                    e.compile
                    self.possibilities[-1].append(e)
#                    if not self.has_recur:
#                        self.has_recur = e.has_recur
                else:
                    self.possibilities[-1].append(e)
        del self.cache
        self.compiled = True
        return self
        
    def match(self, objs, meta_info = None, partial = True):
        
        if not meta_info: 
            meta_info = MetaInfo()
        print("   "*meta_info.rdx, self.name, meta_info.trace)
        try:
            print(f"ready to parsed-begin:{objs[meta_info.count]}",)
        except:
            print(None)
        # debug
#        for i, possible in enumerate(self.possibilities):
        # ===
        
        for possible in self.possibilities:
            meta_info.branch
            res   = mode().setName(self.name)
            for thing in possible:
                # eliminates the left recursion 
                if thing.has_recur:
                    history_i = (meta_info.count, thing.name)
                    if history_i in meta_info.trace:
                        print("Found L-R! Dealed!")
                        r = None
                    else:
                        meta_info.trace.append(history_i)
                        r = thing.match(objs, meta_info=meta_info, partial = True)
                else:
                    r = thing.match(objs, meta_info=meta_info, partial = True)
                
                
                # debug
                print(f"{self.name} -- {thing.name} <=", r)
                # ===
            
                if r is None:
                    # nexr possible
                    res.clear()
                    meta_info.rollback
                    break
                
                print()
                if isinstance(thing, Seq):
                    res.extend(r)
                else:
                    res.append(r)
                print('Added Seq ', res)
                
            else:
                break
            continue
        else:
            print('RET')
            print()
            return None
        print('RET')
        print()
        return res
                
                    
class Seq(ast):
    def __init__(self,compile_closure, *ebnf, name = None, atleast = 1):
        super(Seq, self).__init__(compile_closure, *ebnf, name = name)
        self.atleast = atleast
        
    def match(self, objs, meta_info=None, partial = True):
        if not meta_info: 
            meta_info = MetaInfo()
            
#        # eliminates the left recursion 
#        if self.has_recur and self.name:
#            history_i = (meta_info.count, self.name)
#            if history_i in meta_info.trace:
#                print("Found L-R! Dealed!")
#                return None
#            else:
#                meta_info.trace.append(history_i)
                                  
        res   = mode().setName(self.name)
        
        
        if not objs[meta_info.count:]:
            if self.atleast is 0:
                return res
            return None
        
        # debug
#        i = 0
        # ===
        meta_info.branch
        while True:
            
            # debug
#            i+=1
#            if i>20:raise
            # ===
            r = super(Seq, self).match(objs, meta_info = meta_info, partial = True)
            print(f' SEQ {self.name} : {res}')
            if r is None:
                break
            res.extend(r)
            
            
        if len(res) < self.atleast:
            meta_info.rollback
            return  None

        return res
                
                    
                
            
    
                
            
    
    
    
