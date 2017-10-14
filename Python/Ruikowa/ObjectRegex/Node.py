#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:53:53 2017

@author: misakawa
"""
from ..Core.BaseDef import *
from .MetaInfo import MetaInfo
from ..ErrorFamily import *
from .PatternMatching import *

class Ast(list):
    pass

class BaseParser:
    """Abstract Class"""
    name       = Undef
    has_recur  = Undef
    def match(self, objs, meta, recursive):
        """Abstract Method"""
        raise Exception("There is no access to an abstract method.")
        # incomplete

class CharParser(BaseParser):
    """
    To parse the single character.
    """
    def __init__(self, mode:'char'):
        length = len(mode)
        assert length is 1 or (length is 2 and mode[0] == '\\')
        self.mode  = mode
        self.match = Match_Char_By(self)

class LiteralParser(BaseParser):
    """
    To parse the literal.
    """
    def __init__(self, mode:str,
                       name:str,
                       isRegex:bool = False,
                       ifIsRegexThenEscape:bool=True):
        self.name = name
        self.isRegex = isRegex
        if isRegex:
            self.mode  = Generate_RegexPatten_From(mode, escape=ifIsRegexThenEscape)
            self.match = Match_With_Regex_By(self)
        else:
            self.mode  = mode
            self.match = Match_Without_Regex_By(self)

    def RawFormDealer(rawStr, name):
        return LiteralParser(rawStr, name = name, isRegex = False)




















