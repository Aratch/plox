#!/usr/bin/env python3

def report(line: int, where: str, message: str):
    print(f"[{line}] Error{where}: {message}")
    had_error = True

def error(line: int, message: str):
    report(line, "", message)
