# -*- coding: utf-8 -*-

#from EBNFParser.ObjRegex.PatternMatching import   Seq, Any,patMatch, multi_pattern, single_pattern
#from EBNFParser.Token import token, Number, Name, String, \
#                              Bracket, Access, END, Op, NEWLINE
#                              
#
#with open('./test.l') as f:
#    s = f.read()
#
#import re
#def reMatch(x, make = lambda x:x):
#    re_ = re.compile(x)
#    def _1(ys):
#        if not ys: return None
#        r = re_.match(ys[0])
#        if not r : return None
#        a, b = r.span()
#        if a!=0 : raise Exception('a is not 0')
#        if b is not len(ys[0]):
#            return None
#        return 1, ys[0]
#    return _1

#name = Any(reMatch(Name))
#_assign = multi_pattern([Any(reMatch('=')), name], name = None)
#assign = multi_pattern([name, Seq(_assign.match)], name = 'assign')
#assign.match(['a','=','b']) ->> print

#import sys
#sys.setrecursionlimit(100)
#
#from EBNFParser.ObjRegex.Match import *
#res = token.findall(s)
#def reMatch(x, make = lambda x:x):
#    re_ = re.compile(x)
#    def _1(y):
#        r = re_.match(y)
#        if not r : return None
#        a, b = r.span()
#        if a!=0 : raise Exception('a is not 0')
#        if b is not len(y):
#            return None
#        return True
#    return dict(f = _1, make = lambda x: re_.findall(x)[0])
#    
#import re



#p = PM([fSeq(reMatch(Number))])
#AttrMatch = PM([fAny(reMatch(Name)), fSeq(lambda x: x=='\n'),'.', fAny(reMatch(Name))])
#
#from copy import deepcopy
#
#
#
#acc = statusMatch([fAny(reMatch(Name)), '.', fAny(reMatch(Name))])
#acc.append(statusMatch(['=>', acc]))
#setMatch = multi_PM([acc,'=',fAny(reMatch(Name))], [fAny(reMatch(Name)),'->', 'end'])
#setMatch.match(['a','.','m','=>','a','.','m','=','a'])
#        
#        

#assign_to_str = multi_pattern([ fAny(**reMatch(Name)), idp('='), fAny(**reMatch(String))])
#multi_call  = fSeq(atleast = 3,**reMatch(Name))
#pm = PM([assign_to_str], [multi_call])
#pm.match(['a','b','c','d']) ->> print

