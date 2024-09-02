#!/usr/bin/env python

import sys
import readline

from .stmt import Stmt
from .interpreter import Interpreter
from .parser import Parser
from .ast_printer import AstPrinter
from .token import Token
from .scanner import Scanner
from .resolver import Resolver
from .expr import Expr
from .error import *

class Plox:
    had_error = False
    had_runtime_error = False
    interpreter = None

    def run(self, source: str, in_repl = False):
        scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        parser = Parser(tokens)

        statements: list[Stmt] = []
        expr: Expr | None = None

        # XXX: This assumes single lines
        # FIXME: This bugs, obviously. As expected from bad design, see note above.
        if in_repl:
            if source.strip().endswith(";"):
                statements: list[Stmt] = parser.parse()
            else:
                expr: Expr | None = parser.parse_single_expr()
        else:
            statements: list[Stmt] = parser.parse()

        if not Plox.interpreter:
            Plox.interpreter = Interpreter()

        if Plox.had_error:
            return

        resolver = Resolver(Plox.interpreter)

        # Make pyright shut the hell up
        if statements:
            resolver.resolve(statements)
            Plox.interpreter.interpret(statements)

        elif expr:
            # NOTE: Ignore this for now
            print(Plox.interpreter.evaluate(expr))

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
