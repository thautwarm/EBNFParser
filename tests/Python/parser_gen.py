
from Misakawa.Bootstrap.Parser import *
from Misakawa.ObjectRegex.Node import MetaInfo, Ast
from Misakawa.ErrorFamily import handle_error
from Misakawa.Bootstrap.Ast import ast_for_stmts
from Misakawa.Bootstrap.Compile import compile as bootstrap_comp
def go():
    with open('../bootstrap.ebnf') as f:
        lex = f.read()
    bootstrap_comp(lex, '')
    tokens = token.findall(lex)
    parser = handle_error(Stmt.match)
    res = parser(tokens, partial=False)
    print(res)
    return res
with open('../bootstrap.ebnf') as f:
        lex = f.read()
s= bootstrap_comp(lex, '')
with open('../parser_gen(bootstrap).py','w') as f:f.write(s)
def grpFunc(stmt : Ast):
   return  _newline if stmt.name == 'NEWLINE' else  \
           _literal_eq if stmt[2].name == 'Str' else \
           _compose_eq
