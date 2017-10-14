
from Ruikowa.ObjectRegex.Node import LiteralParser, CharParser
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
inputs = ['a', '\n', 'abc']
charParser1 = CharParser('a')
charParser2 = CharParser('\n')
litParser   = LiteralParser.RawFormDealer(rawStr='abc', name = 'ABC')
meta = MetaInfo()
assert charParser1.match(inputs, meta) is 'a'
assert litParser.match(inputs, meta)   is None
assert charParser2.match(inputs, meta) is '\n'
assert litParser.match(inputs, meta)   == 'abc'
