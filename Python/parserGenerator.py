#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:48:35 2017

@author: misakawa
"""

from Misakawa.Bootstrap.Compile import compile as bootstrap_comp
import argparse

cmdparser = argparse.ArgumentParser(description='using EBNFParser.')
cmdparser.add_argument("InputFile",  metavar = 'in_filename', type = str,
                       help='EBNF file which defines your grammar.')
cmdparser.add_argument("OutputFile", metavar = 'out_filename', type= str,
                       help='generated python file(s) that makes a parser for your language.')

args = cmdparser.parse_args()
inp, outp = args.InputFile, args.OutputFile

with open(inp, 'r', encoding='utf8') as file: raw = file.read()
with open(outp,'w', encoding='utf8') as file: file.write(bootstrap_comp(raw, ''))


