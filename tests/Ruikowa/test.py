
from Ruikowa.ObjectRegex.Node import Ast, Ref, LiteralParser, CharParser, SeqParser, AstParser
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from Ruikowa.Core.BaseDef import Trace
inputs = ['a', '\n', 'abc']
charParser1 = CharParser('a')
charParser2 = CharParser('\n')
litParser   = LiteralParser.RawFormDealer(rawStr='abc', name = 'ABC')
meta = MetaInfo()
assert charParser1.match(inputs, meta) is 'a'
assert litParser.match(inputs, meta)   is None
assert charParser2.match(inputs, meta) is '\n'
assert litParser.match(inputs, meta)   == 'abc'

a = LiteralParser('a', name = 'a')
c = LiteralParser('c', name = 'c')
d = LiteralParser('d', name = 'd')
ASeq = AstParser([Ref('U'), d],[a], name = 'ASeq')
U    = AstParser([Ref('ASeq'), c],  name = 'U')
namespace = globals()
seset     = set()
ASeq.compile(namespace, seset)
x = MetaInfo()
print(ASeq.match(['a', 'c','d','c','d','k'], x))


a = LiteralParser('a', name = 'a')
c = LiteralParser('c', name = 'c')
d = LiteralParser('d', name = 'd')
ASeq = AstParser([Ref('ASeq'), d],[a], name = 'ASeq')
#U    = AstParser([Ref('ASeq'), c],  name = 'U')
namespace = globals()
seset     = set()
ASeq.compile(namespace, seset)
x = MetaInfo()
print(ASeq.match(['a', 'd','d','d','d','d','g'], x).dump_to_json())




