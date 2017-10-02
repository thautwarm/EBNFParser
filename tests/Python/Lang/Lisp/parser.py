
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
import re
namespace     = globals()
recurSearcher = set()
token = re.compile('|'.join(['\)','\(','[\w\\\+\*\-]+','\n']))
Expr = AstParser([Ref('Liter')],[Ref('Left'),SeqParser([Ref('Expr')]),Ref('Right')], name = 'Expr')
Stmt = AstParser([SeqParser([SeqParser([Ref('NEWLINE')]),SeqParser([Ref('Expr')], atleast = 1),SeqParser([Ref('NEWLINE')])])], name = 'Stmt')
Liter = LiteralParser('[\w\\\+\*\-]+', name = 'Liter')
Left = LiteralParser.Eliteral('(', name = 'Left')
Right = LiteralParser.Eliteral(')', name = 'Right')
NEWLINE = LiteralParser('\n', name = 'NEWLINE')
Expr.compile(namespace, recurSearcher)
Stmt.compile(namespace, recurSearcher)
