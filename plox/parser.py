#!/usr/bin/env python3

from .error import error
from .token import Token, TokenType
from .expr import *
from .stmt import *
from typing import Callable

globals().update(TokenType.__members__)

class ParseError(RuntimeError):
    pass

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens : list[Token] = tokens
        self.current : int = 0

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []

        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    # TODO: Delete this at some point
    def parse_single_expr(self) -> Expr | None:
        try:
            return self.expression()
        except ParseError:
            return None

    def is_at_end(self):
        return self.peek().type == EOF

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]


    ## Statement parsing

    def declaration(self) -> Stmt:
        try:
            if self.match(VAR):
                return self.var_declaration()

            return self.statement()
        except ParseError as error:
            self.synchronize()
            return None

    def var_declaration(self) -> Stmt:
        name : Token = self.consume(IDENTIFIER, "Expected variable name.")

        initializer : Expr = None
        if self.match(EQUAL):
            initializer = self.expression()

        self.consume(SEMICOLON, "Expected ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(PRINT):
            return self.print_statement()
        if self.match(LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def block(self) -> list[Stmt]:
        statements: list[Stmt] = []

        while not self.check(RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def print_statement(self):
        value: Expr = self.expression()
        self.consume(SEMICOLON, "Expected ';' after value.")
        return Print(value)

    def expression_statement(self):
        expr: Expr = self.expression()
        self.consume(SEMICOLON, "Expected ';' after expression.")
        return Expression(expr)

    ## Expression parsing

    def expression(self) -> Expr:
        # DONE: Restore this to sidestep potentially problematic sequence operator
        # (this broke the tests, but oh well)
        # return self.equality()
        return self.assignment()
        # XXX: Restore call to self.sequence() when I'm sure that
        # the textbook implementation is actually working
        # return self.sequence()


    # TODO: Check if a functional generator would even make sense
    # def __binary(self, rule, preceding, tokens) -> Callable:
    #     def fun():
    #         expr = Expr()
    #         right = Expr()
    #     return fun

    def sequence(self) -> Expr:
        # XXX: Restore direct calls to self.equality() 
        expr : Expr = self.ternary()

        while self.match(COMMA):
            operator : Token = self.previous()
            right : Expr = self.ternary()
            expr = Binary(expr, operator, right)

        return expr

    def assignment(self) -> Expr:
        expr: Expr = self.equality()

        if self.match(EQUAL):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            error(equals, "Invalid assignment target.")

        return expr

    # XXX: Require + 2.0s from plox.expr import Ternary
    # *and* regenerate ast
    def ternary(self) -> Expr:
        expr : Expr = self.equality()

        # If the next operator is a question mark
        while self.match(QUESTION_MARK):
            operator: Token = self.previous()
            condition : Expr = self.expression()
            if self.match(COLON):
                right : Expr = self.ternary()
                expr = Ternary(operator, expr, condition, right)
            else:
                raise self.error(self.peek(), "Expected colon in ternary expression.")
        return expr

    def equality(self) -> Expr:
        expr : Expr = self.comparison()

        while self.match(BANG_EQUAL, EQUAL_EQUAL):
            operator : Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr : Expr = self.term()

        while self.match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL):
            operator : Token = self.previous()
            right : Expr = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr : Expr = self.factor()

        while self.match(MINUS, PLUS):
            operator : token = self.previous()
            right : Expr = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(SLASH, STAR):
            operator: Token = self.previous()
            right : expr = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(BANG, MINUS):
            operator : Token = self.previous()
            right : Expr = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(FALSE):
            return Literal(False)
        if self.match(TRUE):
            return Literal(True)
        if self.match(NIL):
            return Literal(None)
        if self.match(NUMBER, STRING):
            return Literal(self.previous().literal)
        if self.match(IDENTIFIER):
            return Variable(self.previous())

        if self.match(LEFT_PAREN):
            expr : Expr = self.expression()
            self.consume(RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)


        binary_operators = set([COMMA, BANG_EQUAL, EQUAL_EQUAL,
                                GREATER, GREATER_EQUAL, LESS, LESS_EQUAL,
                                MINUS, PLUS,
                                SLASH, STAR])

        for op in binary_operators:
            if self.match(op):
                operator_token = self.previous()
                expr = self.expression() # will be discarded?
                raise self.error(
                    operator_token,
                    f"Expected left-hand side of binary operator {operator_token.lexeme}."
                )

        raise self.error(self.peek(), "Expected expression.")

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> Exception:
        error(token, message)
        return ParseError()

    def match(self, *types : TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == SEMICOLON: return

            match self.peek().type:
                case TokenType.CLASS | \
                    TokenType.FUN | \
                    TokenType.VAR | \
                    TokenType.FOR | \
                    TokenType.IF | \
                    TokenType.WHILE | \
                    TokenType.PRINT | \
                    TokenType.RETURN: # pyright: ignore
                    return
                case _:
                    pass

            self.advance()
