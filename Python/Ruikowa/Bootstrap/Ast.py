import linq
import os
from collections import namedtuple, OrderedDict
from typing import List, Tuple
from .Token import NameEnum, Tokenizer
from ..ObjectRegex.Tokenizer import Mode, TokenSpec
from ..Core.BaseDef import *
from ..ErrorFamily import UnsupportedStringPrefix, find_location
from ..ObjectRegex.Node import Ast
from ..color import Colored
from ..io import grace_open

SeqParserParams = namedtuple('DA', ['at_least', 'at_most'])
CompilingNodes = namedtuple('CN', ['reachable', 'alone'])

T = 'Union[Ast, List[Union[Ast, Tokenizer]]]'


def get_string_and_mode(prefix_string: str):
    if prefix_string[0] is not '\'':
        return prefix_string[0], prefix_string[1:]
    else:
        return None, prefix_string


def surround_with_double_quotes(string):
    return '"{}"'.format(string)


class Compiler:
    def __init__(self, filename: str = None, src_code: str = None):
        self.src = src_code
        self.filename = filename

        self.token_func_src = None
        self.token_spec = TokenSpec()
        self.token_ignores = ('{}', '{}')

        self.literal_parser_definitions = []
        self.combined_parsers = []

        self.compile_helper = CompilingNodes(set(), set())
        self._current_indent = None
        self._current__combined_parser_name = None
        self._current_events = None
        self._current_anonymous_count = 0

    def ast_for_stmts(self, stmts: T) -> None:
        """
        Stmts    ::= TokenDef{0, 1} Equals*;
        """
        if not stmts:
            raise ValueError('no ast found!')
        head, *equals = stmts

        if head.name is NameEnum.TokenDef:
            self.ast_for_token_def(head)
        elif head.name is NameEnum.TokenIgnore:
            self.ast_for_token_ignore(head)
        else:
            self.ast_for_equals(head)

        for each in equals:
            self.ast_for_equals(each)

    def ast_for_token_ignore(self, token_ignore: T):
        _, _, *items, _ = token_ignore
        grouped = linq.Flow(items).GroupBy(lambda x: x.name is NameEnum.Str).Unboxed()
        lit_ignore = "{{{}}}".format(', '.join(map(lambda _: _.string, grouped[True])))
        name_ignore = "{{{}}}".format(', '.join(map(lambda _: '"' + _.string + '"', grouped[False])))
        self.token_ignores = (name_ignore, lit_ignore)

    def ast_for_token_def(self, token_def: T):
        content = token_def[1]
        if content.name is NameEnum.Name:
            path = os.path.join(*
                                map(lambda _: '..' if _ == 'parent' else _,
                                    content.string.split('.')))
            self.token_func_src = grace_open(path).read()
            return
        else:
            self.token_func_src = content.string[2:-2]

    def ast_for_equals(self, equals: T):
        if equals[-2].name is NameEnum.Str:
            name, _, *str_tks, _ = equals
            name = name.string
            for str_tk in str_tks:
                str_tk: 'Tokenizer'
                mode, string = get_string_and_mode(str_tk.string)
                if mode is 'R':
                    mode = Mode.regex
                elif len(string) is 3:
                    mode = Mode.char
                else:
                    mode = Mode.const
                self.token_spec.append(name, mode, string, name_unique=False)
                self.literal_parser_definitions.append("{} = LiteralNameParser('{}')".format(name, name))
        else:
            if equals[1].name is NameEnum.Throw:
                name, throw, _, expr, _ = equals
                name: 'Tokenizer'
                throw: 'T' = self.ast_for_throw(throw)
                grouped = linq.Flow(throw).GroupBy(lambda x: x.name is NameEnum.Str).Unboxed()
            else:
                name, _, expr, _ = equals
                name: 'Tokenizer'
                grouped = {True: (), False: ()}
            self._current__combined_parser_name = name.string
            if name.string not in self.compile_helper.reachable:
                self.compile_helper.alone.add(name.string)

            indent = '             ' + " " * len(name.string)
            self.combined_parsers.append(
                '{name} = AstParser({possibilities},\n'
                '{indent}name="{name}",\n'
                '{indent}to_ignore=({name_ignore}, {lit_ignore}))'
                ''.format(
                    indent=indent,
                    name=name.string,
                    possibilities=(',\n{}'.format(indent)).join(self.ast_for_expr(expr)),
                    lit_ignore="{{{}}}".format(', '.join(map(lambda _: _.string, grouped[True]))),
                    name_ignore="{{{}}}".format(', '.join(map(lambda _: '"' + _.string + '"', grouped[False])))
                ))

    def ast_for_throw(self, throw: T):
        _, _, *items, _ = throw
        return items

    def ast_for_expr(self, expr: T):
        return (self.ast_for_or(each) for each in expr[::2])

    def ast_for_or(self, or_expr: T):

        return '[{}]'.format(', '.join(self.ast_for_atom_expr(each) for each in or_expr))

    def ast_for_atom_expr(self, atom_expr: T):
        if len(atom_expr) is 1:
            atom = atom_expr[0]
            atom: 'Ast'
            maybe_tk, default_attrs = self.ast_for_atom(atom)
            default_attrs: 'SeqParserParams'
            if maybe_tk.__class__ is Tokenizer:
                if maybe_tk.name is NameEnum.Name:

                    if maybe_tk.string in self.compile_helper.alone:
                        self.compile_helper.alone.remove(maybe_tk.string)

                    if maybe_tk.name not in self.compile_helper.reachable:
                        self.compile_helper.reachable.add(maybe_tk.string)

                    return "Ref('{}')".format(maybe_tk.string)

                else:
                    mode, string = get_string_and_mode(maybe_tk.string)
                    if not mode:
                        if len(string) is 3 and string[1] not in self.token_spec:
                            self.token_spec.append(':char', Mode.char, string)
                            return string
                        for k, mode, v in self.token_spec.source:
                            if mode is Mode.const and v is string:
                                break
                        else:
                            self.token_spec.append(':const', Mode.const, string)
                        return string

                    if mode is 'R':
                        for k, mode, v in self.token_spec.source:
                            if mode is Mode.regex and v == string:

                                if k in self.compile_helper.alone:
                                    self.compile_helper.alone.remove(k)

                                if k not in self.compile_helper.reachable:
                                    self.compile_helper.reachable.add(k)

                                return "Ref('{}')".format(k)

                        name: str = 'anonymous_{}'.format(self._current_anonymous_count)
                        self._current_anonymous_count += 1
                        warnings.warn(
                            Colored.LightBlue +
                            '\nFor efficiency of the parser, '
                            'we do not do regex matching when parsing(only in tokenizing we use regex), '
                            'you are now creating a anonymous regex literal parser '
                            '{}<{}>{} when defining combined parser{}\n'
                            .format(Colored.Red, name, Colored.LightBlue, Colored.Clear))

                        self.token_spec.append(name, Mode.regex, string, name_unique=True)
                        self.literal_parser_definitions.append("{} = LiteralNameParser('{}')".format(name, name))

                        if name in self.compile_helper.alone:
                            self.compile_helper.alone.remove(name)

                        if name not in self.compile_helper.reachable:
                            self.compile_helper.reachable.add(name)

                        return "Ref('{}')".format(name)
                    raise UnsupportedStringPrefix(mode, find_location(self.filename, maybe_tk, self.src))

            return ('SeqParser({possibilities}, '
                    'at_least={at_least},'
                    'at_most={at_most})'
                    .format(possibilities=', '.join(maybe_tk),
                            at_least=default_attrs.at_least,
                            at_most=default_attrs.at_most))


        else:
            atom, trailer = atom_expr
            maybe_tk, _ = self.ast_for_atom(atom)
            attrs = self.ast_for_trailer(trailer)
            if maybe_tk.__class__ is Tokenizer:
                return ('SeqParser([{atom}], '
                        'at_least={at_least}, '
                        'at_most={at_most})'
                    .format(
                    atom='Ref("{}")'.format(maybe_tk.string) if maybe_tk.name is NameEnum.Name else maybe_tk.string,
                    at_least=attrs.at_least,
                    at_most=attrs.at_most))

            return ('SeqParser({possibilities}, '
                    'at_least={at_least}, '
                    'at_most={at_most})'
                    .format(possibilities=','.join(maybe_tk),
                            at_least=attrs.at_least,
                            at_most=attrs.at_most))

    def ast_for_atom(self, atom: 'Ast'):
        if atom[0].string is '(':
            return self.ast_for_expr(atom[1]), SeqParserParams(1, 1)
        elif atom[0].string is '[':
            return self.ast_for_expr(atom[1]), SeqParserParams(0, 1)

        return atom[0], None

    def ast_for_trailer(self, trailer):
        if len(trailer) is 1:
            trailer: 'Tokenizer' = trailer[0]
            return SeqParserParams(0, 'Undef') if trailer.string is '*' else SeqParserParams(1, 'Undef')
        else:
            _, *numbers, _ = trailer
            numbers: 'List[Tokenizer]'
            if len(numbers) is 2:
                a, b = numbers
                return SeqParserParams(a.string, a.string)
            else:
                return SeqParserParams(numbers[0].string, 'Undef')
