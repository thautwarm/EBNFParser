#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 22:28:51 2017

@author: misakawa

Ast.py
"""
DEBUG = True
import re
from ..ObjectRegex.Node import Ast
from ..scalable.core import groupBy, fn
_compose_eq = 0
_literal_eq = 1
_newline    = 2

def ast_for_stmts(stmt : Ast, info = None):
    if DEBUG: assert stmt.name == 'Stmt'
#    def grpFunc(stmt : Ast):
#       return  _newline if stmt.name == 'NEWLINE' else  \
#               _literal_eq if stmt[2].name == 'Str' else \
#               _compose_eq
#    grps = groupBy(grpFunc)(ast)
    row_idx = 0
    res = []    
    for eq_or_newline in stmt:
        if eq_or_newline.name == 'NEWLINE':
            row_idx += 1
            continue
        else:
            res.append(ast_for_equal(eq_or_newline, info))  
    return res
              
           
#     groupBy(lambda x : )


def ast_for_equal(eq : Ast, info = None):
    if DEBUG: assert eq.name == 'Equals'
    case = eq[2].name
    name = eq[0].value
    
    if case == 'Str':
        value = eq[2].value
        if value.startswith('R'): 
            value = value[1:]
            return f"{name} = LiteralParser({value}, name = '{name}')"
        else:
            return f"{name} = LiteralParser.Eliteral({value}, name = '{name}')"
    elif case == 'Expr':
        value = ast_for_expr(eq[2], info)
        return f"{name} = AstParser({value}, name = '{name}')"    
    
def ast_for_expr(expr : Ast, info = None):
    return ','.join(ast_for_or(or_expr, info) for or_expr in expr if or_expr.name != 'OrSign')

def ast_for_or(or_expr : Ast, info = None):
    return '[{res}]'.format(res = ','.join(ast_for_atomExpr(atomExpr, info) for atomExpr in or_expr))

   
    
