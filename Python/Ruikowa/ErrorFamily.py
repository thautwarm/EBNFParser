#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 19:28:51 2017

@author: misakawa
"""

import warnings


class ObjectUsageError(Exception):
    pass


class CheckConditionError(Exception):
    pass


class UnsolvedError(Exception):
    pass


class DSLSyntaxError(SyntaxError):
    pass


def handle_error(parser):
    func = parser.match

    def _f(words, meta=None, partial=True):
        if not meta:
            raise CheckConditionError("Meta Information not defined yet!")
        res = func(words, meta=meta)
        if res is None:
            c = meta.count
            r = meta.rdx
            for ch in words[c:]:
                if ch is '\n':
                    r += 1
                    c += 1
                    continue
                break
            info = " ".join(words[c:c + 10])
            if len(words) > c + 10:
                info += '...'
            raise DSLSyntaxError('''
Syntax Error at {filename} row {r}
   Error startswith :
{info}
'''.format(r=r, info=info, filename=meta.fileName))
        else:
            if not partial and len(words) != meta.count:
                warnings.warn("Parsing unfinished.")
                c = meta.count
                r = meta.rdx
                for ch in words[c:]:
                    if ch is '\n':
                        r += 1
                        c += 1
                        continue
                    break
                info = " ".join(words[c:c + 10])
                if len(words) > c + 10:
                    info += '...'
                raise DSLSyntaxError('''
Syntax Error at row {r}
   Error startswith :
{info}
'''.format(r=r, info=info))
        return res

    return _f
