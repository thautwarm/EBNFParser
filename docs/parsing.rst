About Parsing
=======================


EBNFParser is a parser generator framework to parse raw string into structured AST. 

Steps
--------------

- Tokenizing

    Tokenizing is the very first step to split input string and 
    transform each to a :code:`Ruikowa.ObjectRegex.Tokenizer` object.
    
    A :code:`Ruikowa.ObjectRegex.Tokenizer` has the following **readonly** attributes:
    
    - name : str 
        type of the tokenizer. 
    - string : str 
        string content(from input raw string) of the tokenizer.
    - colno : int 
        column number in current file. 
    - lineno : int 
        row number in current file.

    Example:

    .. code ::

        MyTokenType  := 'abc' '233';

        parserToTest ::= MyTokenType+;




