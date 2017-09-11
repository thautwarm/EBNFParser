#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:13:34 2017

@author: misakawa
"""

# Error File

Regex = 1
from .Node import Name,  Number, String,\
                 Bracket,NEWLINE,END,Comment,Op,\
                 Liter, ast, mode, redef, recur, Seq, ELiter
                 
                 

LangLiter = ast(
           
           [Number],
           [String],
           [Liter('True(?![a-zA-Z_0-9])',name = 'True')],
           [Liter('False(?![a-zA-Z_0-9])',name = 'False')],
           [Liter('None(?![a-zA-Z_0-9])', name = 'None')],
           [Name],
           name = 'Liter')

Trailer = Seq()
Expr    = ast() 

Atom = Seq()


# factor
Factor = ast()
redef(Factor,
      [Atom],
      [Op, Factor],
      name = 'Factor'
      )

BinOp = ast([Factor, 
             Seq([Op, Factor], atleast = 0)
             ],
            name = 'BinOp')

Closure = ast()
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
       
redef(Expr,
      [Closure],
      [BinOp],
      name = 'Expr'
      )

redef(Trailer, 
            [ELiter('['), Seq([Atom], atleast = 0), ELiter(']')],
            [ELiter('('), Seq([Atom], atleast = 0), ELiter(')')],
            [ELiter('.'), Name],
          name = 'Trailer', atleast = 0)


AtomExpr = ast([LangLiter, Trailer], name = 'AtomExpr')
redef(Atom,
      [AtomExpr],
      [LangLiter],
      [Closure],
      [BinOp],
      
#      [Expr],
#      [ELiter('('), Expr, ELiter(')')],
      name = 'Atom'
      )

AST = ast(
        [Expr],
        [Atom],
        name = 'AST'
        )






