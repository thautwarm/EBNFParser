
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
from token import token 
import re
namespace     = globals()
recurSearcher = set()
Expr = AstParser([Ref('Atom')],[Ref('Quote')],[LiteralParser.Eliteral('(', name = '\'(\''),SeqParser([SeqParser([Ref('NEWLINE')]),SeqParser([Ref('Expr')]),SeqParser([Ref('NEWLINE')])]),LiteralParser.Eliteral(')', name = '\')\'')], name = 'Expr', toIgnore={'NEWLINE'})
Quote = AstParser([LiteralParser.Eliteral('`', name = '\'`\''),Ref('Expr')], name = 'Quote')
Atom = LiteralParser('[^\(\)\s]+', name = 'Atom')
NEWLINE = LiteralParser('\n', name = 'NEWLINE')
Stmt = AstParser([SeqParser([SeqParser([Ref('NEWLINE')]),SeqParser([Ref('Expr')]),SeqParser([Ref('NEWLINE')])])], name = 'Stmt', toIgnore={'NEWLINE'})
Expr.compile(namespace, recurSearcher)
Quote.compile(namespace, recurSearcher)
Stmt.compile(namespace, recurSearcher)
