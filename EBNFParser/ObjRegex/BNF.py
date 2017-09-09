#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:13:34 2017

@author: misakawa
"""

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
           name = 'Atom')

Trailer = Seq()
Expr    = ast() 

Atom = Seq([LangLiter, 
           Trailer
           ],
           [Expr,
            Trailer
           ],
      name = 'Atom') 

Factor = ast()

redef(Factor,
      [Atom],
      [Op, Factor],
      name = 'Factor'
      )

#Factor = ast([Seq([Op],atleast = 0), 
#              Atom
#              ], 
#        name = 'Factor')

BinOp = ast([Factor, 
             Seq([Op, Factor], atleast = 0)
             ],
            name = 'BinOp')

Closure = ast()
redef(Closure,
      [ELiter('{'), 
       Seq([Atom,
              Seq([NEWLINE], atleast = 0)
              ],atleast = 0),
       ELiter('}')
        ],
       [ELiter('def(?![a-zA-Z_0-9])'),
        Seq([Name], atleast = 0),
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






