
# This file is automatically generated by EBNFParser.
import argparse, json

cmd_parser = argparse.ArgumentParser(description='test language parsers swiftly.')
cmd_parser.add_argument("parser", type=str,
                       help='What kind of parser do you want to test with?(e.g Stmt, Expr, ...)')
cmd_parser.add_argument("codes", metavar='codes', type=str,
                        help='input some codes in your own language here.')
cmd_parser.add_argument('-o', help='output. support .json and .ast suffix.', type=str)
cmd_parser.add_argument("--testTk", nargs='?', default=False, const=True)
cmd_parser.add_argument('--debug', nargs='?', default=False, const=True,
                       help='print tokens of grammar file?')

args = cmd_parser.parse_args()
                       
if args.debug:
    from Ruikowa.Config import Debug
    Debug.append(1)         
    
from Ruikowa.ErrorHandler import ErrorHandler, Colored
from Ruikowa.ObjectRegex.ASTDef import Ast
from Ruikowa.io import grace_open
from lisp_parser import *              
print(Colored.Green,'=========================ebnfparser test script================================', Colored.Clear)

print_token = args.testTk
ast: Ast = ErrorHandler(eval(args.parser).match, token_func).from_source_code('<input>', args.codes, print_token=print_token)
print(Colored.Blue, ast, Colored.Clear)
if args.o:
    o: str = args.o.lower()
    if o.endswith('.json'):
        grace_open(o).write(json.dumps(ast.dump_to_json(), indent=2))
    elif o.endswith('.ast'):
        grace_open(o).write(ast.dump())
    else:
        raise Exception('Unsupported file ext.')    

    