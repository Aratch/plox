#!/usr/bin/env python3
from typing import Any
from abc import ABCMeta, abstractmethod
from time import time

from .exceptions import PloxReturnException

from .environment import Environment
from .stmt import *

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

class PloxFunction(PloxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"

    def call(self, interpreter, arguments: list) -> Any:
        environment = Environment(interpreter.globals)

        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except PloxReturnException as return_exception:
            return return_exception.value

        return None # NOTE: Return values will be coming later


# TODO: Figure out if I should do native funcs like this or not

class PloxFnClock():
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments: list) -> Any:
        return time()
