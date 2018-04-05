About Parser
=======================


EBNFParser is a parser generator framework to parse raw string into structured AST.

Pasring of EBNFParser has following steps:

Tokenizing
---------------

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

- parsing_tokenizing.ruiko

.. code :: shell

    MyTokenType  := 'abc' '233';
    # The above syntax defines a literal parser to parse strings like "abc" or "233".
    # "abc", "233" will be added into `token_table` to generate automatical tokenizing function.
    
    parserToTest ::= MyTokenType+;
    # The above syntax defines a combined parser with `MyTokenType`.
    
    # A combined parser is combined by several literal parsers and other combined parsers,
    #   which can handle very complicated cases of a sequence of `Ruikowa.ObjectRegex.Tokenizer` objects.    

- compile it

.. code :: shell

    ruiko parsing_tokenizing.ruiko parsing_tokenizing.py --test

- test it

.. code :: shell

    python test_lang.py parserToTest "abc233233"
    =========================ebnfparser test script================================ 
    parserToTest[
        [name: MyTokenType, string: "abc"]
        [name: MyTokenType, string: "233"]
        [name: MyTokenType, string: "233"]
    ]

Take care that if you're using anonymous literal pattern when definining a combined parser like the following:

.. code :: 

    Just ::= 'just';



CastMap(Optional)
------------------------

Sometimes we need special cases, a vivid instance is :code:`keyword` .

The string content of a :code:`keyword` could be also matched 
by :code:`identifier` (in most programming languages we have identifiers),
just as the following case:

- parsing_CastMap.ruiko

.. code ::


    ignore [space]
    space        := R'\s+';
    # ignore the whitespace characters.

    
    identifier   := R'[a-zA-Z_]{1}[a-zA-Z_0-9]*';
    keyword      := 'def' 'for' 'public';

    parserToTest ::= (identifier | keyword)+;

There is no doubt that :code:`identifier` will cover the cases of :code:`keyword`

.. code :: shell

    ruiko parsing_CastMap.ruiko parsing_CastMap.py --test
    python test.py parserToTest "def for public"
    =========================ebnfparser test script================================ 
    parserToTest[
        [name: identifier, string: "def"]
        [name: identifier, string: "for"]
        [name: identifier, string: "public"]
    ] 


Take care that all of the Tokenizers have name **identifier**, not **keyword** !
As as result, the keyword could be used in some illegal places, just like:

.. code ::
    
    for = 1
    for for <- [for] do
        for

The above example might not trouble you, but of course there could be something severer.

I'd like to give a solution adopted by EBNFParser auto-token.

(modify parsing_CastMap.ruiko

.. code ::

    identifier   := R'[a-zA-Z_]{1}[a-zA-Z_0-9]*';
    keyword cast := 'def' 'for' 'public';

Here we define a :code:`cast map` that will map the string tokenized by :code:`identifier`(like
:code:`"def"`, :code:`"for"` and :code:`"public"`) to a **const string**, and 
output a :code:`Ruikowa.ObjectRegex.Tokenizer` which name is a **const string** :code:`"keyword"`.

.. code :: shell

    ruiko parsing_CastMap.ruiko parsing_CastMap.py --test
    python test.py parserToTest "def for public other"
    =========================ebnfparser test script================================ 
     parserToTest[
        [name: keyword, string: "def"]
        [name: keyword, string: "for"]
        [name: keyword, string: "public"]
        [name: identifier, string: "other"]
    ] 


Perfect!


ReStructure Tokenizers
-----------------------------

This is what the word "parsing" accurately means.

Maybe you've heard about some sequence operation like 
:code:`flatMap` (Scala-flatMap_) , :code:`collect` (FSharp-collect_) , :code:`selectMany` (Linq-SelectMany_),
that's great, because parsing is its inverse!

.. code ::
    
    raw words : 
    
        ["def", "f", "(", "x", ")", "=", "x"]
    
    after parsing there is an AST:

        FunctionDef[ 
            "f"   
                  # "def" is thrown away because it's useless to semantics, but you can 
                  # preserve it, causing noises. The same below.
            ArgList[
                "x"
            ],

            Expression[
                "x"
            ]
        ]

And structures of the parsed just match what you defined with EBNF_. 

Here is an example to generate above AST by using a EBNF idiom - :code:`ruiko` 
which is proposed by EBNFParser to extend primary EBNF.

.. code :: ebnf

    keyword     cast as K       := 'def';
    identifier                  := R'[a-zA-Z_]{1}[a-zA-Z_0-9]*';
    FunctionDef throw ['def']   ::= K'def' identifier '(' ArgList ')' '=' Expression;
    Expression                  ::= ... # omit
    ArgList                     ::= ... # omit
    



EBNFParser supplies you a convenient way to use an EBNF idiom to   

.. _Scala-flatMap: https://www.scala-lang.org/api/current/?search=flatMap

.. _FSharp-collect: https://msdn.microsoft.com/en-us/visualfsharpdocs/conceptual/list.collect['t,'u]-function-[fsharp]

.. _Linq-SelectMany: https://msdn.microsoft.com/en-us/library/bb534336(v=vs.110).aspx

.. _EBNF: https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form

