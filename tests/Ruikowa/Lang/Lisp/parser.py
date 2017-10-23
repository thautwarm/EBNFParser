
from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo, DependentAstParser
from etoken import token 
import re
namespace     = globals()
recurSearcher = set()
Atom = LiteralParser('[^\(\)\s\`]+', name = 'Atom', isRegex = True)
Expr = AstParser([Ref('Atom')],[Ref('Quote')],[CharParser('(', name='\'(\''),SeqParser([SeqParser([Ref('NEWLINE')]),SeqParser([Ref('Expr')]),SeqParser([Ref('NEWLINE')])]),CharParser(')', name='\')\'')], name = 'Expr', toIgnore = [set(), {"'\\n'"}])
Quote = AstParser([CharParser('`', name='\'`\''),Ref('Expr')], name = 'Quote')
NEWLINE = CharParser('\n', name = 'NEWLINE')
Stmt = AstParser([SeqParser([SeqParser([Ref('NEWLINE')]),SeqParser([Ref('Expr')]),SeqParser([Ref('NEWLINE')])])], name = 'Stmt', toIgnore = [set(), {"'\\n'"}])
Expr.compile(namespace, recurSearcher)
Quote.compile(namespace, recurSearcher)
Stmt.compile(namespace, recurSearcher)
