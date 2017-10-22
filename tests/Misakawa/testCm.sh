# Cm lang
parserGenerator tests/Python/Lang/Cm/grammar tests/Python/Lang/Cm/parser.py -test True -comment True -multiline True
python tests/Python/Lang/Cm/testLang.py statements "let s:int = 1;" -testTk True -o tests/Python/Lang/Cm/test1
python tests/Python/Lang/Cm/testLang.py statements "{}" -testTk True -o tests/Python/Lang/Cm/test2
python tests/Python/Lang/Cm/testLang.py statements "

var f : auto = (i:i32, inner:[i32 => i32])->{inner(i)}
f 2+1 i:auto-> 1+2
" -testTk True -o tests/Python/Lang/Cm/test3


python tests/Python/Lang/Cm/testLang.py statements "
var f : auto = (i:i32, inner:[i32 => i32])->{inner(i)};
f 2+1  i:auto-> 1+2 
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
<T> (x:i32)=>i32->x+1
" -o tests/Python/Lang/Cm/test4



