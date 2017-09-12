#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 12:16:26 2017

@author: misakawa
"""
from ..ObjectRegex.Node import   Liter, ast, recur, Seq, ELiter,handle_error, re
Name   = Liter('[a-zA-Z_][a-zA-Z0-9]*', name = 'NAME')
Number = Liter('\d+',name = 'Number')
String = Liter("[R]{0,1}'[\w|\W]*?'", name = 'String')


L_Bracket= '\{|\}|\(|\)|\[|\]'
LBB = ELiter('{', name = 'LBB')
LB  = ELiter('[', name = 'LB')
LP  = ELiter('(', name = 'LP')
RBB = ELiter('}', name = 'RBB')
RB  = ELiter(']', name = 'RB')
RP  = ELiter(')', name = 'RP')

SeqStar = ELiter('*', name = 'SeqStar')
SeqPlus = ELiter('+', name = 'SeqPlus')

Def     = ELiter('::=', name = 'Def')
OrSign  = ELiter('|',   name = 'OrSign')

#token = re.compile(
#        '|'.join([
#        String.token_rule,
#        Name.token_rule,
#        L_Bracket,
#        SeqStar.token_rule,
#        SeqPlus.token_rule,
#        Def.token_rule,
#        OrSign.token_rule
#        ]))
  

compile_closure = globals()

Or   = ast(compile_closure,
           [recur('Atom'), Seq(compile_closure,
                              [OrSign, recur('Atom')],
                              atleast = 0,
                              name = "('|' Atom)*")
           ],
           name = 'Or')
Atom = ast(compile_closure, 
           [Name],
           [LP,recur('Atom'),RP, 
                Seq(compile_closure, 
                    [SeqStar],
                    [SeqPlus],
                    [LBB,Seq(compile_closure,
                             [Number],
                             atleast = 1,
                             atmost  = 2,
                             name    = 'Number{1,2}'
                             ),
                         RBB],
                    atleast = 0,
                    atmost  = 1,
                    name = "['*'|'+']")],
           [LB,recur('Atom'),RB],
           name = 'Atom'
           )
                
Equals = ast(compile_closure,
             [Name, Def, recur('Or')],
             name = 'Equals'
        )
    
Stmt  = ast(compile_closure,
            [Seq(compile_closure,
                [Equals],
                name = '(Equals)*',
                atleast = 0
                )],
            name = 'Stmt')
                    
                    
Atom.compile
Atom.has_recur   =True
Or.compile
Or.has_recur     =True
Equals.compile
Equals.has_recur =True
Stmt.compile
Stmt.has_recur   =True
 

        
tkr = []
for var_name in list(compile_closure.keys()):
    var= compile_closure[var_name]
    if type(var) in (ELiter, Liter):
        tkr.append(var.token_rule)
token = re.compile('|'.join(tkr))
        


