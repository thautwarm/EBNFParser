
from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo
from etoken import token 
import re
namespace     = globals()
recurSearcher = set()
type = LiteralParser('t', name = 'type')
prefix = AstParser([Ref('ex'),LiteralParser('(', name='\'(\''),SeqParser([Ref('ex')]),LiteralParser(')', name='\')\'')],[Ref('ex'),LiteralParser('=>', name='\'=>\''),Ref('ex')],[Ref('type')], name = 'prefix')
ex = AstParser([Ref('ex'),LiteralParser(':', name='\':\''),Ref('ex')],[Ref('prefix')], name = 'ex')
prefix.compile(namespace, recurSearcher)
ex.compile(namespace, recurSearcher)
