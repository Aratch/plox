#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Expr(ABC):
    pass

@dataclass(eq=True, frozen=True)
class Assign(Expr):
    name: Token
    value: Expr

@dataclass(eq=True, frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass(eq=True, frozen=True)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

@dataclass(eq=True, frozen=True)
class Grouping(Expr):
    expression: Expr

@dataclass(eq=True, frozen=True)
class Literal(Expr):
    value: object

@dataclass(eq=True, frozen=True)
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass(eq=True, frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass(eq=True, frozen=True)
class Ternary(Expr):
    operator: Token
    condition: Expr
    left: Expr
    right: Expr

@dataclass(eq=True, frozen=True)
class Variable(Expr):
    name: Token

@dataclass(eq=True, frozen=True)
class Lambda(Expr):
    token: Token
    params: list[Token]
    body: 'list[Stmt]'

