from Ruikowa.ObjectRegex.ASTDef import Ast
from Ruikowa.ErrorHandler import ErrorHandler
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from Ruikowa.ObjectRegex.Tokenizer import Tokenizer

from lisp_parser import Stmts, token_table

import typing as t

def token_func(src_code: str) -> t.Iterable[Tokenizer]:
    return Tokenizer.from_raw_strings(src_code, token_table, ({"space"}, {}))

parser = ErrorHandler(Stmts.match, token_func)

def parse(filename: str) -> Ast:

    return parser.from_file(filename)


print(parse("test.lisp"))