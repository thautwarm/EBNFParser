test_lang_templates = (
    """
from Ruikowa.ErrorHandler import ErrorHandler
from Ruikowa.ObjectRegex.ASTDef import Ast
from Ruikowa.io import grace_open
from {} import *

import argparse, json

print('=========================ebnfparser test script================================')
def test():
    cmd_parser = argparse.ArgumentParser(description='test language parsers swiftly.')
    cmd_parser.add_argument("parser", type=str,
                           help='What kind of parser do you want to test with?(e.g Stmt, Expr, ...)')
    cmd_parser.add_argument("codes", metavar='codes', type=str,
                            help='input some codes in your own language here.')
    cmd_parser.add_argument('-o', nargs='?', help='output. support .json and .ast suffix.', type=str)
    cmd_parser.add_argument("-testTk", default=False, type=bool)

    args = cmd_parser.parse_args()
    print_token = args.testTk
    ast: Ast = ErrorHandler(eval(args.parser).match, token_func).from_source_code('<input>', args.codes, print_token=print_token)

    if args.o:
        o: str = args.o.lower()
        if o.endswith('.json'):
            grace_open(o).write(json.dumps(ast.dump_to_json(), indent=2))
        elif o.endswith('.ast'):
            grace_open(o).write(ast.dump())
        else:
            raise Exception('Unsupported file ext.')    
if __name__ == '__main__':
    test()
    """)

import os


def main():
    from .Bootstrap.Compile import compile as bootstrap_comp
    from .io import grace_open
    import argparse
    import sys, os
    cmdparser = argparse.ArgumentParser(description='using EBNFParser.')
    cmdparser.add_argument("InputFile", metavar='path of input file', type=str,
                           help='EBNF file which describes your language\'s grammar.')
    cmdparser.add_argument("OutputFile", metavar='path of output file', type=str,
                           help='generate python file(s) that makes a parser for your language.')
    cmdparser.add_argument('--test', nargs='?', help='make a script to test language parsers quickly?')

    args = cmdparser.parse_args()
    inp, outp = args.InputFile, args.OutputFile

    head_from, _ = os.path.split(sys.argv[0])
    head_to, __ParserFile__ = os.path.split(outp)

    generated_codes = bootstrap_comp(inp)
    path = os.path.join(head_to, outp)
    if path[-3:].lower() != '.py':
        path = '{}.py'.format(path)
    module = os.path.splitext(os.path.basename(outp))[0]
    grace_open('{}'.format(path)).write(generated_codes)
    grace_open('{}'
               .format(os.path.join(head_to, 'test_lang.py'))
               ).write(test_lang_templates.format(module))

    if __name__ == '__main__':
        main()
