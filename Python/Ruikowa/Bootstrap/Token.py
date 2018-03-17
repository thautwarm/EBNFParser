import re as re
from ..ObjectRegex.Tokenizer import (Tokenizer, str_matcher, regex_matcher,
                                     char_matcher, unique_literal_cache_pool)


def _escape(*strs):
    return '|'.join([re.escape(str) for str in strs])


class NameEnum:
    Comments = unique_literal_cache_pool['Comments']
    Str = unique_literal_cache_pool['Str']
    Codes = unique_literal_cache_pool['Codes']

    Name = unique_literal_cache_pool['Name']
    Number = unique_literal_cache_pool['Number']
    Newline = unique_literal_cache_pool['Newline']

    Single = unique_literal_cache_pool['Single']
    Eq = unique_literal_cache_pool['Eq']
    TokenRelated = unique_literal_cache_pool['TokenRelated']

    AV_Token = unique_literal_cache_pool['AutoValue-Token']
    Throw = unique_literal_cache_pool['Throw']


token_table = (
    # match by value
    ("TokenRelated", str_matcher(
        ("Token", "Throw")
    )),
    # match by value
    ("Single", char_matcher(
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
    ("Eq", str_matcher(
        ("::=", ":=")
    )),

    # match by name
    ('Comment', regex_matcher(re.compile(r'(#.*)|(((/\*)+?[\w\W]+?(\*/)+))'))),
    ("Str", regex_matcher(re.compile(r"[A-Z]'([^\\']+|\\.)*?'|'([^\\']+|\\.)*?'"))),
    ("Codes", regex_matcher(re.compile('\{\{[\w\W]+?\}\}'))),

    ("Name", regex_matcher("[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\.]*")),
    ("Number", regex_matcher("\d+")),

    # do not match
    ("Space", regex_matcher('\s+')),

)

token_table = tuple((unique_literal_cache_pool[k], v) for k, v in token_table)
token_func = lambda _: Tokenizer.from_raw_strings(_,
                                                  token_table,
                                                  to_ignore=({'Space', 'Comment'}, {}))
