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
Atom = ast(
           
           [Number],
           [String],
           [Liter('True(?![a-zA-Z_0-9])')],
           [Liter('False(?![a-zA-Z_0-9])')],
           [Liter('None(?![a-zA-Z_0-9])')],
           [Name],
           
           name = 'Atom')

Access  = Seq(
        [Atom, ELiter('.'),Atom],
        name = 'Access'
        )
Trailer = Seq(
            [ELiter('['), Seq([Atom]), ELiter(']')],
            [ELiter('('), Seq([Atom]), ELiter(')')],
            [ELiter('.'), Access],
            
        
          name = 'Trailer')