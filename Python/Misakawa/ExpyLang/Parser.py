#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 20:20:59 2017

@author: misakawa
"""


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


LBB = LiteralParser.Eliteral('{', name = 'LBB')
LB  = LiteralParser.Eliteral('[', name = 'LB')
LP  = LiteralParser.Eliteral('(', name = 'LP')

RBB = LiteralParser.Eliteral('}', name = 'RBB')
RB  = LiteralParser.Eliteral(']', name = 'RB')
RP  = LiteralParser.Eliteral(')', name = 'RP')

Comma  = LiteralParser.Eliteral(',', 'Comma')
Access = LiteralParser.Eliteral('.', name = 'Access')
Def = LiteralParser('def(?![a-zA-Z_0-9])', name = 'Def')

namespace     = globals()
recurSearcher = set()


Literal = AstParser(
           [Number],
           [String],
           [LiteralParser('True(?![a-zA-Z_0-9])',name = 'True')],
           [LiteralParser('False(?![a-zA-Z_0-9])',name = 'False')],
           [LiteralParser('None(?![a-zA-Z_0-9])', name = 'None')],
           [Name],
           name = 'Literal')
Closure = AstParser(
              [LBB, Ref("Stmt"), RBB],
              [     Def, 
                    SeqParser([Name], atleast = 0), 
                    SeqParser([LP, SeqParser([Name], atleast = 0), RP], atleast = 0), 
                    Ref('Closure')],
              name = 'Closure')
Atom = AstParser(
           [SeqParser(
                   [Ref('Closure')],
                   [Ref('Literal')],

                   atleast = 1,
                   atmost  = 1),
            Ref('Trailer')],
           name = 'Atom')
           
Expr = AstParser(
           [Ref('BinOp')],
           [Ref('Factor')],
           [LP, Ref("ExprList"), RP],
           [LB, Ref("ExprList"), RB],
           name = 'Expr')

ExprList = AstParser([SeqParser([Ref('Expr'), SeqParser([Comma])])], name = 'ExprList')

BinOp = AstParser(
            [Ref('Factor'),
             SeqParser([Op, Ref('Factor')], atleast = 0)],
             name = 'BinOp')
            
Factor = AstParser([SeqParser([Op]),Ref('Atom')],name = 'Factor')           

Trailer= AstParser(
            [SeqParser(
                    [LB, SeqParser([Ref('Expr')]), RB],
                    [LP, SeqParser([Ref('Expr')]), RP],
                    [Access, Name])],
            name = 'Trailer')
            

Stmt = AstParser(
           [SeqParser(
                   [SeqParser([NEWLINE]),
                    SeqParser([Ref("Expr")]),
                    SeqParser([NEWLINE])])],
           name = 'Stmt')

Stmt.compile(namespace, recurSearcher)    

from ..GenericToken import token
              