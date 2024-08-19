#!/usr/bin/env python3

from plox.token import Token
from typing import Self

class Environment:
    def __init__(self, enclosing: Self | None = None):
        self.__values = dict()
        self.enclosing = enclosing

    def define(self, name: str, value):
        self.__values[name] = value

    def assign(self, name: Token, value):
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        from .interpreter import PloxRuntimeError
        raise PloxRuntimeError(name,
                               f"Undefined variable {name.lexeme}.")

    def get(self, name: Token):
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        from .interpreter import PloxRuntimeError
        raise PloxRuntimeError(name,
                               f"Undefined variable '{name.lexeme}'.")
