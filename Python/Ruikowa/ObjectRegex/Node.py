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
from .ASTDef import Ast
from .Optimize import optimize

class Ignore:
    Value = 0
    Name  = 1

class BaseParser:
    """Abstract Class"""
    name       = Undef
    has_recur  = Undef
    def match(self, objs, meta, recur=Undef):
        """Abstract Method"""
        raise Exception("There is no access to an abstract method.")
        # incomplete

class CharParser(BaseParser):
    """
    To parse the single character.
    """
    def __init__(self, mode, name = Undef):
        length = len(mode)
        assert length is 1
        self.mode  = mode
        self.name  = "'{MODE}'".format(MODE=mode) if name is Undef else name
        self.match = Match_Char_By(self)

class LiteralParser(BaseParser):
    """
    To parse the literal.
    """
    def __init__(self, mode,
                       name = Undef,
                       isRegex = False,
                       ifIsRegexThenEscape = False):
        self.name = name if name is not Undef else "'{MODE}'".format(MODE=mode)
        self.isRegex = isRegex

        if isRegex:
            self.mode  = Generate_RegexPatten_From(mode, escape=ifIsRegexThenEscape)
            self.match = Match_With_Regex_By(self)
        else:
            self.mode  = mode
            self.match = Match_Without_Regex_By(self)

class Ref(BaseParser):
    def __init__(self,name):self.name = name


class AstParser(BaseParser):
    def __init__(self, *ebnf, name=Undef, toIgnore = Undef):
        # each in the cache will be processed into a parser.
        self.cache = optimize(ebnf)

        # the possible output types for an series of input tokenized words.
        self.possibilities = []

        # whether this parser will refer to itself.
        self.has_recur = False

        # the identity of a parser.

        self.name = name if name is not Undef else \
            ' | '.join(' '.join(map(lambda parser: parser.name, ebnf_i)) for ebnf_i in ebnf)

        # is this parser compiled, must be False when initializing.
        self.compiled = False

        #  if a parser's name is in this set, the result it output will be ignored when parsing.
        self.toIgnore = toIgnore


    def compile(self, namespace, recurSearcher):
        if self.name in recurSearcher:
            self.has_recur = True
            self.compiled  = True
        else:
            recurSearcher.add(self.name)

        if self.compiled:
            return self

        for es in self.cache:
            self.possibilities.append([])

            for e in es:

                if isinstance(e, LiteralParser) or \
                        isinstance(e, CharParser):
                    self.possibilities[-1].append(e)

                elif isinstance(e, Ref):

                    e = namespace[e.name]

                    if isinstance(e, AstParser):
                        e.compile(namespace, recurSearcher)

                    self.possibilities[-1].append(e)

                    if not self.has_recur and e.has_recur:
                        self.has_recur = True

                elif isinstance(e, AstParser):

                    if e.name not in namespace:
                        namespace[e.name] = e
                    else:
                        e = namespace[e.name]

                    e.compile(namespace, recurSearcher)
                    self.possibilities[-1].append(e)

                    if not self.has_recur and e.has_recur:
                        self.has_recur = True

                else:
                    print(e)
                    raise UnsolvedError("Unknown Parser Type.")

        if hasattr(self, 'cache'):
            del self.cache

        if self.name in recurSearcher:
            recurSearcher.remove(self.name)

        if not self.compiled:
            self.compiled = True

    def match(self, objs, meta, recur=Undef):

        if self.has_recur and self in meta.trace[meta.count]:
            if isinstance(self, SeqParser) or recur is self:
                return Const.UnMatched

            raise RecursiveFound(self)

        meta.branch()

        if self.has_recur:
            meta.trace[meta.count].append(self)

        for possibility in self.possibilities:
            meta.branch()
            result = self.patternMatch(objs, meta, possibility, recur = recur)
            if result is Const.UnMatched:
                meta.rollback()
                continue
            elif isinstance(result, Ast):
                meta.pull()
                break
            elif isinstance(result, RecursiveFound):
                meta.rollback()
                break

        meta.pull()
        return result

    def patternMatch(self, objs, meta, possibility, recur=Undef):

        try: # Not recur
            result = Ast(meta.clone(), self.name)
            for parser in possibility:
                r = parser.match(objs, meta=meta, recur=recur)

                # if `result` is still empty, it might not allow LR now.
                if isinstance(r, str) or isinstance(r, Ast):
                    resultMerge(result, r, parser, self.toIgnore)

                elif r is Const.UnMatched:
                    return Const.UnMatched

                elif isinstance(r, RecursiveFound):
                    raise r

                else:
                    raise UnsolvedError("Unsolved return type. {}".format(r.__class__))
            else:
                return result

        except RecursiveFound as RecurInfo:
            RecurInfo.add((self, possibility[possibility.index(parser)+1:]))

            # RecurInfo has a trace of Beginning Recur Node to Next Recur Node with
            # specific possibility.
            if RecurInfo.node is not self:
                return RecurInfo

            return leftRecursion(objs, meta, possibility, RecurInfo)

