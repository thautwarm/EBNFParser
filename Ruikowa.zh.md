EBNFParser 使用的EBNF方言简介。  
版本适用: EBNFParser 1.1及以前的版本。    
平白地描述这些知识，然后你能解决一切上下文无关文法的Parser.

从示例中学习对很多朋友是非常有效的，所以我放上`Lisp`和`Cm`的Grammar:
[Lisp](https://github.com/thautwarm/EBNFParser/blob/master/tests/Ruikowa/Lang/Lisp/grammar),
[Cm](https://github.com/thautwarm/EBNFParser/blob/master/tests/Ruikowa/Lang/Cm/grammar).

# 基本语法

- `:=`  
定义一个字面量的引用(如果不追求极限效率，可以完全不使用它，仅仅使用`::=`即可)。
    ```
    a := 't';
    
    b ::= a;
    ```
    在以上情形下, `b ::= a`和 `b ::= 't'`等价，`:=`理解为一个记号。

- `::=`  
    定义一个语法。

    ```
    a ::= '(' 'word'* ')' ;
    ```

    这样一个语法可以匹配如下词组(此处以空格分词)
    ```
    1. ( word word word )
    2. ( )
    ```

- `;`  
    之前你应该已经看见了，这个就是一个等式的结尾标志。  
    示例:

    ```
    a ::= b c d | e f g ;
    b ::= h i j;
    ```

- `*`  

    表示一个匹配可以进行**0**到**+∞**次。  
    见上面的 `a ::= '(' 'word' ')' ;`

- `+`  

    类似`*`, 表示一个匹配可以进行至少**1**, 至多**+∞**次。  

- `|`  

    匹配分支。  
    示例:
    ```
    a ::= b c d | e f g;
    ```
    表示语法`a`可以匹配两种可能性，分别是`a b c`和`e f g`。


- `(`  `)`  

    句中句。表示括号内是一个整体。  
    示例:
    ```
    a ::= 'b' 'c' 'd' ('e' 'f' 'g')+ 'h';
    ```
    以上语法能够匹配以下词组(此处以空格分词)
    ```
    b c d e f g h
    b c d e f g e f g h
    ```

- `[` `]`  

    句中句。同`(` `)`, 但是呢, 它表示方括号内匹配1次或0次。  
    示例:  
    ```
    a ::= 'b' ['c' | 'd'] e;
    ```
    以上语法可以匹配如下词组(此处以空格分词)
    ```
    b e
    b c e
    b d e
    ```
- `{` `}`  

    示例1 
    ```
    a = 'b'{2}
    ```
    表示至少匹配`'b'`字符两次。  

    示例2
    ```
    a ::= ('b' 'c' | 'c'){2, 3};
    ```
    表示匹配`'b' 'c' | 'c'`部分**2**到**3**次。
    

# 扩展

- 字面量前缀标注  

    使用正则表达式 : `R'<RegExp>'`

    ```
    Name ::= R'[a-zA-Z][a-zA-Z_0-9]*'; # 一般语言的变量名
    ```

    EBNFParser对于单个字符的parse有专门的优化，你可以这样使用。
    ```
    SingleA := C'A' ;
    Newline := C'\n';   # \x 是单字符哦:)
    ```


- Automatic Tokenizer  

    EBNFParser可以根据你文法中涉及到字面量自动生成tokenizer, 也可以自定义token函数:
    (`token(string:str)->List[str]`

    EBNFParser可以将非正则定义的token正确的组合起来。  
    对非正则串， 在token时不会存在永远被访问不到的情形，如下

    ```
    a ::= L't' | L'tt';
    ```

    以上情况下，**如果不对`t`和`tt`参与tokenizer生成的顺序做调整**，那么所有的tt都会被分成两个`t`, 也就是说你将永远得不到`tt`这个词！  
    好在EBNFParser自动的帮你解决了这个冲突。  
    不过也不是万能的，因为面对正则表达式的时候，这个问题依旧存在。
    ```
    a ::=  R'\w' | R'\w+\.\w+';
    ```
    显然，如果像上面这样定义，你永远不会得到`A.B`这样一个词，你需要这样写。
    ```
    a ::=  R'\w+\.\w+' | R'\w';
    ```

    **进阶提示**: 使用字符前缀控制自动token。
    ```
    a := K'keyword1';
    b := K'regex::\w+';
    c := L'keyword2';
    d := C'x';
    e := R'\w+';
    ``` 
    以上定义了五个字面量parser, 其中对生成tokenizer有贡献的是`c, d, e`。   
    其中
    - `C`前缀表示对单字符字面量parser进行优化。影响auto token. 
    - `L`前缀定义原始字面量parser。影响auto token。  
    - `R`表示定义正则字面量parser。影响auto token。
    - `K`前缀表示定义只用于匹配，不影响auto token。`K'regex::xxx'`表示使用正则匹配。
    - 无前缀默认转换为`K`前缀。
    
    上述的`a`定义的一个原始字面量parser只能用于匹配，同理，`b`定义的正则字面量parser也不会对自动分词有影响。
    
    


- Custom Tokenizer  
 
    如果不能定做奇怪的、上下文有关的tokenizer, 那实在是有些遗憾。  
    我自然不想要遗憾...  
    在grammar文件的第一行，可以定义Tokenizer
    ```
    Token {{lambda string:list(string)}}
    ```
    或者
    ```python
    Token {{
    toListLike = lambda func: lambda arg: list(func(arg))
    @toListLike
    def token(string):
        ...
        for ch in string:
            if ...:
                yield ch
            ...
        ...
    }}
    ```
    
    你也可以把token定义写在别的文件里，比如在grammar所在目录下，token文件夹的test.py文件里。  
    ```
    grammar
    token\
        test.py
    ```

    然后grammar里面这样写:
    ```
    Token token.test
    ```
    此处句末可不加分号...

- 忽略部分parsed结果  

    ```
    a Throw ['\n', b] ::= c b d '\n';
    ```
    得到的结果只是`c d`，**能够忽略的**只有**AST和非正则定义的字面量**(看官可以想一下: 如果支持忽略正则，会明显影响性能


## 如何使用自动生成的Parser

- 见[API简介](https://github.com/thautwarm/EBNFParser/blob/master/api.md)  
- [简短而完整的示例](https://github.com/thautwarm/EBNFParser/blob/master/tests/Ruikowa/Lang/Lisp/test_api.py)








    















    


