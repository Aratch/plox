#!/usr/bin/env python3

from .plox_callable import PloxCallable

class PloxClass(PloxCallable):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def call(self, interpreter, arguments: list) -> object:
        from .plox_instance import PloxInstance
        instance: PloxInstance = PloxInstance(self)
        return instance

    def arity(self) -> int:
        return 0
