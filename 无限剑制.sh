export PYTHONPATH="Python"
python Python/parserGenerator.py tests/Python/Lang/文言/grammar tests/Python/Lang/文言/parser.py -test True -comment True

python tests/Python/Lang/文言/testLang.py 语句 "[吾身]作为剑所[天成]。" -o tests/Python/Lang/文言/吾身乃剑所天成 -testTk True

python tests/Python/Lang/文言/testLang.py 语句 "血作为[铁潮];心作为[琉璃]。" -o tests/Python/Lang/文言/血潮为铁，心为琉璃

python tests/Python/Lang/文言/testLang.py 语句 "[跨越][无数战场];立于[不败之地]。" -o tests/Python/Lang/文言/跨越无数战场，立于不败之地
python tests/Python/Lang/文言/testLang.py 语句 "未曾[败退]。" -o tests/Python/Lang/文言/未曾败退
python tests/Python/Lang/文言/testLang.py 语句 "无一作为[知己]。" -o tests/Python/Lang/文言/无一知己

python tests/Python/Lang/文言/testLang.py 语句 "常独自[一人]立于[剑丘];[陶醉]于[胜利]。"  -o tests/Python/Lang/文言/常孤身沉醉于剑丘之上，陶醉于胜利之中。

python tests/Python/Lang/文言/testLang.py 语句 "因此[他的][一生]([失去][意义])于[已然]。"  -o tests/Python/Lang/文言/故其之一生，没有意义

python tests/Python/Lang/文言/testLang.py 语句 "如所[期许]，[此身]作为[无限剑制]。" -o tests/Python/Lang/文言/此身定为无限剑制



