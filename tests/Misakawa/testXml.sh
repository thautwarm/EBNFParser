parserGenerator tests/Python/Lang/Xml/grammar tests/Python/Lang/Xml/parser.py -test True -multiline True

python tests/Python/Lang/Xml/testLang.py Module "<html> x+1 </html>" -o tests/Python/Lang/Xml/Simple -testTk True
python tests/Python/Lang/Xml/testLang.py Module "
<top>
<x>
x+1
</x>
</top>

<a>
sss
<d> </d>
</a>
" -o tests/Python/Lang/Xml/RecursiveTag -testTk True
