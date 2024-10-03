#!/usr/bin/env python3

import unittest
from plox.ast_printer import AstPrinter
from plox.token import TokenType, Token
from plox.scanner import Scanner
from plox.parser import Parser
from plox.expr import *
from plox.ast_matcher import AstMatcher

from .nostderr import nostderr

globals().update(TokenType.__members__)

matcher = AstMatcher()
printer = AstPrinter()

def mismatch(actual, expected):
    msg = f"""
Expr's not matching
Expected:\n{expected} {printer.print(expected)}
Actual:\n{actual} {printer.print(actual)}"""
    return msg

@unittest.skip("Skip until eq() issues are resolved")
class TestParserGrammar(unittest.TestCase):
    def parse_expression(self, source: str) -> Expr | None:
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        parser = Parser(tokens)
        expression: Expr | None = parser.parse_single_expr()
        return expression

    def test_string_literal(self):
        literal = '"foo"'
        actual = self.parse_expression(literal)
        expected = Literal(literal.strip("\""))
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    def test_numeric_literal(self):
        literal = '42'
        actual = self.parse_expression(literal)
        # XXX: lox is like js: all numbers are floats
        expected = Literal(float(literal))
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    def test_unary(self):
        source = "-1.0"
        actual = self.parse_expression(source)
        expected = Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(1.0)
        )
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    def test_binary(self):
        source = "1.0 + 2.0"
        actual = self.parse_expression(source)
        expected = Binary(
            Literal(1.0),
            Token(TokenType.PLUS, "+", None, 1),
            Literal(2.0)
        )
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    def test_grouped_expression(self):
        source = "-123 * (45.67)"
        actual = self.parse_expression(source)
        expected = Binary(
            Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Literal(123.0)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(
                Literal(45.67)
            )
        )
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    def test_grouped_complex_expression(self):
        source = "-123 * (45.67 + 2.0)"
        actual = self.parse_expression(source)
        expected = Binary(
            Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Literal(123.0)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(
                Binary(Literal(45.67),
                       Token(TokenType.PLUS, "+", None, 1),
                       Literal(2.0))

            )
        )
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    def test_parse_errors(self):
        maligned = ["!", ".3", "(", ","]
        results = []
        with nostderr():
            for source in maligned:
                results.append(self.parse_expression(source) == None)
            self.assertTrue(results != [])
            self.assertTrue(all(results))

    @unittest.skip("Not implemented yet")
    def test_sequential_comma_operator(self):
        source = "1.0 , 2.0"
        actual = self.parse_expression(source)
        expected = Binary(
            Literal(1.0),
            Token(TokenType.COMMA, ",", None, 1),
            Literal(2.0)
        )
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    @unittest.skip("Not implemented yet")
    def test_ternary_conditional(self):
        source = "2 == 1 ? 2 + 1 : 2 * 2"
        actual = self.parse_expression(source)
        expected = Ternary(
            Token(TokenType.QUESTION_MARK, "?", None, 1),
            Binary(Literal(2.0),
                   Token(TokenType.EQUAL_EQUAL, "==", None, 1),
                   Literal(1.0)),
            Binary(Literal(2.0),
                   Token(TokenType.PLUS, "+", None, 1),
                   Literal(1.0)),
            Binary(Literal(2.0),
                   Token(TokenType.STAR, "*", None, 1),
                   Literal(2.0))
        )
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                        mismatch(actual, expected))

    def test_discard_malformed_binary(self):
        # https://stackoverflow.com/a/61533524
        import io
        import contextlib

        f = io.StringIO()

        source = "+ 2"

        with contextlib.redirect_stderr(f):
            actual = self.parse_expression(source)

        self.assertIsNone(actual)
        self.assertRegex(f.getvalue(),
                            "Error at '\+'")
        self.assertRegex(f.getvalue(),
                            "Expected left-hand side")

if __name__ == "__main__":
    unittest.main()
