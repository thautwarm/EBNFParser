#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 19:44:21 2017

@author: misakawa
"""
import warnings
from .typepy import strict
import re



        
        


left  = 1
right = 0

class Graminit:
    """
    
    . match(str)
    . __eq__(Graminit)
    . code : int
    . children : dict[int, Graminit]
    . parser_direct := {left|right}
    
    """
    
    code_num = 0
    code_dic = dict()
    

class GrammarAtom(Graminit):
    @strict.args(Graminit, str, re.compile(" ").__class__)
    def __init__(self, id, re):
        self.code = Graminit.code_num
        Graminit.code_dic[Graminit.code_num] = id
        Graminit.code_num +=1
        
        self.re    = re
        self.match = lambda Str: self.re.match(Str).span()
        
    @strict.args(Graminit, Graminit)
    def __eq__(self, v):
        return self.code == v.code
    
class Atoms:
    Number = GrammarAtom('Number', re.compile('\d+'))  
    Name   = GrammarAtom('Name',   re.compile('[a-zA-Z_][a-zA-Z0-9]*'))
    String = GrammarAtom('String', re.compile('[a-z]{0,1}"[\w|\W]*"'))
    L_None = GrammarAtom('Liter_None', re.compile('None'))
    L_True = GrammarAtom('Liter_True', re.compile('True'))
    L_False= GrammarAtom('Liter_False',re.compile('False'))



class Grammar(Graminit):
    
    def __init__(self, id, match = None, children = None, parser_direct = left ):
        self.code = Graminit.code_num
        Graminit.code_dic[Graminit.code_num] = id
        Graminit.code_num +=1
        
        self.children = children
        self.parser_direct = parser_direct

        if children:
            if match:
                warnings.warn("Don't need param <match>.")
            def _match(Str):
                orders = self.children.keys()
                for order in orders:
                    tmp = self.children[order].match(Str)
                    if tmp.match(Str):
                        return tmp
                return None
            self.match = _match
            
        else:
            # for atom
            self.match = match
            
    @strict.args(Graminit, Graminit)
    def __eq__(self, v):
        return self.code is v.code

            

                        



