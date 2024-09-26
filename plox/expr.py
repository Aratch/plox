#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Expr(ABC):
    pass

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Assign(Expr):
    name: Token
    value: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Grouping(Expr):
    expression: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Literal(Expr):
    value: object

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Ternary(Expr):
    operator: Token
    condition: Expr
    left: Expr
    right: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Variable(Expr):
    name: Token

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Lambda(Expr):
    token: Token
    params: list[Token]
    body: 'list[Stmt]'

