#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:40:09 2017

@author: misakawa
"""

import re
from ..Core.BaseDef import Const, Trace
from .Tokenizer import Tokenizer, unique_literal_cache_pool


def match_by_name_enum(self):
    self.name = unique_literal_cache_pool[self.name]

    def match(objs, meta, recur=None):
        try:
            value: 'Tokenizer' = objs[meta.count]
        except IndexError:
            return Const.UnMatched
        if value.name is self.name:
            meta.new()
            return value
        return Const.UnMatched

    return match


def match_liter_by(self):
    self.mode = unique_literal_cache_pool[self.mode]

    def match(objs, meta, recur=None):
        try:
            value: 'Tokenizer' = objs[meta.count]
        except IndexError:
            return Const.UnMatched
        if value.string is self.mode:
            meta.new()
            return value
        return Const.UnMatched

    return match
