from collections import defaultdict
from functools import reduce
from typing import List, Dict, Type, TypeVar, Callable, Iterable

T = TypeVar("T")
S = TypeVar("S")
K = TypeVar("K")




def andthen(*func_stack:List[Callable[[T],T]]) -> Callable[[T], T]:
    def _1(*args, **kwargs) -> T:
        for func in func_stack:
            try:
                mid=func(mid)
            except NameError:
                mid=func(*args, **kwargs)
        return mid

    return _1
def _andthen2(func1:Callable[[T],S], func2:Callable[[S],K])->Callable[[T],K]:
    def _1(*args, **kwargs) -> K:
        return func1(func2(*args, **kwargs))
    return _1
andthen.dual = _andthen2




def compose(*func_stack):
    def _1(*args, **kwargs):
        for func in func_stack[::-1]:
            try:
                mid=func(mid)
            except NameError:
                mid=func(*args, **kwargs)
        return mid

    return _1

def _compose2(func1:Callable[[S],K], func2:Callable[[T],S])->Callable[[T],K]:
    def _1(*args, **kwargs) -> K:
        return func2(func1(*args, **kwargs))
    return _1
compose.dual = _compose2


def foreach(f: object) -> callable:
    def _1(self):
        for item in self:
            f(item)

    return _1


def groupBy(func : callable) -> defaultdict(list):
    def _1(self):
        that=defaultdict(list)
        foreach(lambda item: that[func(item)].append(item)) \
            (self)
        return that
    return _1

def flatten(seq: Iterable[Iterable[T]])-> Iterable[T]:
    def _f(_seq):
        for item in _seq:
            if not isinstance(item, list):
                yield item
            else:
                yield from _f(item)
    return _f(seq)


def _flatten(seq: list):
    """
    this is the implementation of function flatten without recursion.
    """
    head=[]
    tmp=seq
    idx=[0]
    while True:
        try:
            item=tmp[idx[-1]]
        except IndexError:
            try:
                tmp=head.pop()
                idx.pop()
                continue
            except IndexError:
                break
        idx[-1]+=1
        if not isinstance(item, list):
            yield item
        else:
            head.append(tmp)
            tmp=item
            idx.append(0)

def __flatten(seq: list):
    """
    this is the implementation of function flatten without recursion.
    """
    head=[]
    store=[]
    tmp=seq
    idx=[0]
    while True:
        try:
            item=tmp[idx[-1]]
        except IndexError:
            try:
                tmp=head.pop()
                idx.pop()
                continue
            except IndexError:
                break
        idx[-1]+=1
        if not isinstance(item, list):
            store.append(item)
        else:
            head.append(tmp)
            tmp=item
            idx.append(0)
    return store



class fn:
    @staticmethod
    def map(f : Callable[[T], S])->Callable[[Iterable[T]], Iterable[S]]:
        def _1(*args : Iterable[Iterable[T]]) -> Iterable[S]:
            return map(f, *args)
        return _1

    @staticmethod
    def filter(f : Callable[[T], bool])->Callable[[Iterable[T]], Iterable[T]]:
        def _1(*args: List[Iterable[T]]) -> Iterable[T]:
            return filter(f, *args)
        return _1
    @staticmethod
    def reduce(f:Callable[[T,T], S]) -> Callable[[Iterable[T]], S]:
        def _1(*args: List[Iterable[T]]) -> S:
            return reduce(f, *args)
        return _1

    @staticmethod
    def flatMap(f:Callable[[T],S]) -> Callable[[Iterable[Iterable[T]]], Iterable[S]]:
        return _andthen2(flatten, fn.map(f))


flatten.noRecur = _flatten
flatten.noRecur.strict = __flatten




