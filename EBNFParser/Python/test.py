#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:24:21 2017

@author: misakawa
"""

from EBNFParser.Parser.ExpyParser import handle_error, Stmt
import sys
from EBNFParser.Token import token
sys.setrecursionlimit(300)
parser = handle_error(Stmt.match)


try:
    f = parser(token.findall('(1 2 3)'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e
    

try:
    f = parser(token.findall('f(1 2 3)'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e
    

try:
    f = parser(token.findall('def (){1 2 3}'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e


try:
    f = parser(token.findall('def (){ (1 2 3) }'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e

try:
    f = parser(token.findall('def f(a b){ (a+b) }'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e


try:
    f = parser(token.findall('def (a){ def (c) {a+c} }'), partial= False)
    assert f[0][0][0][0][0].name == 'Closure'
    print(f'result =>\n{f}')
except Exception as e:
    raise e
    
try:
    f = parser(token.findall('f(a(b))'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e
    
try:
    f = parser(token.findall('q"123+s"'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e
    
try:
    f = parser(token.findall('q"123+s"'), partial= False)
    print(f'result =>\n{f}')
except Exception as e:
    raise e
