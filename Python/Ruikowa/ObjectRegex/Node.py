#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:53:53 2017

@author: misakawa
"""




DEBUG = True

def debugger(Begin='', End = '', Check = lambda x:Undef):
    def funcHook(matcher):
        def innerHook(*args, **kwargs):
            locals()['args'] = args
            locals().update(kwargs)
            exec(Begin, locals())
            ret = matcher(*args, **kwargs)
            checked = Check(ret)
            if checked is Undef : pass
            else:
                print(checked)
            exec(End, locals())
            return ret
        return innerHook
    return funcHook




from ..Core.BaseDef import *
from .MetaInfo import MetaInfo
from ..ErrorFamily import *
from .PatternMatching import *
from .ASTDef import Ast

class Ignore:
    Value = 0
    Name  = 1

class BaseParser:
    """Abstract Class"""
    name       = Undef
    has_recur  = Undef
    def match(self, objs:List[str], meta:MetaInfo, allowLR:bool):
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

    def RawFormProcessor(rawStr, name = Undef):
        return LiteralParser(rawStr, name = name, isRegex = False)

class Ref(BaseParser):
    def __init__(self,name):self.name = name

class AstParser(BaseParser):
    def __init__(self, *ebnf, name=Undef, toIgnore: List[set] = Undef):
        # each in the cache will be processed into a parser.
        self.cache = ebnf

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

    def compile(self, namespace: dict, recurSearcher: set):

        if self.name in recurSearcher:
            self.has_recur = True
            self.compiled = True
        else:
            recurSearcher.add(self.name)

        if self.compiled:
            return self

        self.patternMatch = patternMatch(self)
        if isinstance(self, SeqParser):
            self.matchOne = AstMatch(self)
        else:
            self.match = AstMatch(self)

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
                    if e.has_recur:
                        self.has_recur = True

                elif isinstance(e, AstParser):
                    if e.name not in namespace:
                        namespace[e.name] = e
                    else:
                        e = namespace[e.name]
                    e.compile(namespace, recurSearcher)
                    self.possibilities[-1].append(e)
                    if e.has_recur:
                        self.has_recur = True
                else:
                    raise UnsolvedError("Unknown Parser Type.")

        if hasattr(self, 'cache'):
            del self.cache

        if self.name in recurSearcher:
            recurSearcher.remove(self.name)

        if not self.compiled:
            self.compiled = True

def AstMatch(self):

    def match(objs, meta, allowLR = True):
        meta.branch()
        if self.has_recur:
            if self not in meta.trace[meta.count][:meta.trace[meta.count].length]:
                # if DEBUG:
                #     print('{name} Has Recur Possibility : '.format(name = self.name))
                #     print('LENGTH BEFORE: {len}'.format(len = meta.trace[meta.count].length))
                meta.trace[meta.count].push(self)
                # if DEBUG:
                #     print('LENGTH BEFORE: {len}'.format(len=meta.trace[meta.count].length))
            else:
                meta.rollback()
                # if DEBUG:
                #     print('ROLLBACK ', self.name)

                if not allowLR or isinstance(self, SeqParser):
                    return Const.UnMatched
                # if DEBUG:
                #     print('FOUND LEFT RECUR : {name}'.format(name = self.name))

                raise RecursiveFound(self)

        # if DEBUG:
        #     enum = 0

        for possibility in self.possibilities:

            result = self.patternMatch(objs, meta, possibility, allowLR = allowLR)

            if result is Const.UnMatched:
                # if DEBUG:
                #     print('POSSIBILITY {enum} failed.'.format(enum = enum))
                #     enum += 1
                meta.rollback()
                meta.branch()
                continue

            elif isinstance(result, Ast):
                # if DEBUG:
                #     print('GET RESULT for NODE {name}: \n{result}'.format(result = result, name = self.name))

                meta.pull()
                # if DEBUG:
                #     print('PULL ', self.name)

                return result

            elif isinstance(result, RecursiveFound):
                # if DEBUG:
                #     print('ROLLBACK ', self.name)

                if self is result.node:
                    # if DEBUG:
                    #     print("RECUR DONE AT {name}".format(name = self.name))

                    meta.rollback()
                    break # Deal (Cycle) Left Recursive Cases
                else:
                    # if DEBUG:
                    #     print("RECUR PASS BY {name}".format(name = self.name))

                    meta.rollback()  # rollback or pull?
                    return result

        else:
            # if DEBUG:
            #     print('Failed at all in NODE {name}.'.format(name = self.name))

            meta.rollback()
            # if DEBUG:
            #     print('ROLLBACK ', self.name)

            return Const.UnMatched

        # if LR :
        # if DEBUG:
        #     print(meta.history, ' <= hisory')
        recur:RecursiveFound = result
        veryFirst = recur.node.match(objs, meta, allowLR=False)
        # if DEBUG:
        #     print('veryFirst =>', veryFirst)
        first = veryFirst
        if first is Const.UnMatched:
            return Const.UnMatched
        # if DEBUG:
        #     print('RECUR STRUCTURE:')
        #     print(recur)
        # do left recur :
        while True:
            meta.branch()
            for parser, possibility in recur.possibilities:
                result : Ast= parser.patternMatch(objs, meta, possibility)
                if result is Const.UnMatched:
                    meta.rollback()
                    return veryFirst
                elif isinstance(result, Ast):
                    result.appendleft(first)
                else:
                    raise UnsolvedError("???Emmmmm....")
                first = result
            meta.pull()
            veryFirst = first

        # unexpected end.
        raise UnsolvedError("unexpected LR!!!")
    return match



def patternMatch(self):
    # @debugger(
    #     Begin=r'print("-----------------------------\nCOUNT :",args[1].count, "  TRACE LENGTH :",args[1].trace.length)',
    #     End=r'print("COUNT :",args[1].count, "  TRACE LENGTH :",args[1].trace.length,"\n-----------------------------")')
    def subMatch(
             objs,
             meta,
             possibility,
             allowLR = True):
        try: # Not recur
            result = Ast(meta.clone(), self.name)
            for parser in possibility:

                # if DEBUG:
                #     print("Try Parsing Node {name}".format(name = parser.name))

                r = parser.match(objs, meta = meta, allowLR = True if result else allowLR)
                # if `result` is still empty, it might not allow LR now.

                if isinstance(r, str) or isinstance(r, Ast):

                    # if DEBUG:
                    #     print('PARSED RESULT : {r}\n From Parser {name}'.format(r = r, name = parser.name))

                    if self.toIgnore is Undef:

                        if isinstance(parser, SeqParser):
                            result.extend(r)
                        else:
                            result.append(r)
                    else:

                        if isinstance(parser, SeqParser):
                            result.extend([maybeAst for maybeAst in r if
                                           (maybeAst.name not in self.toIgnore[Const.NameFilter] \
                                                if isinstance(maybeAst, Ast) \
                                            else maybeAst not in self.toIgnore[Const.RawFilter])
                                           ])

                        else:

                            if isinstance(r, str) and r not in self.toIgnore[Const.RawFilter]:

                                result.append(r)

                            elif r.name not in self.toIgnore[Const.NameFilter]: # r is Ast

                                result.append(r)

                elif r is Const.UnMatched:
                    # if DEBUG:
                    #     print('No Matched by Parser {name}'.format(name = parser.name))
                    return Const.UnMatched

                elif isinstance(r, RecursiveFound):
                    # if DEBUG:
                    #     print('PASS LEFT RECURSION BY {name}'.format(name = parser.name))
                    r.add((self, possibility[possibility.index(parser)+1:]) )
                    return r

            else:
                # if DEBUG:
                #     print('SUCCESS at a kind of possibility of Parser {name}'.format(name = self.name))
                return result

        except RecursiveFound as RecurInfo:
            # if DEBUG:
            #     print("Found Left Recursion at Parser {name}:\n".format(name = self.name), RecurInfo)
            RecurInfo.add((self, possibility[possibility.index(parser)+1:]))
            # RecurInfo has a trace of Beginning Recur Node to Next Recur Node with
            # specific possibility.
            return RecurInfo

    return subMatch

class SeqParser(AstParser):
    def __init__(self, *ebnf, name=Undef, atleast=0, atmost=Undef):
        super(SeqParser, self).__init__(*ebnf, name = name)

        if atmost is Undef:
            if atleast is 0:
                self.name = "({NAME})*".format(NAME = self.name)
            else:
                self.name = '({NAME}){{{AT_LEAST}}}'.format(NAME = self.name, AT_LEAST=atleast)
        else:
            self.name = "({NAME}){{{AT_LEAST},{AT_MOST}}}".format(
                                                                NAME =self.name,
                                                                AT_LEAST=atleast,
                                                                AT_MOST =atmost)
        self.atleast = atleast
        self.atmost  = atmost

    def match(self, objs, meta, allowLR=True):
        result = Ast(meta.clone(), self.name)

        if meta.count == len(objs):  # boundary cases
            if self.atleast is 0:
                return result
            return Const.UnMatched

        meta.branch()
        idx = 0
        if self.atmost is not Undef:
            """ (ast){a b} """
            while True:
                if idx >= self.atmost:
                    break
                try:
                    r = self.matchOne(objs, meta=meta)

                except IndexError:
                    break

                if r is Const.UnMatched:
                    # if DEBUG:
                    #     print('No Matched by Parser {name}'.format(name=self.name))
                    break
                elif isinstance(r, RecursiveFound):
                    meta.rollback()
                    return Const.UnMatched
                # if DEBUG:
                #     print('PARSED RESULT : {r}\n From Sequence Parser {name}'.format(r=r, name=self.name))

                result.extend(r)
                idx += 1
        else:
            """ ast{a} | [ast] | ast* """
            while True:

                try:
                    r = self.matchOne(objs, meta=meta)

                except IndexError:
                    break

                if r is Const.UnMatched:
                    # if DEBUG:
                    #     print('No Matched by Parser {name}'.format(name=self.name))
                    break

                elif isinstance(r, RecursiveFound):
                    meta.rollback()
                    return Const.UnMatched

                # if DEBUG:
                #     print('PARSED RESULT : {r}\n From Sequence Parser {name}'.format(r=r, name=self.name))

                result.extend(r)
                idx += 1

        # if DEBUG:
        #     print('Sequence Length : {idx}'.format(idx = idx))

        if  idx < self.atleast:
            # if DEBUG:
            #     print('No Matched by Parser {name} BECAUSE of NOT ENOUGH MATCHED.'.format(name=self.name))
            meta.rollback()
            return Const.UnMatched

        meta.pull()
        return result






    # if not SndNodeOfRecur : NoRecur = True

















