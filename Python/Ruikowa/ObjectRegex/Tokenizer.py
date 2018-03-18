try:
    from typing import Iterable, Tuple, List

    if False:
        from re import __Regex
except ModuleNotFoundError:
    pass

import re
import json
import linq
from collections import defaultdict
from ..ErrorFamily import UniqueNameConstraintError
from ..ErrorHandler import Colored, Warnings as warnings


class Mode:
    regex = 0
    const = 1
    char = 2


class TokenSpec:
    def __init__(self):
        self.source = []
        self.names = set()

    def append(self, name, mode, string, name_unique=False):
        if name_unique:
            if name in self.names:
                raise UniqueNameConstraintError(name)

            self.source.append((name, mode, string))
            self.names.add(name)
            return
        if name in self.names and mode is Mode.regex:
            warnings.warn(Colored.Yellow + "Sharing one name" + Colored.Red + " '{}' ".format(
                name) + Colored.Yellow + "with multiple regex literal parsers." + Colored.Clear)
        self.source.append((name, mode, string))
        self.names.add(name)

    def to_token_table(self, indent=15):
        groups = linq.Flow(self.source).Group(
            lambda name, mode, string: (name, string if mode is Mode.regex else mode)).Unboxed()

        def make_each(group: 'List[Tuple[str, int, str]]'):
            name, mode, string = group[0]
            if mode is Mode.regex:
                return '(unique_literal_cache_pool["{name}"], regex_matcher({string}))'.format(name=name, string=string)

            match_mode = ', '.join(sorted(tuple(string for _, _, string in group), reverse=True))
            if mode is Mode.char:
                return '(unique_literal_cache_pool["{}"], char_matcher(({})))'.format(name, match_mode)

            return '(unique_literal_cache_pool["{}"], str_matcher(({})))'.format(name, match_mode)

        return "({})".format(',\n{indent}'.format(indent=' ' * indent).join(make_each(each) for each in groups))

    def to_name_enum(self):
        groups = linq.Flow(
            self.source
        ).Filter(
            lambda name, mode, b: mode is not Mode.char and (
                    name.isidentifier() or name[0] is ':' and name[1:].isidentifier())
        ).Group(
            lambda name, mode, string: (name, string if mode is Mode.regex else mode)
        ).Unboxed()

        indent = ' ' * 4

        def make_each(group: 'List[Tuple[str, int, str]]'):
            name, mode, string = group[0]

            if mode is Mode.regex:
                if name[0] is ':':
                    return '{name} = unique_literal_cache_pool["{name}"]'.format(name=name[1:])
                return '{name} = unique_literal_cache_pool["{name}"]'.format(name=name)

            return '\n{}'.format(indent).join(
                'const_{name} = unique_literal_cache_pool["{name}"]'.format(name=name) for _, _, string in
                group)

        enum_class_spec = """
class UNameEnum:
{}{}
        """.format(indent,
                   '\n{}'
                   .format(indent)
                   .join(make_each(each) for each in groups))
        return enum_class_spec

    def __contains__(self, item):
        return item in self.names


class Tokenizer:
    def __init__(self, name: str, string: str, lineno: int, colno: int):
        self.name = name
        self.lineno = lineno
        self.colno = colno
        self.string = string

    def dump_to_json(self):
        return dict(name=self.name, string=self.string, lineno=self.lineno, colno=self.colno)

    def dump(self):
        return self.__str__()

    def __repr__(self):
        return '[name: {}, string: "{}", lineno: {}, colno: {}]'.format(self.name,
                                                                        self.string,
                                                                        self.lineno,
                                                                        self.colno)

    def __str__(self):

        return '[name: {}, string: "{}"]'.format(self.name, self.string)

    @staticmethod
    def from_raw_strings(raw_string: str, token_table: 'Iterable', to_ignore=({}, {})):
        if not raw_string:
            return ()
        lineno = 0
        colno = 0
        pos = 0
        n = len(raw_string)
        while True:
            for name, pat in token_table:
                w = pat(raw_string, pos)

                if w:
                    row_inc = w.count('\n')
                    length = len(w)

                    if row_inc:
                        lineno += row_inc
                        colno = length - w.rfind('\n') - 1
                    else:
                        colno += length

                    pos += length

                    if name not in to_ignore[0] and w not in to_ignore[1]:
                        yield Tokenizer(unique_literal_cache_pool[name], w, lineno, colno)

                    if n == pos:
                        return
                    break

            else:
                warnings.warn('no token def {}'.format(raw_string[pos].encode()))
                if raw_string[pos] is '\n':
                    colno = 0
                    lineno += 1
                else:
                    colno += 1
                pos += 1
                if n == pos:
                    return


def char_matcher(mode):
    """
    a faster way for characters to generate token strings cache
    """

    def f_raw(inp_str, pos):
        return mode if inp_str[pos] is mode else None

    def f_collection(inp_str, pos):
        ch = inp_str[pos]
        for each in mode:
            if ch is each:
                return ch
        return None

    if isinstance(mode, str):
        return f_raw

    if len(mode) is 1:
        mode = mode[0]
        return f_raw

    return f_collection


def str_matcher(mode):
    """
    generate token strings' cache
    """

    def f_raw(inp_str, pos):
        return unique_literal_cache_pool[mode] if inp_str.startswith(mode, pos) else None

    def f_collection(inp_str, pos):
        for each in mode:
            if inp_str.startswith(each, pos):
                return unique_literal_cache_pool[each]
        return None

    if isinstance(mode, str):
        return f_raw

    if len(mode) is 1:
        mode = mode[0]
        return f_raw

    return f_collection


def regex_matcher(regex_pat):
    """
    generate token names' cache
    :param regex_pat:
    :return:
    """
    if isinstance(regex_pat, str):
        regex_pat = re.compile(regex_pat)

    def f(inp_str, pos):
        m = regex_pat.match(inp_str, pos)
        return m.group() if m else None

    return f


class UniqueLiteralCachePool:
    def __init__(self, dictionary: dict):
        self.content = dictionary

    def __getitem__(self, item):
        try:
            return self.content[item]
        except KeyError:
            self.content[item] = item
            return item


unique_literal_cache_pool = UniqueLiteralCachePool({})


def unique_lit_name(obj):
    if obj.name is not unique_literal_cache_pool[obj.name]:
        obj.name = unique_literal_cache_pool[obj.name]
