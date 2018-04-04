[![Build Status](https://travis-ci.org/thautwarm/EBNFParser.svg?branch=boating-new)](https://travis-ci.org/thautwarm/EBNFParser)
[![PyPI version](https://img.shields.io/pypi/v/EBNFParser.svg)](https://pypi.python.org/pypi/EBNFParser)
[![Doc](https://img.shields.io/badge/docs-yellow.svg?style=flat)](http://ebnfparser.readthedocs.io/en/boating-new)
[![Release Note](https://img.shields.io/badge/note-release-orange.svg)](https://github.com/thautwarm/EBNFParser/blob/boating-new/Python/release-note)
[![MIT License](https://img.shields.io/badge/license-MIT-Green.svg?style=flat)](https://github.com/thautwarm/EBNFParser/blob/boating-new/LICENSE)

# EBNFParser
Parse Many, Any, Every
-----------------------
[HomePage](https://github.com/thautwarm/EBNFParser)

- [Python Project(Support Python 3.6+)](https://github.com/thautwarm/EBNFParser/tree/boating-new/Python) (v 2.0)
    - [Old Version : Misakawa(v0.x)](https://github.com/thautwarm/EBNFParser/tree/master/Misakawa.md)
    - [Old Version : Ruikowa(v1.x)](https://github.com/thautwarm/EBNFParser/tree/master/README.md)
 
--------------------

## Install
- Python
    - pip  

    `pip installl -U EBNFParser`
    
    - setup 
    ```shell
    git clone https://github.com/thautwarm/EBNFParser
    cd EBNFParser/Python
    python setup.py install
    ``` 


## An Introduce to EBNFParser

`EBNFParser` seems to be a parser framework for parsing EBNF syntaxes, however, 
the syntax of `EBNF` here is not the same as that standard one.  
The name of current EBNFParser's version  is `Ruikowa`, so you can call this idiom as `Ruikowa` for convenience' sake.

Here is an example for you to get a knowledge of `Ruikowa` for parsing Java `switch` syntax. 

```BNF

deftoken Token.Java # use the token definition at source file `./Token/Java`.

ignore [Space] # ignore tokens like Space;

Space    := R'\s+'; # define tokenizer(s) with specific name `Space`

switch   ::= 'switch' '(' expression ')' newline*
             '{'  
                case*
                [default]
             '}' ;

case     ::= 'case' ':' body    ;

default  ::= 'default' ':' body ;

body     ::= block | statement  ;

block    ::= '{' statement* '}' ;

...

```

Now I'm going to tell you how to use `EBNFParser` to write a parser for `Lisp` quickly.

- Install
    
    `pip install -U EBNFParser`


- Write a file and name it as `lispGrammar` with following content.

    ```BNF

    ignore [N]
    
    N := R'\n', R'\t', ' ';

    Atom    := R'[^\(\)\s\`]?'; # use Regex
    Expr  ::= Atom
            | Quote
            | '(' Expr* ')';

    Quote ::=  '`' Expr ;
    Stmt  ::= Expr*;

    ```

- Generate your parser and tokenizer.

    `ruiko ./lispGrammar ./lispParser.py`

- Test your parser.

    ```shell
    python testLang.py Stmt "(+ 1 2)" -o test.ast
    Stmt[
        Expr[
            "("
            Expr[
                "+"
            ]
            Expr[
                "1"
            ]
            Expr[
                "2"
            ]
            ")"
        ]
    ]
    ```

    Moreover, here is a result in `JSON` format at [test.json](https://github.com/thautwarm/EBNFParser/blob/boating-new/tests/Ruikowa/Lang/Lisp/test.json).

## Usage 

- Command Line Tools
    - `ruiko`.

    ```shell
    ruiko ./<grammar File> ./<output Python File(endswith ".py")>
            [--testTk] # print tokenized words or not
    ```
    Use command `ruiko` to generate parser and token files, and then you can use `testLang.py` to test your parser.

    ```shell
    python ./test_lang.py Stmt " (+ 1 2) " -o test.json --testTk
    ```

- Use `EBNFParser` in your own project.


Here are some examples to refer:  

EBNFParser 2.0

- [Rem](https://github.com/thautwarm/Rem)  
    The Rem programming language.

Before EBNFParser 1.1.  

- [DBG-Lang](https://github.com/thautwarm/dbg-lang)  
    A DSL for SQL development in Python areas.

- [Rem(Based EBNFParser1.1)](https://github.com/thautwarm/Rem/tree/backend-ebnfparser1.1)  
    A full featured modern language to enhance program readability based on CPython.

- [Lang.Red](https://github.com/thautwarm/lang.red)  
    An attempt to making ASDL in CPython(unfinished yet)



## Source

- [Source of Ruikowa](https://github.com/thautwarm/EBNFParser/tree/boating-new/Python/Ruikowa)
- [Core : Node.py](https://github.com/thautwarm/EBNFParser/tree/boating-new/Python/Ruikowa/ObjectRegex/Node.py)
- [Bootstrap Compiler](https://github.com/thautwarm/EBNFParser/tree/boating-new/Python/Ruikowa/Bootstrap)

Will support C# and Rem.

## License  
[MIT](./LICENSE)

    













