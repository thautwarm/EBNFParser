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
Atom = ast([LangLiter, 
           Trailer
           ],
      name = 'Atom') 

        
redef(Trailer, 
            [ELiter('['), Seq([Atom], atleast = 0), ELiter(']')],
            [ELiter('('), Seq([Atom], atleast = 0), ELiter(')')],
            [ELiter('.'), Name],
          name = 'Trailer')
