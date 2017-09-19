#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 20:20:59 2017

@author: misakawa
"""

bootstrap = False
from ..ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser
lit = LiteralParser

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

Name   = LiteralParser(L_Name, 'Name')
String = LiteralParser(L_String,'String')
Number = LiteralParser(L_Number,'Number')
Bracket= LiteralParser(L_Bracket,'Bracket')
NEWLINE= LiteralParser(L_NEWLINE,'NEWLINE')
END    = LiteralParser(L_END,'END')
Comment= LiteralParser(L_Comment,'Comment')
Op     = LiteralParser(L_Op,'Op')


LBB = LiteralParser.ELiter('{', name = 'LBB')
LB  = LiteralParser.ELiter('[', name = 'LB')
LP  = LiteralParser.ELiter('(', name = 'LP')

RBB = LiteralParser.ELiter('}', name = 'RBB')
RB  = LiteralParser.ELiter(']', name = 'RB')
RP  = LiteralParser.ELiter(')', name = 'RP')
Def = LiteralParser('def(?![a-zA-Z_0-9])', name = 'Def')




Literal = AstParser(
           [Number],
           [String],
           [LiteralParser('True(?![a-zA-Z_0-9])',name = 'True')],
           [LiteralParser('False(?![a-zA-Z_0-9])',name = 'False')],
           [LiteralParser('None(?![a-zA-Z_0-9])', name = 'None')],
           [Name],
           name = 'Literal')
