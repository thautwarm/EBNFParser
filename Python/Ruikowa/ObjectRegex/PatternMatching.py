#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:40:09 2017

@author: misakawa
"""

import re
from .MetaInfo import MetaInfo
from ..Core.BaseDef import Const, Trace
from typing import List, TypeVar






def Generate_RegexPatten_From(mode:str, escape:bool=False)->re._pattern_type:
    return re.compile(re.escape(mode)) if escape else re.compile(mode)




# The Reason why to repeat myself at the following three functions.
#    `Match_Char_By` `Match_Without_Regex_By`, `Match_With_Regex_By`
"""
    This pattern is the key to speed up the parser framework.
    For sure, I can abstract the way how the input string compares 
    with the parser's memeber `mode`, and then, these codes
        `if value == self.mode`
        `self.mode.fullmatch(value)`
    can be unified to 
        `if someFunc(value, mode)` or `if someFunc(value, self)`
    
    However, abstraction can have costly results.
    
"""

def Match_Char_By(self):
    self: LiteralParser
    def match(objs:List[str], meta:MetaInfo, allowLR:bool = None):
        value = objs[meta.count]
        if value is self.mode:
            if value is '\n':
                meta.rdx   += 1
            meta.count += 1
            meta.trace.push(Trace())
            return value
        return Const.UnMatched
    return match

def Match_Without_Regex_By(self):
    self: LiteralParser
    def match(objs:List[str], meta:MetaInfo, allowLR:bool = None):
        value = objs[meta.count]
        if value == self.mode:
            if value is '\n':
                meta.rdx   += 1
            meta.count += 1
            meta.trace.push(Trace())
            return value
        return Const.UnMatched
    return match

def Match_With_Regex_By(self):
    self: LiteralParser
    def match(objs:List[str], meta:MetaInfo, allowLR:bool = None):
        value = objs[meta.count]
        if self.mode.fullmatch(value):
            if value is '\n':
                meta.rdx += 1
            meta.count += 1
            meta.trace.push(Trace())
            return value
        return Const.UnMatched
    return match










