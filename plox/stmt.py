#!/usr/bin/env python3

from abc import ABC
from .token import Token
from dataclasses import dataclass
from .expr import Expr

class Stmt(ABC):
    pass

@dataclass
class Block(Stmt):
    statements: list[Stmt]

@dataclass
class Expression(Stmt):
    expression: Expr

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

@dataclass
class Print(Stmt):
    expression: Expr

@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr = None

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

@dataclass
class Break(Stmt):
    token: Token

