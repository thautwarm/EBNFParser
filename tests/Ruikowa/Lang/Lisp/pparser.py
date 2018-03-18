from Ruikowa.ObjectRegex.Tokenizer import unique_literal_cache_pool, regex_matcher, char_matcher, str_matcher, Tokenizer
from Ruikowa.ObjectRegex.Node import AstParser, Ref, SeqParser, LiteralValueParser, LiteralNameParser, Undef
namespace = globals()
recur_searcher = set()
token_table = ((unique_literal_cache_pool["N"], regex_matcher('\n')),
               (unique_literal_cache_pool["N"], regex_matcher('\t')),
               (unique_literal_cache_pool["N"], char_matcher((' '))),
               (unique_literal_cache_pool["Atom"], regex_matcher('[^\(\)\s\`]?')),
               (unique_literal_cache_pool[":char"], char_matcher(('`', ')', '('))))

class UNameEnum:
    N = unique_literal_cache_pool["N"]
    N = unique_literal_cache_pool["N"]
    Atom = unique_literal_cache_pool["Atom"]
        
token_func = lambda _: Tokenizer.from_raw_strings(_, token_table, ({"N"}, {}))
N = LiteralNameParser('N')
N = LiteralNameParser('N')
N = LiteralNameParser('N')
Atom = LiteralNameParser('Atom')
Expr = AstParser([Ref('Atom')],
                 [Ref('Quote')],
                 ['(', SeqParser([Ref("Expr")], at_least=0, at_most=Undef), ')'],
                 name="Expr",
                 to_ignore=({}, {}))
Quote = AstParser(['`', Ref('Expr')],
                  name="Quote",
                  to_ignore=({}, {}))
Stmt = AstParser([SeqParser([Ref("Expr")], at_least=0, at_most=Undef)],
                 name="Stmt",
                 to_ignore=({}, {}))
Stmt.compile(namespace, recur_searcher)