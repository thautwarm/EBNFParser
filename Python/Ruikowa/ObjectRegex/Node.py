#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:53:53 2017

@author: misakawa
"""
from abc import ABC, abstractmethod
from typing import Union, List, Tuple, Collection
from ..Core.BaseDef import *
from .MetaInfo import MetaInfo
from ..ErrorFamily import *
from .ASTDef import Ast
from .Optimize import optimize
from .Tokenizer import unique_lit_name, unique_lit_value, unique_literal_cache_pool, Tokenizer
from ..Config import Debug

if Debug:
    from ..Tools import function_debugger

    DEBUG_INDENT = 1
    debugger = function_debugger('tag', 'content')


class Ignore:
    Value = 0
    Name = 1


def debug(msg):
    def wrap(func):
        def call(self, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', *args, **kwargs):
            global DEBUG_INDENT
            if not isinstance(self, AstParser):
                now = tokens[meta.count]
                if hasattr(self, 'mode'):
                    profile = f'{self.name}[{self.mode}] matching {now}'
                else:
                    profile = f'{self.name} matching {now}'
            else:
                profile = self.name
            print(Colored.Purple2,
                  debugger(dict(
                      tag=f'start {self.__class__.__name__}',
                      Profile=profile,
                      Name=self.name,
                      content=msg,
                      Meta=meta.count),
                      indent=DEBUG_INDENT * 4,
                      inc_indent=2),
                  Colored.Clear, '\n')

            DEBUG_INDENT += 1
            res = func(self, tokens, meta, *args, **kwargs)
            DEBUG_INDENT -= 1

            print(Colored.LightBlue,
                  debugger(
                      dict(
                          tag=f'end {self.__class__.__name__}',
                          Name=self.name,
                          Profile=profile,
                          content=msg,
                          Return=True if res else False,
                          Meta=meta.count),
                      indent=DEBUG_INDENT * 4,
                      inc_indent=1),
                  Colored.Clear, '\n')

            return res

        return call if Debug else func

    return wrap


ParserCollections = 'Union[LiteralNameParser, LiteralNameValueParser, LiteralValueParser, AstParser, SeqParser]'


def parser_name_helper(
        pattern: 'ParserCollections'):
    if pattern.__class__ is LiteralNameValueParser:
        return f"{pattern.name}['{pattern.mode}']"
    elif pattern.__class__ is LiteralValueParser:
        return f"'{pattern.mode}'"
    else:
        return pattern.name


class BaseParser(ABC):
    """Abstract Class"""
    name = Undef
    has_recur = Undef

    @abstractmethod
    def match(self, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', recur: 'Recur' = Undef):
        """Abstract Method"""
        raise NotImplemented


class LiteralNameParser(BaseParser):
    """
    To parse tokenizer with specific name.
    for regex exp
    """

    def __init__(self, name):
        self.name = name

    def match(self, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', recur: 'Recur' = Undef):
        try:
            value: 'Tokenizer' = tokens[meta.count]
        except IndexError:
            return Const.UnMatched
        if value.name is self.name:
            meta.new()
            return value
        return Const.UnMatched


class LiteralValueParser(BaseParser):
    """
    for const char*
    """

    def __init__(self, mode):
        self.name = self.mode = mode

    def match(self, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', recur: 'Recur' = Undef):
        try:
            value: 'Tokenizer' = tokens[meta.count]
        except IndexError:
            return Const.UnMatched
        if value.string is self.mode:
            meta.new()
            return value
        return Const.UnMatched


class LiteralNameValueParser(BaseParser):
    """
    for const char* and its group name
    """

    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

    @debug('literal name value')
    def match(self, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', recur: 'Recur' = Undef):
        try:
            value: 'Tokenizer' = tokens[meta.count]
        except IndexError:
            return Const.UnMatched
        if value.name is self.name and value.string is self.mode:
            meta.new()
            return value
        return Const.UnMatched


class Ref(BaseParser):
    def __init__(self, name):
        self.name = unique_literal_cache_pool[name]

    def match(self, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', recur: 'Recur' = Undef):
        raise NotImplemented


class AstParser(BaseParser):

    def __init__(self, *cases, name=Undef, to_ignore=Undef):
        # each in the cache will be processed into a parser.
        cases = tuple(
            tuple(
                LiteralValueParser(each) if isinstance(each, str) else
                LiteralNameValueParser(each[0], each[1]) if isinstance(each, tuple) else
                each
                for each in p)
            for p in cases)
        self.cache: 'Tuple[Tuple[ParserCollections]]' = optimize(cases)

        # the possible output types for an series of input tokenized words.
        self.possibilities = []

        # whether this parser will refer to itself.
        self.has_recur = False

        # the identity of a parser.

        self.name = name if name is not Undef else \
            ' | '.join(
                ' '.join(
                    map(parser_name_helper, case)) for case in cases)

        # is this parser compiled, must be False when initializing.
        self.compiled = False

        #  if a parser's name is in this set, the result it output will be ignored when parsing.
        self.to_ignore = to_ignore

    def compile(self, namespace: dict, recur_searcher: set):
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

                if e.__class__ is LiteralNameParser:

                    if e.name not in namespace:
                        unique_lit_name(e)
                        namespace[e.name] = e

                    else:
                        e = namespace[e.name]

                    self.possibilities[-1].append(e)

                elif e.__class__ is LiteralValueParser:
                    literal = parser_name_helper(e)

                    if literal not in namespace:
                        unique_lit_value(e)
                        namespace[literal] = e

                    else:
                        e = namespace[literal]

                    self.possibilities[-1].append(e)

                elif e.__class__ is LiteralNameValueParser:
                    name_literal = parser_name_helper(e)

                    if name_literal not in namespace:
                        unique_lit_value(e)
                        unique_lit_name(e)
                        namespace[name_literal] = e
                    else:
                        e = namespace[name_literal]

                    self.possibilities[-1].append(e)

                elif e.__class__ is Ref:
                    e = namespace[e.name]

                    if isinstance(e, AstParser):
                        e.compile(namespace, recur_searcher)

                    self.possibilities[-1].append(e)

                    if not self.has_recur and e.has_recur:
                        self.has_recur = True

                else:
                    if e.name not in namespace:
                        unique_lit_name(e)
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

    @debug("match")
    def match(self, tokens, meta: 'MetaInfo', recur: 'Recur' = Undef):
        if self.has_recur and self in meta.trace[meta.count]:
            if isinstance(self, SeqParser) or recur is self:
                return Const.UnMatched

            raise RecursiveFound(self)
        history = meta.commit()
        if self.has_recur:
            meta.trace[meta.count].append(self)

        for possibility in self.possibilities:
            result = self.pattern_match(tokens, meta, possibility, recur=recur)
            if result is Const.UnMatched:
                meta.rollback(history)
                continue
            elif isinstance(result, Ast):
                break
            elif isinstance(result, RecursiveFound):
                meta.rollback(history)
                break
        else:
            return Const.UnMatched

        return result

    def pattern_match(self, tokens, meta, possibility, recur=Undef):

        try:  # Not recur
            result = Ast(meta.clone(), self.name)
            for parser in possibility:
                r = parser.match(tokens, meta=meta, recur=recur)
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
            parser: 'ParserCollections'
            RecurInfo.add((self, possibility[possibility.index(parser) + 1:]))

            # RecurInfo has a trace of Beginning Recur Node to Next Recur Node with
            # specific possibility.
            if RecurInfo.node is not self:
                return RecurInfo

            return left_recursion(tokens, meta, possibility, RecurInfo)


def result_merge(result, r, parser, to_ignore):
    if parser.__class__ is SeqParser or parser.__class__ is AccompaniedAstParser:

        if to_ignore is Undef:
            result.extend(r)
        else:
            result.extend([item for item in r if
                           ((item.string not in to_ignore[Const.RawFilter]
                             and item.name not in to_ignore[Const.NameFilter]
                             ) if item.__class__ is Tokenizer else (
                                   item.name not in to_ignore[Const.NameFilter]))])
    else:
        if to_ignore is Undef:
            result.append(r)
        else:
            if r.__class__ is Tokenizer:
                if r.string not in to_ignore[Const.RawFilter] and r.name not in to_ignore[Const.NameFilter]:
                    result.append(r)
            elif r.name not in to_ignore[Const.NameFilter]:
                result.append(r)


def left_recursion(cases, meta: 'MetaInfo', recur_case, recur_info):
    recur = recur_info.node
    for case in recur.possibilities:
        if case is recur_case:
            continue

        very_first = recur.pattern_match(cases, meta, case, recur=recur)
        if isinstance(very_first, RecursiveFound) or very_first is Const.UnMatched:
            continue
        else:
            history = meta.commit()
            first = very_first
            recur_depth_count = 0
            while True:
                for parser, possibility in recur_info.possibilities:
                    result = parser.pattern_match(cases, meta, possibility, recur=recur)
                    if result is Const.UnMatched:
                        meta.rollback(history)
                        return Const.UnMatched if recur_depth_count is 0 else very_first
                    elif isinstance(result, Ast):
                        result.appendleft(first)
                    elif isinstance(result, RecursiveFound):
                        raise UnsolvedError("Error occurs : found a new left recursion when handling an other.")
                    else:
                        raise UnsolvedError("Unsolved return from method `patternMatch`.")
                    first = result
                recur_depth_count += 1
                very_first = first
    else:
        # Fail to match any case.
        return Const.UnMatched


class AccompaniedAstParser(AstParser):
    pass


class SeqParser(AstParser):

    def __init__(self, *cases, name=Undef, at_least=0, at_most=Undef):
        super(SeqParser, self).__init__(*cases, name=name)

        if at_most is Undef:
            if at_least is 0:
                self.name = f"({self.name})*"
            else:
                self.name = f'({self.name}){{{at_least}}}'
        else:
            self.name = f"({self.name}){{{at_least},{at_most}}}"

        self.at_least = at_least
        self.at_most = at_most

    def match(self, tokens, meta: 'MetaInfo', recur=Undef):

        result = Ast(meta.clone(), self.name)

        if meta.count == len(tokens):  # boundary cases
            if self.at_least is 0:
                return result
            return Const.UnMatched

        history = meta.commit()
        matched_num = 0
        if self.at_most is not Undef:
            """ (ast){a b} """
            while True:
                if matched_num >= self.at_most:
                    break
                try:
                    r = AstParser.match(self, tokens, meta=meta, recur=recur)
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
                    r = AstParser.match(self, tokens, meta=meta, recur=recur)
                except IndexError:
                    break

                if r is Const.UnMatched:
                    break

                elif isinstance(r, RecursiveFound):
                    raise UnsolvedError("Cannot make left recursions in SeqParser!!!")

                result.extend(r)
                matched_num += 1

        if matched_num < self.at_least:
            meta.rollback(history)
            return Const.UnMatched

        return result
