#!/usr/bin/env python

from .token import Token, TokenType
from .expr import Expr, Binary, Grouping, Unary, Literal, Ternary
from .visitor import visitor

def is_truthy(obj):
    if obj == None: return False
    # Redundant cast, but whatever
    if isinstance(obj, bool): return bool(obj)
    return True

def is_equal(a, b):
    # This might be superfluous because we don't run the risk of
    # causing a null pointer dereference like in Java
    if a is None and b is None: return True
    if a is None: return False

    return a == b

class Interpreter:
    def evaluate(self, expr: Expr):
        return self.visit(expr)

    @visitor(Literal)
    def visit(self, expr: Literal):
        return expr.value

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        self.evaluate(expr.expression)

    @visitor(Unary)
    def visit(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return -float(right)
            case TokenType.BANG:
                return not is_truthy(right)

        # Unreachable
        return None

    @visitor(Binary)
    def visit(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)

            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.STAR:
                return float(left) * float(right)

            case TokenType.BANG_EQUAL: return False
            case TokenType.EQUAL_EQUAL: return True

        # Unreachable
        return None
