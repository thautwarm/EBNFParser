#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:24:21 2017

@author: misakawa
"""

from EBNFParser.ObjRegex.MetaBNF import *
import sys
from EBNFParser.Token import token
sys.setrecursionlimit(150)



# flowpython

#x = Trailer.match(token.findall('()'))
#print()
#f = Trailer.match(['(',')'])
#print(f'result => {f}')
#print('SPLIT')
#f = Expr.match(token.findall('1+2'))
#print(f'result => {f}')
#print('SPLIT')
f = Expr.match(token.findall('def f(a b c){ c(a b)'))
print(f'result => {f}')
#print(x)
#Expr.match('a(a(a))' ->> token.findall) ->> print
#Expr.match('{1+2}'->>token.findall) ->> print
#Expr.match('def f(a b c){ c(a b) }' ->> token.findall) ->> print
#Expr.match('f = def (a){ a+1 }'->>token.findall)->>print