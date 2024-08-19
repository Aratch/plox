#!/usr/bin/env python

import sys
import readline

from .stmt import Stmt
from .interpreter import Interpreter
from .parser import Parser
from .ast_printer import AstPrinter
from .token import Token
from .scanner import Scanner
from .expr import Expr
from .error import *

class Plox:
    had_error = False
    had_runtime_error = False
    interpreter = None

    def run(self, source: str):
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        parser = Parser(tokens)
        statements: list[Stmt] = parser.parse()

        if not Plox.interpreter:
            Plox.interpreter = Interpreter()

        if Plox.had_error:
            return

        # Make pyright shut the hell up
        if statements:
            # print(AstPrinter().print(expression))
            Plox.interpreter.interpret(statements)

    def run_file(self, path: str):
        with open(path, "r") as f:
            source = f.read()
            self.run(source)

            if Plox.had_error: sys.exit(65)
            if Plox.had_runtime_error: sys.exit(70)

    def run_prompt(self):
        while True:
            try:
                line : str = input("> ")
                if line == "": break
                self.run(line)
                Plox.had_error = False
            except EOFError:
                sys.exit(0)
