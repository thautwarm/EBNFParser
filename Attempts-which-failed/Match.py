#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:31:36 2017

@author: misakawa
"""
from .PatternMatching import  Seq, Any,patMatch, multi_pattern, redef, recur,ast, single_pattern
from ..Token import token, Number, Name, String, \
                    Bracket, Access, END, Op, NEWLINE
import re

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

# simple
name   = Any(reMatch(Name))
num    = Any(reMatch(Number))
string = Any(reMatch(String))
true   = Any(reMatch('True'))
false  = Any(reMatch('False'))
none   = Any(reMatch('None'))




Expr = multi_pattern(
        [],
        name = 'Expr'
        )
Closure = multi_pattern(
        [],
        name=None)

Atom = multi_pattern(
        [true],
        [false],
        [none],
        [name],
        [num],
        [string],
        [Expr],
        name = 'Atom')

op = Any(reMatch(Op))

Factor = multi_pattern(
        [Atom],
        name = 'Factor'
        )
Factor.appendLeft(ast([Atom, op, Factor]))
Factor.appendLeft(ast([op, Factor]))


SExpr = multi_pattern(
        [],
        name = 'SExpr'
        )
redef(SExpr,
      [Factor,
       Seq(
           multi_pattern([
                Any(reMatch('\(')),
                
#                multi_pattern([
                Seq(
                    multi_pattern([
                            Factor, 
                            Any(reMatch(','))
                            ]).match, atleast = 0),
#                Seq(Factor.match, atleast = 0),
                
#                ]),
                Any(reMatch('\)'))       
                ]).match, atleast = 0
            )
       ]
      )
#
#SExpr.appendLeft(ast([
#                  SExpr, 
#                  Any(reMatch('\(')), 
#                  Seq( 
#                    single_pattern([SExpr, Any(reMatch(','))]).match, atleast = 0), 
#                  Any(reMatch('\)'))
#                  ]
#                ))

redef(Expr,
        [Factor],
        name = 'Expr')
Expr.append(ast([
                 Expr, 
                 Any(reMatch('\(')), 
                 Seq(Expr.match, atleast = 0), 
                 Any(reMatch('\)'))
                 ]
                ))
#Expr.append(ast([
#                 Expr, 
#                 Any(reMatch('\[')), 
#                 Seq(Expr.match, atleast = 0), 
#                 Any(reMatch('\]'))]
#                ))
#Expr.appendLeft(ast([Closure]))


redef(Closure, 
       ast([Any(reMatch('\{')),
       Seq(multi_pattern([
               Expr,
               Any(reMatch(NEWLINE)),
               ]).match, atleast = 0
               ),
       Any(reMatch('\}')),
       ]),
      ast([Any(reMatch('def')),
           Any(reMatch('\(')), 
           Seq(name.match, atleast = 0),
           Any(reMatch('\)')),
           Any(reMatch('\{')),
           Seq(multi_pattern([
               Expr,
               Any(reMatch(NEWLINE)),
               ]).match,atleast = 0
               ),
           Any(reMatch('\}')),
          ]
        ),
      name= 'Closure'
      )










    
        
    

    
#class compile:
#    def __init__(self, *objs):
#        self.objs = self.objs
#    
#    def match(self, obj):
#        a = None
#        b = None
#        while True:
#            if a == 
            
            
        
        
        
        

class regex_obj:
    
    def __init__(self, *objs):
        self.objs = objs
    
    
            