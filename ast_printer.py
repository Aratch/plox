#!/usr/bin/env python3

from scanner import Token, TokenType
from expr import Expr, Binary, Grouping, Unary, Literal
from visitor import visitor

class AstPrinter():
    def print(self, expr: Expr):
        return self.visit(expr).strip()

    @visitor(Binary)
    def visit(self, expr: Binary):
        return self.__parenthesize(expr.operator.lexeme,
                                   expr.left, expr.right)

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        return self.__parenthesize("group", expr.expression)

    @visitor(Literal)
    def visit(self, expr: Literal):
        if expr.value == None: return "nil"
        return str(expr.value)

    @visitor(Unary)
    def visit(self, expr: Unary):
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name: str, *exprs: Expr):
        return f" ({name} {''.join(self.visit(expr) for expr in exprs)} )"

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

    printer = AstPrinter()
    print(printer.print(expression))
