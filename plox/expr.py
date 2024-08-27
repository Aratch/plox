#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass

class Expr(ABC):
    pass

@dataclass
class Assign(Expr):
    name: Token
    value: Expr

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Literal(Expr):
    value: object

@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

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

@dataclass
class Lambda(Expr):
    token: Token
    params: list[Token]
    body: 'list[Stmt]'

