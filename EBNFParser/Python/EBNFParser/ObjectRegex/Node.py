#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 17:49:50 2017

@author: misakawa
"""

import re
DEBUG = False
class MetaInfo(dict):
    """
    Meta information when parsing.
    """
    def __init__(self, count=0 , rdx=0, trace = None):
        self['count'] = count
        self['trace'] = trace if trace else []
        self['rdx']   = rdx
        self['history'] = []
    
    
    @property
    def branch(self):
        """
        Save a record of parsing history in order to trace back. 
        """
        self['history'].append((self.count, self.rdx, len(self.trace)))
        return self
    
    @property
    def rollback(self):
        """
        Trace back.
        """
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
        """
        Confirm the current parsing results.
        Pop a record in parsing history.
        """
        try:
            self['history'].pop()
        except IndexError:
            raise Exception("pull no thing")
        return self

    

  
    
    @property
    def count(self):
        """
        `count` is a property of MetaInfo.
        It shows that how many tokenized(words) have been parsed, 
            which could be used for
                - Alerting.
                - Eliminating left recursions.
        """
        return self['count']
    
    @count.setter
    def count(self,v):
        self['count'] = v
        return self
    
    @property
    def trace(self):
        """
        `trace` is a property of MetaInfo.
        It shows a trace of recursive BNF Nodes,
            which could be used for
                - Debugging.
                - Eliminating left recursions.
        """
        return self['trace']
    
    @trace.setter
    def trace(self,v):
        self['trace'] = v
        return self
    
    @property
    def rdx(self):
        """
        `rdx` is a property of MetaInfo.
        It shows how many lines have beeb parsed now.
            which could be used for
                - Alerting.
                - Debugging.
        
        """
        return self['rdx']
    
    @rdx.setter
    def rdx(self,v):
        self['rdx'] = v
        return self
    
    
class simple_mode(str):
    """
    a `simple_mode` is a `str` which has a name. 
    """
    def setName(self,name):
        self.name = name
        return self
    def __str__(self, i = 0):
        body = super(simple_mode, self).__str__()
        body = f"['{body}']" if body != '\n' else r'[\n]'+'\n'+'  '*(i+1)
        return f"{self.name} {body}"
    
class mode(list):
    """
    a `mode` is a `list` which has a name. 
    """
    def setName(self, name):
        self.name = name
        return self
    def __str__(self, i = 0):
        body  = " ".join([ item.__str__(i+1) for item in  self])
        space = '  '*(i+1) 
        return f"{self.name}[{body}]\n{space}"
    
    
    
def reMatch(x, make = lambda x:x, escape = False):
    token_rule = re.escape(x) if escape else x
    re_        = re.compile( token_rule )
    
    def _1(y):
        if not y: return None
        r = re_.match(y)
        if not r : return None
        a, b = r.span()
        if a is not 0 : raise Exception('a is not 0')
        if b != len(y):
            return None
        return y
    return token_rule, _1


class Liter:
    """
    Literal which can be initialized by an escaped string. 
    """
    def __init__(self, i, name = None):
        self.token_rule, self.f = reMatch(i)
        self.name = name
        self.has_recur = False
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info: meta_info = MetaInfo()
        
        left = len(objs) - meta_info.count;
        if not left: return None
        r = self.f(objs[meta_info.count])
        if r is None or (not partial and left != 1):
            return None
        
        if r == '\n':
            meta_info.rdx += 1
        meta_info.count += 1
        return simple_mode(r).setName(self.name)
    
class ELiter:
    """
    Literal which can be initialized by a raw string. 
    """
    def __init__(self, i, name = None):
        self.token_rule, self.f = reMatch(i, escape = True)
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
        return simple_mode(r).setName(self.name)
    
class recur:
    def __init__(self, name):
        self.name = name


def redef(self, *args, **kwargs):
    self.__init__(*args, **kwargs)
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
    def __init__(self,compile_closure, *ebnf, name = None, atleast = 1, atmost = None):
        super(Seq, self).__init__(compile_closure, *ebnf, name = name)
        self.atleast = atleast
        self.atmost  = atmost 
    def match(self, objs, meta_info=None, partial = True):
        if not meta_info: 
            meta_info = MetaInfo()
        if DEBUG:
            print(f'{self.name} WITH {meta_info.trace}')
        res     = mode().setName(self.name)
        atleast = self.atleast
        if not objs[meta_info.count:]:
            if atleast is 0:
                return res
            return None
        meta_info.branch
        atmost = self.atmost
        idx = 0
        if atmost:
            
            while True:
                if idx >= atmost:
                    break
                r = super(Seq, self).match(objs, meta_info = meta_info)
                if r is None:
                    break
                res.extend(r)
                idx += 1
        else:
            while True:
                r = super(Seq, self).match(objs, meta_info = meta_info)
                if r is None:
                    break
                res.extend(r)
                idx+=1
        if DEBUG:
            print(f"{self.name} <= {r}")
        if idx < self.atleast:
            meta_info.rollback
            return  None
        meta_info.pull
        return res
            
            
            
            
            
            
            
            