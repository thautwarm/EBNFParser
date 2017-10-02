# cd Python/
# export PYTHONPATH="../Python"
export PYTHONPATH="Python"
python tests/Python/test.py
python tests/Python/test_bootstrap.py
python tests/Python/test_expy.py
python tests/Python/parser_gen.py
python tests/Python/test_lisp.py
python Python/parserGenerator.py tests/Python/Lang/Lisp/grammar tests/Python/Lang/Lisp/parser.py
python tests/Python/Lang/Lisp/testLang.py "(set r 1) (define a b (+ a (+ r 1)))"

# python 部分语法的parser. 见 /tests/Python/Lang/Python/grammar
python Python/parserGenerator.py tests/Python/Lang/Python/grammar tests/Python/Lang/Python/parser.py
python tests/Python/Lang/Python/testLang.py "lambda x,y : x+y and 2"
python tests/Python/Lang/Python/testLang.py "lambda x,y : lambda z : x + y + z"


