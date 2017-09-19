#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:43:37 2017

@author: misakawa
"""
import sys
a = 1
sys.setrecursionlimit(68)
from Misakawa.Bootstrap.Parser import *
from Misakawa.ObjectRegex.Node import MetaInfo
from Misakawa.ErrorFamily import handle_error
meta = MetaInfo()
print(handle_error(Stmt.match)(token.findall("Number ::= R'\d+' \n Number ::= R'\d+'\n"), meta, partial= False))
