#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 01:05:06 2017

@author: misakawa
"""

# Meta BNF


from .NodeBNF import   Liter, ast, recur, Seq, ELiter
L_Number = '\d+|\d*\.\d+'  

L_Name   = '[a-zA-Z_][a-zA-Z0-9]*'

L_String = '[a-z]{0,1}"[\w|\W]*"'

L_Bracket= '\{|\}|\(|\)|\[|\]'

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

Name   = Liter(L_Name, 'Name')
String = Liter(L_String,'String')
Number = Liter(L_Number,'Number')
Bracket= Liter(L_Bracket,'Bracket')
NEWLINE= Liter(L_NEWLINE,'NEWLINE')
END    = Liter(L_END,'END')
Comment= Liter(L_Comment,'Comment')
Op     = Liter(L_Op,'Op')


LBB = ELiter('{', name = 'LBB')
LB  = ELiter('[', name = 'LB')
LP  = ELiter('(', name = 'LP')

RBB = ELiter('}', name = 'RBB')
RB  = ELiter(']', name = 'RB')
RP  = ELiter(')', name = 'RP')
Def = Liter('def(?![a-zA-Z_0-9])', name = 'Def')


compile_closure = globals()

Atom = ast(compile_closure,
           [Number],
           [String],
           [Liter('True(?![a-zA-Z_0-9])',name = 'True')],
           [Liter('False(?![a-zA-Z_0-9])',name = 'False')],
           [Liter('None(?![a-zA-Z_0-9])', name = 'None')],
           [Name],
           name = 'Atom')

Closure = ast(compile_closure,
              [LBB, 
               Seq(compile_closure,
                   [recur('Expr'),
                    Seq(compile_closure,
                        [NEWLINE], 
                        atleast = 0, name = '(NEWLINE)*')
                    ],atleast = 0, name = '(Expr (NEWLINE)*)*'),
               RBB
               ],
               [Def,  # lambda 
               LP,
               Seq(compile_closure,
                   [Name],
                   atleast = 0, name = '(Name)*'),
               RP,
               recur
               ]        
               ,
               [Def, # function with Name definition.
                Name,
                LP,
                Seq(compile_closure,
                    [Name],
                    atleast = 0, name = '(Name)*'),
                RP,
                recur
                ],
              name = 'Closure'
              )

BinOp = ast(compile_closure,
            [recur('Expr'), Seq(compile_closure,
                               [Op, recur('Expr')],
                               atleast = 0, name = 'Expr (Op Expr)*')],
            name = 'BinOp'
            )

Expr = ast(compile_closure,
           [ast(compile_closure, 
                [recur("Closure")],
                [recur("BinOp")], 
                [recur("Atom")], 
                
                name = 'BinOp | Atom | Closure'),
                
            recur("Trailer")],
           name = 'Expr'
           )


               


Trailer= Seq(compile_closure,
            [LB, Seq(compile_closure,[Expr], atleast = 0, name = "(Expr)*"), RB],
            [LP, Seq(compile_closure,[Expr], atleast = 0, name = "(Expr)*"), RP],
            [ELiter('.', name = 'ACC'), Name],
            name = 'Trailer', atleast = 0)
             

Atom.compile
Closure.compile
BinOp.compile
BinOp.has_recur = True
Expr.compile
Expr.has_recur = True
Trailer.compile


          


