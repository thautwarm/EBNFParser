#

from collections import deque, Iterable
class recur:pass
class node:
    def __init__(self, data):
        self.info     = dict(no_rec_s = []) 
        self.children = deque()
        self.parent   = None
    
    def setP(self, parent):
        self.parent = parent
        return self
    
    def append(self, data):
        self.children.append(node(data).setP(self))
        return self
    
    def appendLeft(self,data):
        self.children.appendLeft(node(data).setP(self))
        return self        
    
    def match(self, obj_s):
        
        if isinstance(obj_s, Iterable):
            objs = obj_s
            if isinstance(self.children, node):
                for child in self.children:
                    r = child.match(objs)
                    if r:
                        return r
        else:
            if not self.info['no_rec_s'] : return None
            obj  = obj_s
            for no_rec in self.info['no_rec_s']:
                r =  no_rec.match(obj)
                if r:
                    return r

            
        


    
    

    