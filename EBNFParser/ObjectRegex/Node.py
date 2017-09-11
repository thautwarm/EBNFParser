#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 17:49:50 2017

@author: misakawa
"""

import re
DEBUG = False
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
    def pull(self):
        try:
            self['history'].pop()
        except IndexError:
            raise Exception("pull no thing")
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
    
def handle_error(func):
    def _f(objs, meta_info = None, partial = True):
        if not meta_info: 
            meta_info = MetaInfo()
        if  meta_info.trace:
            return func(objs, meta_info = meta_info, partial = partial)
        res = func(objs, meta_info = meta_info, partial = partial)
        if res is None:
            c = meta_info.count
            r = meta_info.rdx
            for ch in objs[c:]:
                if ch is '\n':
                    r += 1
                    c += 1
                    continue
                break
            info = " ".join(objs[c:c+10])
            if len(objs)>c+10:
                info += '...'
            raise SyntaxError(f'Syntax Error at row {r} <= {info}')
        return res
    return _f

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
                elif isinstance(e, ast):
                    e.compile
                    self.possibilities[-1].append(e)
                else:
                    self.possibilities[-1].append(e)
        del self.cache
        self.compiled = True
        return self
    
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info: 
            meta_info = MetaInfo()
        if DEBUG:
            print(f'{self.name} WITH {meta_info.trace}')
        res   = mode().setName(self.name)
        for possible in self.possibilities:
            meta_info.branch
            for thing in possible:
                history_i = (meta_info.count, thing.name)
                if thing.has_recur:
                    
                    if history_i in meta_info.trace:
                        print("Found L-R! Dealed!")
                        r = None
                    else:
                        meta_info.trace.append(history_i)
                        r = thing.match(objs, meta_info=meta_info)
                else:
                    meta_info.trace.append(history_i)
                    r = thing.match(objs, meta_info=meta_info)
                
                if r is None:
                    # nexr possible
                    res.clear()
                    meta_info.rollback
                    break
                
                if isinstance(thing, Seq):
                    res.extend(r)
                else:
                    res.append(r)
                if DEBUG:
                    print(f"{thing.name} <= {r}")
            else:
                break
            continue
        else:
            if DEBUG:
                print('RET\n')
            return None
        meta_info.pull
        if DEBUG:
            print('RET\n')
        if partial or meta_info.count == len(objs):
            if DEBUG:
                print('RET\n')
            return res
        if DEBUG:
            print('RET\n')
        return None

    
class Seq(ast):
    def __init__(self,compile_closure, *ebnf, name = None, atleast = 1):
        super(Seq, self).__init__(compile_closure, *ebnf, name = name)
        self.atleast = atleast
    def match(self, objs, meta_info=None, partial = True):
        if not meta_info: 
            meta_info = MetaInfo()
        if DEBUG:
            print(f'{self.name} WITH {meta_info.trace}')
        res   = mode().setName(self.name)
        if not objs[meta_info.count:]:
            if self.atleast is 0:
                return res
            return None
        meta_info.branch
        while True:
            r = super(Seq, self).match(objs, meta_info = meta_info)
            if r is None:
                break
            res.extend(r)
        if DEBUG:
            print(f"{self.name} <= {r}")
        if len(res) < self.atleast:
            meta_info.rollback
            return  None
        meta_info.pull
        return res
            
            
            
            
            
            
            
            