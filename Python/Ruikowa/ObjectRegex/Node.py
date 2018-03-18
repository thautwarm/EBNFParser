#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:53:53 2017

@author: misakawa
"""
from abc import ABC, abstractmethod
from ..Core.BaseDef import *
from .MetaInfo import MetaInfo
from ..ErrorFamily import *
from .PatternMatching import *
from .ASTDef import Ast
from .Optimize import optimize
from .Tokenizer import unique_lit_name


class Ignore:
    Value = 0
    Name = 1


class BaseParser(ABC):
    """Abstract Class"""
    name = Undef
    has_recur = Undef

    def match(self, objs, meta, recur=Undef):
        """Abstract Method"""
        raise Exception("There is no access to an abstract method.")
        # incomplete


class LiteralNameParser(BaseParser):
    """
    To parse tokenizer with specific name.
    for regex exp
    """

    def __init__(self, name):
        self.name = name
        self.match = match_by_name_enum(self)


class LiteralValueParser(BaseParser):
    """
    for const char*
    """

    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.match = match_liter_by(self)


LiteralParsers = (LiteralValueParser, LiteralNameParser)


class Ref(BaseParser):
    def __init__(self, name):
        self.name = unique_literal_cache_pool[name]


class AstParser(BaseParser):
    def __init__(self, *ebnf, name=Undef, to_ignore=Undef):
        # each in the cache will be processed into a parser.
        ebnf = tuple(
            tuple(
                LiteralValueParser(':const', each) if isinstance(each, str) else each for each in p)
            for p in ebnf)
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
        self.to_ignore = to_ignore

    def compile(self, namespace, recur_searcher):
        if self.name in recur_searcher:
            self.has_recur = True
            self.compiled = True
        else:
            recur_searcher.add(self.name)

        if self.compiled:
            return self

        for es in self.cache:
            self.possibilities.append([])

            for e in es:

                if e.__class__ in LiteralParsers:
                    self.possibilities[-1].append(e)
                    unique_lit_name(e)

                    if e.name not in namespace:
                        namespace[e.name] = e.name
                    else:
                        e = namespace[e.name]

                elif isinstance(e, Ref):
                    unique_lit_name(e)

                    e = namespace[e.name]

                    if isinstance(e, AstParser):
                        e.compile(namespace, recur_searcher)

                    self.possibilities[-1].append(e)

                    if not self.has_recur and e.has_recur:
                        self.has_recur = True

                else:
                    unique_lit_name(e)
                    if e.name not in namespace:
                        namespace[e.name] = e
                    else:
                        e = namespace[e.name]

                    e.compile(namespace, recur_searcher)
                    self.possibilities[-1].append(e)

                    if not self.has_recur and e.has_recur:
                        self.has_recur = True

        if hasattr(self, 'cache'):
            del self.cache

        if self.name in recur_searcher:
            recur_searcher.remove(self.name)

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
            result = self.pattern_match(objs, meta, possibility, recur=recur)
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

    def pattern_match(self, objs, meta, possibility, recur=Undef):

        try:  # Not recur
            result = Ast(meta.clone(), self.name)
            for parser in possibility:
                r = parser.match(objs, meta=meta, recur=recur)

                # if `result` is still empty, it might not allow LR now.
                if isinstance(r, Tokenizer) or isinstance(r, Ast):
                    result_merge(result, r, parser, self.to_ignore)

                elif r is Const.UnMatched:
                    return Const.UnMatched

                elif isinstance(r, RecursiveFound):
                    raise r

                else:
                    raise UnsolvedError("Unsolved return type. {}".format(r.__class__))
            else:
                return result

        except RecursiveFound as RecurInfo:
            RecurInfo.add((self, possibility[possibility.index(parser) + 1:]))

            # RecurInfo has a trace of Beginning Recur Node to Next Recur Node with
            # specific possibility.
            if RecurInfo.node is not self:
                return RecurInfo

            return left_recursion(objs, meta, possibility, RecurInfo)


def result_merge(result, r, parser, to_ignore):
    if parser.__class__ is SeqParser or parser.__class__ is AccompaniedAstParser:

        if to_ignore is Undef:
            result.extend(r)
        else:
            result.extend([item for item in r if
                           ((item.string not in to_ignore[Const.RawFilter]
                             and item.name not in to_ignore[Const.NameFilter])
                            if item.__class__ is Tokenizer else
                            (item.name not in to_ignore[Const.NameFilter]))])
    else:
        if to_ignore is Undef:
            result.append(r)
        else:
            if r.__class__ is Tokenizer:
                if r.string not in to_ignore[Const.RawFilter] and r.name not in to_ignore[Const.NameFilter]:
                    result.append(r)
            elif r.name not in to_ignore[Const.NameFilter]:
                result.append(r)


def left_recursion(objs, meta, recur_case, recur_info):
    recur = recur_info.node
    for case in recur.possibilities:
        if case is recur_case: continue
        meta.branch()
        very_first = recur.pattern_match(objs, meta, case, recur=recur)
        if isinstance(very_first, RecursiveFound) or very_first is Const.UnMatched:
            meta.rollback()
            continue
        else:
            meta.pull()
            first = very_first
            recur_depth_count = 0
            while True:
                meta.branch()
                for parser, possibility in recur_info.possibilities:
                    result = parser.pattern_match(objs, meta, possibility, recur=recur)
                    if result is Const.UnMatched:
                        meta.rollback()
                        return Const.UnMatched if recur_depth_count is 0 else very_first
                    elif isinstance(result, Ast):
                        result.appendleft(first)
                    elif isinstance(result, RecursiveFound):
                        raise UnsolvedError("Error occurs : found a new left recursion when handling an other.")
                    else:
                        raise UnsolvedError("Unsolved return from method `patternMatch`.")
                    first = result
                recur_depth_count += 1
                meta.pull()
                very_first = first
    else:
        # Fail to match any case.
        return Const.UnMatched


class AccompaniedAstParser(AstParser): pass


class SeqParser(AstParser):

    def __init__(self, *ebnf, name=Undef, at_least=0, at_most=Undef):
        super(SeqParser, self).__init__(*ebnf, name=name)

        if at_most is Undef:
            if at_least is 0:
                self.name = "({NAME})*".format(NAME=self.name)
            else:
                self.name = '({NAME}){{{AT_LEAST}}}'.format(NAME=self.name, AT_LEAST=at_least)
        else:
            self.name = "({NAME}){{{AT_LEAST},{AT_MOST}}}".format(
                NAME=self.name,
                AT_LEAST=at_least,
                AT_MOST=at_most)
        self.at_least = at_least
        self.at_most = at_most

    def match(self, objs, meta, recur=Undef):

        result = Ast(meta.clone(), self.name)

        if meta.count == len(objs):  # boundary cases
            if self.at_least is 0:
                return result
            return Const.UnMatched

        meta.branch()
        matched_num = 0
        if self.at_most is not Undef:
            """ (ast){a b} """
            while True:
                if matched_num >= self.at_most:
                    break
                try:
                    r = super(SeqParser, self).match(objs, meta=meta, recur=recur)
                except IndexError:
                    break

                if r is Const.UnMatched:
                    break
                elif isinstance(r, RecursiveFound):
                    raise UnsolvedError("Cannot make left recursions in SeqParser!!!")
                result.extend(r)
                matched_num += 1
        else:
            """ ast{a} | [ast] | ast* """
            while True:
                try:
                    r = super(SeqParser, self).match(objs, meta=meta, recur=recur)
                except IndexError:
                    break

                if r is Const.UnMatched:
                    break

                elif isinstance(r, RecursiveFound):
                    raise UnsolvedError("Cannot make left recursions in SeqParser!!!")

                result.extend(r)
                matched_num += 1

        if matched_num < self.at_least:
            meta.rollback()
            return Const.UnMatched

        meta.pull()
        return result
