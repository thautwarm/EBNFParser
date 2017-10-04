export PYTHONPATH="Python"
# Lisp语法解析
python Python/parserGenerator.py tests/Python/Lang/Lisp/grammar tests/Python/Lang/Lisp/parser.py -test True
python tests/Python/Lang/Lisp/testLang.py Stmt "(set r 1) (define a b (+ a (+ r 1)))" 

#ExtraPy 语法解析
python Python/parserGenerator.py tests/Python/Lang/Expy/grammar tests/Python/Lang/Expy/parser.py -test True
#python tests/Python/Lang/Expy/testLang.py Stmt "def(){1+2}"
#python tests/Python/Lang/Expy/testLang.py Stmt "def(){ 1+2   f(2+3) }"
python tests/Python/Lang/Expy/testLang.py Stmt "
				def f1() {1+2   f2(2+3) }
				def f2() { 1 }
				tp = (1,)
				tp = (1, tp, tp)
				s  = def(x){ x+1 }
"

# EBNFParser 自省
python Python/parserGenerator.py tests/Python/Lang/EBNF/grammar tests/Python/Lang/EBNF/parser.py -test True
python tests/Python/Lang/EBNF/testLang.py Stmt "
		a ::= b | c | d | a [b c] | '(' a ')' 
		d ::= a+
"

# python 表达式部分的部分语法(除去了位运算)的parser. 见 /tests/Python/Lang/Python/grammar
python Python/parserGenerator.py tests/Python/Lang/Python/grammar tests/Python/Lang/Python/parser.py -test True
python tests/Python/Lang/Python/testLang.py Test "lambda x,y : x+y and 2"
python tests/Python/Lang/Python/testLang.py Test "lambda x,y : lambda z   : x + y + z"
python tests/Python/Lang/Python/testLang.py Test "lambda x,y : lambda z,d : x + y * (1+2)"

