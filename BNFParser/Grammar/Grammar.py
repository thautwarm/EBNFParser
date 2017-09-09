#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 21:01:53 2017

@author: misakawa
"""


from ..graminit import Atoms, Grammar,strict




Ast = Grammar(
        id       =  'Ast',
        match    =  None,
        children =  {
                0:Grammar(
                        id       = 'Expr',
                        match    = None,
                        children = {
                                
                                
                                }
                        
                ),
                1:Grammar(
    
                        
                )
                }
        
        
            
    )




