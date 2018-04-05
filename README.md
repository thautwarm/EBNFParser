[![Build Status](https://travis-ci.org/thautwarm/EBNFParser.svg?branch=boating-new)](https://travis-ci.org/thautwarm/EBNFParser)
[![PyPI version](https://img.shields.io/pypi/v/EBNFParser.svg)](https://pypi.python.org/pypi/EBNFParser)
[![Release Note](https://img.shields.io/badge/note-release-orange.svg)](https://github.com/thautwarm/EBNFParser/blob/boating-new/Python/release-note)
[![MIT License](https://img.shields.io/badge/license-MIT-Green.svg?style=flat)](https://github.com/thautwarm/EBNFParser/blob/boating-new/LICENSE)

# EBNFParser
Parse Many, Any, Every [![Doc](https://img.shields.io/badge/document-2.1.2-yellow.svg?style=flat)](http://ebnfparser.readthedocs.io/en/boating-new)
-----------------------

```
LR ::= LR 'a' 'b' | LR 'c' | 'd';
```


- [Python Project(Support Python 3.6+)](https://github.com/thautwarm/EBNFParser/tree/boating-new/Python) (v 2.0+)
    - [Old Version : Misakawa v0.x](https://github.com/thautwarm/EBNFParser/tree/master/Misakawa.md)
    - [Old Version : Ruikowa v1.x](https://github.com/thautwarm/EBNFParser/tree/master/README.md)
 
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

## Usage 

- Command Line Tools
    - `ruiko`.

    ```shell
    ruiko ./<grammar File> ./<output filename>
            [--testTk] # print tokenized words or not
            [--test] # generate test script "test_lang.py"
    ```
    Use command `ruiko` to generate parser and token files, and then you can use `test_lang.py` to test your parser.

    ```shell
    python ./test_lang.py Stmt " (+ 1 2) " -o test.json --testTk
    ```

- Integrated into your own project

    ```python

        from Ruikowa.ObjectRegex.ASTDef import Ast
        from Ruikowa.ErrorHandler import ErrorHandler
        from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
        from Ruikowa.ObjectRegex.Tokenizer import Tokenizer

        from <your own generated parser module> import <top parser>, token_table


        import typing as t

        def token_func(src_code: str) -> t.Iterable[Tokenizer]:
            return Tokenizer.from_raw_strings(src_code, token_table, ({<the names of tokenizers you would ignore>}, {<the string contents of tokenizers you would ignore>}))

        parser = ErrorHandler(<top parser>.match, token_func)

        def parse(filename: str) -> Ast:

            return parser.from_file(filename)


        print(parse(<filename of your dsl source code>))

    ```

Need more? See [the documents](http://ebnfparser.readthedocs.io/en/boating-new).

## Examples:

Here are some examples to refer:  

EBNFParser 2.0

- [Rem](https://github.com/thautwarm/Rem)  
    The Rem programming language.


Old version(Before EBNFParser 1.1).  

- [DBG-Lang](https://github.com/thautwarm/dbg-lang)  
    A DSL for SQL development in Python areas.

- [Rem(Based EBNFParser1.1)](https://github.com/thautwarm/Rem/tree/backend-ebnfparser1.1)  
    A full featured modern language to enhance program readability based on CPython.

- [Lang.Red](https://github.com/thautwarm/lang.red)  
    An attempt to making ASDL in CPython(unfinished yet)

Will support F# and Rem.

    













