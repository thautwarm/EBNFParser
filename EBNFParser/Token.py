#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 21:45:58 2017

@author: misakawa
"""

import re

Number = '\d+|\d*\.\d+'  

Name   = '[a-zA-Z_][a-zA-Z0-9]*'

String = '[a-z]{0,1}"[\w|\W]*"'

Bracket= '\{|\}|\(|\)|\[|\]'

Access = '\.'

END    = ';'

NEWLINE= '\n'

Comment = '#[\w|\W]*?\n'

Op = '|'.join(['//', 
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

def gen_token_group(*group):
    return re.compile('|'.join(map(lambda item: f'{item}', group)))

token = gen_token_group(Number, 
                        Name,
                        String,
                        Bracket,
                        Access,
                        END,
                        NEWLINE,
                        Op,
                        Comment
                        )

Factor = {
        0:Number,
        1:Name,
        2:String,
        3:Bracket,
        4:Access,
        5:END,
        6:NEWLINE,
        7:Op
        }

Expr = [0,1,2, (1, 4, 1), ()]





    
