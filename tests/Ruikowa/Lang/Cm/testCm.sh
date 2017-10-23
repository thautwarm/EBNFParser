ruiko grammar ./parser.py -comment True
python testLang.py statements "
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
" -o cmlang-example
