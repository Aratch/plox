#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass
from .expr import Expr

class Stmt(ABC):
    pass

@dataclass
class Expression(Stmt):
    expression: Expr

@dataclass
class Print(Stmt):
    expression: Expr

