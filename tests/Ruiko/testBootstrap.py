#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 20:07:44 2017

@author: misakawa
"""

from Ruikowa.Bootstrap.Parser import *
from Ruikowa.ObjectRegex.MetaInfo import *
words = token.findall("a Throw [d e f] ::=b c d")
meta = MetaInfo()
Equals.match(words, meta)
