#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 15:28:09 2017

@author: misakawa
"""



class ObjectUsageError(Exception):
    pass

class CheckConditionError(Exception):
    pass

class UnsolvedError(Exception):
    pass


class MetaInfo:
    
    """
    Meta information when parsing.

        `count` is a property of MetaInfo.
        It shows that how many tokenized(words) have been parsed,
            which could be used for
                - Alerting.
                - Eliminating left recursions.

        `trace` is a property of MetaInfo.
        It shows a trace of recursive BNF Nodes,
            which could be used for
                - Debugging.
                - Eliminating left recursions.

        `rdx` is a property of MetaInfo.
        It shows how many lines have beeb parsed now.
            which could be used for
                - Alerting.
                - Debugging.
                
        `fileName` is also a property of MetaInfo.
        It suggests which file the parser works on.  

    """

    def __init__(self, count=0, rdx=0, trace=None, fileName = None):
        """

        :rtype: MetaInfo
        """
        self.count   = count
        self.trace   = trace if trace else []
        self.rdx     = rdx
        self.history = []
        self.fileName= fileName if fileName else "<input>"

    def branch(self):
        """
        Save a record of parsing history in order to trace back. 
        """
        self.history.append((self.count, self.rdx, len(self.trace)))

    def rollback(self):
        """
        Trace back.
        """
        try:
            count, rdx, length =self.history.pop()
        except IndexError:
            return None
        self.count = count
        self.rdx = rdx
        self.trace = self.trace[:length]

    def pull(self):
        """
        Confirm the current parsing results.
        Pop a record in parsing history.
        """
        try:
            self.history.pop()
        except IndexError:
            raise Exception("pull no thing")
        
    def clone(self):
        """
        Get a copy of 
                    (RowIdx, 
                     NumberOfParsedWords, 
                     FileName) 
                    from current meta information.
        """
        return (self.rdx, self.count, self.fileName)
        





def handle_error(parser):
    func    = parser.match
    history = (0, parser.name)
    def _f(objs, meta = None, partial=True):
        if not meta:
            meta = MetaInfo()
            meta.trace.append(history)
        if meta.trace:
            return func(objs, meta=meta, partial=partial)

        res = func(objs, meta=meta, partial=partial)
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
            raise SyntaxError(f'''
Syntax Error at row {r}
   Error startswith :
{info}
''')
        return res
    return _f