# 十分钟学会学写这样的编译器

# 用知乎里大家一致认为最垃圾python来写吧。
# 预先定义库函数
mul = lambda a, b : a*b
add = lambda a, b : a+b
sub = lambda a, b : a-b

# Misakawa是EBNFParser的一个实现，是我第二次重构后的版本。
from Misakawa.ErrorFamily import handle_error # 函数装饰器用来做智能错误提示
from Misakawa.ObjectRegex import Ast
from parser import Expr # parser.py是parserGenerator根据语法文件自动生成的。
from etoken import token
parser = handle_error(Expr.match)
parse  = lambda codes : parser(token(codes), partial = False)
# 下面是代码生成
def defFun(ast, *formalArgs, area):
    def __call__(*realArgs):
        newArea = area.copy()
        newEnv = dict(zip(formalArgs, realArgs))
        newArea.update(newEnv)
        return  astForExpr(ast, newArea)
    return __call__

def setq(x, ast, area):
    area[x] = astForExpr(ast, area)
    return area[x]

def parserArgName(expr):
    return [arg[0].value for arg in expr[1:-1]]

def astForExpr(expr, area):
    # Expr ::= Atom | Quote | '('  Expr*  ')' 
    if len(expr) is 1:
       if expr[0].name == 'Quote': # 文中没涉及我们就暂不谈咯
            return expr[0][1]
       else :
            ret =  eval(expr[0].value, area) 
            if ret.__class__ is Ast:
                return astForExpr(ret, area)
            return ret
            # 如果不用eval自然没有问题，
            # 但是你需要判断是怎样的Atom, 是数字，是字符串，还是符号等。
    else:
        length = len(expr)
        if length is 2:
            # Expr = '(' ')'
            return list()
        else:
            expr = expr[1:-1]
            keywordTest = expr[0]
            if keywordTest[0].name == 'Atom' and keywordTest[0].value == 'def':
                arglist = ()
                try:
                    assert length is 6
                    name, arglist, ast = expr[1][0].value, parserArgName(expr[2]), expr[3]
                except:
                    assert length is 5
                    name, ast = expr[1][0].value,  expr[2]
                new = {name: defFun(ast, *arglist, area=area)}
                area.update(new)
                return new[name]
            elif keywordTest[0].name == 'Atom' and keywordTest[0].value == 'setq':
                assert length is 5
                return setq(expr[1][0].value, expr[2],  area)
                
            else:
                exprlist = [astForExpr(maybeAtom, area) for maybeAtom in  expr]
                return exprlist[0](*exprlist[1:])
     
area = dict(mul = mul, add = add, sub = sub)
while True:
    string = input('>> ')
    if string == ':q': break
    print('=> ', astForExpr(parse(string), area))