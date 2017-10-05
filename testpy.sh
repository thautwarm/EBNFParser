export PYTHONPATH="Python"
# Lisp语法解析
python Python/parserGenerator.py tests/Python/Lang/Lisp/grammar tests/Python/Lang/Lisp/parser.py -test True
python tests/Python/Lang/Lisp/testLang.py Stmt "(set r 1) (define a b (+ a (+ r 1)))"  -o tests/Python/Lang/Lisp/test1

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
" -o tests/Python/Lang/Expy/test1

# EBNFParser 自省
python Python/parserGenerator.py tests/Python/Lang/EBNF/grammar tests/Python/Lang/EBNF/parser.py -test True
python tests/Python/Lang/EBNF/testLang.py Stmt "
		a ::= b | c | d | a [b c] | '(' a ')' 
		d ::= a+
" -o tests/Python/Lang/EBNF/test1

# python 表达式部分的部分语法(除去了位运算)的parser. 见 /tests/Python/Lang/Python/grammar
python Python/parserGenerator.py tests/Python/Lang/Python/grammar tests/Python/Lang/Python/parser.py -test True
python tests/Python/Lang/Python/testLang.py Test "lambda x,y : x+y and 2" -o tests/Python/Lang/Python/test1
python tests/Python/Lang/Python/testLang.py Test "lambda x,y : lambda z   : x + y + z" -o tests/Python/Lang/Python/test2
python tests/Python/Lang/Python/testLang.py Test "lambda x,y : lambda z,d : x + y * (1+2)" -o tests/Python/Lang/Python/test3

# Cm lang
python Python/parserGenerator.py tests/Python/Lang/Cm/grammar tests/Python/Lang/Cm/parser.py -test True -comment True -multiline True
python tests/Python/Lang/Cm/testLang.py statements "let s:int = 1;" -testTk True -o tests/Python/Lang/Cm/test1
python tests/Python/Lang/Cm/testLang.py statements "{}" -testTk True -o tests/Python/Lang/Cm/test2
python tests/Python/Lang/Cm/testLang.py statements "
var f : auto = i:i32, inner:[i32 => i32]->{inner(i)};
f 2+1 i:auto-> 1+2
" -testTk True -o tests/Python/Lang/Cm/test3


python tests/Python/Lang/Cm/testLang.py statements "
var f : auto = i:i32, inner:[i32 => i32]->{inner(i)};
f 2+1 i:auto-> 1+2
let f2 : [[i32=>i32]=>i32] = {
	g:auto -> 
		2*g(10)	
};
f2 {
   i:auto -> i*20
}
struct Some{
	a:i32
	f:[i32=>i32]
	g:[[i32=>i32]=>[i32=>i32]]
}
" -testTk True -o tests/Python/Lang/Cm/test4


