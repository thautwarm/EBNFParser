#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 18:47:20 2017

@author: misakawa
"""
# ===========
import re

L_Number = '\d+|\d*\.\d+'  

L_Name   = '[a-zA-Z_][a-zA-Z0-9]*'

L_String = '[a-z]{0,1}"[\w|\W]*"'

L_Bracket= '\{|\}|\(|\)|\[|\]'

L_Access = '\.'

L_END    = ';'

L_NEWLINE= '\n'

L_Comment = '#[\w|\W]*?\n'

L_Op = '|'.join(['//', 
               '/' ,
               '\|',
               '\|\|',
               '>>','<<',
               '>=','<=',
               '<-',
               '>' ,'<', 
               '=>','->',
               '\?', 
               '--',
               '\+\+', 
               '\*\*',
               '\+','-','\*','==','=','~',
               '@',
               '\$',
               '%',
               '\^',
               '&',
               '\!',
               '\:\:',
               '\:',
               ])

def reMatch(x, make = lambda x:x):
    re_ = re.compile(x)
    def _1(ys):
        if not ys: return None
        r = re_.match(ys[0])
        if not r : return None
        a, b = r.span()
        if a!=0 : raise Exception('a is not 0')
        if b is not len(ys[0]):
            return None
        return 1, ys[0]
    return _1

class Liter:
    def __init__(self, i):
        self.f = reMatch(i)
    def match(self, objs, partial = True):
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                return r
            return None

Name   = Liter(L_Name)
String = Liter(L_String)
Number = Liter(L_Name)
Access = Liter(L_Access)
Bracket= Liter(L_Bracket)
NEWLINE= Liter(L_NEWLINE)
END    = Liter(L_END)
Comment= Liter(Comment)





class recur:pass

    
class mode(list):
    def setName(self, name):
        self.name = name



class ast:
    def __init__(self, *ebnf, name = None):
        
        self.name     = name
        self.parent   = None
        self.possibles: 'list[mode[ast, re]]' = \
                    [ mode([self if e is recur else e for e in es]) for es in ebnf ] 
        
    
    def setP(self, parent): self.parent = parent; parent.append(self); return self
    
    def match(self, objs, partial = True):
        res   = mode().setName(self.name)
        count = 0
        for possible in self.possibles:
            for thing in possible:
                r = thing.match(objs[count:], partial = partial)
                if not r:
                    # nexr possible
                    res.clear()
                    count = 0
                    break
                
                a, b = r
                count +=  a
                
                if b:
                    if isinstance(thing, Seq):
                        res.extend(b)
                    else:
                        res.append(b)
                        
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
        while True:
            
            r = super(Seq, self).__init__(objs, partial = True)
            if not r:
                break
            
            a , b = r
            res.extend(b)
            
            count += a
            
        if count < self.atleast:
            return  None
        
        return count, res
                
                    
                
            
    
                
            
    
    
    