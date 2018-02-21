cd Lisp/
ruiko grammar ./parser.py -comment True
python testLang.py Stmt "
	(+ 1 2)
" -o test
