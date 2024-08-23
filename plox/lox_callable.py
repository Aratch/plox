#!/usr/bin/env python3
from abc import ABCMeta

class PloxCallable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return(hasattr(subclass, 'call') and
               callable(subclass.call))
