#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass

class Expr(ABC):
    pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Literal(Expr):
    value: object

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass
class Ternary(Expr):
    operator: Token
    condition: Expr
    left: Expr
    right: Expr

@dataclass
class Variable(Expr):
    name: Token

