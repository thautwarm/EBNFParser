if False:
    from .ObjectRegex.MetaInfo import MetaInfo
    from typing import Sequence, Optional
    from .ObjectRegex.Tokenizer import Tokenizer
from .ErrorFamily import *
from pprint import pprint


class ErrorHandler:

    def __init__(self, parse_func, token_func=None):
        self.parse_func = parse_func
        self.token_func = token_func

    def mut_parser_by(self, new_func):
        self.parse_func = new_func(self.parse_func)

    def mut_token_by(self, new_func):
        self.token_func = new_func(self.token_func)

    def from_file(self, filename: str, meta: 'MetaInfo' = None, partial=False, print_token=False):
        with open(filename, 'r', encoding='utf8') as f:
            raw_string = f.read()
        return self.from_source_code(filename, raw_string, meta, partial, print_token)

    def from_source_code(self, filename: str, src_code: str, meta: 'MetaInfo' = None, partial=False, print_token=False):
        tokens: 'Sequence[Tokenizer]' = tuple(self.token_func(src_code))
        if print_token:
            pprint(tokens)
        return self.from_tokens(filename, src_code, tokens, meta, partial)

    def from_tokens(self, filename: str, src_code: str, tokens: 'Sequence[Tokenizer]', meta: 'MetaInfo', partial=False):
        if meta is None:
            from .ObjectRegex.MetaInfo import MetaInfo
            meta = MetaInfo(fileName=filename)

        if not meta:
            raise CheckConditionError("Meta Information not defined yet!")

        res = self.parse_func(tokens, meta=meta)
        if res is None or (not partial and len(tokens) != meta.count):
            max_fetched = meta.max_fetched
            try:
                where = tokens[max_fetched]
            except IndexError:
                for i in range(max_fetched - 1, meta.count, -1):
                    try:
                        where = tokens[i]
                        break
                    except:
                        continue
                else:
                    raise DSLSyntaxError(
                        f"totally wrong syntax!(first word has been wrong!)")

            row = src_code.splitlines()[where.lineno]
            raise DSLSyntaxError(
                "{}{}{}{} ---- at file {} line {}{}"
                    .format(Colored.Green, row[:where.colno - 1], Colored.Red,
                            row[where.colno - 1:],
                            filename, where.lineno + 1, Colored.Clear))
        return res
