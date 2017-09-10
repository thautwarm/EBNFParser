#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 22:45:50 2017

@author: misakawa
"""

import re, warnings

class mode:
    def setName(self, name):
        self.name = name
        return self
    
class AST_Store(self, name, struts = None):
    self.name   = name
    self.struts = struts if structs else []
    
    def __add__(self, ast_store):
        pass

class MetaInfo(dict):
    
    def __init__(self, name = None, parsed=None, count = None, rdx = None, search_trace = None):
        super(MetaInfo, dict).__init__()
        self['count']        = count if count else 0
        self['rdx']          = rdx   if count else 0
        self['search_trace'] = search_trace if count else []
        self['parsed']       = parsed if parsed else AST_Store(name = name)
        if not name:
            warnings.warn("AST Node without names!!! Please do not do this in formal occasions!!")
            self.name = name
        else:
            self['name']    = [name]
        
    def bandha(self, meta):
        for key in meta:
            self[key] += meta[key]
        return self
    
    def merge(self, meta):
        return MetaInfo(**{key: self[key]+meta[key] for key in meta})
    
    def count(self, i):
        self['count'] += i
    
    def rdx(self, i):
        self['rdx'] += i
    
    def search_trace(self, list):
        self['search_trace'] += list
    
    def parsed(self, list):
        self['parsed'] += list
    

        
    

    
    
        
    


def reMatch(x, make = lambda x:x, escape = False):
    
    re_ = re.compile( re.escape(x) if escape else x)
    def _1(ys):
        if not ys: return None
        r = re_.match(ys[0])
        if not r : return None
        a, b = r.span()
        if a!=0 : raise Exception('a is not 0')
        if b is not len(ys[0]):
            return None
        return ys[0]
    return _1

class Liter:
    def __init__(self, i, name = None):
        self.f = reMatch(i)
        self.name = name
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info:
            meta_info = MetaInfo(name = self.name)
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                meta_info.count(1)
                meta_info.parsed([r])
                if r == '\n':
                    meta_info.rdx(1)
                return r
#            return None
#        return None
        
class ELiter:
    def __init__(self, i, name = None):
        self.f = reMatch(i, escape = True)
        self.name = name
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info:
            meta_info = MetaInfo(name = self.name)
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                meta_info.count(1)
                meta_info.parsed([r])
                if r == '\n':
                    meta_info.rdx(1)
                return r
#            return None
#        return None
    


class recur:pass
def redef(self, *args, **kwargs):
    self.__init__(*args, **kwargs)
    return self
    




class ast:
    def __init__(self, *ebnf, name = None):
        
        self.name     = name
        self.parent   = None
        self.possibles: 'list[mode[ast, re]]' = \
                    [ mode([self if e is recur else e for e in es]) for es in ebnf ] 
        
    
    def setP(self, parent): self.parent = parent; parent.append(self); return self
    
    def match(self, objs, meta_info=None, partial = True):
        if not meta_info:
            meta_info = MetaInfo(name = self.name)
        
        meta_info.
            
        res   = mode().setName(self.name)
        count = 0
        goto = False
        # debug
#        for i, possible in enumerate(self.possibles):
        # ===
        
        for possible in self.possibles:
            for thing in possible:
                
                
                r = thing.match(objs[count:], partial = partial)
                
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
                        res.extend(b)
                    else:
                        res.append(b)
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
            
            
            r = super(Seq, self).match(objs[count:], partial = True)
            if not r:
                break

            a , b = r
            
            if b:
                res.extend(b)
            
            count += a
            
        if len(res) < self.atleast:
            return  None
        
        return count, res
                
                    
                
            
    
                
            
    
    
    