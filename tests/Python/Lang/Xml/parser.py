
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
import re
namespace     = globals()
recurSearcher = set()
token = re.compile('|'.join(['\n','\<[a-zA-Z_0-9\n]*?\>','\</[a-zA-Z_0-9\n]*?\>','[^\n]*?(?=\</[a-zA-Z_0-9\n]*?\>|\<[a-zA-Z_0-9\n]*?\>|\n)']))
Token = AstParser([LiteralParser('\n', name = '\'\n\'')],[LiteralParser('\<[a-zA-Z_0-9\n]*?\>', name = '\'\<[a-zA-Z_0-9\n]*?\>\'')],[LiteralParser('\</[a-zA-Z_0-9\n]*?\>', name = '\'\</[a-zA-Z_0-9\n]*?\>\'')],[LiteralParser('[^\n]*?(?=\</[a-zA-Z_0-9\n]*?\>|\<[a-zA-Z_0-9\n]*?\>|\n)', name = '\'[^\n]*?(?=\</[a-zA-Z_0-9\n]*?\>|\<[a-zA-Z_0-9\n]*?\>|\n)\'')], name = 'Token')
Space = LiteralParser('\s', name = 'Space')
TagHead = LiteralParser('\<[a-zA-Z_0-9\n]*?\>', name = 'TagHead')
TagEnd = LiteralParser('\</[a-zA-Z_0-9\n]*?\>', name = 'TagEnd')
Cell = LiteralParser('(?!\<[a-zA-Z_0-9\n]*?\>|\</[a-zA-Z_0-9\n]*?\>)[^\n]*', name = 'Cell')
Block = AstParser([Ref('TagHead'),SeqParser([SeqParser([Ref('Space')],[Ref('Cell')],[Ref('Block')], atleast = 1, atmost = 1)]),Ref('TagEnd')], name = 'Block', toIgnore={'Space'})
Module = AstParser([SeqParser([SeqParser([Ref('Space')]),SeqParser([Ref('Block')]),SeqParser([Ref('Space')])])], name = 'Module', toIgnore={'Space'})
Token.compile(namespace, recurSearcher)
Block.compile(namespace, recurSearcher)
Module.compile(namespace, recurSearcher)
