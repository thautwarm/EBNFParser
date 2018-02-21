#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 22:28:51 2017

@author: misakawa

Ast.py
"""
DEBUG = True
from ..ObjectRegex.Node import Ast
from .. import ErrorFamily
import re, os
esc = lambda str: str.replace("'",r"\'").replace('"',r'\"')
_compose_eq = 0
_literal_eq = 1
_newline    = 2

def ast_for_stmts(stmts : Ast, info = None):
    global codesDefToken
    if DEBUG: assert stmts.name == 'Stmt'
    res = []   
    to_compile= []
    DefTokenInEBNF= True
    if stmts[0].name  == 'Using':
        usingType =  stmts[0][1].name  
        if usingType == 'Name':
            usingFrom =  stmts[0][1].value  
            if usingFrom == 'list':
                codesDefToken = 'list'
            else:
                with open(f"./{os.path.join(usingFrom.split('.'))}") as read_from:
                    codesDefToken = read_from.read()
        else:
            codesDefToken = stmts[0][1].value[2:-2]
        DefTokenInEBNF    = False      
        stmts = stmts[1:]
        
    for eq in stmts:
        define, tp = ast_for_equal(eq, info)
        if tp is None:
            to_compile.append(eq[0].value)
        elif DefTokenInEBNF:
            status, tk = tp
            if status is 'R':
                info['regex'].append(tk)
            if status is 'L':
                info['raw'].append(f"'{re.escape(tk[1:-1])}'")
        res.append(define) 
    tks = info if DefTokenInEBNF else codesDefToken
    return res, tks, to_compile
              
           
#     groupBy(lambda x : )


def ast_for_equal(eq : Ast, info):
    if DEBUG: assert eq.name == 'Equals'
    case = eq[1].name
    name = eq[0].value
    if case == 'LitDef':
        value = eq[2].value
        if value.startswith('R'): 
            value = value[1:]
            return f"{name} = LiteralParser({value}, name = '{name}')", ('R', value)
        elif value.startswith('K'):
            value = value[1:]
            return f"{name} = LiteralParser({value}, name = '{name}')", ('K', value)
        else:
            return f"{name} = LiteralParser.Eliteral({value}, name = '{name}')", ('L', value)
    else:
        value = ast_for_expr(eq[-1], info)
        toIgnore = eq[2:-2]
        if not toIgnore:
            return f"{name} = AstParser({','.join(value)}, name = '{name}')", None
        else:
            toIgnore = {ignore.value for ignore in toIgnore}
            return f"{name} = AstParser({','.join(value)}, name = '{name}', toIgnore={toIgnore})", None
            
    
def ast_for_expr(expr : Ast, info):
    return [ast_for_or(or_expr, info) for or_expr in expr if or_expr.name != 'OrSign']

def ast_for_or(or_expr : Ast, info):
    return '[{res}]'.format(res = ','.join(ast_for_atomExpr(atomExpr, info) for atomExpr in or_expr))

def ast_for_atomExpr(atomExpr : Ast, info):
    
    res =  ast_for_atom(atomExpr[0], info)
    if len(atomExpr) is 2:
        case = atomExpr[1][0].name
        if case == 'SeqStar':
            res = ast_for_trailer(f"[{res}]", info)
        elif case == 'SeqPlus':
            res = ast_for_trailer(f"[{res}]", atleast = 1, info = info)
        elif case == 'LBB':
            atleast = atomExpr[1][1].value
            case    = atomExpr[1][2].name
            if case == 'RBB':
                res = ast_for_trailer(f"[{res}]", atleast = atleast, info = info)
            else:
                atmost = atomExpr[1][2].value
                res = ast_for_trailer(f"[{res}]", atleast = atleast, atmost = atmost, info = info)
    return res

def ast_for_atom(atom : Ast, info):
    n = len(atom)
    if n is 1:
        liter = atom[0]
        if liter.name == 'Name':
            return f"Ref('{liter.value}')"
        elif liter.name == 'Str':
            string = liter.value
            if string.startswith('R'):
                string = string[1:]
                if string not in info['regex']:
                    info['regex'].append(string)
                return f"LiteralParser({string}, name = '{esc(string)}')"
            elif string.startswith('K'):
                string = string[1:]
                return f"LiteralParser({string}, name = '{esc(string)}')"
            else:
                toadd = f"'{re.escape(string[1:-1])}'"
                if toadd not in info['raw']:
                    info['raw'].append(toadd)
                return f"LiteralParser.Eliteral({string}, name = '{esc(string)}')"
        else:
            raise ErrorFamily.UnsolvedError("Unsolved Literal Parsed Ast.")
    else:
        if DEBUG:
            assert n is 3
        case = atom[0].name
        if case == 'LB':
            value = ','.join(ast_for_expr(atom[1], info = info))
            return ast_for_trailer(f"{value}", atleast = 0, atmost = 1, info = info)
        elif case == 'LP':
            or_exprs = ast_for_expr(atom[1], info = info)
            if len(or_exprs) is 1:
                return or_exprs[0][1:-1]
            value = ','.join(or_exprs)
            return ast_for_trailer(f"{value}", atleast = 1, atmost = 1, info = info)
        else:
            ErrorFamily.UnsolvedError("Unsolved Atom Parsed Ast.")


def ast_for_trailer(series_expr, info, atleast = 0, atmost = None):
    if atleast is 0:
        if atmost is None:
            return f"SeqParser({series_expr})"
        else:
            return f"SeqParser({series_expr}, atmost = {atmost})"
    else:
        if atmost is None:
            return f"SeqParser({series_expr}, atleast = {atleast})"
        else:
            return f"SeqParser({series_expr}, atleast = {atleast}, atmost = {atmost})"





    
    
        
        

   
    
