#!/usr/bin/env python3

from plox.token import Token
from typing import Self, Any

class Environment:
    def __init__(self, enclosing: Self | None = None):
        self.values = dict()
        self.enclosing = enclosing

    def define(self, name: str, value):
        self.values[name] = value

    def get_at(self, distance: int, name: str):
        return self.ancestor(distance).values.get(name)

    def ancestor(self, distance: int):
        environment: Environment = self
        for i in range(distance):
            environment = environment.enclosing

        return environment

    def assign(self, name: Token, value):
        from .interpreter import PloxRuntimeError

        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

            # CAVEAT: Redundant?
            # if self.enclosing:
            #     self.enclosing.assign(name, value)
            #     return

        raise PloxRuntimeError(name,
                               f"Undefined variable {name.lexeme}.")

    def assign_at(self, distance: int, name: Token, value: Any):
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, name: Token):
        from .interpreter import PloxRuntimeError, Uninitialized

        if name.lexeme in self.values:
            if self.values[name.lexeme] == Uninitialized:
                raise PloxRuntimeError(name,
                                       f"Uninitialized variable '{name.lexeme}'")
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        raise PloxRuntimeError(name,
                               f"Undefined variable '{name.lexeme}'.")
