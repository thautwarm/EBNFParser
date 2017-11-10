#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 21:10:08 2017

@author: misakawa
"""

import numba as nb

class Node:
    def __init__(self, content = None):
        self.next = None
        self.content = content
    def __str__(self):
        return self.content.__str__()
    def __repr__(self):
        return self.content.__str__()
    
    
class LinkedList:
    def __init__(self, headEnd = None):
        if headEnd:
            self.head, self.end = headEnd
        else:
            self.head = None
            self.end  = None
    @nb.autojit
    def appendNode(self, node):
        try:
            self.end.next = node
        except AttributeError:
            self.head = self.end = node
        self.end = node
    @nb.autojit
    def append(self, v):
        self.appendNode(Node(v))
    @nb.autojit
    def appendLeftNode(self, node):
        node.next = self.head
        self.head = node
        if self.end is None:
            self.end = node
    @nb.autojit
    def appendLeft(self, v):
        self.appendLeftNode(Node(v))

    def extend(self, linkedlist):
        self.end.next = linkedlist.head
        self.end      = linkedlist.end
    
    def extendLeft(self, linkedlist):
        linkedlist.end.next = self.head
        self.head           = linkedlist.head
    
    def __iter__(self):
        if self.head is None:return None
        else:
            n = self.head
            while n.next:
                yield n
                n = n.next
            yield n
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return [n for n in self].__str__()
    
            
        
        
    @property
    def tail(self):
        return LinkedList(headEnd=(self.head.next, self.end) \
                                  if self.head is not self.end else None)
        
            
            
    
        
        
        
    
    
    
    
    



if __name__ == '__main__':
    
    pass
