#!/usr/bin/env python

import sys
import readline
from .parser import Parser
from .ast_printer import AstPrinter
from .token import Token
from .scanner import Scanner
from .expr import Expr
from .error import *

class Plox:
    def __init__(self):
        self.had_error : bool = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        parser = Parser(tokens)
        expression: Expr | None = parser.parse()

        if self.had_error:
            return

        # Make pyright shut the hell up
        if expression:
            print(AstPrinter().print(expression))

    def run_file(self, path: str):
        with open(path, "r") as f:
            source = f.read()
            self.run(source)

            if self.had_error: sys.exit(65)

    def run_prompt(self):
        while True:
            line : str = input("> ")
            if line == "": break
            self.run(line)
            self.had_error = False
