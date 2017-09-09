#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thautwarm committed on 5 Jun 2017

@author: misakawa
"""

from collections import Iterable,defaultdict
import re
PMRegex=re.compile('__.*__')
def DefaultReturn(RetDeal=None):
    def outw(func):
        def wrapper(*args,**kwargs):
            try:
                tail=func(*args,**kwargs)
            except:
                return RetDeal
            return tail
        return wrapper
    return outw
class Any:pass
class Seq:pass


class tAny(Any):
    def __init__(self,family=object):
        self.family=family
    def __eq__(self,var):
        if isinstance(var,Any):
            return var.family==self.family
        return isinstance(var,self.family)
    def __hash__(self):
        return hash((self.family,...))
    
class tSeq(Seq,tAny):
    def __init__(self,family=object,atleast=0):
        self.family=family
        self.least=atleast


class fAny(Any):
    def __init__(self, func=lambda x:x):
        self.func = func
    def __eq__(self,var):
        return self.func(var)
    def __hash__(self):
        return hash((self.func ,...))
    
class fSeq(Seq, fAny):
    def __init__(self, func=lambda x,y:x==y,atleast=0):
        self.func=func
        self.least=atleast
        

    
    
def AlgebraDiv(iterator,func):
    subStructures=defaultdict(set)
    for item in iterator:
        subStructures[func(item)].add(item)
    return subStructures
#@DefaultReturn(RetDeal=False)   
def patMatch(val,var,partial = False):
    
    if isinstance(val,Iterable) and not issubclass(val.__class__,str):
        try:
#============================================================
            # Set
            if issubclass(val.__class__,set):
                
                subStructures=AlgebraDiv(val,
                    lambda item: isinstance(item,Any))
                
                NormalDefined,GeneralDefined =subStructures[False],subStructures[True]
                
                judge_one= len(NormalDefined&var)== len(NormalDefined)
                
                if not judge_one:return False
                
                for idx,item in enumerate(var):
                    toRemove=None.__class__
                    for val_i in val: 
                        if patMatch(val_i,item,partial=partial):
                            toRemove=val_i
                            break
                    if toRemove!=None.__class__:
                        val.remove(val_i)
                        continue
                    
                    #there is not any instance of "Any", however there is atleast 1 item left in "var".
                    if not GeneralDefined:return True if partial else False

                    toRemove=None.__class__
                    for genItem in GeneralDefined:
                        if genItem==item:
                            toRemove=genItem
                            break
                    if toRemove!=None.__class__:
                        GeneralDefined.remove(toRemove)
                    else:
                        # An item does not match any instance of "Any" left,
                        #       which means the "val"  not equaled with "var".
                        if not partial:
                            return False
                return not GeneralDefined and (True if partial else (idx+1)==len(var))
#=============================================================
            #Dict
            elif issubclass(val.__class__,dict):
                if not partial and len(val.keys())!=len(var.key()):
                    return False
                for key in val.keys():
                    if not patMatch(val[key],var[key],partial=partial):
                        return False
                return True
#=============================================================
            # Iterator Except str
            else:
                if len(val)==0 :
#                    print(1,val,var)
                    return len(val)==0 and len(var)==0
                elif isinstance(val[0],Seq):
                    catchNum = 0
                    for var_i in var:
                        if val[0] == var_i:
                            catchNum += 1
                        else:
                            break
                    if catchNum>=val[0].least:
#                        print(2.1)
                        return patMatch(val[1:],var[catchNum:],partial=partial)
                    else:
#                        print(2.2)
                        return False
                elif isinstance(val[0],Iterable) and not issubclass(val[0].__class__,str):
#                    print(3)
                    return patMatch(val[0],var[0],partial=partial) and patMatch(val[1:],var[1:],partial=partial)
                else:
#                    print(4)
                    return False if not patMatch(val[0],var[0],partial=partial) \
                                    else patMatch(val[1:],var[1:],partial=partial)
                







#=====================================================
        except Exception as e:
            print(e)
            return False
            
    else:
        
        for type_i in (str,int,float,bool,bytes,complex,Any):
            if issubclass(val.__class__,type_i):
                return val==var
                
        attrs=list(filter(lambda x:not PMRegex.findall(x) ,dir(val)))
        if not partial:
            attrsVar=list(filter(lambda x:not PMRegex.findall(x) ,dir(var)))
            if set(attrs)&set(attrsVar)!= len(attrs):
                return False
        for attr in attrs:
            
            if  not (hasattr(var,attr) and (getattr(var,attr)==getattr(val,attr) or
                                     getattr(var,attr).__class__==getattr(val,attr).__class__) ):
                return False
        return True
    
class PatternMatching:
    def __init__(self,matchvalue):
        self.matchvalue=matchvalue
    def match(self,value,partial=False):
        return patMatch(self.matchvalue, value, partial)

PM=PatternMatching

if True:
  class sample:
    def __init__(self,a,b,c):
      self.a=a
      self.b=b
      self.c=c
    def dosome(self):pass