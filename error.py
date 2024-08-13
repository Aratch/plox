#!/usr/bin/env python3

from scanner import Token, TokenType

def report(line: int, where: str, message: str):
    print(f"[{line}] Error{where}: {message}")
    had_error = True

def error(obj: int | Token, message: str):
    if isinstance(obj, int):
        line = obj
        report(line, "", message)
    elif isinstance(obj, Token):
        token = obj
        if token.type == TokenType.EOF:
            report(token.line, " at end", message)
        else:
            report(token.line, f" at '{token.lexeme}'", message)
