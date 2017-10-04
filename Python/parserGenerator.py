#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:48:35 2017

@author: misakawa
"""

from Misakawa.Bootstrap.Compile import compile as bootstrap_comp
import argparse
import re

_regexCommentRemove   = re.compile('#[\w\W]*?\n')
regexCommentRemove    = lambda string : _regexCommentRemove.sub('', string)
regexMultiLineSupport = lambda string : string.replace('\n','').replace('ENDL','\n')

cmdparser = argparse.ArgumentParser(description='using EBNFParser.')
cmdparser.add_argument("InputFile",  metavar = 'in_filename', type = str,
                       help='EBNF file which defines your grammar.')
cmdparser.add_argument("OutputFile", metavar = 'out_filename', type= str,
                       help='generated python file(s) that makes a parser for your language.')
cmdparser.add_argument("-test", default = True, type=bool, help="generate testLang.py?")
cmdparser.add_argument("-comment", default = False, type=bool, help="generate testLang.py?")
cmdparser.add_argument("-multiline", default = False, type=bool, help="generate testLang.py?")

args = cmdparser.parse_args()
inp, outp, is_test = args.InputFile, args.OutputFile, args.test
if is_test:
	import sys, shutil, os
	head_from , _ = os.path.split(sys.argv[0])
	head_to   , _ = os.path.split(outp)
	shutil.copy(f"{head_from}/testLang.py", f"{head_to}/testLang.py")

def getRaw(inp):
    with open(inp, 'r', encoding='utf8') as file: 
        ret = file.read()
    return ret

def selectMode(mode):
    toDo = []
    if 'comment' in mode:
        toDo.append(regexCommentRemove)
    if 'multiline' in mode:
        toDo.append(regexMultiLineSupport)
    return toDo
def transform(raw, mode):
    for f in selectMode(mode):
        raw = f(raw)
    return raw

mode = []
if args.comment:
    mode.append('comment')
if args.multiline:
    mode.append('multiline')

with open(outp,'w', encoding='utf8') as file: file.write(bootstrap_comp(
        transform(getRaw(inp), mode)
        , 'Unnamed'))


