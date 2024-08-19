#!/usr/bin/env python3

from plox.token import Token


class Environment:
    def __init__(self):
        self.__values = dict()

    def define(self, name: str, value):
        self.__values[name] = value

    def assign(self, name: Token, value):
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return

        from .interpreter import PloxRuntimeError
        raise PloxRuntimeError(name,
                               f"Undefined variable {name.lexeme}.")

    def get(self, name: Token):
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        from .interpreter import PloxRuntimeError
        raise PloxRuntimeError(name,
                               f"Undefined variable '{name.lexeme}'.")
