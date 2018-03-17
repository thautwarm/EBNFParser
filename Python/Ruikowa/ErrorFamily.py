#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:28:51 2017

@author: misakawa
"""
from pprint import pprint
from .color import Colored

if False:
    from .ObjectRegex.MetaInfo import MetaInfo
    from typing import Sequence, Optional
    from .ObjectRegex.Tokenizer import Tokenizer

import warnings


class ObjectUsageError(Exception):
    pass


class CheckConditionError(Exception):
    pass


class UnsolvedError(Exception):
    pass


class DSLSyntaxError(SyntaxError):
    pass


class UnsupportedStringPrefix(Exception):
    def __init__(self, mode):
        Exception.__init__(self,
                           Colored.LightBlue + "Unsupported string prefix " + Colored.Red + '{}'
                           .format(mode) + Colored.LightBlue + "." + Colored.Clear)
