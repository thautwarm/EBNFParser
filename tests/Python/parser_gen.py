
from Misakawa.Bootstrap.Parser import *
from Misakawa.ObjectRegex.Node import MetaInfo, Ast
from Misakawa.ErrorFamily import handle_error
from Misakawa.Bootstrap.Ast import ast_for_stmts
from Misakawa.Bootstrap.Compile import compile as bootstrap_comp
with open('bootstrap.ebnf') as f:
        lex = f.read()
s= bootstrap_comp(lex, '')
with open('parser_gen(bootstrap).py','w') as f:f.write(s)

