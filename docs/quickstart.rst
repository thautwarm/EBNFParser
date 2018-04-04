Quick Start
================



Installing
--------------------------------

The EBNFParser only supports Python 3.6+ now.

You can install it by using **PyPI**.

.. code :: shell

    pip install -U EBNFParser



Hello World
--------------------------------

We can try to parse Lisp grammar syntax into AST(Abstract Synatx Tree) as our first attempt.

.. code :: lisp 

    (define add3 (x y z) 
              (add x
                  (add y z)))


Here is a source code example:

- lisp.ruiko

.. code ::

   ignore [space]  # ignore the tokens with this(these) name(s).

    space   := R'\s';

    Atom    := R'[^\(\)\s\`]+'; # use Regex

    Expr    ::= Atom
            | Quote
            | '(' Expr* ')';


    Quote   ::=  '`' Expr ;

    Stmts   ::= Expr*;

And then use it to generate a parser and make a test script automatically by EBNFParser.

Finally, test it.

.. code ::

    ruiko lisp.ruiko lisp_parser.py --test
    python test_lang.py Stmt "(definie f (x y z) (add (add x y) z))"



Integrate EBNFParser Into Your Own Project
---------------------------------------------

For example, if we have generated the lisp parser file like the above as a module `MyProject.Lisp.parser`.

.. code :: python

    from Ruikowa.ObjectRegex.ASTDef import Ast
    from Ruikowa.ErrorHandler import ErrorHandler
    from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
    from Ruikowa.ObjectRegex.Tokenizer import Tokenizer

    from lisp_parser import Stmts, token_table

    import typing as t

    def token_func(src_code: str) -> t.Iterable[Tokenizer]:
        return Tokenizer.from_raw_strings(
            src_code, token_table, ({"space"}, {}))

    parser = ErrorHandler(Stmts.match, token_func)

    def parse(filename: str) -> Ast:

        return parser.from_file(filename)

    # just create a file `test.lisp` and write some lisp codes.
    print(parse("./test.lisp"))  
    


An :code:`Ruikowa.ObjectRegex.Ast` is a nested list of Tokenizers, for instance:

.. code ::

    AstName[
        AstName[
            Tokenizer1
            Tokenizer2
            AstName[
                ...
            ]
        ]
        Tokenizer3
    ]

You can use :code:`obj.name` to get the name of an instance of :code:`Ast` or :code:`Tokenizer`.




