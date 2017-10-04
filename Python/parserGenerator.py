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
cmdparser.add_argument("-test", default = True, type=bool, help="generate testLang.py?")

args = cmdparser.parse_args()
inp, outp, is_test = args.InputFile, args.OutputFile, args.test
if is_test:
	import sys, shutil, os
	head_from , _ = os.path.split(sys.argv[0])
	head_to   , _ = os.path.split(outp)
	shutil.copy(f"{head_from}/testLang.py", f"{head_to}/testLang.py")

with open(inp, 'r', encoding='utf8') as file: raw = file.read()
with open(outp,'w', encoding='utf8') as file: file.write(bootstrap_comp(raw, ''))


