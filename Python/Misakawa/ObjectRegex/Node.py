#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 15:23:36 2017

@author: misakawa

"""

# CONFIG
DEBUG = False


from .. import ErrorFamily
from ..ErrorFamily import MetaInfo
from typing import List
import warnings



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
#            if a is not 0:
#                raise Exception('Do not match string at the first character.')
            if b != len(y):
                return None
            return y
        return token_rule, _1

class BaseParser:
    """Abstract Class"""
    name       = None
    has_recur  = None
    def match(self, objs, meta, partial):
        """Abstract Method"""
        pass

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

class LiteralParser(BaseParser):
    def __init__(self, regex_str, name = None, escape = False):
        self.has_recur = False
        self.token_rule,self.match_func = Tools.reMatch(regex_str, escape = escape) 
        self.isRegex   = not escape
        if name is None:
            self.name = self.token_rule
        else:
            self.name = name
            
    def match(self, objs, meta, partial=True):
        left = len(objs) - meta.count;
        if not left: return None
        r = self.match_func(objs[meta.count])
        if r is None or (not partial and left != 1):
            return None
        if r is '\n':
            meta.rdx += 1
        meta.count += 1
        return Ast(meta.clone(), r, type = str, name = self.name if self.name else r)
    
    @staticmethod
    def Eliteral(regex_str, name):
        return LiteralParser(regex_str, name = name, escape = True)
    



class Ref(BaseParser):
    def __init__(self, name):self.name = name


class AstParser(BaseParser):
    def __init__(self, *ebnf, name = None, toIgnore : set = None):
        
        # each in the cache will be processed into a parser.
        self.cache          = ebnf
        
        # the possible output types for an series of input tokenized words.
        self.possibilities  = []  
        
        # whether this parser will refer to itself.
        self.has_recur      = False
        
        
        # the identity of a parser.
        
        self.name           = name if name is not None else \
                ' | '.join(' '.join(map(lambda parser : parser.name,ebnf_i)) for ebnf_i in ebnf)
        
        # is this parser compiled, must be False when initializing.
        self.compiled       = False
        
        #  if a parser's name is in this set, the result it output will be ignored when parsing.
        self.toIgnore       = toIgnore
        
    
    def compile(self, namespace: dict, recurSearcher: set):
        if self.name in recurSearcher:
            self.has_recur = True
            self.compiled = True
        else:
            recurSearcher.add(self.name)

        if self.compiled:
            return self

        for es in self.cache:
            self.possibilities.append([])
            for e in es:
                if isinstance(e, LiteralParser):
                    self.possibilities[-1].append(e)
                elif isinstance(e, Ref):
                    e = namespace[e.name]
                    if isinstance(e, AstParser):
                        e.compile(namespace, recurSearcher)
                    self.possibilities[-1].append(e)
                    if e.has_recur:
                        self.has_recur = True
                elif isinstance(e, AstParser):
                    if e.name not in namespace:
                        namespace[e.name] = e
                    else:
                        e = namespace[e.name]
                    e.compile(namespace, recurSearcher)
                    self.possibilities[-1].append(e)
                    if e.has_recur:
                        self.has_recur = True
                else:
                    raise UnsolvedError("Unknown Parser Type.")

        if hasattr(self, 'cache'):
            del self.cache

        if self.name in recurSearcher:
            recurSearcher.remove(self.name)

        if not self.compiled:
            self.compiled = True
        
    def match(self, objs, meta, partial = True):
        res = Ast(meta.clone(), type = list, name = self.name)
        recursivePossibilities = []
        if DEBUG:
            print(f"{self.name} WITH {meta.trace}")
        for possibility in self.possibilities:
            meta.branch()
            status = patternMatching(self, res, objs, meta,
                                     possibility, recursivePossibilities)

            if status is Matched:
                break
            elif status is GotoNext:
                continue
        else:
            """ end case 1: no possibility matched.
                Meta-information has been rollbacked!
            """
            return None
        meta.pull()
        if recursivePossibilities:
            while True:
                for possibility in recursivePossibilities:
                    meta.branch()
                    recurRes = Ast(meta.clone(), type=list, name=self.name)
                    status = patternMatching(self, recurRes, objs, meta,
                                             possibility, None)
                    if status is GotoNext:
                        continue
                    elif status is Matched:
                        meta.pull()
                        r   = res
                        res = Ast(meta.clone(), type=list, name=self.name)
                        res.append(r)
                        res.extend(recurRes)
                        break
                else:
                    break

        if partial or meta.count == len(objs):
            """ end case 2: found a possibility matched and match exactly.
            """
            return res

        """ end case 3: although a possibility matched, do not match exactly.
            (do not match in partial mode and do not match completely).
        """
        return None



GotoNext   = object()
Matched    = object()
continueLR = object()

def patternMatching(self:AstParser,
                    res:Ast,
                    objs:List[str],
                    meta:MetaInfo,
                    possibility:List[BaseParser],
                    recursivePossibilities:List[List[BaseParser]] = None)->object:

    for ast_struct in possibility:
        history = (meta.count, ast_struct.name)
        if ast_struct.has_recur:
            if history in meta.trace:
                if DEBUG:
                    print("Found L-R! Dealed!")
                r = None
                if recursivePossibilities is not None:
                    if len(possibility)>1:
                        recursivePossibilities.append(possibility[1:])
                    else:
                        warnings.warn("Invalid left recursion. => a ::= a | ... ;")
            else:
                meta.trace.append(history)
                r = ast_struct.match(objs, meta=meta)
        else:
            if DEBUG:
                meta.trace.append(history)
            r = ast_struct.match(objs, meta=meta)
        if r is None:
            res.clear()
            meta.rollback()
            return GotoNext
        if isinstance(ast_struct, SeqParser):
            if not self.toIgnore:
                res.extend(r)
            else:
                for _r in r:
                    if _r.name not in self.toIgnore:
                        res.append(_r)
        else:
            if not self.toIgnore or r.name not in self.toIgnore:
                res.append(r)
        if DEBUG:
            print(f"{ast_struct.name} << \n{r}")
    else:
        return Matched
            
                    
    
        

class SeqParser(AstParser):
    def __init__(self, *ebnf, name=None, atleast=0, atmost=None):
        super(SeqParser, self).__init__(*ebnf, name = name)
        if atmost is None:
            if atleast is 0:
                self.name = f"({self.name})*"
            else:
                self.name = f"({self.name}){{{atleast}}}"
        else:
            self.name = f"({self.name}){{{atleast},{atmost}}}"
        self.atleast = atleast
        self.atmost  = atmost

    def match(self, objs, meta, partial=True):
        res = Ast(meta.clone(), type = list, name = self.name)
        if meta.count == len(objs):
            if self.atleast is 0:
                return res
            return None
        meta.branch()
        idx = 0
        if self.atmost is not None:
            """ (ast){a b} """
            while True:
                if idx >= self.atmost:
                    break
                r = super(SeqParser, self).match(objs, meta=meta)
                if r is None:
                    break
                res.extend(r)
                idx += 1
        
        else:
            """ ast{a} | [ast] | ast* """
            
            while True:
                r = super(SeqParser, self).match(objs, meta=meta)
                if r is None:
                    break
                res.extend(r)
                idx += 1
                
        if DEBUG:
            print(f"{self.name} << \n{r}")
        
        if idx < self.atleast:
            meta.rollback()
            return None
        meta.pull()
        return res
        
        
    
        


        
    


