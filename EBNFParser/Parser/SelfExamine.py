#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 12:16:26 2017

@author: misakawa
"""

from ..ObjectRegex.Node import   Liter, ast, recur, Seq, ELiter,handle_error

Name   = Liter('[a-zA-Z_][a-zA-Z0-9]*', name = 'NAME')

String = Liter("'[\w|\W]*'", name = 'String')


LBB = ELiter('{', name = 'LBB')
LB  = ELiter('[', name = 'LB')
LP  = ELiter('(', name = 'LP')

RBB = ELiter('}', name = 'RBB')
RB  = ELiter(']', name = 'RB')
RP  = ELiter(')', name = 'RP')