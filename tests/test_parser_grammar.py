#!/usr/bin/env python3

import unittest

from plox.token import TokenType, Token
from plox.scanner import Scanner
from plox.parser import Parser
from plox.expr import *
from plox.ast_matcher import AstMatcher


globals().update(TokenType.__members__)

matcher = AstMatcher()

class TestParserGrammar(unittest.TestCase):
    def parse_expression(self, source: str) -> Expr | None:
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        parser = Parser(tokens)
        expression: Expr | None = parser.parse()
        return expression

    def test_string_literal(self):
        actual = self.parse_expression('"foo"')
        expected = Literal("foo")
        self.assertIsNotNone(actual)
        self.assertTrue(matcher.match(actual, expected),
                         f"Expr's not matching\nExpected: {expected}\nActual: {actual}")

if __name__ == "__main__":
    unittest.main()
