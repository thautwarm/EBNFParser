# 十分钟学会学写这样的编译器

# 用知乎里大家一致认为最垃圾python来写吧。
# 预先定义库函数
mul = lambda a, b : a*b
add = lambda a, b : a+b
sub = lambda a, b : a-b

# Misakawa是EBNFParser的一个实现，是我第二次重构后的版本。
from Misakawa.ErrorFamily import handle_error # 函数装饰器用来做智能错误提示
from parser import Expr # parser.py是parserGenerator根据语法文件自动生成的。
from token import token
parser = handle_error(Expr.match)
parse  = lambda codes : parser(token(codes), partial = False)
# 下面是代码生成
def astForExpr(expr):
    # Expr ::= Atom | Quote | '('  Expr*  ')' 
    if len(expr) is 1:
       if expr[0].name == 'Quote': # 文中没涉及我们就暂不谈咯
            return ...
       else :
            return eval(expr[0].value) 
            # 如果不用eval自然没有问题，
            # 但是你需要判断是怎样的Atom, 是数字，是字符串，还是符号等。
    else:
       length = len(expr)
       if length is 2:
         # Expr = '(' ')'
         return list()
       else:
         exprlist = [astForExpr(maybeAtom) for maybeAtom in  expr[1:-1]]
         return exprlist[0](*exprlist[1:])
