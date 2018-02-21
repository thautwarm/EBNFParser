#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:54:45 2017

@author: misakawa
"""
from ..Core.BaseDef import *



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

    def __init__(self, count=0, rdx=0, trace=None, fileName=None):

        self.count = count
        if trace:
            self.trace = trace
        else:
            self.trace = Trace()
            self.trace.append(Trace())
        self.rdx   = rdx
        self.history  = []
        self.fileName = fileName if fileName else "<input>"

    def new(self):
        self.count += 1
        self.trace.new(Trace)

    def branch(self):
        """
        Save a record of parsing history in order to trace back.
        """
        self.history.append((self.count, self.rdx, self.trace[self.count].length))

    def rollback(self):
        """
        Trace back.
        """
        try:
            count, rdx, length = self.history.pop()
        except IndexError:
            return None
        self.count = count
        self.rdx   = rdx
        self.trace.length = count+1
        self.trace[count].length = length


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

    def __str__(self):
        return """
--------------------
COUNT   : {COUNT}
ROW_IDX : {ROW_DIX}
TRACE   :
{TRACE}
--------------------
""".format(COUNT = self.count,
           ROW_DIX = self.rdx,
           TRACE   = '\n'.join(
               ['['+(','.join([item.name for item in unit ]))+']'for unit in self.trace])
           )



"""
use list as trace
"""
# class MetaInfo:
#     def __init__(self, count=0, rdx=0, trace=None, fileName=None):
#
#         self.count = count
#         if trace:
#             self.trace = trace
#         else:
#             self.trace = [[]]
#         self.rdx   = rdx
#         self.history  = []
#         self.fileName = fileName if fileName else "<input>"
#
#     def branch(self):
#         """
#         Save a record of parsing history in order to trace back.
#         """
#         self.history.append((self.count, self.rdx, len(self.trace[self.count]) ))
#     def rollback(self):
#         """
#         Trace back.
#         """
#
#         try:
#             count, rdx, length = self.history.pop()
#         except IndexError:
#             return None
#
#         self.count = count
#         self.rdx   = rdx
#         self.trace[count] = self.trace[count][:length]
#
#     def pull(self):
#         """
#         Confirm the current parsing results.
#         Pop a record in parsing history.
#         """
#         try:
#             self.history.pop()
#         except IndexError:
#             raise Exception("pull no thing")
#
#     def new(self):
#         self.count += 1
#         self.trace.append([])
#
#     def clone(self):
#         """
#         Get a copy of
#                     (RowIdx,
#                      NumberOfParsedWords,
#                      FileName)
#                     from current meta information.
#         """
#         return (self.rdx, self.count, self.fileName)
#
#         def __str__(self):
#             return """
#     --------------------
#     COUNT   : {COUNT}
#     ROW_IDX : {ROW_DIX}
#     TRACE   :
#     {TRACE}
#     --------------------
#     """.format(COUNT=self.count,
#                ROW_DIX=self.rdx,
#                TRACE='\n'.join(
#                    ['[' + (','.join([item.name for item in unit])) + ']' for unit in self.trace])
#                )