#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:40:09 2017

@author: misakawa
"""
from ..Config import Debug


def debug(msg, self=None):
    def wrap(func):
        def call(objs, meta, recur):
            tk = objs[meta.count]
            res = func(objs, meta, recur)
            if hasattr(self, 'mode'):
                print(msg, ':', f'{self.name}[{self.mode.encode()}]', 'matching', tk, 'return =>', res)
            else:
                print(msg, ':', f'{self.name}', 'matching', tk, 'return =>', res)
            return res

        return call

    return wrap


import re
from ..Core.BaseDef import Const, Trace
from .Tokenizer import Tokenizer, unique_literal_cache_pool


def match_by_name_enum(self):
    self.name = unique_literal_cache_pool[self.name]

    # @debug('name_enum', self=self)
    def match(objs, meta, recur=None):
        try:
            value: 'Tokenizer' = objs[meta.count]
        except IndexError:
            return Const.UnMatched
        if value.name is self.name:
            meta.new()
            return value
        return Const.UnMatched

    return debug('name_enum', self=self)(match) if Debug else match


def match_liter_by(self):
    self.mode = unique_literal_cache_pool[self.mode]

    # @debug('liter', self=self)
    def match(objs, meta, recur=None):
        try:
            value: 'Tokenizer' = objs[meta.count]
        except IndexError:
            return Const.UnMatched
        if value.string is self.mode:
            meta.new()
            return value
        return Const.UnMatched

    return debug('liter', self=self)(match) if Debug else match
