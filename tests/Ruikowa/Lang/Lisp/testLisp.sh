cd Lisp/
ruiko ./grammar ./pparser.py
python ./test_lang.py Stmt "
    (+ 1 2) as we can
" -o test.json --testTk