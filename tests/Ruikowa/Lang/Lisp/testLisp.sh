cd Lisp/
misakawa ./grammar ./pparser.py
python ./test_lang.py Stmt "
    (+ 1 2)
" -o test.json

python ./test_lang.py Stmt "
    (+ 1 2)
" -o test.ast