try:
    from typing import Iterable, Tuple, List, Dict, Set

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
    keyword = const = 1
    char = 2


class TokenSpec:
    def __init__(self):
        self.enums: 'Dict[str, str]' = {}
        # enum name -> const string

        self.tokens: 'List[Tuple[str, int, str]]' = []

    def to_token_table(self, indent=15):
        generated_tokens = set()
        _join = f',\n{" "*indent}'.join
        if not self.tokens:
            return '()'
        groups = linq.Flow(self.tokens).Group(lambda name, mode, string: (name, mode if mode is not Mode.regex else string)).Unboxed()

        def make_each(group: 'List[Tuple[str, int, str]]'):
            name, mode, string = group.__iter__().__next__()
            if mode is Mode.regex:
                return '(unique_literal_cache_pool["{name}"], regex_matcher({string}))'.format(name=name, string=string)

            modes = []
            for _, _, string in group:

                tp = (name, string)
                if tp not in generated_tokens:
                    modes.append(string)
                    generated_tokens.add(tp)

            if not modes:
                return None

            match_mode = ', '.join(sorted(modes, reverse=True))

            if mode is Mode.char:
                return '(unique_literal_cache_pool["{}"], char_matcher(({})))'.format(name, match_mode)

            return '(unique_literal_cache_pool["{}"], str_matcher(({})))'.format(name, match_mode)

        token_items = linq.Flow(groups).Map(make_each).Filter(lambda x: x).Then(_join).Unboxed()
        return '({})'.format(token_items)

    def to_name_enum(self):

        if not self.enums:
            return ""
        indent = f'\n{" "*4}'
        _join = indent.join

        name_enums = linq.Flow(
            self.enums.items()
        ).Map(
            lambda name, string: f"{name} = unique_literal_cache_pool[{string}]"
        ).Then(
            _join
        ).Unboxed()

        enum_class_spec = """
class UNameEnum:
# names
{}{}
        """.format(indent,
                   name_enums)

        return enum_class_spec


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
        return f'[name: {self.name}, string: "{self.string}", lineno: {self.lineno}, colno: {self.colno}]'

    def __str__(self):

        return '[name: {}, string: "{}"]'.format(self.name, self.string)

    @staticmethod
    def from_raw_strings(raw_string: str, token_table: 'Iterable', to_ignore=({}, {}), cast_map: dict = None):
        if cast_map is None:
            cast_map = {}

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
                        if w in cast_map:
                            name = cast_map[w]
                            w = unique_literal_cache_pool[w]
                            yield Tokenizer(name, w, lineno, colno)
                        else:
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
                break


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


def unique_lit_value(obj):
    if obj.mode is not unique_literal_cache_pool[obj.mode]:
        obj.mode = unique_literal_cache_pool[obj.mode]
