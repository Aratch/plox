#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass
from .expr import Expr

@dataclass(eq=True, frozen=True)
class Stmt(ABC):
    pass

@dataclass(eq=True, frozen=True)
class Block(Stmt):
    statements: list[Stmt]

@dataclass(eq=True, frozen=True)
class Expression(Stmt):
    expression: Expr

@dataclass(eq=True, frozen=True)
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

@dataclass(eq=True, frozen=True)
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

@dataclass(eq=True, frozen=True)
class Print(Stmt):
    expression: Expr

@dataclass(eq=True, frozen=True)
class Return(Stmt):
    keyword: Token
    value: Expr

@dataclass(eq=True, frozen=True)
class Var(Stmt):
    name: Token
    initializer: Expr = None

@dataclass(eq=True, frozen=True)
class While(Stmt):
    condition: Expr
    body: Stmt

@dataclass(eq=True, frozen=True)
class Break(Stmt):
    token: Token

