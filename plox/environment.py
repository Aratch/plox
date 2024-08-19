#!/usr/bin/env python3

from plox.token import Token


class Environment:
    def __init__(self):
        self.__values = dict()

    def define(self, name: str, value):
        self.__values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        from plox.interpreter import PloxRuntimeError
        raise PloxRuntimeError(name,
                               f"Undefined variable '{name.lexeme}'.")
