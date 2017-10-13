parserGenerator tests/Python/LR/lr tests/Python/LR/lrTestParser.py 


python tests/Python/LR/testLang.py prefix "t(t)(t)" -o tests/Python/LR/test1  

python tests/Python/LR/testLang.py prefix "t(t)=>t(t)(t)" -o tests/Python/LR/test2


