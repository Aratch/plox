#!/usr/bin/env python3
from typing import Any
from abc import ABCMeta, abstractmethod

# NOTE: Might replace with typing.Protocol down the line

class PloxCallable(metaclass=ABCMeta):

    methods = ["call", "arity"]

    @abstractmethod
    def arity(self) -> int:
        return NotImplemented

    # just duck-type the interpreter, goddammit
    @abstractmethod
    def call(self, interpreter, arguments: list) -> Any:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return all((
            hasattr(subclass, m) \
            and callable(subclass.__dict__[m])) \
            for m in PloxCallable.methods
                   )
