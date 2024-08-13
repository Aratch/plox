#!/usr/bin/env python3

import sys
import readline
from plox.parser import Parser
from plox.ast_printer import AstPrinter
from plox.token import Token
from plox.scanner import Scanner
from plox.expr import Expr
from plox.error import *

had_error : bool = False

def run(source: str):
    scanner = Scanner(source)
    tokens: list[Token] = scanner.scan_tokens()
    parser = Parser(tokens)
    expression: Expr | None = parser.parse()

    if had_error:
        return

    # Make pyright shut the hell up
    if expression:
        print(AstPrinter().print(expression))

def run_file(path: str):
    with open(path, "r") as f:
        source = f.read()
        run(source)

        if had_error: sys.exit(65)

def run_prompt():
    while True:
        line : str = input("> ")
        if line == "": break
        run(line)
        had_error = False

def main(argv: list):
    if len(argv) > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(argv) == 1:
        run_file(argv[0])
    else:
        run_prompt()

if __name__ == '__main__':
    main(sys.argv[1:])
