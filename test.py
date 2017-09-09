#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:24:21 2017

@author: misakawa
"""

from EBNFParser.ObjRegex.BNF import *
import sys
from EBNFParser.Token import token
sys.setrecursionlimit(60)



# flowpython

Expr.match('a()' ->> token.findall) ->> print
#Expr.match('a(a(a))' ->> token.findall) ->> print
#Expr.match('{1+2}'->>token.findall) ->> print
#Expr.match('def f(a b c){ c(a b) }' ->> token.findall) ->> print
#Expr.match('f = def (a){ a+1 }'->>token.findall)->>print