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

use_py_error = False
use_py_warnings = False

import warnings


class ObjectUsageError(Exception):
    pass


class CheckConditionError(Exception):
    pass


class UnsolvedError(Exception):
    pass


class DSLSyntaxError(SyntaxError):
    pass


if use_py_warnings:
    Warnings = warnings
else:
    class Warnings:
        @classmethod
        def warn(cls, *msg):
            print(Colored.LightBlue, 'UserWarning:', *msg)

if use_py_error:
    class Error:
        def __init__(self, *args):
            print(Colored.Purple, '{}: '.format(self.__class__.__name__), *args)
            raise Exception(self.__class__.__name__)
else:
    Error = Exception


class UnsupportedStringPrefix(Error):
    def __init__(self, mode, msg=''):
        Error.__init__(self,
                       '\n' + msg + '\n' +
                       Colored.LightBlue + "Unsupported string prefix " + Colored.Red + '{}'
                       .format(mode) + Colored.LightBlue + "." + Colored.Clear)


def find_location(filename, where: 'Tokenizer', src_code: str = None):
    if src_code:
        row = src_code.splitlines()[where.lineno]
    else:
        row = ''

    return "{}{}{}{} ---- at file {} line {}".format(Colored.Green, row[:where.colno], Colored.Red, row[where.colno:],
                                                     filename, where.lineno + 1) + Colored.Clear


class UniqueNameConstraintError(Error):
    def __init__(self, name, msg=''):
        Error.__init__(self,
                       '\n' + msg + '\n' +
                       Colored.Blue + "Name " + Colored.Red + '{}'
                       .format(name) + Colored.Blue + "should be unique." + Colored.Clear)
