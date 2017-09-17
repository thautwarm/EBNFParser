#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 15:23:36 2017

@author: misakawa

"""

# CONFIG
DEBUG = True


from .. import ErrorFamily

class Tools:
    import re
    @staticmethod
    def reMatch(x, escape=False):
        token_rule = Tools.re.escape(x) if escape else x
        regex      = Tools.re.compile(token_rule)
        def _1(y):
            if not y: return None
            r = regex.match(y)
            if not r: return None
            a, b = r.span()
            if a is not 0:
                raise Exception('Do not match string at the first character.')
            if b != len(y):
                return None
            return y
        return token_rule, _1
    @staticmethod
    def check_obj(check_func):
        def _1(func):
            def _2(self, *args, **kwargs):
                if not check_func(self):
                    raise ErrorFamily.CheckConditionError(f"{func.__name__} checked failed.")
                return func(self, *args, **kwargs)
            return _2
        return _1

class MetaInfo:
    
    """
    Meta information when parsing.

        `count` is a property of MetaInfo.
        It shows that how many tokenized(words) have been parsed,
            which could be used for
                - Alerting.
                - Eliminating left recursions.

        `trace` is a property of MetaInfo.
        It shows a trace of recursive BNF Nodes,
            which could be used for
                - Debugging.
                - Eliminating left recursions.

        `rdx` is a property of MetaInfo.
        It shows how many lines have beeb parsed now.
            which could be used for
                - Alerting.
                - Debugging.

    """

    def __init__(self, count=0, rdx=0, trace=None):
        """

        :rtype: MetaInfo
        """
        self.count   = count
        self.trace   = trace if trace else []
        self.rdx     = rdx
        self.history = []

    def branch(self):
        """
        Save a record of parsing history in order to trace back. 
        """
        self.history.append((self.count, self.rdx, len(self.trace)))

    def rollback(self):
        """
        Trace back.
        """
        try:
            count, rdx, length =self.history.pop()
        except IndexError:
            return None
        self.count = count
        self.rdx = rdx
        self.trace = self.trace[:length]

    def pull(self):
        """
        Confirm the current parsing results.
        Pop a record in parsing history.
        """
        try:
            self.history.pop()
        except IndexError:
            raise Exception("pull no thing")



class BaseParser:
    """Abstract Class"""
    name       = None
    has_recur  = None
    def __init__(self, *args, **kwargs):
        try:
            initial_method = getattr(self, eval("self.__class__.__name__"))
        except AttributeError:
            raise ErrorFamily.ObjectUsageError(f"No constructor for class `{self.__class__}` has been defined!")
        initial_method(*args, **kwargs)
    def match(self, objs, meta, partial):
        """Abstract Method"""
        pass

class Ast:
    """To Store Ast Structures(Parsed)."""
    
    name = None
    def __init__(self, *v, type = list, name = None):
        self.value = type(*v)
        self.name  = name
        
    def __getitem__(self, v):
        return self.value.__getitem__(v)
    
    @property
    def type(self):
        return self.value.__class__
    
    @Tools.check_obj(lambda self: self.value.__class__ is list)
    def append(self, v):
        self.value.append(v)
        
    def dump(self, indent = 0):
        space = ' '*(4*indent+1)
        if isinstance(self.value, str):
            value = 'NEWLINE' if self.value is '\n' else self.value
            return f"{self.name}[{value}]\n{space}"
        else:
            body = ''.join(map(lambda x:x.dump(indent+1), self.value))
            return f"{self.name}[{body}]\n{space}"
    def setName(self, name):
        self.name = name
        return self

    def __str__(self, i=0):
        body  = " ".join([item.__str__(i + 1) for item in self])
        space = '  ' * (i + 1)
        return f'{self.name}[{body}]\n{space}'

class LiteralParser(BaseParser):
    def LiteralParser(self, regex_str, name = None, escape = False):
        self.name      = name
        self.has_recur = False
        self.token_rule,self.match_func = Tools.reMatch(regex_str, escape = escape) 

    def match(self, objs, meta_info, partial=True):
        left = len(objs) - meta_info.count;
        if not left: return None
        r = self.f(objs[meta_info.count])
        if r is None or (not partial and left != 1):
            return None
        if r is '\n':
            meta_info.rdx += 1
        meta_info.count += 1
        return Ast(r, type = str, name = self.name if self.name else r)
    
    @staticmethod
    def Eliteral(regex_str, name):
        return LiteralParser(regex_str, name = name, escape = True)
    

class LazyDefParser(BaseParser):
    def init(self, name):self.name = name

class AstParser(BaseParser):
    def AstParser(self, *ebnf, name = None): 
        self.name          = name
        
        # the possibilities for an series of input tokenized words.
        self.possibilities = [] 
        
        self.has_recur     = False
        self.cache         = ebnf
        self.compiled      = False
    
    def compile(self, namespace: dict, recurSearcher: set):
        
        if self.name:
            if self.name in recurSearcher:
                self.has_recur = True
                self.compiled  = True
            else:
                recurSearcher.add(self.name)
        
        if self.compiled: return self
        
        for es in self.cache:
            self.possibilities.append([])
            for e in es:
                if isinstance(e, LiteralParser):
                    self.possibilities[-1].append(self)
                elif isinstance(e, LazyDefParser):
                    e = namespace[e.name]
                    e.compile(namespace, recurSearcher)
                    self.possibilities[-1].append(e)
                    if self.name and e.has_recur:
                        self.has_recur = True
                        
                elif isinstance(e, AstParser):
                    e.compile(namespace, recurSearcher)
                    self.possibilities[-1].append(e)
                    if self.name and e.has_recur:
                        self.has_recur = True
                else:
                    raise ErrorFamily.UnsolvedError("Unknown Parser Type.")
                
        if DEBUG and self.has_recur: print(f"Found recursive Parser {self.name}")
        
        if hasattr(self, 'cache'):
            del self.cache
        
        if not self.compiled: self.compiled = True
        

def SeqParser(AstParser):
    def init(self, *ebnf, name=None, atleast=1, atmost=None):
        AstParser.__init__(self, *ebnf, name = name)
        self.atleast = atleast
        self.atmost  = atmost
    
    
        


        
    


