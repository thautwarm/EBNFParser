import re as re
from ..ObjectRegex.Tokenizer import (Tokenizer, str_matcher, regex_matcher,
                                     char_matcher, unique_literal_cache_pool)


def _escape(*str_s):
    return '|'.join([re.escape(string) for string in str_s])


class NameEnum:
    keyword_as = unique_literal_cache_pool['as']
    keyword_of = unique_literal_cache_pool['of']
    keyword_throw = unique_literal_cache_pool['throw']
    keyword_deftoken = unique_literal_cache_pool['deftoken']
    keyword_ignore = unique_literal_cache_pool['ignore']

    Of = unique_literal_cache_pool['Of']
    Prefix = unique_literal_cache_pool['Prefix']
    Comments = unique_literal_cache_pool['Comments']
    Str = unique_literal_cache_pool['Str']
    Codes = unique_literal_cache_pool['Codes']

    Name = unique_literal_cache_pool['Name']
    Number = unique_literal_cache_pool['Number']
    Newline = unique_literal_cache_pool['Newline']

    TokenIgnore = unique_literal_cache_pool['TokenIgnore']
    Single = unique_literal_cache_pool['Single']
    Eq = unique_literal_cache_pool['Eq']
    TokenRelated = unique_literal_cache_pool['TokenRelated']

    TokenDef = unique_literal_cache_pool['TokenDef']
    Throw = unique_literal_cache_pool['Throw']


token_table = (
    # match by value
    ("auto_const", char_matcher(
        ('|',
         '{',
         '}',
         ';',
         '[',
         ']',
         '(',
         ')',
         '+',
         '*',
         '.')
    )),

    # match by value
    ("auto_const", str_matcher(
        ("::=", ":=")
    )),

    # match by name
    ('Comment', regex_matcher(re.compile(r'(#.*)|(((/\*)+?[\w\W]+?(\*/)+))'))),
    ("Str", regex_matcher(re.compile(r"[A-Z]'([^\\']+|\\.)*?'|'([^\\']+|\\.)*?'"))),
    ("Codes", regex_matcher(re.compile(r'{{[\w\W]+?\}\}'))),

    ("Name", regex_matcher("[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5\.]*")),
    ("Number", regex_matcher("\d+")),

    # do not match
    ("Space", regex_matcher('\s+|,')),

)

token_table = tuple((unique_literal_cache_pool[k], v) for k, v in token_table)
keyword = unique_literal_cache_pool['keyword']
cast_map = {
    'as': keyword,
    'throw': keyword,
    'deftoken': keyword,
    'ignore': keyword,
    'for': keyword,
    'of': keyword
}

token_func = lambda _: Tokenizer.from_raw_strings(_,
                                                  token_table,
                                                  to_ignore=({'Space', 'Comment'}, {}), cast_map=cast_map)
