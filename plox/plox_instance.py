#!/usr/bin/env python3

from .plox_class import PloxClass

class PloxInstance:
    def __init__(self, klass: PloxClass):
        self.klass = klass

    def __str__(self):
        return f"{self.klass} instance"

    def __repr__(self):
        return f"{self.klass} instance"
