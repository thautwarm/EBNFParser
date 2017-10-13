
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
from etoken import token 
import re
namespace     = globals()
recurSearcher = set()
type = LiteralParser.Eliteral('t', name = 'type')
prefix = AstParser([Ref('ex'),LiteralParser.Eliteral('(', name = '\'(\''),SeqParser([Ref('ex')]),LiteralParser.Eliteral(')', name = '\')\'')],[Ref('ex'),LiteralParser.Eliteral('=>', name = '\'=>\''),Ref('ex')],[Ref('type')], name = 'prefix')
ex = AstParser([Ref('ex'),LiteralParser.Eliteral(':', name = '\':\''),Ref('ex')],[Ref('prefix')], name = 'ex')
prefix.compile(namespace, recurSearcher)
ex.compile(namespace, recurSearcher)