def resultMerge(result, r, parser, toIgnore):

    if isinstance(parser, SeqParser) or isinstance(parser, DependentAstParser):

        if toIgnore is Undef:
            result.extend(r)
        else:
            result.extend([item for item in r if
                           ((item not in toIgnore[Const.RawFilter])
                            if isinstance(item, str) else
                            (item.name not in toIgnore[Const.NameFilter]))])
    else:
        if toIgnore is Undef:
            result.append(r)
        else:
            if isinstance(r, str):
                if r not in toIgnore[Const.RawFilter]:
                    result.append(r)
            elif r.name not in toIgnore[Const.NameFilter]:
                result.append(r)

def leftRecursion(objs, meta, RecurCase, RecurInfo):

    recur = RecurInfo.node
    for case in recur.possibilities:
        if case is RecurCase: continue
        meta.branch()
        veryFirst = recur.patternMatch(objs, meta, case, recur=recur)
        if isinstance(veryFirst, RecursiveFound) or veryFirst is Const.UnMatched:
            meta.rollback()
            continue
        else:
            meta.pull()
            first = veryFirst
            recurDeepCount = 0
            while True:
                meta.branch()
                for parser, possibility in RecurInfo.possibilities:

                    result = parser.patternMatch(objs, meta, possibility, recur=recur)
                    if result is Const.UnMatched:
                        meta.rollback()
                        return Const.UnMatched if recurDeepCount is 0 else veryFirst
                    elif isinstance(result, Ast):
                        result.appendleft(first)
                    elif isinstance(result, RecursiveFound):
                        raise UnsolvedError("Error occurs : found a new left recursion when handling an other.")
                    else:
                        raise UnsolvedError("Unsolved return from method `patternMatch`.")
                    first = result
                recurDeepCount += 1
                meta.pull()
                veryFirst = first
    else:
        # Fail to match any case.
        return Const.UnMatched

class DependentAstParser(AstParser):pass

class SeqParser(AstParser):

    def __init__(self, *ebnf, name=Undef, atleast=0, atmost=Undef):
        super(SeqParser, self).__init__(*ebnf, name=name)

        if atmost is Undef:
            if atleast is 0:
                self.name = "({NAME})*".format(NAME=self.name)
            else:
                self.name = '({NAME}){{{AT_LEAST}}}'.format(NAME=self.name, AT_LEAST=atleast)
        else:
            self.name = "({NAME}){{{AT_LEAST},{AT_MOST}}}".format(
                NAME=self.name,
                AT_LEAST=atleast,
                AT_MOST=atmost)
        self.atleast = atleast
        self.atmost  = atmost

    def match(self, objs, meta, recur = Undef):

        result = Ast(meta.clone(), self.name)

        if meta.count == len(objs):  # boundary cases
            if self.atleast is 0:
                return result
            return Const.UnMatched

        meta.branch()
        matchedNum = 0
        if self.atmost is not Undef:
            """ (ast){a b} """
            while True:
                if matchedNum >= self.atmost:
                    break
                try:
                    r = super(SeqParser, self).match(objs, meta=meta, recur = recur)
                except IndexError:
                    break

                if r is Const.UnMatched:
                    break
                elif isinstance(r, RecursiveFound):
                    raise UnsolvedError("Cannot make left recursions in SeqParser!!!")
                result.extend(r)
                matchedNum += 1
        else:
            """ ast{a} | [ast] | ast* """
            while True:
                try:
                    r = super(SeqParser, self).match(objs, meta=meta, recur = recur)
                except IndexError:
                    break

                if r is Const.UnMatched:
                    break

                elif isinstance(r, RecursiveFound):
                    raise UnsolvedError("Cannot make left recursions in SeqParser!!!")

                result.extend(r)
                matchedNum += 1

        if matchedNum < self.atleast:
            meta.rollback()
            return Const.UnMatched


        meta.pull()
        return result



# class DEBUG:
#     b = True
#
#     @staticmethod
#     def ShowHead(objs,meta):
#         print(list(objs[meta.count:3+meta.count]))
#
#
#     @staticmethod
#     def AstParserEnter(self, meta):
#         if not DEBUG.b : return
#         print('==============')
#         print(f'Name      :{self.name}')
#         print(f'Meta Count:{meta.count}')
#         print(f'Meta Trace: {[i.name for i in meta.trace[meta.count]]}')
#
#     @staticmethod
#     def FoundRecur(self):
#         if not DEBUG.b: return
#         print(f"Found Recur at{self.name}")
#
#     @staticmethod
#     def PassRecur(parser, self):
#         if not DEBUG.b: return
#         print(f'Pass RecurInfo from {parser.name} to {self.name}')
#
#     @staticmethod
#     def LogResult(self, res):
#         if not DEBUG.b: return
#         print(f"{self.name} <= \n {res} \n ")


# def debugger(Begin='', End = '', Check = lambda x:Undef):
#     def funcHook(matcher):
#         def innerHook(*args, **kwargs):
#             locals()['args'] = args
#             locals().update(kwargs)
#             exec(Begin, locals())
#             ret = matcher(*args, **kwargs)
#             checked = Check(ret)
#             if checked is Undef : pass
#             else:
#                 print(checked)
#             exec(End, locals())
#             return ret
#         return innerHook
#     return funcHook








