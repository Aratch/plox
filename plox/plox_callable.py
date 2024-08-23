#!/usr/bin/env python3
from typing import Any
from abc import ABCMeta, abstractmethod
from time import time

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

    def __str__(self) -> str:
        return "<native fn>"

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return all((
            hasattr(subclass, m) \
            and callable(subclass.__dict__[m])) \
            for m in PloxCallable.methods
                   )


# TODO: Figure out if I should do native funcs like this or not

class PloxFnClock():
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments: list) -> Any:
        return time()
