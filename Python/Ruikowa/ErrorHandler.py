if False:
    from .ObjectRegex.MetaInfo import MetaInfo
    from typing import Sequence, Optional
    from .ObjectRegex.Tokenizer import Tokenizer
from .ErrorFamily import *


class ErrorHandler:

    def __init__(self, parse_func, token_func=None):
        self.parse_func = parse_func
        self.token_func = token_func

    def from_file(self, filename: str, meta: 'MetaInfo' = None, partial=False):
        with open(filename, 'r', encoding='utf8') as f:
            raw_string = f.read()
        return self.from_source_code(filename, raw_string, meta, partial)

    def from_source_code(self, filename: str, src_code: str, meta: 'MetaInfo' = None, partial=False):
        tokens: 'Sequence[Tokenizer]' = tuple(self.token_func(src_code))
        return self.from_tokens(filename, src_code, tokens, meta, partial)

    def from_tokens(self, filename: str, src_code: str, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', partial=False):
        if meta is None:
            from .ObjectRegex.MetaInfo import MetaInfo
            meta = MetaInfo()

        if not meta:
            raise CheckConditionError("Meta Information not defined yet!")

        res = self.parse_func(tokens, meta=meta)
        print(res)

        if res is None or (not partial and len(tokens) != meta.count):
            max_fetched = meta.max_fetched
            try:
                where = tokens[max_fetched]
            except IndexError:
                where = tokens[max_fetched - 1]

            row = src_code.splitlines()[where.lineno]
            raise DSLSyntaxError(
                "{}{}{}{} ---- at file {} line {}"
                    .format(Colored.Green, row[:where.colno], Colored.Red, row[where.colno:],
                            filename, where.lineno + 1))
        return res
