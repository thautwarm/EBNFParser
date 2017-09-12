#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 22:34:41 2017

@author: misakawa
"""

def ast_for_stmt(mode):
    pass

def ast_for_equals(mode):
    pass

def ast_for_atomexpr(mode):
    pass

def ast_for_Atom(mode):
    """ Atom    ::= Name | String | '[' Expr ']' | '(' Expr ')' """
    n = len(mode)
    if n is 1:
        if mode.name == 'Name':
            pass
    pass

def ast_for_trailer(mode):
    pass

def ast_for_or(mode):
    pass

def ast_for_expr(mode):
    pass

