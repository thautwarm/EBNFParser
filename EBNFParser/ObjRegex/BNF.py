#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:34:03 2017

@author: misakawa
"""

from .Node import   Liter, ast, mode, redef, recur, Seq, ELiter
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



         
            
# Error File
# 左递归未解决。

Atom   = ast(    
           [Number],
           [String],
           [Liter('True(?![a-zA-Z_0-9])',name = 'True')],
           [Liter('False(?![a-zA-Z_0-9])',name = 'False')],
           [Liter('None(?![a-zA-Z_0-9])', name = 'None')],
           [Name],
           name = 'Atom')

Expr    = ast()
Closure = ast()
BinOp   = ast()
Factor  = ast()
Trailer = Seq()
Tpdef   = Seq([Name], atleast = 0, name = 'Tpdef')

redef(Expr,
      [ast([Atom],[Closure],[BinOp]), Trailer],
       name = 'Expr'
      )

redef(Closure,
      [ELiter('{'), 
       Seq([Expr,
            Seq([NEWLINE], atleast = 0)
            ],atleast = 0),
       ELiter('}')
       ],
       [Liter('def(?![a-zA-Z_0-9])'),  # lambda 
       ELiter('('),
       Seq([Name], atleast = 0),
       ELiter(')'),
       Closure
       ]        
       ,
       [Liter('def(?![a-zA-Z_0-9])'), # function with Name definition.
        Name,
        ELiter('('),
        Seq([Name], atleast = 0),
        ELiter(')'),
        Closure
        ],
        name = 'Closure'
      )

redef(BinOp,
      [Expr, Seq([Op, Expr], atleast = 0)],
      name = "BinOp"
      )

redef(Factor,
      [Op, Expr],
      [Expr],
      name = "Factor"
      )

redef(Trailer, 
            [ELiter('['), Seq([Expr], atleast = 0), ELiter(']')],
            [ELiter('('), Seq([Expr], atleast = 0), ELiter(')')],
            [ELiter('.'), Name],
          name = 'Trailer', atleast = 0)
