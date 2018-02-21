from Ruikowa.ErrorFamily import handle_error
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from my_parser import token
from my_parser import Stmt

parser = handle_error(Stmt)
codes = """
(add 1 (add 2 3))
(set a 1)
"""
filename = 'test.lisp'
tokenized = token(codes)

ast = parser(tokenized, meta = MetaInfo(fileName=filename), partial=False)
# partial: decide whether to parse partially. Mark it as True when you're making a repr.

print(ast[0][1])
# Expr[
#     "add"
# ]

print(ast[0][1].name)  # Expr

print(ast[0])
# Expr[
#     "("
#     Expr[
#         "add"
#     ]
#     Expr[
#         "1"
#     ]
#     Expr[
#         "("
#         Expr[
#             "add"
#         ]
#         Expr[
#             "2"
#         ]
#         Expr[
#             "3"
#         ]
#         ")"
#     ]
#     ")"
# ]

print(ast[0].name)
# Expr

print(ast.name)
# Stmt

print(ast)
# Stmt[
#     Expr[
#         "("
#         Expr[
#             "add"
#         ]
#         Expr[
#             "1"
#         ]
#         Expr[
#             "("
#             Expr[
#                 "add"
#             ]
#             Expr[
#                 "2"
#             ]
#             Expr[
#                 "3"
#             ]
#             ")"
#         ]
#         ")"
#     ]
#     Expr[
#         "("
#         Expr[
#             "set"
#         ]
#         Expr[
#             "a"
#         ]
#         Expr[
#             "1"
#         ]
#         ")"
#     ]
# ]