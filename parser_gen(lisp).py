
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
import re
namespace     = globals()
recurSearcher = set()
token = re.compile('|'.join(['\)','\(','[\w|\W]+']))
expr = AstParser([Ref('anystr')],[Ref('lp'),SeqParser([Ref('expr')]),Ref('rp')], name = 'expr')
anystr = LiteralParser('[\w|\W]+', name = 'anystr')
lp = LiteralParser.Eliteral('(', name = 'lp')
rp = LiteralParser.Eliteral(')', name = 'rp')
expr.compile(namespace, recurSearcher)
