#!/usr/bin/env python3

from .token import Token, TokenType
from .expr import Expr, Binary, Grouping, Unary, Literal, Ternary
from .visitor import visitor

class AstMatcher:
    def match(self, left: Expr, right: Expr):
        return self.visit(left) == self.visit(right)


    @visitor(Ternary)
    def visit(self, expr: Ternary): #pyright: ignore
        return expr.operator.lexeme, \
            self.visit(expr.condition), \
            self.visit(expr.left), \
            self.visit(expr.right) #pyright: ignore

    @visitor(Binary)
    def visit(self, expr: Binary): #pyright: ignore
        return expr.operator.lexeme, self.visit(expr.left), self.visit(expr.right) #pyright: ignore

    @visitor(Grouping)
    def visit(self, expr: Grouping): #pyright: ignore
        return "group", expr.expression

    @visitor(Literal)
    def visit(self, expr: Literal): #pyright: ignore
        value = "nil" if expr.value == None else expr.value
        return "literal", value

    @visitor(Unary)
    def visit(self, expr: Unary): #pyright: ignore
        return expr.operator.lexeme, self.visit(expr.right) #pyright: ignore

if __name__ == "__main__":
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )
    expression2 = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    expression3 = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal("foo")
        )
    )

    matcher = AstMatcher()
    print(matcher.match(expression, expression2))
    print(matcher.match(expression, expression3))
