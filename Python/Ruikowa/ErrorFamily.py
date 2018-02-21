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


def handle_error(parser):
    func    = parser.match
    history = (0, parser.name)
    def _f(objs, meta = None, partial=True):
        if not meta: raise CheckConditionError("Meta Information not defined yet!")
        res  = func(objs, meta=meta)
        if res is None:
            c = meta.count
            r = meta.rdx
            for ch in objs[c:]:
                if ch is '\n':
                    r += 1
                    c += 1
                    continue
                break
            info = " ".join(objs[c:c + 10])
            if len(objs) > c + 10:
                info += '...'
            raise SyntaxError('''
Syntax Error at {filename} row {r}
   Error startswith :
{info}
'''.format(r = r, info = info, filename=meta.fileName))
        else:
            if not partial and len(objs) != meta.count:
                warnings.warn("Parsing unfinished.")
                c = meta.count
                r = meta.rdx
                for ch in objs[c:]:
                    if ch is '\n':
                        r += 1
                        c += 1
                        continue
                    break
                info = " ".join(objs[c:c + 10])
                if len(objs) > c + 10:
                    info += '...'
                raise SyntaxError('''
Syntax Error at row {r}
   Error startswith :
{info}
'''.format(r=r, info=info))
        return res
    return _f