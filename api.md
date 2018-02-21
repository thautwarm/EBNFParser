# API

## API Usage

See an [example codes](https://github.com/thautwarm/EBNFParser/blob/master/tests/Ruikowa/Lang/Lisp/test_api.py) about using the lisp parser in your Python codes.

- Tips: Raise Errors with details(line number and filename).
```python
from Ruikowa.ErrorFamily import handle_error
from your_parser_module import top_parser, token
parser = handle_error(top_parser)
codes = "your codes"
tokenized = token(codes)
ast = parser(tokenized, MetaInfo(fileName='this_file'), partial=False)
```
An error might occur if there is something wrong with your input codes, and it will be displayed like:
```
Syntax Error at <filename, 'this_file'> row <the line of the error>:
   Error startswith: 
   <some of your codes>
```

- AST

An instance of class `AST` performs like a `list` with name.
```
>> ast
Expr[
    "add"
]
>> len(ast)
1
>> ast.name
'Expr'
>> ast[0]
'add'
```

What's more, AST has meta informations with itself:
```
>> ast.meta
(1, 3, "test.lisp")
# which means (<line number>, <currrent number of tokenized words>, <filename>)
```


## Document

To be continue...   
