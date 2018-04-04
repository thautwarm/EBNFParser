import os
import linq
from collections import namedtuple
from typing import List, Tuple
from .Token import NameEnum
from ..Core.BaseDef import *
from ..ErrorFamily import UnsupportedStringPrefix, find_location
from ..ObjectRegex.Node import Ast
from ..ObjectRegex.Tokenizer import Mode, TokenSpec, Tokenizer
from ..color import Colored
from ..io import grace_open

SeqParserParams = namedtuple('DA', ['at_least', 'at_most'])
CompilingNodes = namedtuple('CN', ['reachable', 'alone'])

T = 'Union[Ast, List[Union[Ast, Tokenizer]]]'


def get_string_and_mode(prefix_string: str) -> 'Tuple[Optional[str],  str]':
    if prefix_string[0] is not '\'':
        return prefix_string[0], prefix_string[1:]
    else:
        return None, prefix_string


def surround_with_double_quotes(string):
    return '"{}"'.format(string)


class Compiler:
    # TODO: refactor and clear redundant items.
    def __init__(self, filename: str = None, src_code: str = None):
        self.src = src_code
        self.filename = filename

        self.token_func_src = None
        self.token_spec = TokenSpec()
        self.token_ignores = ('{}', '{}')  # define what to ignore when tokenizing.
        self.prefix_mapping = {}
        self.cast_map = {}
        self.c_macro = {}

        self.generated_token_names = set()

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

        # if every combined parser can reach any other combined, 
        # just take any of them and compile it!
        if not self.compile_helper.alone and self._current__combined_parser_name:
            self.compile_helper.alone.add(self._current__combined_parser_name)

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
        str_tks: 'List[Tokenizer]'
        if equals[-2].name is NameEnum.Str:

            defining_cast_map = False
            if equals[1].name is NameEnum.Prefix:
                name, prefix, _, *str_tks, _ = equals
                prefix: 'Ast'
                prefix_string = prefix[1].string
                if len(prefix_string) > 1:
                    raise UnsupportedStringPrefix(prefix_string,
                                                  " the length of prefix name should be 1 only." +
                                                  find_location(self.filename, prefix[1], self.src))
                self.prefix_mapping[prefix_string] = name.string
                defining_cast_map = True

            elif equals[1].name is NameEnum.Of:

                ref_name, of, _, *str_tks, _ = equals
                name = of[1]
                self.c_macro[ref_name.string] = name.string

            else:
                name, _, *str_tks, _ = equals

            name = name.string

            if defining_cast_map:
                # define cast map
                for str_tk in str_tks:
                    mode, string = get_string_and_mode(str_tk.string)
                    if mode:
                        raise UnsupportedStringPrefix(mode,
                                                      'do not support setting prefix when defining custom prefix.' +
                                                      find_location(self.filename, str_tk, self.src))
                    self.cast_map[string] = name
                    if str_tk.string[1:-1].isidentifier():
                        self.token_spec.enums.__setitem__(f'{name}_{str_tk.string[1:-1]}', str_tk.string)
            else:
                # define how to tokenize
                for str_tk in str_tks:
                    mode, string = get_string_and_mode(str_tk.string)
                    if mode is 'R':
                        mode = Mode.regex
                    elif len(string) is 3:
                        mode = Mode.char
                    else:
                        mode = Mode.const
                    self.token_spec.tokens.append((name, mode, string))
                    if string[1:-1].isidentifier():
                        self.token_spec.enums.__setitem__(f'{name}_{string[1:-1]}', string)

            if name not in self.generated_token_names:
                self.literal_parser_definitions.append("{} = LiteralNameParser('{}')".format(name, name))
                self.generated_token_names.add(name)
            self.token_spec.enums.__setitem__(name, f"'{name}'")


        else:
            if equals[1].name is NameEnum.Throw:
                name, throw, _, expr, _ = equals
                throw: 'T' = self.ast_for_throw(throw)
                grouped = linq.Flow(throw).GroupBy(lambda x: x.name is NameEnum.Str).Unboxed()
            else:
                name, _, expr, _ = equals
                grouped = {True: (), False: ()}

            name = self._current__combined_parser_name = name.string
            self.token_spec.enums.__setitem__(name, f"'{name}'")

            if name not in self.compile_helper.reachable:
                self.compile_helper.alone.add(name)

            indent = '             ' + " " * len(name)
            self.combined_parsers.append(
                '{name} = AstParser({possibilities},\n'
                '{indent}name="{name}",\n'
                '{indent}to_ignore=({name_ignore}, {lit_ignore}))'
                ''.format(
                    indent=indent,
                    name=name,
                    possibilities=(',\n{}'.format(indent)).join(self.ast_for_expr(expr)),
                    lit_ignore="{{{}}}".format(', '.join(map(lambda _: _.string, grouped[True]))),
                    name_ignore="{{{}}}".format(', '.join(map(lambda _: '"' + _.string + '"', grouped[False])))
                ))

    @classmethod
    def ast_for_throw(cls, throw: T):
        _, _, *items, _ = throw
        return items

    def ast_for_expr(self, expr: T):
        return (self.ast_for_or(each) for each in expr[::2])

    def ast_for_or(self, or_expr: T):

        return '[{}]'.format(', '.join(self.ast_for_atom_expr(each) for each in or_expr))

    def handle_atom_with_trailer(self, atom: T):
        maybe_tk, default_attrs = self.ast_for_atom(atom)
        default_attrs: 'SeqParserParams'
        if maybe_tk.__class__ is Tokenizer:
            if maybe_tk.name is NameEnum.Name:

                name = self.c_macro.get(maybe_tk.string, maybe_tk.string)

                if name in self.compile_helper.alone:
                    self.compile_helper.alone.remove(name)

                if name not in self.compile_helper.reachable:
                    self.compile_helper.reachable.add(name)

                return "Ref('{}')".format(name)

            else:
                mode, string = get_string_and_mode(maybe_tk.string)
                if not mode:
                    for k, mode, v in self.token_spec.tokens:
                        # check if need to create a new token pattern
                        if v is string and k == 'auto_const':
                            break

                    else:
                        if len(string) is 3:
                            self.token_spec.tokens.append(('auto_const', Mode.char, string))
                        else:
                            self.token_spec.tokens.append(('auto_const', Mode.const, string))
                    return string

                if mode is 'R':
                    for k, mode, v in self.token_spec.tokens:
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

                    self.token_spec.tokens.append((name, Mode.regex, string))
                    self.token_spec.enums.__setitem__(name, f"'{name}'")
                    self.literal_parser_definitions.append("{} = LiteralNameParser('{}')".format(name, name))

                    if name in self.compile_helper.alone:
                        self.compile_helper.alone.remove(name)

                    if name not in self.compile_helper.reachable:
                        self.compile_helper.reachable.add(name)

                    return "Ref('{}')".format(name)

                elif mode is 'L':
                    return f"L({string})"

                elif mode not in self.prefix_mapping:
                    raise UnsupportedStringPrefix(mode, "Prefix not defined."
                                                  + find_location(self.filename, maybe_tk, self.src))

                else:
                    name = self.prefix_mapping[mode]
                    self.cast_map[string] = name
                    return f"('{name}', {string})"

        return dict(possibilities=', '.join(maybe_tk),
                    at_least=default_attrs.at_least,
                    at_most=default_attrs.at_most)

    def ast_for_atom_expr(self, atom_expr: T):
        if len(atom_expr) is 1:
            res = self.handle_atom_with_trailer(atom_expr[0])
            if res.__class__ is dict:
                return ('SeqParser({possibilities}, '
                        'at_least={at_least},'
                        'at_most={at_most})'.format(**res))
            return res

        atom, trailer = atom_expr
        res = self.handle_atom_with_trailer(atom)
        attrs = self.ast_for_trailer(trailer)

        if res.__class__ is dict:
            res.update(at_least=attrs.at_least, at_most=attrs.at_most)

            return ('SeqParser({possibilities}, '
                    'at_least={at_least},'
                    'at_most={at_most})'.format(**res))

        return ('SeqParser({possibilities}, '
                'at_least={at_least},'
                'at_most={at_most})'.format(possibilities=res if res[0] is '[' else f'[{res}]',
                                            at_most=attrs.at_most,
                                            at_least=attrs.at_least))

    def ast_for_atom(self, atom: 'Ast'):
        if atom[0].string is '(':
            return self.ast_for_expr(atom[1]), SeqParserParams(1, 1)
        elif atom[0].string is '[':
            return self.ast_for_expr(atom[1]), SeqParserParams(0, 1)

        return atom[0], None

    @classmethod
    def ast_for_trailer(cls, trailer):
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
