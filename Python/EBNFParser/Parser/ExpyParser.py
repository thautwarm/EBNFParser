#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 20:23:21 2017

@author: misakawa
"""

from ..ObjectRegex.Node import   Liter, ast, recur, Seq, ELiter,handle_error
L_Number = '\d+|\d*\.\d+'  

L_Name   = '[a-zA-Z_][a-zA-Z0-9]*'

L_String = '[a-z]{0,1}"[\w|\W]*?"'

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

Literal = ast(compile_closure,
           [Number],
           [String],
           [Liter('True(?![a-zA-Z_0-9])',name = 'True')],
           [Liter('False(?![a-zA-Z_0-9])',name = 'False')],
           [Liter('None(?![a-zA-Z_0-9])', name = 'None')],
           [Name],
           name = 'Literal')

Closure = ast(compile_closure,
              [LBB, 
               recur("Stmt"),
#               Seq(compile_closure,
#                   [recur('Expr'),
#                    Seq(compile_closure,
#                        [NEWLINE], 
#                        atleast = 0, name = '(NEWLINE)*')
#                    ],atleast = 0, name = '(Expr (NEWLINE)*)*'),
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



Atom = ast(compile_closure,
           [Seq(compile_closure,
                [recur('Closure')],
                [recur('Literal')],
                name = '(Closure | Literal)',
                atleast = 1,
                atmost  = 1
                ),
            recur('Trailer')
            ],
#           [recur("Closure"), recur("Trailer")],
#           [recur("Literal"), recur("Trailer")],
           name = 'Atom'
           )


Expr = ast(compile_closure,
           [recur('BinOp')],
           [recur('Factor')],
           [LP, recur("ExprList"), RP],
           [LB, recur("ExprList"), RP],
           name = 'Expr')
         
ExprList = ast(compile_closure,
               [Seq(compile_closure,
                    [recur('Expr')],
                    name    = "(Expr)*",
                    atleast = 0),
               Seq(compile_closure,
                    [ELiter(',')],
                    name    = "[,]",
                    atleast = 0,
                    atmost  = 1),
               ],
               name = 'ExprList'
               )

BinOp = ast(compile_closure,
            [recur('Factor'),
             Seq(compile_closure,
                [Op, 
                recur('Factor')],
                name = '(Op Factor)',
                atleast = 0),
             ],
             name = 'BinOp')
        
Factor = ast(compile_closure,
             [Seq(compile_closure,
                [Op],
                name = '(Op)*',
                atleast = 0),
             recur('Atom')
             ],
             name = 'Factor')

Stmt = ast(compile_closure,
           [Seq(compile_closure,
                  [Seq(compile_closure,
                       [NEWLINE],
                       name = 'LINESPLIT',
                       atleast = 0),
                   recur("Expr")
                   ],
                  name = 'AWAIT',
                  atleast = 0)
            ],
           name = 'Stmt')
                  
Trailer= Seq(compile_closure,
            [LB, Seq(compile_closure,[recur('Expr')], atleast = 0, name = "(Expr)*"), RB],
            [LP, Seq(compile_closure,[recur('Expr')], atleast = 0, name = "(Expr)*"), RP],
            [ELiter('.', name = 'ACC'), Name],
            name = 'Trailer', atleast = 0)


Literal.compile
Closure.compile
Expr.compile
Atom.compile
Trailer.compile
Stmt.compile
BinOp.compile
Factor.compile
ExprList.compile

Closure.has_recur = True
Expr.has_recur    = True
Atom.has_recur    = True
Stmt.has_recur    = True
BinOp.has_recur   = True
Factor.has_recur  = True
ExprList.has_recur= True

