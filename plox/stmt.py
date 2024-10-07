#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass
from .expr import Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Stmt(ABC):
    pass

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Block(Stmt):
    statements: list[Stmt]

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Class(Stmt):
    name: Token
    methods: list['Function']

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Expression(Stmt):
    expression: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Print(Stmt):
    expression: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Return(Stmt):
    keyword: Token
    value: Expr

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Var(Stmt):
    name: Token
    initializer: Expr = None

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class While(Stmt):
    condition: Expr
    body: Stmt

@dataclass(eq=False, frozen=True, unsafe_hash=True)
class Break(Stmt):
    token: Token

